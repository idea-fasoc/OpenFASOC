#!/usr/bin/env python3
"""
Simple LLM Inference Script
Run this with your HF token to test actual prompt → strict syntax generation
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append('.')

def run_llm_inference(hf_token, prompt):
    """Run actual LLM inference with the given prompt"""
    
    print("=" * 60)
    print("OpenFASoC LLM - Real Inference")
    print("=" * 60)
    
    try:
        # Import the LLM system
        from train_and_run import GlayoutLLMSessionHandler
        
        print("1. Loading LLM session...")
        print("   This may take a few minutes for first-time model download...")
        
        # Initialize session with 7B model (Mistral)
        session = GlayoutLLMSessionHandler(
            model="7b",
            accesstoken=hf_token,
            converse_mode=False
        )
        
        # Check for existing checkpoint
        checkpoint_dir = "glayout_llm_checkpointsphi"
        if Path(checkpoint_dir).exists():
            print(f"   Loading fine-tuned checkpoint: {checkpoint_dir}")
            session.load_model_from_checkpoint(checkpoint_dir)
        else:
            print("   Using base model (no fine-tuned checkpoint found)")
        
        print("✓ LLM session ready!")
        
        print(f"\n2. Processing prompt:")
        print(f"   '{prompt}'")
        
        print("\n3. Generating strict syntax...")
        result = session.generate(prompt)
        
        print("\n4. Generated Strict Syntax:")
        print("-" * 50)
        print(result)
        print("-" * 50)
        
        # Save result
        output_file = "llm_generated.convo"
        with open(output_file, 'w') as f:
            f.write("LLMGenerated\n" + result)
        
        print(f"\n✓ Saved to {output_file}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main function"""
    
    # Get HF token from environment or user input
    hf_token = os.environ.get('HF_TOKEN')
    
    if not hf_token:
        print("Please provide your Hugging Face token:")
        print("Option 1: Set environment variable: export HF_TOKEN=your_token")
        print("Option 2: Edit this script and set token below")
        print()
        
        # You can set your token here instead of using environment variable
        hf_token = "your_hf_token_here"  # Replace with your actual token
        
        if hf_token == "your_hf_token_here":
            print("❌ No Hugging Face token provided!")
            print("Get one from: https://huggingface.co/settings/tokens")
            return
    
    # Test prompts
    test_prompts = [
        "Create a differential pair with NMOS transistors. Parametrize width and length.",
        "Build a current mirror using PMOS transistors.",
        "Design a common source amplifier with NMOS input transistor."
    ]
    
    print("Available test prompts:")
    for i, prompt in enumerate(test_prompts, 1):
        print(f"{i}. {prompt}")
    
    print("\nChoose a prompt (1-3) or enter your own:")
    choice = input("> ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(test_prompts):
        prompt = test_prompts[int(choice) - 1]
    else:
        prompt = choice if choice else test_prompts[0]
    
    # Run inference
    result = run_llm_inference(hf_token, prompt)
    
    if result:
        print("\n" + "=" * 60)
        print("SUCCESS! LLM generated strict syntax.")
        print("You can now validate with: python validate_synthetic_data.py")
        print("=" * 60)

if __name__ == "__main__":
    main()
