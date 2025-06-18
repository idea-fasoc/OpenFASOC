#!/usr/bin/env python3
"""
Working LLM Demo
================

This demonstrates the LLM flow without requiring full glayout installation.
We'll modify the imports to work with the current directory structure.
"""

import os
import sys
from pathlib import Path

# Add the parent directories to Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent  # Go up to generators/glayout
sys.path.insert(0, str(parent_dir))

def create_simplified_demo():
    """Create a simplified demo that shows the expected flow"""
    
    print("🔬 OpenFASoC LLM Flow Demonstration")
    print("=" * 50)
    
    # Step 1: Show the natural language prompts
    prompts = [
        {
            "id": 1,
            "prompt": "Create a simple NMOS current mirror with parametrized width and length",
            "category": "Current Sources"
        },
        {
            "id": 2, 
            "prompt": "Make a P-type differential pair. Parametrize everything.",
            "category": "Amplifiers"
        },
        {
            "id": 3,
            "prompt": "Build a common source amplifier with diode load",
            "category": "Amplifiers"
        }
    ]
    
    print("\n📝 Example Natural Language Prompts:")
    print("-" * 40)
    for p in prompts:
        print(f"{p['id']}. {p['prompt']}")
        print(f"   Category: {p['category']}")
        print()
    
    # Step 2: Show the RAG process
    print("🧠 RAG (Retrieval Augmented Generation) Process:")
    print("-" * 50)
    print("1. User prompt is processed by sentence transformer")
    print("2. Relevant design knowledge retrieved from vector DB")
    print("3. Retrieved context enhances the LLM prompt")
    print("4. LLM generates strict syntax with domain knowledge")
    
    # Step 3: Show example outputs
    example_outputs = {
        1: """// NMOS Current Mirror
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
route between reference_source_S and mirror_source_S using smart_route""",
        
        2: """// P-type Differential Pair  
create a float parameter called vin1_width
create a float parameter called vin2_width
create a float parameter called transistor_length
create a int parameter called vin1_fingers
create a int parameter called vin2_fingers
create a int parameter called vin1_multiplier
create a int parameter called vin2_multiplier

place a pmos called vin1 with width=vin1_width, length=transistor_length, fingers=vin1_fingers, rmult=1, multipliers=vin1_multiplier, with_substrate_tap=False, with_tie=True, with_dummy=True, with_dnwell=False
place a pmos called vin2 with width=vin2_width, length=transistor_length, fingers=vin2_fingers, rmult=1, multipliers=vin2_multiplier, with_substrate_tap=False, with_tie=True, with_dummy=True, with_dnwell=False

move vin1 to the left of vin2

route between vin1_source_N and vin2_source_N using smart_route"""
    }
    
    print("\n📄 Generated Strict Syntax Examples:")
    print("-" * 50)
    
    for prompt_id, output in example_outputs.items():
        prompt_text = next(p['prompt'] for p in prompts if p['id'] == prompt_id)
        print(f"\nPrompt {prompt_id}: \"{prompt_text}\"")
        print("\nGenerated Strict Syntax:")
        print("```")
        print(output)
        print("```")
        print()
    
    # Step 4: Save example outputs
    print("💾 Saving Example Outputs:")
    print("-" * 30)
    
    for prompt_id, output in example_outputs.items():
        filename = f"example_{prompt_id}.convo"
        circuit_name = ["", "CurrentMirror", "DiffPair"][prompt_id]
        
        with open(filename, "w") as f:
            f.write(f"{circuit_name}\n")
            f.write(output)
        
        print(f"✅ Saved: {filename}")
    
    # Step 5: Show next steps
    print("\n🎯 Next Steps - Converting to Layout:")
    print("-" * 40)
    conversion_code = """# Convert .convo file to actual layout
from glayout.syntaxer.dynamic_load import run_session, show_glayout_code_cell
from glayout.flow.pdk.gf180_mapped import gf180_mapped_pdk

# Convert strict syntax to Python code
code = run_session("example_1.convo", restore_and_exit=True)

# Generate and display layout
component = show_glayout_code_cell(gf180_mapped_pdk, code)
component.show()  # Display the layout"""
    
    print(conversion_code)
    
    return True

def show_actual_llm_setup():
    """Show how to set up the actual LLM"""
    print("\n🚀 Setting Up Actual LLM Generation:")
    print("=" * 50)
    
    setup_code = """# 1. Set up environment
export HF_TOKEN='your_huggingface_token'

# 2. Install dependencies (if not already done)
pip install -r requirements.txt
pip install -r requirements.ml.txt

# 3. One-time model training/fine-tuning
python -c "
from glayout.llm.train_and_run import run_full_SFT_training
run_full_SFT_training(model='7b', accesstoken='your_token')
"

# 4. Generate strict syntax from prompts
python -c "
from glayout.llm.train_and_run import GlayoutLLMSessionHandler

session = GlayoutLLMSessionHandler(model='7b', accesstoken='your_token')
result = session.generate('Create a simple NMOS current mirror')
print(result)

with open('my_circuit.convo', 'w') as f:
    f.write('MyCircuit\\n' + result)
"

# 5. Convert to layout
python -c "
from glayout.syntaxer.dynamic_load import run_session, show_glayout_code_cell
from glayout.flow.pdk.gf180_mapped import gf180_mapped_pdk

code = run_session('my_circuit.convo', restore_and_exit=True)
show_glayout_code_cell(gf180_mapped_pdk, code)
\""""
    
    print(setup_code)

def explore_training_data():
    """Show the training data that teaches the LLM"""
    print("\n📚 Training Data Overview:")
    print("=" * 40)
    
    # Check if training data exists
    rag_data_dir = Path("rag_data")
    syntax_data_dir = Path("syntax_data")
    
    if rag_data_dir.exists():
        print(f"\n🧠 RAG Knowledge Base ({rag_data_dir}):")
        rag_files = list(rag_data_dir.glob("*.md"))
        for i, f in enumerate(rag_files[:5], 1):
            print(f"  {i}. {f.name} - Analog design knowledge")
        if len(rag_files) > 5:
            print(f"  ... and {len(rag_files) - 5} more files")
    
    if syntax_data_dir.exists():
        print(f"\n📝 Training Examples ({syntax_data_dir}):")
        training_files = list(syntax_data_dir.glob("*.json"))
        convo_files = list((syntax_data_dir / "convos").glob("*.convo"))
        
        print(f"  - {len(training_files)} JSON training files")
        print(f"  - {len(convo_files)} example .convo files")
        
        # Show a few example files
        if convo_files:
            print("\n  Example circuits in training data:")
            for i, f in enumerate(convo_files[:8], 1):
                name = f.stem.replace('_', ' ')
                print(f"    {i}. {name}")
            if len(convo_files) > 8:
                print(f"    ... and {len(convo_files) - 8} more")

def main():
    """Main demonstration"""
    # Create the basic demonstration
    create_simplified_demo()
    
    # Show training data
    explore_training_data()
    
    # Show actual LLM setup
    show_actual_llm_setup()
    
    print("\n✨ Demo Complete!")
    print("\nSummary of the Flow:")
    print("1. 📝 Natural language prompt (e.g., 'Create a current mirror')")
    print("2. 🧠 RAG retrieves relevant design knowledge") 
    print("3. 🤖 LLM generates Glayout strict syntax")
    print("4. 💾 Save to .convo file")
    print("5. 🏗️  Convert to actual circuit layout")
    print()
    print("Files created in this demo:")
    created_files = ["example_1.convo", "example_2.convo"]
    for f in created_files:
        if os.path.exists(f):
            print(f"  ✅ {f}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
