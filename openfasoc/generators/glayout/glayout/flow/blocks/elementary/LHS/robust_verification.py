# 



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
        
        # Try to derive pdk_root from conda_prefix first
        if conda_prefix:
            potential_pdk_root = os.path.join(conda_prefix, 'share', 'pdk')
            # If it doesn't exist, try with /envs/GLdev appended (common pattern)
            if not os.path.isdir(potential_pdk_root):
                potential_pdk_root = os.path.join(conda_prefix, 'envs', 'GLdev', 'share', 'pdk')
            
            if os.path.isdir(potential_pdk_root):
                pdk_root = potential_pdk_root
        
        # If still not found, use the known GLdev env path as fallback
        if not pdk_root or not os.path.isdir(pdk_root):
            pdk_root = "/home/adityakak/miniconda3/envs/GLdev/share/pdk"
            if not os.path.isdir(pdk_root):
                raise RuntimeError(
                    f"Could not find PDK at any expected location. Tried:\n"
                    f"  - $PDK_ROOT (not set)\n"
                    f"  - {conda_prefix}/share/pdk (not found)\n"
                    f"  - {pdk_root} (not found)\n"
                    f"Please set the PDK_ROOT environment variable to the correct path."
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
    passable_errors = []
    reviewable_errors = []
    critical_errors = []

    passable_phrases = ["spacing", "min spacing", "min enclosure", "min space"]
    critical_phrases = ["must be enclosed", "no overlap", "can not overlap", "can not straddle"]

    current_rule = ""
    for line in report_content.strip().splitlines():
        stripped_line = line.strip()
        if stripped_line == "----------------------------------------":
            continue
        if re.match(r"^[a-zA-Z]", stripped_line):
            current_rule = stripped_line
        elif re.match(r"^[0-9]", stripped_line):
            if any(phrase in current_rule.lower() for phrase in [p.lower() for p in passable_phrases]):
                passable_errors.append({"rule": current_rule, "details": stripped_line})
            elif any(phrase in current_rule.lower() for phrase in [p.lower() for p in critical_phrases]):
                critical_errors.append({"rule": current_rule, "details": stripped_line})
            else:
                reviewable_errors.append({"rule": current_rule, "details": stripped_line})
    total_errors = len(passable_errors) + len(reviewable_errors) + len(critical_errors)
    is_pass = total_errors == 0
    critical_error = len(critical_errors) > 0
    if not is_pass and re.search(r"count:\s*0\s*$", report_content, re.IGNORECASE):
        is_pass = True

    return {
        "is_pass": is_pass,
        "total_errors": total_errors,
        "passable_errors_count": len(passable_errors),
        "reviewable_errors_count": len(reviewable_errors),
        "critical_error": critical_error,
        "critical_errors_count": len(critical_errors),
        "passable_error_details": passable_errors,
        "reviewable_error_details": reviewable_errors,
        "critical_error_details": critical_errors
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
        
        # FIX: Pass pdk_root and magic_drc_file to use correct technology
        magic_drc_file = Path(pdk_root) / "sky130A" / "libs.tech" / "magic" / "sky130A.magicrc"
        sky130_mapped_pdk.drc_magic(
            layout_path, 
            component_name, 
            pdk_root=pdk_root,
            magic_drc_file=magic_drc_file,
            output_file=drc_report_path
        )
        
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
        
        # FIX: mappedpdk.py's lvs_netgen has an issue where passing an absolute path
        # as output_file_path causes problems - it tries to create a nested directory
        # structure and the temp directory gets cleaned up. Instead, we pass a simple
        # filename, then find and copy the report from the regression directory.
        # 
        # OLD CODE (commented out for tracking):
        # sky130_mapped_pdk.lvs_netgen(layout=top_level, design_name=component_name, 
        #                              output_file_path=lvs_report_path, copy_intermediate_files=True)
        
        # NEW CODE: Pass simple filename with pdk_root AND magic_drc_file, then copy from regression directory
        report_filename = f"{component_name}.lvs.rpt"
        # Construct path to the correct magicrc file
        magic_drc_file = Path(pdk_root) / "sky130A" / "libs.tech" / "magic" / "sky130A.magicrc"
        lvs_result = sky130_mapped_pdk.lvs_netgen(
            layout=top_level, 
            design_name=component_name,
            pdk_root=pdk_root,  # FIX: Must pass pdk_root to use correct technology
            magic_drc_file=magic_drc_file,  # FIX: Must pass magicrc file explicitly
            output_file_path=report_filename,  # Simple filename, not absolute path
            copy_intermediate_files=True
        )
        
        # The report gets saved to: glayout/regression/lvs/{component_name}/{report_filename}
        # We need to find it and copy it to our working directory
        import sys
        import shutil
        
        # Find the glayout package location to locate the regression directory
        glayout_module_path = None
        for path in sys.path:
            potential_path = Path(path) / "glayout" / "regression" / "lvs" / component_name / report_filename
            if potential_path.exists():
                glayout_module_path = potential_path
                print(f"Found LVS report at: {glayout_module_path}")
                break
        
        # Try alternate location (relative to mappedpdk.py)
        if glayout_module_path is None:
            try:
                import glayout
                glayout_root = Path(glayout.__file__).parent.parent
                # Check in both locations: glayout/flow/regression and glayout/regression
                for search_path in [
                    glayout_root / "glayout" / "flow" / "regression" / "lvs" / component_name / report_filename,
                    glayout_root / "regression" / "lvs" / component_name / report_filename
                ]:
                    if search_path.exists():
                        glayout_module_path = search_path
                        print(f"Found LVS report at: {glayout_module_path}")
                        break
            except:
                pass
        
        report_content = ""
        # Try to copy the report from regression directory
        if glayout_module_path and glayout_module_path.exists():
            shutil.copy(str(glayout_module_path), lvs_report_path)
            with open(lvs_report_path, 'r') as report_file:
                report_content = report_file.read()
            print(f"LVS report copied and read successfully: {len(report_content)} chars")
        elif os.path.exists(lvs_report_path):
            # Report might already be in the correct location
            with open(lvs_report_path, 'r') as report_file:
                report_content = report_file.read()
            print(f"LVS report found at expected location: {len(report_content)} chars")
        else:
            # Report not found - this is an error condition
            raise FileNotFoundError(f"LVS report not found at {lvs_report_path} or in regression directory")
        
        lvs_summary = parse_lvs_report(report_content)
        verification_results["lvs"].update({
            "summary": lvs_summary, 
            "is_pass": lvs_summary["is_pass"], 
            "status": "pass" if lvs_summary["is_pass"] else "fail"
        })
        
    except Exception as e:
        print(f"LVS failed with exception: {e}")
        import traceback
        traceback.print_exc()
        # Record the error without creating fallback reports
        verification_results["lvs"]["status"] = f"error: {e}"
        verification_results["lvs"]["is_pass"] = False
    
    # PEX Extraction
    pex_spice_path = os.path.abspath(f"./{component_name}_pex.spice")
    verification_results["pex"]["spice_file"] = pex_spice_path
    
    try:
        # Clean up any existing PEX file
        if os.path.exists(pex_spice_path):
            os.remove(pex_spice_path)
        
        print(f"Running PEX extraction for {component_name}...")
        
        # Find run_pex.sh relative to this file's location
        script_dir = Path(__file__).resolve().parent
        pex_script = script_dir / "run_pex.sh"
        
        if not pex_script.exists():
            raise FileNotFoundError(f"run_pex.sh not found at {pex_script}")
        
        # Run the PEX extraction script 
        subprocess.run(["bash", str(pex_script), layout_path, component_name], 
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
