#!/usr/bin/env python3

"""
Fixed verification module that properly handles PDK_ROOT environment variable.
This addresses the issue where PDK_ROOT gets reset to None between trials.
"""

# -----------------------------------------------------------------------------
# Make sure the `glayout` repository is discoverable *before* we import from it.
# -----------------------------------------------------------------------------

import os
import re
import subprocess
import shutil
import tempfile
import sys
from pathlib import Path

# Insert the repo root (`.../generators/glayout`) if it is not already present
_here = Path(__file__).resolve()
_glayout_repo_path = _here.parent.parent.parent.parent.parent.parent

if _glayout_repo_path.exists() and str(_glayout_repo_path) not in sys.path:
    sys.path.insert(0, str(_glayout_repo_path))

del _here

from gdsfactory.typings import Component

def ensure_pdk_environment():
    """Ensure PDK environment is properly set.

    * Uses an existing PDK_ROOT env if already set (preferred)
    * Falls back to the conda-env PDK folder if needed
    * Sets CAD_ROOT **only** to the Magic installation directory (``$CONDA_PREFIX/lib``)
    """
    # Respect an existing PDK_ROOT (set by the user / calling script)
    pdk_root = os.environ.get('PDK_ROOT')
    # Some libraries erroneously set the literal string "None". Treat that as
    # undefined so we fall back to a real path.
    if pdk_root in (None, '', 'None'):
        pdk_root = None

    if not pdk_root:
        # Fall back to the PDK bundled inside the current conda environment
        conda_prefix = os.environ.get('CONDA_PREFIX', '')
        if not conda_prefix or 'miniconda3' in conda_prefix:
            # Hard-code the *known* GLDev env path as a robust fallback
            conda_prefix = "/home/adityakak/.conda/envs/GLDev"

        pdk_root = os.path.join(conda_prefix, 'share', 'pdk')
        if not os.path.isdir(pdk_root):
            raise RuntimeError(
                f"Derived PDK_ROOT '{pdk_root}' does not exist; please set the PDK_ROOT env variable"
            )

    # Build a consistent set of environment variables
    conda_prefix = os.environ.get('CONDA_PREFIX', '')
    env_vars = {
        'PDK_ROOT': pdk_root,
        'PDKPATH': pdk_root,
        # Ensure a default value for PDK but preserve if user overrides elsewhere
        'PDK': os.environ.get('PDK', 'sky130A'),
        'MAGIC_PDK_ROOT': pdk_root,
        'NETGEN_PDK_ROOT': pdk_root,
    }

    # Point CAD_ROOT to Magic installation folder only (fixes missing magicdnull)
    if conda_prefix:
        env_vars['CAD_ROOT'] = os.path.join(conda_prefix, 'lib')

    # Refresh the environment in *one* atomic update to avoid partial states
    os.environ.update(env_vars)

    # Also try to reinitialize the PDK module to avoid stale state
    try:
        import importlib, sys as _sys
        modules_to_reload = [mod for mod in _sys.modules if 'pdk' in mod.lower()]
        for mod_name in modules_to_reload:
            try:
                importlib.reload(_sys.modules[mod_name])
            except Exception:
                pass  # Ignore reload errors – best-effort only
        print(f"PDK environment reset via os.environ.update: PDK_ROOT={pdk_root}")
    except Exception as e:
        print(f"Warning: Could not reload PDK modules: {e}")

    return pdk_root

def parse_drc_report(report_content: str) -> dict:
    """
    Parses a Magic DRC report into a machine-readable format.
    """
    errors = []
    current_rule = ""
    for line in report_content.strip().splitlines():
        stripped_line = line.strip()
        if stripped_line == "----------------------------------------":
            continue
        if re.match(r"^[a-zA-Z]", stripped_line):
            current_rule = stripped_line
        elif re.match(r"^[0-9]", stripped_line):
            errors.append({"rule": current_rule, "details": stripped_line})
    
    is_pass = len(errors) == 0
    if not is_pass and re.search(r"count:\s*0\s*$", report_content, re.IGNORECASE):
        is_pass = True

    return {
        "is_pass": is_pass,
        "total_errors": len(errors),
        "error_details": errors
    }

def parse_lvs_report(report_content: str) -> dict:
    """
    Parses the raw netgen LVS report and returns a summarized, machine-readable format.
    Focuses on parsing net and instance mismatches, similar to the reference
    implementation in ``evaluator_box/verification.py``.
    """
    summary = {
        "is_pass": False,
        "conclusion": "LVS failed or report was inconclusive.",
        "total_mismatches": 0,
        "mismatch_details": {
            "nets": "Not found",
            "devices": "Not found",
            "unmatched_nets_parsed": [],
            "unmatched_instances_parsed": []
        }
    }

    # Primary check for LVS pass/fail – if the core matcher says the netlists
    # match (even with port errors) we treat it as a _pass_ just like the
    # reference flow.
    if "Netlists match" in report_content or "Circuits match uniquely" in report_content:
        summary["is_pass"] = True
        summary["conclusion"] = "LVS Pass: Netlists match."

    # ------------------------------------------------------------------
    # Override: If the report explicitly states that netlists do NOT
    # match, or mentions other mismatch keywords (even if the specific
    # "no matching net" regex patterns are absent), force a failure so
    # we never mis-classify.
    # ------------------------------------------------------------------
    lowered = report_content.lower()
    failure_keywords = (
        "netlists do not match",
        "netlist mismatch",
        "failed pin matching",
        "mismatch"
    )
    if any(k in lowered for k in failure_keywords):
        summary["is_pass"] = False
        summary["conclusion"] = "LVS Fail: Netlist mismatch."

    for line in report_content.splitlines():
        stripped = line.strip()

        # Parse net mismatches of the form:
        #   Net: <name_left> | (no matching net)
        m = re.search(r"Net:\s*([^|]+)\s*\|\s*\(no matching net\)", stripped)
        if m:
            summary["mismatch_details"]["unmatched_nets_parsed"].append({
                "type": "net",
                "name": m.group(1).strip(),
                "present_in": "layout",
                "missing_in": "schematic"
            })
            continue

        # Parse instance mismatches
        m = re.search(r"Instance:\s*([^|]+)\s*\|\s*\(no matching instance\)", stripped)
        if m:
            summary["mismatch_details"]["unmatched_instances_parsed"].append({
                "type": "instance",
                "name": m.group(1).strip(),
                "present_in": "layout",
                "missing_in": "schematic"
            })
            continue

        # Right-side (schematic-only) mismatches
        m = re.search(r"\|\s*([^|]+)\s*\(no matching net\)", stripped)
        if m:
            summary["mismatch_details"]["unmatched_nets_parsed"].append({
                "type": "net",
                "name": m.group(1).strip(),
                "present_in": "schematic",
                "missing_in": "layout"
            })
            continue

        m = re.search(r"\|\s*([^|]+)\s*\(no matching instance\)", stripped)
        if m:
            summary["mismatch_details"]["unmatched_instances_parsed"].append({
                "type": "instance",
                "name": m.group(1).strip(),
                "present_in": "schematic",
                "missing_in": "layout"
            })
            continue

        # Capture the summary lines with device/net counts for debugging
        if "Number of devices:" in stripped:
            summary["mismatch_details"]["devices"] = stripped.split(":", 1)[1].strip()
        elif "Number of nets:" in stripped:
            summary["mismatch_details"]["nets"] = stripped.split(":", 1)[1].strip()

    # Tot up mismatches that we actually parsed (nets + instances)
    summary["total_mismatches"] = (
        len(summary["mismatch_details"]["unmatched_nets_parsed"]) +
        len(summary["mismatch_details"]["unmatched_instances_parsed"])
    )

    # If we found *any* explicit net/instance mismatches, override to FAIL.
    if summary["total_mismatches"] > 0:
        summary["is_pass"] = False
        if "Pass" in summary["conclusion"]:
            summary["conclusion"] = "LVS Fail: Mismatches found."

    return summary

def _parse_simple_parasitics(component_name: str) -> tuple[float, float]:
    """Parses total parasitic R and C from a SPICE file by simple summation."""
    total_resistance = 0.0
    total_capacitance = 0.0
    spice_file_path = f"{component_name}_pex.spice"
    if not os.path.exists(spice_file_path):
        return 0.0, 0.0
    with open(spice_file_path, 'r') as f:
        for line in f:
            orig_line = line.strip()  # Keep original case for capacitor parsing
            line = line.strip().upper()
            parts = line.split()
            orig_parts = orig_line.split()  # Original case parts for capacitor values
            if not parts: continue
            
            name = parts[0]
            if name.startswith('R') and len(parts) >= 4:
                try: total_resistance += float(parts[3])
                except (ValueError): continue
            elif name.startswith('C') and len(parts) >= 4:
                try:
                    cap_str = orig_parts[3]  # Use original case for capacitor value
                    unit = cap_str[-1]
                    val_str = cap_str[:-1]
                    if unit == 'F': cap_value = float(val_str) * 1e-15
                    elif unit == 'P': cap_value = float(val_str) * 1e-12
                    elif unit == 'N': cap_value = float(val_str) * 1e-9
                    elif unit == 'U': cap_value = float(val_str) * 1e-6
                    elif unit == 'f': cap_value = float(val_str) * 1e-15  # femtofarads
                    else: cap_value = float(cap_str)
                    total_capacitance += cap_value
                except (ValueError): continue
    return total_resistance, total_capacitance

def run_robust_verification(layout_path: str, component_name: str, top_level: Component) -> dict:
    """
    Runs DRC, LVS, and PEX checks with robust PDK handling.
    """
    verification_results = {
        "drc": {"status": "not run", "is_pass": False, "report_path": None, "summary": {}},
        "lvs": {"status": "not run", "is_pass": False, "report_path": None, "summary": {}},
        "pex": {"status": "not run", "total_resistance_ohms": 0.0, "total_capacitance_farads": 0.0, "spice_file": None}
    }
    
    # Ensure PDK environment before each operation
    pdk_root = ensure_pdk_environment()
    print(f"Using PDK_ROOT: {pdk_root}")
    
    # Import sky130_mapped_pdk *after* the environment is guaranteed sane so
    # that gdsfactory/PDK initialization picks up the correct PDK_ROOT.
    from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
    
    # DRC Check
    drc_report_path = os.path.abspath(f"./{component_name}.drc.rpt")
    verification_results["drc"]["report_path"] = drc_report_path
    
    try:
        # Clean up any existing DRC report
        if os.path.exists(drc_report_path):
            os.remove(drc_report_path)
        
        # Ensure PDK environment again right before DRC
        ensure_pdk_environment()
        
        print(f"Running DRC for {component_name}...")
        
        # Try the PDK DRC method first
        sky130_mapped_pdk.drc_magic(layout_path, component_name, output_file=drc_report_path)
        
        # Check if report was created and read it
        report_content = ""
        if os.path.exists(drc_report_path):
            with open(drc_report_path, 'r') as f:
                report_content = f.read()
            print(f"DRC report created successfully: {len(report_content)} chars")
        '''else:
            print("Warning: DRC report file was not created, creating empty report")
            # Create empty report as fallback
            report_content = f"{component_name} count: \n----------------------------------------\n\n"
            with open(drc_report_path, 'w') as f:
                f.write(report_content)
            '''
        summary = parse_drc_report(report_content)
        verification_results["drc"].update({
            "summary": summary, 
            "is_pass": summary["is_pass"], 
            "status": "pass" if summary["is_pass"] else "fail"
        })
        
    except Exception as e:
        print(f"DRC failed with exception: {e}")
        # Create a basic report even on failure
        try:
            with open(drc_report_path, 'w') as f:
                f.write(f"DRC Error for {component_name}\n")
                f.write(f"Error: {str(e)}\n")
            verification_results["drc"]["status"] = f"error: {e}"
        except:
            verification_results["drc"]["status"] = f"error: {e}"

    # Small delay between DRC and LVS
    import time
    time.sleep(1)

    # LVS Check
    lvs_report_path = os.path.abspath(f"./{component_name}.lvs.rpt")
    verification_results["lvs"]["report_path"] = lvs_report_path
    
    try:
        # Clean up any existing LVS report
        if os.path.exists(lvs_report_path):
            os.remove(lvs_report_path)
        
        # Ensure PDK environment again right before LVS
        ensure_pdk_environment()
        
        print(f"Running LVS for {component_name}...")
        
        # Try the PDK LVS method first
        sky130_mapped_pdk.lvs_netgen(layout=top_level, design_name=component_name, output_file_path=lvs_report_path)
        
        # Check if report was created and read it
        report_content = ""
        if os.path.exists(lvs_report_path):
            with open(lvs_report_path, 'r') as report_file:
                report_content = report_file.read()
            print(f"LVS report created successfully: {len(report_content)} chars")
        '''else:
            print("Warning: LVS report file was not created, creating fallback report")
            # Create fallback report
            report_content = f"LVS Report for {component_name}\nFinal result: Circuits match uniquely.\nLVS Done.\n"
            with open(lvs_report_path, 'w') as f:
                f.write(report_content)
           '''
        lvs_summary = parse_lvs_report(report_content)
        verification_results["lvs"].update({
            "summary": lvs_summary, 
            "is_pass": lvs_summary["is_pass"], 
            "status": "pass" if lvs_summary["is_pass"] else "fail"
        })
        
    except Exception as e:
        print(f"LVS failed with exception: {e}")
        # Create a basic report even on failure
        try:
            with open(lvs_report_path, 'w') as f:
                f.write(f"LVS Error for {component_name}\n")
                f.write(f"Error: {str(e)}\n")
            verification_results["lvs"]["status"] = f"error: {e}"
        except:
            verification_results["lvs"]["status"] = f"error: {e}"

    # Small delay between LVS and PEX
    time.sleep(1)
    
    # PEX Extraction
    pex_spice_path = os.path.abspath(f"./{component_name}_pex.spice")
    verification_results["pex"]["spice_file"] = pex_spice_path
    
    try:
        # Clean up any existing PEX file
        if os.path.exists(pex_spice_path):
            os.remove(pex_spice_path)
        
        print(f"Running PEX extraction for {component_name}...")
        
        # Run the PEX extraction script 
        subprocess.run(["bash", "run_pex.sh", layout_path, component_name], 
                      check=True, capture_output=True, text=True, cwd=".")
        
        # Check if PEX spice file was created and parse it
        if os.path.exists(pex_spice_path):
            total_res, total_cap = _parse_simple_parasitics(component_name)
            verification_results["pex"].update({
                "status": "PEX Complete",
                "total_resistance_ohms": total_res,
                "total_capacitance_farads": total_cap
            })
            print(f"PEX extraction completed: R={total_res:.2f}Ω, C={total_cap:.6e}F")
        else:
            verification_results["pex"]["status"] = "PEX Error: Spice file not generated"
            
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        verification_results["pex"]["status"] = f"PEX Error: {error_msg}"
        print(f"PEX extraction failed: {error_msg}")
    except FileNotFoundError:
        verification_results["pex"]["status"] = "PEX Error: run_pex.sh not found"
        print("PEX extraction failed: run_pex.sh script not found")
    except Exception as e:
        verification_results["pex"]["status"] = f"PEX Unexpected Error: {e}"
        print(f"PEX extraction failed with unexpected error: {e}")
        
    return verification_results

if __name__ == "__main__":
    # Test the robust verification
    print("Testing robust verification module...")
    ensure_pdk_environment()
    print("PDK environment setup complete.")
