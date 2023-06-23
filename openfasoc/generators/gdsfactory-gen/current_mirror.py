import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk
from gdsfactory.component import Component, ComponentReference

from gdsfactory.generic_tech import get_generic_pdk
import sky130

gf.config.rich_output()
PDK = get_generic_pdk()
PDK.activate()

pwell_drawing = (64,13)
dnwell_drawing = (64,18)
nwell_drawing = (64,20)
outline_ref = (236,0)
diff_drawing = (65,20)
psdm_drawing = (94,20)
nsdm_drawing = (93,44)
poly_drawing = (66,20)
licon1_drawing = (66, 44)
npc_drawing = (95, 20)
li1_drawing = (67,20)
mcon_drawing = (67,44)
met1_drawing = (68,20)
met1_label = (68,5)
met1_pin = (68,16)
via_drawing = (68,44)
met2_drawing = (69,20)
met2_label = (69,5)
met2_pin = (69,16)
via2_drawing = (69,44)
met3_drawing = (70,20)
met3_label = (70,5)
met3_pin = (70,16)
text_drawing = (83,44)

@gf.cell
def nmos() -> Component:
    c = Component()

    ##nsdm
    nsdm_height = 0.67
    nsdm_width = 1.1

    nsdm_outline_rect = gf.components.rectangle(size=(nsdm_width,nsdm_height), layer=nsdm_drawing)
    nsdm_outline_rect_ref = c << nsdm_outline_rect

    ##poly
    poly_width = 0.25
    poly_height = 0.68

    poly_rect = gf.components.rectangle(size=(poly_width,poly_height), layer=poly_drawing)
    poly_rect_ref = c << poly_rect

    poly_rect_ref.movex(0.425).movey(-0.005)

    ##diff
    diff_width = 0.85
    diff_height = 0.42
    diff_rect = gf.components.rectangle(size=(diff_width,diff_height), layer=diff_drawing)
    diff_rect_ref = c << diff_rect

    diff_rect_ref.movex(0.125).movey(0.125)

    ##li1_drawing
    li1_height = 0.5
    li1_width = 0.17
    li1_rect = gf.components.rectangle(size=(li1_width,li1_height), layer=li1_drawing)

    li1_rect_ref1 = c << li1_rect
    li1_rect_ref1.movey(0.085).movex(0.19)
    li1_rect_ref2 = c << li1_rect
    li1_rect_ref2.movey(0.085).movex(0.74)

    ##mcon
    mcon_height = 0.17
    mcon_width = 0.17

    mcon_rect = gf.components.rectangle(size=(mcon_width,mcon_height), layer=mcon_drawing)
    mcon_rect_ref1 = c << mcon_rect
    mcon_rect_ref1.movey(0.25).movex(0.19)
    mcon_rect_ref2 = c << mcon_rect
    mcon_rect_ref2.movey(0.25).movex(0.74)

    ##licon1
    licon1_height = 0.17
    licon1_width = 0.17

    licon1_rect = gf.components.rectangle(size=(licon1_width,licon1_height), layer=licon1_drawing)
    licon1_rect_ref1 = c << licon1_rect
    licon1_rect_ref1.movey(0.25).movex(0.19)
    licon1_rect_ref2 = c << licon1_rect
    licon1_rect_ref2.movey(0.25).movex(0.74)

    ##met1
    met1_height = 0.42
    met1_width = 0.23

    met1_rect = gf.components.rectangle(size=(met1_width,met1_height), layer=met1_drawing)

    met1_rect_ref1 = c << met1_rect
    met1_rect_ref1.movey(0.125).movex(0.16)

    met1_rect_ref2 = c << met1_rect
    met1_rect_ref2.movey(0.125).movex(0.71)

    ##labels

    met1_label_s = c.add_label("S", position=(0.255,0.36), layer=met1_label, magnification=0.2)
    met1_label_d = c.add_label("D", position=(0.81,0.36), layer=met1_label, magnification=0.2)
    #c.add_label()

    return c

@gf.cell
def cmirror_top(mult=3) -> Component:

    Top_cell = gf.Component("top")

    cmirror = nmos()
    cell_height = 0.67
    cell_width = 1.1
    space_bet_rows = 0.66
    #mult = 8

    ##pwell
    pwell_width = (cell_width*mult) + 0.11
    pwell_height = (cell_height*2) + space_bet_rows + 0.11

    pwell_rect = gf.components.rectangle(size=(pwell_width,pwell_height), layer=pwell_drawing)
    pwell_rect_ref = Top_cell << pwell_rect

    pwell_rect_ref.movex(-0.055).movey(-0.055)

    ##dnwell
    dnwell_width = (cell_width*mult) + 0.91
    dnwell_height = (cell_height*2) + space_bet_rows + 0.91

    dnwell_rect = gf.components.rectangle(size=(dnwell_width,dnwell_height), layer=dnwell_drawing)
    dnwell_rect_ref = Top_cell << dnwell_rect

    dnwell_rect_ref.movex(-0.455).movey(-0.455)


    for i in range(mult):
        for j in range(2):
            print(j)
            ref = Top_cell << cmirror
            ref.movex(cell_width*i).movey(cell_height*(j) + space_bet_rows*(j))

    for i in range(mult):
        for j in range(2):
            poly_width = 0.25
            poly_height = 1.85

            poly_row_conn_rect = gf.components.rectangle(size=(poly_width,poly_height), layer=poly_drawing)
            poly_row_conn_rect_ref = Top_cell << poly_row_conn_rect

            poly_row_conn_rect_ref.movex(cell_width*i + 0.425).movey(-0.005)

            via_height = 0.17
            via_width = 0.17
            via_rect = gf.components.rectangle(size=(via_height,via_width), layer=via_drawing)

            via_rect_ref = Top_cell << via_rect
            via_rect_ref.movex(cell_width*i + 0.425 + 0.04).movey(0.9)


    for i in range(mult):
        for j in range(2):
            met1_height = 1.59
            met1_width = 0.23

            met1_row_conn_rect = gf.components.rectangle(size=(met1_width,met1_height), layer=met1_drawing)

            met1_row_conn_rect_ref = Top_cell << met1_row_conn_rect
            met1_row_conn_rect_ref.movex(cell_width*i + 0.16).movey(0.125)

            via_height = 0.17
            via_width = 0.17
            via_rect = gf.components.rectangle(size=(via_height,via_width), layer=via_drawing)

            via_rect_ref = Top_cell << via_rect
            via_rect_ref.movex(cell_width*i + 0.16 + 0.03).movey(0.9)

    met2_pin_width = 0.23
    met2_pin_height = 0.23

    met2_pin_rect = gf.components.rectangle(size=(met2_pin_width,met2_pin_height), layer=met2_pin)

    ## Center VSS M2 path
    met2_center_width = 0.5 + cell_width*mult
    met2_center_height = 0.23
    met2_center = gf.components.rectangle(size=(met2_center_width,met2_center_height), layer=met2_drawing)

    met2_center_ref = Top_cell << met2_center

    met2_center_ref.movex(-0.5).movey(0.9 - 0.03)

    met2_pin_VSS = Top_cell << met2_pin_rect
    met2_pin_VSS.movex(-0.5).movey(0.9 - 0.03)

    met2_label_I_in = Top_cell.add_label("VSS", position=(-0.5,0.9 - 0.03), layer=met2_label, magnification=0.2)

    #Iin and Iout Metal trunk
    met2_tb_width = 0.5 + cell_width*mult + 1.25
    met2_tb_height = 0.23

    met2_tb = gf.components.rectangle(size=(met2_tb_width,met2_tb_height), layer=met2_drawing)

    ##Top trunk
    met2_top_I_in_ref = Top_cell << met2_tb
    met2_top_I_in_ref.movex(-0.5).movey(2.5)

    met2_pin_I_in = Top_cell << met2_pin_rect
    met2_pin_I_in.movex(-0.5).movey(2.5)

    met2_label_I_in = Top_cell.add_label("I_in", position=(-0.5,2.5), layer=met2_label, magnification=0.2)

    met2_top_I_out_ref = Top_cell << met2_tb
    met2_top_I_out_ref.movex(-0.5).movey(2.5 + 0.5)

    met2_pin_I_out = Top_cell << met2_pin_rect
    met2_pin_I_out.movex(-0.5).movey(2.5 + 0.5)

    met2_label_I_out = Top_cell.add_label("I_out", position=(-0.5,2.5+0.5), layer=met2_label, magnification=0.2)

    ## Bottom trunk
    met2_bottom_I_in_ref = Top_cell << met2_tb
    met2_bottom_I_in_ref.movex(-0.5).movey(-0.73)

    met2_bottom_I_out_ref = Top_cell << met2_tb
    met2_bottom_I_out_ref.movex(-0.5).movey(-0.73 - 0.5)


    ## Right end Trunks
    met1_right_width = 0.23
    met1_right_height_1 = 4.46
    met1_right_height_2 = 3.46

    met1_right_trunk_1 = gf.components.rectangle(size=(met1_right_width,met1_right_height_2), layer=met1_drawing)
    met1_right_trunk_2 = gf.components.rectangle(size=(met1_right_width,met1_right_height_1), layer=met1_drawing)

    ## Right - I_in trunk
    met1_right_trunk_ref_I_in = Top_cell << met1_right_trunk_1
    trunk_1_x_shift = 0.5 + cell_width*mult 
    met1_right_trunk_ref_I_in.movex(trunk_1_x_shift).movey(-0.73)

    ## Right - I_out trunk
    met1_right_trunk_ref_I_out = Top_cell << met1_right_trunk_2
    trunk_2_x_shift = 0.5 + trunk_1_x_shift
    met1_right_trunk_ref_I_out.movex(trunk_2_x_shift).movey(-1.23)

    via_height = 0.17
    via_width = 0.17
    via_rect = gf.components.rectangle(size=(via_height,via_width), layer=via_drawing)

    via_rect_ref = Top_cell << via_rect
    via_rect_ref.movex(trunk_1_x_shift + 0.03).movey(-0.73 + 0.03)
    via_rect_ref = Top_cell << via_rect
    via_rect_ref.movex(trunk_1_x_shift + 0.03).movey(met1_right_height_2 - 0.73 -0.17 - 0.03)

    via_rect_ref = Top_cell << via_rect
    via_rect_ref.movex(trunk_2_x_shift + 0.03).movey(-1.23 + 0.03)
    via_rect_ref = Top_cell << via_rect
    via_rect_ref.movex(trunk_2_x_shift + 0.03).movey(met1_right_height_1 - 1.23 -0.17 - 0.03)


    ##Connecting to trunk
    ## i --->  col
    ## j --->  row
    for i in range(mult):
        for j in range(2):
            met1_tr_conn_height_1 = 1.275
            met1_tr_conn_height_2 = 1.775
            met1_tr_conn_width = 0.23

            via_height = 0.17
            via_width = 0.17
            via_rect = gf.components.rectangle(size=(via_height,via_width), layer=via_drawing)

            met1_tr_conn_rect_1 = gf.components.rectangle(size=(met1_tr_conn_width,met1_tr_conn_height_1), layer=met1_drawing)

            met1_tr_conn_rect_2 = gf.components.rectangle(size=(met1_tr_conn_width,met1_tr_conn_height_2), layer=met1_drawing)

            
            if(i%2 != 0):
                if(j%2 != 0):
                    met1_tr_conn_rect_ref = Top_cell << met1_tr_conn_rect_2
                    met1_tr_conn_rect_ref.movex(cell_width*i + 0.16+0.55).movey(-1.23)

                    via_rect_ref = Top_cell << via_rect
                    via_rect_ref.movex(cell_width*i + 0.16 + 0.55 + 0.03).movey(-1.23 + 0.03)
                else: 
                    met1_tr_conn_rect_ref = Top_cell << met1_tr_conn_rect_1
                    met1_tr_conn_rect_ref.movex(cell_width*i + 0.16+0.55).movey(1.455)

                    via_rect_ref = Top_cell << via_rect
                    via_rect_ref.movex(cell_width*i + 0.16 + 0.55 + 0.03).movey(1.455 + met1_tr_conn_height_1 - 0.17 - 0.03)
            else:
                if(j%2 != 0):
                    met1_tr_conn_rect_ref = Top_cell << met1_tr_conn_rect_1
                    met1_tr_conn_rect_ref.movex(cell_width*i + 0.16+0.55).movey(-0.73)

                    via_rect_ref = Top_cell << via_rect
                    via_rect_ref.movex(cell_width*i + 0.16 + 0.55 + 0.03).movey(-0.73 + 0.03)
                else:
                    met1_tr_conn_rect_ref = Top_cell << met1_tr_conn_rect_2
                    met1_tr_conn_rect_ref.movex(cell_width*i + 0.16+0.55).movey(1.455)

                    via_rect_ref = Top_cell << via_rect
                    via_rect_ref.movex(cell_width*i + 0.16 + 0.55 + 0.03).movey(1.455 + met1_tr_conn_height_2 - 0.17 - 0.03)
    return Top_cell

Top_cell = cmirror_top(2)
Top_cell.show()

