#!/usr/bin/env python3
"""
Standalone GRPO Training Runner
===============================

This script runs GRPO training using the existing grpo.py implementation.
It works with the existing output.json data and a base model.

Usage:
------
python run_grpo.py --base_model codellama/CodeLlama-7b-Instruct-hf --num_samples 100

Or with a LoRA adapter:
python run_grpo.py --base_model ./initial_finetuned_models/7b_20251129_141949/CodeLlama-7b-Instruct-hf --num_samples 100
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime

# Import the existing grpo_trainer
from grpo import grpo_trainer


def main():
    parser = argparse.ArgumentParser(description="Run GRPO Training")
    
    # Model configuration
    parser.add_argument("--base_model", type=str, 
                       default="codellama/CodeLlama-7b-Instruct-hf",
                       help="Base model path or HuggingFace model ID")
    
    # Data configuration
    parser.add_argument("--input_json", type=str, default="output.json",
                       help="Path to input JSON with VLSI evaluation data")
    parser.add_argument("--num_samples", type=int, default=None,
                       help="Number of samples to use (None = all)")
    
    # Training configuration
    parser.add_argument("--num_epochs", type=int, default=3,
                       help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=4,
                       help="Batch size (gradient accumulation steps)")
    parser.add_argument("--learning_rate", type=float, default=5e-6,
                       help="Learning rate")
    parser.add_argument("--group_size", type=int, default=4,
                       help="Number of generations per prompt for GRPO")
    parser.add_argument("--kl_coef", type=float, default=0.1,
                       help="KL divergence coefficient")
    
    # LoRA configuration
    parser.add_argument("--lora_r", type=int, default=64,
                       help="LoRA rank")
    parser.add_argument("--lora_alpha", type=int, default=64,
                       help="LoRA alpha")
    parser.add_argument("--lora_dropout", type=float, default=0.05,
                       help="LoRA dropout")
    
    # Output configuration
    parser.add_argument("--output_dir", type=str, default="grpo_standalone_outputs",
                       help="Output directory for trained model")
    
    args = parser.parse_args()
    
    # Create output directory with timestamp
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(args.output_dir) / f"run_{run_id}"
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("GRPO Training Runner")
    print("=" * 60)
    print(f"Base Model: {args.base_model}")
    print(f"Input JSON: {args.input_json}")
    print(f"Output Dir: {output_path}")
    print(f"Num Epochs: {args.num_epochs}")
    print(f"Batch Size: {args.batch_size}")
    print(f"Group Size: {args.group_size}")
    print(f"Learning Rate: {args.learning_rate}")
    print("=" * 60)
    
    # Load data
    print(f"\nLoading data from {args.input_json}...")
    with open(args.input_json, 'r') as f:
        data = json.load(f)
    
    if isinstance(data, dict):
        data = [data]
    
    # Optionally limit samples
    if args.num_samples and args.num_samples < len(data):
        data = data[:args.num_samples]
        print(f"Using first {args.num_samples} samples")
    else:
        print(f"Using all {len(data)} samples")
    
    # Save the subset for reproducibility
    subset_file = output_path / "training_data.json"
    with open(subset_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved training data subset to {subset_file}")
    
    # Initialize trainer
    print("\nInitializing GRPO Trainer...")
    trainer = grpo_trainer(
        model_name=args.base_model,
        learning_rate=args.learning_rate,
        group_size=args.group_size,
        kl_coef=args.kl_coef,
        lora_r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
    )
    
    # Run training
    print("\nStarting GRPO training...")
    trainer.train(
        json_files=[str(subset_file)],
        num_epochs=args.num_epochs,
        batch_size=args.batch_size,
        save_path=str(output_path / "trained_model"),
    )
    
    print("\n" + "=" * 60)
    print("GRPO Training Complete!")
    print(f"Model saved to: {output_path / 'trained_model'}")
    print("=" * 60)


if __name__ == "__main__":
    main()

