#!/usr/bin/env python3
"""
Debug script to investigate the netlist reconstruction issue.
"""

import sys
import os

# Add the glayout path
glayout_path = "/home/arnavshukla/OpenFASOC/openfasoc/generators/glayout"
if glayout_path not in sys.path:
    sys.path.insert(0, glayout_path)

# Set up environment
os.environ['PDK_ROOT'] = '/opt/conda/envs/GLdev/share/pdk'
os.environ['PDK'] = 'sky130A'

def debug_netlist_storage():
    """Debug what's actually being stored in component.info"""
    print("🔍 Debugging Netlist Storage...")
    
    from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
    from transmission_gate import transmission_gate
    
    pdk = sky130_mapped_pdk
    
    print("📋 Creating transmission gate...")
    tg = transmission_gate(pdk=pdk, width=(1.0, 2.0), length=(0.15, 0.15))
    
    print("\n📊 Component Info Contents:")
    print("Keys:", list(tg.info.keys()))
    
    for key, value in tg.info.items():
        print(f"\n{key}: {type(value)}")
        if isinstance(value, str):
            print(f"  Length: {len(value)}")
            print(f"  Preview: {value[:100]}...")
        elif isinstance(value, dict):
            print(f"  Dict keys: {list(value.keys())}")
            for k, v in value.items():
                print(f"    {k}: {type(v)} - {str(v)[:50]}...")
    
    # Test reconstruction
    print("\n🔧 Testing Reconstruction...")
    if 'netlist_data' in tg.info:
        from glayout.flow.spice.netlist import Netlist
        data = tg.info['netlist_data']
        print(f"Netlist data: {data}")
        
        try:
            netlist_obj = Netlist(
                circuit_name=data['circuit_name'],
                nodes=data['nodes']
            )
            netlist_obj.source_netlist = data['source_netlist']
            
            print(f"Reconstructed netlist object: {netlist_obj}")
            print(f"Circuit name: {netlist_obj.circuit_name}")
            print(f"Nodes: {netlist_obj.nodes}")
            print(f"Source netlist: {netlist_obj.source_netlist}")
            
            generated = netlist_obj.generate_netlist()
            print(f"Generated netlist length: {len(generated)}")
            print(f"Generated content:\n{generated}")
            
        except Exception as e:
            print(f"Error reconstructing: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_netlist_storage()
