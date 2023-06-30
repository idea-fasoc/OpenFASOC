from gdsfactory.cell import cell
from gdsfactory.component import Component, copy
from gdsfactory.components.rectangle import rectangle
from PDK.mappedpdk import MappedPDK
from typing import Optional
from fet import nmos, pmos, multiplier
from diff_pair import diff_pair
from guardring import tapring


@cell
def opamp(
    pdk: MappedPDK,
    diffpair_params: Optional[tuple[float, float, int, int]] = (6, 0, 4, 2),
    tailcurrent_params: Optional[tuple[float, float, int, int]] = (6, 2, 4, 1),
    cmirror_hparams: Optional[tuple[float, float, int, int]] = (6, 2, 8, 3),
    pamp_hparams: Optional[tuple[float, float, int, int]] = (7, 1, 10, 3),
) -> Component:
    """create an opamp, args:
    pdk=pdk to use
    diffpair_params = diffpair (width,length,fingers,mults)
    tailcurrent_params = tailcurrent nmos (width,length,fingers,mults)
    cmirror_hparams = cmirror_hparams (width,length,fingers,mults)
    """
    opamp_top = Component()
    # place nmos components
    # create and center diffpair
    diffpair_i_ = Component("temp diffpair and current source")
    center_diffpair_comp = diff_pair(
        pdk,
        cell_height=diffpair_params[0],
        fingers=diffpair_params[2],
        mult=diffpair_params[3],
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
    # create tap ring
    # tapcenter_rect = [2*opamp_top.xmax, 2*opamp_top.ymax]
    # opamp_top << tapring(pdk, tapcenter_rect, "p+s/d")
    # create and position current mirror symetrically
    x_dim_center = opamp_top.xmax
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
        )
        halfMultn_ref = opamp_top << halfMultn
        direction = (-1) ** i
        halfMultn_ref.movex(direction * abs(x_dim_center + halfMultn_ref.xmax))
    # place pmos components
    pmos_comps = Component("temp pmos section top")
    # center and position
    shared_gate_comps = Component("temp pmos shared gates")
    pcompL = multiplier(pdk, "p+s/d", width=6, length=1, fingers=6, dummy=(True, False))
    pcompR = multiplier(pdk, "p+s/d", width=6, length=1, fingers=6, dummy=(False, True))
    (shared_gate_comps << pcompL).movex(-1 * pcompL.xmax)
    (shared_gate_comps << pcompR).movex(-1 * pcompR.xmin)
    # center
    relative_dim_comp = multiplier(
        pdk, "p+s/d", width=6, length=1, fingers=4, dummy=False
    )
    single_dim = relative_dim_comp.xmax
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
        )
        halfMultp_ref = pmos_comps << halfMultp
        halfMultp_ref.movex(direction * abs(x_dim_center + halfMultp_ref.xmax))
    # finish place
    ydim_ncomps = opamp_top.ymax - opamp_top.ymin
    pmos_comps_ref = opamp_top << pmos_comps
    pmos_comps_ref.movey(ydim_ncomps + pmos_comps_ref.ymax)
    # route
    # TODO: implement
    return opamp_top


if __name__ == "__main__":
    from PDK.util.standard_main import pdk

    opamp(pdk).show()
