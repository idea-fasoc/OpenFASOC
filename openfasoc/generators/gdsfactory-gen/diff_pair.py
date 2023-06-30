import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk
from gdsfactory.component import Component, ComponentReference

from gdsfactory.generic_tech import get_generic_pdk
import sky130

from PDK.sky130_mapped import sky130_mapped_pdk
from fet import multiplier
from PDK.gf180_mapped import gf180_mapped_pdk

pdk = sky130_mapped_pdk

gf.config.rich_output()
# PDK = get_generic_pdk()
# PDK.activate()

pwell_drawing = pdk.get_glayer("pwell")
dnwell_drawing = pdk.get_glayer("dnwell")
nwell_drawing = pdk.get_glayer("nwell")
outline_ref = (236, 0)
diff_drawing = pdk.get_glayer("active_diff")
psdm_drawing = pdk.get_glayer("p+s/d")
nsdm_drawing = pdk.get_glayer("n+s/d")
poly_drawing = pdk.get_glayer("poly")
poly_pin = (66, 16)
poly_label = (66, 5)
licon1_drawing = pdk.get_glayer("mcon")
npc_drawing = (95, 20)
li1_drawing = pdk.get_glayer("met1")
mcon_drawing = (67, 44)
met1_drawing = (68, 20)
met1_label = (68, 5)
met1_pin = (68, 16)
via_drawing = (68, 44)
met2_drawing = (69, 20)
met2_label = (69, 5)
met2_pin = (69, 16)
via2_drawing = (69, 44)
met3_drawing = (70, 20)
met3_label = (70, 5)
met3_pin = (70, 16)
text_drawing = (83, 44)


@gf.cell
def nmos(cell_height, finger) -> Component:
    c = Component()

    ##nsdm
    nsdm_height = cell_height  ##0.67
    nsdm_width = 1.1 + (finger - 1) * 0.55

    nsdm_outline_rect = gf.components.rectangle(
        size=(nsdm_width, nsdm_height), layer=nsdm_drawing
    )
    nsdm_outline_rect_ref = c << nsdm_outline_rect

    ##poly
    poly_width = pdk.get_grule("poly")["min_width"]
    poly_height = cell_height + 0.011  ##0.68

    poly_rect = gf.components.rectangle(
        size=(poly_width, poly_height), layer=poly_drawing
    )

    ####### Finger
    for i in range(finger):
        poly_rect_ref = c << poly_rect

        poly_rect_ref.movex(0.425 + 0.55 * i).movey(-0.005)

    ##diff
    diff_width = 0.85 + (finger - 1) * 0.55
    diff_height = cell_height - (0.125 * 2)  ##0.42
    diff_rect = gf.components.rectangle(
        size=(diff_width, diff_height), layer=diff_drawing
    )
    diff_rect_ref = c << diff_rect

    diff_rect_ref.movex(0.125).movey(0.125)

    ##li1_drawing
    li1_height = cell_height - (0.085 * 2)  ##0.5
    li1_width = 0.17
    li1_rect = gf.components.rectangle(size=(li1_width, li1_height), layer=li1_drawing)
    li1_rect_ref1 = c << li1_rect
    li1_rect_ref1.movey(0.085).movex(0.19)

    ######Finger
    for i in range(finger):
        li1_rect_ref1 = c << li1_rect
        li1_rect_ref1.movey(0.085).movex(0.19 + ((i + 1) * 0.55))
    # li1_rect_ref2 = c << li1_rect
    # li1_rect_ref2.movey(0.085).movex(0.74)

    ##mcon
    mcon_height = 0.17
    mcon_width = 0.17

    mcon_rect = gf.components.rectangle(
        size=(mcon_width, mcon_height), layer=mcon_drawing
    )

    for i in range(int(cell_height / 0.67)):
        mcon_rect_ref1 = c << mcon_rect
        mcon_rect_ref1.movey(0.67 * i + 0.25).movex(0.19)
        ######Finger
        for j in range(finger):
            mcon_rect_ref2 = c << mcon_rect
            mcon_rect_ref2.movey(0.67 * i + 0.25).movex(0.19 + ((j + 1) * 0.55))

    ##licon1
    licon1_height = 0.17
    licon1_width = 0.17

    licon1_rect = gf.components.rectangle(
        size=(licon1_width, licon1_height), layer=licon1_drawing
    )

    for i in range(int(cell_height / 0.67)):
        licon1_rect_ref1 = c << licon1_rect
        licon1_rect_ref1.movey(0.67 * i + 0.25).movex(0.19)
        ######Finger
        for j in range(finger):
            licon1_rect_ref2 = c << licon1_rect
            licon1_rect_ref2.movey(0.67 * i + 0.25).movex(0.19 + ((j + 1) * 0.55))

    ##met1
    met1_height = cell_height - (0.125 * 2)  ##0.42
    met1_width = 0.23

    met1_rect = gf.components.rectangle(
        size=(met1_width, met1_height), layer=met1_drawing
    )

    met1_rect_ref1 = c << met1_rect
    met1_rect_ref1.movey(0.125).movex(0.16)

    met1_rect_ref2 = c << met1_rect
    met1_rect_ref2.movey(0.125).movex(0.71)

    ######Finger
    for i in range(finger):
        met1_rect_ref2 = c << met1_rect
        met1_rect_ref2.movey(0.125).movex(0.16 + ((i + 1) * 0.55))

    ##labels
    ######Finger
    for i in range(finger - 1):
        met1_label_s = c.add_label(
            "S",
            position=(0.255 + (i * 1.1), (cell_height / 2)),
            layer=met1_label,
            magnification=0.2,
        )

    for i in range(finger - 2):
        met1_label_d = c.add_label(
            "D",
            position=(0.81 + (i) * 1.1, (cell_height / 2)),
            layer=met1_label,
            magnification=0.2,
        )
    # c.add_label()

    return c


@gf.cell
def diff_pair_top_updated(mult=3, finger=3, cell_height=0.67) -> Component:

    Top_cell = gf.Component("top")

    mult = mult * 2
    # mos_comp = nmos(cell_height, finger)
    mos_comp = multiplier(
        sky130_mapped_pdk, sdlayer="n+s/d", fingers=finger, routing=False, dummy=False
    )
    cell_height = mos_comp.ymax - mos_comp.ymin
    cell_width = mos_comp.xmax - mos_comp.xmin
    # cell_width = 1.1 + 0.55*(finger-1)
    space_bet_rows = 4
    space_bet_mult = 1.5
    rows = 2

    ##pwell
    pwell_width = cell_width * (mult / rows) + 0.11 + space_bet_mult
    pwell_height = (cell_height * 1) * rows + 0.11 + space_bet_rows

    pwell_rect = gf.components.rectangle(
        size=(pwell_width, pwell_height), layer=pwell_drawing
    )
    # pwell_rect_ref = Top_cell << pwell_rect
    # pwell_rect_ref.movex(-0.055).movey(-0.055)

    ##dnwell
    # dnwell_width = (cell_width*((mult+1)/2)) + 0.91
    dnwell_width = cell_width * (mult / rows) + 0.91 + space_bet_mult
    dnwell_height = (cell_height * 1) * rows + 0.91 + space_bet_rows
    dnwell_rect = gf.components.rectangle(
        size=(dnwell_width, dnwell_height), layer=dnwell_drawing
    )
    # dnwell_rect_ref = Top_cell << dnwell_rect
    # dnwell_rect_ref.movex(-0.455).movey(-0.455)

    for i in range(int(mult / rows)):
        j = 0
        for j in range(rows):
            print(j)
            ref = Top_cell << mos_comp
            if i == 0:
                ref.movex(cell_width * i + cell_width / 2).movey(
                    cell_height * (j) + cell_height / 2 + space_bet_rows * (j)
                )
            else:
                ref.movex(cell_width * i + cell_width / 2 + space_bet_mult).movey(
                    cell_height * (j) + cell_height / 2 + space_bet_rows * (j)
                )

    met3_sq_dim = max(
        pdk.get_grule("via2")["min_width"]
        + 2 * pdk.get_grule("met3", "via2")["min_enclosure"],
        pdk.get_grule("met3")["min_width"],
    )

    ##Change from 0.14 to 0.28
    met2_sq_dim = max(
        pdk.get_grule("via1")["min_width"]
        + 2 * pdk.get_grule("met2", "via1")["min_enclosure"],
        pdk.get_grule("met2")["min_width"],
    )
    ##VSS trunk -- merging
    met3_VSS_trunk_width = cell_width * (i + 1) + space_bet_mult * i + 1
    met3_VSS_trunk = gf.components.rectangle(
        size=(met3_VSS_trunk_width, met3_sq_dim), layer=pdk.get_glayer("met3")
    )

    met3_VSS_trunk_ref = Top_cell << met3_VSS_trunk
    met3_VSS_trunk_ref.movey(cell_height + space_bet_rows * 0.9 - met3_sq_dim / 2)

    met3_VSS_trunk_ref = Top_cell << met3_VSS_trunk
    met3_VSS_trunk_ref.movey(cell_height + space_bet_rows * 0.1 - met3_sq_dim / 2)

    met3_met2_VSS_trunk_height = space_bet_rows * 0.8 + met3_sq_dim
    met3_met2_VSS_trunk = gf.components.rectangle(
        size=(met2_sq_dim, met3_met2_VSS_trunk_height), layer=pdk.get_glayer("met2")
    )

    met3_met2_VSS_trunk_ref = Top_cell << met3_met2_VSS_trunk
    met3_met2_VSS_trunk_ref.movey(
        cell_height + space_bet_rows * 0.1 - met3_sq_dim / 2
    ).movex(met3_VSS_trunk_width - met2_sq_dim)

    via2_via_dim = pdk.get_grule("via2")["min_width"]
    via2_via = gf.components.rectangle(
        size=(via2_via_dim, via2_via_dim), layer=pdk.get_glayer("via2")
    )

    ## via2 pulled to met2
    via2_via_ref = Top_cell << via2_via
    via2_via_ref.movey(
        cell_height + space_bet_rows * 0.1 - met3_sq_dim / 2 + via2_via_dim / 2
    ).movex(met3_VSS_trunk_width - met2_sq_dim + via2_via_dim / 2)

    ## via2 pulled to met2
    via2_via_ref = Top_cell << via2_via
    via2_via_ref.movey(
        cell_height
        + space_bet_rows * 0.1
        - met3_sq_dim
        + met3_met2_VSS_trunk_height
        - via2_via_dim / 2
    ).movex(met3_VSS_trunk_width - met2_sq_dim + via2_via_dim / 2)

    # Extending Poly trunk
    for i in range(int(mult / rows)):
        for j in range(rows):

            # poly extending trunk
            poly_width = pdk.get_grule("poly")["min_width"]
            mcon_poly_space = (
                2 * pdk.get_grule("poly", "mcon")["min_seperation"]
                + pdk.get_grule("mcon")["width"]
            )
            poly_finger2finger_x = poly_width + mcon_poly_space

            if finger % 2 != 0:
                poly_left_edge = (
                    cell_width / 2
                    - poly_width / 2
                    - ((finger - 1) / 2) * poly_finger2finger_x
                )
            else:
                poly_left_edge = (
                    cell_width / 2
                    - poly_width / 2
                    - poly_finger2finger_x / 2
                    - ((finger / 2) - 1) * poly_finger2finger_x
                )

            poly_ext_trunk_width = poly_width + (finger - 1) * poly_finger2finger_x

            ##poly_trunk
            # poly_ext_trunk_height = pdk.get_grule("poly")['min_width']
            poly_ext_trunk_height = 0.5
            poly_ext_trunk_ref = gf.components.rectangle(
                size=(poly_ext_trunk_width, poly_ext_trunk_height), layer=poly_drawing
            )

            mcon_via = gf.components.rectangle(
                size=(pdk.get_grule("mcon")["width"], pdk.get_grule("mcon")["width"]),
                layer=pdk.get_glayer("mcon"),
            )

            met1_sq_dim = max(
                pdk.get_grule("mcon")["width"]
                + 2 * pdk.get_grule("met1", "mcon")["min_enclosure"],
                pdk.get_grule("met1")["min_width"],
            )
            met1_square = gf.components.rectangle(
                size=(met1_sq_dim, met1_sq_dim), layer=pdk.get_glayer("met1")
            )

            via1_via_dim = pdk.get_grule("via1")["min_width"]
            via1_via = gf.components.rectangle(
                size=(via1_via_dim, via1_via_dim), layer=pdk.get_glayer("via1")
            )

            ##Change from 0.14 to 0.28
            met2_sq_dim = max(
                pdk.get_grule("via1")["min_width"]
                + 2 * pdk.get_grule("met2", "via1")["min_enclosure"],
                pdk.get_grule("met2")["min_width"],
            )
            met2_square = gf.components.rectangle(
                size=(met2_sq_dim, met2_sq_dim), layer=pdk.get_glayer("met2")
            )

            met2_poly_ext_1_height = 1.5
            met2_poly_ext_2_height = met2_poly_ext_1_height + 1
            met2_poly_ext_1 = gf.components.rectangle(
                size=(met2_sq_dim, met2_poly_ext_1_height), layer=pdk.get_glayer("met2")
            )
            met2_poly_ext_2 = gf.components.rectangle(
                size=(met2_sq_dim, met2_poly_ext_2_height), layer=pdk.get_glayer("met2")
            )

            via2_via_dim = pdk.get_grule("via2")["min_width"]
            via2_via = gf.components.rectangle(
                size=(via2_via_dim, via2_via_dim), layer=pdk.get_glayer("via2")
            )

            via3_via_dim = pdk.get_grule("via3")["min_width"]
            via3_via = gf.components.rectangle(
                size=(via3_via_dim, via3_via_dim), layer=pdk.get_glayer("via3")
            )

            met4_sq_dim = max(
                pdk.get_grule("via3")["min_width"]
                + 2 * pdk.get_grule("met4", "via3")["min_enclosure"],
                pdk.get_grule("met4")["min_width"],
            )

            met3_sq_dim = max(
                pdk.get_grule("via2")["min_width"]
                + 2 * pdk.get_grule("met3", "via2")["min_enclosure"],
                pdk.get_grule("met3")["min_width"],
            )

            met3_poly_ext_width = cell_width * (i + 1) + space_bet_mult * i + 2
            met3_poly_ext = gf.components.rectangle(
                size=(met3_poly_ext_width, met3_sq_dim), layer=pdk.get_glayer("met3")
            )

            met2_poly_ext_outer_trunk_h = cell_height * 2 + space_bet_rows + 2.7 * 2
            met2_poly_ext_outer_trunk = gf.components.rectangle(
                size=(met2_sq_dim, met2_poly_ext_outer_trunk_h),
                layer=pdk.get_glayer("met2"),
            )

            met2_poly_ext_outer_trunk_ref = Top_cell << met2_poly_ext_outer_trunk
            met2_poly_ext_outer_trunk_ref.movex(-2).movey(-2.7)
            met2_poly_ext_outer_trunk_ref = Top_cell << met2_poly_ext_outer_trunk
            met2_poly_ext_outer_trunk_ref.movex(-1).movey(-2.7)

            ## VSS extensions
            met3_VSS_trunk_width = cell_width
            met3_VSS_trunk = gf.components.rectangle(
                size=(met3_VSS_trunk_width, met3_sq_dim), layer=pdk.get_glayer("met3")
            )

            ## Drain extensions
            met3_Drain_trunk_width = cell_width
            met3_Drain_trunk = gf.components.rectangle(
                size=(met3_Drain_trunk_width, met3_sq_dim), layer=pdk.get_glayer("met3")
            )

            ## Drain connections using met3
            ## In the center
            met3_Drain_conn_width = space_bet_mult + 0.3 * 3 + via2_via_dim
            met3_Drain_conn = gf.components.rectangle(
                size=(met3_Drain_conn_width, met3_sq_dim), layer=pdk.get_glayer("met3")
            )
            # met3_Drain_conn
            met3_Drain_conn_ref = Top_cell << met3_Drain_conn
            met3_Drain_conn_ref.movex(cell_width - 0.3 - via2_via_dim * 1.5).movey(
                cell_height + space_bet_rows / 2 - met3_sq_dim / 2
            )

            ## via2 pulled to met2
            via2_via_ref = Top_cell << via2_via
            via2_via_ref.movey(
                cell_height + space_bet_rows / 2 - via2_via_dim / 2
            ).movex(cell_width - 0.3 - via2_via_dim * 1)

            ## via2 pulled to met2
            via2_via_ref = Top_cell << via2_via
            via2_via_ref.movey(
                cell_height + space_bet_rows / 2 - via2_via_dim / 2
            ).movex(
                met3_Drain_conn_width
                + cell_width
                - 0.3
                - via2_via_dim * 1
                - met2_sq_dim
            )

            met2_met3_Drain_conn_height = space_bet_rows * 0.3
            met2_met3_Drain_conn = gf.components.rectangle(
                size=(met2_sq_dim, met2_met3_Drain_conn_height),
                layer=pdk.get_glayer("met2"),
            )
            # met2_Drain_conn
            # met3_Drain_conn
            met2_met3_Drain_conn_ref = Top_cell << met2_met3_Drain_conn
            met2_met3_Drain_conn_ref.movex(cell_width - 0.3 - via2_via_dim * 1.5).movey(
                cell_height + space_bet_rows / 2 - met3_sq_dim / 2
            )

            met2_met3_Drain_conn_ref = Top_cell << met2_met3_Drain_conn
            met2_met3_Drain_conn_ref.movex(
                cell_width + space_bet_mult + 0.3 - via2_via_dim * 1.5 + met2_sq_dim / 2
            ).movey(
                cell_height
                + space_bet_rows / 2
                - met3_sq_dim / 2
                - met2_met3_Drain_conn_height
                + met3_sq_dim
            )

            ## Drain connection using met1
            ## In the center
            met2_Drain_conn_height = space_bet_rows * 0.48
            met2_Drain_conn = gf.components.rectangle(
                size=(met2_sq_dim, met2_Drain_conn_height), layer=pdk.get_glayer("met2")
            )
            # met2_Drain_conn
            met2_Drain_conn_ref = Top_cell << met2_Drain_conn
            met2_Drain_conn_ref.movex(
                cell_width + space_bet_mult / 2 - via2_via_dim / 2
            ).movey(cell_height + space_bet_rows * 0.3 - met3_sq_dim / 2)

            ## via2 pulled to met3 --- > hor
            via2_via_ref = Top_cell << via2_via
            via2_via_ref.movey(
                cell_height + space_bet_rows * 0.3 - via2_via_dim / 2
            ).movex(cell_width + space_bet_mult / 2)

            ## via2 pulled to met3 --- > hor
            via2_via_ref = Top_cell << via2_via
            via2_via_ref.movey(
                cell_height
                + space_bet_rows * 0.3
                + met2_Drain_conn_height
                - via2_via_dim / 2
                - met3_sq_dim
            ).movex(cell_width + space_bet_mult / 2)

            ## met3 connecting cell extensions
            ## In the center
            met3_ext_conn_width = space_bet_mult * 0.5 + 0.3 + met2_sq_dim
            met3_ext_conn = gf.components.rectangle(
                size=(met3_ext_conn_width, met3_sq_dim), layer=pdk.get_glayer("met3")
            )
            # met3_Drain_conn
            met3_ext_conn_ref = Top_cell << met3_ext_conn
            met3_ext_conn_ref.movex(cell_width - 0.3).movey(
                cell_height + space_bet_rows * 0.3 - met3_sq_dim / 2
            )

            # met3_Drain_conn
            met3_ext_conn_ref = Top_cell << met3_ext_conn
            met3_ext_conn_ref.movex(cell_width + space_bet_mult / 2 - 0.3).movey(
                cell_height + space_bet_rows * 0.7 - met3_sq_dim / 2
            )

            if j == 1:
                ##poly trunk
                poly_trunk = Top_cell << poly_ext_trunk_ref
                poly_trunk.movex(
                    poly_left_edge + cell_width * i + space_bet_mult * i
                ).movey(cell_height * 2 + space_bet_rows * (j))
                poly_trunk_center_y = (poly_trunk.ymax - poly_trunk.ymin) / 2

                ## Drain Stripes
                for con in range(finger + 1):
                    if con % 2 != 0:
                        y_move = cell_height + space_bet_rows * 0.7
                        x_move = (
                            cell_width * i
                            + space_bet_mult * i
                            + poly_left_edge
                            + poly_width / 2
                            - poly_finger2finger_x / 2
                            + con * poly_finger2finger_x
                        )

                        ## Drain extensions
                        met3_Drain_trunk_ref = Top_cell << met3_Drain_trunk
                        met3_Drain_trunk_ref.movex(
                            cell_width * i + space_bet_mult * i
                        ).movey(y_move - met3_sq_dim / 2)

                        ## Drain extension connecting via
                        if i == 0:
                            via2_via_ref = Top_cell << via2_via
                            via2_via_ref.movey(y_move - via2_via_dim / 2).movex(
                                cell_width * (i + 1)
                                + space_bet_mult * i
                                - 0.3
                                - via2_via_dim
                            )
                        else:
                            via3_via_ref = Top_cell << via3_via
                            via3_via_ref.movey(y_move - via3_via_dim / 2).movex(
                                cell_width * (i) + space_bet_mult * i + 0.3
                            )

                        ## Drain stripes
                        met2_Drain_stripes = gf.components.rectangle(
                            size=(met2_sq_dim, cell_height + space_bet_rows * 0.3),
                            layer=pdk.get_glayer("met2"),
                        )
                        met2_square_ref = Top_cell << met2_Drain_stripes
                        met2_square_ref.movey(y_move - met2_sq_dim / 2).movex(
                            x_move - met2_sq_dim / 2
                        )

                        via2_via_ref = Top_cell << via2_via
                        via2_via_ref.movey(y_move - via2_via_dim / 2).movex(
                            x_move - via2_via_dim / 2
                        )

                ## VSS Stripes
                for con in range(finger + 1):
                    if con % 2 == 0:
                        y_move = cell_height + space_bet_rows * 0.9
                        x_move = (
                            cell_width * i
                            + space_bet_mult * i
                            + poly_left_edge
                            + poly_width / 2
                            - poly_finger2finger_x / 2
                            + con * poly_finger2finger_x
                        )

                        ## VSS extensions
                        met3_VSS_trunk_ref = Top_cell << met3_VSS_trunk
                        met3_VSS_trunk_ref.movex(
                            cell_width * i + space_bet_mult * i
                        ).movey(y_move - met3_sq_dim / 2)

                        met2_VSS_stripes = gf.components.rectangle(
                            size=(met2_sq_dim, cell_height + space_bet_rows * 0.25),
                            layer=pdk.get_glayer("met2"),
                        )
                        met2_square_ref = Top_cell << met2_VSS_stripes
                        met2_square_ref.movey(y_move - met2_sq_dim / 2).movex(
                            x_move - met2_sq_dim / 2
                        )

                        via2_via_ref = Top_cell << via2_via
                        via2_via_ref.movey(y_move - via2_via_dim / 2).movex(
                            x_move - via2_via_dim / 2
                        )

                ## Drain Stripes
                for con in range(finger + 1):
                    if con % 2 == 0:
                        y_move = (
                            cell_height * 1 + space_bet_rows * (j) + poly_trunk_center_y
                        )
                        x_move = (
                            cell_width * i
                            + space_bet_mult * i
                            + poly_left_edge
                            + poly_width / 2
                            - poly_finger2finger_x / 2
                            + con * poly_finger2finger_x
                        )

                        # met2_VSS_stripes = gf.components.rectangle(size=( met2_sq_dim, cell_height + space_bet_rows*0.25), layer=pdk.get_glayer("met2"))
                        # met2_square_ref = Top_cell << met2_VSS_stripes
                        # met2_square_ref.movey(0).movex( x_move - met2_sq_dim/2 )

                        # via2_via_ref = Top_cell << via2_via
                        # via2_via_ref.movey(cell_height + space_bet_rows/2 - via2_via_dim/2).movex( x_move - via2_via_dim/2)

                ## Contacts on Poly trunk
                for con in range(finger - 1):
                    y_move = (
                        cell_height * 2 + space_bet_rows * (j) + poly_trunk_center_y
                    )
                    x_move = (
                        cell_width * i
                        + space_bet_mult * i
                        + poly_left_edge
                        + poly_width / 2
                        + poly_finger2finger_x / 2
                        + con * poly_finger2finger_x
                    )

                    mcon_via_ref = Top_cell << mcon_via
                    mcon_via_ref.movey(
                        y_move - pdk.get_grule("mcon")["width"] / 2
                    ).movex(x_move - pdk.get_grule("mcon")["width"] / 2)

                    met1_square_ref = Top_cell << met1_square
                    met1_square_ref.movey(y_move - met1_sq_dim / 2).movex(
                        x_move - met1_sq_dim / 2
                    )

                    via1_via_ref = Top_cell << via1_via
                    via1_via_ref.movey(y_move - via1_via_dim / 2).movex(
                        x_move - via1_via_dim / 2
                    )

                    met2_square_ref = Top_cell << met2_square
                    met2_square_ref.movey(y_move - met2_sq_dim / 2).movex(
                        x_move - met2_sq_dim / 2
                    )

                    if i == 0:
                        met2_poly_ext_1_ref = Top_cell << met2_poly_ext_1
                        met2_poly_ext_1_ref.movey(y_move - met2_sq_dim / 2).movex(
                            x_move - met2_sq_dim / 2
                        )

                        via2_via_ref = Top_cell << via2_via
                        via2_via_ref.movey(
                            met2_poly_ext_1_height
                            - met2_sq_dim
                            + y_move
                            - via2_via_dim / 2
                        ).movex(x_move - via2_via_dim / 2)

                        met3_poly_ext_ref = Top_cell << met3_poly_ext
                        met3_poly_ext_ref.movey(
                            y_move + met2_poly_ext_1_height - met2_sq_dim - via2_via_dim
                        ).movex(-2)

                        # Connecting to trunk
                        via2_via_ref = Top_cell << via2_via
                        via2_via_ref.movey(
                            met2_poly_ext_1_height
                            - met2_sq_dim
                            + y_move
                            - via2_via_dim / 2
                        ).movex(-1 + via2_via_dim / 2)

                        # Connecting trunk

                    if i == 1:
                        met2_poly_ext_2_ref = Top_cell << met2_poly_ext_2
                        met2_poly_ext_2_ref.movey(y_move - met2_sq_dim / 2).movex(
                            x_move - met2_sq_dim / 2
                        )

                        via2_via_ref = Top_cell << via2_via
                        via2_via_ref.movey(
                            met2_poly_ext_2_height
                            - met2_sq_dim
                            + y_move
                            - via2_via_dim / 2
                        ).movex(x_move - via2_via_dim / 2)

                        met3_poly_ext_ref = Top_cell << met3_poly_ext
                        met3_poly_ext_ref.movey(
                            y_move + met2_poly_ext_2_height - met2_sq_dim - via2_via_dim
                        ).movex(-2)

                        via2_via_ref = Top_cell << via2_via
                        via2_via_ref.movey(
                            met2_poly_ext_2_height
                            - met2_sq_dim
                            + y_move
                            - via2_via_dim / 2
                        ).movex(-2 + via2_via_dim / 2)

            if j == 0:
                ##poly trunk
                poly_trunk = Top_cell << poly_ext_trunk_ref
                poly_trunk.movex(
                    poly_left_edge + cell_width * i + space_bet_mult * i
                ).movey(-poly_ext_trunk_height + cell_height * j + space_bet_rows * (j))
                poly_trunk_center_y = (poly_trunk.ymax - poly_trunk.ymin) / 2

                ## Drain Stripes
                for con in range(finger + 1):
                    if con % 2 != 0:
                        y_move = cell_height + space_bet_rows * 0.3
                        x_move = (
                            cell_width * i
                            + space_bet_mult * i
                            + poly_left_edge
                            + poly_width / 2
                            - poly_finger2finger_x / 2
                            + con * poly_finger2finger_x
                        )

                        ## Drain extensions
                        met3_Drain_trunk_ref = Top_cell << met3_Drain_trunk
                        met3_Drain_trunk_ref.movex(
                            cell_width * i + space_bet_mult * i
                        ).movey(y_move - met3_sq_dim / 2)

                        ## Drain extension connecting via
                        if i == 1:
                            via2_via_ref = Top_cell << via2_via
                            via2_via_ref.movey(y_move - via2_via_dim / 2).movex(
                                cell_width * (i) + space_bet_mult * i + 0.3
                            )
                        met2_Drain_stripes = gf.components.rectangle(
                            size=(met2_sq_dim, cell_height + space_bet_rows * 0.3),
                            layer=pdk.get_glayer("met2"),
                        )
                        met2_square_ref = Top_cell << met2_Drain_stripes
                        met2_square_ref.movey(0 + met2_sq_dim + 0.05).movex(
                            x_move - met2_sq_dim / 2
                        )

                        via2_via_ref = Top_cell << via2_via
                        via2_via_ref.movey(y_move - via2_via_dim / 2).movex(
                            x_move - via2_via_dim / 2
                        )

                ## VSS Stripes
                for con in range(finger + 1):
                    if con % 2 == 0:
                        y_move = cell_height + space_bet_rows * 0.1
                        x_move = (
                            cell_width * i
                            + space_bet_mult * i
                            + poly_left_edge
                            + poly_width / 2
                            - poly_finger2finger_x / 2
                            + con * poly_finger2finger_x
                        )

                        ## VSS extensions
                        met3_VSS_trunk_ref = Top_cell << met3_VSS_trunk
                        met3_VSS_trunk_ref.movex(
                            cell_width * i + space_bet_mult * i
                        ).movey(y_move - met3_sq_dim / 2)

                        met2_VSS_stripes = gf.components.rectangle(
                            size=(met2_sq_dim, cell_height + space_bet_rows * 0.25),
                            layer=pdk.get_glayer("met2"),
                        )
                        met2_square_ref = Top_cell << met2_VSS_stripes
                        met2_square_ref.movey(0 - met2_sq_dim - 0.15).movex(
                            x_move - met2_sq_dim / 2
                        )

                        via2_via_ref = Top_cell << via2_via
                        via2_via_ref.movey(y_move - via2_via_dim / 2).movex(
                            x_move - via2_via_dim / 2
                        )

                ## Contacts on Poly trunk
                for con in range(finger - 1):
                    y_move = (
                        -poly_ext_trunk_height
                        + cell_height * j
                        + space_bet_rows * (j)
                        + poly_trunk_center_y
                    )
                    x_move = (
                        cell_width * i
                        + space_bet_mult * i
                        + poly_left_edge
                        + poly_width / 2
                        + poly_finger2finger_x / 2
                        + con * poly_finger2finger_x
                    )

                    mcon_via_ref = Top_cell << mcon_via
                    mcon_via_ref.movey(
                        y_move - pdk.get_grule("mcon")["width"] / 2
                    ).movex(x_move - pdk.get_grule("mcon")["width"] / 2)

                    met1_square_ref = Top_cell << met1_square
                    met1_square_ref.movey(y_move - met1_sq_dim / 2).movex(
                        x_move - met1_sq_dim / 2
                    )

                    via1_via_ref = Top_cell << via1_via
                    via1_via_ref.movey(y_move - via1_via_dim / 2).movex(
                        x_move - via1_via_dim / 2
                    )

                    met2_square_ref = Top_cell << met2_square
                    met2_square_ref.movey(y_move - met2_sq_dim / 2).movex(
                        x_move - met2_sq_dim / 2
                    )

                    if i == 1:
                        met2_poly_ext_1_ref = Top_cell << met2_poly_ext_1
                        met2_poly_ext_1_ref.movey(
                            met2_sq_dim
                            - met2_poly_ext_1_height
                            + y_move
                            - met2_sq_dim / 2
                        ).movex(x_move - met2_sq_dim / 2)

                        via2_via_ref = Top_cell << via2_via
                        via2_via_ref.movey(
                            met2_sq_dim
                            - met2_poly_ext_1_height
                            + y_move
                            - via2_via_dim / 2
                        ).movex(x_move - via2_via_dim / 2)

                        met3_poly_ext_ref = Top_cell << met3_poly_ext
                        met3_poly_ext_ref.movey(
                            met2_sq_dim - met2_poly_ext_1_height + y_move - via2_via_dim
                        ).movex(-2)

                        via2_via_ref = Top_cell << via2_via
                        via2_via_ref.movey(
                            met2_sq_dim
                            - met2_poly_ext_1_height
                            + y_move
                            - via2_via_dim / 2
                        ).movex(-2 + via2_via_dim / 2)

                    if i == 0:
                        met2_poly_ext_2_ref = Top_cell << met2_poly_ext_2
                        met2_poly_ext_2_ref.movey(
                            met2_sq_dim
                            - met2_poly_ext_2_height
                            + y_move
                            - met2_sq_dim / 2
                        ).movex(x_move - met2_sq_dim / 2)

                        via2_via_ref = Top_cell << via2_via
                        via2_via_ref.movey(
                            met2_sq_dim
                            - met2_poly_ext_2_height
                            + y_move
                            - via2_via_dim / 2
                        ).movex(x_move - via2_via_dim / 2)

                        met3_poly_ext_ref = Top_cell << met3_poly_ext
                        met3_poly_ext_ref.movey(
                            met2_sq_dim - met2_poly_ext_2_height + y_move - via2_via_dim
                        ).movex(-2)

                        via2_via_ref = Top_cell << via2_via
                        via2_via_ref.movey(
                            met2_sq_dim
                            - met2_poly_ext_2_height
                            + y_move
                            - via2_via_dim / 2
                        ).movex(-1 + via2_via_dim / 2)

    """
    #VSS Met2 trunk
    met2_VSS_width = 0.5 + cell_width*(mult/rows) + 0.75 + space_bet_mult


    met2_tb = gf.components.rectangle(size=(met2_VSS_width,met2_height), layer=met2_drawing)
    #VSS Top trunk
    met2_VSS_top_ref = Top_cell << met2_tb
    met2_VSS_top_ref.movex(-0.5).movey(cell_height*rows + space_bet_rows + 0.5)

    #VSS Bottom trunk
    met2_VSS_bottom_ref = Top_cell << met2_tb
    met2_VSS_bottom_ref.movex(-0.5).movey(-0.5 - 0.23)

    # GM1 trunk
    met2_GM1_ref = Top_cell << met2_tb
    met2_GM1_ref.movex(-0.5).movey(cell_height + 0.5)

    # DM1 trunk
    met2_DM1_ref = Top_cell << met2_tb
    met2_DM1_ref.movex(-0.5).movey(cell_height + 0.5 + met2_height + 0.25)

    # DM2 trunk
    met2_DM2_ref = Top_cell << met2_tb
    met2_DM2_ref.movex(-0.5).movey(cell_height + 0.5 + met2_height * 2 + 0.25*2 )

    # GM2 trunk
    met2_GM2_ref = Top_cell << met2_tb
    met2_GM2_ref.movex(-0.5).movey(cell_height + 0.5 + met2_height * 3 + 0.25*3 )




    #Extending Poly trunk
    for i in range(int(mult/rows)):
        for j in range(rows):


            met1_height = 1.95
            met1_width = 0.23

            met1_row_conn_rect = gf.components.rectangle(size=(met1_width,met1_height), layer=met1_drawing)

            if j == 0 :
                for fin in range(finger-1):
                    met1_row_conn_rect_ref = Top_cell << met1_row_conn_rect
                    met1_row_conn_rect_ref.movex(0.16 + space_bet_mult*i + cell_width*i + 1.1*fin).movey( cell_height*j -0.73 )

            if j == 1 :
                for fin in range(finger-1):
                    met1_row_conn_rect_ref = Top_cell << met1_row_conn_rect
                    met1_row_conn_rect_ref.movex(0.16 + space_bet_mult*i + cell_width*i + 1.1*fin).movey( cell_height*j  + space_bet_rows*(j) - 0.73 + 0.85)

    #Extending Drain trunk
    for i in range(int(mult/rows)):
        for j in range(rows):


            met1_height_1 = 1.95 - 0.3
            met1_height_2 = 1.95 + 0.96
            met1_width = 0.23

            met1_row_conn_rect_1 = gf.components.rectangle(size=(met1_width,met1_height_1), layer=met1_drawing)
            met1_row_conn_rect_2 = gf.components.rectangle(size=(met1_width,met1_height_2), layer=met1_drawing)

            if j == 0 :
                if i == 0:
                    for fin in range(finger-2):
                        met1_row_conn_rect_ref = Top_cell << met1_row_conn_rect_1
                        met1_row_conn_rect_ref.movex(0.16 + 0.55 + space_bet_mult*i + cell_width*i + 1.1*fin).movey( cell_height*j -0.73 + 0.85 )

                if i == 1:
                    for fin in range(finger-2):
                        met1_row_conn_rect_ref = Top_cell << met1_row_conn_rect_2
                        met1_row_conn_rect_ref.movex(0.16 + 0.55 + space_bet_mult*i + cell_width*i + 1.1*fin).movey( cell_height*j -0.73 + 0.85 )

            #if j == 1 :
            #    for fin in range(finger-1):
            #        met1_row_conn_rect_ref = Top_cell << met1_row_conn_rect
            #        met1_row_conn_rect_ref.movex(0.16 + space_bet_mult*i + cell_width*i + 1.1*fin).movey( cell_height*j  + space_bet_rows*(j) - 0.73 + 0.85)


    for i in range(mult):
        #for j in range(2):
        if (i%2 == 0) :
            poly_width = 0.25
            poly_height = cell_height + 0.1

            poly_row_conn_rect = gf.components.rectangle(size=(poly_width,poly_height), layer=poly_drawing)
            poly_row_conn_rect_ref = Top_cell << poly_row_conn_rect

            poly_row_conn_rect_ref.movex(cell_width*i - (cell_width*i/2) + 0.425).movey(-0.1)

        elif (i%2 != 0) :
            poly_width = 0.25
            poly_height = cell_height + 0.1

            poly_row_conn_rect = gf.components.rectangle(size=(poly_width,poly_height), layer=poly_drawing)
            poly_row_conn_rect_ref = Top_cell << poly_row_conn_rect

            poly_row_conn_rect_ref.movex(cell_width*i - (cell_width*i/2) + 0.425).movey(0)

            #via_height = 0.17
            #via_width = 0.17
            #via_rect = gf.components.rectangle(size=(via_height,via_width), #layer=via_drawing)

            #via_rect_ref = Top_cell << via_rect
            #via_rect_ref.movex(cell_width*i + 0.425 + 0.04).movey(0.9)

    """
    """
    for i in range(mult):
        #for j in range(2):
            met1_height = 1.59
            met1_width = 0.23

            met1_row_conn_rect = gf.components.rectangle(size=(met1_width,met1_height), layer=met1_drawing)

            met1_row_conn_rect_ref = Top_cell << met1_row_conn_rect
            met1_row_conn_rect_ref.movex(cell_width*i + 0.16).movey(0.125)

            via_height = 0.17
            via_width = 0.17
            via_rect = gf.components.rectangle(size=(via_height,via_width), layer=via_drawing)

            #via_rect_ref = Top_cell << via_rect
            #via_rect_ref.movex(cell_width*i + 0.16 + 0.03).movey(0.9)
    """
    """'
    met2_pin_width = 0.23
    met2_pin_height = 0.23

    met2_pin_rect = gf.components.rectangle(size=(met2_pin_width,met2_pin_height), layer=met2_pin)

    poly_pin_width = poly_pin_height = 0.25
    poly_pin_rect = gf.components.rectangle(size=(poly_pin_width,poly_pin_height), layer=poly_pin)

    ## Center VSS M2 path
    #met2_center_width = 0.5 + cell_width*mult
    #met2_center_height = 0.23
    #met2_center = gf.components.rectangle(size=(met2_center_width,#met2_center_height), layer=met2_drawing)

    #met2_center_ref = Top_cell << met2_center

    #met2_center_ref.movex(-0.5).movey(0.9 - 0.03)

    #met2_pin_VSS = Top_cell << met2_pin_rect
    #met2_pin_VSS.movex(-0.5).movey(0.9 - 0.03)

    ## VSS pin label
    #met2_label_VSS = Top_cell.add_label("VSS", position=(-0.5,0.9 - 0.03), layer=met2_label, magnification=0.2)

    #G_M1 and G_M2 Poly Trunk
    poly_tb_width = 0.5 + cell_width*((mult+1)/2)
    poly_tb_height = 0.25

    poly_tb_ref = gf.components.rectangle(size=(poly_tb_width,poly_tb_height), layer=poly_drawing)
    ## Top poly trunk

    #G_M1
    poly_top_G_M1 = Top_cell << poly_tb_ref
    poly_top_G_M1.movex(-0.5).movey(cell_height + 0.1)

    poly_pin_G_M1 = Top_cell << poly_pin_rect
    poly_pin_G_M1.movex(-0.5).movey(cell_height + 0.1)

    poly_label_G_M1 = Top_cell.add_label("G_M1", position=(-0.5 + 0.25,cell_height + 0.1 + 0.25), layer=poly_label, magnification=0.2)

    #G_M2
    poly_top_G_M2 = Top_cell << poly_tb_ref
    poly_top_G_M2.movex(-0.5).movey(-0.23- 0.1)

    poly_pin_G_M2 = Top_cell << poly_pin_rect
    poly_pin_G_M2.movex(-0.5).movey( -0.23 - 0.1)

    poly_label_G_M2 = Top_cell.add_label("G_M2", position=(-0.5 + 0.25, -0.23 - 0.1 +0.25), layer=poly_label, magnification=0.2)

    #D_M1 and D_M2 Metal trunk
    met2_tb_width = 0.5 + cell_width*((mult+1)/2) + 0.75
    met2_tb_height = 0.23

    met2_tb = gf.components.rectangle(size=(met2_tb_width,met2_tb_height), layer=met2_drawing)

    ##Top trunk

    #D_M1
    met2_top_I_in_ref = Top_cell << met2_tb
    met2_top_I_in_ref.movex(-0.5).movey(cell_height + 0.5)

    met2_pin_I_in = Top_cell << met2_pin_rect
    met2_pin_I_in.movex(-0.5).movey(cell_height + 0.5)

    met2_label_I_in = Top_cell.add_label("VSS", position=(-0.5 + 0.25,cell_height + 0.5 + 0.2), layer=met2_label, magnification=0.2)

    #D_M2
    met2_top_I_out_ref = Top_cell << met2_tb
    met2_top_I_out_ref.movex(-0.5).movey(cell_height + 0.5 + 0.5)

    met2_pin_I_out = Top_cell << met2_pin_rect
    met2_pin_I_out.movex(-0.5).movey(cell_height + 0.5 + 0.5)

    met2_label_I_out = Top_cell.add_label("D_M1", position=(-0.5 + 0.25, cell_height + 1.0 + 0.25), layer=met2_label, magnification=0.2)

    ## Bottom trunk

    ##D_M1
    met2_bottom_I_in_ref = Top_cell << met2_tb
    met2_bottom_I_in_ref.movex(-0.5).movey(-0.5 - 0.23)

    ##D_M2
    met2_bottom_I_out_ref = Top_cell << met2_tb
    met2_bottom_I_out_ref.movex(-0.5).movey(-0.5 - 0.23 - 0.5)

    met2_pin_I_in = Top_cell << met2_pin_rect
    met2_pin_I_in.movex(-0.5).movey(-0.5 - 0.23 - 0.5)

    met2_label_I_in = Top_cell.add_label("D_M1", position=(-0.5 + 0.25,-0.5 - 0.23 - 0.5 + 0.25), layer=met2_label, magnification=0.2)


    ## Right end Trunks
    met1_right_width = 0.23
    met1_right_height_1 = cell_height + (0.5*2) + (0.23*2)
    met1_right_height_2 = 3.46

    met1_right_trunk_1 = gf.components.rectangle(size=(met1_right_width,met1_right_height_1), layer=met1_drawing)
    met1_right_trunk_2 = gf.components.rectangle(size=(met1_right_width,met1_right_height_2), layer=met1_drawing)

    ## Right - I_in trunk
    met1_right_trunk_ref_I_in = Top_cell << met1_right_trunk_1
    trunk_1_x_shift = 0.5 + cell_width*((mult+1)/2)
    met1_right_trunk_ref_I_in.movex(trunk_1_x_shift).movey( -(0.5 + 0.23))

    ## Right - I_out trunk
    #met1_right_trunk_ref_I_out = Top_cell << met1_right_trunk_2
    #trunk_2_x_shift = 0.5 + trunk_1_x_shift
    #met1_right_trunk_ref_I_out.movex(trunk_2_x_shift).movey(-1.23)

    via_height = 0.17
    via_width = 0.17
    via_rect = gf.components.rectangle(size=(via_height,via_width), layer=via_drawing)

    via_rect_ref = Top_cell << via_rect
    via_rect_ref.movex(trunk_1_x_shift + 0.03).movey(-(0.5+0.23) + 0.03)
    via_rect_ref = Top_cell << via_rect
    via_rect_ref.movex(trunk_1_x_shift + 0.03).movey(met1_right_height_1 - (0.5 + 0.23) -0.17 - 0.03)

    #via_rect_ref = Top_cell << via_rect
    #via_rect_ref.movex(trunk_2_x_shift + 0.03).movey(-1.23 + 0.03)
    #via_rect_ref = Top_cell << via_rect
    #via_rect_ref.movex(trunk_2_x_shift + 0.03).movey(met1_right_height_2 - 1.23 -0.17 - 0.03)


    ##Connecting to trunk
    ## i --->  col
    ## j --->  row
    connect = "up"
    for i in range(mult):
        #for j in range(2):
            met1_tr_conn_height_1 = (cell_height + 0.5 + 0.23 ) - 0.125 ##1.275
            met1_tr_conn_height_2 = (cell_height + 1.0 + 0.23 ) - 0.125 ##1.775
            met1_tr_conn_width = 0.23

            via_height = 0.17
            via_width = 0.17
            via_rect = gf.components.rectangle(size=(via_height,via_width), layer=via_drawing)

            met1_tr_conn_rect_1 = gf.components.rectangle(size=(met1_tr_conn_width,met1_tr_conn_height_1), layer=met1_drawing)

            met1_tr_conn_rect_2 = gf.components.rectangle(size=(met1_tr_conn_width,met1_tr_conn_height_2), layer=met1_drawing)

            if(i == 0):
                    met1_tr_conn_rect_ref = Top_cell << met1_tr_conn_rect_2
                    met1_tr_conn_rect_ref.movex( 0.16).movey(0.125)

                    via_rect_ref = Top_cell << via_rect
                    via_rect_ref.movex(0.16 + 0.03).movey(0.125 + met1_tr_conn_height_2 - 0.17 - 0.03)

            if(i%2 != 0):
                #if((i+3)%2 == 0):
                if connect == "up":
                    print("\nMult position")
                    print(i)
                    met1_tr_conn_rect_ref = Top_cell << met1_tr_conn_rect_2
                    met1_tr_conn_rect_ref.movex(cell_width*i - (cell_width*i/2) + 0.16+0.55).movey(-1.23)

                    via_rect_ref = Top_cell << via_rect
                    via_rect_ref.movex(cell_width*i - (cell_width*i/2) + 0.16 + 0.55 + 0.03).movey(-1.23 + 0.03)
                    connect = "down"
                else:
                    print("\nElse ---- > Mult position")
                    print(i)
                    met1_tr_conn_rect_ref = Top_cell << met1_tr_conn_rect_2
                    met1_tr_conn_rect_ref.movex(cell_width*i - (cell_width*i/2) + 0.16+0.55).movey(0.125)

                    via_rect_ref = Top_cell << via_rect
                    via_rect_ref.movex(cell_width*i - (cell_width*i/2) + 0.16 + 0.55 + 0.03).movey(0.125 + met1_tr_conn_height_2 - 0.17 - 0.03)
                    connect = "up"

            if(i%2 == 0):
                if(i%4 != 0):

                    met1_tr_conn_rect_ref = Top_cell << met1_tr_conn_rect_1
                    met1_tr_conn_rect_ref.movex(cell_width*i - (cell_width*i/2) + 0.16+0.55).movey(-0.73)

                    via_rect_ref = Top_cell << via_rect
                    via_rect_ref.movex(cell_width*i - (cell_width*i/2) + 0.16 + 0.55 + 0.03).movey(-0.73 + 0.03)
                else:
                    met1_tr_conn_rect_ref = Top_cell << met1_tr_conn_rect_1
                    met1_tr_conn_rect_ref.movex(cell_width*i - (cell_width*i/2) + 0.16+0.55).movey(0.125)

                    via_rect_ref = Top_cell << via_rect
                    via_rect_ref.movex(cell_width*i - (cell_width*i/2) + 0.16 + 0.55 + 0.03).movey(0.125 + met1_tr_conn_height_1 - 0.17 - 0.03)
    """

    return Top_cell


# Top_cell = multiplier(sky130_mapped_pdk, sdlayer="n+s/d",fingers=2,routing=True,dummy=False)
# print(Top_cell.x, Top_cell.y)
## Top cell creation
Top_cell = diff_pair_top_updated(mult=2, finger=4, cell_height=1.34)
# Top_cell = nmos(cell_height=1.34, finger=3)
Top_cell.show()
