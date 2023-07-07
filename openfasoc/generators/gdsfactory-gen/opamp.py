#TODO: report as bug (clear_cache)
from gdsfactory.cell import cell, clear_cache
from gdsfactory.component import Component, copy
from gdsfactory.components.rectangle import rectangle
from PDK.mappedpdk import MappedPDK
from typing import Optional
from fet import nmos, pmos, multiplier
from diff_pair import diff_pair
from guardring import tapring
from mimcap import mimcap
from L_route import L_route
from c_route import c_route
from PDK.util.custom_comp_utils import rename_ports_by_orientation, rename_ports_by_list, add_ports_perimeter, print_ports, evaluate_bbox

@cell
def opamp(
    pdk: MappedPDK,
    diffpair_params: Optional[tuple[float, float, int, int]] = (6, 0, 4),
    tailcurrent_params: Optional[tuple[float, float, int, int]] = (6, 2, 4, 1),
    cmirror_hparams: Optional[tuple[float, float, int, int]] = (6, 2, 8, 3),
    cmirror_outhparams: Optional[tuple[float, float, int, int]] = (6, 2, 2, 1),
    pamp_hparams: Optional[tuple[float, float, int, int]] = (7, 1, 10, 3),
    mim_cap_size=(12, 12),
    output_amphparams: Optional[tuple[float, float, int, int]] = (5, 1, 8, 1),
) -> Component:
    """create an opamp, args:
    pdk=pdk to use
    diffpair_params = diffpair (width,length,fingers)
    tailcurrent_params = tailcurrent nmos (width,length,fingers,mults)
    cmirror_hparams = west current mirror (width,length,fingers,mults)
    cmirror_outhparams = east current mirror used to bias output fet (width,length,fingers,mults)
    pamp_hparams = pmos top component amp (width,length,fingers,mults)
    mim_cap_size = width,length of individual mim_cap
    """
    opamp_top = Component()
    # place nmos components
    # create and center diffpair
    diffpair_i_ = Component("temp diffpair and current source")
    center_diffpair_comp = diff_pair(
        pdk,
        width=diffpair_params[0],
        fingers=diffpair_params[2],
        length=1
    )
    diffpair_i_.add(center_diffpair_comp.ref_center())
    # create and position tail current source
    tailcurrent_comp = nmos(
        pdk,
        width=tailcurrent_params[0],
        length=tailcurrent_params[1],
        fingers=tailcurrent_params[2],
        multipliers=tailcurrent_params[3],
        with_tie=False,
        with_dnwell=False,
        with_substrate_tap=False,
        with_dummy=False,
    )
    tailcurrent_ref = diffpair_i_ << tailcurrent_comp
    tailcurrent_ref.movey(
        -0.5 * (center_diffpair_comp.ymax - center_diffpair_comp.ymin)
        - abs(tailcurrent_ref.ymax)
    )
    # add to opamp comp
    opamp_top.add(diffpair_i_.ref_center())
    # create and position current mirror symetrically
    x_dim_center = opamp_top.xmax
    src_gnd_port = [None,None]
    for i, dummy in enumerate([(False, True), (True, False)]):
        halfMultn = nmos(
            pdk,
            width=cmirror_hparams[0],
            length=cmirror_hparams[1],
            fingers=cmirror_hparams[2],
            multipliers=cmirror_hparams[3],
            with_tie=True,
            with_dnwell=False,
            with_substrate_tap=False,
            with_dummy=dummy,
            sd_route_left = bool(i)
        )
        halfMultn_ref = opamp_top << halfMultn
        direction = (-1) ** i
        halfMultn_ref.movex(direction * abs(x_dim_center + halfMultn_ref.xmax))
        opamp_top.add_ports(halfMultn_ref.get_ports_list(), prefix="nfet_Isrc_"+str(i)+"_")
    opamp_top.add_padding(layers=(pdk.get_glayer("pwell"),),default=0)
    opamp_top << c_route(pdk, opamp_top.ports["nfet_Isrc_0_multiplier_0_source_con_S"], opamp_top.ports["nfet_Isrc_1_multiplier_0_source_con_S"], extension=20,fullbottom=True)
    # place pmos components
    pmos_comps = Component("temp pmos section top")
    # center and position
    shared_gate_comps = Component("temp pmos shared gates")
    #TODO: report as bug
    clear_cache()
    pcompR = multiplier(pdk, "p+s/d", width=6, length=1, fingers=6, dummy=(False, True))
    pcompL = multiplier(pdk, "p+s/d", width=6, length=1, fingers=6, dummy=(True, False))
    (shared_gate_comps << pcompL).movex(-1 * pcompL.xmax - 0.1)
    (shared_gate_comps << pcompR).movex(-1 * pcompR.xmin + 0.1)
    # center
    relative_dim_comp = multiplier(
        pdk, "p+s/d", width=6, length=1, fingers=4, dummy=False
    )
    single_dim = relative_dim_comp.xmax + 0.1
    for i in [-2, -1, 1, 2]:
        dummy = False
        extra_t = 0
        if i == -2:
            dummy = [True, False]
            pcenterfourunits = multiplier(
                pdk, "p+s/d", width=6, length=1, fingers=4, dummy=dummy
            )
            extra_t = -1 * single_dim
        elif i == 2:
            dummy = [False, True]
            pcenterfourunits = multiplier(
                pdk, "p+s/d", width=6, length=1, fingers=4, dummy=dummy
            )
            extra_t = single_dim
        else:
            pcenterfourunits = relative_dim_comp
        (pmos_comps << pcenterfourunits).movex(i * single_dim + extra_t)
    ytranslation_pcenter = 2 * pcenterfourunits.ymax
    (pmos_comps << shared_gate_comps).movey(ytranslation_pcenter)
    (pmos_comps << shared_gate_comps).movey(-1 * ytranslation_pcenter)
    shared_gate_comps.show()
    pmos_comps.show()
    # pcore to output
    x_dim_center = pmos_comps.xmax
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
            sd_route_left=bool(direction-1)
        )
        halfMultp_ref = pmos_comps << halfMultp
        halfMultp_ref.movex(direction * abs(x_dim_center + halfMultp_ref.xmax+1))
    # finish place central
    ydim_ncomps = opamp_top.ymax - opamp_top.ymin
    pmos_comps.add_padding(
        layers=[pdk.get_glayer("nwell")],
        default=pdk.get_grule("nwell", "active_tap")["min_enclosure"],
    )
    # tapcenter_rect = [2*pmos_comps.xmax+pdk.get_grule("nwell","active_tap")["min_separation"], 2*pmos_comps.ymax+pdk.get_grule("nwell","active_tap")["min_separation"]]
    tapcenter_rect = [2 * pmos_comps.xmax + 1, 2 * pmos_comps.ymax + 1]
    pmos_comps << tapring(pdk, tapcenter_rect, "p+s/d")
    pmos_comps_ref = opamp_top << pmos_comps
    pmos_comps_ref.movey(ydim_ncomps + pmos_comps_ref.ymax)
    # place mimcaps
    mimcap_single = mimcap(pdk, mim_cap_size)
    prev_xmax = opamp_top.xmax
    center_xmax = opamp_top.xmax + mimcap_single.xmax
    mimcap_space = (
        pdk.get_grule("capmet")["min_separation"]
        + evaluate_bbox(mimcap_single)[0]
    )
    # TODO: fix glayer should be capmet + 1, size should be standardized
    h_mimcap_spacer = rectangle(size=(1,pdk.get_grule("capmet")["min_separation"]+2),layer=pdk.get_glayer("met5"),centered=True)
    v_mimcap_spacer = rectangle(size=(pdk.get_grule("capmet")["min_separation"]+2,1),layer=pdk.get_glayer("met5"),centered=True)
    mimcaps_ref = opamp_top.add_array(
        mimcap_single, rows=3, columns=2, spacing=(mimcap_space, mimcap_space)
    )
    spacing_factory_h = [dim + evaluate_bbox(h_mimcap_spacer)[1] for dim in evaluate_bbox(mimcap_single)]
    mimcap_hspacer = opamp_top.add_array(h_mimcap_spacer,rows=2,columns=2,spacing=spacing_factory_h)
    mimcap_vspacer = opamp_top.add_array(v_mimcap_spacer, rows=3,columns=1,spacing=spacing_factory_h)
    # TODO: fix mimcap to transistor separation
    displace_fact = 4 * pdk.get_grule("met5")["min_separation"]
    mimcaps_ref.movex(center_xmax + displace_fact)
    mimcap_hspacer.movex(center_xmax + displace_fact)
    mimcap_vspacer.movex(center_xmax + displace_fact + mimcap_single.xmax)
    mimcaps_ref.movey(pmos_comps_ref.ymin + mimcap_single.ymax)
    mimcap_hspacer.movey(pmos_comps_ref.ymin + 2*mimcap_single.ymax)
    mimcap_vspacer.movey(pmos_comps_ref.ymin + mimcap_single.ymax)
    # TODO: implement
    return opamp_top


if __name__ == "__main__":
    from PDK.util.standard_main import pdk

    opamp(pdk).show()
