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
from glayout.flow.pdk.util.comp_utils import (
    evaluate_bbox,
    prec_ref_center,
    movex,
    movey,
    to_decimal,
    to_float,
    move,
    align_comp_to_port,
    get_padding_points_cc,
)
from glayout.flow.pdk.util.port_utils import (
    rename_ports_by_orientation,
    rename_ports_by_list,
    add_ports_perimeter,
    print_ports,
    set_port_orientation,
    rename_component_ports,
)
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid
from pydantic import validate_arguments
from glayout.flow.placement.two_transistor_interdigitized import two_nfet_interdigitized
from glayout.flow.spice import Netlist
from glayout.flow.blocks.current_mirror import current_mirror_netlist

def diff_pair_ibias_netlist(center_diffpair: Component, current_mirror: Component, antenna_diode: Optional[Component] = None) -> Netlist:
    netlist = Netlist(
        circuit_name="DIFFPAIR_CMIRROR_BIAS",
        nodes=['VP', 'VN', 'VDD1', 'VDD2', 'IBIAS', 'VSS', 'B']
    )

    diffpair_ref = netlist.connect_netlist(
        center_diffpair.info['netlist'],
        []
    )

    cmirror_ref = netlist.connect_netlist(
        current_mirror.info['netlist'],
        [('VREF', 'IBIAS'), ('VB', 'VSS')]
    )

    netlist.connect_subnets(
        cmirror_ref,
        diffpair_ref,
        [('VCOPY', 'VTAIL')]
    )

    if antenna_diode is not None:
        netlist.connect_netlist(
            antenna_diode.info['netlist'],
            [('D', 'VSS'), ('G', 'VSS'), ('B', 'VSS'), ('S', 'VP')]
        )

        netlist.connect_netlist(
            antenna_diode.info['netlist'],
            [('D', 'VSS'), ('G', 'VSS'), ('B', 'VSS'), ('S', 'VN')]
        )

    return netlist

@validate_arguments
def diff_pair_ibias(
    pdk: MappedPDK,
    half_diffpair_params: tuple[float, float, int],
    diffpair_bias: tuple[float, float, int],
    rmult: int,
    with_antenna_diode_on_diffinputs: int,
) -> Component:
    # create and center diffpair
    diffpair_i_ = Component("temp diffpair and current source")
    center_diffpair_comp = diff_pair(
        pdk,
        width=half_diffpair_params[0],
        length=half_diffpair_params[1],
        fingers=half_diffpair_params[2],
        rmult=rmult,
    )
    # add antenna diodes if that option was specified
    diffpair_centered_ref = prec_ref_center(center_diffpair_comp)
    diffpair_i_.add(diffpair_centered_ref)
    diffpair_i_.add_ports(diffpair_centered_ref.get_ports_list())
    antenna_diode_comp = None
    if with_antenna_diode_on_diffinputs:
        antenna_diode_comp = nmos(
            pdk,
            1,
            with_antenna_diode_on_diffinputs,
            1,
            with_dummy=False,
            with_tie=False,
            with_substrate_tap=False,
            with_dnwell=False,
            length=0.5,
            sd_route_topmet="met2",
            gate_route_topmet="met1",
        ).copy()
        antenna_diode_comp << straight_route(
            pdk,
            antenna_diode_comp.ports["multiplier_0_row0_col0_rightsd_top_met_S"],
            antenna_diode_comp.ports["multiplier_0_gate_N"],
        )
        antenna_diode_refL = diffpair_i_ << antenna_diode_comp
        antenna_diode_refR = diffpair_i_ << antenna_diode_comp
        align_comp_to_port(
            antenna_diode_refL, diffpair_i_.ports["MINUSgateroute_W_con_N"], ("r", "t")
        )
        antenna_diode_refL.movex(pdk.util_max_metal_seperation())
        align_comp_to_port(
            antenna_diode_refR, diffpair_i_.ports["MINUSgateroute_E_con_N"], ("L", "t")
        )
        antenna_diode_refR.movex(0 - pdk.util_max_metal_seperation())
        # route the antenna diodes to gnd and
        Lgndcon = diffpair_i_.ports["tap_W_top_met_N"]
        Lgndcon.layer = pdk.get_glayer("met1")
        Rgndcon = diffpair_i_.ports["tap_E_top_met_N"]
        Rgndcon.layer = pdk.get_glayer("met1")
        diffpair_i_ << L_route(
            pdk, antenna_diode_refL.ports["multiplier_0_gate_E"], Lgndcon
        )
        diffpair_i_ << L_route(
            pdk, antenna_diode_refR.ports["multiplier_0_gate_W"], Rgndcon
        )
        diffpair_i_ << straight_route(
            pdk,
            antenna_diode_refL.ports["multiplier_0_source_W"],
            diffpair_i_.ports["MINUSgateroute_W_con_N"],
        )
        diffpair_i_ << straight_route(
            pdk,
            antenna_diode_refR.ports["multiplier_0_source_W"],
            diffpair_i_.ports["PLUSgateroute_E_con_N"],
        )
    # create and position tail current source
    cmirror = two_nfet_interdigitized(
        pdk,
        width=diffpair_bias[0],
        length=diffpair_bias[1],
        numcols=diffpair_bias[2],
        with_tie=True,
        with_substrate_tap=False,
        gate_route_topmet="met3",
        sd_route_topmet="met3",
        rmult=rmult,
        tie_layers=("met2", "met2"),
    )
    # cmirror routing
    metal_sep = pdk.util_max_metal_seperation()
    gate_short = cmirror << c_route(
        pdk,
        cmirror.ports["A_gate_E"],
        cmirror.ports["B_gate_E"],
        extension=3 * metal_sep,
        viaoffset=None,
    )
    cmirror << L_route(
        pdk,
        gate_short.ports["con_N"],
        cmirror.ports["A_drain_E"],
        viaoffset=False,
        fullbottom=False,
    )
    srcshort = cmirror << c_route(
        pdk,
        cmirror.ports["A_source_W"],
        cmirror.ports["B_source_W"],
        extension=metal_sep,
        viaoffset=False,
    )
    cmirror.add_ports(srcshort.get_ports_list(), prefix="purposegndports")
    # current mirror netlist
    cmirror.info['netlist'] = current_mirror_netlist(
        pdk,
        width=diffpair_bias[0],
        length=diffpair_bias[1],
        multipliers=diffpair_bias[2]
    )

    # add cmirror
    tailcurrent_ref = diffpair_i_ << cmirror
    tailcurrent_ref.movey(
        pdk.snap_to_2xgrid(
            -0.5 * (center_diffpair_comp.ymax - center_diffpair_comp.ymin)
            - abs(tailcurrent_ref.ymax)
            - metal_sep
        )
    )
    purposegndPort = tailcurrent_ref.ports["purposegndportscon_S"].copy()
    purposegndPort.name = "ibias_purposegndport"
    diffpair_i_.add_ports([purposegndPort])
    diffpair_i_.add_ports(tailcurrent_ref.get_ports_list(), prefix="ibias_")

    diffpair_i_ref = prec_ref_center(diffpair_i_)

    diffpair_i_ref.info['netlist'] = diff_pair_ibias_netlist(center_diffpair_comp, cmirror, antenna_diode_comp)
    return diffpair_i_ref

