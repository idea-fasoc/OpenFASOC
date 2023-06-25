from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle

from typing import Optional
from via_gen import via_stack
from guardring import ptapring

# GF180
# NMOS target hieght = 2.19
# PMOS target height = 2.59
# standard hieght = 4.78


@cell
def PARTIALsingle_multiplier_gen_no_diff(
    pdk, width: float = 3, fingers: Optional[int] = 1
) -> Component:
    pmultiplier = Component("partial multiplier")
    if fingers==0:
        return pmultiplier
    # create the poly gate
    length = pdk.get_grule("poly")["min_width"]
    poly_height = width + 2 * pdk.get_grule("poly", "active_diff")["overhang"]
    poly_gate_comp = rectangle(
        size=(length, poly_height), layer=pdk.get_glayer("poly"), centered=True
    )
    # create active diff to met1 vias
    sd_via_comp = Component("temp via array")
    # TODO: implement sd_via_comp as via array
    sd_via_comp << via_stack(pdk, "active_diff", "met1")
    # figure out poly spacing s.t. metal does not overlap transistor
    viasize = sd_via_comp.xmax - sd_via_comp.xmin
    mcon_poly_space = (
        2 * pdk.get_grule("poly", "mcon")["min_seperation"]
        + pdk.get_grule("mcon")["width"]
    )
    poly_spacing = max(viasize, mcon_poly_space)
    # lay poly for all fingers
    if fingers % 2:  # odd number of fingers
        pmultiplier << poly_gate_comp  # center poly
        sd_via_refr = pmultiplier << sd_via_comp
        sd_via_refr.movex(0.5 * (length + poly_spacing))
        sd_via_refl = pmultiplier << sd_via_comp
        sd_via_refl.movex(-0.5 * (length + poly_spacing))
        for fingermirror_num in range(int(fingers / 2)):
            f_offset_ = fingermirror_num * (poly_spacing + length)
            poly_gate_refr = pmultiplier << poly_gate_comp
            poly_gate_refr.movex(f_offset_ + length + poly_spacing)
            poly_gate_refl = pmultiplier << poly_gate_comp
            poly_gate_refl.movex(-1 * (f_offset_ + length + poly_spacing))
            f_offset_ += poly_spacing + length
            sd_via_refr = pmultiplier << sd_via_comp
            sd_via_refr.movex(0.5 * (length + poly_spacing) + f_offset_)
            sd_via_refl = pmultiplier << sd_via_comp
            sd_via_refl.movex(-0.5 * (length + poly_spacing) - f_offset_)
    else:
        mirror_pmult = Component("half partial multiplier")
        mirror_pmult << poly_gate_comp
    return pmultiplier.flatten()


@cell
def nmos(
    pdk,
    width: float = 3,
    fingers: Optional[int] = 1,
    multiplier: Optional[int] = 1,
    with_tie: Optional[bool] = True,
    with_dummy: Optional[bool] = True,
):
    """Generic NMOS generator: uses minumum length without deep nwell
    width = expands the NMOS in the y direction
    fingers = introduces additional fingers (sharing source/drain) of width=width
    with_tie = true or false, specfies if a bulk tie is required
    """
    if width < pdk.get_grule("active_diff")["min_width"]:
        raise ValueError("transistor min width violated")
    # TODO: glayer checks
    pdk.activate()
    # 1) create one multiplier
    # 2) multiplier.movey up then reflect the multiplier across the x axis
    # 3) make sure all multipliers are on component then use bbox to place tie ring around nfet
    # 4) place pwell
    # 5) place dnwell
    # 6) place tap ring

    # create a single multiplier
    multiplier = Component("temp multiplier")
    partialmult = PARTIALsingle_multiplier_gen_no_diff(
        pdk, width=width, fingers=fingers
    )

    diff_dims = (
        partialmult.xmax
        - partialmult.xmin
        + 2 * pdk.get_grule("poly", "active_diff")["overhang"],
        width,
    )
    # TODO: revise ruleset for active__diff, default=pdk.get_grule("active_tap","p+s/d")["min_enclosure"]
    # .add_padding(layers=(pdk.get_glayer("p+s/d")),default=pdk.get_grule("active_tap","p+s/d")["min_enclosure"])
    multiplier << rectangle(
        size=diff_dims, layer=pdk.get_glayer("active_diff"), centered=True
    )
    # multiplier.add_padding(layers=(pdk.get_glayer("p+s/d")),default=pdk.get_grule("poly","active_diff")["overhang"])
    multiplier.add_padding(layers=(pdk.get_glayer("p+s/d")), default=0.1)
    multiplier << partialmult
    return multiplier.flatten()


# @cell
# def pmos(pdk: MappedPDK, width: float, fingers = Optional[int] = 1, with_tie: Optional[bool] = False):
# 	"""Generic PMOS generator: uses minumum length
# 	width = expands the PMOS in the y direction
# 	fingers = introduces additional fingers (sharing source/drain) of width=width
# 	with_tie = true or false, specfies if a bulk tie is required
# 	"""
# 	return

if __name__ == "__main__":
    from PDK.gf180_mapped import gf180_mapped_pdk

    gf180_mapped_pdk.activate()
    nmos(gf180_mapped_pdk, fingers=5).show()
