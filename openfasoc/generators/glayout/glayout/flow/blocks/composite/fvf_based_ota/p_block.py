from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.component_reference import ComponentReference
from gdsfactory import Component
from glayout.flow.primitives.fet import nmos, pmos, multiplier
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, prec_center, prec_ref_center
from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid
from glayout.flow.pdk.util.port_utils import rename_ports_by_orientation
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.primitives.guardring import tapring
from glayout.flow.pdk.util.port_utils import add_ports_perimeter, rename_ports_by_list
from glayout.flow.spice.netlist import Netlist
from glayout.flow.primitives.via_gen import via_stack
from gdsfactory.components import text_freetype, rectangle
from glayout.flow.placement.four_transistor_interdigitized import generic_4T_interdigitzed

def p_block_netlist(pdk: MappedPDK, pblock: tuple[float, float, int]) -> Netlist:
    return Netlist(
        circuit_name="p_block",
        nodes=['MA_1_D', 'MA_2_D', 'MA_G', 'MB_1_D', 'MB_2_D', 'VDD'],
        source_netlist=""".subckt {circuit_name} {nodes} """ + f'l={pblock[1]} wb={pblock[0]} wt={pblock[0] * pblock[2]} ' + """
XTOP1 MB_1_D MA_1_D VDD VDD {model} l={{l}} w={{wt}} 
XTOP2 MB_2_D MA_2_D VDD VDD {model} l={{l}} w={{wt}} 
XBOT1 MA_1_D MA_G VDD VDD {model} l={{l}} w={{wb}} 
XBOT2 MA_2_D MA_G VDD VDD {model} l={{l}} w={{wb}} 
.ends {circuit_name}""",
        instance_format="X{name} {nodes} {circuit_name} l={length} wt={width_top} wb={width_bot}",
        parameters={
            'model': pdk.models['pfet'],
            'width_top': pblock[0] * pblock[2],
            'width_bot': pblock[0],
            'length': pblock[1],
        }
    )


@cell
def  p_block(
        pdk: MappedPDK,
        width: float = 4.5,
        length: float = 1,
        fingers: int = 1,
        ratio: int = 1,
        ) -> Component:
    """
    p_block for super class AB OTA

    """
    #top level component
    top_level = Component(name="p_block")
    top_kwargs = {
            "fingers": ratio*fingers,
            "width": width,
            "with_tie": True,
            "sd_rmult":3
            }
    bottom_kwargs = {
            "fingers": fingers,
            "width": width,
            "with_tie": True,
            "sd_rmult":3
            }

    p_block = generic_4T_interdigitzed(pdk, top_row_device = "pfet", bottom_row_device = "pfet", numcols = 2, length = length, with_substrate_tap = False, top_kwargs = top_kwargs, bottom_kwargs = bottom_kwargs)
    p_block_ref = top_level << p_block

    top_level << c_route(pdk, p_block.ports["top_A_0_gate_W"], p_block.ports["bottom_A_0_drain_W"])
    top_level << c_route(pdk, p_block.ports["top_B_1_gate_E"], p_block.ports["bottom_B_1_drain_E"])
    top_level << c_route(pdk, p_block.ports["bottom_A_0_gate_W"], p_block.ports["bottom_B_0_gate_W"], width1=0.29, width2=0.29, cwidth=0.29)
    
    top_level << c_route(pdk, p_block.ports["top_A_0_source_W"], p_block.ports["top_B_0_source_W"])
    top_level << straight_route(pdk, p_block.ports["top_A_0_source_W"], p_block.ports["top_welltie_W_top_met_W"], glayer1='met1', width=0.6)
    top_level << c_route(pdk, p_block.ports["bottom_A_0_source_W"], p_block.ports["bottom_B_0_source_W"], extension=1.2, cwidth=0.29)
    top_level << straight_route(pdk, p_block.ports["bottom_A_0_source_W"], p_block.ports["bottom_welltie_W_top_met_W"], glayer1='met1', width=0.6)
    
    top_level << straight_route(pdk, p_block.ports["top_welltie_S_top_met_S"], p_block.ports["bottom_welltie_N_top_met_N"], glayer1='met2', width=3)
    
    #adding a nwell    
    nwell_rectangle = rectangle(layer=(pdk.get_glayer("nwell")), size=evaluate_bbox(top_level))
    nwell_rectangle_ref = prec_ref_center(nwell_rectangle)
    nwell_rectangle_ref.move(p_block_ref.center) 
    top_level.add(nwell_rectangle_ref)

    #Renaming Ports
    top_level.add_ports(p_block.get_ports_list())
    
    component = component_snap_to_grid(rename_ports_by_orientation(top_level))
    # Store netlist as string to avoid gymnasium info dict type restrictions
    # Compatible with both gdsfactory 7.7.0 and 7.16.0+ strict Pydantic validation
    netlist_obj = p_block_netlist(pdk, pblock=(width,length,ratio))
    component.info['netlist'] = str(netlist_obj)
    # Store serialized netlist data for reconstruction if needed
    component.info['netlist_data'] = {
        'circuit_name': netlist_obj.circuit_name,
        'nodes': netlist_obj.nodes,
        'source_netlist': netlist_obj.source_netlist
    }
    #print(component.info['netlist'].generate_netlist())

    return component
