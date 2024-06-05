from glayout.flow.pdk.mappedpdk import MappedPDK
from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
from gdsfactory.components.rectangular_ring import rectangular_ring
from glayout.flow.primitives.via_gen import via_array, via_stack
from typing import Optional
from glayout.flow.pdk.util.comp_utils import to_decimal, to_float, evaluate_bbox
from glayout.flow.pdk.util.port_utils import print_ports
from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid
from glayout.flow.routing.L_route import L_route


#@cell
def tapring(
    pdk: MappedPDK,
    enclosed_rectangle=(2.0, 4.0),
    sdlayer: str = "p+s/d",
    horizontal_glayer: str = "met2",
    vertical_glayer: str = "met1",
    sides: tuple[bool,bool,bool,bool] = (True,True,True,True)
) -> Component:
    """ptapring produce a p substrate / pwell tap rectanglular ring
    This ring will legally enclose a rectangular shape
    args:
    pdk: MappedPDK is the pdk to use
    enclosed_rectangle: tuple is the (width, hieght) of the area to enclose
    ****NOTE: the enclosed_rectangle will be the enclosed dimensions of active_tap
    horizontal_glayer: string=met2, layer used over the ring horizontally
    vertical_glayer: string=met1, layer used over the ring vertically
    sides: instead of creating the ring on all sides, only create it on the specified sides (W,N,E,S)
    ports:
    Narr_... all ports in top via array
    Sarr_... all ports in bottom via array
    Earr_... all ports in right via array
    Warr_... all ports in left via array
    bl_corner_...all ports in bottom left L route
    """
    enclosed_rectangle = pdk.snap_to_2xgrid(enclosed_rectangle,return_type="float")
    # check layers, activate pdk, create top cell
    pdk.has_required_glayers(
        [sdlayer, "active_tap", "mcon", horizontal_glayer, vertical_glayer]
    )
    pdk.activate()
    ptapring = Component()
    if not "met" in horizontal_glayer or not "met" in vertical_glayer:
        raise ValueError("both horizontal and vertical glayers should be metals")
    # check that ring is not too small
    min_gap_tap = pdk.get_grule("active_tap")["min_separation"]
    if enclosed_rectangle[0] < min_gap_tap:
        raise ValueError("ptapring must be larger than " + str(min_gap_tap))
    # create active tap
    tap_width = max(
        pdk.get_grule("active_tap")["min_width"],
        2 * pdk.get_grule("active_tap", "mcon")["min_enclosure"]
        + pdk.get_grule("mcon")["width"],
    )
    ptapring << rectangular_ring(
        enclosed_size=enclosed_rectangle,
        width=tap_width,
        centered=True,
        layer=pdk.get_glayer("active_tap"),
    )
    # create p plus area
    pp_enclosure = pdk.get_grule("active_tap", sdlayer)["min_enclosure"]
    pp_width = 2 * pp_enclosure + tap_width
    pp_enclosed_rectangle = [dim - 2 * pp_enclosure for dim in enclosed_rectangle]
    ptapring << rectangular_ring(
        enclosed_size=pp_enclosed_rectangle,
        width=pp_width,
        centered=True,
        layer=pdk.get_glayer(sdlayer),
    )
    # create via arrs
    via_width_horizontal = evaluate_bbox(via_stack(pdk, "active_tap", horizontal_glayer))[0]
    arr_size_horizontal = enclosed_rectangle[0]
    horizontal_arr = via_array(
        pdk,
        "active_tap",
        horizontal_glayer,
        (arr_size_horizontal, via_width_horizontal),
        minus1=True,
        lay_every_layer=True
    )
    via_width_vertical = evaluate_bbox(via_stack(pdk, "active_tap", vertical_glayer))[1]
    arr_size_vertical = enclosed_rectangle[1]
    vertical_arr = via_array(
        pdk,
        "active_tap",
        vertical_glayer,
        (via_width_vertical, arr_size_vertical),
        minus1=True,
        lay_every_layer=True
    )
    # add via arrs
    refs_prefixes = list()
    if sides[1]:
        metal_ref_n = ptapring << horizontal_arr
        metal_ref_n.movey(round(0.5 * (enclosed_rectangle[1] + tap_width),4))
        refs_prefixes.append((metal_ref_n,"N_"))
    if sides[2]:
        metal_ref_e = ptapring << vertical_arr
        metal_ref_e.movex(round(0.5 * (enclosed_rectangle[0] + tap_width),4))
        refs_prefixes.append((metal_ref_e,"E_"))
    if sides[3]:
        metal_ref_s = ptapring << horizontal_arr
        metal_ref_s.movey(round(-0.5 * (enclosed_rectangle[1] + tap_width),4))
        refs_prefixes.append((metal_ref_s,"S_"))
    if sides[0]:
        metal_ref_w = ptapring << vertical_arr
        metal_ref_w.movex(round(-0.5 * (enclosed_rectangle[0] + tap_width),4))
        refs_prefixes.append((metal_ref_w,"W_"))
    # connect vertices
    if sides[1] and sides[0]:
        tlvia = ptapring << L_route(pdk, metal_ref_n.ports["top_met_W"], metal_ref_w.ports["top_met_N"])
        refs_prefixes += [(tlvia,"tl_")]
    if sides[1] and sides[2]:
        trvia = ptapring << L_route(pdk, metal_ref_n.ports["top_met_E"], metal_ref_e.ports["top_met_N"])
        refs_prefixes += [(trvia,"tr_")]
    if sides[3] and sides[0]:
        blvia = ptapring << L_route(pdk, metal_ref_s.ports["top_met_W"], metal_ref_w.ports["top_met_S"])
        refs_prefixes += [(blvia,"bl_")]
    if sides[3] and sides[2]:
        brvia = ptapring << L_route(pdk, metal_ref_s.ports["top_met_E"], metal_ref_e.ports["top_met_S"])
        refs_prefixes += [(brvia,"br_")]
    # add ports, flatten and return
    for ref_, prefix in refs_prefixes:
        ptapring.add_ports(ref_.get_ports_list(),prefix=prefix)
    return component_snap_to_grid(ptapring)



