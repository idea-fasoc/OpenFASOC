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

def row_csamplifier_diff_to_single_ended_converter_netlist(diff_to_single: Component) -> Netlist:
    overall_netlist = Netlist(
        circuit_name="DIFF_TO_SINGLE_CS",
        nodes=['VIN1', 'VIN2', 'VOUT', 'VSS', 'VSS2']
    )

    overall_netlist.connect_netlist(
        diff_to_single.info['netlist'],
        [('VIN', 'VIN1'), ('VOUT', 'VIN2')]
    )

    return overall_netlist

def __connect_cs_netlist(pmos_comps: Component, half_cs_pmos: Component):
    pmos_comps.info['netlist'].connect_netlist(
        half_cs_pmos.info['netlist'],
        [('D', 'VOUT'), ('S', 'VSS'), ('B', 'VSS'), ('G', 'VIN2')]
    )

def row_csamplifier_diff_to_single_ended_converter(pdk: MappedPDK, diff_to_single_ended_converter: Component, pamp_hparams, rmult) -> Component:
    pmos_comps = diff_to_single_ended_converter

    pmos_comps.info['netlist'] = row_csamplifier_diff_to_single_ended_converter_netlist(diff_to_single_ended_converter)

    x_dim_center = max(abs(pmos_comps.xmax),abs(pmos_comps.xmin))
    for direction in [-1, 1]:
        halfMultp = pmos(
            pdk,
            width=pamp_hparams[0],
            length=pamp_hparams[1],
            fingers=pamp_hparams[2],
            multipliers=pamp_hparams[3],
            with_tie=True,
            dnwell=False,
            with_substrate_tap=False,
            sd_route_left=bool(direction-1),
            rmult=rmult,
            tie_layers=("met2","met2")
        )
        halfMultp_ref = pmos_comps << halfMultp
        halfMultp_ref.movex(direction * abs(x_dim_center + halfMultp_ref.xmax+1))
        label = "L_" if direction==-1 else "R_"
        # this special marker is used to rename these ports in the opamp to commonsource_Pamp_
        pmos_comps.add_ports(halfMultp_ref.get_ports_list(),prefix="halfpspecialmarker_"+label)

        __connect_cs_netlist(pmos_comps, halfMultp)

    # add npadding and add ports
    nwellbbox = pmos_comps.extract(layers=[pdk.get_glayer("poly"),pdk.get_glayer("active_diff"),pdk.get_glayer("active_tap"), pdk.get_glayer("nwell"),pdk.get_glayer("dnwell")]).bbox
    nwellspacing = pdk.get_grule("nwell", "active_tap")["min_enclosure"]
    nwell_points = get_padding_points_cc(nwellbbox, default=nwellspacing, pdk_for_snap2xgrid=pdk)
    pmos_comps.add_polygon(nwell_points, layer=pdk.get_glayer("nwell"))
    tapcenter_rect = [(evaluate_bbox(pmos_comps)[0] + 1), (evaluate_bbox(pmos_comps)[1] + 1)]
    topptap = prec_ref_center(tapring(pdk, tapcenter_rect, "p+s/d",vertical_glayer="met2"),destination=tuple(pmos_comps.center))
    pmos_comps.add(topptap)
    pmos_comps.add_ports(topptap.get_ports_list(),prefix="top_ptap_")
    # vdd taprings of the center components
    pmos_comps << straight_route(pdk, pmos_comps.ports["ptopAB_L_welltap_W_top_met_W"],pmos_comps.ports["halfpspecialmarker_L_tie_E_top_met_N"],width=2,glayer1="met2",via1_alignment=('c','c'),fullbottom=True)
    pmos_comps << straight_route(pdk, pmos_comps.ports["ptopAB_R_welltap_E_top_met_E"],pmos_comps.ports["halfpspecialmarker_R_tie_W_top_met_N"],width=2,glayer1="met2",via1_alignment=('c','c'),fullbottom=True)
    pmos_comps << straight_route(pdk, pmos_comps.ports["pbottomAB_L_welltap_W_top_met_W"],pmos_comps.ports["halfpspecialmarker_L_tie_E_top_met_W"],width=2,glayer1="met2",via1_alignment=('c','c'),via2_alignment=('c','c'),fullbottom=True)
    pmos_comps << straight_route(pdk, pmos_comps.ports["pbottomAB_R_welltap_E_top_met_E"],pmos_comps.ports["halfpspecialmarker_R_tie_W_top_met_E"],width=2,glayer1="met2",via1_alignment=('c','c'),via2_alignment=('c','c'),fullbottom=True)
    return pmos_comps

