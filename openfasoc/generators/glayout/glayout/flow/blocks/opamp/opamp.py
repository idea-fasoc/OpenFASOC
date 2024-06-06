from gdsfactory.cell import cell, clear_cache
from gdsfactory.component import Component, copy
from gdsfactory.component_reference import ComponentReference
from gdsfactory.components.rectangle import rectangle
from glayout.flow.pdk.mappedpdk import MappedPDK
from typing import Optional, Union
from glayout.flow.primitives.fet import nmos, pmos, multiplier
from glayout.flow.blocks.diff_pair import diff_pair
from glayout.flow.primitives.guardring import tapring
from glayout.flow.primitives.mimcap import mimcap_array, mimcap
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.primitives.via_gen import via_stack, via_array
from gdsfactory.routing.route_quad import route_quad
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, prec_ref_center, movex, movey, to_decimal, to_float, move, align_comp_to_port, get_padding_points_cc
from glayout.flow.pdk.util.port_utils import rename_ports_by_orientation, rename_ports_by_list, add_ports_perimeter, print_ports, set_port_orientation, rename_component_ports
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid
from pydantic import validate_arguments
from glayout.flow.placement.two_transistor_interdigitized import two_nfet_interdigitized
from glayout.flow.spice import Netlist

from glayout.flow.blocks.opamp.opamp_twostage import opamp_twostage
from glayout.flow.blocks.current_mirror import current_mirror_netlist

def opamp_output_stage_netlist(pdk: MappedPDK, output_amp_fet_ref: ComponentReference, biasParams: list) -> Netlist:
    bias_netlist = current_mirror_netlist(pdk, biasParams[0], biasParams[1], biasParams[2])

    output_stage_netlist = Netlist(
        circuit_name="OUTPUT_STAGE",
        nodes=['VDD', 'GND', 'IBIAS', 'VIN', 'VOUT']
    )

    output_stage_netlist.connect_netlist(
        output_amp_fet_ref.info['netlist'],
        [('D', 'VDD'), ('G', 'VIN'), ('B', 'GND'), ('S', 'VOUT')]
    )

    output_stage_netlist.connect_netlist(
        bias_netlist,
        [('VREF', 'IBIAS'), ('VSS', 'GND'), ('VCOPY', 'VOUT'), ('VB', 'GND')]
    )

    return output_stage_netlist

@validate_arguments
def __add_output_stage(
    pdk: MappedPDK,
    opamp_top: Component,
    amplifierParams: tuple[float, float, int],
    biasParams: list,
    rmult: int,
) -> tuple[Component, Netlist]:
    '''add output stage to opamp_top, args:
    pdk = pdk to use
    opamp_top = component to add output stage to
    amplifierParams = [width,length,fingers,mults] for amplifying FET
    biasParams = [width,length,fingers,mults] for bias FET
    '''
    # Instantiate output amplifier
    amp_fet_ref = opamp_top << nmos(
        pdk,
        width=amplifierParams[0],
        length=amplifierParams[1],
        fingers=amplifierParams[2],
        multipliers=1,
        sd_route_topmet="met3",
        gate_route_topmet="met3",
        rmult=rmult,
        with_dnwell=False,
        with_tie=True,
        with_substrate_tap=False,
        tie_layers=("met2","met2")
    )
    # Instantiate bias FET
    cmirror_ibias = opamp_top << two_nfet_interdigitized(
        pdk,
        numcols=biasParams[2],
        width=biasParams[0],
        length=biasParams[1],
        fingers=1,
        gate_route_topmet="met3",
        sd_route_topmet="met3",
        rmult=rmult,
        with_substrate_tap=False,
        tie_layers=("met2","met2")
    )

    metal_sep = pdk.util_max_metal_seperation()
    # Locate output stage relative position
    # x-coordinate: Center of SW capacitor in array
    # y-coordinate: Top of NMOS blocks
    xref_port = opamp_top.ports["mimcap_row0_col0_bottom_met_S"]
    x_cord = xref_port.center[0] - xref_port.width/2
    y_cord = opamp_top.ports["commonsource_cmirror_output_R_tie_N_top_met_N"].center[1]
    dims = evaluate_bbox(amp_fet_ref)
    center = [x_cord + dims[0]/2, y_cord - dims[1]/2]
    amp_fet_ref.move(center)
    amp_fet_ref.movey(pdk.get_grule("active_tap", "p+s/d")["min_enclosure"])
    dims = evaluate_bbox(cmirror_ibias)
    cmirror_ibias.movex(amp_fet_ref.xmin + dims[0]/2)
    cmirror_ibias.movey(amp_fet_ref.ymin - dims[1]/2 - metal_sep)
    # route input of output_stage to output of previous stage
    n_to_p_output_route = opamp_top.ports["special_con_npr_con_S"]
    opamp_top << L_route(pdk, n_to_p_output_route, amp_fet_ref.ports["multiplier_0_gate_W"])
    # route drain of amplifier to vdd
    vdd_route_extension = opamp_top.ymax-opamp_top.ports["pin_vdd_e4"].center[1]+metal_sep
    opamp_top << c_route(pdk,amp_fet_ref.ports["multiplier_0_drain_N"],set_port_orientation(opamp_top.ports["pin_vdd_e4"],"N"),width1=5,width2=5,extension=vdd_route_extension,e2glayer="met3")
    vddvia = opamp_top << via_stack(pdk,"met3","met4",fullbottom=True)
    align_comp_to_port(vddvia,opamp_top.ports["pin_vdd_e4"],('c','t'))
    # route drain of cmirror to source of amplifier
    opamp_top << c_route(pdk, cmirror_ibias.ports["B_drain_E"],amp_fet_ref.ports["multiplier_0_source_E"],extension=metal_sep)
    # route cmirror: A gate, B gate and A drain together. Then A source and B source to ground
    gate_short = opamp_top << c_route(pdk, cmirror_ibias.ports["A_gate_E"],cmirror_ibias.ports["B_gate_E"],extension=3*metal_sep,viaoffset=None)
    opamp_top << L_route(pdk, gate_short.ports["con_N"],cmirror_ibias.ports["A_drain_E"],viaoffset=False,fullbottom=False)
    srcshort = opamp_top << c_route(pdk, cmirror_ibias.ports["A_source_W"],cmirror_ibias.ports["B_source_W"],extension=metal_sep)
    opamp_top << straight_route(pdk, srcshort.ports["con_N"], cmirror_ibias.ports["welltie_N_top_met_S"],via2_alignment_layer="met2")
    # Route all tap rings together and ground them
    opamp_top << straight_route(pdk, cmirror_ibias.ports["welltie_N_top_met_N"],amp_fet_ref.ports["tie_S_top_met_S"])
    opamp_top << L_route(pdk, cmirror_ibias.ports["welltie_S_top_met_S"], opamp_top.ports["pin_gnd_E"],hwidth=4)
    # add ports, add bias/output pin, and return
    psuedo_out_port = movex(amp_fet_ref.ports["multiplier_0_source_E"].copy(),6*metal_sep)
    output_pin = opamp_top << straight_route(pdk, amp_fet_ref.ports["multiplier_0_source_E"], psuedo_out_port)
    opamp_top.add_ports(amp_fet_ref.get_ports_list(),prefix="outputstage_amp_")
    opamp_top.add_ports(cmirror_ibias.get_ports_list(),prefix="outputstage_bias_")
    opamp_top.add_ports(output_pin.get_ports_list(),prefix="pin_output_")
    bias_pin = opamp_top << rectangle(size=(5,3),layer=pdk.get_glayer("met3"),centered=True)
    bias_pin.movex(cmirror_ibias.center[0]).movey(cmirror_ibias.ports["B_gate_S"].center[1]-bias_pin.ymax-5*metal_sep)
    opamp_top << straight_route(pdk, bias_pin.ports["e2"], cmirror_ibias.ports["B_gate_S"],width=1)
    opamp_top.add_ports(bias_pin.get_ports_list(),prefix="pin_outputibias_")

    output_stage_netlist = opamp_output_stage_netlist(pdk, amp_fet_ref, biasParams)
    return opamp_top, output_stage_netlist

def opamp_netlist(two_stage_netlist: Netlist, output_stage_netlist: Netlist) -> Netlist:
    top_level_netlist = Netlist(
        circuit_name="opamp",
        nodes=["CSoutput", "vdd", "plus", "minus", "commonsourceibias", "outputibias", "diffpairibias", "gnd", "output"]
    )

    top_level_netlist.connect_netlist(
        two_stage_netlist,
        [('VDD', 'vdd'), ('GND', 'gnd'), ('DIFFPAIR_BIAS', 'diffpairibias'), ('VP', 'plus'), ('VN', 'minus'), ('CS_BIAS', 'commonsourceibias'), ('VOUT', 'CSoutput')]
    )

    top_level_netlist.connect_netlist(
        output_stage_netlist,
        [('VDD', 'vdd'), ('GND', 'gnd'), ('IBIAS', 'outputibias'), ('VIN', 'CSoutput'), ('VOUT', 'output')]
    )

    return top_level_netlist

@cell
def opamp(
    pdk: MappedPDK,
    half_diffpair_params: tuple[float, float, int] = (6, 1, 4),
    diffpair_bias: tuple[float, float, int] = (6, 2, 4),
    half_common_source_params: tuple[float, float, int, int] = (7, 1, 10, 3),
    half_common_source_bias: tuple[float, float, int, int] = (6, 2, 8, 2),
    output_stage_params: tuple[float, float, int] = (5, 1, 16),
    output_stage_bias: tuple[float, float, int] = (6, 2, 4),
    half_pload: tuple[float,float,int] = (6,1,6),
    mim_cap_size=(12, 12),
    mim_cap_rows=3,
    rmult: int = 2,
    with_antenna_diode_on_diffinputs: int=5, 
    add_output_stage: Optional[bool] = True
) -> Component:
    """
    create a two stage opamp with an output buffer, args->
    pdk: pdk to use
    half_diffpair_params: diffpair (width,length,fingers)
    diffpair_bias: bias transistor for diffpair nmos (width,length,fingers). The ref and output of the cmirror are identical
    half_common_source_params: pmos top component amp (width,length,fingers,mults)
    half_common_source_bias: bottom L/R large nmos current mirror (width,length,fingers,mults). The ref of the cmirror always has 1 multplier. multiplier must be >=2
    ****NOTE: change the multiplier option to change the relative sizing of the current mirror ref/output
    output_stage_amp_params: output amplifier transistor params (width, length, fingers)
    output_stage_bias: output amplifier current mirror params (width, length, fingers). The ref and output of the cmirror are identical
    half_pload: all 4 pmos load transistors of first stage (width,length,...). The last element in the tuple is the fingers of the bottom two pmos.
    mim_cap_size: width,length of individual mim_cap
    mim_cap_rows: number of rows in the mimcap array (always 2 cols)
    rmult: routing multiplier (larger = wider routes)
    with_antenna_diode_on_diffinputs: adds antenna diodes with_antenna_diode_on_diffinputs*(1um/0.5um) on the positive and negative inputs to the opamp
    """
    opamp_top = opamp_twostage(
        pdk,
        half_diffpair_params,
        diffpair_bias,
        half_common_source_params,
        half_common_source_bias,
        half_pload,
        mim_cap_size,
        mim_cap_rows,
        rmult,
        with_antenna_diode_on_diffinputs
    )
    # add output amplfier stage
    if add_output_stage:
        opamp_top, output_stage_netlist = __add_output_stage(pdk, opamp_top, output_stage_params, output_stage_bias, rmult)
        opamp_top.info['netlist'] = opamp_netlist(opamp_top.info['netlist'], output_stage_netlist)

    # return
    return rename_ports_by_orientation(component_snap_to_grid(opamp_top))


