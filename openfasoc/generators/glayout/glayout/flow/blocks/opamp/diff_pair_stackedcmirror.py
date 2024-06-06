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
from glayout.flow.primitives.via_gen import via_stack, via_array
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.c_route import c_route
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


@validate_arguments
def __add_diff_pair_and_bias(pdk: MappedPDK, toplevel_stacked: Component, half_diffpair_params: tuple[float, float, int], diffpair_bias: tuple[float, float, int], rmult: int, with_antenna_diode_on_diffinputs: int) -> Component:
    clear_cache()
    diffpair_i_ref = diff_pair_ibias(pdk, half_diffpair_params, diffpair_bias, rmult, with_antenna_diode_on_diffinputs)
    toplevel_stacked.add(diffpair_i_ref)
    toplevel_stacked.add_ports(diffpair_i_ref.get_ports_list(),prefix="diffpair_")

    toplevel_stacked.info['netlist'] = diffpair_i_ref.info['netlist']

    return toplevel_stacked

@validate_arguments
def __add_common_source_nbias_transistors(pdk: MappedPDK, toplevel_stacked: Component, half_common_source_nbias: tuple[float, float, int, int], rmult: int) -> Component:
    clear_cache()
    x_dim_center = toplevel_stacked.xmax
    for i in range(2):
        direction = (-1) ** i
        cmirrorref_ref, cmirrorout_ref = stacked_nfet_current_mirror(pdk, half_common_source_nbias, rmult, direction < 0)
        # xtranslation
        xtranslationO = direction * abs(x_dim_center + cmirrorout_ref.xmax + pdk.util_max_metal_seperation())
        xtranslationR = direction * abs(x_dim_center + cmirrorref_ref.xmax + pdk.util_max_metal_seperation())
        xtranslationO, xtranslationR = pdk.snap_to_2xgrid([xtranslationO, xtranslationR])
        cmirrorout_ref.movex(xtranslationO)
        cmirrorref_ref.movex(xtranslationR)
        # ytranslation
        cmirrorout_ref.movey(toplevel_stacked.ports["diffpair_bl_multiplier_0_gate_S"].center[1])
        cmirrorref_ref.movey(cmirrorout_ref.ymin - evaluate_bbox(cmirrorref_ref)[1]/2 - pdk.util_max_metal_seperation())
        # add ports
        toplevel_stacked.add(cmirrorref_ref)
        toplevel_stacked.add(cmirrorout_ref)
        side = "R" if i==0 else "L"
        toplevel_stacked.add_ports(cmirrorout_ref.get_ports_list(), prefix="commonsource_cmirror_output_"+side+"_")
        toplevel_stacked.add_ports(cmirrorref_ref.get_ports_list(), prefix="commonsource_cmirror_ref_"+side+"_")
        toplevel_stacked << straight_route(pdk, toplevel_stacked.ports["commonsource_cmirror_output_"+side+"_tie_S_top_met_S"], toplevel_stacked.ports["commonsource_cmirror_ref_"+side+"_tie_N_top_met_N"])
    return toplevel_stacked

@validate_arguments
def __route_bottom_ncomps_except_drain_nbias(pdk: MappedPDK, toplevel_stacked: Component, gndpin: Union[Component,ComponentReference], halfmultn_num_mults: int) -> tuple:
    clear_cache()
    # route diff pair cmirror
    toplevel_stacked << L_route(pdk, toplevel_stacked.ports["diffpair_ibias_purposegndport"],gndpin.ports["W"])
    # gnd diff pair substrate tap
    toplevel_stacked << straight_route(pdk, toplevel_stacked.ports["diffpair_tap_W_top_met_E"], toplevel_stacked.ports["commonsource_cmirror_output_L_tie_E_top_met_W"],width=1,glayer2="met1")
    toplevel_stacked << straight_route(pdk, toplevel_stacked.ports["diffpair_tap_E_top_met_W"], toplevel_stacked.ports["commonsource_cmirror_output_R_tie_W_top_met_E"],width=1,glayer2="met1")
    # common source
    # route to gnd the sources of cmirror
    _cref = toplevel_stacked << c_route(pdk, toplevel_stacked.ports["commonsource_cmirror_output_R_multiplier_0_source_con_S"], toplevel_stacked.ports["commonsource_cmirror_output_L_multiplier_0_source_con_S"], extension=abs(gndpin.ports["N"].center[1]-toplevel_stacked.ports["commonsource_cmirror_output_R_multiplier_0_source_con_S"].center[1]),fullbottom=True)
    toplevel_stacked << straight_route(pdk, toplevel_stacked.ports["commonsource_cmirror_ref_R_multiplier_0_source_E"],_cref.ports["con_E"],glayer2="met3",via2_alignment=('c','c'))
    toplevel_stacked << straight_route(pdk, toplevel_stacked.ports["commonsource_cmirror_ref_L_multiplier_0_source_W"],_cref.ports["con_W"],glayer2="met3",via2_alignment=('c','c'))
    # connect cmirror ref drain to cmirror output gate, then short cmirror ref drain and gate
    Ldrainport = toplevel_stacked.ports["commonsource_cmirror_ref_L_multiplier_0_drain_N"]
    Lgateport = toplevel_stacked.ports["commonsource_cmirror_output_L_multiplier_0_gate_S"]
    Rdrainport = toplevel_stacked.ports["commonsource_cmirror_ref_R_multiplier_0_drain_N"]
    Rgateport = toplevel_stacked.ports["commonsource_cmirror_output_R_multiplier_0_gate_S"]
    draintogate_L = toplevel_stacked << straight_route(pdk, Ldrainport, Lgateport, glayer1="met3",via1_alignment=('c','b'),via2_alignment=('c','t'),width=1)
    draintogate_R = toplevel_stacked << straight_route(pdk, Rdrainport, Rgateport, glayer1="met3",via1_alignment=('c','b'),via2_alignment=('c','t'),width=1)
    Lcmirrorrefgate = toplevel_stacked.ports["commonsource_cmirror_ref_L_multiplier_0_gate_E"]
    Rcmirrorrefgate = toplevel_stacked.ports["commonsource_cmirror_ref_R_multiplier_0_gate_W"]
    extension = pdk.util_max_metal_seperation()
    toplevel_stacked << c_route(pdk, toplevel_stacked.ports["commonsource_cmirror_ref_L_multiplier_0_drain_E"], Lcmirrorrefgate, extension=extension)
    toplevel_stacked << c_route(pdk, toplevel_stacked.ports["commonsource_cmirror_ref_R_multiplier_0_drain_W"], Rcmirrorrefgate, extension=extension)
    # connect gates and drains of cmirror output
    halfMultn_left_gate_port = toplevel_stacked.ports["commonsource_cmirror_output_R_multiplier_"+str(halfmultn_num_mults-2)+"_gate_con_N"]
    halfMultn_right_gate_port = toplevel_stacked.ports["commonsource_cmirror_output_L_multiplier_"+str(halfmultn_num_mults-2)+"_gate_con_N"]
    halfmultn_gate_routeref = toplevel_stacked << c_route(pdk, halfMultn_left_gate_port, halfMultn_right_gate_port, extension=abs(toplevel_stacked.ymax-halfMultn_left_gate_port.center[1])+1,fullbottom=True, viaoffset=(False,False))
    halfMultn_left_drain_port = toplevel_stacked.ports["commonsource_cmirror_output_R_multiplier_"+str(halfmultn_num_mults-2)+"_drain_con_N"]
    halfMultn_right_drain_port = toplevel_stacked.ports["commonsource_cmirror_output_L_multiplier_"+str(halfmultn_num_mults-2)+"_drain_con_N"]
    halfmultn_drain_routeref = toplevel_stacked << c_route(pdk, halfMultn_left_drain_port, halfMultn_right_drain_port, extension=abs(toplevel_stacked.ymax-halfMultn_left_drain_port.center[1])+1,fullbottom=True)
    # route to gnd the guardring of cmirror output and the diff pair cmirror ring
    toplevel_stacked << straight_route(pdk,toplevel_stacked.ports["commonsource_cmirror_ref_R_tie_S_top_met_S"],movey(gndpin.ports["W"],evaluate_bbox(gndpin)[1]/4),width=2,glayer1="met3",fullbottom=True)
    toplevel_stacked << straight_route(pdk,toplevel_stacked.ports["commonsource_cmirror_ref_L_tie_S_top_met_S"],movey(gndpin.ports["E"],evaluate_bbox(gndpin)[1]/4),width=2,glayer1="met3",fullbottom=True)
    toplevel_stacked << straight_route(pdk,toplevel_stacked.ports["commonsource_cmirror_ref_L_tie_E_top_met_E"],toplevel_stacked.ports["diffpair_ibias_welltie_W_top_met_W"])
    toplevel_stacked << straight_route(pdk,toplevel_stacked.ports["commonsource_cmirror_ref_R_tie_W_top_met_W"],toplevel_stacked.ports["diffpair_ibias_welltie_E_top_met_E"])
    # diffpair
    # route source of diffpair to drain of diffpair cmirror
    toplevel_stacked << L_route(pdk,toplevel_stacked.ports["diffpair_source_routeW_con_N"],toplevel_stacked.ports["diffpair_ibias_B_drain_W"])
    toplevel_stacked << L_route(pdk,toplevel_stacked.ports["diffpair_source_routeE_con_N"],toplevel_stacked.ports["diffpair_ibias_B_drain_E"])
    return toplevel_stacked, halfmultn_drain_routeref, halfmultn_gate_routeref, _cref


def diff_pair_stackedcmirror(
    pdk: MappedPDK,
    half_diffpair_params: tuple[float, float, int],
    diffpair_bias: tuple[float, float, int],
    half_common_source_nbias: tuple[float, float, int, int],
    rmult: int,
    with_antenna_diode_on_diffinputs: int
) -> Component:
    # create toplevel_stacked component
    toplevel_stacked = Component()
    # place nmos components
    diffpair_and_bias = __add_diff_pair_and_bias(pdk, toplevel_stacked, half_diffpair_params, diffpair_bias, rmult, with_antenna_diode_on_diffinputs)
    # create and position each half of the nmos bias transistor for the common source stage symetrically
    toplevel_stacked = __add_common_source_nbias_transistors(pdk, toplevel_stacked, half_common_source_nbias, rmult)
    toplevel_stacked.add_padding(layers=(pdk.get_glayer("pwell"),),default=0)
    # add ground pin
    gndpin = toplevel_stacked << rename_ports_by_orientation(rectangle(size=(5,3),layer=pdk.get_glayer("met4"),centered=True))
    gndpin.movey(pdk.snap_to_2xgrid(toplevel_stacked.ymin-pdk.util_max_metal_seperation()-gndpin.ymax))
    # route bottom ncomps except drain of nbias (still need to place common source pmos amp)
    toplevel_stacked, halfmultn_drain_routeref, halfmultn_gate_routeref, _cref = __route_bottom_ncomps_except_drain_nbias(pdk, toplevel_stacked, gndpin, half_common_source_nbias[3])
    toplevel_stacked.add_ports(gndpin.get_ports_list(), prefix="pin_gnd_")

    return toplevel_stacked, halfmultn_drain_routeref, halfmultn_gate_routeref, _cref
