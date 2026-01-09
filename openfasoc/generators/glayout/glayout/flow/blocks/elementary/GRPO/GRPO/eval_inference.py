#!/usr/bin/env python3
"""
GRPO Model Evaluation - Generate Parameter Sets for Transmission Gates
=======================================================================

Generates 20 VLSI parameter sets from the GRPO-trained model for evaluation.
Constrained for Transmission Gate (exactly 2 devices: NMOS + PMOS).
Tightened constraints based on training data analysis for optimal area.
"""

import json
import re
import torch
from pathlib import Path
from datetime import datetime

# Model path
MODEL_PATH = "grpo_standalone_outputs/run_20251130_062650/trained_model/merged"

# Format tokens (from grpo.py)
REASONING_START = "<start_working_out>"
REASONING_END = "<end_working_out>"
SOLUTION_START = "<SOLUTION>"
SOLUTION_END = "</SOLUTION>"

SYSTEM_PROMPT = f"""You are a VLSI circuit design expert specializing in Transmission Gate design.
A Transmission Gate has exactly 2 transistors: 1 NMOS and 1 PMOS.
Your goal is to minimize area while maintaining DRC/LVS compliance.
Think about the problem and provide your working out.
Place it between {REASONING_START} and {REASONING_END}.
Then, provide your optimized parameters in JSON format between {SOLUTION_START}{SOLUTION_END}"""


def extract_json_params(response: str) -> dict:
    """Extract JSON parameters from model response."""
    # Try to find JSON in SOLUTION tags first
    solution_match = re.search(
        rf"{SOLUTION_START}(.*?){SOLUTION_END}",
        response, re.DOTALL
    )
    if solution_match:
        text = solution_match.group(1)
    else:
        text = response
    
    # Find JSON object with nested structures
    json_patterns = [
        r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # Nested JSON
        r'\{[^{}]+\}',  # Simple JSON
    ]
    
    for pattern in json_patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            try:
                parsed = json.loads(match)
                # Check if it looks like VLSI parameters
                if any(k.lower() in ['width', 'length', 'fingers', 'multipliers'] for k in parsed.keys()):
                    return parsed
            except json.JSONDecodeError:
                continue
    
    return None


def validate_and_fix_params(params: dict) -> dict:
    """
    Validate and fix parameters for Transmission Gate.
    Ensures exactly 2 devices with TIGHT constraints based on training data analysis.
    
    Best training samples have:
    - Width: 0.5 - 3.0 μm (small values = low area)
    - Length: 0.15 - 2.5 μm
    - Fingers: 1-2 only (higher = more area)
    - Multipliers: always [1, 1]
    """
    if params is None:
        return None
    
    fixed = {}
    
    for key in ['width', 'length', 'fingers', 'multipliers']:
        key_lower = key.lower()
        # Find the key case-insensitively
        actual_key = None
        for k in params.keys():
            if k.lower() == key_lower:
                actual_key = k
                break
        
        if actual_key is None:
            return None  # Missing required parameter
        
        val = params[actual_key]
        
        if not isinstance(val, list):
            val = [val, val]  # Convert single value to pair
        
        # Ensure exactly 2 elements
        if len(val) < 2:
            val = [val[0], val[0]]
        elif len(val) > 2:
            val = val[:2]
        
        # Apply TIGHT constraints based on training data analysis
        if key_lower == 'width':
            # Width: 0.5 - 5.0 μm (best samples are 0.5-3.0)
            val = [max(0.5, min(5.0, float(v))) for v in val]
        elif key_lower == 'length':
            # Length: 0.15 - 2.5 μm
            val = [max(0.15, min(2.5, float(v))) for v in val]
        elif key_lower == 'fingers':
            # Fingers: 1-2 ONLY (higher = more area)
            val = [max(1, min(2, int(round(v)))) for v in val]
        elif key_lower == 'multipliers':
            # Multipliers: ALWAYS [1, 1] - training data shows this
            val = [1, 1]
        
        fixed[key] = val
    
    return fixed


def create_prompt(sample_id: int, base_params: dict) -> str:
    """Create a VLSI parameter optimization prompt for Transmission Gate."""
    return f"""Design VLSI Transmission Gate circuit: tg_sample_{sample_id:04d}

A Transmission Gate consists of exactly 2 transistors in (NMOS, PMOS) order.

Task: Generate OPTIMAL parameters to MINIMIZE AREA while passing DRC/LVS.
Current parameters:
{json.dumps(base_params, indent=2)}

Optimization goals (in priority order):
1. LVS compliance (6 nets, 4 devices)
2. DRC compliance
3. MINIMIZE AREA - use small widths and low finger counts
4. Good symmetry

CRITICAL constraints for minimal area:
- width: 0.5 - 5.0 μm (smaller = better)
- length: 0.15 - 2.5 μm  
- fingers: 1 or 2 ONLY (1 is best for area)
- multipliers: MUST be [1, 1]

Best designs have area < 500 μm². 
Provide your optimized parameters in JSON format."""


def generate_random_base_params(seed: int) -> dict:
    """Generate random base parameters for a Transmission Gate (2 devices)."""
    import random
    random.seed(seed)
    
    # Start with reasonable base params that might need optimization
    return {
        "width": [round(random.uniform(1.0, 4.0), 2), round(random.uniform(0.5, 3.0), 2)],
        "length": [round(random.uniform(0.3, 2.0), 2), round(random.uniform(0.2, 1.5), 2)],
        "fingers": [random.randint(1, 2), random.randint(1, 2)],
        "multipliers": [1, 1]
    }


def main():
    from unsloth import FastLanguageModel
    
    print("=" * 60)
    print("GRPO Model Evaluation - Transmission Gate (Tight Constraints)")
    print("=" * 60)
    print("Target: Area < 500 μm², fingers [1,1] or [1,2], multipliers [1,1]")
    print("=" * 60)
    
    # Load model
    print(f"\nLoading model from: {MODEL_PATH}")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=MODEL_PATH,
        max_seq_length=2048,
        load_in_4bit=True,
    )
    
    # Enable fast inference
    FastLanguageModel.for_inference(model)
    
    print("✅ Model loaded successfully!")
    
    # Generate 20 parameter sets
    num_samples = 20
    results = []
    
    print(f"\nGenerating {num_samples} Transmission Gate parameter sets...\n")
    
    for i in range(num_samples):
        sample_id = 1000 + i
        base_params = generate_random_base_params(seed=sample_id)
        
        # Create prompt
        user_content = create_prompt(sample_id, base_params)
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ]
        
        # Tokenize
        inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(model.device)
        
        # Generate with lower temperature for more conservative outputs
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_new_tokens=1024,
                temperature=0.5,  # Lower temperature for more focused outputs
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
            )
        
        # Decode
        response = tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
        
        # Extract and validate parameters
        raw_params = extract_json_params(response)
        validated_params = validate_and_fix_params(raw_params)
        
        result = {
            "sample_id": f"tg_sample_{sample_id:04d}",
            "input_params": base_params,
            "raw_extracted_params": raw_params,
            "generated_params": validated_params,
            "raw_response": response,
            "extraction_success": validated_params is not None
        }
        results.append(result)
        
        # Print progress
        status = "✅" if validated_params else "❌"
        print(f"[{i+1:2d}/{num_samples}] {status} tg_sample_{sample_id:04d}")
        if validated_params:
            print(f"         Parameters: {json.dumps(validated_params)}")
    
    # Summary
    success_count = sum(1 for r in results if r["extraction_success"])
    print(f"\n" + "=" * 60)
    print(f"Generation Complete!")
    print(f"Success rate: {success_count}/{num_samples} ({100*success_count/num_samples:.1f}%)")
    print("=" * 60)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"eval_params_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n📁 Full results saved to: {output_file}")
    
    # Also save just the parameters for easy evaluation
    params_only_file = f"eval_params_only_{timestamp}.json"
    params_only = []
    for r in results:
        if r["generated_params"]:
            params_only.append({
                "sample_id": r["sample_id"],
                "parameters": r["generated_params"]
            })
    
    with open(params_only_file, 'w') as f:
        json.dump(params_only, f, indent=2)
    print(f"📁 Parameters only saved to: {params_only_file}")
    
    # Print sample of valid parameters
    print(f"\n📋 Sample validated parameters:")
    for r in results[:5]:
        if r["generated_params"]:
            print(f"   {r['sample_id']}: {json.dumps(r['generated_params'])}")


if __name__ == "__main__":
    main()
