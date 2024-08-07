from gdsfactory.cell import cell, clear_cache
from gdsfactory.component import Component, copy
from gdsfactory.component_reference import ComponentReference
from gdsfactory.components.rectangle import rectangle
from glayout.flow.pdk.mappedpdk import MappedPDK
from typing import Optional, Union
from glayout.flow.blocks.diff_pair import diff_pair
from glayout.flow.primitives.fet import nmos, pmos, multiplier
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



@validate_arguments
def __create_sharedgatecomps(pdk: MappedPDK, rmult: int, half_pload: tuple[float,float,int]) -> tuple:
    # add diffpair current mirror loads (this is a pmos current mirror split into 2 for better matching/compensation)
    shared_gate_comps = Component("shared gate components")
    # create the 2*2 multiplier transistors (placed twice later)
    twomultpcomps = Component("2 multiplier shared gate comps")
    pcompR = multiplier(pdk, "p+s/d", width=half_pload[0], length=half_pload[1], fingers=half_pload[2], dummy=True,rmult=rmult).copy()
    tapref = pcompR << tapring(pdk, evaluate_bbox(pcompR,padding=0.3+pdk.get_grule("n+s/d", "active_tap")["min_enclosure"]),"n+s/d","met1","met1")
    pcompR.add_padding(layers=(pdk.get_glayer("nwell"),), default=pdk.get_grule("active_tap", "nwell")["min_enclosure"])
    pcompR.add_ports(tapref.get_ports_list(),prefix="welltap_")
    pcompR << straight_route(pdk,pcompR.ports["dummy_L_gsdcon_top_met_W"],pcompR.ports["welltap_W_top_met_W"],glayer2="met1")
    pcompR << straight_route(pdk,pcompR.ports["dummy_R_gsdcon_top_met_W"],pcompR.ports["welltap_E_top_met_E"],glayer2="met1")
    pcompL = pcompR.copy()
    pcomp_AB_spacing = max(2*pdk.util_max_metal_seperation() + 6*pdk.get_grule("met4")["min_width"],pdk.get_grule("p+s/d")["min_separation"])
    _prefL = (twomultpcomps << pcompL).movex(-1 * pcompL.xmax - pcomp_AB_spacing/2)
    _prefR = (twomultpcomps << pcompR).movex(-1 * pcompR.xmin + pcomp_AB_spacing/2)
    twomultpcomps.add_ports(_prefL.get_ports_list(),prefix="L_")
    twomultpcomps.add_ports(_prefR.get_ports_list(),prefix="R_")
    twomultpcomps << route_quad(_prefL.ports["gate_W"], _prefR.ports["gate_E"], layer=pdk.get_glayer("met2"))
    # center
    relative_dim_comp = multiplier(
        pdk, "p+s/d", width=half_pload[0], length=half_pload[1], fingers=4, dummy=False, rmult=rmult
    )
    # TODO: figure out single dim spacing rule then delete both test delete and this
    single_dim = to_decimal(relative_dim_comp.xmax) + to_decimal(0.11) + to_decimal(half_pload[1])/2
    LRplusdopedPorts = list()
    LRgatePorts = list()
    LRdrainsPorts = list()
    LRsourcesPorts = list()
    LRdummyports = list()
    for i in [-2, -1, 1, 2]:
        dummy = False
        appenddummy = None
        extra_t = 0
        if i == -2:
            dummy = [True, False]
            appenddummy="L"
            pcenterfourunits = multiplier(
                pdk, "p+s/d", width=half_pload[0], length=half_pload[1], fingers=4, dummy=dummy, rmult=rmult
            )
            extra_t = -1 * single_dim
        elif i == 2:
            dummy = [False, True]
            appenddummy="R"
            pcenterfourunits = multiplier(
                pdk, "p+s/d", width=half_pload[0], length=half_pload[1], fingers=4, dummy=dummy, rmult=rmult
            )
            extra_t = single_dim
        else:
            pcenterfourunits = relative_dim_comp
        pref_ = prec_ref_center(pcenterfourunits).movex(pdk.snap_to_2xgrid(to_float(i * single_dim + extra_t)))
        shared_gate_comps.add(pref_)
        if appenddummy:
            LRdummyports+= [pref_.ports["dummy_"+appenddummy+"_gsdcon_top_met_N"]]
        LRplusdopedPorts += [pref_.ports["plusdoped_W"] , pref_.ports["plusdoped_E"]]
        LRgatePorts += [pref_.ports["gate_W"],pref_.ports["gate_E"]]
        LRdrainsPorts += [pref_.ports["source_W"],pref_.ports["source_E"]]
        LRsourcesPorts += [pref_.ports["drain_W"],pref_.ports["drain_E"]]
    # combine the two multiplier top and bottom with the 4 multiplier center row
    ytranslation_pcenter = 2 * pcenterfourunits.ymax + 5*pdk.util_max_metal_seperation()
    ptop_AB = (shared_gate_comps << twomultpcomps).movey(ytranslation_pcenter)
    pbottom_AB = (shared_gate_comps << twomultpcomps).movey(-1 * ytranslation_pcenter)

    return shared_gate_comps, ptop_AB, pbottom_AB, LRplusdopedPorts, LRgatePorts, LRdrainsPorts, LRsourcesPorts, LRdummyports



def __route_sharedgatecomps(pdk: MappedPDK, shared_gate_comps, via_location, ptop_AB, pbottom_AB, LRplusdopedPorts, LRgatePorts, LRdrainsPorts, LRsourcesPorts,LRdummyports) -> Component:
    _max_metal_seperation_ps = pdk.util_max_metal_seperation()
    # ground dummy transistors of the 4 center multipliers
    shared_gate_comps << straight_route(pdk,LRdummyports[0],pbottom_AB.ports["L_welltap_N_top_met_S"],glayer2="met1")
    shared_gate_comps << straight_route(pdk,LRdummyports[1],pbottom_AB.ports["R_welltap_N_top_met_S"],glayer2="met1")
    # connect p+s/d layer of the transistors
    shared_gate_comps << route_quad(LRplusdopedPorts[0],LRplusdopedPorts[-1],layer=pdk.get_glayer("p+s/d"))
    # connect drain of the left 2 and right 2, short sources of all 4
    shared_gate_comps << route_quad(LRdrainsPorts[0],LRdrainsPorts[3],layer=LRdrainsPorts[0].layer)
    shared_gate_comps << route_quad(LRdrainsPorts[4],LRdrainsPorts[7],layer=LRdrainsPorts[0].layer)
    shared_gate_comps << route_quad(LRsourcesPorts[0],LRsourcesPorts[-1],layer=LRsourcesPorts[0].layer)
    pcomps_2L_2R_sourcevia = shared_gate_comps << via_stack(pdk,pdk.layer_to_glayer(LRsourcesPorts[0].layer), "met4")
    pcomps_2L_2R_sourcevia.movey(evaluate_bbox(pcomps_2L_2R_sourcevia.parent.extract(layers=[LRsourcesPorts[0].layer,]))[1]/2 + LRsourcesPorts[0].center[1])
    shared_gate_comps.add_ports(pcomps_2L_2R_sourcevia.get_ports_list(),prefix="2L2Rsrcvia_")
    # short all the gates
    shared_gate_comps << route_quad(LRgatePorts[0],LRgatePorts[-1],layer=pdk.get_glayer("met2"))
    shared_gate_comps.add_ports(ptop_AB.get_ports_list(),prefix="ptopAB_")
    shared_gate_comps.add_ports(pbottom_AB.get_ports_list(),prefix="pbottomAB_")
    # short all gates of shared_gate_comps
    pcenter_gate_route_extension = pdk.snap_to_2xgrid(shared_gate_comps.xmax - min(ptop_AB.ports["R_gate_E"].center[0], LRgatePorts[-1].center[0]) - pdk.get_grule("active_diff")["min_width"])
    pcenter_l_croute = shared_gate_comps << c_route(pdk, ptop_AB.ports["L_gate_W"], pbottom_AB.ports["L_gate_W"],extension=pcenter_gate_route_extension)
    pcenter_r_croute = shared_gate_comps << c_route(pdk, ptop_AB.ports["R_gate_E"], pbottom_AB.ports["R_gate_E"],extension=pcenter_gate_route_extension)
    shared_gate_comps << straight_route(pdk, LRgatePorts[0], pcenter_l_croute.ports["con_N"])
    shared_gate_comps << straight_route(pdk, LRgatePorts[-1], pcenter_r_croute.ports["con_N"])
    # connect drain of A to the shorted gates
    shared_gate_comps << L_route(pdk,ptop_AB.ports["L_source_W"],pcenter_l_croute.ports["con_N"])
    shared_gate_comps << straight_route(pdk,pbottom_AB.ports["R_source_E"],pcenter_r_croute.ports["con_N"])
    # connect source of A to the drain of 2L
    pcomps_route_A_drain_extension = shared_gate_comps.xmax-max(ptop_AB.ports["R_drain_E"].center[0], LRdrainsPorts[-1].center[0])+_max_metal_seperation_ps
    pcomps_route_A_drain = shared_gate_comps << c_route(pdk, ptop_AB.ports["L_drain_W"], LRdrainsPorts[0], extension=pcomps_route_A_drain_extension)
    row_rectangle_routing = rectangle(layer=ptop_AB.ports["L_drain_W"].layer,size=(pbottom_AB.ports["R_source_N"].width,pbottom_AB.ports["R_source_W"].width)).copy()
    Aextra_top_connection = align_comp_to_port(row_rectangle_routing, pbottom_AB.ports["R_source_N"], ('c','t')).movey(row_rectangle_routing.ymax + _max_metal_seperation_ps)
    shared_gate_comps.add(Aextra_top_connection)
    shared_gate_comps << straight_route(pdk,Aextra_top_connection.ports["e4"],pbottom_AB.ports["R_drain_N"])
    shared_gate_comps << L_route(pdk,pcomps_route_A_drain.ports["con_S"], Aextra_top_connection.ports["e1"],viaoffset=(False,True))
    # connect source of B to drain of 2R
    pcomps_route_B_source_extension = shared_gate_comps.xmax-max(LRsourcesPorts[-1].center[0],ptop_AB.ports["R_source_E"].center[0])+_max_metal_seperation_ps
    mimcap_connection_ref = shared_gate_comps << c_route(pdk, ptop_AB.ports["R_source_E"], LRdrainsPorts[-1],extension=pcomps_route_B_source_extension,viaoffset=(True,False))
    bottom_pcompB_floating_port = set_port_orientation(movey(movex(pbottom_AB.ports["L_source_E"].copy(),5*_max_metal_seperation_ps), destination=Aextra_top_connection.ports["e1"].center[1]+Aextra_top_connection.ports["e1"].width+_max_metal_seperation_ps),"S")
    pmos_bsource_2Rdrain_v = shared_gate_comps << L_route(pdk,pbottom_AB.ports["L_source_E"],bottom_pcompB_floating_port,vglayer="met3")
    # fix the extension when the top row of transistors extends farther than the middle row
    if LRdrainsPorts[-1].center[0] < ptop_AB.ports["R_source_E"].center[0]:
        pcomps_route_B_source_extension += ptop_AB.ports["R_source_E"].center[0] - LRdrainsPorts[-1].center[0]
    shared_gate_comps << c_route(pdk, LRdrainsPorts[-1], set_port_orientation(bottom_pcompB_floating_port,"E"),extension=pcomps_route_B_source_extension,viaoffset=(True,False))
    pmos_bsource_2Rdrain_v_center = via_stack(pdk,"met2","met3",fulltop=True)
    shared_gate_comps.add(align_comp_to_port(pmos_bsource_2Rdrain_v_center, bottom_pcompB_floating_port,('r','t')))
    # connect drain of B to each other directly over where the diffpair top left drain will be
    pmos_bdrain_diffpair_v = shared_gate_comps << via_stack(pdk, "met2","met5",fullbottom=True)
    pmos_bdrain_diffpair_v = align_comp_to_port(pmos_bdrain_diffpair_v, movex(pbottom_AB.ports["L_gate_S"].copy(),destination=via_location))
    pmos_bdrain_diffpair_v.movey(0-_max_metal_seperation_ps)
    pcomps_route_B_drain_extension = shared_gate_comps.xmax-ptop_AB.ports["R_drain_E"].center[0]+_max_metal_seperation_ps
    shared_gate_comps << c_route(pdk, ptop_AB.ports["R_drain_E"], pmos_bdrain_diffpair_v.ports["bottom_met_E"],extension=pcomps_route_B_drain_extension +_max_metal_seperation_ps)
    shared_gate_comps << c_route(pdk, pbottom_AB.ports["L_drain_W"], pmos_bdrain_diffpair_v.ports["bottom_met_W"],extension=pcomps_route_B_drain_extension +_max_metal_seperation_ps)
    shared_gate_comps.add_ports(pmos_bdrain_diffpair_v.get_ports_list(),prefix="minusvia_")
    shared_gate_comps.add_ports(mimcap_connection_ref.get_ports_list(),prefix="mimcap_connection_")
    return shared_gate_comps

def differential_to_single_ended_converter_netlist(pdk: MappedPDK, half_pload: tuple[float, float, int]) -> Netlist:
    return Netlist(
        circuit_name="DIFF_TO_SINGLE",
        nodes=['VIN', 'VOUT', 'VSS', 'VSS2'],
        source_netlist=""".subckt {circuit_name} {nodes} """ + f'l={half_pload[1]} w={half_pload[0]} mt={4*2} mb={2 * half_pload[2]} ' + """
XTOP1 V1   VIN VSS  VSS {model} l={{l}} w={{w}} m={{mt}}
XTOP2 VSS2 VIN VSS  VSS {model} l={{l}} w={{w}} m={{mt}}
XBOT1 VIN  VIN V1   VSS {model} l={{l}} w={{w}} m={{mb}}
XBOT2 VOUT VIN VSS2 VSS {model} l={{l}} w={{w}} m={{mb}}
.ends {circuit_name}""",
        instance_format="X{name} {nodes} {circuit_name} l={length} w={width} mt={mult_top} mb={mult_bot}",
        parameters={
            'model': pdk.models['pfet'],
            'width': half_pload[0],
            'length': half_pload[1],
            'mult_top': 4 * 2,
            'mult_bot': 2 * (half_pload[2])
        }
    )

def differential_to_single_ended_converter(pdk: MappedPDK, rmult: int, half_pload: tuple[float,float,int], via_xlocation) -> Component:
    clear_cache()
    pmos_comps, ptop_AB, pbottom_AB, LRplusdopedPorts, LRgatePorts, LRdrainsPorts, LRsourcesPorts, LRdummyports = __create_sharedgatecomps(pdk, rmult,half_pload)
    clear_cache()
    pmos_comps = __route_sharedgatecomps(pdk, pmos_comps, via_xlocation, ptop_AB, pbottom_AB, LRplusdopedPorts, LRgatePorts, LRdrainsPorts, LRsourcesPorts, LRdummyports)

    pmos_comps.info['netlist'] = differential_to_single_ended_converter_netlist(pdk, half_pload)

    return pmos_comps
