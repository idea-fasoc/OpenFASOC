from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
from fet import multiplier


@cell
def diff_pair(pdk, mult=3, fingers=3, cell_height=0.67) -> Component:
    pwell_drawing = pdk.get_glayer("pwell")
    dnwell_drawing = pdk.get_glayer("dnwell")
    poly_drawing = pdk.get_glayer("poly")

    Top_cell = Component("top")

    mult = mult * 2
    # mos_comp = nmos(cell_height, fingers)
    mos_comp = multiplier(
        pdk, sdlayer="n+s/d", fingers=fingers, routing=False, dummy=False
    )
    cell_height = mos_comp.ymax - mos_comp.ymin
    cell_width = mos_comp.xmax - mos_comp.xmin
    # cell_width = 1.1 + 0.55*(fingers-1)
    space_bet_rows = 4
    space_bet_mult = 1.5
    rows = 2

    ##pwell
    pwell_width = cell_width * (mult / rows) + 0.11 + space_bet_mult
    pwell_height = (cell_height * 1) * rows + 0.11 + space_bet_rows

    pwell_rect = rectangle(size=(pwell_width, pwell_height), layer=pwell_drawing)
    # pwell_rect_ref = Top_cell << pwell_rect
    # pwell_rect_ref.movex(-0.055).movey(-0.055)

    ##dnwell
    # dnwell_width = (cell_width*((mult+1)/2)) + 0.91
    dnwell_width = cell_width * (mult / rows) + 0.91 + space_bet_mult
    dnwell_height = (cell_height * 1) * rows + 0.91 + space_bet_rows
    dnwell_rect = rectangle(size=(dnwell_width, dnwell_height), layer=dnwell_drawing)
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
    met3_VSS_trunk = rectangle(
        size=(met3_VSS_trunk_width, met3_sq_dim), layer=pdk.get_glayer("met3")
    )

    met3_VSS_trunk_ref = Top_cell << met3_VSS_trunk
    met3_VSS_trunk_ref.movey(cell_height + space_bet_rows * 0.9 - met3_sq_dim / 2)

    met3_VSS_trunk_ref = Top_cell << met3_VSS_trunk
    met3_VSS_trunk_ref.movey(cell_height + space_bet_rows * 0.1 - met3_sq_dim / 2)

    met3_met2_VSS_trunk_height = space_bet_rows * 0.8 + met3_sq_dim
    met3_met2_VSS_trunk = rectangle(
        size=(met2_sq_dim, met3_met2_VSS_trunk_height), layer=pdk.get_glayer("met2")
    )

    met3_met2_VSS_trunk_ref = Top_cell << met3_met2_VSS_trunk
    met3_met2_VSS_trunk_ref.movey(
        cell_height + space_bet_rows * 0.1 - met3_sq_dim / 2
    ).movex(met3_VSS_trunk_width - met2_sq_dim)

    via2_via_dim = pdk.get_grule("via2")["min_width"]
    via2_via = rectangle(
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
                2 * pdk.get_grule("poly", "mcon")["min_separation"]
                + pdk.get_grule("mcon")["width"]
            )
            poly_finger2finger_x = poly_width + mcon_poly_space

            if fingers % 2 != 0:
                poly_left_edge = (
                    cell_width / 2
                    - poly_width / 2
                    - ((fingers - 1) / 2) * poly_finger2finger_x
                )
            else:
                poly_left_edge = (
                    cell_width / 2
                    - poly_width / 2
                    - poly_finger2finger_x / 2
                    - ((fingers / 2) - 1) * poly_finger2finger_x
                )

            poly_ext_trunk_width = poly_width + (fingers - 1) * poly_finger2finger_x

            ##poly_trunk
            # poly_ext_trunk_height = pdk.get_grule("poly")['min_width']
            poly_ext_trunk_height = 0.5
            poly_ext_trunk_ref = rectangle(
                size=(poly_ext_trunk_width, poly_ext_trunk_height), layer=poly_drawing
            )

            mcon_via = rectangle(
                size=(pdk.get_grule("mcon")["width"], pdk.get_grule("mcon")["width"]),
                layer=pdk.get_glayer("mcon"),
            )

            met1_sq_dim = max(
                pdk.get_grule("mcon")["width"]
                + 2 * pdk.get_grule("met1", "mcon")["min_enclosure"],
                pdk.get_grule("met1")["min_width"],
            )
            met1_square = rectangle(
                size=(met1_sq_dim, met1_sq_dim), layer=pdk.get_glayer("met1")
            )

            via1_via_dim = pdk.get_grule("via1")["min_width"]
            via1_via = rectangle(
                size=(via1_via_dim, via1_via_dim), layer=pdk.get_glayer("via1")
            )

            ##Change from 0.14 to 0.28
            met2_sq_dim = max(
                pdk.get_grule("via1")["min_width"]
                + 2 * pdk.get_grule("met2", "via1")["min_enclosure"],
                pdk.get_grule("met2")["min_width"],
            )
            met2_square = rectangle(
                size=(met2_sq_dim, met2_sq_dim), layer=pdk.get_glayer("met2")
            )

            met2_poly_ext_1_height = 1.5
            met2_poly_ext_2_height = met2_poly_ext_1_height + 1
            met2_poly_ext_1 = rectangle(
                size=(met2_sq_dim, met2_poly_ext_1_height), layer=pdk.get_glayer("met2")
            )
            met2_poly_ext_2 = rectangle(
                size=(met2_sq_dim, met2_poly_ext_2_height), layer=pdk.get_glayer("met2")
            )

            via2_via_dim = pdk.get_grule("via2")["min_width"]
            via2_via = rectangle(
                size=(via2_via_dim, via2_via_dim), layer=pdk.get_glayer("via2")
            )

            via3_via_dim = pdk.get_grule("via3")["min_width"]
            via3_via = rectangle(
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
            met3_poly_ext = rectangle(
                size=(met3_poly_ext_width, met3_sq_dim), layer=pdk.get_glayer("met3")
            )

            met2_poly_ext_outer_trunk_h = cell_height * 2 + space_bet_rows + 2.7 * 2
            met2_poly_ext_outer_trunk = rectangle(
                size=(met2_sq_dim, met2_poly_ext_outer_trunk_h),
                layer=pdk.get_glayer("met2"),
            )

            met2_poly_ext_outer_trunk_ref = Top_cell << met2_poly_ext_outer_trunk
            met2_poly_ext_outer_trunk_ref.movex(-2).movey(-2.7)
            met2_poly_ext_outer_trunk_ref = Top_cell << met2_poly_ext_outer_trunk
            met2_poly_ext_outer_trunk_ref.movex(-1).movey(-2.7)

            ## VSS extensions
            met3_VSS_trunk_width = cell_width
            met3_VSS_trunk = rectangle(
                size=(met3_VSS_trunk_width, met3_sq_dim), layer=pdk.get_glayer("met3")
            )

            ## Drain extensions
            met3_Drain_trunk_width = cell_width
            met3_Drain_trunk = rectangle(
                size=(met3_Drain_trunk_width, met3_sq_dim), layer=pdk.get_glayer("met3")
            )

            ## Drain connections using met3
            ## In the center
            met3_Drain_conn_width = space_bet_mult + 0.3 * 3 + via2_via_dim
            met3_Drain_conn = rectangle(
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
            met2_met3_Drain_conn = rectangle(
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
            met2_Drain_conn = rectangle(
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
            met3_ext_conn = rectangle(
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
                for con in range(fingers + 1):
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
                        met2_Drain_stripes = rectangle(
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
                for con in range(fingers + 1):
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

                        met2_VSS_stripes = rectangle(
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
                for con in range(fingers + 1):
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

                        # met2_VSS_stripes = rectangle(size=( met2_sq_dim, cell_height + space_bet_rows*0.25), layer=pdk.get_glayer("met2"))
                        # met2_square_ref = Top_cell << met2_VSS_stripes
                        # met2_square_ref.movey(0).movex( x_move - met2_sq_dim/2 )

                        # via2_via_ref = Top_cell << via2_via
                        # via2_via_ref.movey(cell_height + space_bet_rows/2 - via2_via_dim/2).movex( x_move - via2_via_dim/2)

                ## Contacts on Poly trunk
                for con in range(fingers - 1):
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
                for con in range(fingers + 1):
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
                        met2_Drain_stripes = rectangle(
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
                for con in range(fingers + 1):
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

                        met2_VSS_stripes = rectangle(
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
                for con in range(fingers - 1):
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

    return Top_cell


if __name__ == "__main__":
    from PDK.util.standard_main import pdk

    Top_cell = diff_pair(pdk, mult=2, fingers=4, cell_height=1.34)
    Top_cell.show()
