from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
from PDK.mappedpdk import MappedPDK
from typing import Optional
from via_gen import via_array, via_stack
from guardring import ptapring
from math import ceil

# GF180
# NMOS target hieght = 2.19
# PMOS target height = 2.59
# standard hieght = 4.78


@cell
def PARTIAL_multiplier_no_diff(
    pdk: MappedPDK, width: float = 3, fingers: Optional[int] = 1
) -> Component:
    pmultiplier = Component("partial multiplier")
    if fingers == 0:
        return pmultiplier
    # create the poly gate
    length = pdk.get_grule("poly")["min_width"]
    poly_height = width + 2 * pdk.get_grule("poly", "active_diff")["overhang"]
    poly_gate_comp = rectangle(
        size=(length, poly_height), layer=pdk.get_glayer("poly"), centered=True
    )
    # figure out poly spacing s.t. metal/via does not overlap transistor
    tempviastack = via_stack(pdk, "active_diff", "met1")
    viasize = tempviastack.xmax - tempviastack.xmin
    mcon_poly_space = (
        2 * pdk.get_grule("poly", "mcon")["min_seperation"]
        + pdk.get_grule("mcon")["width"]
    )
    poly_spacing = max(viasize, mcon_poly_space)
    # create active diff to met1 vias
    sd_via_comp = via_array(pdk, "active_diff", "met1", size=(viasize, width))
    # lay poly and via arrays
    for fingernum in range(fingers + 1):
        spacing_multiplier = ((-1) ** fingernum) * ceil(fingernum / 2)
        finger_spacing = poly_spacing + length
        finger_offset = spacing_multiplier * finger_spacing
        if (fingers % 2) == 0:  # even correction
            finger_offset += 0.5 * finger_spacing
        if fingernum == fingers:  # lay leftmost via then loop is done
            left_sd_via_ref = pmultiplier << sd_via_comp
            left_sd_via_ref.movex(0.5 * finger_spacing - abs(finger_offset))
            break
        poly_gate_ref = pmultiplier << poly_gate_comp
        poly_gate_ref.movex(finger_offset)
        right_sd_via_ref = pmultiplier << sd_via_comp
        right_sd_via_ref.movex(finger_offset + 0.5 * finger_spacing)
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
    partialmult = PARTIAL_multiplier_no_diff(pdk, width=width, fingers=fingers)
    # add diffusion
    diff_dims = (
        partialmult.xmax
        - partialmult.xmin
        + 2 * pdk.get_grule("mcon", "active_diff")["min_enclosure"],
        width,
    )
    multiplier << rectangle(
        size=diff_dims, layer=pdk.get_glayer("active_diff"), centered=True
    )
    # add pplus
    pplusoh = pdk.get_grule("p+s/d", "active_diff")["min_enclosure"]
    multiplier.add_padding(layers=(pdk.get_glayer("p+s/d"),), default=pplusoh)
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
    nmos(gf180_mapped_pdk, fingers=4).show()
