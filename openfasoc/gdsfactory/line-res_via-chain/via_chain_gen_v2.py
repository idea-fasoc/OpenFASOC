import argparse

import gdsfactory as gf


@gf.cell
def via_chain(
    dim=40,
    spacing=2.3,
    width=0.5,
    res_sets=8,
    via_sets=10,
    via_spacing=1.5,
    seg_width=0.5,
    via_dim=0.15,
    wire_layer1=(69, 20),
    wire_layer2=(69, 20),
):

    """
    Args:
        dim: dimension of floorplan width and length.
        spacing: spacing of wire
        width: width of wire
        res_sets: number of turns, must be even number
        via_sets: number of vias on one horizontal line, must be even number
        via_spacing: spacing between two vias
        seg_width: segment (lower metal) width
        via_dim: W & L of via

    """

    # center wire width, also the distance between two sense connections
    res_width = ((res_sets * 2) - 1) * spacing

    # tail length on each end
    res_tail = (dim - res_width) / 2

    # WIRES and VIAS
    pt_x = 0
    pt_y = 0

    # points list
    pt_list = []

    # a set of pts that need to place a via
    via_place_set = set()

    via_seg_pitch = dim / via_sets

    for i in range(res_sets):
        # hor line in one direction
        pt_list.append((pt_x, pt_y))

        for j in range(via_sets):
            segment_center_x = 0 + 1 / 2 * via_seg_pitch + j * via_seg_pitch
            pt_x_1 = segment_center_x - 1 / 2 * via_spacing
            pt_x_2 = segment_center_x + 1 / 2 * via_spacing

            pt_list.append((pt_x_1, pt_y))
            pt_list.append((pt_x_2, pt_y))
            via_place_set.add((pt_x_1, pt_y))
            via_place_set.add((pt_x_2, pt_y))

        pt_list.append((pt_x + dim, pt_y))
        # hor line in opposite direction
        pt_list.append((pt_x + dim, pt_y + spacing))

        for j in range(via_sets):
            segment_center_x = dim - 1 / 2 * via_seg_pitch - j * via_seg_pitch
            pt_x_1 = segment_center_x + 1 / 2 * via_spacing
            pt_x_2 = segment_center_x - 1 / 2 * via_spacing

            pt_list.append((pt_x_1, pt_y + spacing))
            pt_list.append((pt_x_2, pt_y + spacing))
            via_place_set.add((pt_x_1, pt_y + spacing))
            via_place_set.add((pt_x_2, pt_y + spacing))

        pt_list.append((pt_x, pt_y + spacing))

        # move the pts (really just pt_y) to next location
        pt_y += 2 * spacing

    # create a wire + vias component to keep all references
    Cviachain = gf.Component("via_chain")

    # cross section of wires and segments
    Xwire = gf.CrossSection(width=width, offset=0, layer=wire_layer1)
    Xseg = gf.CrossSection(width=seg_width, offset=0, layer=wire_layer2)

    # create wire and via segments from points
    is_wire = True  # by default, the first piece between two points is a wire

    for i in range(0, len(pt_list) - 1):
        pts = pt_list[i : i + 2]

        # if the y coordinate changes, it must be a wire
        if pts[0][1] != pts[1][1]:
            # create a 4-pt segment for the U-turns
            pts.insert(0, pt_list[i - 1])
            pts.append(pt_list[i + 2])

            Cwire = gf.path.extrude(gf.Path(pts), Xwire)
            Cviachain << Cwire

            # the next two dots will also be a wire
            is_wire = True
            continue

        # otherwise, create the wire/segment
        if is_wire:
            Cwire = gf.path.extrude(gf.Path(pts), Xwire)
            Cviachain << Cwire
        else:
            Cseg = gf.path.extrude(gf.Path(pts), Xseg)
            Cviachain << Cseg
        # alternate between wire and segment
        is_wire = not is_wire

    # create a "via component"
    Cvia = gf.Component("via_stack")
    r = Cvia << gf.components.rectangle(size=[seg_width, seg_width], layer=wire_layer1)
    r.move([-seg_width / 2, -seg_width / 2])
    r = Cvia << gf.components.rectangle(size=[width, width], layer=wire_layer2)
    r.move([-width / 2, -width / 2])
    r = Cvia << gf.components.rectangle(size=[via_dim, via_dim], layer=wire_layer2)
    r.move([-via_dim / 2, -via_dim / 2])

    # place the vias at locations
    for coord in via_place_set:
        v = Cviachain << Cvia
        v.move(list(coord))

    # TOP
    # create top level component
    Ctop = gf.Component("top")

    # create a reference in top
    Rviachain = Ctop << Cviachain

    # move the wire component reference
    translation = (dim / 2 - Cviachain.center[0], dim / 2 - Cviachain.center[1])
    Rviachain.move(translation)

    # create and reference tails
    Ctail1 = gf.path.extrude(gf.Path([(dim / 2, 0), (dim / 2, res_tail)]), Xwire)
    Ctail2 = gf.path.extrude(
        gf.Path([(dim / 2, dim), (dim / 2, dim - res_tail)]), Xwire
    )

    Ctop << Ctail1
    Ctop << Ctail2

    # STRUCTURE
    # create top gds with pads
    Cstructure = gf.Component()

    # import and place pads
    Cpad = gf.import_gds("./pad_forty_met1_met5.GDS")
    for i in range(4):
        Rpad = Cstructure << Cpad
        Rpad.move([0, i * 60])

    # move top to a proper location
    Rtop = Cstructure << Ctop
    Rtop.move([50, 90])

    # connect current ports of top to pads
    Xwire_i = gf.CrossSection(width=3 * width, offset=0, layer=wire_layer1)
    Ctail1 = gf.path.extrude(gf.Path([(70, 130), (70, 200), (40, 200)]), Xwire_i)
    Ctail2 = gf.path.extrude(gf.Path([(70, 90), (70, 20), (40, 20)]), Xwire_i)

    Cstructure << Ctail1
    Cstructure << Ctail2

    # connect voltage ports of top to pads
    v_pt_a_y = pt_list[0][1] + 90 + translation[1]
    v_pt_b_y = pt_list[-1][1] + 90 + translation[1]

    Ctail1 = gf.path.extrude(gf.Path([(40, v_pt_a_y), (50, v_pt_a_y)]), Xwire)
    Ctail2 = gf.path.extrude(gf.Path([(40, v_pt_b_y), (50, v_pt_b_y)]), Xwire)

    Cstructure << Ctail1
    Cstructure << Ctail2
    return Cstructure


if __name__ == "__main__":
    c = via_chain()
    c.show()

    # Cstructure.write_gds(str(wire_layer) + "_via_chain.gds")
