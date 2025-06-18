#!/usr/bin/env python3
"""
Complete LLM Demo - Shows the actual prompt → strict syntax flow
This uses the real trained model if HF token is provided
"""

import sys
import os
from pathlib import Path

sys.path.append('.')

def demonstrate_complete_flow():
    """Demonstrate the complete flow using actual components"""
    
    print("=" * 70)
    print("OpenFASoC LLM - COMPLETE DEMONSTRATION")
    print("Prompt → RAG Retrieval → LLM Generation → Strict Syntax")
    print("=" * 70)
    
    # Step 1: Show RAG knowledge retrieval
    print("\n1. RAG KNOWLEDGE RETRIEVAL")
    print("-" * 35)
    
    try:
        from rag import RAGdb
        
        rag_dir = Path("rag_data")
        rag = RAGdb(rag_data_dir=rag_dir)
        
        test_prompt = "Create a differential pair with NMOS transistors"
        print(f"User Prompt: '{test_prompt}'")
        print("\nRetrieving relevant knowledge...")
        
        # Query RAG for relevant knowledge
        rag_results = rag.query("differential pair NMOS transistors", k=2)
        
        print("Retrieved Knowledge:")
        for i, result in enumerate(rag_results[:2], 1):
            if result and result != "None":
                preview = result.replace('\n', ' ')[:200]
                print(f"  {i}. {preview}...")
        
        print("✓ RAG retrieval successful!")
        
    except Exception as e:
        print(f"❌ RAG error: {e}")
        rag_results = None
    
    # Step 2: Check for trained model
    print("\n2. LLM MODEL STATUS")
    print("-" * 25)
    
    checkpoint_dir = Path("glayout_llm_checkpointsphi")
    if checkpoint_dir.exists():
        checkpoints = list(checkpoint_dir.glob("checkpoint-*"))
        print(f"✓ Found trained model with {len(checkpoints)} checkpoints")
        print(f"  Latest checkpoint: {checkpoint_dir}")
    else:
        print("⚠️  No trained checkpoint found")
    
    # Step 3: Demonstrate LLM generation
    print("\n3. LLM GENERATION")
    print("-" * 20)
    
    hf_token = os.environ.get('HF_TOKEN')
    if not hf_token:
        hf_token = "your_hf_token_here"  # Replace with your token
    
    if hf_token != "your_hf_token_here":
        print("Attempting to use actual LLM...")
        try:
            result = run_actual_llm(hf_token, test_prompt)
            if result:
                print("✓ Successfully generated strict syntax using actual LLM!")
                return result
        except Exception as e:
            print(f"❌ LLM error: {e}")
    
    # Fallback: Show expected output based on training data
    print("Using training data to show expected output...")
    result = demonstrate_expected_output(test_prompt)
    return result

def run_actual_llm(hf_token, prompt):
    """Run the actual LLM if token is provided"""
    
    from train_and_run import GlayoutLLMSessionHandler
    
    print("Loading LLM session (this may take a few minutes)...")
    session = GlayoutLLMSessionHandler(
        model="7b",  # Mistral 7B
        accesstoken=hf_token,
        converse_mode=False
    )
    
    # Checkpoint loading is handled automatically in the constructor
    
    print(f"Generating strict syntax for: '{prompt}'")
    result = session.generate(prompt)
    
    print("\nGenerated Strict Syntax:")
    print("-" * 40)
    print(result)
    print("-" * 40)
    
    # Save result
    with open("llm_output.convo", 'w') as f:
        f.write("LLMOutput\n" + result)
    print("✓ Saved to llm_output.convo")
    
    return result

def demonstrate_expected_output(prompt):
    """Show what the output should look like based on training data"""
    
    print(f"Input Prompt: '{prompt}'")
    print("\nExpected Strict Syntax Output:")
    print("-" * 40)
    
    # Load an example from training data
    try:
        convo_file = Path("syntax_data/convos/DiffPair.convo")
        if convo_file.exists():
            with open(convo_file, 'r') as f:
                content = f.read()
            print(content)
            
            # Also save as example
            with open("expected_output.convo", 'w') as f:
                f.write(content)
            print("✓ Saved expected output to expected_output.convo")
            
            return content
        else:
            print("Training data not found")
            return None
            
    except Exception as e:
        print(f"Error loading training data: {e}")
        return None

def show_validation_process():
    """Show how to validate the generated syntax"""
    
    print("\n4. VALIDATION PROCESS")
    print("-" * 25)
    
    print("To validate generated .convo files:")
    print("1. Run: python validate_synthetic_data.py")
    print("2. This will attempt to instantiate layouts from the .convo files")
    print("3. Successful validation means the syntax is correct")
    
    # Try to run validation on existing files
    try:
        from validate_synthetic_data import instantiate_convo
        from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
        
        test_files = ["llm_output.convo", "expected_output.convo", "simulated_diffpair.convo"]
        
        print("\nValidating generated files:")
        for test_file in test_files:
            if Path(test_file).exists():
                print(f"  Testing {test_file}...")
                try:
                    result = instantiate_convo(sky130_mapped_pdk, test_file)
                    if result:
                        print(f"    ✓ {test_file} is valid!")
                    else:
                        print(f"    ❌ {test_file} failed validation")
                except Exception as e:
                    print(f"    ❌ {test_file} error: {e}")
    
    except Exception as e:
        print(f"Validation test error: {e}")

def main():
    """Main demonstration"""
    
    result = demonstrate_complete_flow()
    show_validation_process()
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE!")
    print("\nThis shows the complete flow:")
    print("1. Natural language prompt")
    print("2. RAG knowledge retrieval")
    print("3. LLM processing with context")
    print("4. Strict syntax generation")
    print("5. Validation and layout generation")
    print("\nTo run with your own prompts:")
    print("- Set HF_TOKEN environment variable")
    print("- Run: python simple_llm_test.py")
    print("=" * 70)

if __name__ == "__main__":
    main()
