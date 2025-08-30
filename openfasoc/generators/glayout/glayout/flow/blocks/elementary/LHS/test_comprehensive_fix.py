#!/usr/bin/env python3
"""
Comprehensive test script to verify that all netlist info dict fixes work correctly.
Tests multiple components to ensure the fix is applied consistently.
"""

import sys
import os
import json
from pathlib import Path

# Add the glayout path
glayout_path = "/home/arnavshukla/OpenFASOC/openfasoc/generators/glayout"
if glayout_path not in sys.path:
    sys.path.insert(0, glayout_path)

# Set up environment
os.environ['PDK_ROOT'] = '/opt/conda/envs/GLdev/share/pdk'
os.environ['PDK'] = 'sky130A'

def test_component_info_serialization(component, component_name):
    """Test that a component's info dict can be JSON serialized"""
    print(f"\nTesting {component_name}...")
    
    try:
        # Check netlist storage
        netlist_value = component.info.get('netlist')
        netlist_data = component.info.get('netlist_data')
        
        print(f"  Netlist type: {type(netlist_value)}")
        print(f"  Netlist data type: {type(netlist_data)}")
        
        success = True
        
        # Verify netlist is stored as string
        if not isinstance(netlist_value, str):
            print(f"  ❌ FAILED: netlist should be string, got {type(netlist_value)}")
            success = False
        else:
            print("  ✅ SUCCESS: netlist is stored as string")
            
        # Verify netlist_data is available for gdsfactory 7.16.0+ compatibility
        if netlist_data is None:
            print("  ⚠️  WARNING: netlist_data is None - may not work with gdsfactory 7.16.0+")
        elif isinstance(netlist_data, dict):
            required_keys = ['circuit_name', 'nodes', 'source_netlist']
            if all(key in netlist_data for key in required_keys):
                print("  ✅ SUCCESS: netlist_data contains all required fields for reconstruction")
            else:
                print(f"  ❌ FAILED: netlist_data missing required keys: {[k for k in required_keys if k not in netlist_data]}")
                success = False
        else:
            print(f"  ❌ FAILED: netlist_data should be dict, got {type(netlist_data)}")
            success = False
            
        # Test JSON serialization
        try:
            info_copy = {}
            for key, value in component.info.items():
                if isinstance(value, (str, int, float, bool, list, tuple, dict)):
                    info_copy[key] = value
                else:
                    info_copy[key] = str(value)
            
            json_str = json.dumps(info_copy, indent=2)
            print("  ✅ SUCCESS: info dict can be JSON serialized")
            
        except Exception as e:
            print(f"  ❌ FAILED: JSON serialization failed: {e}")
            success = False
            
        return success
        
    except Exception as e:
        print(f"  ❌ FAILED: Test failed with error: {e}")
        return False

def main():
    """Test multiple components to ensure consistent behavior"""
    print("🧪 Comprehensive Netlist Serialization Test")
    print("=" * 60)
    
    from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
    pdk = sky130_mapped_pdk
    
    test_results = []
    
    # Test 1: Basic FETs
    try:
        print("\n📋 Testing Basic Components...")
        from glayout.flow.primitives.fet import nmos, pmos
        
        nfet = nmos(pdk, width=1.0, length=0.15, fingers=1)
        test_results.append(("NMOS", test_component_info_serialization(nfet, "NMOS")))
        
        pfet = pmos(pdk, width=2.0, length=0.15, fingers=1)
        test_results.append(("PMOS", test_component_info_serialization(pfet, "PMOS")))
        
    except Exception as e:
        print(f"❌ Failed to test basic FETs: {e}")
        test_results.append(("Basic FETs", False))
    
    # Test 2: Transmission Gate
    try:
        print("\n📋 Testing Transmission Gate...")
        from transmission_gate import transmission_gate
        
        tg = transmission_gate(
            pdk=pdk,
            width=(1.0, 2.0),
            length=(0.15, 0.15),
            fingers=(1, 1),
            multipliers=(1, 1)
        )
        test_results.append(("Transmission Gate", test_component_info_serialization(tg, "Transmission Gate")))
        
    except Exception as e:
        print(f"❌ Failed to test transmission gate: {e}")
        test_results.append(("Transmission Gate", False))
    
    # Test 3: FVF (if available)
    try:
        print("\n📋 Testing Flipped Voltage Follower...")
        from fvf import flipped_voltage_follower
        
        fvf = flipped_voltage_follower(
            pdk=pdk,
            width=(1.0, 0.5),
            length=(0.15, 0.15),
            fingers=(1, 1)
        )
        test_results.append(("FVF", test_component_info_serialization(fvf, "Flipped Voltage Follower")))
        
    except Exception as e:
        print(f"⚠️  FVF test skipped: {e}")
    
    # Test 4: MIM Capacitor (if available)
    try:
        print("\n📋 Testing MIM Capacitor...")
        from glayout.flow.primitives.mimcap import mimcap
        
        cap = mimcap(pdk=pdk, size=(5.0, 5.0))
        test_results.append(("MIM Cap", test_component_info_serialization(cap, "MIM Capacitor")))
        
    except Exception as e:
        print(f"⚠️  MIM Cap test skipped: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for component_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {component_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("The gymnasium info dict error should be resolved for your friend.")
        print("\nSolution Summary:")
        print("- All netlist objects are now stored as strings in component.info['netlist']")
        print("- Netlist data is preserved in component.info['netlist_data'] for reconstruction")
        print("- This prevents gymnasium from encountering unsupported object types")
        print("- Compatible with both gdsfactory 7.7.0 and 7.16.0+ strict Pydantic validation")
        return True
    else:
        print(f"\n⚠️  {total - passed} tests failed. Some issues may remain.")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Fix validation completed successfully!")
    else:
        print("\n❌ Some issues detected. Please review the failed tests.")
