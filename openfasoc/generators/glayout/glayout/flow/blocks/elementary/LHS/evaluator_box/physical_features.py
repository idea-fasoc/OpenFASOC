# physical_features.py
import os
import re
import subprocess
import shutil
from pathlib import Path
from gdsfactory.typings import Component
from gdsfactory.geometry.boolean import boolean

def calculate_area(component: Component) -> float:
    """Calculates the area of a gdsfactory Component."""
    return float(component.area())

def _mirror_and_xor(component: Component, axis: str) -> float:
    """Helper to perform mirroring and XOR for symmetry calculation."""
    # --- Operate on a copy to prevent modifying the original ---
    comp_copy = component.copy()
    comp_copy.unlock()
    
    mirrored_ref = comp_copy.copy() 
    if axis == 'vertical':
        mirrored_ref = mirrored_ref.mirror((0, -100), (0, 100))
    elif axis == 'horizontal':
        mirrored_ref = mirrored_ref.mirror((-100, 0), (100, 0))
    else:
        return 0.0
    
    # Pass the copies to the boolean operation
    asymmetry_layout = boolean(A=comp_copy, B=mirrored_ref, operation="xor")
    return float(asymmetry_layout.area())

def calculate_symmetry_scores(component: Component) -> tuple[float, float]:
    """Calculates horizontal and vertical symmetry scores (1.0 = perfect symmetry)."""
    original_area = calculate_area(component)
    if original_area == 0:
        return (1.0, 1.0)
        
    asymmetry_y_area = _mirror_and_xor(component, 'horizontal')
    asymmetry_x_area = _mirror_and_xor(component, 'vertical')
    
    symmetry_score_horizontal = 1.0 - (asymmetry_x_area / original_area)
    symmetry_score_vertical = 1.0 - (asymmetry_y_area / original_area)
    return symmetry_score_horizontal, symmetry_score_vertical

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

def run_physical_feature_extraction(layout_path: str, component_name: str, top_level: Component) -> dict:
    """
    Runs PEX and calculates geometric features, returning a structured result.
    """
    physical_results = {
        "pex": {"status": "not run", "total_resistance_ohms": 0.0, "total_capacitance_farads": 0.0},
        "geometric": {"raw_area_um2": 0.0, "symmetry_score_horizontal": 0.0, "symmetry_score_vertical": 0.0}
    }
    
    # PEX and Parasitics
    try:
        pex_spice_path = f"{component_name}_pex.spice"
        if os.path.exists(pex_spice_path):
            os.remove(pex_spice_path)
        subprocess.run(["./run_pex.sh", layout_path, component_name], check=True, capture_output=True, text=True)
        physical_results["pex"]["status"] = "PEX Complete"
        total_res, total_cap = _parse_simple_parasitics(component_name)
        physical_results["pex"]["total_resistance_ohms"] = total_res
        physical_results["pex"]["total_capacitance_farads"] = total_cap
    except subprocess.CalledProcessError as e:
        physical_results["pex"]["status"] = f"PEX Error: {e.stderr}"
    except FileNotFoundError:
        physical_results["pex"]["status"] = "PEX Error: run_pex.sh not found."
    except Exception as e:
        physical_results["pex"]["status"] = f"PEX Unexpected Error: {e}"
        
    # Geometric Features
    try:
        physical_results["geometric"]["raw_area_um2"] = calculate_area(top_level)
        sym_h, sym_v = calculate_symmetry_scores(top_level)
        physical_results["geometric"]["symmetry_score_horizontal"] = sym_h
        physical_results["geometric"]["symmetry_score_vertical"] = sym_v
    except Exception as e:
        print(f"Warning: Could not calculate geometric features. Error: {e}")

    return physical_results 