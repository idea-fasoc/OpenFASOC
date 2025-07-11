#!/usr/bin/env python3
"""
Op-amp Dataset Generator – 250 Samples
======================================
Reads the parameter combinations produced by `elhs.py` in
`opamp_250_params/opamp_params.json`, lays out each op-amp (buffer disabled),
then runs the full verification / physical-feature extraction flow.

The structure follows the proven `generate_diff_pair_dataset.py` template but
with op-amp-specific tweaks and lighter logging.
"""
# ---------------------------------------------------------------------------------
# Standard imports
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
# Make sure local `glayout` package is importable BEFORE anything that depends on it
# ---------------------------------------------------------------------------------
_here = Path(__file__).resolve()
_glayout_repo_path = _here.parent.parent.parent.parent.parent.parent
if not _glayout_repo_path.exists():
    _glayout_repo_path = Path("/home/adityakak/OpenFASOC/openfasoc/generators/glayout")
if str(_glayout_repo_path) not in sys.path:
    sys.path.insert(0, str(_glayout_repo_path))

del _here, _glayout_repo_path

# ---------------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------------
# Stable PDK accessor
# ---------------------------------------------------------------------------------
GLOBAL_SKY130_PDK = None

def get_global_pdk():
    global GLOBAL_SKY130_PDK
    if GLOBAL_SKY130_PDK is None:
        from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as _pdk
        GLOBAL_SKY130_PDK = _pdk
    return GLOBAL_SKY130_PDK

# Use shared env helper
from robust_verification import ensure_pdk_environment

def setup_environment() -> str:
    pdk_root = ensure_pdk_environment()
    try:
        import gdsfactory as gf
    except ImportError:
        import gdsfactory as gf
    # disable cache
    try:
        gf.CONFIG.use_cache = False
    except AttributeError:
        try:
            gf.config.CONF.use_cache = False
        except Exception:
            pass
    glayout_path = "/home/adityakak/OpenFASOC/openfasoc/generators/glayout"
    if glayout_path not in sys.path:
        sys.path.insert(0, glayout_path)
    pp = os.environ.get("PYTHONPATH", "")
    if glayout_path not in pp.split(":"):
        os.environ["PYTHONPATH"] = f"{glayout_path}:{pp}"
    logger.info(f"Environment refreshed: PDK_ROOT={pdk_root}")
    return pdk_root

# ---------------------------------------------------------------------------------
# Op-amp wrapper (adds labels)
# ---------------------------------------------------------------------------------

def robust_opamp(_, **params):
    from opamp import opamp as opamp_gen, sky130_add_opamp_2_labels
    pdk = get_global_pdk()
    comp = opamp_gen(pdk=pdk, **params)
    try:
        comp = sky130_add_opamp_2_labels(comp)
    except Exception as e:
        logger.warning(f"Failed to add pin labels: {e}")
    return comp

# ---------------------------------------------------------------------------------
# Parameter loading
# ---------------------------------------------------------------------------------

def load_opamp_parameters(n_samples: int | None = None) -> List[Dict[str, Any]]:
    param_file = (
        Path(__file__).parent / "opamp_250_params" / "opamp_params.json"
    )
    with open(param_file, "r") as f:
        params: List[Dict[str, Any]] = json.load(f)
    if n_samples is None:
        n_samples = len(params)
    logger.info(f"Loaded {n_samples} parameter sets from {param_file}")
    return params[:n_samples]

# ---------------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------------

def cleanup_files():
    import glob
    patterns = [
        "*.gds", "*.drc.rpt", "*.lvs.rpt", "*.ext", "*.spice",
        "*.res.ext", "*.sim", "*.nodes", "*_lvsmag.spice", "*_sim.spice",
        "*_pex.spice", "*.pex.spice",
    ]
    for pat in patterns:
        for f in glob.glob(pat):
            try:
                os.remove(f)
            except OSError:
                pass

def make_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [make_serializable(i) for i in obj]
    if isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    try:
        json.dumps(obj)
        return obj
    except Exception:
        return str(obj)

# ---------------------------------------------------------------------------------
# Single trial
# ---------------------------------------------------------------------------------

def run_single(trial_num: int, params: Dict[str, Any], out_dir: Path) -> Dict[str, Any]:
    t0 = time.time()
    import random
    random.seed(trial_num * 1000)
    np.random.seed(trial_num * 1000)
    os.environ["PYTHONHASHSEED"] = str(trial_num * 1000)

    setup_environment()

    # clear gf cache
    import gdsfactory as gf
    if hasattr(gf, "clear_cache"):
        gf.clear_cache()
    if hasattr(gf, "clear_cell_cache"):
        gf.clear_cell_cache()

    # reload pdk to avoid pydantic mismatch
    import importlib
    if "glayout.flow.pdk.sky130_mapped" in sys.modules:
        importlib.reload(sys.modules["glayout.flow.pdk.sky130_mapped"])

    comp_name = f"opamp_sample_{trial_num:04d}"
    comp = robust_opamp(None, **params)
    comp.name = comp_name
    gds_file = f"{comp_name}.gds"
    comp.write_gds(gds_file)

    from evaluator_wrapper import run_evaluation
    results = run_evaluation(gds_file, comp_name, comp)

    # persist artefacts
    sample_dir = out_dir / f"sample_{trial_num:04d}"
    sample_dir.mkdir(exist_ok=True)
    for fname in [gds_file, f"{comp_name}.drc.rpt", f"{comp_name}.lvs.rpt", f"{comp_name}_pex.spice", f"{comp_name}.res.ext"]:
        if Path(fname).exists():
            shutil.copy(fname, sample_dir / fname)

    elapsed = time.time() - t0
    success = results["drc"]["is_pass"] and results["lvs"]["is_pass"]

    summary = {
        "sample_id": trial_num,
        "component_name": comp_name,
        "success": success,
        "drc_pass": results["drc"]["is_pass"],
        "lvs_pass": results["lvs"]["is_pass"],
        "execution_time": elapsed,
        "parameters": make_serializable(params),
        "pex_status": results.get("pex", {}).get("status", "not run"),
        "total_resistance_ohms": results.get("pex", {}).get("total_resistance_ohms", 0.0),
        "total_capacitance_farads": results.get("pex", {}).get("total_capacitance_farads", 0.0),
        "area_um2": results.get("geometric", {}).get("raw_area_um2", 0.0),
    }

    logger.info(
        f"Trial {trial_num:04d}: {elapsed:.1f}s – DRC {'✓' if summary['drc_pass'] else '✗'} | LVS {'✓' if summary['lvs_pass'] else '✗'}"
    )

    cleanup_files()
    return summary

# ---------------------------------------------------------------------------------
# Dataset driver
# ---------------------------------------------------------------------------------

def run_dataset(n_samples: int = 250):
    out_dir = Path("opamp_dataset_250")
    out_dir.mkdir(exist_ok=True)

    params = load_opamp_parameters(n_samples)
    results: List[Dict[str, Any]] = []

    for idx, p in enumerate(params, start=1):
        results.append(run_single(idx, p, out_dir))
        # quick checkpoint after each sample
        with open(out_dir / "checkpoint.json", "w") as f:
            json.dump({"results": make_serializable(results)}, f, indent=2)

    # summary
    successes = [r for r in results if r["success"]]
    rate = len(successes) / len(results) * 100 if results else 0.0
    logger.info(f"Dataset finished – success rate {len(successes)}/{len(results)} = {rate:.1f}%")

    # persist
    with open(out_dir / "opamp_results.json", "w") as f:
        json.dump(make_serializable(results), f, indent=2)
    pd.DataFrame(results).to_csv(out_dir / "opamp_summary.csv", index=False)

    return rate >= 80.0

# ---------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------

if __name__ == "__main__":
    ok = run_dataset()
    sys.exit(0 if ok else 1) 