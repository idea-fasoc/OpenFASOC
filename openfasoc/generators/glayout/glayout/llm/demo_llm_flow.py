#!/usr/bin/env python3
"""
Demo Script: Natural Language Prompt → Strict Syntax using LLM
=============================================================

This script demonstrates the complete flow from natural language prompts 
to Glayout strict syntax using the OpenFASoC LLM system.

Flow:
1. User provides natural language description of a circuit
2. LLM generates Glayout strict syntax
3. (Optional) Validate and convert to actual layout

Requirements:
- Hugging Face token for model access
- Installed dependencies (requirements.txt + requirements.ml.txt)
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path to import glayout modules
sys.path.insert(0, str(Path(__file__).parent.parent))

def check_requirements():
    """Check if all required dependencies are installed"""
    required_modules = [
        'transformers', 'torch', 'langchain', 'chromadb', 
        'sentence_transformers', 'peft', 'trl'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ Missing required modules: {', '.join(missing_modules)}")
        print("Please install requirements:")
        print("pip install -r requirements.txt")
        print("pip install -r requirements.ml.txt")
        return False
    
    print("✅ All required modules are installed")
    return True

def setup_environment():
    """Setup the environment and check for HF token"""
    # Check for Hugging Face token
    hf_token = os.getenv('HF_TOKEN') or os.getenv('HUGGINGFACE_HUB_TOKEN')
    
    if not hf_token:
        print("⚠️  No Hugging Face token found!")
        print("Please set your HF token:")
        print("export HF_TOKEN='your_token_here'")
        print("or")
        print("export HUGGINGFACE_HUB_TOKEN='your_token_here'")
        
        # Prompt for manual entry
        hf_token = input("\nEnter your HF token (or press Enter to continue without): ").strip()
        
        if not hf_token:
            print("⚠️  Continuing without HF token (may cause authentication errors)")
            hf_token = "dummy_token"
    
    return hf_token

def demonstrate_basic_usage():
    """Demonstrate basic usage of the LLM system"""
    print("\n" + "="*70)
    print("DEMONSTRATION: Natural Language → Strict Syntax")
    print("="*70)
    
    # Example prompts and expected outputs
    example_prompts = [
        {
            "prompt": "Create a simple current mirror with NMOS transistors",
            "description": "Basic current mirror circuit with two NMOS devices"
        },
        {
            "prompt": "Make a differential pair with PMOS transistors. Parametrize width and length.",
            "description": "P-type differential pair with parameterized dimensions"
        },
        {
            "prompt": "Build a common source amplifier with a diode-connected load",
            "description": "Common source amplifier topology"
        }
    ]
    
    print("\nExample Natural Language Prompts:")
    print("-" * 50)
    
    for i, example in enumerate(example_prompts, 1):
        print(f"\n{i}. Prompt: \"{example['prompt']}\"")
        print(f"   Description: {example['description']}")
    
    return example_prompts

def show_expected_strict_syntax():
    """Show examples of what the strict syntax should look like"""
    print("\n" + "="*70)
    print("EXPECTED STRICT SYNTAX OUTPUT")
    print("="*70)
    
    example_syntax = """
// Example: Differential Pair
// create parameters: vin1_width, vin2_width, vin1_length, vin2_length, vin1_multiplier, vin2_multiplier, vin1_fingers, vin2_fingers
create a float parameter called vin1_width
create a float parameter called vin2_width
create a float parameter called vin1_length
create a float parameter called vin2_length
create a int parameter called vin1_multiplier
create a int parameter called vin2_multiplier
create a int parameter called vin1_fingers
create a int parameter called vin2_fingers
// place
place a nmos called vin1 with width=vin1_width, length=vin1_length, fingers=vin1_fingers, rmult=1, multipliers=vin1_multiplier, with_substrate_tap=False, with_tie=True, with_dummy=True, with_dnwell=False
place a nmos called vin2 with width=vin2_width, length=vin2_length, fingers=vin2_fingers, rmult=1, multipliers=vin2_multiplier, with_substrate_tap=False, with_tie=True, with_dummy=True, with_dnwell=False
// move components for layout
move vin1 to the left of vin2
// routing connections
route between vin1_source_N and vin2_source_N using smart_route
"""
    
    print(example_syntax)

def demonstrate_with_actual_llm(hf_token, model_size="7b"):
    """Demonstrate with actual LLM (requires HF token)"""
    print("\n" + "="*70)
    print(f"RUNNING ACTUAL LLM DEMO (Model: {model_size})")
    print("="*70)
    
    try:
        # Import the actual LLM modules
        from train_and_run import GlayoutLLMSessionHandler
        
        print(f"🚀 Initializing LLM session handler with {model_size} model...")
        
        # Create session handler
        session = GlayoutLLMSessionHandler(
            model=model_size, 
            accesstoken=hf_token,
            converse_mode=False
        )
        
        print("✅ LLM session initialized successfully!")
        
        # Test with a simple prompt
        test_prompt = "Create a simple NMOS differential pair. Parametrize width and length."
        print(f"\n📝 Testing with prompt: \"{test_prompt}\"")
        print("\n🤔 Generating strict syntax...")
        
        # Generate strict syntax
        result = session.generate(test_prompt)
        
        print("\n📄 Generated Strict Syntax:")
        print("-" * 50)
        print(result)
        print("-" * 50)
        
        # Save to file
        output_file = Path(__file__).parent / "demo_output.convo"
        with open(output_file, "w") as f:
            f.write("DemoCircuit\n")
            f.write(result)
        
        print(f"\n💾 Output saved to: {output_file}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the correct directory and all dependencies are installed.")
        return False
    except Exception as e:
        print(f"❌ Error during LLM demonstration: {e}")
        print("This might be due to:")
        print("- Invalid or missing HF token")
        print("- Network connectivity issues")
        print("- Model download/loading issues")
        return False

def show_next_steps():
    """Show what to do after generating strict syntax"""
    print("\n" + "="*70)
    print("NEXT STEPS: Converting to Layout")
    print("="*70)
    
    next_steps = """
After generating the strict syntax (.convo file), you can convert it to an actual layout:

1. Using the Glayout syntaxer:
   ```python
   from glayout.syntaxer.dynamic_load import run_session, show_glayout_code_cell
   from glayout.flow.pdk.gf180_mapped import gf180_mapped_pdk
   
   # Convert .convo to Python code
   code = run_session("demo_output.convo", restore_and_exit=True)
   
   # Generate and display layout
   show_glayout_code_cell(gf180_mapped_pdk, code)
   ```

2. Manual inspection and validation:
   - Check the generated syntax for correctness
   - Verify parameter definitions
   - Ensure proper component placement and routing

3. Integration with larger systems:
   - Use the generated circuit as a component in larger designs
   - Combine multiple LLM-generated circuits
   - Optimize layouts for specific design requirements
"""
    
    print(next_steps)

def interactive_mode():
    """Interactive mode for testing custom prompts"""
    print("\n" + "="*70)
    print("INTERACTIVE MODE")
    print("="*70)
    
    print("Enter your custom circuit description prompts.")
    print("Type 'quit' to exit interactive mode.")
    
    while True:
        try:
            prompt = input("\n🎯 Enter circuit prompt: ").strip()
            
            if prompt.lower() in ['quit', 'exit', 'q']:
                print("👋 Exiting interactive mode...")
                break
                
            if not prompt:
                continue
                
            print(f"\n📝 Your prompt: \"{prompt}\"")
            print("\n💡 This would be processed by the LLM to generate strict syntax.")
            print("   (Run with actual LLM for real generation)")
            
        except KeyboardInterrupt:
            print("\n\n👋 Exiting interactive mode...")
            break

def main():
    """Main demonstration function"""
    print("🚀 OpenFASoC LLM Demonstration")
    print("Natural Language → Glayout Strict Syntax")
    print("=" * 70)
    
    # Check requirements
    if not check_requirements():
        return 1
    
    # Setup environment
    hf_token = setup_environment()
    
    # Show basic usage examples
    example_prompts = demonstrate_basic_usage()
    
    # Show expected syntax format
    show_expected_strict_syntax()
    
    # Ask user if they want to run actual LLM
    print("\n" + "="*70)
    print("ACTUAL LLM DEMONSTRATION")
    print("="*70)
    
    if hf_token and hf_token != "dummy_token":
        choice = input("\n🤖 Run actual LLM demonstration? (y/N): ").strip().lower()
        
        if choice in ['y', 'yes']:
            model_choice = input("Choose model size (3b/7b/22b) [7b]: ").strip() or "7b"
            success = demonstrate_with_actual_llm(hf_token, model_choice)
            
            if success:
                show_next_steps()
        else:
            print("⏭️  Skipping actual LLM demonstration")
    else:
        print("⚠️  Skipping actual LLM demonstration (no valid HF token)")
    
    # Interactive mode
    interactive_choice = input("\n🎮 Enter interactive mode? (y/N): ").strip().lower()
    if interactive_choice in ['y', 'yes']:
        interactive_mode()
    
    print("\n✨ Demo completed!")
    print("\nTo run the full flow:")
    print("1. Set up HF token: export HF_TOKEN='your_token'")
    print("2. Run: python demo_llm_flow.py")
    print("3. Follow the prompts to generate strict syntax")
    print("4. Use the generated .convo files with Glayout")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
