########################################################################################################################
# Copyright 2022 Mabrains Company LLC
#
# Licensed under the LGPL v2.1 License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##
########################################################################################################################
##
# Copyright (C) 2018-2021 Mabrains Company LLC <contact@mabrains.com>
##
########################################################################################################################

########################################################################################################################
## Mabrains Company LLC
##
## Mabrains poly resistor 1.8V Generator for Skywaters 130nm
########################################################################################################################
import pya
import math
from .layers_definiations import *



class PolyRes:
    """
    Mabrains poly resistor Generator for Skywaters 130nm
    """

    def __init__(self,layout,
                w=0.35,l=1,
                rx=1,ry=1,
                gr=0,series=0,

                ):
       
        self.layout = layout
        self.w = w
        self.l = l
        self.rx = rx
        self.ry = ry
        self.gr = gr
        self.series = series
        # constants
        self.licon_enclosure = 0.08
        self.licon_length = 2
        self.res_spacing_x = 1.24
        self.res_spacing_y = 0.52

        self.gr_half_width = 0.255
        self.psdm_spacing = 0.38
        self.psdm_enclosure = 0.11
        self. urpm_enclosure = 0.2
       

    
         # layers_definations
        self.l_poly = self.layout.layer(poly_lay_num, poly_lay_dt)  # Poly
        self.l_licon = self.layout.layer(licon_lay_num, licon_lay_dt)  # licon local interconnect
        self.l_li = self.layout.layer(li_lay_num, li_lay_dt)
        self.l_mcon = self.layout.layer(mcon_lay_num, mcon_lay_dt)
        self.l_met1 = self.layout.layer(met1_lay_num, met1_lay_dt)
        self.l_urpm = self.layout.layer(urpm_lay_num, urpm_lay_dt)
        self.l_psdm = self.layout.layer(psdm_lay_num, psdm_lay_dt)  # psdm source drain impaln
        self.l_tap = self.layout.layer(tap_lay_num, tap_lay_dt)
        self.l_npc = self.layout.layer(npc_lay_num, npc_lay_dt)
        self.l_poly_res = self.layout.layer(poly_res_lay_num, poly_res_lay_dt)

        cell_str = "poly_res_w" + str(w).replace(".", "p") + "u_l" + str(l).replace(".", "p") + "u_repeatx" + str(
        rx) + "_repeaty" + str(ry) + "_guard_ring" + str(gr) + "series_connection" + str(series)
        self.cell = self.layout.create_cell(cell_str)
   

   

   

    def draw_polyres(self):
        # precision value for scaling
        PERCISION = 1/self.layout.dbu

       

        # inputs
        # self.draw_one_finger(self.w, self.l, 0, 0, PERCISION)
        # self.draw_metal1_between(0+self.w*PERCISION, 0, PERCISION)
        lfx = 0
        lfy = 0
        lfx_res = lfx + (self.gr_half_width + self.psdm_spacing + self.psdm_enclosure) * PERCISION
        lfy_res = lfy + (self.gr_half_width + self.psdm_spacing + self.psdm_enclosure) * PERCISION

        gr_width = 2*self.gr_half_width + 2*self.psdm_spacing + 2*self.psdm_enclosure + \
                   (self.rx - 1)*self.res_spacing_x + self.rx*self.w
        gr_height = 2 * self.gr_half_width + 2 * self.psdm_spacing + 2 * self.psdm_enclosure + \
                   (self.ry - 1) * self.res_spacing_y + self.ry*(4*self.licon_enclosure + 2*self.licon_length + self.l)
        self.draw_matrix(lfx_res, lfy_res, PERCISION)

        if self.rx ==1 and self.ry > 1 :
            urpm_enclosure = ((1.27 * PERCISION - self.w * PERCISION) / 2)
            urpm_lfx = lfx_res - urpm_enclosure
            urpm_urx = urpm_lfx + self.w*PERCISION + 2*urpm_enclosure
            urpm_lfy = lfy_res - self.urpm_enclosure * PERCISION
            urpm_ury = urpm_lfy + (gr_height+2*self.urpm_enclosure - (2 * self.gr_half_width + 2 * self.psdm_spacing + 2 * self.psdm_enclosure)) * PERCISION
            self.cell.shapes(self.l_urpm).insert(pya.Box(urpm_lfx, urpm_lfy, urpm_urx, urpm_ury))

        else:
            urpm_lfx = lfx_res - self.urpm_enclosure*PERCISION
            urpm_urx = lfx_res + ((self.rx - 1)*self.res_spacing_x + self.rx*self.w + self.urpm_enclosure)*PERCISION
            urpm_lfy = lfy_res - self.urpm_enclosure * PERCISION
            urpm_ury = urpm_lfy + (gr_height + 2 * self.urpm_enclosure - (
                        2 * self.gr_half_width + 2 * self.psdm_spacing + 2 * self.psdm_enclosure)) * PERCISION
            self.cell.shapes(self.l_urpm).insert(pya.Box(urpm_lfx, urpm_lfy, urpm_urx, urpm_ury))

        if self.gr:
            self.draw_guard_ring(lfx, lfy, gr_width, gr_height, PERCISION)

        return self.cell

    def draw_one_finger(self, width, length, lfx, lfy, precision,m1=1):
        """ Draw one finger of resistor given width and starting and ending points
        =
        Parameters
        ----------
        width : double
            Width of finger.

        lfx : double
            lower left x position of point to start drawing

        lfy : double
            lower left y position of point to start drawing

        length : double
            length of resistor

        precision : int
            precision of grid
        """
        # **** important note all dimensions are referenced to poly box
        # ury = length + licon margin *4 + length + 2*li length
        height = (0.08 * 4 + length + 2 * self.licon_length) * precision
        ury = lfy + height
        urx = lfx + width * precision
        # draw poly box
        self.cell.shapes(self.l_poly).insert(pya.Box(lfx, lfy, urx, ury))

        # draw psdm box
        psdm_enclosure = 0.110 * precision
        psdm_lfx = lfx - psdm_enclosure
        psdm_lfy = lfy - psdm_enclosure
        psdm_urx = urx + psdm_enclosure
        psdm_ury = ury + psdm_enclosure
        self.cell.shapes(self.l_psdm).insert(pya.Box(psdm_lfx, psdm_lfy, psdm_urx, psdm_ury))

        # draw npc box
        npc_enclosure = 0.095 * precision
        npc_lfx = lfx - npc_enclosure
        npc_lfy = lfy - npc_enclosure
        npc_urx = urx + npc_enclosure
        npc_ury = ury + npc_enclosure
        self.cell.shapes(self.l_npc).insert(pya.Box(npc_lfx, npc_lfy, npc_urx, npc_ury))

        if self.rx == 1 and self. ry == 1:
            # draw urpm box
            urpm_enclosure = 0.2 * precision
            urpm_lfy = lfy - urpm_enclosure
            urpm_ury = ury + urpm_enclosure

            # if width < 0.69 we put extra enclosure to pass min width of urpm rule which is 1.27
            if width > 0.7:
                urpm_lfx = lfx - urpm_enclosure
                urpm_urx = urx + urpm_enclosure
            else:
                urpm_enclosure = ((1.27* precision - width * precision)/2)
                urpm_lfx = lfx - urpm_enclosure
                urpm_urx = urx + urpm_enclosure
            self.cell.shapes(self.l_urpm).insert(pya.Box(urpm_lfx, urpm_lfy, urpm_urx, urpm_ury))

        # draw licon box
        licon_enclosure = self.licon_enclosure * precision
        # licon count =>  0.35=> 1, 0.69=> 1, 1.41=> 2, 2.85=> 4, 5.73=> 8

        licon_lfy1 = lfy + licon_enclosure
        licon_ury1 = licon_lfy1 + self.licon_length * precision

        licon_lfy2 = lfy + (3 * licon_enclosure + self.licon_length * precision + length * precision)
        licon_ury2 = licon_lfy2 + self.licon_length * precision
        if str(width)[0:4] == "0.35":
            self.draw_one_licon(lfx, 0.08, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2)
        elif str(width)[0:4] == "0.69":
            self.draw_one_licon(lfx, 0.25, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2)

        elif str(width)[0:4] == "1.41":
            self.draw_one_licon(lfx, 0.35, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2)
            self.draw_one_licon(lfx, 0.88, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2)
        elif str(width)[0:4] == "2.85":
            self.draw_one_licon(lfx, 0.418, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2)
            self.draw_one_licon(lfx, 1.026, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2)
            self.draw_one_licon(lfx, 1.634, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2)
            self.draw_one_licon(lfx, 2.242, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2)

        elif str(width)[0:4] == "5.73":
            self.draw_one_licon(lfx, 0.46, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2)
            self.draw_one_licon(lfx, 1.11, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2)
            self.draw_one_licon(lfx, 1.76, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2)
            self.draw_one_licon(lfx, 2.41, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2)
            self.draw_one_licon(lfx, 3.06, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2)
            self.draw_one_licon(lfx, 3.71, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2)
            self.draw_one_licon(lfx, 4.36, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2)
            self.draw_one_licon(lfx, 5.01, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2)

        # draw polyres box
        poly_res_lfy = lfy + 2 * licon_enclosure + self.licon_length * precision
        poly_res_ury = poly_res_lfy + length * precision
        self.cell.shapes(self.l_poly_res).insert(pya.Box(lfx, poly_res_lfy, urx, poly_res_ury))

        # draw li box
        self.cell.shapes(self.l_li).insert(pya.Box(lfx, lfy, urx, poly_res_lfy))
        self.cell.shapes(self.l_li).insert(pya.Box(lfx, poly_res_ury, urx, ury))

        # draw mcon
        if m1:
            self.draw_mcon_in_li(lfx, lfy, width * precision, poly_res_lfy - lfy, precision)
            self.draw_mcon_in_li(lfx, poly_res_ury, width * precision,  poly_res_lfy - lfy, precision)

        # draw M1 box
        if m1 :

            self.cell.shapes(self.l_met1).insert(pya.Box(lfx, lfy, urx, poly_res_lfy))
            self.cell.shapes(self.l_met1).insert(pya.Box(lfx, poly_res_ury, urx, ury))

        

        


    def draw_one_licon(self, lfx, start_x, precision, licon_lfy1, licon_ury1, licon_lfy2, licon_ury2):
        """ Draw one pair of licon.

        Parameters
        ----------
        lfx : double
            lower left x position of poly.

        start_x : double
            lower left spacing to start draw from.

        licon_lfy1 : double
            lower left y position of point to start drawing for first licon.

        licon_ury1 : double
            upper right y position of point to start drawing for first licon.

        licon_lfy2 : double
            lower left y position of point to start drawing for second licon.

        licon_ury2 : double
            upper right y position of point to start drawing for second licon.

        precision : int
            precision of grid
        """
        licon_lfx1 = lfx + start_x * precision
        licon_urx1 = licon_lfx1 + 0.19 * precision
        licon_lfx2 = licon_lfx1
        licon_urx2 = licon_urx1
        self.cell.shapes(self.l_licon).insert(pya.Box(licon_lfx1, licon_lfy1, licon_urx1, licon_ury1))
        self.cell.shapes(self.l_licon).insert(pya.Box(licon_lfx2, licon_lfy2, licon_urx2, licon_ury2))

    def draw_mcon_in_li(self, lfx, lfy, width, height, precision):

        """ Draw one pair of licon.

        Parameters
        ----------
        lfx : double
           lower left x position of point to start drawing from.

        lfy : double
           lower left y position of point to start drawing from.

        width : double
           total width of li layer

        height : double
           total height of li layer

        precision : int
            precision of grid
        """
        mcon_width = 0.17 * precision
        mcon_spacing = 0.19 * precision

        x_num_mcon, x_spacing = self.number_spc_contacts(width, 0, mcon_spacing, mcon_width)
        y_num_mcon, y_spacing = self.number_spc_contacts(height, 0, mcon_spacing, mcon_width)
        init_lfy = lfy + y_spacing/2
        current_lfx = lfx + x_spacing / 2
        # loop and draw each row of mcon
        for i in range(x_num_mcon):
            current_lfy = init_lfy
            for j in range(y_num_mcon):
                urx = current_lfx + 0.17 * precision
                ury = current_lfy + 0.17 * precision
                self.cell.shapes(self.l_mcon).insert(pya.Box(current_lfx, current_lfy, urx, ury))
                current_lfy = current_lfy + mcon_width + mcon_spacing

            current_lfx = current_lfx + mcon_width + mcon_spacing

    def number_spc_contacts(self, box_width, min_enc, cont_spc, cont_width):
        """ Calculate number of contacts in a given dimensions and the free space for symmetry.

        By getting the min enclosure,the width of the box,the width of the cont. or via
        and the spacing between cont. or via

        Parameters
        ----------
        box_width : double
            The length you place the via or cont. in

        min_enc : double
            the spacing between the edge of the box and the first via or cont.

        cont_spc : double
            the spacing between different via's or cont

        cont_width: double
            the cont. or via width in the same direction

        """

        spc_cont = box_width - 2 * min_enc
        num_cont = int((spc_cont + cont_spc) / (cont_width + cont_spc))
        free_spc = box_width - (num_cont * cont_width + (num_cont - 1) * cont_spc)
        return num_cont, free_spc

    def draw_metal1_between(self, lfx, lfy, precision):
        """ draw one metal between resistors.

        Parameters
        ----------
        lfx : double
           lower left x position of point to start drawing from.

        lfy : double
           lower left y position of point to start drawing from.

        precision : int
            precision of grid
        """
        urx = lfx + 2*self.res_spacing_x * precision 
        ury = lfy +(self.licon_length + 2 * self.licon_enclosure) * precision

        self.cell.shapes(self.l_met1).insert(pya.Box(lfx, lfy, urx, ury))

    def draw_one_raw(self, lfx, lfy, width, length, precision, num_of_res, first_down):
        """ draw one metal between resistors.

        width : double
            Width of finger.

        lfx : double
            lower left x position of point to start drawing

        lfy : double
            lower left y position of point to start drawing

        length : double
            length of resistor

        precision : int
            precision of grid

        num_of_res : int
            num of res to draw

        first_down : bool
            is first metal1 is down or not
        """
        current_lfx = lfx
        returned_lfx = lfx
        returned_lfy = lfy
        for i in range(1, num_of_res+1):
            self.draw_one_finger(width, length, current_lfx, lfy, precision)

            if (not first_down) and (i == num_of_res):
                returned_lfx = current_lfx
            if i == num_of_res:  # skip last loop
                continue
            lfx_metal1 = current_lfx + self.w * precision
            if first_down:
                if i % 2 == 1:
                    lfy_metal1 = lfy
                else:
                    lfy_metal1 = lfy + (self.licon_enclosure * 2 + self.licon_length + length) * precision
            else:
                if i % 2 == 1:
                    lfy_metal1 = lfy + (self.licon_enclosure * 2 + self.licon_length + length) * precision
                else:
                    lfy_metal1 = lfy
            if self.series:
                self.draw_metal1_between(lfx_metal1, lfy_metal1, precision)

            current_lfx += (width + self.res_spacing_x) * precision

        return returned_lfx, returned_lfy

    def draw_matrix(self, lfx, lfy, precision):
        """ draw resistor matrix

        lfx : double
            lower left x position of point to start drawing

        lfy : double
            lower left y position of point to start drawing

        precision : int
            precision of grid
        """

        current_lfy = lfy
        for i in range(1, self.ry+1):
            if i % 2 == 1:
                returned_lfx, returned_lfy = self.draw_one_raw(lfx, current_lfy, self.w, self.l, precision, self.rx, False)
            else:
                returned_lfx, returned_lfy = self.draw_one_raw(lfx, current_lfy, self.w, self.l, precision, self.rx, True)

            if i != self.ry:
                metal_lfy = returned_lfy + (4 * self.licon_enclosure + 2*self. licon_length + self.l) * precision
                metal_ury = metal_lfy + self.res_spacing_y * precision
                metal_urx = returned_lfx + self.w * precision
                if self.series and self.rx % 2 == 1:
                    self.cell.shapes(self.l_met1).insert(pya.Box(returned_lfx, metal_lfy, metal_urx, metal_ury))

            current_lfy += (4 * self.licon_enclosure + 2 * self. licon_length + self.l + self.res_spacing_y) * precision

    def draw_guard_ring(self, x, y, guard_width, guard_height, precision, tap_width=0.26):
        l_psdm = self.layout.layer(psdm_lay_num, psdm_lay_dt)  # psdm source drain impaln
        l_licon = self.layout.layer(licon_lay_num, licon_lay_dt)  # licon local interconnect
        l_li = self.layout.layer(li_lay_num, li_lay_dt)
        l_mcon = self.layout.layer(mcon_lay_num, mcon_lay_dt)
        l_met1 = self.layout.layer(met1_lay_num, met1_lay_dt)
        l_tap = self.layout.layer(tap_lay_num, tap_lay_dt)
        l_via = self.layout.layer(via_lay_num, via_lay_dt)
        l_met2 = self.layout.layer(met2_lay_num, met2_lay_dt)
        PERCISION = precision
        guard_width *= PERCISION
        guard_height *= PERCISION
        npsdm_enc_diff = .125 * PERCISION
        licon_size = 0.17 * PERCISION
        mcon_m1_enc = 0.03 * PERCISION
        via_met_enc = 0.085*PERCISION
        mcon_size = 0.17 * PERCISION
        mcon_spc = 0.19 * PERCISION
        via_size = 0.15 * PERCISION
        via_spc = 0.17 * PERCISION
        tap_width = tap_width *PERCISION
        guard_ring_lower_left = pya.Point(x,y)
        guard_ring_upper_left = pya.Point(x,y+guard_height)
        guard_ring_upper_right = pya.Point(x+guard_width,y+guard_height)
        guard_ring_lower_right = pya.Point(guard_ring_upper_right.x, guard_ring_lower_left.y)
        guard_ring_path = pya.Path(
            [guard_ring_lower_left, guard_ring_upper_left, guard_ring_upper_right, guard_ring_lower_right,
             guard_ring_lower_left], tap_width, tap_width / 2, 0)
        psdm_guard_ring_path = pya.Path(
            [guard_ring_lower_left, guard_ring_upper_left, guard_ring_upper_right, guard_ring_lower_right,
             guard_ring_lower_left], tap_width + 2 * npsdm_enc_diff, (tap_width + 2 * npsdm_enc_diff) / 2, 0)
        gurad_ring_metal1_upper = pya.Path([guard_ring_upper_left, guard_ring_upper_right], tap_width, tap_width / 2,
                                           tap_width / 2)
        self.cell.shapes(l_met1).insert(gurad_ring_metal1_upper)
        gurad_ring_metal1_lower = pya.Path([guard_ring_lower_left, guard_ring_lower_right], tap_width, tap_width / 2,
                                           tap_width / 2)
        self.cell.shapes(l_met1).insert(gurad_ring_metal1_lower)
        gurad_ring_metal1_right = pya.Path([guard_ring_lower_right, guard_ring_upper_right], tap_width, tap_width / 2,
                                           tap_width / 2)
        self.cell.shapes(l_met1).insert(gurad_ring_metal1_right)
        gurad_ring_metal1_left = pya.Path([guard_ring_lower_left, guard_ring_upper_left], tap_width, tap_width / 2,
                                          tap_width / 2)
        self.cell.shapes(l_met1).insert(gurad_ring_metal1_left)
        self.cell.shapes(l_met2).insert(gurad_ring_metal1_upper)
        self.cell.shapes(l_met2).insert(gurad_ring_metal1_lower)
        self.cell.shapes(l_met2).insert(gurad_ring_metal1_right)
        self.cell.shapes(l_met2).insert(gurad_ring_metal1_left)
        self.cell.shapes(l_tap).insert(guard_ring_path)
        self.cell.shapes(l_psdm).insert(psdm_guard_ring_path)
        self.cell.shapes(l_li).insert(guard_ring_path)
        # top_nmos_cell.shapes(l_met1).insert(guard_ring_path)
        distance_cont_guard_vert = guard_ring_upper_left.y - guard_ring_lower_left.y
        num_licon_guard_vert, free_spc_licon_guard_left = self.number_spc_contacts(distance_cont_guard_vert,
                                                                                   mcon_m1_enc,
                                                                                   licon_size, licon_size)
        licon_guard_p1_x_left = guard_ring_lower_left.x - licon_size / 2
        licon_guard_p1_x_right = guard_ring_lower_right.x - licon_size / 2
        licon_guard_p1_y = guard_ring_lower_left.y + free_spc_licon_guard_left / 2
        licon_guard_p2_x_left = licon_guard_p1_x_left + licon_size
        licon_guard_p2_x_right = licon_guard_p1_x_right + licon_size
        licon_guard_p2_y = licon_guard_p1_y + licon_size
        # drawing vertical licon in guard_ring
        for licon in range(num_licon_guard_vert):
            licon_guard_box_left = pya.Box(licon_guard_p1_x_left, licon_guard_p1_y, licon_guard_p2_x_left,
                                           licon_guard_p2_y)
            licon_guard_box_right = pya.Box(licon_guard_p1_x_right, licon_guard_p1_y, licon_guard_p2_x_right,
                                            licon_guard_p2_y)
            self.cell.shapes(l_licon).insert(licon_guard_box_left)
            self.cell.shapes(l_licon).insert(licon_guard_box_right)
            licon_guard_p1_y += 2 * licon_size
            licon_guard_p2_y += 2 * licon_size
        num_mcon_guard_vert, free_spc_mcon_guard_left = self.number_spc_contacts(distance_cont_guard_vert, mcon_m1_enc,
                                                                                 mcon_spc, mcon_size)
        mcon_guard_p1_x_left = guard_ring_lower_left.x - mcon_size / 2
        mcon_guard_p1_x_right = guard_ring_lower_right.x - mcon_size / 2
        mcon_guard_p1_y = guard_ring_lower_left.y + free_spc_mcon_guard_left / 2
        mcon_guard_p2_x_left = mcon_guard_p1_x_left + mcon_size
        mcon_guard_p2_x_right = mcon_guard_p1_x_right + mcon_size
        mcon_guard_p2_y = mcon_guard_p1_y + licon_size
        for mcon in range(num_mcon_guard_vert):
            mcon_guard_box_left = pya.Box(mcon_guard_p1_x_left, mcon_guard_p1_y, mcon_guard_p2_x_left, mcon_guard_p2_y)
            mcon_guard_box_right = pya.Box(mcon_guard_p1_x_right, mcon_guard_p1_y, mcon_guard_p2_x_right,
                                           mcon_guard_p2_y)
            self.cell.shapes(l_mcon).insert(mcon_guard_box_left)
            self.cell.shapes(l_mcon).insert(mcon_guard_box_right)
            mcon_guard_p1_y += mcon_size + mcon_spc
            mcon_guard_p2_y += mcon_size + mcon_spc
        num_via_guard_vert, free_spc_via_guard_left = self.number_spc_contacts(distance_cont_guard_vert,
                                                                               via_met_enc,
                                                                               via_spc, via_size)
        via_guard_p1_x_left = guard_ring_lower_left.x - via_size / 2
        via_guard_p1_x_right = guard_ring_lower_right.x - via_size / 2
        via_guard_p1_y = guard_ring_lower_left.y + free_spc_via_guard_left / 2
        via_guard_p2_x_left = via_guard_p1_x_left + via_size
        via_guard_p2_x_right = via_guard_p1_x_right + via_size
        via_guard_p2_y = via_guard_p1_y + via_size
        for via in range(num_via_guard_vert):
            via_guard_box_left = pya.Box(via_guard_p1_x_left, via_guard_p1_y, via_guard_p2_x_left,
                                         via_guard_p2_y)
            via_guard_box_right = pya.Box(via_guard_p1_x_right, via_guard_p1_y, via_guard_p2_x_right,
                                          via_guard_p2_y)
            self.cell.shapes(l_via).insert(via_guard_box_left)
            self.cell.shapes(l_via).insert(via_guard_box_right)
            via_guard_p1_y += via_size + via_spc
            via_guard_p2_y += via_size + via_spc
        distance_cont_guard_hori = (guard_ring_upper_right.x - guard_ring_upper_left.x) - 2 * mcon_spc
        num_licon_guard_hori, free_spc_licon_guard_hori = self.number_spc_contacts(distance_cont_guard_hori,
                                                                                   mcon_m1_enc,
                                                                                   licon_size, licon_size)
        licon_guard_p1_x_hori = guard_ring_lower_left.x + free_spc_licon_guard_hori / 2 + mcon_spc
        licon_guard_p1_y_lower = guard_ring_lower_left.y - licon_size / 2
        licon_guard_p1_y_upper = guard_ring_upper_left.y - licon_size / 2
        licon_guard_p2_x_hori = licon_guard_p1_x_hori + licon_size
        licon_guard_p2_y_upper = guard_ring_upper_left.y + licon_size / 2
        licon_guard_p2_y_lower = guard_ring_lower_left.y + licon_size / 2
        for licon in range(num_licon_guard_hori):
            licon_guard_box_upper = pya.Box(licon_guard_p1_x_hori, licon_guard_p1_y_upper, licon_guard_p2_x_hori,
                                            licon_guard_p2_y_upper)
            licon_guard_box_lower = pya.Box(licon_guard_p1_x_hori, licon_guard_p1_y_lower, licon_guard_p2_x_hori,
                                            licon_guard_p2_y_lower)
            self.cell.shapes(l_licon).insert(licon_guard_box_upper)
            self.cell.shapes(l_licon).insert(licon_guard_box_lower)
            licon_guard_p1_x_hori += 2 * licon_size
            licon_guard_p2_x_hori += 2 * licon_size
            num_mcon_guard_hori, free_spc_mcon_guard_hori = self.number_spc_contacts(distance_cont_guard_hori,
                                                                                     mcon_m1_enc,
                                                                                     mcon_spc, mcon_size)
            mcon_guard_p1_x_hori = guard_ring_lower_left.x + free_spc_mcon_guard_hori / 2 + mcon_spc
            mcon_guard_p1_y_lower = guard_ring_lower_left.y - mcon_size / 2
            mcon_guard_p1_y_upper = guard_ring_upper_left.y - mcon_size / 2
            mcon_guard_p2_x_hori = mcon_guard_p1_x_hori + mcon_size
            mcon_guard_p2_y_upper = guard_ring_upper_left.y + mcon_size / 2
            mcon_guard_p2_y_lower = guard_ring_lower_left.y + mcon_size / 2
            for mcon in range(num_mcon_guard_hori):
                mcon_guard_box_upper = pya.Box(mcon_guard_p1_x_hori, mcon_guard_p1_y_upper,
                                               mcon_guard_p2_x_hori,
                                               mcon_guard_p2_y_upper)
                mcon_guard_box_lower = pya.Box(mcon_guard_p1_x_hori, mcon_guard_p1_y_lower,
                                               mcon_guard_p2_x_hori,
                                               mcon_guard_p2_y_lower)
                self.cell.shapes(l_mcon).insert(mcon_guard_box_upper)
                self.cell.shapes(l_mcon).insert(mcon_guard_box_lower)
                mcon_guard_p1_x_hori += mcon_size + mcon_spc
                mcon_guard_p2_x_hori += mcon_size + mcon_spc
            num_via_guard_hori, free_spc_via_guard_hori = self.number_spc_contacts(distance_cont_guard_hori,
                                                                                   via_met_enc,
                                                                                   via_spc, via_size)
            via_guard_p1_x_hori = guard_ring_lower_left.x + free_spc_via_guard_hori / 2 + via_spc
            via_guard_p1_y_lower = guard_ring_lower_left.y - via_size / 2
            via_guard_p1_y_upper = guard_ring_upper_left.y - via_size / 2
            via_guard_p2_x_hori = via_guard_p1_x_hori + via_size
            via_guard_p2_y_upper = guard_ring_upper_left.y + via_size / 2
            via_guard_p2_y_lower = guard_ring_lower_left.y + via_size / 2
            for via in range(num_via_guard_hori):
                via_guard_box_upper = pya.Box(via_guard_p1_x_hori, via_guard_p1_y_upper,
                                              via_guard_p2_x_hori,
                                              via_guard_p2_y_upper)
                via_guard_box_lower = pya.Box(via_guard_p1_x_hori, via_guard_p1_y_lower,
                                              via_guard_p2_x_hori,
                                              via_guard_p2_y_lower)
                self.cell.shapes(l_via).insert(via_guard_box_upper)
                self.cell.shapes(l_via).insert(via_guard_box_lower)
                via_guard_p1_x_hori += via_size + via_spc
                via_guard_p2_x_hori += via_size + via_spc


layout = pya.Layout()
top_cell = layout.create_cell("TOP")
poly1 = PolyRes(layout=layout)
cell_name = poly1.draw_polyres()

write_cells = pya.CellInstArray(cell_name.cell_index(), pya.Trans(pya.Point(0, 0)),
                                        pya.Vector(0, 0), pya.Vector(0, 0), 1, 1)
top_cell.insert(write_cells)
poly1 = PolyRes(layout=layout,rx=4,series=1,gr=1)
cell_name = poly1.draw_polyres()
write_cells = pya.CellInstArray(cell_name.cell_index(), pya.Trans(pya.Point(3000, 0)),
                                        pya.Vector(0, 0), pya.Vector(0, 0), 1, 1)

top_cell.insert(write_cells)

layout.write("poly_res.gds")
