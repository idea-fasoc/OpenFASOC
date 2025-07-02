# verification.py
import os
import re
import subprocess
import shutil
import tempfile
import sys
from pathlib import Path
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
from gdsfactory.typings import Component

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
    Focuses on parsing net and instance mismatches.
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

def run_verification(layout_path: str, component_name: str, top_level: Component) -> dict:
    """
    Runs DRC and LVS checks and returns a structured result dictionary.
    """
    verification_results = {
        "drc": {"status": "not run", "is_pass": False, "report_path": None, "summary": {}},
        "lvs": {"status": "not run", "is_pass": False, "report_path": None, "summary": {}}
    }
    
    # DRC Check
    drc_report_path = os.path.abspath(f"./{component_name}.drc.rpt")
    verification_results["drc"]["report_path"] = drc_report_path
    try:
        if os.path.exists(drc_report_path):
            os.remove(drc_report_path)
        sky130_mapped_pdk.drc_magic(layout_path, component_name, output_file=drc_report_path)
        report_content = ""
        if os.path.exists(drc_report_path):
            with open(drc_report_path, 'r') as f:
                report_content = f.read()
        summary = parse_drc_report(report_content)
        verification_results["drc"].update({"summary": summary, "is_pass": summary["is_pass"], "status": "pass" if summary["is_pass"] else "fail"})
    except Exception as e:
        verification_results["drc"]["status"] = f"error: {e}"

    # LVS Check
    lvs_report_path = os.path.abspath(f"./{component_name}.lvs.rpt")
    verification_results["lvs"]["report_path"] = lvs_report_path
    try:
        if os.path.exists(lvs_report_path):
            os.remove(lvs_report_path)
        sky130_mapped_pdk.lvs_netgen(layout=top_level, design_name=component_name, output_file_path=lvs_report_path)
        report_content = ""
        if os.path.exists(lvs_report_path):
            with open(lvs_report_path, 'r') as report_file:
                report_content = report_file.read()
        lvs_summary = parse_lvs_report(report_content)
        verification_results["lvs"].update({"summary": lvs_summary, "is_pass": lvs_summary["is_pass"], "status": "pass" if lvs_summary["is_pass"] else "fail"})
    except Exception as e:
        verification_results["lvs"]["status"] = f"error: {e}"
        
    return verification_results