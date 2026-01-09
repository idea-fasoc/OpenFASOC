#!/usr/bin/env python3
"""
Data Processing for CodeLlama Fine-tuning
Collects and tokenises OpenFASOC placement/routing Python sources + explicit training pairs.
"""

import os
import json
import argparse
from pathlib import Path
from transformers import AutoTokenizer
from datasets import Dataset


# =================================================================
# MODEL MAPPING SYSTEM
# Unified model shortcuts that map to full paths/names
# =================================================================
MODEL_MAPPINGS = {
    "7b": "codellama/CodeLlama-7b-Instruct-hf",
    "13b": "codellama/CodeLlama-13b-Instruct-hf", 
    "7b-ft": "./models/7b_finetuned",  # Local fine-tuned model
    "13b-ft": "./models/13b_finetuned",  # Local fine-tuned model
    # Add more mappings as needed
}

def resolve_model_path(model_input: str) -> str:
    """Resolve model shortcut to full path/name."""
    if model_input in MODEL_MAPPINGS:
        resolved = MODEL_MAPPINGS[model_input]
        print(f"📋 Resolved model '{model_input}' → '{resolved}'")
        return resolved
    else:
        print(f"📋 Using direct model path: '{model_input}'")
        return model_input


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------

def collect_python_files(directories):
    """Walk the provided directories and return a list of non-trivial Python
    files (source code + metadata)."""
    files_data = []
    for directory in directories:
        if not os.path.exists(directory):
            print(f"⚠️  {directory} not found – skipping")
            continue
        print(f"📂 Scanning {directory} …")
        for root, _dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, "r", encoding="utf-8") as fh:
                            content = fh.read().strip()
                        # Skip tiny/empty files – they add little training signal
                        if content and len(content) > 100:
                            files_data.append(
                                {
                                    "text": content,
                                    "source": filepath,
                                    "length": len(content),
                                    "type": "source_file"
                                }
                            )
                            print(f"  ✓ Added {file} ({len(content)} chars)")
                    except Exception as e:
                        print(f"  ⚠️  Error reading {filepath}: {e}")
    return files_data


def load_training_pairs(training_pairs_file):
    """Load explicit input-output training pairs from JSONL file."""
    training_pairs = []
    if not os.path.exists(training_pairs_file):
        print(f"⚠️  {training_pairs_file} not found – skipping training pairs")
        return training_pairs
    
    print(f"📋 Loading training pairs from {training_pairs_file} …")
    try:
        with open(training_pairs_file, "r", encoding="utf-8") as fh:
            for line_num, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    pair = json.loads(line)
                    if ("input" in pair or "instruction" in pair) and "output" in pair:
                        # Get the instruction from either 'input' or 'instruction' field
                        instruction = pair.get('input') or pair.get('instruction')
                        # Format as instruction-following conversation
                        formatted_text = f"""<s>[INST] <<SYS>>
You are PCELL-GPT, a Python-3 code generator.
Return ONLY a single python code block; do NOT add commentary, do not use placeholders.
Code **must** compile under `python -m py_compile`.
<</SYS>>
TASK: {instruction}
[/INST]
```python
{pair['output']}
```</s>"""
                        training_pairs.append({
                            "text": formatted_text,
                            "source": f"{training_pairs_file}:line_{line_num}",
                            "length": len(formatted_text),
                            "type": "input_output_pair"
                        })
                        print(f"  ✓ Added training pair {line_num} ({len(formatted_text)} chars)")
                    else:
                        print(f"  ⚠️  Line {line_num}: Missing 'input'/'instruction' or 'output' key")
                except json.JSONDecodeError as e:
                    print(f"  ⚠️  Line {line_num}: JSON decode error: {e}")
    except Exception as e:
        print(f"  ⚠️  Error reading {training_pairs_file}: {e}")
    
    return training_pairs


def create_training_dataset(files_data, model_path: str):
    """Tokenise the collected code using the specified model's tokenizer and return a 🤗 Dataset."""

    print(f"🗃  Creating dataset from {len(files_data)} files using tokenizer: {model_path}")
    
    # Report composition
    source_files = [f for f in files_data if f.get("type") == "source_file"]
    training_pairs = [f for f in files_data if f.get("type") == "input_output_pair"]
    print(f"  📄 Source files: {len(source_files)}")
    print(f"  🎯 Training pairs: {len(training_pairs)}")

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    dataset = Dataset.from_list(files_data)

    def _tok(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            max_length=2048,
            padding=False,
            return_tensors=None,
        )

    print("🔑 Tokenising …")
    tokenised = dataset.map(
        _tok,
        batched=True,
        remove_columns=dataset.column_names,
        desc="Tokenising",
    )
    return tokenised


# ----------------------------------------------------------------------------
# Entry-point
# ----------------------------------------------------------------------------


def main() -> None:
    """Main function with command line argument support."""
    parser = argparse.ArgumentParser(description="Process OpenFASOC data for fine-tuning")
    parser.add_argument(
        "--model", 
        type=str, 
        default="13b",
        help="Model to use for tokenization (7b, 13b, 7b-ft, 13b-ft, or full model path)"
    )
    parser.add_argument(
        "--openfasoc_path",
        type=str,
        default="external/OpenFASOC/",
        help="Path to OpenFASOC directory (default: external/OpenFASOC/)"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
        help="Optional output directory to save processed dataset (default: training_data_<model>)"
    )
    
    args = parser.parse_args()
    
    # Resolve model path using mapping system
    model_path = resolve_model_path(args.model)
    
    print(f"🚀 Data Processing for {args.model} Fine-tuning")
    print(f"🎯 Using tokenizer from: {model_path}")
    print("=" * 60)

    source_dirs = [
        args.openfasoc_path,  # Use configurable OpenFASOC path
    ]

    # Collect source files from OpenFASOC
    files_data = collect_python_files(source_dirs)

    all_training_data = files_data
    
    if not all_training_data:
        print("❌ No training data found – aborting.")
        import sys
        sys.exit(1)  # Exit with error code when no data found

    print(f"📊 Total training examples: {len(all_training_data)}")

    # --------------------------------------------------------------------
    # 🧹 Deduplicate identical examples to mitigate over-fitting on
    #     repeated code blocks that can lead to repetition collapse at
    #     generation time.
    # --------------------------------------------------------------------
    dedup_map = {}
    for item in all_training_data:
        text_hash = hash(item["text"])
        # Keep only the first instance of each unique text.
        if text_hash not in dedup_map:
            dedup_map[text_hash] = item

    if len(dedup_map) != len(all_training_data):
        print(f"🧹 Removed {len(all_training_data) - len(dedup_map)} duplicate examples")

    all_training_data = list(dedup_map.values())

    # Create dataset with specified model's tokenizer
    dataset = create_training_dataset(all_training_data, model_path)

    # Determine output directory
    model_suffix = args.model.replace("/", "_").replace(":", "_")
    out_dir = args.output_dir if args.output_dir else f"training_data_{model_suffix}"
    out_dir_path = Path(out_dir).resolve()
    os.makedirs(out_dir_path, exist_ok=True)
    dataset.save_to_disk(str(out_dir_path))
    print(f"✅ Tokenised dataset saved to {out_dir}")

    # Save raw file metadata for bookkeeping
    with open(os.path.join(str(out_dir_path), "raw_files.json"), "w", encoding="utf-8") as fh:
        json.dump(all_training_data, fh, indent=2)

    # ========================================================================
    # ALSO save JSONL format for train.py compatibility
    # Convert raw Python files to code-fix format for domain adaptation
    # ========================================================================
    model_size = args.model if args.model in ["7b", "13b"] else "model"
    jsonl_file = out_dir_path / f"train_data_{model_size}.jsonl"
    
    print(f"📝 Converting to train.py format (domain adaptation)...")
    with open(jsonl_file, "w", encoding="utf-8") as fout:
        for item in all_training_data:
            # Extract filename from source path or use generic name
            source_path = item.get("source", "openfasoc_code.py")
            # Get just the filename from the full path
            filename = Path(source_path).name if source_path else "openfasoc_code.py"
            code_text = item.get("text", "")
            
            # For domain adaptation, create a "code understanding" task
            # This teaches the model to understand and reproduce OpenFASOC code
            training_item = {
                "filename": filename,
                "analysis": [{
                    "issue": "Code documentation and understanding",
                    "explanation": {
                        "problem": "Understanding OpenFASOC analog generator code patterns",
                        "reason": "Learning domain-specific code structure and conventions",
                        "fix": "Study and reproduce the code structure"
                    }
                }],
                "fixed_code": code_text
            }
            fout.write(json.dumps(training_item, ensure_ascii=False) + "\n")
    
    print(f"✅ JSONL file saved: {jsonl_file.relative_to(out_dir_path.parent)}")
    print(f"📊 Total samples: {len(all_training_data)}")
    print(f"🎉 Processing complete! Use with:")
    print(f"   - gpu_finetune.py --model {args.model} --training_data_dir {out_dir}")
    print(f"   - train.py --train_file {jsonl_file}")


if __name__ == "__main__":
    main() 