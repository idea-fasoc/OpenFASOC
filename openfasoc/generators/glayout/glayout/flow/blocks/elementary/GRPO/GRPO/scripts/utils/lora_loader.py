#!/usr/bin/env python3
"""
LoRA Adapter Loader Utility
============================

Helper functions to load base models with LoRA adapters for inference.

This module provides a unified interface to load models whether they are:
- Full merged models (legacy)
- LoRA adapters (new, space-efficient)
- Base models (for initial inference)

Usage:
------
from scripts.utils.lora_loader import load_model_for_inference

# Automatically detects and loads the right way
model, tokenizer = load_model_for_inference("path/to/model_or_adapter")
"""

from pathlib import Path
from typing import Tuple, Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Base model mappings
BASE_MODEL_MAP = {
    "7b": "codellama/CodeLlama-7b-Instruct-hf",
    "13b": "codellama/CodeLlama-13b-Instruct-hf",
    "CodeLlama-7b-Instruct-hf": "codellama/CodeLlama-7b-Instruct-hf",
    "CodeLlama-13b-Instruct-hf": "codellama/CodeLlama-13b-Instruct-hf",
}


def is_lora_adapter(model_path: Path) -> bool:
    """Check if a directory contains a LoRA adapter (not a full model)."""
    model_path = Path(model_path)
    
    # LoRA adapters have adapter_config.json
    has_adapter_config = (model_path / "adapter_config.json").exists()
    
    # Full models have model.safetensors or pytorch_model.bin
    has_full_model = (
        (model_path / "model.safetensors").exists() or
        (model_path / "pytorch_model.bin").exists() or
        list(model_path.glob("model-*.safetensors"))  # Sharded models
    )
    
    return has_adapter_config and not has_full_model


def get_base_model_for_adapter(adapter_path: Path) -> str:
    """Infer which base model to use for a given adapter."""
    adapter_path = Path(adapter_path)
    
    # Try to read from adapter_config.json
    adapter_config_path = adapter_path / "adapter_config.json"
    if adapter_config_path.exists():
        import json
        with open(adapter_config_path) as f:
            config = json.load(f)
            if "base_model_name_or_path" in config:
                base_model = config["base_model_name_or_path"]
                LOGGER.info(f"Found base model in adapter config: {base_model}")
                return base_model
    
    # Fallback: infer from path
    path_str = str(adapter_path).lower()
    if "7b" in path_str:
        LOGGER.info("Inferring 7B base model from path")
        return BASE_MODEL_MAP["7b"]
    elif "13b" in path_str:
        LOGGER.info("Inferring 13B base model from path")
        return BASE_MODEL_MAP["13b"]
    
    # Default to 7B
    LOGGER.warning("Could not infer base model, defaulting to 7B")
    return BASE_MODEL_MAP["7b"]


def load_model_for_inference(
    model_path: str,
    torch_dtype=torch.bfloat16,
    device_map: str = "auto",
    trust_remote_code: bool = True,
) -> Tuple[AutoModelForCausalLM, AutoTokenizer]:
    """
    Load a model for inference, automatically handling LoRA adapters or full models.
    
    Args:
        model_path: Path to model directory or adapter directory
        torch_dtype: Data type for model weights
        device_map: Device mapping strategy
        trust_remote_code: Whether to trust remote code
        
    Returns:
        (model, tokenizer) tuple ready for inference
        
    Examples:
        # Load LoRA adapter (will automatically load base + adapter)
        model, tokenizer = load_model_for_inference("initial_finetuned_models/7b_20251111/CodeLlama-7b-Instruct-hf")
        
        # Load full merged model (legacy support)
        model, tokenizer = load_model_for_inference("initial_finetuned_models/7b_20251111/CodeLlama-7b-Instruct-hf/merged")
        
        # Load base model
        model, tokenizer = load_model_for_inference("codellama/CodeLlama-7b-Instruct-hf")
    """
    model_path = Path(model_path)
    
    # Check if this is a LoRA adapter
    if model_path.exists() and is_lora_adapter(model_path):
        LOGGER.info(f"🔧 Detected LoRA adapter at {model_path}")
        
        # Get base model
        base_model_name = get_base_model_for_adapter(model_path)
        LOGGER.info(f"📥 Loading base model: {base_model_name}")
        
        # Load base model
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch_dtype,
            device_map=device_map,
            trust_remote_code=trust_remote_code,
        )
        
        # Load LoRA adapter on top
        LOGGER.info(f"🔧 Loading LoRA adapter from {model_path}")
        model = PeftModel.from_pretrained(
            base_model,
            str(model_path),
            torch_dtype=torch_dtype,
        )
        
        # Load tokenizer from adapter (it should have the same tokenizer as base)
        tokenizer = AutoTokenizer.from_pretrained(
            str(model_path),
            trust_remote_code=trust_remote_code
        )
        
        LOGGER.info(f"✅ Loaded base model + LoRA adapter (total ~13GB in memory, only 40MB on disk)")
        
    else:
        # Load as full model (either base model or merged model)
        LOGGER.info(f"📥 Loading full model from {model_path}")
        
        model = AutoModelForCausalLM.from_pretrained(
            str(model_path),
            torch_dtype=torch_dtype,
            device_map=device_map,
            trust_remote_code=trust_remote_code,
        )
        
        tokenizer = AutoTokenizer.from_pretrained(
            str(model_path),
            trust_remote_code=trust_remote_code
        )
        
        LOGGER.info(f"✅ Loaded full model")
    
    return model, tokenizer


def merge_lora_adapter_to_full_model(
    adapter_path: str,
    output_path: str,
    torch_dtype=torch.bfloat16,
) -> None:
    """
    Merge a LoRA adapter with its base model and save as a full model.
    
    Use this only for final deployment. During training/iteration, use adapters directly.
    
    Args:
        adapter_path: Path to LoRA adapter directory
        output_path: Path to save merged full model
        torch_dtype: Data type for model weights
    """
    adapter_path = Path(adapter_path)
    output_path = Path(output_path)
    
    if not is_lora_adapter(adapter_path):
        raise ValueError(f"{adapter_path} is not a LoRA adapter")
    
    LOGGER.info(f"🔄 Merging LoRA adapter to full model...")
    LOGGER.info(f"   Adapter: {adapter_path}")
    LOGGER.info(f"   Output: {output_path}")
    
    # Load base model
    base_model_name = get_base_model_for_adapter(adapter_path)
    LOGGER.info(f"📥 Loading base model: {base_model_name}")
    
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch_dtype,
        device_map="auto",
    )
    
    # Load adapter
    LOGGER.info(f"🔧 Loading LoRA adapter...")
    model = PeftModel.from_pretrained(base_model, str(adapter_path))
    
    # Merge
    LOGGER.info(f"🔄 Merging weights...")
    merged_model = model.merge_and_unload()
    
    # Save
    output_path.mkdir(parents=True, exist_ok=True)
    LOGGER.info(f"💾 Saving merged model to {output_path}")
    merged_model.save_pretrained(str(output_path))
    
    # Save tokenizer
    tokenizer = AutoTokenizer.from_pretrained(str(adapter_path))
    tokenizer.save_pretrained(str(output_path))
    
    LOGGER.info(f"✅ Merged model saved successfully (~13GB)")
    LOGGER.info(f"💡 Note: This is only needed for deployment. For training, use the adapter directly.")


if __name__ == "__main__":
    # Quick test
    import sys
    if len(sys.argv) < 2:
        print("Usage: python lora_loader.py <model_or_adapter_path> [--merge output_path]")
        print()
        print("Examples:")
        print("  # Test loading (no merge)")
        print("  python lora_loader.py initial_finetuned_models/7b_20251111/CodeLlama-7b-Instruct-hf")
        print()
        print("  # Merge adapter to full model")
        print("  python lora_loader.py adapter_path --merge output_path")
        sys.exit(1)
    
    model_path = sys.argv[1]
    
    if "--merge" in sys.argv:
        merge_idx = sys.argv.index("--merge")
        if merge_idx + 1 < len(sys.argv):
            output_path = sys.argv[merge_idx + 1]
            merge_lora_adapter_to_full_model(model_path, output_path)
        else:
            print("Error: --merge requires output path")
            sys.exit(1)
    else:
        # Just test loading
        print(f"Testing model loading from: {model_path}")
        model, tokenizer = load_model_for_inference(model_path)
        print(f"✅ Successfully loaded model")
        print(f"   Model type: {type(model)}")
        print(f"   Tokenizer vocab size: {len(tokenizer)}")

