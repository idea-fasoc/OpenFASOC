"""
train.py  –  Supervised fine-tuning script for code-fix datasets with LoRA.

Dataset format (JSON per line or list of JSON objects):
{
  "filename": "example.py",
  "analysis": [
    {
      "issue": "Brief description of issue #1",
      "explanation": {
        "problem": "What exactly is wrong?",
        "reason": "Why it's a problem",
        "fix": "How to fix it"
      }
    }
  ],
  "fixed_code": "<full corrected code>"
}

The script builds an input prompt from the first analysis item:
INPUT  =  "Filename: {filename}\nIssue: {issue}\nProblem: {problem}\nReason: {reason}\n### Fix:\n"
OUTPUT =  "{fix}\n\n### Fixed Code:\n{fixed_code}"

It then fine-tunes a causal-LM so that it learns to generate OUTPUT
conditioned on INPUT using LoRA (Low-Rank Adaptation) for memory efficiency.

LoRA Configuration
------------------
Use --lora_r to set the rank (default: 16, higher = more capacity)
Use --lora_alpha to set the scaling factor (default: 32, typically 2x lora_r)
Use --use_8bit to enable 8-bit quantization for even lower memory usage
The script saves both the LoRA adapter and a merged model for inference.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import gc
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

import torch
from torch.utils.data import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    TaskType,
    PeftModel,
)

# GPU memory optimization
os.environ.setdefault("WANDB_SILENT", "true")
os.environ.setdefault("WANDB_CONSOLE", "off")
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True,max_split_size_mb:256"

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Supervised fine-tune a causal LM on code-fix dataset")

    parser.add_argument("--train_file", type=str, required=True, help="Path to training data (.jsonl or .json)")
    parser.add_argument("--eval_file", type=str, default=None, help="Optional evaluation data path")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to store checkpoints")

    parser.add_argument(
        "--model_paths",
        type=str,
        nargs="+",
        required=True,
        help="One or more local directories or model identifiers to fine-tune sequentially (e.g. ./7b/final_model ./13b/final_model)",
    )
    parser.add_argument("--max_length", type=int, default=1024, help="Max sequence length")

    # LoRA Configuration (NEW - replaces full weight training)
    parser.add_argument("--use_lora", action="store_true", default=True, help="Use LoRA for efficient fine-tuning (default: True)")
    parser.add_argument("--lora_r", type=int, default=16, help="LoRA rank (8-64, higher = more capacity)")
    parser.add_argument("--lora_alpha", type=int, default=32, help="LoRA alpha scaling (typically 2x lora_r)")
    parser.add_argument("--lora_dropout", type=float, default=0.05, help="LoRA dropout rate")
    parser.add_argument(
        "--lora_target_modules",
        type=str,
        nargs="+",
        default=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        help="Modules to apply LoRA to (for CodeLlama/Llama)",
    )
    parser.add_argument("--use_8bit", action="store_true", default=False, help="Use 8-bit quantization for lower memory")

    # Training hyper-params (optimized for LoRA)
    parser.add_argument("--per_device_train_batch_size", type=int, default=None, help="Auto-set based on GPU memory if not specified")
    parser.add_argument("--per_device_eval_batch_size", type=int, default=2)
    parser.add_argument("--learning_rate", type=float, default=2e-4, help="Learning rate for LoRA (higher than full FT)")
    parser.add_argument("--num_train_epochs", type=int, default=3)
    parser.add_argument("--gradient_accumulation_steps", type=int, default=None, help="Auto-set based on GPU memory if not specified")
    parser.add_argument("--logging_steps", type=int, default=10)
    parser.add_argument("--save_total_limit", type=int, default=2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--weight_decay", type=float, default=0.01)
    parser.add_argument("--warmup_ratio", type=float, default=0.1)
    parser.add_argument("--max_grad_norm", type=float, default=1.0)

    # Advanced options
    parser.add_argument("--resume_from_checkpoint", type=str, default=None, help="Resume training from checkpoint")
    parser.add_argument("--use_wandb", action="store_true", help="Enable Weights & Biases logging")

    return parser.parse_args()


class CodeFixDataset(Dataset):

    def __init__(self, data: List[Dict[str, Any]], tokenizer, max_length: int = 1024):
        self.samples = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        sample = self.samples[idx]

        # Handle empty analysis arrays safely
        analysis_list = sample.get("analysis", [])
        if len(analysis_list) == 0:
            # Create a default analysis item if list is empty
            analysis_item = {
                "issue": "No specific issue identified",
                "explanation": {
                    "problem": "Code review completed",
                    "reason": "General code improvement",
                    "fix": "Code has been optimized"
                }
            }
        else:
            analysis_item = analysis_list[0]
        
        issue = analysis_item.get("issue", "")
        explanation = analysis_item.get("explanation", {})

        prompt = (
            f"Filename: {sample.get('filename', '')}\n"
            f"Issue: {issue}\n"
            f"Problem: {explanation.get('problem', '')}\n"
            f"Reason: {explanation.get('reason', '')}\n"
            f"### Fix:\n"
        )
        target = (
            f"{explanation.get('fix', '')}\n\n"
            f"### Fixed Code:\n{sample.get('fixed_code', '')}"
        )

        full_text = prompt + target + (self.tokenizer.eos_token or "</s>")

        tokenized = self.tokenizer(
            full_text,
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt",
        )
        input_ids = tokenized.input_ids.squeeze(0)
        attention_mask = tokenized.attention_mask.squeeze(0)

        # Mask labels so loss is only computed on target tokens
        labels = input_ids.clone()
        prompt_len = len(self.tokenizer(prompt).input_ids)
        labels[:prompt_len] = -100  # ignore prompt tokens

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels,
        }


def load_json_data(path: str | Path) -> List[Dict[str, Any]]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    data: List[Dict[str, Any]] = []
    if path.suffix in {".jsonl", ".json"}:
        with path.open() as f:
            if path.suffix == ".jsonl":
                current_json = ""
                in_json_block = False
                
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    if line.startswith("```json"):
                        in_json_block = True
                        current_json = ""
                        continue
                    elif line.startswith("```") and in_json_block:
                        if current_json.strip():
                            try:
                                parsed = json.loads(current_json.strip())
                                data.append(parsed)
                            except json.JSONDecodeError as e:
                                LOGGER.warning(f"Failed to parse JSON block: {e}")
                        in_json_block = False
                        current_json = ""
                        continue
                    elif in_json_block:
                        current_json += line + "\n"
                    elif line.startswith("{"):
                        try:
                            data.append(json.loads(line))
                        except json.JSONDecodeError as e:
                            LOGGER.warning(f"Failed to parse JSON line: {e}")
                
                if in_json_block and current_json.strip():
                    try:
                        parsed = json.loads(current_json.strip())
                        data.append(parsed)
                    except json.JSONDecodeError as e:
                        LOGGER.warning(f"Failed to parse final JSON block: {e}")
            else:
                parsed = json.load(f)
                if isinstance(parsed, list):
                    data.extend(parsed)
                else:
                    data.append(parsed)
    else:
        raise ValueError("Unsupported file type; expected .json or .jsonl")

    LOGGER.info("Loaded %d samples from %s", len(data), path)
    return data


def force_empty_gpu_cache():
    """Aggressively clear GPU memory"""
    LOGGER.info("🧹 Force clearing GPU cache...")
    torch.cuda.empty_cache()
    torch.cuda.synchronize()
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.reset_accumulated_memory_stats()
        allocated = torch.cuda.memory_allocated() / (1024**3)
        cached = torch.cuda.memory_reserved() / (1024**3)
        LOGGER.info(f"💾 After clearing - Allocated: {allocated:.1f}GB, Cached: {cached:.1f}GB")


def setup_lora_model(model, args):
    """Configure model with LoRA for memory-efficient training."""
    LOGGER.info("🔧 Setting up LoRA configuration")
    
    # Prepare model for training if using quantization
    if hasattr(args, 'use_8bit') and args.use_8bit:
        model = prepare_model_for_kbit_training(model)
    
    # LoRA configuration
    lora_config = LoraConfig(
        r=args.lora_r,  # Rank of LoRA matrices
        lora_alpha=args.lora_alpha,  # Scaling factor
        target_modules=args.lora_target_modules,  # Which modules to apply LoRA to
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )
    
    # Apply LoRA to model
    model = get_peft_model(model, lora_config)
    
    # Print trainable parameters
    trainable_params = 0
    total_params = 0
    for _, param in model.named_parameters():
        total_params += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    
    LOGGER.info(
        f"✅ LoRA configured: {trainable_params:,} trainable / {total_params:,} total "
        f"({100 * trainable_params / total_params:.2f}% trainable)"
    )
    LOGGER.info(f"   LoRA rank (r): {args.lora_r}")
    LOGGER.info(f"   LoRA alpha: {args.lora_alpha}")
    LOGGER.info(f"   Target modules: {args.lora_target_modules}")
    
    return model

def get_optimal_batch_settings(use_lora: bool = True):
    """Auto-determine optimal batch size and gradient accumulation based on GPU memory and training mode."""
    if not torch.cuda.is_available():
        return 2, 1
    
    # Get GPU memory in GB
    gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    LOGGER.info(f"💾 Detected GPU memory: {gpu_mem:.1f}GB")
    
    if use_lora:
        # More generous settings for LoRA (uses much less memory)
        if gpu_mem >= 80:  # A100 80GB
            return 8, 2  # Large batches possible
        elif gpu_mem >= 40:  # A100 40GB
            return 4, 4
        elif gpu_mem >= 24:  # RTX 4090/A6000
            return 2, 8
        elif gpu_mem >= 16:  # RTX 3090/4080
            return 2, 16
        else:  # Smaller GPUs
            return 1, 32
    else:
        # Conservative settings for full weight training (legacy)
        if gpu_mem >= 80:
            return 2, 32
        elif gpu_mem >= 40:
            return 1, 64
        elif gpu_mem >= 24:
            return 1, 128
        else:
            return 1, 256


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    # GPU setup and memory optimization
    if not torch.cuda.is_available():
        LOGGER.warning("  CUDA not available! Training will be very slow on CPU.")
    else:
        gpu_count = torch.cuda.device_count()
        LOGGER.info(f" Detected {gpu_count} GPU(s)")
        for i in range(gpu_count):
            prop = torch.cuda.get_device_properties(i)
            LOGGER.info(f"  GPU {i}: {torch.cuda.get_device_name(i)} ({prop.total_memory/1024**3:.1f}GB)")
    
    force_empty_gpu_cache()

    # Prepare datasets (load once, reuse across models)
    train_data = load_json_data(args.train_file)

    eval_data = None
    if args.eval_file:
        eval_data = load_json_data(args.eval_file)

    for model_path in args.model_paths:
        LOGGER.info(f"\n=========== Fine-tuning model {model_path} ===========")

        # (Re)load tokenizer & model for each iteration to avoid weight leakage
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        # Load model with optional quantization
        LOGGER.info(f"📥 Loading model from {model_path}")
        load_kwargs = {
            "torch_dtype": torch.bfloat16,
            "device_map": "auto",
            "low_cpu_mem_usage": True,
            "use_cache": False,
        }
        
        if args.use_8bit:
            load_kwargs["load_in_8bit"] = True
            LOGGER.info("⚙️  Loading model in 8-bit mode for memory efficiency")
        
        model = AutoModelForCausalLM.from_pretrained(model_path, **load_kwargs)

        # Apply LoRA configuration (REPLACES old freezing logic)
        if args.use_lora:
            model = setup_lora_model(model, args)
        else:
            LOGGER.warning("⚠️  Running without LoRA (not recommended for memory-constrained environments)")
            # Fallback: enable all parameters for training
            for param in model.parameters():
                param.requires_grad = True

        # Enable gradient checkpointing for memory efficiency (compatible with LoRA)
        if hasattr(model, 'enable_input_require_grads'):
            model.enable_input_require_grads()
        if not args.use_8bit:  # Skip gradient checkpointing with 8-bit
            model.gradient_checkpointing_enable()
        if hasattr(model.config, "use_cache"):
            model.config.use_cache = False

        # Auto-determine batch settings if not specified
        batch_size = args.per_device_train_batch_size
        grad_accum = args.gradient_accumulation_steps
        
        if batch_size is None or grad_accum is None:
            auto_batch, auto_grad = get_optimal_batch_settings(use_lora=args.use_lora)
            if batch_size is None:
                batch_size = auto_batch
            if grad_accum is None:
                grad_accum = auto_grad
            LOGGER.info(f"⚙️  Auto-selected: batch_size={batch_size}, gradient_accumulation_steps={grad_accum}")

        train_ds = CodeFixDataset(train_data, tokenizer, max_length=args.max_length)
        eval_ds = (
            CodeFixDataset(eval_data, tokenizer, max_length=args.max_length) if eval_data else None
        )

        # Collator (prompt labels already set)
        data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

        # Make a sub-directory inside output_dir for each model (use folder name)
        model_slug = Path(model_path).name.replace("/", "_")
        out_dir = Path(args.output_dir) / model_slug
        out_dir.mkdir(parents=True, exist_ok=True)

        # Enhanced training arguments for LoRA training
        training_args = TrainingArguments(
            output_dir=str(out_dir),
            overwrite_output_dir=True,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=args.per_device_eval_batch_size,
            learning_rate=args.learning_rate,
            num_train_epochs=args.num_train_epochs,
            gradient_accumulation_steps=grad_accum,
            weight_decay=args.weight_decay,
            warmup_ratio=args.warmup_ratio,
            max_grad_norm=args.max_grad_norm,
            eval_strategy="steps" if eval_ds is not None else "no",
            eval_steps=500 if eval_ds is not None else None,
            logging_steps=args.logging_steps,
            save_strategy="epoch",
            save_total_limit=args.save_total_limit,
            seed=args.seed,
            bf16=torch.cuda.is_available() and not args.use_8bit,  # Use bfloat16 if GPU available and not 8-bit
            fp16=args.use_8bit,  # Use fp16 with 8-bit quantization
            gradient_checkpointing=True and not args.use_8bit,
            dataloader_pin_memory=False,
            remove_unused_columns=False,
            ddp_find_unused_parameters=False,
            optim="adamw_torch",  # Standard optimizer works well with LoRA
            report_to="wandb" if args.use_wandb else "none",
            run_name=f"lora_sft_{model_slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}" if args.use_wandb else None,
        )

        # Handle both old and new transformers versions
        try:
            trainer = Trainer(
                model=model,
                processing_class=tokenizer,
                args=training_args,
                train_dataset=train_ds,
                eval_dataset=eval_ds,
                data_collator=data_collator,
            )
        except TypeError:
            # Fallback for older transformers versions
            trainer = Trainer(
                model=model,
                tokenizer=tokenizer,
                args=training_args,
                train_dataset=train_ds,
                eval_dataset=eval_ds,
                data_collator=data_collator,
            )

        force_empty_gpu_cache()
        
        # Train the model
        LOGGER.info("🚀 Starting training...")
        if args.resume_from_checkpoint:
            trainer.train(resume_from_checkpoint=args.resume_from_checkpoint)
        else:
            trainer.train()
        
        # Save LoRA adapter and merged model
        LOGGER.info(f"💾 Saving model to {out_dir}")
        
        if args.use_lora:
            # Save LoRA adapter weights
            model.save_pretrained(str(out_dir))
            tokenizer.save_pretrained(str(out_dir))
            LOGGER.info(f"✅ LoRA adapter saved to {out_dir}")
            
            # Merge and save full model
            merged_dir = out_dir / "merged"
            merged_dir.mkdir(exist_ok=True)
            LOGGER.info(f"🔄 Merging LoRA weights and saving to {merged_dir}")
            
            try:
                # Merge LoRA weights with base model
                merged_model = model.merge_and_unload()
                merged_model.save_pretrained(str(merged_dir))
                tokenizer.save_pretrained(str(merged_dir))
                LOGGER.info(f"✅ Merged model saved to {merged_dir}")
                del merged_model
            except Exception as e:
                LOGGER.warning(f"⚠️  Failed to merge model: {e}. Using adapter only.")
        else:
            trainer.save_model()
            tokenizer.save_pretrained(str(out_dir))
        
        LOGGER.info(f"✅ Finished fine-tuning {model_path}")

        # Clean GPU memory before next model
        del model
        del trainer
        force_empty_gpu_cache()


if __name__ == "__main__":
    main() 