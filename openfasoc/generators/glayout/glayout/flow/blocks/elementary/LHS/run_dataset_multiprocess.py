#!/usr/bin/env python3
"""
Transmission Gate Dataset Generator - 100 Samples Version
Based on the proven approach from generate_fvf_360_robust_fixed.py.
Generates dataset using 100 parameter combinations from txgate_parameters.json and monitors runtime.
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

# Suppress overly verbose gdsfactory logging
import warnings
warnings.filterwarnings(
    "ignore", 
    message="decorator is deprecated and will be removed soon.*"
)
warnings.filterwarnings(
    "ignore", 
    message=".*we will remove unlock to discourage use.*"
)
# Also suppress info with "* PDK is now active"
logging.getLogger("gdsfactory").setLevel(logging.WARNING)

# -----------------------------------------------------------------------------
# Ensure the *local* `glayout` package is discoverable *before* we import any
# module that depends on it (e.g. `robust_verification`).
# -----------------------------------------------------------------------------
_here = Path(__file__).resolve()
_glayout_repo_path = _here.parent.parent.parent.parent.parent.parent
pwd_path = Path.cwd().resolve()
print("Current working directory:", pwd_path)
# Fallback hard-coded path if relative logic fails (for robustness when the
# script is moved around). Adjust this if your repo structure changes.
if not _glayout_repo_path.exists():
    _glayout_repo_path = pwd_path / "../../../../"

if _glayout_repo_path.exists() and str(_glayout_repo_path) not in sys.path:
    sys.path.insert(0, str(_glayout_repo_path))

del _here, _glayout_repo_path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# We *delay* importing gdsfactory until *after* the PDK environment variables
# are guaranteed to be correct. Importing it too early locks-in an incorrect
# `PDK_ROOT`, which then causes Magic/Netgen to fall back to the built-in
# "minimum" tech, triggering the dummy fallback reports the user wants to
# avoid.

# Helper to obtain a stable sky130 mapped PDK instance
GLOBAL_SKY130_PDK = None

def get_global_pdk():
    """Return a *stable* sky130_mapped_pdk instance (cached)."""
    global GLOBAL_SKY130_PDK
    if GLOBAL_SKY130_PDK is None:
        from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as _pdk
        GLOBAL_SKY130_PDK = _pdk
    return GLOBAL_SKY130_PDK

# Import the shared PDK environment helper so we keep a single source of truth
from robust_verification import ensure_pdk_environment
from contextlib import contextmanager

@contextmanager
def chdir(path: Path):
    """Temporarily change working directory to `path`."""
    prev = Path.cwd()
    try:
        os.makedirs(path, exist_ok=True)
        os.chdir(path)
        yield
    finally:
        os.chdir(prev)

def setup_environment():
    """Set up (or refresh) the PDK environment for this trial.

    We rely on the **shared** `ensure_pdk_environment` helper so that the
    exact same logic is used across the entire code-base. This prevents the
    two implementations from drifting apart and guarantees that *every*
    entry-point resets the PDK environment in one atomic `os.environ.update`
    call.
    """

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
    glayout_path = pwd_path / "../../../../"
    print("Using glayout path:", glayout_path)
    if glayout_path not in sys.path:
        sys.path.insert(0, glayout_path)

    # Prepend to PYTHONPATH so subprocesses (if any) inherit the correct path
    current_pythonpath = os.environ.get('PYTHONPATH', '')
    if glayout_path not in current_pythonpath.split(":"):
        os.environ['PYTHONPATH'] = f"{glayout_path}:{current_pythonpath}"

    logger.info(f"Environment refreshed: PDK_ROOT={pdk_root}")
    return pdk_root

def robust_transmission_gate(_, **params):
    """Return a transmission_gate with a *fresh* MappedPDK every call.

    We sidestep all pydantic ValidationErrors by importing/reloading
    ``glayout.flow.pdk.sky130_mapped`` each time and passing that brand-new
    ``sky130_mapped_pdk`` instance to the circuit generator.
    """
    from transmission_gate import transmission_gate, add_tg_labels
    # Use a *stable* PDK instance across all trials to avoid Pydantic class mismatch
    pdk = get_global_pdk()
    comp = transmission_gate(pdk=pdk, **params)
    # Add physical pin shapes so Magic extracts a correct pin list for LVS
    try:
        comp = add_tg_labels(comp, pdk)
    except Exception as e:
        logger.warning(f"Failed to add pin labels to TG: {e}")
    return comp

def load_tg_parameters_from_json(json_file=""):
    """Load transmission gate parameters from the generated JSON file"""
    json_path = Path(json_file)
    if not json_path.exists():
        raise FileNotFoundError(f"Parameter file not found: {json_file}")
    with open(json_path, 'r') as f:
        parameters = json.load(f)
    logger.info(f"Loaded {len(parameters)} transmission gate parameter combinations from {json_file}")
    # Log parameter distribution statistics
    widths_nmos = [p["width"][0] for p in parameters]
    widths_pmos = [p["width"][1] for p in parameters]
    lengths_nmos = [p["length"][0] for p in parameters]
    lengths_pmos = [p["length"][1] for p in parameters]
    logger.info(f"Parameter ranges:")
    logger.info(f"  NMOS width: {min(widths_nmos):.2f} - {max(widths_nmos):.2f} μm")
    logger.info(f"  PMOS width: {min(widths_pmos):.2f} - {max(widths_pmos):.2f} μm")
    logger.info(f"  NMOS length: {min(lengths_nmos):.3f} - {max(lengths_nmos):.3f} μm")
    logger.info(f"  PMOS length: {min(lengths_pmos):.3f} - {max(lengths_pmos):.3f} μm")
    # Show first few parameter examples
    logger.info(f"First 3 parameter combinations:")
    for i, params in enumerate(parameters[:3], 1):
        nmos_w, pmos_w = params["width"]
        nmos_l, pmos_l = params["length"]
        nmos_f, pmos_f = params["fingers"]
        nmos_m, pmos_m = params["multipliers"]
        
        logger.info(f"  Sample {i}: NMOS({nmos_w:.2f}μm/{nmos_l:.3f}μm, {nmos_f}f×{nmos_m}), "
                   f"PMOS({pmos_w:.2f}μm/{pmos_l:.3f}μm, {pmos_f}f×{pmos_m})")
    return parameters

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
# Parallelized
def run_single_evaluation(trial_num, params, output_dir):
    """Run a single TG evaluation in its own isolated working directory."""
    trial_start = time.time()

    # Per-trial working dir (all scratch files live here)
    trial_work_dir = Path(output_dir) / "_work" / f"sample_{trial_num:04d}"
    # Per-trial final results dir (curated outputs copied here)
    trial_out_dir = Path(output_dir) / f"sample_{trial_num:04d}"

    try:
        with chdir(trial_work_dir):
            # === DETERMINISTIC SEEDING FIX ===
            import random
            import numpy as np
            base_seed = trial_num * 1000
            random.seed(base_seed)
            np.random.seed(base_seed)
            os.environ['PYTHONHASHSEED'] = str(base_seed)
            logger.info(f"Trial {trial_num}: Set deterministic seed = {base_seed}")

            # Setup environment for each trial (safe in subprocess)
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
            try:
                if hasattr(gf, '_CACHE'):
                    gf._CACHE.clear()
                if hasattr(gf.Component, '_cell_cache'):
                    gf.Component._cell_cache.clear()
                if hasattr(gf, 'CONFIG'):
                    if hasattr(gf.CONFIG, 'use_cache'):
                        gf.CONFIG.use_cache = False
                    if hasattr(gf.CONFIG, 'cache'):
                        gf.CONFIG.cache = False
            except Exception as e:
                logger.warning(f"Could not clear some gdsfactory caches: {e}")

            # Fresh PDK import per trial/process
            import importlib, sys
            if 'glayout.flow.pdk.sky130_mapped' in sys.modules:
                importlib.reload(sys.modules['glayout.flow.pdk.sky130_mapped'])
            from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
            pdk = sky130_mapped_pdk

            # Create and name component
            component_name = f"tg_sample_{trial_num:04d}"
            comp = robust_transmission_gate(pdk, **params)
            comp.name = component_name

            # Write GDS into the trial's **work** dir
            gds_file = f"{component_name}.gds"
            comp.write_gds(gds_file)
            gds_path = Path.cwd() / gds_file  # absolute path

            # Run comprehensive evaluation (DRC, LVS, PEX, Geometry)
            from evaluator_wrapper import run_evaluation
            comprehensive_results = run_evaluation(str(gds_path), component_name, comp)
            drc_result = comprehensive_results["drc"]["is_pass"]
            lvs_result = comprehensive_results["lvs"]["is_pass"]

            # Extract PEX and geometry data
            pex_data = comprehensive_results.get("pex", {})
            geometry_data = comprehensive_results.get("geometric", {})

            # Copy curated artifacts to the **final** per-trial results dir
            trial_out_dir.mkdir(parents=True, exist_ok=True)
            files_to_copy = [
                gds_file,
                f"{component_name}.drc.rpt",
                f"{component_name}.lvs.rpt",
                f"{component_name}_pex.spice",
                f"{component_name}.res.ext",
                f"{component_name}.ext",
                f"{component_name}_lvsmag.spice",
                f"{component_name}_sim.spice",
            ]
            for file_path in files_to_copy:
                p = Path(file_path)
                if p.exists():
                    shutil.copy(p, trial_out_dir / p.name)

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
                "output_directory": str(trial_out_dir),
                # PEX data
                "pex_status": pex_data.get("status", "not run"),
                "total_resistance_ohms": pex_data.get("total_resistance_ohms", 0.0),
                "total_capacitance_farads": pex_data.get("total_capacitance_farads", 0.0),
                # Geometry data
                "area_um2": geometry_data.get("raw_area_um2", 0.0),
                "symmetry_horizontal": geometry_data.get("symmetry_score_horizontal", 0.0),
                "symmetry_vertical": geometry_data.get("symmetry_score_vertical", 0.0),
            }

            pex_status_short = "✓" if pex_data.get("status") == "PEX Complete" else "✗"
            nmos_w, pmos_w = params["width"]
            nmos_f, pmos_f = params["fingers"]
            param_summary = f"NMOS:{nmos_w:.1f}μm×{nmos_f}f, PMOS:{pmos_w:.1f}μm×{pmos_f}f"
            logger.info(
                f"✅ Sample {trial_num:04d} completed in {trial_time:.1f}s "
                f"(DRC: {'✓' if drc_result else '✗'}, LVS: {'✓' if lvs_result else '✗'}, PEX: {pex_status_short}) "
                f"[{param_summary}]"
            )
            return result

    except Exception as e:
        trial_time = time.time() - trial_start
        logger.error(f"❌ Sample {trial_num:04d} failed: {e}")
        return {
            "sample_id": trial_num,
            "component_name": f"tg_sample_{trial_num:04d}",
            "success": False,
            "error": str(e),
            "execution_time": trial_time,
            "parameters": make_json_serializable(params),
        }

    finally:
        # Clean ONLY this trial's scratch via CWD-scoped globbing
        with chdir(trial_work_dir):
            cleanup_files()
            try:
                import gdsfactory as gf
            except ImportError:
                import gdsfactory as gf
            if hasattr(gf, 'clear_cache'):
                gf.clear_cache()
            if hasattr(gf, 'clear_cell_cache'):
                gf.clear_cell_cache()

from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
# Parallelized
def run_dataset_generation(parameters, output_dir, max_workers=1):
    """Run the dataset generation for all parameters (in parallel, per-trial isolation)."""
    n_samples = len(parameters)
    logger.info(f"🚀 Starting Transmission Gate Dataset Generation for {n_samples} samples")

    # Prepare top-level dirs
    out_dir = Path(output_dir)
    work_root = out_dir / "_work"
    out_dir.mkdir(exist_ok=True)
    work_root.mkdir(exist_ok=True)

    # Save parameter configuration
    with open(out_dir / "tg_parameters.json", 'w') as f:
        json.dump(parameters, f, indent=2)

    results = []
    total_start = time.time()
    logger.info(f"📊 Processing {n_samples} transmission gate samples in parallel...")
    logger.info(f"Using {max_workers} parallel workers")

    futures = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for i, params in enumerate(parameters, start=1):
            futures.append(executor.submit(run_single_evaluation, i, params, output_dir))

        completed = 0
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            completed += 1

            # Progress logging similar to your sequential version
            if completed % 10 == 0 or completed < 5:
                success_rate = (
                    sum(1 for r in results if r.get("success")) / len(results) * 100
                    if results else 0.0
                )
                elapsed = time.time() - total_start
                avg_time = elapsed / completed
                eta = avg_time * (n_samples - completed)
                logger.info(
                    f"📈 Progress: {completed}/{n_samples} "
                    f"({completed/n_samples*100:.1f}%) - "
                    f"Success: {success_rate:.1f}% - "
                    f"Elapsed: {elapsed/60:.1f}m - ETA: {eta/60:.1f}m"
                )

    # Final summary (unchanged)
    total_time = time.time() - total_start
    successful = [r for r in results if r.get("success")]
    success_rate = (len(successful) / len(results) * 100) if results else 0.0

    logger.info(f"\n🎉 Transmission Gate Dataset Generation Complete!")
    logger.info(f"📊 Total time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
    logger.info(f"📈 Success rate: {len(successful)}/{len(results)} ({success_rate:.1f}%)")

    if successful:
        drc_passes = sum(1 for r in successful if r.get("drc_pass"))
        lvs_passes = sum(1 for r in successful if r.get("lvs_pass"))
        pex_passes = sum(1 for r in successful if r.get("pex_status") == "PEX Complete")
        avg_time = sum(r["execution_time"] for r in successful) / len(successful)
        avg_area = sum(r.get("area_um2", 0) for r in successful) / len(successful)
        avg_sym_h = sum(r.get("symmetry_horizontal", 0) for r in successful) / len(successful)
        avg_sym_v = sum(r.get("symmetry_vertical", 0) for r in successful) / len(successful)

        logger.info(f"   DRC passes: {drc_passes}/{len(successful)} ({drc_passes/len(successful)*100:.1f}%)")
        logger.info(f"   LVS passes: {lvs_passes}/{len(successful)} ({lvs_passes/len(successful)*100:.1f}%)")
        logger.info(f"   PEX passes: {pex_passes}/{len(successful)} ({pex_passes/len(successful)*100:.1f}%)")
        logger.info(f"   Average time per sample: {avg_time:.1f}s")
        logger.info(f"   Average area: {avg_area:.2f} μm²")
        logger.info(f"   Average symmetry (H/V): {avg_sym_h:.3f}/{avg_sym_v:.3f}")

    failed = [r for r in results if not r.get("success")]
    if failed:
        logger.info(f"\n⚠️ Failed Samples Summary ({len(failed)} total):")
        error_counts = {}
        for r in failed:
            error = r.get("error", "Unknown error")
            error_key = error.split('\n')[0][:50]
            error_counts[error_key] = error_counts.get(error_key, 0) + 1
        for error, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"   {count}x: {error}")

    # Persist results/summary (same as before)
    results_file = out_dir / "tg_results.json"
    try:
        serializable_results = make_json_serializable(results)
        with open(results_file, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        logger.info(f"📄 Results saved to: {results_file}")
    except Exception as e:
        logger.error(f"Failed to save JSON results: {e}")

    df_results = pd.DataFrame(results)
    summary_file = out_dir / "tg_summary.csv"
    df_results.to_csv(summary_file, index=False)
    logger.info(f"📄 Summary saved to: {summary_file}")

    # Threshold as before
    return success_rate >= 50, len(successful), len(results)

import argparse
def main():
    """Main function for Dataset generation"""

    # Argument parsing
    parser = argparse.ArgumentParser(description="Dataset Generator - 100 Samples")
    parser.add_argument("json_file",    type=str,                   help="Path to the JSON file containing parameters")
    parser.add_argument("--n_cores",    type=int, default=1,        help="Number of CPU cores to use") # Number of CPU cores to use, default=1
    parser.add_argument("--output_dir", type=str, default="result", help="Output directory for the generated dataset")
    parser.add_argument("-y", "--yes", action="store_true", help="Automatic yes to prompts")
    args = parser.parse_args()
    json_file = Path(args.json_file).resolve()
    output_dir = args.output_dir
    n_cores = args.n_cores if args.n_cores > 0 else 1
    if n_cores > (os.cpu_count()):
        n_cores = os.cpu_count()
    print("="*30+" Arguments "+"="*30)
    print(f"Using {n_cores} CPU cores for parallel processing")
    print(f"Input file: {json_file}")
    print(f"Output will be saved to: {output_dir}")
    print("="*70)
    
    # Load parameters from JSON
    # Todo: make this work with other kind of cells
    try:
        parameters = load_tg_parameters_from_json(json_file)
        n_samples = len(parameters)
        print(f"Loaded {n_samples} parameter combinations")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print(f"Make sure you have run 'python elhs.py' first to generate the parameters")
        return False
    except Exception as e:
        print(f"❌ Error loading parameters: {e}")
        return False
    
    # Show parameter distribution
    widths_nmos = [p["width"][0] for p in parameters]
    widths_pmos = [p["width"][1] for p in parameters]
    print(f"\n📋 Parameter Distribution:")
    print(f"   NMOS width range: {min(widths_nmos):.2f} - {max(widths_nmos):.2f} μm")
    print(f"   PMOS width range: {min(widths_pmos):.2f} - {max(widths_pmos):.2f} μm")
    print(f"   Finger combinations: {len(set(tuple(p['fingers']) for p in parameters))} unique")
    print(f"   Multiplier combinations: {len(set(tuple(p['multipliers']) for p in parameters))} unique")
    print(f"\n📋 Sample Parameter Examples:")
    for i, params in enumerate(parameters[:3], 1):
        nmos_w, pmos_w = params["width"]
        nmos_l, pmos_l = params["length"]
        nmos_f, pmos_f = params["fingers"]
        nmos_m, pmos_m = params["multipliers"]
        print(f"   {i}. NMOS: {nmos_w:.2f}μm/{nmos_l:.3f}μm×{nmos_f}f×{nmos_m} | "
              f"PMOS: {pmos_w:.2f}μm/{pmos_l:.3f}μm×{pmos_f}f×{pmos_m}")
    
    # Prompt user to continue
    print(f"\nContinue with transmission gate dataset generation for {n_samples} samples? (y/n): ", end="")
    response = input().lower().strip()
    if response != 'y':
        print("Stopping as requested.")
        return True
    
    # Generate dataset
    print(f"\nStarting generation of {n_samples} transmission gate samples...")
    success, passed, total = run_dataset_generation(parameters, output_dir, max_workers=n_cores)
    
    if success:
        print(f"\n🎉 Transmission gate dataset generation completed successfully!")
    else:
        print(f"\n⚠️ Dataset generation completed with issues")
    print(f"📊 Final results: {passed}/{total} samples successful")
    print(f"📁 Dataset saved to: {output_dir}/")
    return success


if __name__ == "__main__":
    main()