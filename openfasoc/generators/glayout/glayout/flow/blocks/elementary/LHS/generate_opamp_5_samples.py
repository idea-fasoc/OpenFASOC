#!/usr/bin/env python3
"""
Opamp Dataset Generator - 5 Samples Version
================================================
This script generates a small **5-sample** dataset for the `opamp` composite block found in
`opamp.py`.  Each sample is laid-out, exported to GDS, and run through the same comprehensive
evaluation pipeline (DRC, LVS, PEX, geometry) used by the FVF and TG dataset scripts.

It closely follows the proven `generate_fvf_360_robust_fixed.py` flow but is trimmed down for
quick experimentation: short runtime, deterministic seeding, JSON/CSV result dumps, and
checkpoint-resume support.

Usage (example):
----------------
```bash
# --- Environment (as requested) ---------------------------------------------
conda activate GLdev
export PDK_ROOT=/home/adityakak/.conda/envs/GLDev/share/pdk
cd /home/adityakak/OpenFASOC/openfasoc/generators/glayout/glayout/flow/blocks/elementary/LHS
chmod +x run_pex.sh

# --- Generate the dataset ----------------------------------------------------
python3 generate_opamp_5_samples.py
```

The dataset (GDS, reports, JSON, CSV) will be written to
`opamp_dataset_5_samples/`.\n"""
# ---------------------------------------------------------------------------------
# Standard library imports
# ---------------------------------------------------------------------------------
import logging
import os
import sys
import time
import json
import shutil
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------------
# Ensure the *local* `glayout` package is discoverable *before* importing anything
# that indirectly relies on it (to avoid mismatched PDK_PATH issues).
# ---------------------------------------------------------------------------------
_here = Path(__file__).resolve()
_glayout_repo_path = _here.parent.parent.parent.parent.parent.parent

# Fallback hard-coded path (update if repo structure changes)
if not _glayout_repo_path.exists():
    _glayout_repo_path = Path("/home/adityakak/OpenFASOC/openfasoc/generators/glayout")

if _glayout_repo_path.exists() and str(_glayout_repo_path) not in sys.path:
    sys.path.insert(0, str(_glayout_repo_path))

del _here, _glayout_repo_path

# ---------------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------------
# Post-PDK import helper utilities
# ---------------------------------------------------------------------------------
GLOBAL_SKY130_PDK = None  # Cached stable PDK instance


def get_global_pdk():
    """Return a *stable* sky130_mapped_pdk instance (cached)."""
    global GLOBAL_SKY130_PDK
    if GLOBAL_SKY130_PDK is None:
        from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as _pdk
        GLOBAL_SKY130_PDK = _pdk
    return GLOBAL_SKY130_PDK


# Shared helper to set / refresh environment
from robust_verification import ensure_pdk_environment  # Re-use single source of truth


def setup_environment() -> str:
    """Prepare the PDK environment **once per trial**.

    This mirrors the logic used in other dataset generators so that every entry
    point refreshes the environment atomically (preventing drift).
    """
    pdk_root = ensure_pdk_environment()

    # Safe import of gdsfactory *after* PDK is locked-in
    try:
        import gdsfactory as gf
    except ImportError:
        import gdsfactory as gf  # pragma: no cover (should always succeed)

    # Disable gdsfactory component cache to avoid stale class references
    try:
        gf.CONFIG.use_cache = False  # Old style
    except AttributeError:
        try:
            gf.config.CONF.use_cache = False  # Newer style
        except Exception:
            pass

    # Make sure `glayout` path is in PYTHONPATH for child processes
    glayout_path = "/home/adityakak/OpenFASOC/openfasoc/generators/glayout"
    if glayout_path not in sys.path:
        sys.path.insert(0, glayout_path)

    current_ppath = os.environ.get("PYTHONPATH", "")
    if glayout_path not in current_ppath.split(":" ):
        os.environ["PYTHONPATH"] = f"{glayout_path}:{current_ppath}"

    logger.info(f"Environment refreshed: PDK_ROOT={pdk_root}")
    return pdk_root


# ---------------------------------------------------------------------------------
# Opamp generation helper
# ---------------------------------------------------------------------------------

def robust_opamp(_, **params):
    """Create an opamp component with fresh MappedPDK and add pin labels."""
    from opamp import opamp as opamp_gen, sky130_add_opamp_2_labels

    pdk = get_global_pdk()  # Re-use stable instance
    comp = opamp_gen(pdk=pdk, **params)

    # Add sky130-style labels so Magic extracts pins correctly
    try:
        comp = sky130_add_opamp_2_labels(comp)
    except Exception as e:
        logger.warning(f"Failed to add pin labels: {e}")

    return comp


# ---------------------------------------------------------------------------------
# Parameter generation (synthetic, 5 combos)
# ---------------------------------------------------------------------------------

def generate_opamp_parameters(num_samples: int = 5) -> List[Dict[str, Any]]:
    """Return a list of *num_samples* dictionaries containing opamp parameters."""
    params: List[Dict[str, Any]] = []

    # Sample 1 – baseline (defaults)
    params.append({})

    # Sample 2 – wider diff-pair & bias
    params.append({
        "half_diffpair_params": (7, 1, 4),
        "diffpair_bias": (7, 2, 4),
    })

    # Sample 3 – larger common-source stage
    params.append({
        "half_common_source_params": (8, 1, 12, 3),
        "half_common_source_bias": (7, 2, 10, 2),
    })

    # Sample 4 – beefier output buffer
    params.append({
        "output_stage_params": (6, 1, 20),
        "output_stage_bias": (6, 2, 6),
    })

    # Sample 5 – smaller pload + no output stage (two-stage only)
    params.append({
        "half_pload": (5, 1, 4),
        "add_output_stage": False,
    })

    logger.info(f"Generated {len(params)} synthetic opamp parameter combinations")

    # Ensure *every* sample disables the optional output buffer per user request
    for p in params:
        p["add_output_stage"] = False

    return params[:num_samples]


# ---------------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------------

def cleanup_files():
    """Remove leftover files between trials to keep workspace clean."""
    patterns = [
        "*.gds", "*.drc.rpt", "*.lvs.rpt", "*.ext", "*.spice",
        "*.res.ext", "*.sim", "*.nodes", "*_lvsmag.spice", "*_sim.spice",
        "*_pex.spice", "*.pex.spice",
    ]
    import glob
    for pattern in patterns:
        for f in glob.glob(pattern):
            try:
                os.remove(f)
            except OSError:
                pass


def make_json_serializable(obj):
    """Convert numpy / PDK objects so `json.dump` doesn’t crash."""
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [make_json_serializable(i) for i in obj]
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif hasattr(obj, "__dict__"):
        try:
            return make_json_serializable(obj.__dict__)
        except Exception:
            return str(obj)
    else:
        try:
            json.dumps(obj)
            return obj
        except Exception:
            return str(obj)


# ---------------------------------------------------------------------------------
# Core per-trial evaluation
# ---------------------------------------------------------------------------------

from pathlib import Path


def run_single_evaluation(trial_num: int, params: Dict[str, Any], output_dir: str):
    """Lay-out, evaluate, and collect metrics for **one** sample."""
    t0 = time.time()

    # Deterministic seeding (helps reproduce geometry variations)
    import random
    random.seed(trial_num * 1000)
    np.random.seed(trial_num * 1000)
    os.environ["PYTHONHASHSEED"] = str(trial_num * 1000)

    logger.info(f"Trial {trial_num}: seed={trial_num * 1000}")

    # Fresh environment each run
    setup_environment()

    # Clear gdsfactory caches to avoid class mismatch across trials
    import gdsfactory as gf
    if hasattr(gf, "clear_cache"):
        gf.clear_cache()
    if hasattr(gf, "clear_cell_cache"):
        gf.clear_cell_cache()

    # Reload PDK module to sidestep pydantic caching bugs
    import importlib
    if "glayout.flow.pdk.sky130_mapped" in sys.modules:
        importlib.reload(sys.modules["glayout.flow.pdk.sky130_mapped"])

    # --- Generate layout ------------------------------------------------------
    comp_name = f"opamp_sample_{trial_num:04d}"
    comp = robust_opamp(None, **params)
    comp.name = comp_name
    gds_path = f"{comp_name}.gds"
    comp.write_gds(gds_path)

    # --- Evaluation -----------------------------------------------------------
    from evaluator_wrapper import run_evaluation
    results = run_evaluation(gds_path, comp_name, comp)

    # --- Gather / persist -----------------------------------------------------
    trial_dir = Path(output_dir) / f"sample_{trial_num:04d}"
    trial_dir.mkdir(exist_ok=True)

    # Copy key files for later inspection
    for fname in [
        gds_path,
        f"{comp_name}.drc.rpt",
        f"{comp_name}.lvs.rpt",
        f"{comp_name}_pex.spice",
        f"{comp_name}.res.ext",
    ]:
        if Path(fname).exists():
            shutil.copy(fname, trial_dir / fname)

    elapsed = time.time() - t0
    success = results["drc"]["is_pass"] and results["lvs"]["is_pass"]

    summary = {
        "sample_id": trial_num,
        "component_name": comp_name,
        "success": success,
        "drc_pass": results["drc"]["is_pass"],
        "lvs_pass": results["lvs"]["is_pass"],
        "execution_time": elapsed,
        "parameters": make_json_serializable(params),
        "output_directory": str(trial_dir),
        # PEX / geometry summaries
        "pex_status": results.get("pex", {}).get("status", "not run"),
        "total_resistance_ohms": results.get("pex", {}).get("total_resistance_ohms", 0.0),
        "total_capacitance_farads": results.get("pex", {}).get("total_capacitance_farads", 0.0),
        "area_um2": results.get("geometric", {}).get("raw_area_um2", 0.0),
    }

    logger.info(
        f"✅ Trial {trial_num:04d} finished in {elapsed:.1f}s (DRC: {'✓' if summary['drc_pass'] else '✗'}, "
        f"LVS: {'✓' if summary['lvs_pass'] else '✗'})"
    )

    cleanup_files()
    return summary


# ---------------------------------------------------------------------------------
# Dataset driver
# ---------------------------------------------------------------------------------


def run_dataset_generation(n_samples: int, output_dir: str, checkpoint_interval: int = 5):
    logger.info(f"🚀 Starting Opamp Dataset Generation for {n_samples} samples")

    Path(output_dir).mkdir(exist_ok=True)

    parameters = generate_opamp_parameters(n_samples)

    # Persist parameter list for transparency
    with open(Path(output_dir) / "opamp_parameters.json", "w") as f:
        json.dump(parameters, f, indent=2)

    results = []
    total_start = time.time()

    for i in range(n_samples):
        res = run_single_evaluation(i + 1, parameters[i], output_dir)
        results.append(res)

        # Simple checkpoint (overwrite each time)
        if (i + 1) % checkpoint_interval == 0 or (i + 1) == n_samples:
            with open(Path(output_dir) / "checkpoint.json", "w") as f:
                json.dump({"results": make_json_serializable(results)}, f, indent=2)
            logger.info(f"💾 Checkpoint saved at sample {i + 1}")

    # --- Summary -------------------------------------------------------------
    elapsed = time.time() - total_start
    successes = [r for r in results if r["success"]]
    success_rate = len(successes) / len(results) * 100 if results else 0.0

    logger.info(
        """\n🎉 Dataset Generation Complete!\n    Total time   : %.1fs\n    Success rate : %d/%d (%.1f%%)\n"""
        % (elapsed, len(successes), len(results), success_rate)
    )

    # Persist detailed & summary CSV/JSON
    with open(Path(output_dir) / "opamp_results.json", "w") as f:
        json.dump(make_json_serializable(results), f, indent=2)
    pd.DataFrame(results).to_csv(Path(output_dir) / "opamp_summary.csv", index=False)

    return success_rate >= 80.0


# ---------------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------------


def main():
    n_samples = 5
    output_dir = "opamp_dataset_5_samples"

    print("🚀 Generating Opamp dataset (5 samples)…")
    ok = run_dataset_generation(n_samples, output_dir)

    if ok:
        print("\n✅ Dataset generation completed successfully (>80% pass rate)")
    else:
        print("\n⚠️  Dataset generation finished but some samples failed DRC/LVS")


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 