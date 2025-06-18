# OpenFASoC LLM Flow: Natural Language → Strict Syntax → Layout

## Complete Step-by-Step Guide

This guide demonstrates the complete flow from natural language prompts to actual circuit layouts using the OpenFASoC LLM system.

## Prerequisites

1. **Environment Setup**
   ```bash
   cd /home/arnavshukla/OpenFASOC/openfasoc/generators/glayout
   pip install -r requirements.txt
   pip install -r requirements.ml.txt
   ```

2. **Hugging Face Token**
   - Get token from: https://huggingface.co/settings/tokens
   - Set environment variable:
     ```bash
     export HF_TOKEN='your_token_here'
     ```

## Step 1: Training/Loading the LLM (One-time setup)

The LLM needs to be fine-tuned on circuit design data before first use:

```python
# Run this ONCE to fine-tune the model
from glayout.llm.train_and_run import run_full_SFT_training

# Fine-tune a 7B parameter model (recommended)
model, tokenizer = run_full_SFT_training(
    model="7b",  # Options: "3b", "7b", "22b" 
    accesstoken="your_hf_token"
)
```

This will:
- Download the base Mistral-7B model
- Load analog circuit design knowledge (RAG data)
- Fine-tune on Glayout syntax examples
- Save checkpoint for future use

## Step 2: Generate Strict Syntax from Natural Language

### Example 1: Simple Current Mirror

```python
from glayout.llm.train_and_run import GlayoutLLMSessionHandler

# Initialize the session (loads pre-trained model)
session = GlayoutLLMSessionHandler(
    model="7b", 
    accesstoken="your_hf_token"
)

# Natural language prompt
prompt = "Create a simple NMOS current mirror with parametrized width and length"

# Generate strict syntax
strict_syntax = session.generate(prompt)
print(strict_syntax)

# Save to .convo file
with open("CurrentMirror.convo", "w") as f:
    f.write("CurrentMirror\n")
    f.write(strict_syntax)
```

**Expected Output:**
```
// Simple NMOS Current Mirror
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
route between reference_source_S and mirror_source_S using smart_route
```

### Example 2: Differential Pair

```python
# Use the same session for multiple generations
prompt = "Make a P-type differential pair. Parametrize everything."
diff_pair_syntax = session.generate(prompt)

with open("DiffPair.convo", "w") as f:
    f.write("DiffPair\n")
    f.write(diff_pair_syntax)
```

## Step 3: Convert Strict Syntax to Layout

Once you have the .convo file with strict syntax, convert it to actual layout:

```python
from glayout.syntaxer.dynamic_load import run_session, show_glayout_code_cell
from glayout.flow.pdk.gf180_mapped import gf180_mapped_pdk

# Convert .convo file to Python Glayout code
code = run_session("CurrentMirror.convo", restore_and_exit=True)

# Generate and display the layout
component = show_glayout_code_cell(gf180_mapped_pdk, code)
```

This will:
- Parse the strict syntax commands
- Generate the corresponding Python Glayout code
- Create the actual geometric layout
- Display the layout visually

## Complete End-to-End Example

Here's a complete script that demonstrates the entire flow:

```python
#!/usr/bin/env python3
"""
Complete end-to-end example: Prompt → Syntax → Layout
"""

import os
from glayout.llm.train_and_run import GlayoutLLMSessionHandler
from glayout.syntaxer.dynamic_load import run_session, show_glayout_code_cell
from glayout.flow.pdk.gf180_mapped import gf180_mapped_pdk

def main():
    # Set your HF token
    hf_token = os.getenv('HF_TOKEN') or "your_token_here"
    
    # Step 1: Initialize LLM session
    print("🚀 Initializing LLM session...")
    session = GlayoutLLMSessionHandler(model="7b", accesstoken=hf_token)
    
    # Step 2: Generate strict syntax from natural language
    print("📝 Generating strict syntax...")
    prompt = "Create a simple NMOS current mirror with parametrized width and length"
    syntax = session.generate(prompt)
    
    print(f"Generated syntax:\n{syntax}")
    
    # Step 3: Save to .convo file
    convo_file = "example_current_mirror.convo"
    with open(convo_file, "w") as f:
        f.write("ExampleCurrentMirror\n")
        f.write(syntax)
    
    print(f"💾 Saved to {convo_file}")
    
    # Step 4: Convert to layout
    print("🏗️  Converting to layout...")
    code = run_session(convo_file, restore_and_exit=True)
    component = show_glayout_code_cell(gf180_mapped_pdk, code)
    
    print("✅ Layout generated and displayed!")

if __name__ == "__main__":
    main()
```

## RAG System Details

The LLM uses Retrieval Augmented Generation (RAG) to enhance prompts with relevant analog design knowledge:

1. **Knowledge Base** (`rag_data/`):
   - Circuit topology descriptions (current mirrors, diff pairs, etc.)
   - Design best practices and patterns
   - Glayout syntax reference documentation

2. **RAG Process**:
   - User prompt is embedded using sentence transformers
   - Most relevant documents retrieved from vector database
   - Retrieved knowledge added to LLM prompt context
   - Enhanced prompt generates more accurate strict syntax

## Example Natural Language Prompts

Here are various prompts you can try:

### Basic Circuits
- "Create a simple NMOS current mirror"
- "Make a P-type differential pair"
- "Build a common source amplifier"
- "Design an inverter with CMOS"

### With Parameters
- "Make a differential pair with parametrized width and length"
- "Create a current mirror with configurable mirror ratio"
- "Build a common source amp with parametrized load"

### Advanced Circuits
- "Design a two-stage operational amplifier"
- "Create a Wilson current mirror"
- "Build a strong-arm latch"
- "Make a regulated cascode current source"

### With Layout Specifications
- "Create a differential pair using common centroid layout"
- "Make a current mirror with interdigitated fingers"
- "Build an amplifier with folded topology"

## Validation and Testing

Validate generated .convo files:

```python
from glayout.llm.validate_synthetic_data import instantiate_convo, run_all_tests
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk

# Test a single .convo file
success = instantiate_convo(sky130_mapped_pdk, "CurrentMirror.convo")
print(f"Validation result: {success}")

# Test all .convo files in a directory
run_all_tests("./generated_circuits/")
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're in the correct directory and all dependencies are installed
2. **HF Token Issues**: Verify your token has access to the required models
3. **Memory Issues**: Use smaller models (3b) or increase swap space
4. **Syntax Errors**: The generated syntax might need manual review and correction

### Performance Tips

1. **Model Choice**:
   - 3b: Faster, less memory, slightly lower quality
   - 7b: Good balance (recommended)
   - 22b: Best quality, requires more resources

2. **Conversation History**: Use `session.clear_history()` to reset context

3. **Batch Processing**: Generate multiple circuits in one session for efficiency

## Next Steps

1. **Custom Training Data**: Add your own circuit examples to `syntax_data/`
2. **Extended RAG**: Add more design knowledge to `rag_data/`
3. **Model Fine-tuning**: Further customize the model for specific design styles
4. **Integration**: Incorporate into larger design automation workflows

This system bridges natural language circuit descriptions with precise layout generation, enabling more intuitive analog design workflows.
