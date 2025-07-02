#!/usr/bin/env python3
"""
Final robust sequential sweeper for LHS dataset generation.
Integrates all fixes: pydantic validation workaround, robust verification, and proper cleanup.
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
from pyDOE2 import lhs
from decimal import Decimal

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Set up the PDK environment"""
    pdk_root = "/opt/conda/envs/GLdev/share/pdk"
    os.environ['PDK_ROOT'] = pdk_root
    os.environ['PDKPATH'] = pdk_root
    os.environ['PDK'] = 'sky130A'
    return pdk_root

def robust_flipped_voltage_follower(pdk, **params):
    """Robust wrapper around flipped_voltage_follower that handles pydantic issues"""
    from fvf import flipped_voltage_follower
    
    # Try the normal approach first
    try:
        return flipped_voltage_follower(pdk=pdk, **params)
    except Exception as e:
        if "validation error" in str(e).lower() or "pydantic" in str(e).lower():
            logger.warning(f"Pydantic validation error, trying workaround")
            
            # Workaround: Create a new PDK object with fresh properties
            try:
                # Get the PDK class
                from glayout.flow.pdk.mappedpdk import MappedPDK
                
                # Create a new instance with the same properties
                new_pdk = MappedPDK(
                    name=pdk.name,
                    glayers=dict(pdk.glayers),  # Create fresh dict
                    models=dict(pdk.models),    # Create fresh dict
                    layers=dict(pdk.layers) if pdk.layers else None,
                    grules=pdk.grules,
                    pdk_files=dict(pdk.pdk_files),  # Create fresh dict
                    default_decorator=pdk.default_decorator if hasattr(pdk, 'default_decorator') else None,
                )
                new_pdk.grid_size = pdk.grid_size
                
                return flipped_voltage_follower(pdk=new_pdk, **params)
                
            except Exception:
                # Final fallback: Try passing as dictionary
                try:
                    pdk_dict = {
                        'name': pdk.name,
                        'glayers': pdk.glayers,
                        'models': pdk.models,
                        'layers': pdk.layers,
                        'grules': pdk.grules,
                        'pdk_files': pdk.pdk_files,
                    }
                    return flipped_voltage_follower(pdk=pdk_dict, **params)
                    
                except Exception:
                    raise e  # Re-raise original error
        else:
            # Not a pydantic error, re-raise
            raise e

def generate_lhs_samples(n_samples=100, n_vars=4):
    """Generate LHS samples for FVF parameters"""
    logger.info(f"Generating {n_samples} LHS samples...")
    
    # Generate LHS samples (n_samples x n_vars)
    lhs_samples = lhs(n_vars, samples=n_samples, criterion='maximin')
    
    # Define parameter ranges
    param_ranges = {
        'width_min': (3.0, 12.0),
        'width_max': (6.0, 15.0),
        'length_min': (1.0, 2.0),
        'length_max': (1.2, 2.5),
        'fingers_min': (1, 5),
        'fingers_max': (2, 6),
        'multipliers_min': (1, 3),
        'multipliers_max': (1, 4),
    }
    
    # Scale samples to parameter ranges
    scaled_samples = []
    for i, sample in enumerate(lhs_samples):
        # Scale each parameter based on the sample values
        width_min = param_ranges['width_min'][0] + sample[0] * (param_ranges['width_min'][1] - param_ranges['width_min'][0])
        width_max = param_ranges['width_max'][0] + sample[1] * (param_ranges['width_max'][1] - param_ranges['width_max'][0])
        
        length_min = param_ranges['length_min'][0] + sample[2] * (param_ranges['length_min'][1] - param_ranges['length_min'][0])
        length_max = param_ranges['length_max'][0] + sample[3] * (param_ranges['length_max'][1] - param_ranges['length_max'][0])
        
        # For integer parameters, use different sampling
        fingers_min = int(param_ranges['fingers_min'][0] + sample[0] * (param_ranges['fingers_min'][1] - param_ranges['fingers_min'][0]))
        fingers_max = int(param_ranges['fingers_max'][0] + sample[1] * (param_ranges['fingers_max'][1] - param_ranges['fingers_max'][0]))
        
        multipliers_min = int(param_ranges['multipliers_min'][0] + sample[2] * (param_ranges['multipliers_min'][1] - param_ranges['multipliers_min'][0]))
        multipliers_max = int(param_ranges['multipliers_max'][0] + sample[3] * (param_ranges['multipliers_max'][1] - param_ranges['multipliers_max'][0]))
        
        # Ensure max >= min
        if width_max < width_min:
            width_min, width_max = width_max, width_min
        if length_max < length_min:
            length_min, length_max = length_max, length_min
        if fingers_max < fingers_min:
            fingers_min, fingers_max = fingers_max, fingers_min
        if multipliers_max < multipliers_min:
            multipliers_min, multipliers_max = multipliers_max, multipliers_min
            
        scaled_samples.append({
            'width': (width_min, width_max),
            'length': (length_min, length_max),
            'fingers': (fingers_min, fingers_max),
            'multipliers': (multipliers_min, multipliers_max)
        })
    
    logger.info(f"Generated {len(scaled_samples)} parameter combinations")
    return scaled_samples

def run_single_evaluation(trial_num, params, output_dir):
    """Run a single FVF evaluation with robust error handling"""
    trial_start = time.time()
    
    try:
        # Setup environment
        setup_environment()
        
        # Get PDK object
        from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
        pdk = sky130_mapped_pdk
        
        # Create component with robust wrapper
        component_name = f"fvf_sample_{trial_num:04d}"
        comp = robust_flipped_voltage_follower(pdk, **params)
        comp.name = component_name
        
        # Write GDS
        gds_file = f"{component_name}.gds"
        comp.write_gds(gds_file)
        
        # Run verification
        from robust_verification import run_robust_verification
        verification_results = run_robust_verification(gds_file, component_name, comp)
        drc_result = verification_results["drc"]["is_pass"]
        lvs_result = verification_results["lvs"]["is_pass"]
        
        # Create trial directory and copy results
        trial_dir = Path(output_dir) / f"sample_{trial_num:04d}"
        trial_dir.mkdir(exist_ok=True)
        
        # Copy all generated files
        for file_path in [gds_file, f"{component_name}.drc.rpt", f"{component_name}.lvs.rpt"]:
            if Path(file_path).exists():
                shutil.copy(file_path, trial_dir / file_path)
        
        trial_time = time.time() - trial_start
        
        result = {
            "sample_id": trial_num,
            "component_name": component_name,
            "success": True,
            "drc_pass": drc_result,
            "lvs_pass": lvs_result,
            "execution_time": trial_time,
            "parameters": make_json_serializable(params),
            "output_directory": str(trial_dir)
        }
        
        logger.info(f"✅ Sample {trial_num:04d} completed in {trial_time:.1f}s (DRC: {'✓' if drc_result else '✗'}, LVS: {'✓' if lvs_result else '✗'})")
        return result
        
    except Exception as e:
        trial_time = time.time() - trial_start
        logger.error(f"❌ Sample {trial_num:04d} failed: {e}")
        
        result = {
            "sample_id": trial_num,
            "component_name": f"fvf_sample_{trial_num:04d}",
            "success": False,
            "error": str(e),
            "execution_time": trial_time,
            "parameters": make_json_serializable(params)
        }
        return result
    
    finally:
        # Clean up working directory
        cleanup_files()

def cleanup_files():
    """Clean up generated files in working directory"""
    files_to_clean = [
        "*.gds", "*.drc.rpt", "*.lvs.rpt", "*.ext", "*.spice", 
        "*.res.ext", "*.sim", "*.nodes", "*_lvsmag.spice", "*_sim.spice"
    ]
    
    for pattern in files_to_clean:
        import glob
        for file in glob.glob(pattern):
            try:
                os.remove(file)
            except OSError:
                pass

def make_json_serializable(obj):
    """
    Convert complex objects to JSON-serializable formats
    """
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [make_json_serializable(item) for item in obj]
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, Decimal):
        return float(obj)
    elif hasattr(obj, '__dict__'):
        # For custom objects, try to convert to dict
        try:
            return make_json_serializable(obj.__dict__)
        except:
            return str(obj)
    elif hasattr(obj, '__class__') and 'PDK' in str(obj.__class__):
        # For PDK objects, return a simple string representation
        return f"PDK_object_{getattr(obj, 'name', 'unknown')}"
    else:
        try:
            # Try JSON serialization to check if it's already serializable
            json.dumps(obj)
            return obj
        except (TypeError, ValueError):
            # If not serializable, convert to string
            return str(obj)

def main():
    """Main LHS dataset generation pipeline"""
    logger.info("🚀 Starting Robust LHS Dataset Generation")
    
    # Configuration
    n_samples = 50  # Start with 50 samples for validation
    output_dir = "lhs_dataset_robust"
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Generate LHS samples
    samples = generate_lhs_samples(n_samples)
    
    # Save parameter configuration
    with open(Path(output_dir) / "lhs_parameters.json", 'w') as f:
        json.dump(samples, f, indent=2)
    
    # Run evaluations
    results = []
    total_start = time.time()
    
    logger.info(f"📊 Processing {n_samples} samples...")
    
    for i, params in enumerate(samples, 1):
        result = run_single_evaluation(i, params, output_dir)
        results.append(result)
        
        # Progress updates
        if i % 10 == 0:
            success_rate = sum(1 for r in results if r["success"]) / len(results) * 100
            elapsed = time.time() - total_start
            estimated_total = elapsed * n_samples / i
            remaining = estimated_total - elapsed
            
            logger.info(f"📈 Progress: {i}/{n_samples} ({i/n_samples*100:.1f}%) - Success: {success_rate:.1f}% - ETA: {remaining/60:.1f}m")
    
    # Final summary
    total_time = time.time() - total_start
    successful = [r for r in results if r["success"]]
    success_rate = len(successful) / len(results) * 100
    
    logger.info(f"\n🎉 LHS Dataset Generation Complete!")
    logger.info(f"📊 Total time: {total_time/60:.1f} minutes")
    logger.info(f"📈 Success rate: {len(successful)}/{len(results)} ({success_rate:.1f}%)")
    
    if successful:
        drc_passes = sum(1 for r in successful if r["drc_pass"])
        lvs_passes = sum(1 for r in successful if r["lvs_pass"])
        avg_time = sum(r["execution_time"] for r in successful) / len(successful)
        
        logger.info(f"📋 Among successful samples:")
        logger.info(f"   DRC passes: {drc_passes}/{len(successful)} ({drc_passes/len(successful)*100:.1f}%)")
        logger.info(f"   LVS passes: {lvs_passes}/{len(successful)} ({lvs_passes/len(successful)*100:.1f}%)")
        logger.info(f"   Average time per sample: {avg_time:.1f}s")
    
    # Save detailed results with robust JSON serialization
    results_file = Path(output_dir) / "lhs_results.json"
    try:
        # First, make all results JSON-serializable
        serializable_results = make_json_serializable(results)
        with open(results_file, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        logger.info(f"📄 Results saved to: {results_file}")
    except Exception as e:
        logger.error(f"Failed to save JSON results: {e}")
        # Fallback: save without parameters to prevent complete failure
        try:
            fallback_results = []
            for result in results:
                fallback_result = {k: v for k, v in result.items() if k != 'parameters'}
                fallback_result['parameters_serialization_failed'] = True
                fallback_results.append(fallback_result)
            with open(results_file, 'w') as f:
                json.dump(fallback_results, f, indent=2)
            logger.warning(f"📄 Saved fallback results (without parameters) to: {results_file}")
        except Exception as e2:
            logger.error(f"Even fallback JSON save failed: {e2}")
            # Last resort: save as text
            with open(results_file.with_suffix('.txt'), 'w') as f:
                f.write(str(results))
            logger.warning(f"📄 Saved results as text to: {results_file.with_suffix('.txt')}")
    
    # Save summary CSV
    df_results = pd.DataFrame(results)
    summary_file = Path(output_dir) / "lhs_summary.csv"
    df_results.to_csv(summary_file, index=False)
    
    logger.info(f" Summary saved to: {summary_file}")
    
    if success_rate >= 90:
        logger.info("🎉 Excellent success rate! Dataset generation pipeline is robust.")
        return True
    else:
        logger.warning(f"⚠️ Success rate {success_rate:.1f}% below 90%. Review failures.")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        logger.info("✅ Ready to scale up to full dataset!")
    else:
        logger.warning("❌ Review and fix issues before scaling up.")
