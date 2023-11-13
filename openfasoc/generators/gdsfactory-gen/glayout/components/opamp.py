from gdsfactory.cell import cell, clear_cache
from gdsfactory.component import Component, copy
from gdsfactory.component_reference import ComponentReference
from gdsfactory.components.rectangle import rectangle
from glayout.pdk.mappedpdk import MappedPDK
from typing import Optional, Union
from glayout.primitives.fet import nmos, pmos, multiplier
from glayout.components.diff_pair import diff_pair
from glayout.primitives.guardring import tapring
from glayout.primitives.mimcap import mimcap_array, mimcap
from glayout.routing.L_route import L_route
from glayout.routing.c_route import c_route
from glayout.primitives.via_gen import via_stack, via_array
from gdsfactory.routing.route_quad import route_quad
from glayout.pdk.util.comp_utils import evaluate_bbox, prec_ref_center, movex, movey, to_decimal, to_float, move, align_comp_to_port, get_padding_points_cc
from glayout.pdk.util.port_utils import rename_ports_by_orientation, rename_ports_by_list, add_ports_perimeter, print_ports, set_port_orientation, rename_component_ports
from glayout.routing.straight_route import straight_route
from glayout.pdk.util.snap_to_grid import component_snap_to_grid
from pydantic import validate_arguments
from glayout.placement.two_transistor_interdigitized import two_nfet_interdigitized


from glayout.components.opamp_twostage import opamp_twostage


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
def __add_mimcap_arr(pdk: MappedPDK, opamp_top: Component, mim_cap_size, mim_cap_rows, ymin: float, n_to_p_output_route) -> Component:
    mim_cap_size = pdk.snap_to_2xgrid(mim_cap_size, return_type="float")
    max_metalsep = pdk.util_max_metal_seperation()
    mimcaps_ref = opamp_top << mimcap_array(pdk,mim_cap_rows,2,size=mim_cap_size,rmult=6)
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
    return opamp_top




@validate_arguments
def __add_output_stage(
    pdk: MappedPDK,
    opamp_top: Component,
    amplifierParams: tuple[float, float, int],
    biasParams: list,
    rmult: int,
) -> Component:
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
    return opamp_top



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
    with_antenna_diode_on_diffinputs: int=5
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
    opamp_top = __add_output_stage(pdk, opamp_top, output_stage_params, output_stage_bias, rmult)
    # return
    return rename_ports_by_orientation(component_snap_to_grid(opamp_top))


