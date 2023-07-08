from gdsfactory.grid import grid
from gdsfactory.cell import cell
from gdsfactory.component import Component, copy
from gdsfactory.components.rectangle import rectangle
from PDK.mappedpdk import MappedPDK
from typing import Optional, Union
from via_gen import via_array, via_stack
from guardring import tapring
from pydantic import validate_arguments
from PDK.util.custom_comp_utils import rename_ports_by_orientation, rename_ports_by_list, add_ports_perimeter, print_ports, evaluate_bbox, to_float, to_decimal, prec_array, prec_center
from c_route import c_route
from PDK.util.snap_to_grid import component_snap_to_grid
from decimal import Decimal


@cell
def multiplier(
    pdk: MappedPDK,
    sdlayer: str,
    width: Optional[float] = 3,
    fingers: Optional[int] = 1,
    routing: Optional[bool] = True,
    dummy: Optional[Union[bool, tuple[bool, bool]]] = True,
    length: Optional[float] = None,
    sd_route_topmet: Optional[str] = "met2",
    gate_route_topmet: Optional[str] = "met2"
) -> Component:
    """Generic poly/sd vias generator
    args:
    pdk = pdk to use
    sdlayer = either p+s/d for pmos or n+s/d for nmos
    width = expands the transistor in the y direction
    fingers = introduces additional fingers (sharing s/d) of width=width
    routing = true or false, specfies if sd should be connected
    dummy = true or false add dummy active/plus doped regions
    length = transitor length (if left None defaults to min length)
    ports (one port for each edge):
    gate_... all edges (top met route of gate connection)
    source_...all edges (top met route of source connections)
    drain_...all edges (top met route of drain connections)
    """
    # error checking
    if "+s/d" not in sdlayer:
        raise ValueError("specify + doped region for multiplier")
    if not "met" in sd_route_topmet or not "met" in gate_route_topmet:
        raise ValueError("topmet specified must be metal layer")
    multiplier = Component()
    if fingers == 0:
        return multiplier
    # create the poly gate
    length = length or pdk.get_grule("poly")["min_width"]
    length = Decimal(str(length))
    poly_overhang = Decimal(str(pdk.get_grule("poly", "active_diff")["overhang"]))
    width = Decimal(str(width))
    poly_height = width + 2 * poly_overhang
    routing_pfac = Decimal(str(max(pdk.get_grule("met1")["min_separation"],pdk.get_grule("met2")["min_separation"]) if routing else 0))
    poly_height += routing_pfac
    poly_gate_comp = Component("temp poly gate")
    tempref = poly_gate_comp << rectangle(
        size=to_float((length, poly_height)), layer=pdk.get_glayer("poly"), centered=True
    )
    tempref.movey(float(0-routing_pfac/2))
    # figure out poly spacing s.t. metal/via does not overlap transistor
    tempviastack = via_stack(pdk, "active_diff", "met1")
    viasize = evaluate_bbox(tempviastack,True)[0]
    mcon_poly_space = (
        2 * Decimal(str(pdk.get_grule("poly", "mcon")["min_separation"]))
        + Decimal(str(pdk.get_grule("mcon")["width"]))
    )
    poly_spacing = max(viasize, mcon_poly_space)
    # create a single finger
    finger = Component("temp finger comp")
    finger << poly_gate_comp
    routing_mfac = Decimal(str(pdk.get_grule("met1")["min_separation"] if routing else 0))
    vwidth = width + routing_mfac
    sd_via_comp = via_array(pdk, "active_diff", "met1", size=to_float((viasize, vwidth)), minus1=True)
    sd_via_ref_arr = finger << sd_via_comp
    finger_dim = poly_spacing + max(length, Decimal(str(pdk.get_grule("met1")["min_separation"])))
    sd_via_ref_arr.movex(to_float(finger_dim / 2)).movey(to_float(routing_mfac / 2))
    # create finger array and add to multiplier
    fingerarray = Component("temp finger array")
    fingerarray = prec_array(finger, columns=fingers, rows=1, spacing=(finger_dim, 1))
    sd_via_ref_left = fingerarray << sd_via_comp
    sd_via_ref_left.movex(to_float(0-finger_dim/2)).movey(to_float(routing_mfac / 2))
    fingerarray = component_snap_to_grid(fingerarray)
    fingerarray_ref = multiplier << fingerarray
    offset = (fingers - 1) * finger_dim / 2
    fingerarray_ref.movex(to_float(-1 * offset))
    # create diffusion and +doped region
    diff_dims = (
        evaluate_bbox(multiplier,True)[0]
        + 2 * Decimal(str(pdk.get_grule("mcon", "active_diff")["min_enclosure"])),
        width,
    )
    multiplier << rectangle(size=to_float(diff_dims), layer=pdk.get_glayer("active_diff"), centered=True)
    sd_ovhg = Decimal(str(pdk.get_grule(sdlayer, "active_diff")["min_enclosure"]))
    sd_ovhg_dims = [dim + sd_ovhg for dim in diff_dims]
    sdlayer_ref = multiplier << rectangle(layer=pdk.get_glayer(sdlayer), size=to_float(sd_ovhg_dims), centered=True)
    multiplier.add_ports(sdlayer_ref.get_ports_list(),prefix="plusdoped_")
    # route all drains/ gates/ sources
    if routing:
        if fingers == 1:
            raise NotImplementedError("fingers=1 not supported for routing")
        # create sdvia (need dims)
        sdvia = via_stack(pdk, "met1", sd_route_topmet)
        # TODO: fix poly overhang / met1 separation
        extracted_gates = multiplier.extract([pdk.get_glayer("poly")])
        gate_route_width = (
            Decimal(str(pdk.get_grule("mcon")["width"]))
            + 2 * Decimal(str(pdk.get_grule("poly", "mcon")["min_enclosure"]))
        )
        gate_route_length = evaluate_bbox(extracted_gates,True)[0]
        routedims = [gate_route_length, gate_route_width]
        gate_route = Component("gate route")
        gate_route << rectangle(size=to_float(routedims), layer=pdk.get_glayer("poly"), centered=True)
        routedims[1] = 2 * Decimal(str(via_stack(pdk, "poly", gate_route_topmet).ymax))
        va_ref_ = gate_route << via_array(pdk, "poly", gate_route_topmet, size=to_float(routedims))
        gate_route.add_ports([_p for _p in va_ref_.get_ports_list() if "top_met" in _p.name])
        gate_route_ref = multiplier << gate_route
        gate_route_ref.movey(float(0-(poly_height + gate_route_width + routing_pfac)/2))
        multiplier.add_ports(gate_route_ref.get_ports_list(), prefix="gate_")
        # source and drain routing
        sdtop_coords = [ Decimal(str(fingerarray_ref.xmin)) + viasize / 2,
            Decimal(str(fingerarray_ref.parent.extract([pdk.get_glayer("met1")]).ymax))]
        sd_offsets = list()
        for finger in range(fingers + 1):
            # extend the source drain connection to acamodate via
            met1_core_size = Decimal(str(sdvia.extract([pdk.get_glayer("met1")]).ymax))
            extendm_length = Decimal(str(sdvia.ymax)) + met1_core_size
            if finger % 2:
                top_met_seperation = Decimal(str(pdk.get_grule(sd_route_topmet)["min_separation"])) + Decimal(str(0.1))
                extendm_length += 2*Decimal(str(sdvia.ymax)) + top_met_seperation
                extendm = multiplier << rectangle(
                    size=to_float((viasize, extendm_length)),
                    layer=pdk.get_glayer("met1"),
                )
            else:
                extendm = multiplier << rectangle(size=to_float((viasize, extendm_length)), layer=pdk.get_glayer("met1"))
            extendm.move(destination=to_float(sdtop_coords)).movex(to_float(0-viasize/2))
            # create the via between s/d connection and s/d route
            sdvia_ref = multiplier << sdvia
            sdvia_ref.move(destination=to_float(sdtop_coords))
            sdvia_ref.movey(to_float(extendm_length - met1_core_size))
            sdtop_coords[0] += finger_dim
            extendm_length += sdtop_coords[1] - met1_core_size
            sd_offsets += [extendm_length] if len(sd_offsets) < 2 else []
        mett_ext = multiplier.extract([pdk.get_glayer(sd_route_topmet)])
        mettroute_dims = (evaluate_bbox(mett_ext,True)[0], 2 * Decimal(str(sdvia.ymax)))
        sd_mett_connect = rectangle(
            layer=pdk.get_glayer(sd_route_topmet), size=to_float(mettroute_dims), centered=True
        )
        prefix = ["source_", "drain_"]
        for i, mof in enumerate(sd_offsets):
            m2ref = (multiplier << sd_mett_connect).movey(to_float(mof))
            multiplier.add_ports(m2ref.get_ports_list(), prefix=prefix[i])
    # create dummy regions
    if isinstance(dummy, bool):
        dummyl = dummyr = dummy
    else:
        dummyl, dummyr = dummy
    if dummyl or dummyr:
        dummy = Component("temp dummy region")
        size = (length, width)
        dummy << rectangle(
            layer=pdk.get_glayer("active_diff"), size=to_float(size), centered=True
        )
        dummy_space = pdk.get_grule(sdlayer, "active_diff")["min_enclosure"]
        dummy.add_padding(layers=(pdk.get_glayer(sdlayer),), default=dummy_space)
        dummy_space = dummy_space + pdk.get_grule(sdlayer)["min_separation"] + float(size[0] / 2)
        sides = list()
        if dummyl:
            sides.append(-1)
        if dummyr:
            sides.append(1)
        for side in sides:
            dummy_ref = multiplier << dummy
            dummy_ref.movex(side * (dummy_space + multiplier.xmax))
    # ensure correct port names and return
    multiplier = rename_ports_by_list(multiplier, [("source","source_"),("drain","drain_"),("gate","gate_"),("plusdoped","plusdoped_")])
    return component_snap_to_grid(rename_ports_by_orientation(multiplier))


@validate_arguments
def __mult_array_macro(
    pdk: MappedPDK,
    sdlayer: str,
    width: Optional[float] = 3,
    fingers: Optional[int] = 1,
    multipliers: Optional[int] = 1,
    routing: Optional[bool] = True,
    dummy: Optional[Union[bool, tuple[bool, bool]]] = True,
    length: Optional[float] = None,
    sd_route_topmet: Optional[str] = "met2",
    gate_route_topmet: Optional[str] = "met2",
    sd_route_left: Optional[bool] = True,
) -> Component:
    """create a multiplier array with multiplier_0 at the bottom
    The array is correctly centered"""
    # create multiplier array
    pdk.activate()
    # TODO: error checking
    multiplier_arr = Component("temp multiplier array")
    multiplier_comp = multiplier(
        pdk,
        sdlayer,
        width=width,
        fingers=fingers,
        dummy=dummy,
        routing=routing,
        length=length,
        sd_route_topmet=sd_route_topmet,
        gate_route_topmet=gate_route_topmet
    )
    multiplier_separation = (
        to_decimal(pdk.get_grule("met2")["min_separation"])
        + evaluate_bbox(multiplier_comp, True)[1]
    )
    for rownum in range(multipliers):
        row_displacment = rownum * multiplier_separation - (multiplier_separation/2 * (multipliers-1))
        row_ref = multiplier_arr << multiplier_comp
        row_ref.movey(to_float(row_displacment))
        multiplier_arr.add_ports(
            row_ref.get_ports_list(), prefix="multiplier_" + str(rownum) + "_"
        )
    # TODO: fix extension (both extension are broken. IDK src extension and drain extension IDK metal layer)
    src_extension = to_decimal(0.6)
    drain_extension = src_extension + 3*to_decimal(pdk.get_grule("met4")["min_separation"])
    sd_side = "W" if sd_route_left else "E"
    gate_side = "E" if sd_route_left else "W"
    if routing and multipliers > 1:
        for rownum in range(multipliers-1):
            thismult = "multiplier_" + str(rownum) + "_"
            nextmult = "multiplier_" + str(rownum+1) + "_"
            # route sources left
            srcpfx = thismult + "source_"
            this_src = multiplier_arr.ports[srcpfx+sd_side]
            next_src = multiplier_arr.ports[nextmult + "source_"+sd_side]
            src_ref = multiplier_arr << c_route(pdk, this_src, next_src, viaoffset=(True,False), extension=to_float(src_extension))
            multiplier_arr.add_ports(src_ref.get_ports_list(), prefix=srcpfx)
            # route drains left
            drainpfx = thismult + "drain_"
            this_drain = multiplier_arr.ports[drainpfx+sd_side]
            next_drain = multiplier_arr.ports[nextmult + "drain_"+sd_side]
            drain_ref = multiplier_arr << c_route(pdk, this_drain, next_drain, viaoffset=(True,False), extension=to_float(drain_extension))
            multiplier_arr.add_ports(drain_ref.get_ports_list(), prefix=drainpfx)
            # route gates right
            gatepfx = thismult + "gate_"
            this_gate = multiplier_arr.ports[gatepfx+gate_side]
            next_gate = multiplier_arr.ports[nextmult + "gate_"+gate_side]
            gate_ref = multiplier_arr << c_route(pdk, this_gate, next_gate, viaoffset=(True,False), extension=to_float(src_extension))
            multiplier_arr.add_ports(gate_ref.get_ports_list(), prefix=gatepfx)
    multiplier_arr = component_snap_to_grid(rename_ports_by_orientation(multiplier_arr))
    # recenter
    final_arr = Component()
    marrref = final_arr << multiplier_arr
    correctionxy = prec_center(marrref)
    marrref.movex(correctionxy[0]).movey(correctionxy[1])
    final_arr.add_ports(marrref.get_ports_list())
    return component_snap_to_grid(final_arr)


@cell
def nmos(
    pdk,
    width: float = 3,
    fingers: Optional[int] = 1,
    multipliers: Optional[int] = 1,
    with_tie: Optional[bool] = True,
    with_dummy: Optional[Union[bool, tuple[bool, bool]]] = True,
    with_dnwell: Optional[bool] = True,
    with_substrate_tap: Optional[bool] = True,
    length: Optional[float] = None,
    sd_route_topmet: Optional[str] = "met2",
    gate_route_topmet: Optional[str] = "met2",
    sd_route_left: Optional[bool] = True
) -> Component:
    """Generic NMOS generator
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
        pdk, "n+s/d", width, fingers, multipliers, dummy=with_dummy, length=length, sd_route_topmet=sd_route_topmet, gate_route_topmet=gate_route_topmet, sd_route_left=sd_route_left
    )
    multiplier_arr_ref = multiplier_arr.ref()
    nfet.add(multiplier_arr_ref)
    nfet.add_ports(multiplier_arr_ref.get_ports_list())
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
        tiering_ref = nfet << tapring(
            pdk,
            enclosed_rectangle=tap_encloses,
            sdlayer="p+s/d",
            horizontal_glayer="met2",
            vertical_glayer="met1",
        )
        nfet.add_ports(tiering_ref.get_ports_list(), prefix="tie_")
    # add pwell
    nfet.add_padding(
        layers=(pdk.get_glayer("pwell"),),
        default=pdk.get_grule("pwell", "active_tap")["min_enclosure"],
    )
    nfet = add_ports_perimeter(nfet,layer=pdk.get_glayer("pwell"),prefix="well_")
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
        ringtoadd = tapring(
            pdk,
            enclosed_rectangle=substrate_tap_encloses,
            sdlayer="p+s/d",
            horizontal_glayer="met2",
            vertical_glayer="met1",
        )
        tapring_ref = nfet << ringtoadd
        nfet.add_ports(tapring_ref.get_ports_list(),prefix="guardring_")
    return rename_ports_by_orientation(nfet).flatten()


@cell
def pmos(
    pdk,
    width: float = 3,
    fingers: Optional[int] = 1,
    multipliers: Optional[int] = 1,
    with_tie: Optional[bool] = True,
    dnwell: Optional[bool] = False,
    with_dummy: Optional[Union[bool, tuple[bool, bool]]] = True,
    with_substrate_tap: Optional[bool] = True,
    length: Optional[float] = None,
    sd_route_topmet: Optional[str] = "met2",
    gate_route_topmet: Optional[str] = "met2",
    sd_route_left: Optional[bool] = True
) -> Component:
    """Generic PMOS generator
    width = expands the PMOS in the y direction
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
        pdk, "p+s/d", width, fingers, multipliers, dummy=with_dummy, length=length, sd_route_topmet=sd_route_topmet, gate_route_topmet=gate_route_topmet, sd_route_left=sd_route_left
    )
    multiplier_arr_ref = multiplier_arr.ref()
    pfet.add(multiplier_arr_ref)
    pfet.add_ports(multiplier_arr_ref.get_ports_list())
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
    pfet.add_padding(
        layers=(pdk.get_glayer(nwell_glayer),),
        default=pdk.get_grule("active_tap", nwell_glayer)["min_enclosure"],
    )
    pfet = add_ports_perimeter(pfet,layer=pdk.get_glayer(nwell_glayer),prefix="well_")
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
    return rename_ports_by_orientation(pfet).flatten()


if __name__ == "__main__":
    from PDK.util.standard_main import pdk

    showmult = False
    if showmult:
        mycomp = multiplier(pdk, "p+s/d", fingers=8, dummy=True, gate_route_topmet="met4",sd_route_topmet="met3", length=1)
    else:
        #mycomp = pmos(pdk, fingers=8, length=1, multipliers=3, width=6, with_dummy=True)
        mycomp = pmos(pdk, fingers=8, length=1, multipliers=3, width=6, with_dummy=True)
        print(*mycomp.get_polygons(),sep="\n")
        #large = pmos(pdk, fingers=20, length=1, multipliers=5, width=6, with_dummy=True)
        #large.show()
        #mycomp = pmos(pdk, fingers=8, multipliers=2, with_dummy=False, gate_route_topmet="met4",sd_route_topmet="met4")
    mycomp.show()
    for key in mycomp.ports.keys():
        print(key)
