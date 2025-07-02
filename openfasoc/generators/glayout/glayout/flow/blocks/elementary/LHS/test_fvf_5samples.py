#!/usr/bin/env python3
"""
FVF Dataset Test - Generate 5 samples to verify the pipeline works correctly.
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
                    process_name=pdk.process_name,
                    tech_dir=pdk.tech_dir,
                    models_file=pdk.models_file,
                    drc_runset=pdk.drc_runset,
                    lvs_runset=pdk.lvs_runset,
                    pex_runset=pdk.pex_runset
                )
                
                return flipped_voltage_follower(pdk=new_pdk, **params)
            except Exception as e2:
                logger.warning(f"Fresh PDK approach failed, trying dict workaround: {e2}")
                
                # Last resort: convert to dict and create basic object
                try:
                    pdk_dict = {
                        'process_name': getattr(pdk, 'process_name', 'sky130A'),
                        'tech_dir': getattr(pdk, 'tech_dir', '/opt/conda/envs/GLdev/share/pdk/sky130A'),
                        'models_file': getattr(pdk, 'models_file', ''),
                        'drc_runset': getattr(pdk, 'drc_runset', ''),
                        'lvs_runset': getattr(pdk, 'lvs_runset', ''),
                        'pex_runset': getattr(pdk, 'pex_runset', '')
                    }
                    
                    class SimplePDK:
                        def __init__(self, **kwargs):
                            for k, v in kwargs.items():
                                setattr(self, k, v)
                    
                    simple_pdk = SimplePDK(**pdk_dict)
                    return flipped_voltage_follower(pdk=simple_pdk, **params)
                except Exception as e3:
                    logger.error(f"All PDK workarounds failed: {e3}")
                    raise e3
        else:
            logger.error(f"Non-pydantic error in FVF generation: {e}")
            raise e

def load_fvf_parameters(n_test=5):
    """Load the first n_test FVF parameters from JSON file for testing"""
    param_file = Path(__file__).parent / "generated_parameters" / "fvf_parameters.json"
    
    if not param_file.exists():
        raise FileNotFoundError(f"FVF parameters file not found: {param_file}")
    
    with open(param_file, 'r') as f:
        all_parameters = json.load(f)
    
    # Take only first n_test samples for testing
    test_parameters = all_parameters[:n_test]
    
    logger.info(f"Loaded {len(test_parameters)} FVF parameter sets for testing from {param_file}")
    return test_parameters

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
        logger.debug(f"Running sample {trial_num:04d} with params: {params}")
        component = robust_flipped_voltage_follower(pdk=pdk, **params)
        
        # Create sample directory
        trial_dir = Path(output_dir) / f"sample_{trial_num:04d}"
        trial_dir.mkdir(exist_ok=True)
        
        # Generate GDS file
        gds_file = trial_dir / f"fvf_sample_{trial_num:04d}.gds"
        component.write_gds(str(gds_file))
        
        # Run verification with robust error handling
        from robust_verification import run_robust_verification
        
        verification_results = run_robust_verification(
            str(gds_file), 
            str(trial_dir / f"fvf_sample_{trial_num:04d}"),
            component  # Pass the component as top_level
        )
        
        drc_result = verification_results["drc"]["is_pass"]
        lvs_result = verification_results["lvs"]["is_pass"]
        
        trial_time = time.time() - trial_start
        
        result = {
            "sample_id": trial_num,
            "component_name": f"fvf_sample_{trial_num:04d}",
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

def make_json_serializable(obj, depth=0, max_depth=3):
    """
    Convert complex objects to JSON-serializable formats with comprehensive error handling.
    Includes depth limit to prevent infinite recursion.
    """
    # Prevent infinite recursion
    if depth > max_depth:
        return f"<max_depth_reached: {type(obj).__name__}>"
    
    # Handle None
    if obj is None:
        return None
    
    # Handle primitive types that are already JSON serializable
    if isinstance(obj, (str, int, float, bool)):
        return obj
    
    # Handle collections
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            try:
                result[str(k)] = make_json_serializable(v, depth+1, max_depth)
            except Exception as e:
                result[str(k)] = f"<serialization_error: {e}>"
        return result
    
    elif isinstance(obj, (list, tuple)):
        result = []
        for i, item in enumerate(obj):
            try:
                result.append(make_json_serializable(item, depth+1, max_depth))
            except Exception as e:
                result.append(f"<serialization_error: {e}>")
        return result
    
    # Handle numpy types
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, Decimal):
        return float(obj)
    
    # Handle specific known problematic types
    elif hasattr(obj, '__class__'):
        class_name = obj.__class__.__name__
        module_name = getattr(obj.__class__, '__module__', '')
        
        # Skip PDK objects entirely
        if any(x in class_name for x in ['PDK', 'Component']) or 'pdk' in module_name.lower():
            return f"<{class_name}_object>"
        
        # Skip GDSTK/GDSPY objects
        if any(x in module_name for x in ['gdstk', 'gdspy']):
            return f"<{class_name}_object>"
        
        # Skip callable objects
        if callable(obj):
            return f"<function_{getattr(obj, '__name__', 'unknown')}>"
    
    # Handle objects with __dict__
    if hasattr(obj, '__dict__'):
        try:
            obj_dict = {}
            for key, value in obj.__dict__.items():
                # Skip private attributes and known problematic ones
                if key.startswith('_') or any(x in key.lower() for x in ['pdk', 'process', 'component']):
                    continue
                try:
                    obj_dict[key] = make_json_serializable(value, depth+1, max_depth)
                except Exception as e:
                    obj_dict[key] = f"<attr_error: {e}>"
            return obj_dict
        except Exception:
            return f"<{type(obj).__name__}_object>"
    
    # Final attempt: check if already JSON serializable
    try:
        json.dumps(obj)
        return obj
    except (TypeError, ValueError, RecursionError):
        # Last resort: convert to string
        try:
            return str(obj)
        except Exception:
            return f"<{type(obj).__name__}_object>"

def main():
    """Test FVF dataset generation pipeline with 5 samples"""
    logger.info("🧪 Testing FVF Dataset Generation (5 samples)")
    
    # Load pre-generated parameters (first 5 for testing)
    fvf_parameters = load_fvf_parameters(n_test=5)
    n_samples = len(fvf_parameters)
    
    # Configuration
    output_dir = "fvf_test_5samples"
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Save parameter configuration
    with open(Path(output_dir) / "fvf_test_parameters.json", 'w') as f:
        json.dump(fvf_parameters, f, indent=2, default=make_json_serializable)
    
    # Run evaluations
    results = []
    total_start = time.time()
    
    logger.info(f"📊 Processing {n_samples} FVF test samples...")
    
    for i, params in enumerate(fvf_parameters, 1):
        result = run_single_evaluation(i, params, output_dir)
        results.append(result)
        
        # Progress updates
        success_rate = sum(1 for r in results if r["success"]) / len(results) * 100
        elapsed = time.time() - total_start
        
        logger.info(f"📈 Progress: {i}/{n_samples} ({i/n_samples*100:.1f}%) - Success: {success_rate:.1f}%")
    
    # Final summary
    total_time = time.time() - total_start
    successful = [r for r in results if r["success"]]
    success_rate = len(successful) / len(results) * 100
    
    logger.info(f"\n🎉 FVF Test Complete!")
    logger.info(f"📊 Total time: {total_time:.1f} seconds")
    logger.info(f"📈 Success rate: {len(successful)}/{len(results)} ({success_rate:.1f}%)")
    
    if successful:
        drc_passes = sum(1 for r in successful if r["drc_pass"])
        lvs_passes = sum(1 for r in successful if r["lvs_pass"])
        avg_time = sum(r["execution_time"] for r in successful) / len(successful)
        
        logger.info(f"📋 Among successful samples:")
        logger.info(f"   DRC passes: {drc_passes}/{len(successful)} ({drc_passes/len(successful)*100:.1f}%)")
        logger.info(f"   LVS passes: {lvs_passes}/{len(successful)} ({lvs_passes/len(successful)*100:.1f}%)")
        logger.info(f"   Average time per sample: {avg_time:.1f}s")
        
        # Estimate time for full 360 samples
        estimated_360_time = avg_time * 360 / 3600  # in hours
        logger.info(f"⏱️ Estimated time for 360 samples: {estimated_360_time:.1f} hours")
    
    # Save detailed results with robust JSON serialization
    results_file = Path(output_dir) / "fvf_test_results.json"
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
    summary_file = Path(output_dir) / "fvf_test_summary.csv"
    df_results.to_csv(summary_file, index=False)
    
    logger.info(f" Summary saved to: {summary_file}")
    
    if success_rate >= 80:  # Lower threshold for test
        logger.info("🎉 Test passed! Ready to run full 360-sample dataset.")
        return True
    else:
        logger.warning(f"⚠️ Test success rate {success_rate:.1f}% below 80%. Review failures.")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        logger.info("✅ Test completed successfully! Run full dataset with run_fvf_dataset_360.py")
    else:
        logger.warning("❌ Review and fix issues before running full dataset.")
