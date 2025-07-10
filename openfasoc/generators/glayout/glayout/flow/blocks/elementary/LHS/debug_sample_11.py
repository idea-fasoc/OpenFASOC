#!/usr/bin/env python3
"""
Debug script for sample 11 that was hanging
"""

import sys
import time
import json
from pathlib import Path

# Add glayout to path
_here = Path(__file__).resolve()
_root_dir = _here.parent.parent.parent.parent.parent
sys.path.insert(0, str(_root_dir))

from glayout.flow.blocks.elementary.LHS.transmission_gate import transmission_gate, add_tg_labels
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk

def test_sample_11():
    """Test the specific parameters that are causing sample 11 to hang"""
    
    # Sample 11 parameters (index 10)
    params = {
        "width": [15.56987768790995, 19.431313875884364],
        "length": [2.2925198967864566, 0.8947369421533957],
        "fingers": [5, 5],
        "multipliers": [2, 2]
    }
    
    print("Testing sample 11 parameters:")
    print(f"Parameters: {params}")
    
    # Convert to tuples
    width_tuple = tuple(params['width'])
    length_tuple = tuple(params['length'])
    fingers_tuple = tuple(params['fingers'])
    multipliers_tuple = tuple(params['multipliers'])
    
    print(f"Width tuple: {width_tuple}")
    print(f"Length tuple: {length_tuple}")
    print(f"Fingers tuple: {fingers_tuple}")
    print(f"Multipliers tuple: {multipliers_tuple}")
    
    try:
        print("Creating transmission gate...")
        start_time = time.time()
        
        tg_component = transmission_gate(
            pdk=sky130_mapped_pdk,
            width=width_tuple,
            length=length_tuple,
            fingers=fingers_tuple,
            multipliers=multipliers_tuple,
            substrate_tap=True
        )
        
        creation_time = time.time() - start_time
        print(f"✅ Transmission gate created in {creation_time:.2f}s")
        
        print("Adding labels...")
        start_time = time.time()
        cell = add_tg_labels(tg_component, sky130_mapped_pdk)
        cell.name = "test_sample_11"
        label_time = time.time() - start_time
        print(f"✅ Labels added in {label_time:.2f}s")
        
        print("Writing GDS...")
        start_time = time.time()
        cell.write_gds("test_sample_11.gds")
        gds_time = time.time() - start_time
        print(f"✅ GDS written in {gds_time:.2f}s")
        
        print("🎉 Sample 11 test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_sample_11() 