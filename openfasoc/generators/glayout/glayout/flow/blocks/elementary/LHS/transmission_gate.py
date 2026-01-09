import sys
import os
import json
import glayout
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory import Component
from glayout.flow.primitives.fet import nmos, pmos, multiplier
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, prec_center, align_comp_to_port, movex, movey
from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid
from glayout.flow.pdk.util.port_utils import rename_ports_by_orientation
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.primitives.guardring import tapring
from glayout.flow.pdk.util.port_utils import add_ports_perimeter
from glayout.flow.spice.netlist import Netlist
from glayout.flow.primitives.via_gen import via_stack
from gdsfactory.components import text_freetype, rectangle
try:
    from evaluator_wrapper import run_evaluation # pyright: ignore[reportMissingImports]
except ImportError:
    print("Warning: evaluator_wrapper not found. Evaluation will be skipped.")
    run_evaluation = None

def reconstruct_netlist_from_component(component, comp_name):
    """Helper to safely extract and reconstruct netlist from component"""
    try:
        netlist = component.info.get('netlist', None)
        
        if isinstance(netlist, Netlist):
            return netlist
        
        if isinstance(netlist, str):
            netlist_data_json = component.info.get('netlist_data_json', None)
            
            if netlist_data_json:
                try:
                    data = json.loads(netlist_data_json)
                    reconstructed = Netlist(
                        circuit_name=data.get('circuit_name', 'unknown'),
                        nodes=data.get('nodes', ['D', 'G', 'S', 'B'])
                    )
                    reconstructed.source_netlist = data.get('source_netlist', '')
                    if 'parameters' in data:
                        reconstructed.parameters = data['parameters']
                    return reconstructed
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Debug: JSON decode failed for {comp_name}: {e}")
            
            netlist_data = component.info.get('netlist_data', None)
            if netlist_data and isinstance(netlist_data, dict):
                try:
                    reconstructed = Netlist(
                        circuit_name=netlist_data.get('circuit_name', 'unknown'),
                        nodes=netlist_data.get('nodes', ['D', 'G', 'S', 'B'])
                    )
                    reconstructed.source_netlist = netlist_data.get('source_netlist', '')
                    if 'parameters' in netlist_data:
                        reconstructed.parameters = netlist_data['parameters']
                    return reconstructed
                except (KeyError, TypeError) as e:
                    print(f"Debug: netlist_data parse failed for {comp_name}: {e}")
            
            raise ValueError(f"No netlist_data found for string netlist in {comp_name} component")
        
        raise ValueError(f"Invalid netlist for {comp_name}")
        
    except Exception as e:
        print(f"Error reconstructing netlist for {comp_name}: {e}")
        raise

def add_tg_labels(tg_in: Component,
                        pdk: MappedPDK
                        ) -> Component:
	
    tg_in.unlock()
    met2_pin = (68,16)
    met2_label = (68,5)
    # list that will contain all port/comp info
    move_info = list()
    # create labels and append to info list
    # vin
    vinlabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.27,0.27),centered=True).copy()
    vinlabel.add_label(text="VIN",layer=pdk.get_glayer("met2_label"))
    move_info.append((vinlabel,tg_in.ports["N_multiplier_0_source_E"],None))
    
    # vout
    voutlabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.27,0.27),centered=True).copy()
    voutlabel.add_label(text="VOUT",layer=pdk.get_glayer("met2_label"))
    move_info.append((voutlabel,tg_in.ports["P_multiplier_0_drain_W"],None))
    
    # vcc
    vcclabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.5,0.5),centered=True).copy()
    vcclabel.add_label(text="VCC",layer=pdk.get_glayer("met2_label"))
    move_info.append((vcclabel,tg_in.ports["P_tie_S_top_met_S"],None))
    
    # vss
    vsslabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.5,0.5),centered=True).copy()
    vsslabel.add_label(text="VSS",layer=pdk.get_glayer("met2_label"))
    move_info.append((vsslabel,tg_in.ports["N_tie_S_top_met_N"], None))
    
    # VGP
    vgplabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.27,0.27),centered=True).copy()
    vgplabel.add_label(text="VGP",layer=pdk.get_glayer("met2_label"))
    move_info.append((vgplabel,tg_in.ports["P_multiplier_0_gate_E"], None))
    
    # VGN
    vgnlabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.27,0.27),centered=True).copy()
    vgnlabel.add_label(text="VGN",layer=pdk.get_glayer("met2_label"))
    move_info.append((vgnlabel,tg_in.ports["N_multiplier_0_gate_E"], None))

    # move everything to position
    for comp, prt, alignment in move_info:
        alignment = ('c','b') if alignment is None else alignment
        compref = align_comp_to_port(comp, prt, alignment=alignment)
        tg_in.add(compref)
    return tg_in.flatten() 

def tg_netlist(nfet_comp: Component, pfet_comp: Component) -> Netlist:
    """Generate netlist for transmission gate using proper Netlist class
    
    Port names match the labels added by add_tg_labels:
    VIN (source), VOUT (drain), VGP (pmos gate), VGN (nmos gate), VCC (pwell/vdd), VSS (nwell/gnd)
    """
    tg_netlist_obj = Netlist(circuit_name='transmission_gate', nodes=['VIN', 'VOUT', 'VGP', 'VGN', 'VCC', 'VSS'])
    
    # Reconstruct netlists for both FETs
    nfet_netlist = reconstruct_netlist_from_component(nfet_comp, "nfet")
    pfet_netlist = reconstruct_netlist_from_component(pfet_comp, "pfet")
    
    # Connect NMOS: drain=VOUT, gate=VGN, source=VIN, bulk=VSS
    tg_netlist_obj.connect_netlist(
        nfet_netlist,
        [('D', 'VOUT'), ('G', 'VGN'), ('S', 'VIN'), ('B', 'VSS')]
    )
    
    # Connect PMOS: drain=VOUT, gate=VGP, source=VIN, bulk=VCC
    tg_netlist_obj.connect_netlist(
        pfet_netlist,
        [('D', 'VOUT'), ('G', 'VGP'), ('S', 'VIN'), ('B', 'VCC')]
    )
    
    return tg_netlist_obj

@cell
def transmission_gate(
        pdk: MappedPDK,
        width: tuple[float,float] = (10.0,1.82),
        length: tuple[float,float] = (1.57,1.75),
        fingers: tuple[int,int] = (2,4),
        multipliers: tuple[int,int] = (1,1),
        substrate_tap: bool = False,
        tie_layers: tuple[str,str] = ("met2","met1"),
        **kwargs
        ) -> Component:
    """
    creates a transmission gate
    tuples are in (NMOS,PMOS) order
    **kwargs are any kwarg that is supported by nmos and pmos
    """
   
    #top level component
    top_level = Component(name="transmission_gate")

    #two fets
    nfet = nmos(pdk, width=width[0], fingers=fingers[0], multipliers=multipliers[0], with_dummy=True, with_dnwell=False,  with_substrate_tap=False, length=length[0], **kwargs)
    pfet = pmos(pdk, width=width[1], fingers=fingers[1], multipliers=multipliers[1], with_dummy=True, with_substrate_tap=False, length=length[1], **kwargs)
    nfet_ref = top_level << nfet
    pfet_ref = top_level << pfet 
    pfet_ref = rename_ports_by_orientation(pfet_ref.mirror_y())

    #Relative move
    pfet_ref.movey(nfet_ref.ymax + evaluate_bbox(pfet_ref)[1]/2 + pdk.util_max_metal_seperation())
    
    #Routing
    top_level << c_route(pdk, nfet_ref.ports["multiplier_0_source_E"], pfet_ref.ports["multiplier_0_source_E"])
    top_level << c_route(pdk, nfet_ref.ports["multiplier_0_drain_W"], pfet_ref.ports["multiplier_0_drain_W"], viaoffset=False)
    
    #Renaming Ports
    top_level.add_ports(nfet_ref.get_ports_list(), prefix="N_")
    top_level.add_ports(pfet_ref.get_ports_list(), prefix="P_")

    #substrate tap
    if substrate_tap:
            substrate_tap_encloses =((evaluate_bbox(top_level)[0]+pdk.util_max_metal_seperation()), (evaluate_bbox(top_level)[1]+pdk.util_max_metal_seperation()))
            guardring_ref = top_level << tapring(
            pdk,
            enclosed_rectangle=substrate_tap_encloses,
            sdlayer="p+s/d",
            horizontal_glayer='met2',
            vertical_glayer='met1',
        )
            guardring_ref.move(nfet_ref.center).movey(evaluate_bbox(pfet_ref)[1]/2 + pdk.util_max_metal_seperation()/2)
            top_level.add_ports(guardring_ref.get_ports_list(),prefix="tap_")
    
    component = component_snap_to_grid(rename_ports_by_orientation(top_level)) 
    
    # Generate netlist using proper Netlist class
    tg_netlist_obj = tg_netlist(nfet, pfet)
    
    # Store Netlist object (mappedpdk.lvs_netgen expects object with generate_netlist method)
    component.info['netlist'] = tg_netlist_obj
    
    # Store netlist_data as JSON for reconstruction
    component.info['netlist_data_json'] = json.dumps({
        'circuit_name': tg_netlist_obj.circuit_name,
        'nodes': tg_netlist_obj.nodes,
        'source_netlist': tg_netlist_obj.source_netlist,
        'parameters': tg_netlist_obj.parameters if hasattr(tg_netlist_obj, 'parameters') else {}
    })

    return component

if __name__=="__main__":
    transmission_gate = add_tg_labels(transmission_gate(sky130_mapped_pdk),sky130_mapped_pdk)
    transmission_gate.show()
    transmission_gate.name = "Transmission_Gate"
    #magic_drc_result = sky130_mapped_pdk.drc_magic(transmission_gate, transmission_gate.name)
    #netgen_lvs_result = sky130_mapped_pdk.lvs_netgen(transmission_gate, transmission_gate.name)
    transmission_gate_gds = transmission_gate.write_gds("transmission_gate.gds")
    if run_evaluation is not None:
        res = run_evaluation("transmission_gate.gds", transmission_gate.name, transmission_gate)
    else:
        print("Skipping evaluation: evaluator_wrapper not available")
