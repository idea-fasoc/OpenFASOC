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


@validate_arguments
def stacked_nfet_current_mirror(pdk: MappedPDK, half_common_source_nbias: tuple[float, float, int, int], rmult: int, sd_route_left: bool) -> Component:
    cmirror_output = nmos(
        pdk,
        width=half_common_source_nbias[0],
        length=half_common_source_nbias[1],
        fingers=half_common_source_nbias[2],
        multipliers=half_common_source_nbias[3],
        with_tie=True,
        with_dnwell=False,
        with_substrate_tap=False,
        with_dummy=True,
        sd_route_left = sd_route_left,
        rmult=rmult,
        tie_layers=("met2","met2")
    )
    cmirrorref = nmos(
        pdk,
        width=half_common_source_nbias[0],
        length=half_common_source_nbias[1],
        fingers=half_common_source_nbias[2],
        multipliers=1,
        with_tie=True,
        with_dnwell=False,
        with_substrate_tap=False,
        with_dummy=True,
        sd_route_left = sd_route_left,
        rmult=rmult,
        tie_layers=("met2","met2")
    )
    cmirrorref_ref = prec_ref_center(cmirrorref)
    cmirrorout_ref = prec_ref_center(cmirror_output)
    return cmirrorref_ref, cmirrorout_ref

