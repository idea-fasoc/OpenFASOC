# from PDK.mappedpdk import MappedPDK
from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
from gdsfactory.components.rectangular_ring import rectangular_ring
from via_gen import via_stack
from typing import Optional
from math import ceil


@cell
def ptapring(
    pdk,
    enclosed_rectangle=(2.0, 4.0),
    horizontal_glayer: Optional[str] = "met1",
    vertical_glayer: Optional[str] = "met2",
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
    # compute via seperation. via_spacing[0] is horizontal, via_spacing[1] is vertical
    xlvl = int(horizontal_glayer[-1])
    ylvl = int(vertical_glayer[-1])
    via_spacing = list()
    for dlvl in [xlvl, ylvl]:
        via_seperations = [pdk.get_grule("mcon")["min_seperation"]] + [
            pdk.get_grule("via" + str(lvl))["min_seperation"]
            for lvl in range(1, dlvl + 1)
        ]
        metal_seperations = [
            pdk.get_grule("met" + str(lvl))["min_seperation"]
            for lvl in range(1, dlvl + 1)
        ]
        via_spacing.append(max(via_seperations + metal_seperations))
    # compute how many vias and create the vias
    num_vias = list()
    viawidth = 0  # need this for later
    for i, toplayer in enumerate([horizontal_glayer, vertical_glayer]):
        # figure out how many vias
        viastack = via_stack(pdk, "active_tap", toplayer)
        viawidth = max(viastack.xmax - viastack.xmin, viastack.ymax - viastack.ymin)
        viaspacing_full = viawidth + via_spacing[i]
        num_vias = int(enclosed_rectangle[i] / viaspacing_full)
        if num_vias > 1:
            num_vias = num_vias - 1
        # lay vias
        for vianum in range(num_vias):
            viastack_ref_plus = ptapring << viastack
            viastack_ref_minus = ptapring << viastack
            spacing_multiplier = ((-1) ** vianum) * ceil(vianum / 2)
            if i == 0:  # horizontal layer
                viastack_ref_plus.movex(spacing_multiplier * viaspacing_full).movey(
                    0.5 * (enclosed_rectangle[1] + tap_width)
                )
                viastack_ref_minus.movex(spacing_multiplier * viaspacing_full).movey(
                    -0.5 * (enclosed_rectangle[1] + tap_width)
                )
            else:  # vertical layer
                viastack_ref_plus.movex(
                    0.5 * (enclosed_rectangle[0] + tap_width)
                ).movey(spacing_multiplier * viaspacing_full)
                viastack_ref_minus.movex(
                    -0.5 * (enclosed_rectangle[0] + tap_width)
                ).movey(spacing_multiplier * viaspacing_full)
    # lay metal
    ns_side_dims = (
        enclosed_rectangle[0] + 2 * tap_width,
        max(viawidth, pdk.get_grule(horizontal_glayer)["min_width"]),
    )
    ew_side_dims = (
        max(viawidth, pdk.get_grule(horizontal_glayer)["min_width"]),
        enclosed_rectangle[1] + 2 * tap_width,
    )
    metal_ref_n = ptapring << rectangle(
        layer=pdk.get_glayer(horizontal_glayer), size=ns_side_dims, centered=True
    )
    metal_ref_e = ptapring << rectangle(
        layer=pdk.get_glayer(vertical_glayer), size=ew_side_dims, centered=True
    )
    metal_ref_s = ptapring << rectangle(
        layer=pdk.get_glayer(horizontal_glayer), size=ns_side_dims, centered=True
    )
    metal_ref_w = ptapring << rectangle(
        layer=pdk.get_glayer(vertical_glayer), size=ew_side_dims, centered=True
    )
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
