#!/usr/bin/env python3
"""
Transmission Gate Dataset Generator - 200 Samples RESUME Version
Resumes generation from sample 11 to 200 (samples 0001-0010 already completed).
Based on the proven approach from generate_fvf_360_robust_fixed.py.
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

# -----------------------------------------------------------------------------
# Ensure the *local* `glayout` package is discoverable *before* we import any
# module that depends on it (e.g. `robust_verification`).
# -----------------------------------------------------------------------------

_here = Path(__file__).resolve()
_root_dir = _here.parent.parent.parent.parent.parent  # Go up to 'glayout' root
sys.path.insert(0, str(_root_dir))

# Now we can import from our package.
from glayout.flow.blocks.elementary.LHS.robust_verification import run_robust_verification
from glayout.flow.blocks.elementary.LHS.transmission_gate import transmission_gate, add_tg_labels
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk

# =============================================================================
# RESUME CONFIGURATION
# =============================================================================
RESUME_FROM_SAMPLE = 11  # Resume from sample 11 (0-based index 10)
TOTAL_SAMPLES = 200
START_INDEX = RESUME_FROM_SAMPLE - 1  # 0-based index (10)

def setup_logging():
    """Configure logging for the dataset generation."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('tg_dataset_resume.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def load_parameters():
    """Load the 200 transmission gate parameters from JSON file."""
    params_file = Path(__file__).parent / "txgate_200_params" / "txgate_parameters.json"
    
    if not params_file.exists():
        raise FileNotFoundError(f"Parameters file not found: {params_file}")
    
    with open(params_file, 'r') as f:
        params_list = json.load(f)
    
    if len(params_list) < TOTAL_SAMPLES:
        raise ValueError(f"Not enough parameters. Expected {TOTAL_SAMPLES}, got {len(params_list)}")
    
    return params_list

def create_output_structure(output_dir):
    """Create or verify the output directory structure (should already exist)."""
    output_path = Path(output_dir)
    
    # Directory should already exist from previous run
    if not output_path.exists():
        raise FileNotFoundError(f"Output directory not found: {output_path}. Previous run data missing.")
    
    logger.info(f"Resuming in existing output directory: {output_path}")
    return output_path

def estimate_completion_time(current_sample, start_time, total_samples):
    """Estimate completion time based on current progress."""
    if current_sample <= START_INDEX:
        return "Calculating..."
    
    elapsed = time.time() - start_time
    samples_completed = current_sample - START_INDEX
    remaining_samples = total_samples - current_sample
    
    if samples_completed > 0:
        avg_time_per_sample = elapsed / samples_completed
        estimated_remaining = avg_time_per_sample * remaining_samples
        
        hours = int(estimated_remaining // 3600)
        minutes = int((estimated_remaining % 3600) // 60)
        
        return f"{hours}h {minutes}m"
    return "Calculating..."

def check_existing_samples(output_dir):
    """Check which samples already exist to avoid overwriting."""
    output_path = Path(output_dir)
    existing_samples = set()
    
    for i in range(1, TOTAL_SAMPLES + 1):
        sample_dir = output_path / f"sample_{i:04d}"
        if sample_dir.exists() and sample_dir.is_dir():
            # Check if sample appears complete (has key files)
            gds_file = sample_dir / f"tg_sample_{i:04d}.gds"
            if gds_file.exists():
                existing_samples.add(i)
    
    logger.info(f"Found {len(existing_samples)} existing samples: {sorted(list(existing_samples))}")
    return existing_samples

# -----------------------------------------------------------------------------
# Single-Sample Generation (picklable → can run in a separate process)
# -----------------------------------------------------------------------------
# NOTE: The `logger` argument is optional so the function can be dispatched to a
#       separate process without needing to serialise the logger object (which
#       is not picklable).  If ``logger`` is *None* we create a minimal local
#       logger that only writes to stdout to ensure errors are still captured.
# -----------------------------------------------------------------------------

def is_valid_parameter_combination(params):
    """
    Check if parameter combination is likely to cause generation issues.
    Skip combinations that create extremely large layouts.
    """
    width_nmos, width_pmos = params['width']
    fingers_nmos, fingers_pmos = params['fingers']
    mult_nmos, mult_pmos = params['multipliers']
    
    # Calculate effective total widths
    total_width_nmos = width_nmos * fingers_nmos * mult_nmos
    total_width_pmos = width_pmos * fingers_pmos * mult_pmos
    
    # Skip if both NMOS and PMOS have very large total widths
    if total_width_nmos > 100 and total_width_pmos > 100:
        return False, f"Both NMOS ({total_width_nmos:.1f}μm) and PMOS ({total_width_pmos:.1f}μm) total widths too large"
    
    # Skip if either has extremely large total width
    if total_width_nmos > 200 or total_width_pmos > 200:
        return False, f"Extreme total width: NMOS={total_width_nmos:.1f}μm, PMOS={total_width_pmos:.1f}μm"
    
    # Skip if individual widths are too large with high finger/multiplier counts
    if (width_nmos > 15 and fingers_nmos >= 5 and mult_nmos >= 2) or \
       (width_pmos > 15 and fingers_pmos >= 5 and mult_pmos >= 2):
        return False, f"Large width with high finger/multiplier count"
    
    return True, "Valid parameters"

def run_single_sample(sample_idx, params, output_dir, logger=None):
    """
    Generate a single transmission gate sample.
    Returns: (success, runtime, results_dict)
    """
    sample_num = sample_idx + 1
    start_time = time.time()
    
    if logger is None:
        # Create a basic logger that prints to stdout only. This avoids pickling
        # issues when the function is executed in a *separate* process.
        logging.basicConfig(level=logging.INFO,
                            format='[Child %(process)d] %(asctime)s - %(levelname)s - %(message)s',
                            handlers=[logging.StreamHandler()])
        logger = logging.getLogger(f"sample_{sample_num:04d}")

    logger.info(f"=== RESUME SAMPLE {sample_num:04d}/{TOTAL_SAMPLES} ===")
    logger.info(f"Parameters: {params}")
    
    # Create sample-specific directory early for error handling
    sample_dir = Path(output_dir) / f"sample_{sample_num:04d}"
    
    # Validate parameters before attempting generation
    is_valid, validation_msg = is_valid_parameter_combination(params)
    if not is_valid:
        logger.warning(f"  ⚠️  Skipping sample {sample_num:04d}: {validation_msg}")
        runtime = 0.1  # Minimal time for parameter validation
        results = {
            'sample_number': sample_num,
            'parameters': params,
            'runtime_seconds': runtime,
            'error': f'Skipped due to problematic parameters: {validation_msg}',
            'verification_results': {},
            'files': {'sample_dir': str(sample_dir)}
        }
        return False, runtime, results
    
    sample_dir.mkdir(exist_ok=True)
    
    try:
        # Create transmission gate with parameters
        # transmission_gate function expects tuples: (nmos_value, pmos_value)
        # Parameters from JSON are structured as: width=[nmos, pmos], length=[nmos, pmos], etc.
        width_tuple = tuple(params['width'])  # [nmos_width, pmos_width]
        length_tuple = tuple(params['length'])  # [nmos_length, pmos_length]
        fingers_tuple = tuple(params['fingers'])  # [nmos_fingers, pmos_fingers]
        multipliers_tuple = tuple(params['multipliers'])  # [nmos_multipliers, pmos_multipliers]
        
        # File paths
        base_name = f"tg_sample_{sample_num:04d}"
        gds_path = sample_dir / f"{base_name}.gds"
        
        # Generate the layout
        logger.info(f"  Generating layout...")
        tg_component = transmission_gate(
            pdk=sky130_mapped_pdk,
            width=width_tuple,
            length=length_tuple,
            fingers=fingers_tuple,
            multipliers=multipliers_tuple,
            substrate_tap=True  # Enable substrate tap for robustness
        )
        
        # Add labels for better verification
        cell = add_tg_labels(tg_component, sky130_mapped_pdk)
        cell.name = f"tg_sample_{sample_num:04d}"
        
        # Write GDS
        cell.write_gds(str(gds_path))
        logger.info(f"  GDS written: {gds_path}")
        
        # Run verification (inside the sample directory for localised outputs)
        logger.info("  Running verification suite…")

        orig_cwd = os.getcwd()
        try:
            os.chdir(sample_dir)
            verification_results = run_robust_verification(
                str(gds_path),          # layout_path
                cell.name,              # component_name
                cell                    # top_level Component
            )
        finally:
            os.chdir(orig_cwd)
        
        runtime = time.time() - start_time
        
        # Prepare results dictionary
        results = {
            'sample_number': sample_num,
            'parameters': params,
            'runtime_seconds': runtime,
            'verification_results': verification_results,
            'files': {
                'gds': str(gds_path),
                'sample_dir': str(sample_dir)
            }
        }
        
        logger.info(f"  ✅ Sample {sample_num} completed in {runtime:.2f}s")
        return True, runtime, results
        
    except Exception as e:
        runtime = time.time() - start_time
        error_msg = f"Sample {sample_num} failed: {str(e)}"
        logger.error(f"  ❌ {error_msg}")
        
        results = {
            'sample_number': sample_num,
            'parameters': params,
            'runtime_seconds': runtime,
            'error': error_msg,
            'verification_results': {},
            'files': {'sample_dir': str(sample_dir)}
        }
        
        return False, runtime, results

def append_to_summary_csv(results_list, output_dir):
    """Append new results to existing summary CSV or create if doesn't exist."""
    csv_path = Path(output_dir) / "tg_summary.csv"
    
    # Prepare data for CSV
    csv_data = []
    for result in results_list:
        row = {
            'sample_number': result['sample_number'],
            'runtime_seconds': result['runtime_seconds'],
            'success': 'error' not in result,
        }
        
        # Add parameter columns
        if 'parameters' in result:
            for key, value in result['parameters'].items():
                row[f'param_{key}'] = value
        
        # Add verification results
        if 'verification_results' in result:
            for key, value in result['verification_results'].items():
                row[f'verification_{key}'] = value
        
        # Add error info if present
        if 'error' in result:
            row['error'] = result['error']
        
        csv_data.append(row)
    
    # Convert to DataFrame
    new_df = pd.DataFrame(csv_data)
    
    # If CSV exists, append to it
    if csv_path.exists():
        try:
            existing_df = pd.read_csv(csv_path)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        except Exception as e:
            logger.warning(f"Could not read existing CSV, creating new one: {e}")
            combined_df = new_df
    else:
        combined_df = new_df
    
    # Write combined data
    combined_df.to_csv(csv_path, index=False)
    logger.info(f"Summary CSV updated: {csv_path}")

def main():
    """Main function for resuming transmission gate dataset generation."""
    global logger
    logger = setup_logging()
    
    logger.info("="*80)
    logger.info("TRANSMISSION GATE DATASET GENERATOR - RESUME MODE")
    logger.info(f"Resuming from sample {RESUME_FROM_SAMPLE} to {TOTAL_SAMPLES}")
    logger.info("="*80)
    
    try:
        # Load parameters
        logger.info("Loading parameters...")
        params_list = load_parameters()
        logger.info(f"Loaded {len(params_list)} parameter combinations")
        
        # Create/verify output directory
        output_dir = Path(__file__).parent / "tg_dataset_200_lhs"
        output_path = create_output_structure(output_dir)
        
        # Check existing samples
        existing_samples = check_existing_samples(output_dir)
        
        # Track progress
        successful_samples = 0
        failed_samples = 0
        total_runtime = 0
        results_list = []
        start_time = time.time()
        
        # ------------------------------------------------------------------
        # Dataset generation loop with per-sample timeout handling
        # ------------------------------------------------------------------

        TIMEOUT_SECONDS = 1000  #  ≈16.7 minutes

        from concurrent.futures import ProcessPoolExecutor, TimeoutError

        # Resume generation from sample START_INDEX
        for i in range(START_INDEX, TOTAL_SAMPLES):
            sample_num = i + 1
            
            # Skip if sample already exists and is complete
            if sample_num in existing_samples:
                logger.info(f"Skipping existing sample {sample_num:04d}")
                continue
            
            # ------------------------------------------------------------------
            # Generate sample with timeout enforcement
            # ------------------------------------------------------------------

            try:
                with ProcessPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(run_single_sample, i, params_list[i], output_dir, None)
                    success, runtime, results = future.result(timeout=TIMEOUT_SECONDS)
            except TimeoutError:
                runtime = TIMEOUT_SECONDS
                success = False
                results = {
                    'sample_number': sample_num,
                    'parameters': params_list[i],
                    'runtime_seconds': runtime,
                    'error': f'Timeout after {TIMEOUT_SECONDS} seconds',
                    'verification_results': {},
                    'files': {'sample_dir': str(Path(output_dir) / f'sample_{sample_num:04d}')}
                }
                logger.error(f"  ⏰ Timeout: Sample {sample_num:04d} exceeded {TIMEOUT_SECONDS}s and was skipped.")
                # Clean up incomplete directory if present
                sample_dir = Path(output_dir) / f"sample_{sample_num:04d}"
                try:
                    if sample_dir.exists():
                        shutil.rmtree(sample_dir)
                        logger.info(f"  Incomplete sample directory removed: {sample_dir}")
                except Exception as e:
                    logger.warning(f"  Could not remove incomplete directory {sample_dir}: {e}")
            except Exception as e:
                # Catch *any* other exception so the main loop never crashes
                runtime = 0.0
                success = False
                results = {
                    'sample_number': sample_num,
                    'parameters': params_list[i],
                    'runtime_seconds': runtime,
                    'error': f'Unhandled exception: {str(e)}',
                    'verification_results': {},
                    'files': {'sample_dir': str(Path(output_dir) / f'sample_{sample_num:04d}')}
                }
                logger.exception(f"  💥 Exception in sample {sample_num:04d}: {e}. Marked as failed and continuing…")
            
            total_runtime += runtime
            results_list.append(results)
            
            if success:
                successful_samples += 1
            else:
                failed_samples += 1
            
            # Progress update
            completed = successful_samples + failed_samples
            total_processed = (i + 1) - START_INDEX
            success_rate = (successful_samples / total_processed * 100) if total_processed > 0 else 0
            eta = estimate_completion_time(i + 1, start_time, TOTAL_SAMPLES)
            
            logger.info(f"Progress: {completed}/{TOTAL_SAMPLES - START_INDEX} resumed samples | "
                       f"Success: {successful_samples} | Failed: {failed_samples} | "
                       f"Success Rate: {success_rate:.1f}% | ETA: {eta}")
            
            # Save intermediate results every 10 samples
            if len(results_list) % 10 == 0:
                append_to_summary_csv(results_list, output_dir)
                results_list = []  # Clear to save memory
        
        # Final save
        if results_list:
            append_to_summary_csv(results_list, output_dir)
        
        # Final summary
        total_time = time.time() - start_time
        logger.info("="*80)
        logger.info("RESUME GENERATION COMPLETED!")
        logger.info(f"Resumed samples: {TOTAL_SAMPLES - START_INDEX}")
        logger.info(f"Successful: {successful_samples}")
        logger.info(f"Failed: {failed_samples}")
        logger.info(f"Success rate: {successful_samples/(successful_samples+failed_samples)*100:.1f}%")
        logger.info(f"Total runtime: {total_time/3600:.2f} hours")
        logger.info(f"Average per sample: {total_runtime/(successful_samples+failed_samples):.2f}s")
        logger.info(f"Output directory: {output_path}")
        logger.info("="*80)
        
        # Final dataset verification
        final_existing = check_existing_samples(output_dir)
        logger.info(f"Total completed samples in dataset: {len(final_existing)}")
        
        if len(final_existing) == TOTAL_SAMPLES:
            logger.info("🎉 COMPLETE DATASET GENERATED! All 200 samples ready.")
        else:
            missing = TOTAL_SAMPLES - len(final_existing)
            logger.warning(f"⚠️  {missing} samples still missing from complete dataset.")
        
    except Exception as e:
        logger.error(f"Fatal error in dataset generation: {e}")
        raise

if __name__ == "__main__":
    main() 