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

from glayout.flow.blocks.diffpair_cmirror_bias import diff_pair_ibias
from glayout.flow.blocks.stacked_current_mirror import stacked_nfet_current_mirror
from glayout.flow.blocks.differential_to_single_ended_converter import differential_to_single_ended_converter
from glayout.flow.blocks.opamp.row_csamplifier_diff_to_single_ended_converter import row_csamplifier_diff_to_single_ended_converter
from glayout.flow.blocks.opamp.diff_pair_stackedcmirror import diff_pair_stackedcmirror
from glayout.flow.spice import Netlist
from glayout.flow.blocks.current_mirror import current_mirror_netlist

@validate_arguments
def __create_and_route_pins(
    pdk: MappedPDK,
    opamp_top: Component,
    pmos_comps_ref: ComponentReference,
    halfmultn_drain_routeref: ComponentReference,
    halfmultn_gate_routeref: ComponentReference
) -> tuple:
    _max_metal_seperation_ps = pdk.util_max_metal_seperation()
    # route halfmultp source, drain, and gate together, place vdd pin in the middle
    halfmultp_Lsrcport = opamp_top.ports["commonsource_Pamp_L_multiplier_0_source_con_N"]
    halfmultp_Rsrcport = opamp_top.ports["commonsource_Pamp_R_multiplier_0_source_con_N"]
    opamp_top << c_route(pdk, halfmultp_Lsrcport, halfmultp_Rsrcport, extension=opamp_top.ymax-halfmultp_Lsrcport.center[1], fullbottom=True,viaoffset=(False,False))
    # place vdd pin
    vddpin = opamp_top << rectangle(size=(5,3),layer=pdk.get_glayer("met4"),centered=True)
    vddpin.movey(opamp_top.ymax)
    # route vdd to source of 2L/2R
    opamp_top << straight_route(pdk, opamp_top.ports["pcomps_2L2Rsrcvia_top_met_N"], vddpin.ports["e4"])
    # drain route above vdd pin
    halfmultp_Ldrainport = opamp_top.ports["commonsource_Pamp_L_multiplier_0_drain_con_N"]
    halfmultp_Rdrainport = opamp_top.ports["commonsource_Pamp_R_multiplier_0_drain_con_N"]
    halfmultp_drain_routeref = opamp_top << c_route(pdk, halfmultp_Ldrainport, halfmultp_Rdrainport, extension=opamp_top.ymax-halfmultp_Ldrainport.center[1]+pdk.get_grule("met5")["min_separation"], fullbottom=True)
    halfmultp_Lgateport = opamp_top.ports["commonsource_Pamp_L_multiplier_0_gate_con_S"]
    halfmultp_Rgateport = opamp_top.ports["commonsource_Pamp_R_multiplier_0_gate_con_S"]
    ptop_halfmultp_gate_route = opamp_top << c_route(pdk, halfmultp_Lgateport, halfmultp_Rgateport, extension=abs(pmos_comps_ref.ymin-halfmultp_Lgateport.center[1])+pdk.get_grule("met5")["min_separation"],fullbottom=True,viaoffset=(False,False))
    # halfmultn to halfmultp drain to drain route
    extensionL = min(halfmultn_drain_routeref.ports["con_W"].center[0],halfmultp_drain_routeref.ports["con_W"].center[0])
    extensionR = max(halfmultn_drain_routeref.ports["con_E"].center[0],halfmultp_drain_routeref.ports["con_E"].center[0])
    opamp_top << c_route(pdk, halfmultn_drain_routeref.ports["con_W"], halfmultp_drain_routeref.ports["con_W"],extension=abs(opamp_top.xmin-extensionL)+2,cwidth=2)
    n_to_p_output_route = opamp_top << c_route(pdk, halfmultn_drain_routeref.ports["con_E"], halfmultp_drain_routeref.ports["con_E"],extension=abs(opamp_top.xmax-extensionR)+2,cwidth=2)
    # top nwell taps to vdd, top p substrate taps to gnd
    opamp_top << straight_route(pdk, opamp_top.ports["commonsource_cmirror_output_L_tie_N_top_met_N"], opamp_top.ports["pcomps_top_ptap_S_top_met_S"], width=5)
    opamp_top << straight_route(pdk, opamp_top.ports["commonsource_cmirror_output_R_tie_N_top_met_N"], opamp_top.ports["pcomps_top_ptap_S_top_met_S"], width=5)
    L_toptapn_route = opamp_top.ports["commonsource_Pamp_L_tie_N_top_met_N"]
    R_toptapn_route = opamp_top.ports["commonsource_Pamp_R_tie_N_top_met_N"]
    opamp_top << straight_route(pdk, movex(vddpin.ports["e4"],destination=L_toptapn_route.center[0]), L_toptapn_route, glayer1="met3",fullbottom=True)
    opamp_top << straight_route(pdk, movex(vddpin.ports["e4"],destination=R_toptapn_route.center[0]), R_toptapn_route, glayer1="met3",fullbottom=True)
    # bias pins for first two stages
    vbias1 = opamp_top << rectangle(size=(5,3),layer=pdk.get_glayer("met3"),centered=True)
    vbias1.movey(opamp_top.ymin - _max_metal_seperation_ps - vbias1.ymax)
    opamp_top << straight_route(pdk, vbias1.ports["e2"], opamp_top.ports["diffpair_ibias_B_gate_S"],width=1,fullbottom=False)
    vbias2 = opamp_top << rectangle(size=(5,3),layer=pdk.get_glayer("met5"),centered=True)
    vbias2.movex(1+opamp_top.xmax+evaluate_bbox(vbias2)[0]+pdk.util_max_metal_seperation()).movey(opamp_top.ymin+vbias2.ymax)
    opamp_top << L_route(pdk, halfmultn_gate_routeref.ports["con_E"], vbias2.ports["e2"],hwidth=2)
    # route + and - pins (being careful about antenna violations)
    minusi_pin = opamp_top << rectangle(size=(5,2),layer=pdk.get_glayer("met3"),centered=True)
    minusi_pin.movex(opamp_top.xmin).movey(_max_metal_seperation_ps + minusi_pin.ymax + halfmultn_drain_routeref.ports["con_W"].center[1] + halfmultn_drain_routeref.ports["con_W"].width/2)
    iport_antenna1 = movex(minusi_pin.ports["e3"],destination=opamp_top.ports["diffpair_MINUSgateroute_W_con_N"].center[0]-9*_max_metal_seperation_ps)
    opamp_top << L_route(pdk, opamp_top.ports["diffpair_MINUSgateroute_W_con_N"],iport_antenna1)
    iport_antenna2 = movex(iport_antenna1,offsetx=-9*_max_metal_seperation_ps)
    opamp_top << straight_route(pdk, iport_antenna1, iport_antenna2,glayer1="met4",glayer2="met4",via2_alignment=('c','c'),via1_alignment=('c','c'),fullbottom=True)
    iport_antenna2.layer=pdk.get_glayer("met4")
    opamp_top << straight_route(pdk, iport_antenna2, minusi_pin.ports["e3"],glayer1="met3",via2_alignment=('c','c'),via1_alignment=('c','c'),fullbottom=True)
    plusi_pin = opamp_top << rectangle(size=(5,2),layer=pdk.get_glayer("met3"),centered=True)
    plusi_pin.movex(opamp_top.xmin + plusi_pin.xmax).movey(_max_metal_seperation_ps + minusi_pin.ymax + plusi_pin.ymax)
    iport_antenna1 = movex(plusi_pin.ports["e3"],destination=opamp_top.ports["diffpair_PLUSgateroute_E_con_N"].center[0]-9*_max_metal_seperation_ps)
    opamp_top << L_route(pdk, opamp_top.ports["diffpair_PLUSgateroute_E_con_N"],iport_antenna1)
    iport_antenna2 = movex(iport_antenna1,offsetx=-9*_max_metal_seperation_ps)
    opamp_top << straight_route(pdk, iport_antenna1, iport_antenna2, glayer1="met4",glayer2="met4",via2_alignment=('c','c'),via1_alignment=('c','c'),fullbottom=True)
    iport_antenna2.layer=pdk.get_glayer("met4")
    opamp_top << straight_route(pdk, iport_antenna2, plusi_pin.ports["e3"],glayer1="met3",via2_alignment=('c','c'),via1_alignment=('c','c'),fullbottom=True)
    # route top center components to diffpair
    opamp_top << straight_route(pdk,opamp_top.ports["diffpair_tr_multiplier_0_drain_N"], opamp_top.ports["pcomps_pbottomAB_R_gate_S"], glayer1="met5",width=3*pdk.get_grule("met5")["min_width"],via1_alignment_layer="met2",via1_alignment=('c','c'))
    opamp_top << straight_route(pdk,opamp_top.ports["diffpair_tl_multiplier_0_drain_N"], opamp_top.ports["pcomps_minusvia_top_met_S"], glayer1="met5",width=3*pdk.get_grule("met5")["min_width"],via1_alignment_layer="met2",via1_alignment=('c','c'))
    # route minus transistor drain to output
    outputvia_diff_pcomps = opamp_top << via_stack(pdk,"met5","met4")
    outputvia_diff_pcomps.movex(opamp_top.ports["diffpair_tl_multiplier_0_drain_N"].center[0]).movey(ptop_halfmultp_gate_route.ports["con_E"].center[1])
    # add pin ports
    opamp_top.add_ports(vddpin.get_ports_list(), prefix="pin_vdd_")
    opamp_top.add_ports(vbias1.get_ports_list(), prefix="pin_diffpairibias_")
    opamp_top.add_ports(vbias2.get_ports_list(), prefix="pin_commonsourceibias_")
    opamp_top.add_ports(minusi_pin.get_ports_list(), prefix="pin_minus_")
    opamp_top.add_ports(plusi_pin.get_ports_list(), prefix="pin_plus_")
    #opamp_top.add_ports(output.get_ports_list(), prefix="pin_output_")
    return opamp_top, n_to_p_output_route



@validate_arguments
def __add_mimcap_arr(pdk: MappedPDK, opamp_top: Component, mim_cap_size, mim_cap_rows, ymin: float, n_to_p_output_route) -> tuple[Component, Netlist]:
    mim_cap_size = pdk.snap_to_2xgrid(mim_cap_size, return_type="float")
    max_metalsep = pdk.util_max_metal_seperation()
    mimcaps_ref = opamp_top << mimcap_array(pdk,mim_cap_rows,2,size=mim_cap_size,rmult=6)

    mimcap_netlist = mimcaps_ref.info['netlist']

    displace_fact = max(max_metalsep,pdk.get_grule("capmet")["min_separation"])
    mimcaps_ref.movex(pdk.snap_to_2xgrid(opamp_top.xmax + displace_fact + mim_cap_size[0]/2))
    mimcaps_ref.movey(pdk.snap_to_2xgrid(ymin + mim_cap_size[1]/2))
    # connect mimcap to gnd
    port1 = opamp_top.ports["pcomps_mimcap_connection_con_N"]
    port2 = mimcaps_ref.ports["row"+str(int(mim_cap_rows)-1)+"_col0_bottom_met_N"]
    cref2_extension = max_metalsep + opamp_top.ymax - max(port1.center[1], port2.center[1])
    opamp_top << c_route(pdk,port1,port2, extension=cref2_extension, fullbottom=True)
    intermediate_output = set_port_orientation(n_to_p_output_route.ports["con_S"],"E")
    opamp_top << L_route(pdk, mimcaps_ref.ports["row0_col0_top_met_S"], intermediate_output, hwidth=3)
    opamp_top.add_ports(mimcaps_ref.get_ports_list(),prefix="mimcap_")
    # add the cs output as a port
    opamp_top.add_port(name="commonsource_output_E", port=intermediate_output)
    return opamp_top, mimcap_netlist

def opamp_gain_stage_netlist(mimcap_netlist: Netlist, diff_cs_netlist: Netlist, cs_bias_netlist: Netlist) -> Netlist:
    netlist = Netlist(
        circuit_name="GAIN_STAGE",
        nodes=['VIN1', 'VIN2', 'VOUT', 'VDD', 'IBIAS', 'GND']
    )

    diff_cs_ref = netlist.connect_netlist(
        diff_cs_netlist,
        [('VSS', 'VDD')]
    )

    netlist.connect_netlist(
        cs_bias_netlist,
        [('VREF', 'IBIAS'), ('VSS', 'GND'), ('VCOPY', 'VOUT'), ('VB', 'GND')]
    )

    mimcap_ref = netlist.connect_netlist(mimcap_netlist, [('V1', 'VOUT'), ('V2', 'VSS2')])

    netlist.connect_subnets(
        mimcap_ref,
        diff_cs_ref,
        [('V2', 'VSS2')]
    )

    return netlist

def opamp_twostage_netlist(input_stage_netlist: Netlist, gain_stage_netlist: Netlist) -> Netlist:
    two_stage_netlist = Netlist(
        circuit_name="OPAMP_TWO_STAGE",
        nodes=['VDD', 'GND', 'DIFFPAIR_BIAS', 'VP', 'VN', 'CS_BIAS', 'VOUT']
    )

    input_stage_ref = two_stage_netlist.connect_netlist(
        input_stage_netlist,
        [('IBIAS', 'DIFFPAIR_BIAS'), ('VSS', 'GND'), ('B', 'GND')]
    )

    gain_stage_ref = two_stage_netlist.connect_netlist(
        gain_stage_netlist,
        [('IBIAS', 'CS_BIAS')]
    )

    two_stage_netlist.connect_subnets(
        input_stage_ref,
        gain_stage_ref,
        [('VDD1', 'VIN1'), ('VDD2', 'VIN2')]
    )

    return two_stage_netlist

def opamp_twostage(
    pdk: MappedPDK,
    half_diffpair_params: tuple[float, float, int] = (6, 1, 4),
    diffpair_bias: tuple[float, float, int] = (6, 2, 4),
    half_common_source_params: tuple[float, float, int, int] = (7, 1, 10, 3),
    half_common_source_bias: tuple[float, float, int, int] = (6, 2, 8, 2),
    half_pload: tuple[float,float,int] = (6,1,6),
    mim_cap_size=(12, 12),
    mim_cap_rows=3,
    rmult: int = 2,
    with_antenna_diode_on_diffinputs: int=5
) -> Component:
    """
    create a two stage opamp, args->
    pdk: pdk to use
    half_diffpair_params: diffpair (width,length,fingers)
    diffpair_bias: bias transistor for diffpair nmos (width,length,fingers). The ref and output of the cmirror are identical
    half_common_source_params: pmos top component amp (width,length,fingers,mults)
    half_common_source_bias: bottom L/R large nmos current mirror (width,length,fingers,mults). The ref of the cmirror always has 1 multplier. multiplier must be >=2
    ****NOTE: change the multiplier option to change the relative sizing of the current mirror ref/output
    half_pload: all 4 pmos load transistors of first stage (width,length,...). The last element in the tuple is the fingers of the bottom two pmos.
    mim_cap_size: width,length of individual mim_cap
    mim_cap_rows: number of rows in the mimcap array (always 2 cols)
    rmult: routing multiplier (larger = wider routes)
    with_antenna_diode_on_diffinputs: adds antenna diodes with_antenna_diode_on_diffinputs*(1um/0.5um) on the positive and negative inputs to the opamp
    """
    # error checks
    if with_antenna_diode_on_diffinputs!=0 and with_antenna_diode_on_diffinputs<2:
        raise ValueError("number of antenna diodes should be at least 2 (or 0 to specify no diodes)")
    if half_common_source_bias[3] < 2:
        raise ValueError("half_common_source_bias num multiplier must be >= 2")
    opamp_top, halfmultn_drain_routeref, halfmultn_gate_routeref, _cref = diff_pair_stackedcmirror(pdk, half_diffpair_params, diffpair_bias, half_common_source_bias, rmult, with_antenna_diode_on_diffinputs)

    opamp_top.info['netlist'].circuit_name = "INPUT_STAGE"

    # place pmos components
    pmos_comps = differential_to_single_ended_converter(pdk, rmult, half_pload, opamp_top.ports["diffpair_tl_multiplier_0_drain_N"].center[0])
    clear_cache()

    pmos_comps = row_csamplifier_diff_to_single_ended_converter(pdk, pmos_comps, half_common_source_params, rmult)

    cs_bias_netlist = current_mirror_netlist(
        pdk,
        width=diffpair_bias[0],
        length=diffpair_bias[1],
        multipliers=diffpair_bias[2]
    )

    ydim_ncomps = opamp_top.ymax
    pmos_comps_ref = opamp_top << pmos_comps
    pmos_comps_ref.movey(round(ydim_ncomps + pmos_comps_ref.ymax+10))
    opamp_top.add_ports(pmos_comps_ref.get_ports_list(),prefix="pcomps_")
    rename_func = lambda name_, port_ : name_.replace("pcomps_halfpspecialmarker","commonsource_Pamp") if name_.startswith("pcomps_halfpspecialmarker") else name_
    opamp_top = rename_component_ports(opamp_top, rename_function=rename_func)
    # create pins and route
    clear_cache()
    opamp_top, n_to_p_output_route = __create_and_route_pins(pdk, opamp_top, pmos_comps_ref, halfmultn_drain_routeref, halfmultn_gate_routeref)
    # place mimcaps and route
    clear_cache()
    opamp_top, mimcap_netlist = __add_mimcap_arr(pdk, opamp_top, mim_cap_size, mim_cap_rows, pmos_comps_ref.ymin, n_to_p_output_route)
    opamp_top.add_ports(n_to_p_output_route.get_ports_list(),"special_con_npr_")
    # return
    opamp_top.add_ports(_cref.get_ports_list(), prefix="gnd_route_")

    pmos_comps.info['netlist'] = opamp_gain_stage_netlist(mimcap_netlist, pmos_comps.info['netlist'], cs_bias_netlist)
    opamp_top.info['netlist'] = opamp_twostage_netlist(opamp_top.info['netlist'], pmos_comps.info['netlist'])

    return opamp_top


