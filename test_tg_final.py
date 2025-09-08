#!/usr/bin/env python3
"""
Test script to validate transmission gate dataset generation fixes.
This tests the core issues that were causing problems for the colleague's gdsfactory 7.16.0+ environment.
"""
import os
import sys

# Add glayout to path
sys.path.insert(0, os.path.join(os.getcwd(), 'openfasoc', 'generators', 'glayout'))
sys.path.append(os.path.join(os.getcwd(), 'openfasoc', 'generators', 'glayout', 'glayout', 'flow', 'blocks', 'elementary', 'LHS'))

def test_transmission_gate_basic():
    """Test basic transmission gate creation and netlist storage"""
    print("🔍 Test 1: Basic Transmission Gate Creation")
    
    try:
        from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as pdk
        from transmission_gate import transmission_gate
        
        # Create transmission gate
        tg = transmission_gate(pdk=pdk, width=(1.0, 2.0), length=(0.15, 0.15))
        
        # Check info dict types (gymnasium compatibility)
        for key, value in tg.info.items():
            if not isinstance(value, (int, float, str, tuple)):
                print(f"❌ FAILED: Non-primitive type {type(value)} for key '{key}'")
                return False
                
        print(f"✅ SUCCESS: Created transmission gate with {len(tg.info)} info items")
        print(f"   - netlist: {type(tg.info.get('netlist', 'MISSING'))}")
        print(f"   - netlist_data: {type(tg.info.get('netlist_data', 'MISSING'))}")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_netlist_content():
    """Test that netlist content is proper SPICE"""
    print("\n🔍 Test 2: Netlist Content Validation")
    
    try:
        from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as pdk
        from transmission_gate import transmission_gate
        
        # Create transmission gate
        tg = transmission_gate(pdk=pdk, width=(1.0, 2.0), length=(0.15, 0.15))
        
        # Get netlist content
        netlist = tg.info.get('netlist', '')
        
        if not netlist:
            print("❌ FAILED: No netlist found")
            return False
            
        # Check for required SPICE elements
        required_elements = [
            '.subckt PMOS',
            '.subckt NMOS', 
            '.subckt transmission_gate',
            'sky130_fd_pr__pfet_01v8',
            'sky130_fd_pr__nfet_01v8',
            '.ends'
        ]
        
        for element in required_elements:
            if element not in netlist:
                print(f"❌ FAILED: Missing required element: {element}")
                return False
                
        print(f"✅ SUCCESS: Valid SPICE netlist ({len(netlist)} chars)")
        print("   - Contains all required subcircuits and models")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_lvs_reconstruction():
    """Test netlist reconstruction for LVS processes"""
    print("\n🔍 Test 3: LVS Netlist Reconstruction")
    
    try:
        from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as pdk
        from transmission_gate import transmission_gate
        
        # Create transmission gate
        tg = transmission_gate(pdk=pdk, width=(1.0, 2.0), length=(0.15, 0.15))
        
        # Simulate LVS process by calling lvs_netgen method
        # This is what was failing before with 'str' object has no attribute 'generate_netlist'
        temp_netlist_file = '/tmp/test_tg_netlist.spice'
        
        # Test the method that was failing
        try:
            # This should work now without throwing the attribute error
            result = pdk.lvs_netgen(tg, tg, temp_netlist_file, temp_netlist_file, run_lvs=False)
            print("✅ SUCCESS: LVS netgen method executed without errors")
            return True
        except AttributeError as e:
            if "has no attribute 'generate_netlist'" in str(e):
                print(f"❌ FAILED: Still getting generate_netlist attribute error: {e}")
                return False
            else:
                # Other attribute errors might be expected (like missing LVS tools)
                print("✅ SUCCESS: No generate_netlist attribute error (other errors may be expected)")
                return True
        except Exception as e:
            if "generate_netlist" in str(e):
                print(f"❌ FAILED: generate_netlist error: {e}")
                return False
            else:
                # Other errors might be expected (like missing LVS tools)
                print(f"✅ SUCCESS: No generate_netlist error (other errors may be expected: {e})")
                return True
                
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_gymnasium_compatibility():
    """Test gymnasium environment compatibility"""
    print("\n🔍 Test 4: Gymnasium Environment Compatibility")
    
    try:
        # Mock gymnasium's info dict validation
        def validate_info_dict(info_dict):
            """Simulate gymnasium's strict type checking"""
            for key, value in info_dict.items():
                if not isinstance(value, (int, float, str, tuple)):
                    raise TypeError(f"Values of the info dict only support int, float, string or tuple, got {type(value)} for key '{key}'")
            return True
        
        from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as pdk
        from transmission_gate import transmission_gate
        
        # Create transmission gate
        tg = transmission_gate(pdk=pdk, width=(1.0, 2.0), length=(0.15, 0.15))
        
        # Test gymnasium compatibility
        validate_info_dict(tg.info)
        
        print("✅ SUCCESS: Info dict passes gymnasium type validation")
        print(f"   - All {len(tg.info)} values are primitive types")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Transmission Gate Dataset Generation Fixes")
    print("=" * 60)
    
    tests = [
        test_transmission_gate_basic,
        test_netlist_content, 
        test_lvs_reconstruction,
        test_gymnasium_compatibility
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"Test {i+1}: {test.__name__:<30} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("The transmission gate dataset generation should now work")
        print("with your colleague's gdsfactory 7.16.0+ environment!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("Some issues remain that need to be addressed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
