from PDK.mappedpdk import MappedPDK
from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
from gdsfactory.components.rectangular_ring import rectangular_ring
from via_gen import via_array, via_stack
from typing import Optional
from math import ceil


@cell
def ptapring(
    pdk: MappedPDK,
    enclosed_rectangle=(2.0, 4.0),
    horizontal_glayer: Optional[str] = "met2",
    vertical_glayer: Optional[str] = "met1",
) -> Component:
    """ptapring produce a p substrate / pwell tap rectanglular ring
    This ring will legally enclose a rectangular shape
    args:
    pdk: MappedPDK is the pdk to use
    enclosed_rectangle: tuple is the (width, hieght) of the area to enclose
    ****NOTE: the enclosed_rectangle will be the enclosed dimensions of active_tap
    horizontal_glayer: string=met2, layer used over the ring horizontally
    vertical_glayer: string=met1, layer used over the ring vertically
    """
    # check layers, activate pdk, create top cell
    pdk.has_required_glayers(
        ["p+s/d", "active_tap", "mcon", horizontal_glayer, vertical_glayer]
    )
    pdk.activate()
    ptapring = Component()
    if not "met" in horizontal_glayer or not "met" in vertical_glayer:
        raise ValueError("both horizontal and vertical glayers should be metals")
    # check that ring is not too small
    min_gap_tap = pdk.get_grule("active_tap")["min_seperation"]
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
    pp_enclosure = pdk.get_grule("active_tap", "p+s/d")["min_enclosure"]
    pp_width = 2 * pp_enclosure + tap_width
    pp_enclosed_rectangle = [dim - 2 * pp_enclosure for dim in enclosed_rectangle]
    ptapring << rectangular_ring(
        enclosed_size=pp_enclosed_rectangle,
        width=pp_width,
        centered=True,
        layer=pdk.get_glayer("p+s/d"),
    )
    # create via arrs
    via_width_horizontal = 2 * via_stack(pdk, "active_diff", horizontal_glayer).ymax
    arr_size_horizontal = enclosed_rectangle[0]
    horizontal_arr = via_array(
        pdk,
        "active_diff",
        horizontal_glayer,
        (arr_size_horizontal, via_width_horizontal),
        minus1=True,
    )
    via_width_vertical = 2 * via_stack(pdk, "active_diff", vertical_glayer).ymax
    arr_size_vertical = enclosed_rectangle[1]
    vertical_arr = via_array(
        pdk,
        "active_diff",
        vertical_glayer,
        (via_width_vertical, arr_size_vertical),
        minus1=True,
    )
    # add via arrs
    metal_ref_n = ptapring << horizontal_arr
    metal_ref_e = ptapring << vertical_arr
    metal_ref_s = ptapring << horizontal_arr
    metal_ref_w = ptapring << vertical_arr
    metal_ref_n.movey(0.5 * (enclosed_rectangle[1] + tap_width))
    metal_ref_e.movex(0.5 * (enclosed_rectangle[0] + tap_width))
    metal_ref_s.movey(-0.5 * (enclosed_rectangle[1] + tap_width))
    metal_ref_w.movex(-0.5 * (enclosed_rectangle[0] + tap_width))
    # done, flatten and return
    return ptapring.flatten()


if __name__ == "__main__":
    from PDK.gf180_mapped import gf180_mapped_pdk

    gf180_mapped_pdk.activate()
    ptapring(gf180_mapped_pdk, enclosed_rectangle=(5, 5)).show()
