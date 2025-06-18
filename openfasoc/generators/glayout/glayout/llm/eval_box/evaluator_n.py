import subprocess
import re
import os
import logging
import json
from datetime import datetime
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
from gdsfactory.typings import Component
from gdsfactory.geometry.boolean import boolean

# Helper function to get the next available log filename
def get_next_log_filename(base_name="evaluation", extension=".log"):
    """
    Generates the next available log filename with a numerical suffix.
    E.g., evaluation.log, evaluation_1.log, evaluation_2.log, etc.
    """
    filename = f"{base_name}{extension}"
    if not os.path.exists(filename):
        return filename

    i = 1
    while True:
        filename = f"{base_name}_{i}{extension}"
        if not os.path.exists(filename):
            return filename
        i += 1

# --- Point 5: Evaluation Log Export (Setup) ---
# Configure a logger to output structured JSON to a file
# This setup is done once when the module is loaded.
log_file_name = get_next_log_filename() # Get a unique filename for this run
log_file_handler = logging.FileHandler(log_file_name)

# Modified JsonFormatter to directly dump the message if it's a dictionary
class JsonFormatter(logging.Formatter):
    def format(self, record):
        # Directly dump the message if it's a dictionary (our log_entry)
        if isinstance(record.msg, dict):
            return json.dumps(record.msg)
        # Otherwise, format as a regular message
        return super().format(record)

log_file_handler.setFormatter(JsonFormatter())
logger = logging.getLogger(__name__)
logger.addHandler(log_file_handler)
logger.setLevel(logging.INFO)
# ---
# New function: Calculate Area
def calculate_area(component: Component) -> float:
    """
    Calculates the area of a gdsfactory Component.
    """
    area = float(component.area())
    return area

def mirror_vertical(component: Component) -> float:
    component.unlock()
    mirrored_ref = component.copy()
    mirrored_ref = mirrored_ref.mirror((0,-100),(0,100))
    asymmetry_layout = boolean(A=component, B=mirrored_ref, operation="xor")
    asymmetry_area = float(asymmetry_layout.area())
    return asymmetry_area

def mirror_horizontal(component: Component) -> float:
    component.unlock()
    mirrored_ref = component.copy()
    mirrored_ref = mirrored_ref.mirror((-100,0),(100,0))
    asymmetry_layout = boolean(A=component, B=mirrored_ref, operation="xor")
    asymmetry_area = float(asymmetry_layout.area())
    return asymmetry_area

# New function: Calculate Symmetry Score
def calculate_symmetry_score(original_area: float, assymetry_x_area: float, assymetry_y_area:float) -> tuple[float,float]:
    """
    Calculates the symmetry score based on XORing the original and mirrored layouts.
    Assumes mirrored_layout is already correctly mirrored relative to the desired axis.
    A score of 1.0 indicates perfect symmetry, 0.0 indicates complete asymmetry.
    """
    symmetry_score_horizontal = 1.0 - (assymetry_y_area / original_area)
    symmetry_score_vertical = 1.0 - (assymetry_x_area / original_area)

    return symmetry_score_horizontal, symmetry_score_vertical 


def parse_parasitics(component_name: str) -> tuple[float, float]:
    """
    Parses parasitic R and C from the given SPICE file.
    Returns: (total_resistance_in_ohms, total_capacitance_in_farads)
    """
    total_resistance = 0.0
    total_capacitance = 0.0
    spice_file_path = f"{component_name}_pex.spice"
    if not os.path.exists(spice_file_path):
        return 0.0, 0.0
    with open(spice_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('R'):
                parts = line.split()
                try:
                    total_resistance += float(parts[3])
                except (IndexError, ValueError):
                    continue
            elif line.startswith('C'):
                parts = line.split()
                try:
                    cap_str = parts[3]
                    # Handle unit suffixes (f, p, n, u)
                    unit = cap_str[-1].lower()
                    if unit == 'f':
                        cap_value = float(cap_str[:-1]) * 1e-15
                    elif unit == 'p':
                        cap_value = float(cap_str[:-1]) * 1e-12
                    elif unit == 'n':
                        cap_value = float(cap_str[:-1]) * 1e-9
                    elif unit == 'u':
                        cap_value = float(cap_str[:-1]) * 1e-6
                    else:
                        cap_value = float(cap_str)
                    total_capacitance += cap_value
                except (IndexError, ValueError):
                    continue
    return total_resistance, total_capacitance

def parse_drc_report(report_content: str) -> dict:
    """
    Parses a Magic DRC report into a machine-readable format.
    Each line starting with an alphabet is considered a rule.
    Each line starting with a number (after a rule) is considered a detail,
    and contributes to the total error count.
    """
    errors = []
    current_rule = ""

    for line in report_content.strip().splitlines():
        stripped_line = line.strip()

        if stripped_line == "----------------------------------------":
            continue  # Ignore dashed lines

        # If the line starts with an alphabet, it's a new rule
        if re.match(r"^[a-zA-Z]", stripped_line):
            current_rule = stripped_line
        # If the line starts with a number, it's a detail for the current rule
        elif re.match(r"^[0-9]", stripped_line):
            errors.append({"rule": current_rule, "details": stripped_line})
        # Optionally, handle other types of lines if they should be ignored or processed differently
        # For now, lines that are not dashed, don't start with alphabet or number are implicitly ignored

    is_pass = len(errors) == 0
    # Add a fallback check for "0 errors" in the report content, just in case
    # the parsing logic misses something for reports with no errors at all.
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
    Focuses on parsing net and instance mismatches.
    """
    summary = {
        "is_pass": False,
        "conclusion": "LVS failed or report was inconclusive.",
        "total_mismatches": 0,
        "mismatch_details": {
            "nets": "Not found", # Kept for backward compatibility if needed, though replaced by parsed_unmatched_nets
            "devices": "Not found", # Kept for backward compatibility if needed, though replaced by parsed_unmatched_instances
            "unmatched_nets_parsed": [],
            "unmatched_instances_parsed": []
        }
    }
    
    # Primary check for LVS pass/fail
    if "Netlists match" in report_content or "Circuits match uniquely" in report_content:
        summary["is_pass"] = True
        summary["conclusion"] = "LVS Pass: Netlists match."
    elif "Netlist mismatch" in report_content or "Netlists do not match" in report_content:
        summary["conclusion"] = "LVS Fail: Netlist mismatch."

    for line in report_content.splitlines():
        line = line.strip()

        # Parse net mismatches
        net_mismatch_match = re.search(r"Net:\s*([^\|]+)\s*\|\s*\((no matching net)\)", line)
        if net_mismatch_match:
            name_left = net_mismatch_match.group(1).strip()
            # If name is on the left, it's in layout, missing in schematic
            summary["mismatch_details"]["unmatched_nets_parsed"].append({
                "type": "net",
                "name": name_left,
                "present_in": "layout",
                "missing_in": "schematic"
            })
            continue

        # Parse instance mismatches
        instance_mismatch_match = re.search(r"Instance:\s*([^\|]+)\s*\|\s*\((no matching instance)\)", line)
        if instance_mismatch_match:
            name_left = instance_mismatch_match.group(1).strip()
            # If name is on the left, it's in layout, missing in schematic
            summary["mismatch_details"]["unmatched_instances_parsed"].append({
                "type": "instance",
                "name": name_left,
                "present_in": "layout",
                "missing_in": "schematic"
            })
            continue

        # Also capture cases where something is present in schematic but missing in layout (right side of '|')
        net_mismatch_right_match = re.search(r"\s*\|\s*([^\|]+)\s*\((no matching net)\)", line)
        if net_mismatch_right_match:
            name_right = net_mismatch_right_match.group(1).strip()
            # If name is on the right, it's in schematic, missing in layout
            summary["mismatch_details"]["unmatched_nets_parsed"].append({
                "type": "net",
                "name": name_right,
                "present_in": "schematic",
                "missing_in": "layout"
            })
            continue

        instance_mismatch_right_match = re.search(r"\s*\|\s*([^\|]+)\s*\((no matching instance)\)", line)
        if instance_mismatch_right_match:
            name_right = instance_mismatch_right_match.group(1).strip()
            # If name is on the right, it's in schematic, missing in layout
            summary["mismatch_details"]["unmatched_instances_parsed"].append({
                "type": "instance",
                "name": name_right,
                "present_in": "schematic",
                "missing_in": "layout"
            })
            continue

        # Capture summary lines like "Number of devices:" and "Number of nets:"
        if "Number of devices:" in line:
            summary["mismatch_details"]["devices"] = line.split(":", 1)[1].strip() if ":" in line else line
        elif "Number of nets:" in line:
            summary["mismatch_details"]["nets"] = line.split(":", 1)[1].strip() if ":" in line else line

    # Calculate total mismatches
    summary["total_mismatches"] = len(summary["mismatch_details"]["unmatched_nets_parsed"]) + \
                                  len(summary["mismatch_details"]["unmatched_instances_parsed"])

    # If there are any mismatches found, then LVS fails, regardless of "Netlists match" string.
    if summary["total_mismatches"] > 0:
        summary["is_pass"] = False
        if "LVS Pass" in summary["conclusion"]: # If conclusion still says pass, update it
            summary["conclusion"] = "LVS Fail: Mismatches found."

    return summary

def evaluator(layout_path: str, component_name: str, top_level: Component) -> dict:
    """
    Deletes old reports, runs DRC, LVS, and PEX, and provides structured summaries.
    This function now logs its results and returns a structured, JSON-serializable dictionary.
    
    Returns: A dictionary with DRC/LVS/PEX status and detailed summaries.
    """
    # --- Point 1 & 3: Structured result dictionary and fail-fast prep ---
    results = {
        "component_name": component_name,
        "drc_lvs_fail": True, # Default to fail; set to False on success
        "drc": {
            "status": "not run",
            "is_pass": False,
            "report_path": None,
            "summary": {}
        },
        "lvs": {
            "status": "not run",
            "is_pass": False,
            "report_path": None,
            "summary": {}
        },
        "pex": {
            "status": "not run",
            "total_resistance_ohms": 0.0,
            "total_capacitance_farads": 0.0
        },
        "geometric_features": {
            "raw_area_um2": calculate_area(top_level), # Using the new function
            "symmetry_score": calculate_symmetry_score(calculate_area(top_level), mirror_horizontal(top_level), mirror_vertical(top_level))
        }
    }

    # DRC Check
    drc_report_path = os.path.abspath(f"./{component_name}.drc.rpt")
    results["drc"]["report_path"] = drc_report_path
    try:
        if os.path.exists(drc_report_path):
            os.remove(drc_report_path)

        sky130_mapped_pdk.drc_magic(layout_path, component_name, output_file=drc_report_path)

        report_content = ""
        if os.path.exists(drc_report_path):
            with open(drc_report_path, 'r') as f:
                report_content = f.read()

        summary = parse_drc_report(report_content)
        results["drc"]["summary"] = summary
        results["drc"]["is_pass"] = summary["is_pass"]
        results["drc"]["status"] = "pass" if summary["is_pass"] else "fail"
    except Exception as e:
        results["drc"]["status"] = f"error: {e}"
        results["drc"]["summary"] = {"is_pass": False, "total_errors": "Unknown", "error_details": [f"DRC tool failed to run: {e}"]}

    # LVS Check
    lvs_report_path = os.path.abspath(f"./{component_name}.lvs.rpt")
    results["lvs"]["report_path"] = lvs_report_path
    try:
        if os.path.exists(lvs_report_path):
            os.remove(lvs_report_path)

        # The boolean return from the tool can sometimes be unreliable; we parse the report instead.
        sky130_mapped_pdk.lvs_netgen(layout=top_level, design_name=component_name, output_file_path=lvs_report_path)
        
        report_content = ""
        if os.path.exists(lvs_report_path):
            with open(lvs_report_path, 'r') as report_file:
                report_content = report_file.read()
        
        lvs_summary = parse_lvs_report(report_content)
        results["lvs"]["summary"] = lvs_summary
        results["lvs"]["is_pass"] = lvs_summary["is_pass"]
        results["lvs"]["status"] = "pass" if lvs_summary["is_pass"] else "fail"
    except Exception as e:
        results["lvs"]["status"] = f"error: {e}"
        results["lvs"]["summary"] = {"is_pass": False, "conclusion": f"LVS tool failed to run: {e}", "total_mismatches": 0, "mismatch_details": {"unmatched_nets_parsed": [], "unmatched_instances_parsed": []}}

    # PEX and Parasitics
    try:
        pex_spice_path = f"{component_name}_pex.spice"
        if os.path.exists(pex_spice_path):
            os.remove(pex_spice_path)
        # Assuming run_pex.sh is an executable script in the current directory
        subprocess.run(["./run_pex.sh", layout_path, component_name], check=True, capture_output=True)
        results["pex"]["status"] = "PEX Complete"
        total_res, total_cap = parse_parasitics(component_name)
        results["pex"]["total_resistance_ohms"] = total_res
        results["pex"]["total_capacitance_farads"] = total_cap
    except subprocess.CalledProcessError as e:
        results["pex"]["status"] = f"PEX Error: {e.stderr.decode()}"
    except FileNotFoundError:
         results["pex"]["status"] = "PEX Error: run_pex.sh not found or spice file was not generated."
    except Exception as e:
        results["pex"]["status"] = f"PEX Error: {e}"


    # --- Point 3: Set Fail-Fast Indicator ---
    results["drc_lvs_fail"] = not (results["drc"]["is_pass"] and results["lvs"]["is_pass"])

    # --- Point 5: Log the entire evaluation result ---
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "evaluation_metrics": results
    }
    logger.info(log_entry)

    # --- Point 6: Backward compatibility is maintained by returning a dictionary ---
    # The structure is enhanced, but it's an additive change.
    return results
