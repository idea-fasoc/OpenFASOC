#!/usr/bin/env python3
"""
Direct LLM Flow Demonstration
=============================

This script demonstrates the prompt → strict syntax flow using the actual
OpenFASoC LLM system components.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def setup_hf_token():
    """Setup Hugging Face token for model access"""
    # Check for existing token
    hf_token = os.getenv('HF_TOKEN') or os.getenv('HUGGINGFACE_HUB_TOKEN')
    
    if not hf_token:
        print("🔑 Hugging Face Token Required")
        print("=" * 50)
        print("To run the LLM, you need a Hugging Face token.")
        print("Get one at: https://huggingface.co/settings/tokens")
        print()
        
        token_input = input("Enter your HF token (or 'skip' to see demo without LLM): ").strip()
        
        if token_input.lower() == 'skip':
            return None
        
        if token_input:
            # Set the token for this session
            os.environ['HF_TOKEN'] = token_input
            return token_input
        else:
            return None
    
    return hf_token

def demonstrate_llm_generation(hf_token, model_size="7b"):
    """Demonstrate actual LLM generation"""
    print("\n🚀 LIVE LLM DEMONSTRATION")
    print("=" * 50)
    
    try:
        # Import LLM components
        from train_and_run import GlayoutLLMSessionHandler
        
        print(f"📡 Loading {model_size} model... (this may take a few minutes)")
        print("   The first run will download the model if not cached.")
        
        # Initialize the session handler
        session = GlayoutLLMSessionHandler(
            model=model_size,
            accesstoken=hf_token,
            converse_mode=False
        )
        
        print("✅ LLM loaded successfully!")
        
        # Test prompts
        test_prompts = [
            "Create a simple NMOS current mirror with parametrized width and length",
            "Make a P-type differential pair. Parametrize everything.",
            "Build a common source amplifier with diode load"
        ]
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n📝 Test {i}: {prompt}")
            print("-" * 60)
            
            try:
                # Generate strict syntax
                print("🤔 Generating strict syntax...")
                result = session.generate(prompt)
                
                print("📄 Generated Strict Syntax:")
                print(result)
                
                # Save to file
                output_file = current_dir / f"test_{i}_output.convo"
                with open(output_file, "w") as f:
                    f.write(f"TestCircuit{i}\n")
                    f.write(result)
                
                print(f"💾 Saved to: {output_file}")
                
                # Ask if user wants to continue
                if i < len(test_prompts):
                    continue_choice = input("\n⏭️  Continue to next test? (Y/n): ").strip().lower()
                    if continue_choice == 'n':
                        break
                        
            except Exception as e:
                print(f"❌ Error generating for prompt {i}: {e}")
                continue
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the glayout/llm directory")
        return False
    except Exception as e:
        print(f"❌ LLM error: {e}")
        return False

def interactive_generation(hf_token, model_size="7b"):
    """Interactive mode for custom prompts"""
    print("\n🎮 INTERACTIVE MODE")
    print("=" * 50)
    
    try:
        from train_and_run import GlayoutLLMSessionHandler
        
        print(f"📡 Loading {model_size} model for interactive use...")
        session = GlayoutLLMSessionHandler(
            model=model_size,
            accesstoken=hf_token,
            converse_mode=False
        )
        
        print("✅ Ready for interactive prompts!")
        print("Type 'quit' to exit, 'clear' to reset conversation history")
        
        while True:
            try:
                prompt = input("\n🎯 Enter circuit description: ").strip()
                
                if prompt.lower() in ['quit', 'exit', 'q']:
                    print("👋 Exiting interactive mode...")
                    break
                    
                if prompt.lower() == 'clear':
                    session.clear_history()
                    print("🗑️  Conversation history cleared")
                    continue
                    
                if not prompt:
                    continue
                
                print("🤔 Generating...")
                result = session.generate(prompt)
                
                print("\n📄 Generated Strict Syntax:")
                print("-" * 40)
                print(result)
                print("-" * 40)
                
                # Option to save
                save_choice = input("\n💾 Save to file? (y/N): ").strip().lower()
                if save_choice == 'y':
                    filename = input("Enter filename (without .convo): ").strip() or "custom_circuit"
                    output_file = current_dir / f"{filename}.convo"
                    with open(output_file, "w") as f:
                        f.write(f"{filename}\n")
                        f.write(result)
                    print(f"💾 Saved to: {output_file}")
                
            except KeyboardInterrupt:
                print("\n👋 Exiting interactive mode...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
                
    except Exception as e:
        print(f"❌ Error setting up interactive mode: {e}")

def show_manual_examples():
    """Show manual examples of the expected flow"""
    print("\n📚 MANUAL EXAMPLES")
    print("=" * 50)
    
    examples = [
        {
            "prompt": "Create a simple NMOS current mirror",
            "syntax": """// Simple NMOS Current Mirror
create a float parameter called ref_width
create a float parameter called mir_width  
create a float parameter called transistor_length
create a int parameter called ref_fingers
create a int parameter called mir_fingers

place a nmos called reference with width=ref_width, length=transistor_length, fingers=ref_fingers, rmult=1, multipliers=1, with_substrate_tap=False, with_tie=True, with_dummy=True, with_dnwell=False
place a nmos called mirror with width=mir_width, length=transistor_length, fingers=mir_fingers, rmult=1, multipliers=1, with_substrate_tap=False, with_tie=True, with_dummy=True, with_dnwell=False

move reference to the left of mirror

route between reference_gate_W and mirror_gate_E using smart_route
route between reference_drain_N and reference_gate_W using smart_route  
route between reference_source_S and mirror_source_S using smart_route"""
        },
        {
            "prompt": "Make a P-type differential pair",
            "syntax": """// P-type Differential Pair
create a float parameter called vin1_width
create a float parameter called vin2_width
create a float parameter called transistor_length
create a int parameter called vin1_fingers  
create a int parameter called vin2_fingers

place a pmos called vin1 with width=vin1_width, length=transistor_length, fingers=vin1_fingers, rmult=1, multipliers=1, with_substrate_tap=False, with_tie=True, with_dummy=True, with_dnwell=False
place a pmos called vin2 with width=vin2_width, length=transistor_length, fingers=vin2_fingers, rmult=1, multipliers=1, with_substrate_tap=False, with_tie=True, with_dummy=True, with_dnwell=False

move vin1 to the left of vin2

route between vin1_source_N and vin2_source_N using smart_route"""
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. Natural Language Prompt:")
        print(f"   \"{example['prompt']}\"")
        print("\n   Expected Strict Syntax:")
        print("   " + "-" * 40)
        for line in example['syntax'].split('\n'):
            print(f"   {line}")
        print("   " + "-" * 40)

def main():
    """Main demonstration function"""
    print("🔬 OpenFASoC LLM: Prompt → Strict Syntax Demo")
    print("=" * 60)
    
    # Show manual examples first
    show_manual_examples()
    
    # Setup HF token
    hf_token = setup_hf_token()
    
    if not hf_token:
        print("\n⏭️  Skipping live LLM demonstration")
        print("   (Re-run with HF token to see actual LLM generation)")
        return 0
    
    # Choose demonstration mode
    print("\n🎛️  DEMONSTRATION OPTIONS")
    print("=" * 50)
    print("1. Automated tests with preset prompts")
    print("2. Interactive mode (custom prompts)")
    print("3. Skip LLM demo")
    
    choice = input("\nChoose option (1/2/3): ").strip()
    
    model_size = "7b"  # Default model
    
    if choice == "1":
        demonstrate_llm_generation(hf_token, model_size)
    elif choice == "2":
        interactive_generation(hf_token, model_size)
    else:
        print("⏭️  Skipping LLM demonstration")
    
    print("\n✨ Demonstration completed!")
    print("\n📋 Summary of the flow:")
    print("   1. Natural language prompt (e.g., 'Create a current mirror')")
    print("   2. LLM processes with RAG context")  
    print("   3. Generated Glayout strict syntax")
    print("   4. Save to .convo file")
    print("   5. Use with Glayout to create actual layout")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
