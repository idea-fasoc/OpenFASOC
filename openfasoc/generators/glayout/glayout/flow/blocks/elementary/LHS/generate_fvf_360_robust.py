#!/usr/bin/env python3
"""
Robust FVF Dataset Generator for 360 samples.
Based on the successful approach used for the 50-sample generation.
"""

import logging
import os
import sys
import time
import json
import shutil
from pathlib import Path
import numpy as np
import pandas as pd

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Set up the environment for glayout"""
    # Add glayout to Python path
    glayout_path = "/home/adityakak/OpenFASOC/openfasoc/generators/glayout"
    if glayout_path not in sys.path:
        sys.path.insert(0, glayout_path)
    
    # Set PDK_ROOT if not already set
    if 'PDK_ROOT' not in os.environ:
        os.environ['PDK_ROOT'] = '/usr/bin/miniconda3/share/pdk'
    
    # Set PYTHONPATH
    current_pythonpath = os.environ.get('PYTHONPATH', '')
    if glayout_path not in current_pythonpath:
        os.environ['PYTHONPATH'] = f"{glayout_path}:{current_pythonpath}"

def test_imports():
    """Test that all required imports work"""
    try:
        # Test gdsfactory
        from gdsfactory.typings import Component
        logger.info("✓ gdsfactory import successful")
        
        # Test glayout
        from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
        logger.info("✓ glayout PDK import successful")
        
        # Skip FVF import test to avoid PrettyPrint dependency
        # We'll test it when actually generating samples
        logger.info("✓ Skipping FVF block import test (will test during generation)")
        
        return True
    except Exception as e:
        logger.error(f"Import test failed: {e}")
        return False

def load_parameters():
    """Load the pre-generated 360 parameter combinations"""
    try:
        params_file = "generated_parameters/fvf_parameters.json"
        with open(params_file, 'r') as f:
            parameters = json.load(f)
        logger.info(f"Loaded {len(parameters)} parameter combinations from {params_file}")
        return parameters
    except Exception as e:
        logger.error(f"Failed to load parameters: {e}")
        return None

def generate_single_fvf(params, sample_id, output_dir):
    """Generate a single FVF sample with proper error handling"""
    try:
        # Import here to avoid import issues during setup
        # Re-import each time to avoid module caching issues  
        import importlib
        if 'glayout.flow.blocks.elementary.FVF.fvf' in sys.modules:
            importlib.reload(sys.modules['glayout.flow.blocks.elementary.FVF.fvf'])
        from glayout.flow.blocks.elementary.FVF.fvf import fvf
        from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
        
        # Extract parameters (using correct FVF parameter names)
        nf_out = params['nf_out']
        m_out = params['m_out']
        nf_diff = params['nf_diff'] 
        m_diff = params['m_diff']
        
        component_name = f"fvf_sample_{sample_id:04d}"
        
        # Create the FVF component
        start_time = time.time()
        
        # Generate the FVF block with correct parameters
        fvf_component = fvf(
            pdk=sky130_mapped_pdk,
            nf_out=nf_out,
            m_out=m_out,
            nf_diff=nf_diff, 
            m_diff=m_diff
        )
        
        execution_time = time.time() - start_time
        
        # Create sample directory
        sample_dir = output_dir / f"sample_{sample_id:04d}"
        sample_dir.mkdir(parents=True, exist_ok=True)
        
        # Save the GDS file
        gds_file = sample_dir / f"{component_name}.gds"
        fvf_component.write_gds(str(gds_file))
        
        # Create component info
        component_info = {
            'component_name': component_name,
            'gds_file': str(gds_file),
            'parameters': params,
            'execution_time': execution_time
        }
        
        # Save component info
        info_file = sample_dir / f"{component_name}_info.json"
        with open(info_file, 'w') as f:
            json.dump(component_info, f, indent=2)
        
        logger.info(f"✓ Sample {sample_id:04d} generated successfully in {execution_time:.2f}s")
        
        return {
            'sample_id': sample_id,
            'component_name': component_name,
            'success': True,
            'execution_time': execution_time,
            'parameters': params,
            'output_files': {
                'gds': str(gds_file),
                'info': str(info_file)
            }
        }
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"✗ Sample {sample_id:04d} failed: {error_msg}")
        
        return {
            'sample_id': sample_id,
            'component_name': f"fvf_sample_{sample_id:04d}",
            'success': False,
            'error': error_msg,
            'execution_time': time.time() - start_time if 'start_time' in locals() else 0,
            'parameters': params
        }

def main():
    """Main function to generate the 360 FVF dataset"""
    
    print("🚀 Starting FVF 360 Dataset Generation")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Test imports
    if not test_imports():
        print("❌ Environment setup failed. Please check dependencies.")
        return
    
    # Load parameters
    parameters = load_parameters()
    if parameters is None:
        print("❌ Failed to load parameters.")
        return
    
    # Create output directory
    output_dir = Path("fvf_dataset_360_fresh")
    output_dir.mkdir(exist_ok=True)
    
    # Initialize results tracking
    results = []
    
    print(f"📊 Generating {len(parameters)} FVF samples...")
    print("-" * 50)
    
    # Generate samples
    for i, params in enumerate(parameters, 1):
        print(f"Processing sample {i:3d}/{len(parameters)}", end=" ... ")
        
        result = generate_single_fvf(params, i, output_dir)
        results.append(result)
        
        # Progress update
        if i % 10 == 0:
            success_count = sum(1 for r in results if r['success'])
            print(f"\n📈 Progress: {i}/{len(parameters)} samples | ✓ {success_count} successful")
    
    # Save results
    results_file = output_dir / "fvf_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Save parameters used
    params_used_file = output_dir / "fvf_parameters_used.json"
    with open(params_used_file, 'w') as f:
        json.dump(parameters, f, indent=2)
    
    # Generate summary
    success_count = sum(1 for r in results if r['success'])
    failure_count = len(results) - success_count
    
    summary = {
        'total_samples': len(results),
        'successful_samples': success_count,
        'failed_samples': failure_count,
        'success_rate': success_count / len(results) * 100,
        'total_execution_time': sum(r['execution_time'] for r in results),
        'avg_execution_time': sum(r['execution_time'] for r in results) / len(results)
    }
    
    # Save summary
    summary_file = output_dir / "fvf_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Create CSV summary
    df = pd.DataFrame(results)
    csv_file = output_dir / "fvf_summary.csv"
    df.to_csv(csv_file, index=False)
    
    # Final report
    print("\n" + "=" * 50)
    print("🎯 FVF 360 Dataset Generation Complete!")
    print("=" * 50)
    print(f"📊 Total samples: {summary['total_samples']}")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {failure_count}")
    print(f"📈 Success rate: {summary['success_rate']:.1f}%")
    print(f"⏱️  Total time: {summary['total_execution_time']:.1f}s")
    print(f"⚡ Avg time per sample: {summary['avg_execution_time']:.2f}s")
    print(f"📁 Output directory: {output_dir}")
    print("=" * 50)
    
    if success_count > 0:
        print(f"🎉 Dataset generation completed with {success_count} successful samples!")
    else:
        print("⚠️  No successful samples generated. Please check the error logs.")

if __name__ == "__main__":
    main() 