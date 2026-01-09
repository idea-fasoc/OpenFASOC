"""
A script to finetune the models with LoRA, based on input data, which is receieved from the processing pipeline.
This file automatically distributes training across all available GPUs, if multiple are available.
use --training_data_dir to specify the directory to retrieve data from

LoRA Configuration
------------------
Use --lora_r to set the rank (default: 16, higher = more capacity)
Use --lora_alpha to set the scaling factor (default: 32, typically 2x lora_r)
Use --use_8bit to enable 8-bit quantization for even lower memory usage
The script saves both the LoRA adapter and a merged model for inference.
"""

import os
import gc
import torch
import argparse

from datetime import datetime
from datasets import load_from_disk
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    TaskType,
    PeftModel,
)


MODEL_MAPPINGS = {
    "7b": "codellama/CodeLlama-7b-Instruct-hf",
    "13b": "codellama/CodeLlama-13b-Instruct-hf", 
    "7b-ft": "./models/7b_finetuned",  
    "13b-ft": "./models/13b_finetuned",  

}

def resolve_model_path(model_input: str) -> str:
    if model_input in MODEL_MAPPINGS:
        resolved = MODEL_MAPPINGS[model_input]
        print(f"Resolved model '{model_input}' → '{resolved}'")
        return resolved
    else:
        print(f"Using direct model path: '{model_input}'")
        return model_input


# Disable wandb (not configured in non-interactive environment)
os.environ.setdefault("WANDB_DISABLED", "true")
os.environ.setdefault("WANDB_SILENT", "true")
os.environ.setdefault("WANDB_CONSOLE", "off")

# Disable expandable_segments to avoid CUDA allocator issues with gradient checkpointing
# Use roundup_power2_divisions to reduce fragmentation instead
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "roundup_power2_divisions:16,max_split_size_mb:512"


def force_empty_gpu_cache():
    """Aggressively clear GPU cache to prevent memory fragmentation issues"""
    print("🧹 Force clearing GPU cache...")
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        # Run multiple times to ensure cleanup
        for _ in range(2):
            gc.collect()
            torch.cuda.empty_cache()
        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.reset_accumulated_memory_stats()
        allocated = torch.cuda.memory_allocated() / (1024**3)
        cached = torch.cuda.memory_reserved() / (1024**3)
        print(f"💾 After clearing - Allocated: {allocated:.1f}GB, Cached: {cached:.1f}GB")


def setup_lora_model(model, lora_r=16, lora_alpha=32, lora_dropout=0.05, 
                     lora_target_modules=None, use_8bit=False):
    """Configure model with LoRA for memory-efficient training."""
    print("🔧 Setting up LoRA configuration")
    
    # Prepare model for training if using quantization
    if use_8bit:
        model = prepare_model_for_kbit_training(model)
    
    # Default target modules for CodeLlama/Llama
    if lora_target_modules is None:
        lora_target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", 
                               "gate_proj", "up_proj", "down_proj"]
    
    # LoRA configuration
    lora_config = LoraConfig(
        r=lora_r,
        lora_alpha=lora_alpha,
        target_modules=lora_target_modules,
        lora_dropout=lora_dropout,
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
    
    print(
        f"✅ LoRA configured: {trainable_params:,} trainable / {total_params:,} total "
        f"({100 * trainable_params / total_params:.2f}% trainable)"
    )
    print(f"   LoRA rank (r): {lora_r}")
    print(f"   LoRA alpha: {lora_alpha}")
    print(f"   Target modules: {lora_target_modules}")
    
    return model



def main(
    model: str = "13b",
    training_data_dir: str = None,
    output_dir: str = "./final_model", 
    checkpoint_dir: str = "./checkpoints",
    num_train_epochs: int = 3, 
    resume_from_checkpoint: str | None = None, 
    use_lora: bool = True,
    lora_r: int = 16,
    lora_alpha: int = 32,
    lora_dropout: float = 0.05,
    use_8bit: bool = False,
    train_last_n_layers: int = 0  # 0 = train all layers, N = train only last N layers
) -> None:
    # Resolve model using mapping system
    model_path = resolve_model_path(model)
    print(f" Fine-tuning model: {model} → {model_path}")
    
    # Determine training data directory
    if training_data_dir is None:
        # Auto-determine based on model
        model_suffix = model.replace("/", "_").replace(":", "_")
        training_data_dir = f"training_data_{model_suffix}"
    
    print(f" Using training data from: {training_data_dir}")
    
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA not available – need GPUs!")

    n_gpu = torch.cuda.device_count()
    print(f" Detected {n_gpu} CUDA device(s)")
    for idx in range(n_gpu):
        props = torch.cuda.get_device_properties(idx)
        print(f"  GPU {idx}: {torch.cuda.get_device_name(idx)} ({props.total_memory/1024**3:.1f} GB)")

    if not os.path.exists(training_data_dir):
        raise FileNotFoundError(f"Training data directory not found: {training_data_dir}\nRun: python process_data.py --model {model}")
    
    dataset = load_from_disk(training_data_dir)
    split = int(0.9 * len(dataset))
    train_ds, eval_ds = torch.utils.data.random_split(dataset, [split, len(dataset) - split])

    force_empty_gpu_cache()

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    tokenizer.pad_token = tokenizer.pad_token or tokenizer.eos_token

    # Load model with optional quantization
    print(f"📥 Loading model from {model_path}")
    load_kwargs = {
        "torch_dtype": torch.bfloat16,
        "device_map": "auto",  # hf accelerate spreads layers across the visible GPUs
        "low_cpu_mem_usage": True,
        "use_cache": False,
    }
    
    if use_8bit:
        load_kwargs["load_in_8bit"] = True
        print("⚙️  Loading model in 8-bit mode for memory efficiency")
    
    model = AutoModelForCausalLM.from_pretrained(model_path, **load_kwargs)

    # Apply LoRA configuration
    if use_lora:
        model = setup_lora_model(model, lora_r=lora_r, lora_alpha=lora_alpha, 
                                lora_dropout=lora_dropout, use_8bit=use_8bit)
    else:
        print("⚠️  Running without LoRA (not recommended for memory-constrained environments)")
        for p in model.parameters():
            p.requires_grad = True

    # Enable gradient checkpointing for memory efficiency (compatible with LoRA)
    if hasattr(model, 'enable_input_require_grads'):
        model.enable_input_require_grads()
    if not use_8bit:  # Skip gradient checkpointing with 8-bit
        model.gradient_checkpointing_enable()
    if hasattr(model.config, "use_cache"):
        model.config.use_cache = False

    # Freeze lower layers if requested (preserves base model abilities)
    if train_last_n_layers > 0 and use_lora:
        print(f"🔒 Freezing lower layers, training only last {train_last_n_layers} layers (preserves base model abilities)")
        # Find transformer layers
        layers = None
        if hasattr(model.model, 'model') and hasattr(model.model.model, 'layers'):
            layers = model.model.model.layers  # LoRA wrapped model
        elif hasattr(model, 'model') and hasattr(model.model, 'layers'):
            layers = model.model.layers  # Direct model
        
        if layers is not None:
            total_layers = len(layers)
            train_from = max(0, total_layers - train_last_n_layers)
            print(f"  Total layers: {total_layers}, freezing first {train_from}, training last {train_last_n_layers}")
            
            # Freeze lower layers (including their LoRA adapters)
            for idx in range(train_from):
                for param in layers[idx].parameters():
                    param.requires_grad = False
            print(f"✅ Froze {train_from} lower layers")
        else:
            print("⚠️  Could not find transformer layers to freeze")

    # Auto-determine batch settings based on GPU memory and LoRA usage
    per_gpu_mem = torch.cuda.get_device_properties(0).total_memory / 1024**3
    print(f"💾 Detected GPU memory: {per_gpu_mem:.1f}GB")
    
    if use_lora:
        # More generous settings for LoRA (uses much less memory)
        if per_gpu_mem >= 80:
            batch_size = 8
            grad_accum = 2
        elif per_gpu_mem >= 40:
            batch_size = 4
            grad_accum = 4
        elif per_gpu_mem >= 24:
            batch_size = 2
            grad_accum = 8
        else:
            batch_size = 1
            grad_accum = 32
    else:
        # Conservative settings for full weight training
        if per_gpu_mem >= 80:
            batch_size = 2
            grad_accum = 32
        elif per_gpu_mem >= 40:
            batch_size = 1
            grad_accum = 64
        else:
            batch_size = 1
            grad_accum = 128

    print(f"⚙️  Training settings → batch {batch_size} × accum {grad_accum}")

    # Create output directories if they don't exist
    os.makedirs(checkpoint_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Adjusted learning rate for LoRA (higher than full FT)
    learning_rate = 2e-4 if use_lora else 3e-5
    
    args = TrainingArguments(
        output_dir=checkpoint_dir,
        overwrite_output_dir=True,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=2 if use_lora else 1,
        gradient_accumulation_steps=grad_accum,
        learning_rate=learning_rate,
        weight_decay=0.01,
        warmup_ratio=0.1,
        logging_steps=10,
        save_strategy="no",  # Don't save checkpoints during training (we save final model after)
        eval_strategy="steps",
        eval_steps=500,
        bf16=torch.cuda.is_available() and not use_8bit,
        fp16=use_8bit,  # Use fp16 with 8-bit quantization
        gradient_checkpointing=True and not use_8bit,
        optim="adamw_torch" if use_lora else "adafactor",
        ddp_find_unused_parameters=False,
        run_name=f"lora_finetune_{datetime.now().strftime('%Y%m%d_%H%M%S')}" if use_lora else f"finetune_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        report_to="none",  # Disable WandB reporting
        save_total_limit=0,  # No checkpoints needed
        dataloader_pin_memory=False,
        remove_unused_columns=False,
        max_grad_norm=1.0,
    )

    collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    # Handle both old and new transformers versions
    try:
        trainer = Trainer(
            model=model,
            processing_class=tokenizer,
            args=args,
            train_dataset=train_ds,
            eval_dataset=eval_ds,
            data_collator=collator,
        )
    except TypeError:
        # Fallback for older transformers versions
        trainer = Trainer(
            model=model,
            args=args,
            train_dataset=train_ds,
            eval_dataset=eval_ds,
            tokenizer=tokenizer,
            data_collator=collator,
        )

    force_empty_gpu_cache()
    
    # Train the model
    print("🚀 Starting training...")
    trainer.train(resume_from_checkpoint=resume_from_checkpoint) if resume_from_checkpoint else trainer.train()

    # Clean up training checkpoints (we only need the final model)
    print("🧹 Cleaning up training checkpoints...")
    from pathlib import Path
    checkpoint_path = Path(checkpoint_dir)
    checkpoint_dirs = list(checkpoint_path.glob("checkpoint-*"))
    for checkpoint_dir_item in checkpoint_dirs:
        if checkpoint_dir_item.is_dir():
            import shutil
            shutil.rmtree(checkpoint_dir_item)
            print(f"   Deleted checkpoint: {checkpoint_dir_item.name}")

    # Save LoRA adapter only (99.7% space savings vs merged model)
    print(f"💾 Saving LoRA adapter to {output_dir}")
    
    if use_lora:
        # Save LoRA adapter weights (40MB vs 13GB merged model)
        model.save_pretrained(output_dir)
        tokenizer.save_pretrained(output_dir)
        print(f"✅ LoRA adapter saved to {output_dir} (~40MB)")
        print(f"💡 To use: Load base model + this adapter")
        print(f"💡 To merge for deployment: Use scripts/utils/merge_lora.py")
    else:
        # Full weight training fallback
        trainer.save_model(output_dir)
        tokenizer.save_pretrained(output_dir)
        print(f"✅ Full model saved to {output_dir}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Fine-tune language models with LoRA")
    p.add_argument("--model", type=str, default="13b", 
                   help="Model name or path to fine-tune (default: 13b)")
    p.add_argument("--training_data_dir", type=str, default=None,
                   help="Directory containing training data (default: auto-determined)")
    p.add_argument("--output_dir", type=str, default="./final_model",
                   help="Directory to save the final fine-tuned model (default: ./final_model)")
    p.add_argument("--checkpoint_dir", type=str, default="./checkpoints",
                   help="Directory to save training checkpoints (default: ./checkpoints)")
    p.add_argument("--num_train_epochs", type=int, default=3,
                   help="Number of training epochs (default: 3)")
    p.add_argument("--resume_from_checkpoint", type=str, default=None,
                   help="Path to checkpoint to resume training from")
    
    # LoRA Configuration
    p.add_argument("--use_lora", action="store_true", default=True,
                   help="Use LoRA for efficient fine-tuning (default: True)")
    p.add_argument("--no_lora", dest="use_lora", action="store_false",
                   help="Disable LoRA (use full weight training)")
    p.add_argument("--lora_r", type=int, default=16,
                   help="LoRA rank (8-64, higher = more capacity, default: 16)")
    p.add_argument("--lora_alpha", type=int, default=32,
                   help="LoRA alpha scaling (typically 2x lora_r, default: 32)")
    p.add_argument("--lora_dropout", type=float, default=0.05,
                   help="LoRA dropout rate (default: 0.05)")
    p.add_argument("--train_last_n_layers", type=int, default=0,
                   help="Train only last N layers (0=train all layers, default: 0). Freezes lower layers to preserve base model abilities.")
    p.add_argument("--use_8bit", action="store_true", default=False,
                   help="Use 8-bit quantization for lower memory (default: False)")
    
    parsed = p.parse_args()
    main(
        model=parsed.model,
        training_data_dir=parsed.training_data_dir,
        output_dir=parsed.output_dir, 
        checkpoint_dir=parsed.checkpoint_dir,
        num_train_epochs=parsed.num_train_epochs,
        resume_from_checkpoint=parsed.resume_from_checkpoint,
        use_lora=parsed.use_lora,
        lora_r=parsed.lora_r,
        lora_alpha=parsed.lora_alpha,
        lora_dropout=parsed.lora_dropout,
        use_8bit=parsed.use_8bit,
        train_last_n_layers=parsed.train_last_n_layers
    ) 