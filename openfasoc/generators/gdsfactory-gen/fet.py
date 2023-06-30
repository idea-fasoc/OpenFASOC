from gdsfactory.cell import cell
from gdsfactory.component import Component, copy
from gdsfactory.components.rectangle import rectangle
from PDK.mappedpdk import MappedPDK
from typing import Optional
from via_gen import via_array, via_stack
from guardring import tapring
from pydantic import validate_arguments


@cell
def multiplier(
    pdk: MappedPDK,
    sdlayer: str,
    width: Optional[float] = 3,
    fingers: Optional[int] = 1,
    routing: Optional[bool] = True,
    dummy: Optional[bool] = True,
) -> Component:
    # error checking
    if "+s/d" not in sdlayer:
        raise ValueError("specify + doped region for multiplier")
    multiplier = Component()
    if fingers == 0:
        return multiplier
    # create the poly gate
    length = pdk.get_grule("poly")["min_width"]
    poly_overhang = pdk.get_grule("poly", "active_diff")["overhang"]
    poly_height = width + 2 * poly_overhang
    routing_pfac = pdk.get_grule("met1")["min_separation"] if routing else 0
    poly_height += routing_pfac
    poly_gate_comp = Component("temp poly gate")
    tempref = poly_gate_comp << rectangle(
        size=(length, poly_height), layer=pdk.get_glayer("poly"), centered=True
    )
    tempref.movey(-0.5 * routing_pfac)
    # figure out poly spacing s.t. metal/via does not overlap transistor
    tempviastack = via_stack(pdk, "active_diff", "met1")
    viasize = tempviastack.xmax - tempviastack.xmin
    mcon_poly_space = (
        2 * pdk.get_grule("poly", "mcon")["min_separation"]
        + pdk.get_grule("mcon")["width"]
    )
    poly_spacing = max(viasize, mcon_poly_space)
    # create a single finger
    finger = Component("temp finger comp")
    finger << poly_gate_comp
    routing_mfac = pdk.get_grule("met1")["min_separation"] if routing else 0
    vwidth = width + routing_mfac
    sd_via_comp = via_array(pdk, "active_diff", "met1", size=(viasize, vwidth))
    sd_via_ref_arr = finger << sd_via_comp
    finger_dim = poly_spacing + max(length, pdk.get_grule("met1")["min_separation"])
    sd_via_ref_arr.movex(finger_dim / 2).movey(routing_mfac / 2)
    # create finger array and add to multiplier
    fingerarray = Component("temp finger array")
    fingerarray.add_array(finger, columns=fingers, rows=1, spacing=(finger_dim, 1))
    sd_via_ref_left = fingerarray << sd_via_comp
    sd_via_ref_left.movex(-0.5 * finger_dim).movey(routing_mfac / 2)
    fingerarray_ref = multiplier << fingerarray
    offset = (fingers - 1) * finger_dim * 0.5
    fingerarray_ref.movex(-1 * offset)
    # create diffusion and +doped region
    diff_dims = (
        multiplier.xmax
        - multiplier.xmin
        + 2 * pdk.get_grule("mcon", "active_diff")["min_enclosure"],
        width,
    )
    diff_area = copy(
        rectangle(size=diff_dims, layer=pdk.get_glayer("active_diff"), centered=True)
    )
    sd_ovhg = pdk.get_grule(sdlayer, "active_diff")["min_enclosure"]
    diff_area.add_padding(layers=(pdk.get_glayer(sdlayer),), default=sd_ovhg)
    multiplier << diff_area
    # route all drains/ gates/ sources
    if routing:
        if fingers == 1:
            raise NotImplementedError("fingers=1 not supported for routing")
        # create sdvia (need dims)
        sdvia = via_stack(pdk, "met1", "met2")
        # TODO: fix poly overhang / met1 separation
        extracted_gates = multiplier.extract([pdk.get_glayer("poly")])
        gate_route_width = (
            pdk.get_grule("mcon")["width"]
            + 2 * pdk.get_grule("poly", "mcon")["min_enclosure"]
        )
        gate_route_length = extracted_gates.xmax - extracted_gates.xmin
        routedims = [gate_route_length, gate_route_width]
        gate_route = copy(
            rectangle(size=routedims, layer=pdk.get_glayer("poly"), centered=True)
        )
        routedims[1] = 2 * via_stack(pdk, "poly", "met2").ymax
        gate_route << via_array(pdk, "poly", "met2", size=routedims)
        gate_route_ref = multiplier << gate_route
        gate_route_ref.movey(-0.5 * (poly_height + gate_route_width + routing_pfac))
        # source and drain routing
        sw_corner_os = [
            fingerarray_ref.xmin + viasize / 2,
            fingerarray_ref.parent.extract([pdk.get_glayer("met1")]).ymax
            + sdvia.extract([pdk.get_glayer("met1")]).ymax,
        ]
        for finger in range(fingers + 1):
            sdrouting = Component("temp routing comp")
            sdrouting << sdvia
            doffset_met1 = 0
            if finger % 2:
                doffset_met1 = sdvia.ymax - sdvia.extract([pdk.get_glayer("met1")]).ymax
                doffset = (2 * sdvia.ymax) + pdk.get_grule("met2")["min_separation"]
                extendm = sdrouting << rectangle(
                    size=(viasize, doffset + doffset_met1),
                    centered=True,
                    layer=pdk.get_glayer("met1"),
                )
                extendm.movey(-0.5 * doffset - sdvia.ymax + doffset_met1 / 2)
            sdrouting_ref = multiplier << sdrouting
            sdrouting_ref.move(destination=(sw_corner_os))
            if finger % 2:
                sdrouting_ref.movey(extendm.ymax - extendm.ymin)
            sw_corner_os[0] += finger_dim
        met2_ext = multiplier.extract([pdk.get_glayer("met2")])
        met2route_dims = (met2_ext.xmax - met2_ext.xmin, 2 * sdvia.ymax)
        sd_met2_connect = rectangle(
            layer=pdk.get_glayer("met2"), size=met2route_dims, centered=True
        )
        for m2offset in [sw_corner_os[1], met2_ext.ymax - sdvia.ymax]:
            m2ref = multiplier << sd_met2_connect
            m2ref.movey(m2offset)
    if dummy:
        dummy = Component("temp dummy region")
        size = (pdk.get_grule("active_diff")["min_width"], width)
        dummy << rectangle(
            layer=pdk.get_glayer("active_diff"), size=size, centered=True
        )
        dummy_space = pdk.get_grule(sdlayer, "active_diff")["min_enclosure"]
        dummy.add_padding(layers=(pdk.get_glayer(sdlayer),), default=dummy_space)
        dummy_space += pdk.get_grule(sdlayer)["min_separation"] + size[0] / 2
        for side in [-1, 1]:
            dummy_ref = multiplier << dummy
            dummy_ref.movex(side * (dummy_space + multiplier.xmax))
    return multiplier.flatten()


@validate_arguments
def __mult_array_macro(
    pdk: MappedPDK,
    sdlayer: str,
    width: Optional[float] = 3,
    fingers: Optional[int] = 1,
    multipliers: Optional[int] = 1,
    routing: Optional[bool] = True,
    dummy: Optional[bool] = True,
) -> Component:
    # create multiplier array
    pdk.activate()
    # TODO: error checking
    multiplier_arr = Component("temp multiplier array")
    multiplier_comp = multiplier(
        pdk, sdlayer, width=width, fingers=fingers, dummy=dummy, routing=routing
    )
    multiplier_separation = (
        pdk.get_grule("met2")["min_separation"]
        + multiplier_comp.ymax
        - multiplier_comp.ymin
    )
    multiplier_arr.add_array(
        multiplier_comp, columns=1, rows=multipliers, spacing=(1, multiplier_separation)
    )
    return multiplier_arr


@cell
def nmos(
    pdk,
    width: float = 3,
    fingers: Optional[int] = 1,
    multipliers: Optional[int] = 1,
    with_tie: Optional[bool] = True,
    with_dummy: Optional[bool] = True,
    with_dnwell: Optional[bool] = True,
    with_substrate_tap: Optional[bool] = True,
) -> Component:
    """Generic NMOS generator: uses minumum length without deep nwell
    width = expands the NMOS in the y direction
    fingers = introduces additional fingers (sharing source/drain) of width=width
    with_tie = true or false, specfies if a bulk tie is required
    """
    if width < pdk.get_grule("active_diff")["min_width"]:
        raise ValueError("transistor min width violated")
    # TODO: glayer checks
    pdk.activate()
    nfet = Component()
    # create and add multipliers to nfet
    multiplier_arr = __mult_array_macro(
        pdk, "n+s/d", width, fingers, multipliers, dummy=with_dummy
    )
    nfet.add(multiplier_arr.ref_center())
    # add tie if tie
    if with_tie:
        tap_separation = max(
            pdk.get_grule("met2")["min_separation"],
            pdk.get_grule("met1")["min_separation"],
            pdk.get_grule("active_diff", "active_tap")["min_separation"],
        )
        tap_separation += pdk.get_grule("p+s/d", "active_tap")["min_enclosure"]
        tap_encloses = (
            2 * (tap_separation + nfet.xmax),
            2 * (tap_separation + nfet.ymax),
        )
        nfet << tapring(
            pdk,
            enclosed_rectangle=tap_encloses,
            sdlayer="p+s/d",
            horizontal_glayer="met2",
            vertical_glayer="met1",
        )
    # add pwell
    nfet.add_padding(
        layers=(pdk.get_glayer("pwell"),),
        default=pdk.get_grule("pwell", "active_tap")["min_enclosure"],
    )
    # add dnwell if dnwell
    if with_dnwell:
        nfet.add_padding(
            layers=(pdk.get_glayer("dnwell"),),
            default=pdk.get_grule("pwell", "dnwell")["min_enclosure"],
        )
    # add substrate tap if with_substrate_tap
    if with_substrate_tap:
        substrate_tap_separation = pdk.get_grule("dnwell", "active_tap")[
            "min_separation"
        ]
        substrate_tap_encloses = (
            2 * (substrate_tap_separation + nfet.xmax),
            2 * (substrate_tap_separation + nfet.ymax),
        )
        nfet << tapring(
            pdk,
            enclosed_rectangle=substrate_tap_encloses,
            sdlayer="p+s/d",
            horizontal_glayer="met2",
            vertical_glayer="met1",
        )
    return nfet.flatten()


@cell
def pmos(
    pdk,
    width: float = 3,
    fingers: Optional[int] = 1,
    multipliers: Optional[int] = 1,
    with_tie: Optional[bool] = True,
    dnwell: Optional[bool] = False,
    with_dummy: Optional[bool] = True,
    with_substrate_tap: Optional[bool] = True,
) -> Component:
    """Generic NMOS generator: uses minumum length without deep nwell
    width = expands the NMOS in the y direction
    fingers = introduces additional fingers (sharing source/drain) of width=width
    with_tie = true or false, specfies if a bulk tie is required
    """
    if width < pdk.get_grule("active_diff")["min_width"]:
        raise ValueError("transistor min width violated")
    # TODO: glayer checks
    pdk.activate()
    pfet = Component()
    # create and add multipliers to nfet
    multiplier_arr = __mult_array_macro(
        pdk, "p+s/d", width, fingers, multipliers, dummy=with_dummy
    )
    pfet.add(multiplier_arr.ref_center())
    # add tie if tie
    if with_tie:
        tap_separation = max(
            pdk.get_grule("met2")["min_separation"],
            pdk.get_grule("met1")["min_separation"],
            pdk.get_grule("active_diff", "active_tap")["min_separation"],
        )
        tap_separation += pdk.get_grule("n+s/d", "active_tap")["min_enclosure"]
        tap_encloses = (
            2 * (tap_separation + pfet.xmax),
            2 * (tap_separation + pfet.ymax),
        )
        pfet << tapring(
            pdk,
            enclosed_rectangle=tap_encloses,
            sdlayer="n+s/d",
            horizontal_glayer="met2",
            vertical_glayer="met1",
        )
    # add nwell
    nwell_glayer = "dnwell" if dnwell else "nwell"
    nwell_layer = pdk.get_glayer(nwell_glayer)
    pfet.add_padding(
        layers=(nwell_layer,),
        default=pdk.get_grule("active_tap", nwell_glayer)["min_enclosure"],
    )
    # add substrate tap if with_substrate_tap
    if with_substrate_tap:
        substrate_tap_separation = pdk.get_grule("dnwell", "active_tap")[
            "min_separation"
        ]
        substrate_tap_encloses = (
            2 * (substrate_tap_separation + pfet.xmax),
            2 * (substrate_tap_separation + pfet.ymax),
        )
        pfet << tapring(
            pdk,
            enclosed_rectangle=substrate_tap_encloses,
            sdlayer="p+s/d",
            horizontal_glayer="met2",
            vertical_glayer="met1",
        )
    return pfet.flatten()


if __name__ == "__main__":
    from PDK.util.standard_main import pdk

    pmos(pdk, fingers=3).show()
