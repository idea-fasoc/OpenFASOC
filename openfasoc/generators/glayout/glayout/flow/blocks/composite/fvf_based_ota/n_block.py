from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
from gdsfactory import Component
from gdsfactory.cell import cell
from gdsfactory.component_reference import ComponentReference

from glayout.flow.pdk.util.comp_utils import evaluate_bbox, prec_ref_center, prec_center, align_comp_to_port
from glayout.flow.pdk.util.port_utils import rename_ports_by_orientation
from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid
from gdsfactory.components import text_freetype, rectangle

from glayout.flow.spice.netlist import Netlist
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.blocks.elementary.FVF.fvf import fvf_netlist, flipped_voltage_follower
from glayout.flow.blocks.elementary.current_mirror.current_mirror import current_mirror, current_mirror_netlist
from glayout.flow.primitives.via_gen import via_stack, via_array
from glayout.flow.primitives.fet import nmos, pmos, multiplier
from glayout.flow.blocks.composite.fvf_based_ota.low_voltage_cmirror import low_voltage_cmirror, low_voltage_cmirr_netlist

def n_block_netlist(fet_inA_ref: ComponentReference, fet_inB_ref: ComponentReference, fvf_1_ref: ComponentReference, fvf_2_ref: ComponentReference, cmirror: Component, global_c_bias: Component) -> Netlist:

        netlist = Netlist(circuit_name='N_block', nodes=['IBIAS1', 'IBIAS2', 'GND', 'ILCM1', 'ILCM2', 'IFVF1','IFVF2', 'INP', 'INM', 'Min1_D', 'Min2_D', 'OUT_N_1', 'OUT_N_2'])
        netlist.connect_netlist(global_c_bias.info['netlist'], [('IBIAS1','IBIAS1'),('GND','GND'),('IBIAS2','IBIAS2'),('IOUT1','ILCM1'),('IOUT2','ILCM2')])
        netlist.connect_netlist(cmirror.info['netlist'], [('VREF','OUT_N_1'),('VCOPY','OUT_N_2'),('VSS', 'GND'),('VB','GND')])
        netlist.connect_netlist(fet_inA_ref.info['netlist'], [('D', 'Min1_D'),('G','INM'),('B','GND')])
        netlist.connect_netlist(fet_inB_ref.info['netlist'], [('D', 'Min2_D'),('G','INP'),('B','GND')])
        netlist.connect_netlist(fvf_1_ref.info['netlist'], [('VIN','INM'),('VOUT', 'INP'),('VBULK','GND'),('Ib','IFVF1')])
        netlist.connect_netlist(fvf_2_ref.info['netlist'], [('VIN','INP'),('VOUT', 'INM'),('VBULK','GND'),('Ib','IFVF2')])

        return netlist


@cell
def n_block(
        pdk: MappedPDK,
        input_pair_params: tuple[float,float]=(4,2),
        fvf_shunt_params: tuple[float,float]=(2.75,1),
        current_mirror_params: tuple[float,float]=(2.25,1),
        ratio: int=1,
        global_current_bias_params: tuple[float,float,float]=(8.3,1.42,2)
        ) -> Component:
    """
    creates the n-block for super class AB OTA
    pdk: pdk to use
    input_pair_params: differential input pair(N-type) - (width,length), input nmoses of the fvf get the same dimensions
    fvf_shunt_params: feedback fet of fvf - (width,length)
    current_mirror_params: output stage N-type currrent mirrors - (width, length)
    ratio: current mirroring ratio at output stage
    global_current_bias_params: A low voltage current mirror for biasing - consists of 7 nmoses of (W/L) and one nmos of (W'/L) - (W,W',L)
    """ 
    # Create a top level component
    top_level = Component("n_block")
    
    #input differential pair
    fet_in = nmos(pdk, width=input_pair_params[0], length=input_pair_params[1], fingers=1, with_dnwell=False, with_tie=True, with_substrate_tap=False, sd_rmult=3)
    fet_inA_ref = prec_ref_center(fet_in)
    fet_inB_ref = prec_ref_center(fet_in)
    fet_inA_ref.movex(-evaluate_bbox(fet_in)[0]/2 - pdk.util_max_metal_seperation())
    fet_inB_ref.movex(evaluate_bbox(fet_in)[0]/2 + pdk.util_max_metal_seperation())

    top_level.add(fet_inA_ref)
    top_level.add(fet_inB_ref)

    #creating VinP and VinM ports
    viam2m3 = via_stack(pdk, "met2", "met3", centered=True)
    viam3m4 = via_stack(pdk, "met3", "met4", centered=True)
    gate_inA_via = top_level << viam3m4
    gate_inB_via = top_level << viam3m4
    source_inA_via = top_level << viam2m3
    source_inB_via = top_level << viam2m3
    gate_inA_via.move(fet_inA_ref.ports["multiplier_0_gate_W"].center).movex(-evaluate_bbox(fet_in)[0]/4).movey(-evaluate_bbox(fet_in)[1]/2)
    gate_inB_via.move(fet_inB_ref.ports["multiplier_0_gate_E"].center).movex(evaluate_bbox(fet_in)[0]/4).movey(-evaluate_bbox(fet_in)[1]/2)

    source_inA_via.move(fet_inA_ref.ports["multiplier_0_source_W"].center).movex(-evaluate_bbox(fet_in)[0]/4)
    source_inB_via.move(fet_inB_ref.ports["multiplier_0_source_E"].center).movex(evaluate_bbox(fet_in)[0]/4)

    
    top_level << L_route(pdk, fet_inA_ref.ports["multiplier_0_gate_W"], gate_inA_via.ports["bottom_met_N"], hglayer="met2", vglayer="met3")
    top_level << L_route(pdk, fet_inB_ref.ports["multiplier_0_gate_E"], gate_inB_via.ports["bottom_met_N"], hglayer="met2", vglayer="met3")
    top_level << straight_route(pdk, fet_inA_ref.ports["multiplier_0_source_W"], source_inA_via.ports["bottom_met_E"], width=0.29*2)
    top_level << straight_route(pdk, fet_inB_ref.ports["multiplier_0_source_E"], source_inB_via.ports["bottom_met_W"], width=0.29*2)
    
    top_level.add_ports(fet_inA_ref.get_ports_list(), prefix="Min_1_")
    top_level.add_ports(fet_inB_ref.get_ports_list(), prefix="Min_2_")
    top_level.add_ports(gate_inA_via.get_ports_list(), prefix="gate_inA_")
    top_level.add_ports(gate_inB_via.get_ports_list(), prefix="gate_inB_")
    
    #FVF cells
    fvf = flipped_voltage_follower(pdk, width=(input_pair_params[0],fvf_shunt_params[0]), length=(input_pair_params[1],fvf_shunt_params[1]), fingers=(1,1), sd_rmult=3, with_dnwell=False) 
    fvf_1_ref = prec_ref_center(fvf)
    fvf_2_ref = prec_ref_center(fvf)
    fvf_1_ref.movex(fet_inB_ref.xmax + evaluate_bbox(fvf)[0]/2 + pdk.util_max_metal_seperation())
    fvf_2_ref.movex(fet_inB_ref.xmax + evaluate_bbox(fvf)[0]/2 + pdk.util_max_metal_seperation())
    fvf_1_ref = rename_ports_by_orientation(fvf_1_ref.mirror((0,-100),(0,100)))
    top_level.add(fvf_1_ref)
    top_level.add(fvf_2_ref)

    #creating ports for conncetion
    gate_fvf_1A_via = top_level << viam2m3
    gate_fvf_2A_via = top_level << viam2m3
    gate_fvf_1A_via.move(fvf_1_ref.ports["A_multiplier_0_gate_S"].center).movex(-evaluate_bbox(fet_in)[0]/4).movey(-evaluate_bbox(fet_in)[1]/1.5)
    gate_fvf_2A_via.move(fvf_2_ref.ports["A_multiplier_0_gate_S"].center).movex(evaluate_bbox(fet_in)[0]/4).movey(-evaluate_bbox(fet_in)[1]/1.5)


    top_level << L_route(pdk, fvf_1_ref.ports["A_multiplier_0_gate_E"], gate_fvf_1A_via.ports["top_met_N"], hglayer="met2", vglayer="met3")
    top_level << L_route(pdk, fvf_2_ref.ports["A_multiplier_0_gate_E"], gate_fvf_2A_via.ports["top_met_N"], hglayer="met2", vglayer="met3")


    #connecting input pair with fvfs
    top_level << L_route(pdk, gate_inA_via.ports["bottom_met_S"], gate_fvf_1A_via.ports["top_met_E"], hglayer="met2", vglayer="met3")
    top_level << L_route(pdk, gate_inB_via.ports["bottom_met_S"], gate_fvf_2A_via.ports["top_met_W"], hglayer="met2", vglayer="met3")
    top_level << c_route(pdk, source_inA_via.ports["top_met_N"], fvf_2_ref.ports["A_source_top_met_N"], extension=0.8*evaluate_bbox(fet_in)[1], width1=0.4, width2=0.4, cwidth=0.5, e1glayer="met3", e2glayer="met3", cglayer="met2")
    top_level << c_route(pdk, source_inB_via.ports["top_met_N"], fvf_1_ref.ports["A_source_top_met_N"], extension=1.1*evaluate_bbox(fet_in)[1], width1=0.4, width2=0.4, cwidth=0.5, e1glayer="met3", e2glayer="met3", cglayer="met2")
    
    top_level.add_ports(fvf_1_ref.get_ports_list(), prefix="fvf_1_")
    top_level.add_ports(fvf_2_ref.get_ports_list(), prefix="fvf_2_")

    cmirror = current_mirror(pdk, numcols=2, with_substrate_tap=False, width=current_mirror_params[0], length=current_mirror_params[1], fingers=ratio, sd_rmult=3)
    cmirr_ref = prec_ref_center(cmirror)
    cmirr_ref.movey(fvf_1_ref.ymin - (evaluate_bbox(cmirror)[1] + evaluate_bbox(fvf)[1])/2)
    top_level.add(cmirr_ref)
    
    top_level << straight_route(pdk, cmirr_ref.ports["fet_A_source_W"], cmirr_ref.ports["welltie_W_top_met_W"], glayer1='met1', width=0.6)
    top_level << straight_route(pdk, cmirr_ref.ports["fet_A_0_dummy_L_gsdcon_top_met_W"],cmirr_ref.ports["welltie_W_top_met_W"],glayer1="met1", width=0.5)
    top_level << straight_route(pdk, cmirr_ref.ports["fet_B_1_dummy_R_gsdcon_top_met_E"],cmirr_ref.ports["welltie_E_top_met_E"],glayer1="met1", width=0.5)


    top_level.add_ports(cmirr_ref.get_ports_list(), prefix="op_cmirr_")
 
    global_c_bias = low_voltage_cmirror(pdk, width=(global_current_bias_params[0]/2,global_current_bias_params[1]), length=global_current_bias_params[2], fingers=(2,1))
    global_c_bias_ref = prec_ref_center(global_c_bias)
    global_c_bias_ref.movey(cmirr_ref.ymin - evaluate_bbox(global_c_bias)[1]/2 - 8*pdk.util_max_metal_seperation())
    top_level.add(global_c_bias_ref)
    top_level.add_ports(global_c_bias_ref.get_ports_list(), prefix="cbias_")


    fet_1 = nmos(pdk, width=input_pair_params[0], length=input_pair_params[1], fingers=1, with_dnwell=False, with_tie=True, with_substrate_tap=False, sd_rmult=3)
    fet_2 = nmos(pdk, width=input_pair_params[0], length=input_pair_params[1], fingers=1, with_dnwell=False, with_tie=True, with_substrate_tap=False, sd_rmult=3)
    fvf_1 = flipped_voltage_follower(pdk, width=(input_pair_params[0],fvf_shunt_params[0]), length=(input_pair_params[1],fvf_shunt_params[1]), fingers=(1,1), sd_rmult=3, with_dnwell=False)
    fvf_2 = flipped_voltage_follower(pdk, width=(input_pair_params[0],fvf_shunt_params[0]), length=(input_pair_params[1],fvf_shunt_params[1]), fingers=(1,1), sd_rmult=3, with_dnwell=False)

    
    component = component_snap_to_grid(rename_ports_by_orientation(top_level))
    # Store netlist as string to avoid gymnasium info dict type restrictions
    # Compatible with both gdsfactory 7.7.0 and 7.16.0+ strict Pydantic validation
    netlist_obj = n_block_netlist(fet_inA_ref, fet_inB_ref, fvf_1_ref, fvf_2_ref, cmirror, global_c_bias)
    component.info['netlist'] = str(netlist_obj)
    # Store serialized netlist data for reconstruction if needed
    component.info['netlist_data'] = {
        'circuit_name': netlist_obj.circuit_name,
        'nodes': netlist_obj.nodes,
        'source_netlist': netlist_obj.source_netlist
    }
    #print(component.info['netlist'].generate_netlist(only_subcircuits=True))

    return component
