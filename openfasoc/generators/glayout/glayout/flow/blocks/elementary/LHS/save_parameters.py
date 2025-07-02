#!/usr/bin/env python3
"""
Save generated LHS parameters to JSON files for use in GDS generation pipeline.
"""

import json
import os
from elhs import all_samples

def save_parameters():
    """Save all generated parameter sets to JSON files"""
    
    # Create output directory
    output_dir = "generated_parameters"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save each pcell's parameters
    for pcell, samples in all_samples.items():
        output_file = os.path.join(output_dir, f"{pcell}_parameters.json")
        
        print(f"Saving {len(samples)} parameter sets for {pcell} to {output_file}")
        
        with open(output_file, 'w') as f:
            json.dump(samples, f, indent=2)
    
    # Save a summary file
    summary = {
        "total_samples": sum(len(samples) for samples in all_samples.values()),
        "pcell_counts": {pcell: len(samples) for pcell, samples in all_samples.items()},
        "inventory_prescribed_counts": {
            'fvf': 11665,
            'txgate': 7777,
            'current_mirror': 7777,
            'diff_pair': 9721,
            'lvcm': 7777,
            'opamp': 17498,
        }
    }
    
    summary_file = os.path.join(output_dir, "generation_summary.json")
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nGeneration summary saved to {summary_file}")
    print(f"Total samples generated: {summary['total_samples']}")
    
    # Create a simple script to load parameters for each pcell
    loader_script = os.path.join(output_dir, "load_parameters.py")
    with open(loader_script, 'w') as f:
        f.write('''#!/usr/bin/env python3
"""
Helper script to load generated parameters for each pcell.
"""

import json
import os

def load_parameters(pcell):
    """Load parameters for a specific pcell"""
    current_dir = os.path.dirname(__file__)
    param_file = os.path.join(current_dir, f"{pcell}_parameters.json")
    
    if not os.path.exists(param_file):
        raise FileNotFoundError(f"Parameter file not found: {param_file}")
    
    with open(param_file, 'r') as f:
        return json.load(f)

def get_available_pcells():
    """Get list of available pcells"""
    current_dir = os.path.dirname(__file__)
    files = [f for f in os.listdir(current_dir) if f.endswith('_parameters.json')]
    return [f.replace('_parameters.json', '') for f in files]

# Example usage:
if __name__ == "__main__":
    available = get_available_pcells()
    print("Available PCells:", available)
    
    # Load parameters for FVF as example
    if 'fvf' in available:
        fvf_params = load_parameters('fvf')
        print(f"FVF: {len(fvf_params)} parameter sets")
        print("First FVF parameter set:", fvf_params[0])
''')
    
    print(f"Parameter loader script created: {loader_script}")

if __name__ == "__main__":
    save_parameters()
