#!/usr/bin/env python3
"""
Robust Current Mirror Dataset Generator - Fixed Version
Inspired by generate_fvf_360_robust_fixed.py and current_mirror.py.  
Handles environment preparation, deterministic seeding, checkpointing, and
comprehensive evaluation (DRC/LVS/PEX/geometry) for each generated sample.
"""

import logging
import os
import sys
import time
import json
import shutil
from pathlib import Path
from typing import Any
import numpy as np
import pandas as pd

# -----------------------------------------------------------------------------
# Ensure the *local* `glayout` package is discoverable *before* we import any
# module that depends on it (e.g. `robust_verification`).
# -----------------------------------------------------------------------------

_here = Path(__file__).resolve()
# Path to `<repo>/generators/glayout`
_glayout_repo_path = _here.parent.parent.parent.parent.parent.parent

# Fallback hard-coded path if relative logic fails (for robustness when the
# script is moved around). Adjust this if your repo structure changes.
if not _glayout_repo_path.exists():
    _glayout_repo_path = Path("/home/arnavshukla/OpenFASOC/openfasoc/generators/glayout")

if _glayout_repo_path.exists() and str(_glayout_repo_path) not in sys.path:
    sys.path.insert(0, str(_glayout_repo_path))

# Avoid leaking temp globals
del _here, _glayout_repo_path

# -----------------------------------------------------------------------------
# Logging configuration
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# PDK helpers – we cache a single sky130 mapped PDK instance across runs.
# -----------------------------------------------------------------------------
GLOBAL_SKY130_PDK = None

def get_global_pdk():
    """Return a *stable* sky130_mapped_pdk instance (cached)."""
    global GLOBAL_SKY130_PDK
    if GLOBAL_SKY130_PDK is None:
        from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as _pdk
        GLOBAL_SKY130_PDK = _pdk
    return GLOBAL_SKY130_PDK

# -----------------------------------------------------------------------------
# Shared environment preparation helper
# -----------------------------------------------------------------------------
from robust_verification import ensure_pdk_environment

def setup_environment():
    """Set up (or refresh) the PDK environment for this trial."""

    pdk_root = ensure_pdk_environment()

    # Now that the environment is correctly set, it is finally safe to import
    # gdsfactory and disable its Component cache to avoid stale classes.
    try:
        import gdsfactory as gf
    except ImportError:
        import gdsfactory as gf  # should always succeed now
    if hasattr(gf, 'CONFIG') and hasattr(gf.CONFIG, 'use_cache'):
        gf.CONFIG.use_cache = False
    else:
        # Newer gdsfactory versions expose settings via gf.config.CONF
        try:
            gf.config.CONF.use_cache = False  # type: ignore
        except Exception:
            pass

    # Ensure the `glayout` package directory is discoverable regardless of
    # how the user launches the script.
    glayout_path = "/home/arnavshukla/OpenFASOC/openfasoc/generators/glayout"
    if glayout_path not in sys.path:
        sys.path.insert(0, glayout_path)

    # Prepend to PYTHONPATH so subprocesses (if any) inherit the correct path
    current_pythonpath = os.environ.get('PYTHONPATH', '')
    if glayout_path not in current_pythonpath.split(":"):
        os.environ['PYTHONPATH'] = f"{glayout_path}:{current_pythonpath}"

    logger.info(f"Environment refreshed: PDK_ROOT={pdk_root}")
    return pdk_root

# -----------------------------------------------------------------------------
# Circuit generator wrapper – returns a *fresh* component each call.
# -----------------------------------------------------------------------------

def robust_current_mirror(pdk, **params):
    """Return a current_mirror with a *fresh* MappedPDK every call."""
    from current_mirror import current_mirror, add_cm_labels

    # Ensure dummy devices are disabled for LVS consistency
    params_mod = dict(params)
    params_mod.setdefault('with_dummy', False)
    comp = current_mirror(pdk, **params_mod)
    
    # Add physical pin shapes so Magic extracts a correct pin list for LVS
    try:
        comp = add_cm_labels(comp, pdk)
    except Exception as e:
        logger.warning(f"Failed to add pin labels to current mirror: {e}")
    
    return comp

def load_current_mirror_parameters(num_samples=None):
    """Load current mirror parameters from pre-generated parameter file"""
    parameter_file = "/home/arnavshukla/OpenFASOC/openfasoc/generators/glayout/glayout/flow/blocks/elementary/LHS/generated_parameters/current_mirror_parameters.json"
    
    try:
        with open(parameter_file, 'r') as f:
            parameters = json.load(f)
    except FileNotFoundError:
        logger.error(f"Parameter file not found: {parameter_file}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing parameter file: {e}")
        raise
    
    if num_samples is None:
        num_samples = len(parameters)
    
    # Return the requested number of parameters
    selected_parameters = parameters[:num_samples]
    
    logger.info(f"Loaded {len(selected_parameters)} parameter combinations from {parameter_file}")
    return selected_parameters

def cleanup_files():
    """Clean up generated files in working directory"""
    files_to_clean = [
        "*.gds", "*.drc.rpt", "*.lvs.rpt", "*.ext", "*.spice", 
        "*.res.ext", "*.sim", "*.nodes", "*_lvsmag.spice", "*_sim.spice",
        "*_pex.spice", "*.pex.spice"
    ]
    
    for pattern in files_to_clean:
        import glob
        for file in glob.glob(pattern):
            try:
                os.remove(file)
            except OSError:
                pass

def make_json_serializable(obj):
    """Convert complex objects to JSON-serializable formats"""
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [make_json_serializable(item) for item in obj]
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif hasattr(obj, '__dict__'):
        try:
            return make_json_serializable(obj.__dict__)
        except:
            return str(obj)
    elif hasattr(obj, '__class__') and 'PDK' in str(obj.__class__):
        return f"PDK_object_{getattr(obj, 'name', 'unknown')}"
    else:
        try:
            json.dumps(obj)
            return obj
        except (TypeError, ValueError):
            return str(obj)

def run_single_evaluation(trial_num, params, output_dir):
    """Run a single current mirror evaluation with robust error handling"""
    trial_start = time.time()
    
    try:
        # === DETERMINISTIC SEEDING FIX ===
        # Set deterministic seeds before each trial to ensure reproducible results
        import random
        import numpy as np
        
        # Use trial_num as base seed to ensure different trials get different but reproducible layouts
        base_seed = trial_num * 1000  # Multiply to spread seeds apart
        random.seed(base_seed)
        np.random.seed(base_seed)
        
        # Also set seed for any potential hash-based randomization
        os.environ['PYTHONHASHSEED'] = str(base_seed)
        
        logger.info(f"Trial {trial_num}: Set deterministic seed = {base_seed}")
        
        # Setup environment for each trial
        setup_environment()
        
        # Clear any cached gdsfactory Components / PDKs to avoid stale class refs
        try:
            import gdsfactory as gf
        except ImportError:
            import gdsfactory as gf
        if hasattr(gf, 'clear_cache'):
            gf.clear_cache()
        if hasattr(gf, 'clear_cell_cache'):
            gf.clear_cell_cache()
        
        # === COMPREHENSIVE CACHE CLEARING ===
        # Clear all possible gdsfactory caches to ensure fresh state
        try:
            # Clear component cache
            if hasattr(gf, '_CACHE'):
                gf._CACHE.clear()
            # Clear any cell factories
            if hasattr(gf.Component, '_cell_cache'):
                gf.Component._cell_cache.clear()
            # Disable caching entirely for this trial
            if hasattr(gf, 'CONFIG'):
                if hasattr(gf.CONFIG, 'use_cache'):
                    gf.CONFIG.use_cache = False
                if hasattr(gf.CONFIG, 'cache'):
                    gf.CONFIG.cache = False
        except Exception as e:
            logger.warning(f"Could not clear some gdsfactory caches: {e}")
        
        # Use a *stable* PDK instance across all trials to avoid Pydantic class mismatch
        pdk = get_global_pdk()

        # Create component with robust wrapper
        component_name = f"cm_sample_{trial_num:04d}"
        comp = robust_current_mirror(pdk, **params)
        comp.name = component_name

        # Write GDS
        gds_file = f"{component_name}.gds"
        comp.write_gds(gds_file)

        # Run comprehensive evaluation (DRC, LVS, PEX, Geometry)
        from evaluator_wrapper import run_evaluation
        comprehensive_results = run_evaluation(gds_file, component_name, comp)
        drc_result = comprehensive_results["drc"]["is_pass"]
        lvs_result = comprehensive_results["lvs"]["is_pass"]

        # Extract PEX and geometry data
        pex_data = comprehensive_results.get("pex", {})
        geometry_data = comprehensive_results.get("geometric", {})

        # Create trial directory and copy results
        trial_dir = Path(output_dir) / f"sample_{trial_num:04d}"
        trial_dir.mkdir(exist_ok=True)
        
        # Copy all generated files to the trial directory
        files_to_copy = [
            gds_file,
            f"{component_name}.drc.rpt",
            f"{component_name}.lvs.rpt",
            f"{component_name}_pex.spice",
            f"{component_name}.res.ext",
        ]
        for file_path in files_to_copy:
            if Path(file_path).exists():
                shutil.copy(file_path, trial_dir / file_path)

        trial_time = time.time() - trial_start
        success_flag = drc_result and lvs_result

        result = {
            "sample_id": trial_num,
            "component_name": component_name,
            "success": success_flag,
            "drc_pass": drc_result,
            "lvs_pass": lvs_result,
            "execution_time": trial_time,
            "parameters": make_json_serializable(params),
            "output_directory": str(trial_dir),
            # PEX
            "pex_status": pex_data.get("status", "not run"),
            "total_resistance_ohms": pex_data.get("total_resistance_ohms", 0.0),
            "total_capacitance_farads": pex_data.get("total_capacitance_farads", 0.0),
            # Geometry
            "area_um2": geometry_data.get("raw_area_um2", 0.0),
            "symmetry_horizontal": geometry_data.get("symmetry_score_horizontal", 0.0),
            "symmetry_vertical": geometry_data.get("symmetry_score_vertical", 0.0),
        }

        pex_status_short = "✓" if pex_data.get("status") == "PEX Complete" else "✗"
        logger.info(
            f"✅ Sample {trial_num:04d} in {trial_time:.1f}s "
            f"(DRC: {'✓' if drc_result else '✗'}, "
            f"LVS: {'✓' if lvs_result else '✗'}, PEX: {pex_status_short})"
        )
        return result

    except Exception as e:
        trial_time = time.time() - trial_start
        logger.error(f"❌ Sample {trial_num:04d} failed: {e}")
        return {
            "sample_id": trial_num,
            "component_name": f"cm_sample_{trial_num:04d}",
            "success": False,
            "error": str(e),
            "execution_time": trial_time,
            "parameters": make_json_serializable(params),
        }
    finally:
        cleanup_files()
        try:
            import gdsfactory as gf
            if hasattr(gf, 'clear_cache'):
                gf.clear_cache()
            if hasattr(gf, 'clear_cell_cache'):
                gf.clear_cell_cache()
        except Exception:
            pass

# -----------------------------------------------------------------------------
# Dataset generation – orchestrates many trials with checkpointing.
# -----------------------------------------------------------------------------

def run_dataset_generation(n_samples: int, output_dir: str, *, checkpoint_interval: int = 100, resume_from_checkpoint: bool = True):
    """Run the dataset generation with checkpointing support."""

    logger.info(f"🚀 Starting Current Mirror Dataset Generation for {n_samples} samples")
    Path(output_dir).mkdir(exist_ok=True)

    parameters = load_current_mirror_parameters(n_samples)
    with open(Path(output_dir) / "cm_parameters.json", "w") as f:
        json.dump(parameters, f, indent=2)

    checkpoint_file = Path(output_dir) / "checkpoint.json"
    results: list[dict[str, Any]] = []
    start_idx = 0

    if resume_from_checkpoint and checkpoint_file.exists():
        try:
            with open(checkpoint_file, 'r') as f:
                checkpoint_data = json.load(f)
            results = checkpoint_data.get("results", [])
            start_idx = len(results)
            logger.info(f"📂 Resuming from checkpoint: {start_idx}/{n_samples} samples completed")
        except Exception as e:
            logger.warning(f"Failed to load checkpoint: {e}. Starting fresh.")

    total_start = time.time()
    logger.info(f"📊 Processing samples {start_idx + 1} to {n_samples}…")

    for i in range(start_idx, n_samples):
        params = parameters[i]
        result = run_single_evaluation(i + 1, params, output_dir)
        results.append(result)

        # Checkpointing
        if (i + 1) % checkpoint_interval == 0:
            try:
                checkpoint_data = {
                    "timestamp": time.time(),
                    "completed_samples": i + 1,
                    "total_samples": n_samples,
                    "results": make_json_serializable(results),
                }
                with open(checkpoint_file, 'w') as f:
                    json.dump(checkpoint_data, f, indent=2)
                logger.info(f"💾 Checkpoint saved at sample {i + 1}")
            except Exception as e:
                logger.warning(f"Failed to save checkpoint: {e}")

        # Progress reporting
        progress_interval = 10 if n_samples <= 100 else (50 if n_samples <= 1000 else 100)
        if (i + 1) % progress_interval == 0 or (i + 1) <= 10:
            success_rate = sum(1 for r in results if r["success"]) / len(results) * 100
            elapsed = time.time() - total_start
            remaining_samples = n_samples - (i + 1)
            avg_time = elapsed / (i + 1 - start_idx) if (i + 1 - start_idx) else 0
            eta = remaining_samples * avg_time
            if eta > 3600:
                eta_msg = f"ETA: {eta/3600:.1f}h"
            elif eta > 60:
                eta_msg = f"ETA: {eta/60:.1f}m"
            else:
                eta_msg = f"ETA: {eta:.0f}s"
            logger.info(
                f"📈 Progress: {i+1}/{n_samples} ({(i+1)/n_samples*100:.1f}%) - "
                f"Success: {success_rate:.1f}% - {eta_msg}"
            )

    # Final summary
    total_time = time.time() - total_start
    successful = [r for r in results if r["success"]]
    success_rate = len(successful) / len(results) * 100 if results else 0

    logger.info(f"\n🎉 Dataset Generation Complete!")
    logger.info(f"📊 Total time: {total_time/3600:.2f} hours ({total_time/60:.1f} minutes)")
    logger.info(f"📈 Success rate: {len(successful):,}/{len(results):,} ({success_rate:.1f}%)")

    if successful:
        drc_passes = sum(1 for r in successful if r["drc_pass"])
        lvs_passes = sum(1 for r in successful if r["lvs_pass"])
        pex_passes = sum(1 for r in successful if r.get("pex_status") == "PEX Complete")
        avg_time = sum(r["execution_time"] for r in successful) / len(successful)
        logger.info(
            f"   DRC passes: {drc_passes:,}/{len(successful):,} ({drc_passes/len(successful)*100:.1f}%)")
        logger.info(
            f"   LVS passes: {lvs_passes:,}/{len(successful):,} ({lvs_passes/len(successful)*100:.1f}%)")
        logger.info(
            f"   PEX passes: {pex_passes:,}/{len(successful):,} ({pex_passes/len(successful)*100:.1f}%)")
        logger.info(f"   Average time per sample: {avg_time:.1f}s")

    # Save detailed results
    results_file = Path(output_dir) / "cm_results.json"
    try:
        with open(results_file, 'w') as f:
            json.dump(make_json_serializable(results), f, indent=2)
        logger.info(f"📄 Results saved to: {results_file}")
    except Exception as e:
        logger.error(f"Failed to save JSON results: {e}")

    # Save CSV summary
    df_results = pd.DataFrame(results)
    summary_file = Path(output_dir) / "cm_summary.csv"
    df_results.to_csv(summary_file, index=False)
    logger.info(f"📄 Summary saved to: {summary_file}")

    if checkpoint_file.exists():
        try:
            checkpoint_file.unlink()
            logger.info("🗑️ Checkpoint file cleaned up")
        except Exception as e:
            logger.warning(f"Failed to clean up checkpoint: {e}")

    return success_rate >= 80, len(successful), len(results)

# -----------------------------------------------------------------------------
# CLI entry-point
# -----------------------------------------------------------------------------

def main():
    """Main entry-point – kick off dataset generation."""
    print("🚀 Current Mirror Dataset Generation - LHS Samples")
    print("=" * 70)

    # Load parameters just to get the count
    try:
        parameters = load_current_mirror_parameters()
        total_samples = len(parameters)
        print(f"📊 Loaded {total_samples:,} parameter combinations")
    except Exception as e:
        print(f"❌ Failed to load parameters: {e}")
        return False

    estimated_time_hours = (total_samples * 15) / 3600  # ~15s/sample conservative
    print(f"\n⏱️  Estimated completion time: {estimated_time_hours:.1f} hours")
    print("   Assuming 15 seconds per sample average")
    print("\n📁 Output will be saved to: cm_dataset_lhs")
    print("💾 Checkpoints will be saved every 50 samples")
    print("🔄 Can resume from checkpoint if interrupted")

    response = input("\n🤔 Continue with dataset generation? (y/n): ").lower().strip()
    if response != 'y':
        print("Stopping as requested.")
        return True

    start_sample = input("\n🔢 Start from sample number (press Enter for 1): ").strip()
    if start_sample:
        try:
            start_idx = int(start_sample) - 1
            if start_idx < 0 or start_idx >= total_samples:
                print(f"❌ Invalid start sample. Must be between 1 and {total_samples}")
                return False
            parameters = parameters[start_idx:]
            actual_samples = len(parameters)
            print(f"▶️  Starting from sample {start_sample}, will process {actual_samples:,} samples")
        except ValueError:
            print("❌ Invalid sample number")
            return False
    else:
        actual_samples = total_samples

    print(f"\n🚀 Starting generation of {actual_samples:,} samples…")
    success, passed, total = run_dataset_generation(
        actual_samples,
        "cm_dataset_lhs",
        checkpoint_interval=50,
        resume_from_checkpoint=True,
    )

    if success:
        print(f"\n🎉 Dataset generation completed successfully!")
        print(f"📊 Final results: {passed:,}/{total:,} samples successful")
        print("📁 Dataset saved to: cm_dataset_lhs/")
        return True
    else:
        print(f"\n⚠️ Dataset generation completed with issues")
        print(f"📊 Final results: {passed:,}/{total:,} samples successful")
        print("💡 Check logs and results in: cm_dataset_lhs/")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Current Mirror dataset generation pipeline completed!")
    else:
        print("\n❌ Please review and fix issues.") 