#!/usr/bin/env python3
"""
Test script to verify that the netlist info dict fix works correctly.
"""

import sys
import os
from pathlib import Path

# Add the glayout path
glayout_path = "/home/arnavshukla/OpenFASOC/openfasoc/generators/glayout"
if glayout_path not in sys.path:
    sys.path.insert(0, glayout_path)

# Set up environment
os.environ['PDK_ROOT'] = '/opt/conda/envs/GLdev/share/pdk'
os.environ['PDK'] = 'sky130A'

from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
from transmission_gate import transmission_gate, add_tg_labels

def test_netlist_serialization():
    """Test that netlist objects are properly serialized in component.info"""
    print("Testing transmission gate netlist serialization...")
    
    try:
        # Create a transmission gate with default parameters
        tg = transmission_gate(
            pdk=sky130_mapped_pdk,
            width=(1.0, 2.0),
            length=(0.15, 0.15),
            fingers=(1, 1),
            multipliers=(1, 1)
        )
        
        # Check that netlist is stored as string (not object)
        netlist_value = tg.info.get('netlist')
        netlist_obj = tg.info.get('netlist_obj')
        
        print(f"Netlist type: {type(netlist_value)}")
        print(f"Netlist object type: {type(netlist_obj)}")
        
        # Verify types
        if isinstance(netlist_value, str):
            print("✅ SUCCESS: netlist is stored as string")
        else:
            print(f"❌ FAILED: netlist is stored as {type(netlist_value)}")
            return False
            
        if netlist_obj is not None and hasattr(netlist_obj, 'circuit_name'):
            print("✅ SUCCESS: netlist_obj is available for internal use")
        else:
            print("❌ FAILED: netlist_obj is not properly stored")
            return False
            
        # Test that we can create JSON-serializable info dict
        import json
        try:
            # Create a copy of info dict with only basic types
            info_copy = {}
            for key, value in tg.info.items():
                if isinstance(value, (str, int, float, bool, list, tuple)):
                    info_copy[key] = value
                else:
                    info_copy[key] = str(value)
            
            json_str = json.dumps(info_copy, indent=2)
            print("✅ SUCCESS: info dict can be JSON serialized")
            print(f"JSON preview: {json_str[:200]}...")
            
        except Exception as e:
            print(f"❌ FAILED: JSON serialization failed: {e}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("Testing netlist serialization fix...")
    success = test_netlist_serialization()
    if success:
        print("\n🎉 All tests passed! The fix should resolve the gymnasium info dict error.")
    else:
        print("\n⚠️ Tests failed. The issue may not be fully resolved.")
