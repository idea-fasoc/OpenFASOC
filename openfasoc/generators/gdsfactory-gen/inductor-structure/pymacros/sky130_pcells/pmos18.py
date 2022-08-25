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
# This file is authored by:
#           - <Mina Maksimous> <mina_maksimous@mabrains.com>
##
########################################################################################################################

########################################################################################################################
## Mabrains Company LLC
##
## Mabrains PMOS 1.8V Generator for Skywaters 130nm
########################################################################################################################
import pya
import math
from .layers_definiations import *



class PMOS18(pya.PCellDeclarationHelper):
    """
    Mabrains Via Generator for Skywaters 130nm
    """

    def __init__(self):
        ## Initialize super class.
        super(PMOS18, self).__init__()

        # declare the parameters

        self.param("w", self.TypeDouble, "Width", default=0.42)
        self.param("l", self.TypeDouble, "Length", default=0.15)
        self.param("nf", self.TypeInt, "Number of Fingers", default=1)
        self.param("gr", self.TypeBoolean, "guard ring", default=1)
        self.param("dsa", self.TypeInt, "drain and source number of contacts", default=1)

        #self.param("down_connection", self.TypeBoolean, "Gate connection down", default=1)
        #self.param("up_connection", self.TypeBoolean, "Gate connection up", default=0)
        #self.param("alternate_connection", self.TypeBoolean, "Alternate gate connection", default=0)
        connection_option = self.param("connection", self.TypeString, "Connection Option", default="Connection Up")
        connection_option.add_choice("Connection Up", 0)
        connection_option.add_choice("Connection Down", 1)
        connection_option.add_choice("Alternate connection", 2)
        self.param("n", self.TypeInt, "alternate factor", default=1)


        # Below shows how to create hidden parameter is used to determine whether the radius has changed
        # or the "s" handle has been moved
        ## self.param("ru", self.TypeDouble, "Radius", default = 0.0, hidden = True)
        ## self.param("rd", self.TypeDouble, "Double radius", readonly = True)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "PMOS18(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"


    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the
        # numeric parameter has changed (by comparing against the effective
        # radius ru) and set ru to the effective radius. We also update the
        # numerical value or the shape, depending on which on has not changed.
        pass

    def can_create_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we can use any shape which
        # has a finite bounding box
        return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()
    #
    def parameters_from_shape_impl(self):
    #     # Implement the "Create PCell from shape" protocol: we set r and l from the shape's
    #     # bounding box width and layer
        self.r = self.shape.bbox().width() * self.layout.dbu / 2
        self.l = self.layout.get_info(self.layer)
    #
    def transformation_from_shape_impl(self):
            #Implement the "Create PCell from shape" protocol: we use the center of the shape's
    #     # bounding box to determine the transformation
        return pya.Trans(self.shape.bbox().center())

    def number_spc_contacts(self,box_width, min_enc, cont_spc, cont_width):
        spc_cont = box_width - 2 * min_enc
        num_cont = int((spc_cont + cont_spc) / (cont_width + cont_spc))
        free_spc = box_width - (num_cont * cont_width + (num_cont - 1) * cont_spc)
        return num_cont, free_spc

    def produce_impl(self):
        PERCISION = 1000
        nwell_extension = 0.18*PERCISION
        # precision value for scaling
        liconpoly_spc = 0.055 * PERCISION
        source_shared = 1
        # 1 for source_shared 0 for no nf turned into no of multipliers
        multipliers = 1
        diff_spc = 0.27 * PERCISION
        npsdm_enc_diff = .125 * PERCISION
        # the extension of n+ or p+ layer beyond diff to define it's type
        npsdm_spc_opposite = 0.13 * PERCISION
        # the spacing of different regions of doping
        npsdm_spc = 0.38 * PERCISION
        # the spacing of the same type regions of doping
        alternate = 0
        mcon_size = 0.17 * PERCISION
        mcon_spc = 0.19 * PERCISION
        # if 0 alternate 1 gate_connection_up 2 gate_connection_down

        # and the channel length is low todo find the length in code

        diffusion_width_big = self.dsa * mcon_size + (self.dsa - 1) * mcon_spc + 2 * liconpoly_spc
        # diffusion width between fingers
        diffusion_width_small = diffusion_width_big
        diffusion_width_big_samedirection = diffusion_width_big
        # diffusion width between fingers if the gates in the same direction
        # first diffusion and last diffusion width #todo check if matter
        if self.connection == 1 or self.connection == 0:
            # if gates in the same direction
            diffusion_width_big = diffusion_width_big_samedirection
            # if gates in the same direction enlarge diffusion to get through drc
            # todo make the last and first diffusion the same as the between

        nf = self.nf  # number of fingers
        channel_length = self.l * PERCISION

        if source_shared == 0:
            # if no source sharing nf = 1 and repetition become multiplier
            nf = 1

        if nf == 1:
            diffusion_total_width = channel_length + diffusion_width_big + diffusion_width_small
            # todo :correct the diffusion_total_width of singel finger

        diffusion_total_width = nf * channel_length + (nf - 1) * diffusion_width_big + 2 * diffusion_width_big
        channel_width = self.w * PERCISION
        fingers_connected = True
        gate_connection_up = False
        min_channel_width = channel_width
        diff_min_width = 0.28
        poly_min_width = 0.15
        poly_diff_min_enc = 0.13 * PERCISION
        polylicon_spc_diff = 0.19 * PERCISION

        licon_size = 0.17 * PERCISION

        diff_licon_enc_vertical = 0.08 * PERCISION
        diff_licon_enc_horzintal = 0.04 * PERCISION
        liconpoly_enc_vertical = 0.05 * PERCISION
        liconpoly_enc_horizontal = 0.08 * PERCISION
        li_licon_enc = 0.08 * PERCISION
        npc_enc_gate = 0.1 * PERCISION
        m1_width = 0.17 * PERCISION
        mcon_m1_enc = 0.03 * PERCISION
        via_size = 0.15 * PERCISION
        via_spc = 0.17 * PERCISION
        via_met_enc = 0.085 * PERCISION
        if self.connection == 1:
            # gate_connection down todo why
            diffusion_width_big = diffusion_width_big_samedirection

        li_width = 0.17 * PERCISION

        # number of vertical licon's diff todo use the function
        spc_for_licon = channel_width - 2 * diff_licon_enc_vertical
        num_ver_licon = int(((spc_for_licon / licon_size) + 1) / 2)

        # number of vertical mcon diff
        num_ver_mcon = int((channel_width + mcon_spc) / (mcon_spc + mcon_size))
        free_spc_mcon_diff = (channel_width - (num_ver_mcon * (mcon_spc + mcon_size) - mcon_spc))

        # calculate free space for licon
        free_space_diff_licon = channel_width - (2 * num_ver_licon - 1) * licon_size

        # layers_definations
        l_diff = self.layout.layer(diff_lay_num, diff_lay_dt)  # Diffusion
        l_poly = self.layout.layer(poly_lay_num, poly_lay_dt)  # Poly
        l_nsdm = self.layout.layer(nsdm_lay_num, nsdm_lay_dt)  # nsdm source drain impalnt
        l_psdm = self.layout.layer(psdm_lay_num, psdm_lay_dt)  # psdm source drain impaln
        l_licon = self.layout.layer(licon_lay_num, licon_lay_dt)  # licon local interconnect
        l_npc = self.layout.layer(npc_lay_num, npc_lay_dt)
        l_li = self.layout.layer(li_lay_num, li_lay_dt)
        l_mcon = self.layout.layer(mcon_lay_num, mcon_lay_dt)
        l_met1 = self.layout.layer(met1_lay_num, met1_lay_dt)
        l_tap = self.layout.layer(tap_lay_num, tap_lay_dt)
        l_nwell = self.layout.layer(nwell_lay_num, nwell_lay_dt)
        l_via = self.layout.layer(via_lay_num, via_lay_dt)
        l_met2 = self.layout.layer(met2_lay_num, met2_lay_dt)

        ##cells##
        top_nmos_cell = self.layout.create_cell("top_nmos")
        nmos_cell = self.layout.create_cell("nmos")
        gate_cell = self.layout.create_cell("gate")
        licon_cell = self.layout.create_cell("licon")
        licon_between_fingers_cell = self.layout.create_cell("licon_between_fingers")
        up_gate_connection = self.layout.create_cell("up_gate_connection")
        down_gate_connection = self.layout.create_cell("down_gate_connection")
        li_between_fingers_cell = self.layout.create_cell("li_between_fingers")
        mcon_tran_sides_cell = self.layout.create_cell("mcon_transistor_sides")
        mcon_between_fingers_cell = self.layout.create_cell("mcon_between_fingers")
        ##

        diff_box = pya.Box(0, 0, diffusion_total_width, channel_width)
        # main diff box
        nsdm_box = pya.Box(-npsdm_enc_diff, -npsdm_enc_diff, diffusion_total_width + npsdm_enc_diff,
                           channel_width + npsdm_enc_diff)
        # source drain implant diff
        x = 0

        for finger in range(nf):
            gate_box = pya.Box(diffusion_width_big + x, -poly_diff_min_enc, channel_length + diffusion_width_big + x,
                               channel_width + poly_diff_min_enc)

            self.cell.shapes(l_poly).insert(gate_box)
            x += channel_length + diffusion_width_big

        gate_box = pya.Box(diffusion_width_big, -poly_diff_min_enc, channel_length + diffusion_width_big,
                           channel_width + poly_diff_min_enc)

        # connection of gate box dimensions
        contact_gate_width = 2 * liconpoly_enc_horizontal + licon_size
        contact_gate_height = 2 * liconpoly_enc_vertical + 3 * licon_size
        num_horizontal_licon_gate = 1

        free_spc_licon_gate = contact_gate_width - (2 * num_horizontal_licon_gate - 1) * licon_size
        if channel_length > contact_gate_width:
            # calculate number of horizontal licon in gate connection todo use function to do
            contact_gate_width = channel_length
            spc_for_licon_gate = channel_length - 2 * liconpoly_enc_horizontal
            num_horizontal_licon_gate = int(((spc_for_licon_gate / licon_size) + 1) / 2)
            free_spc_licon_gate = channel_length - (2 * num_horizontal_licon_gate - 1) * licon_size

        # contacte_gate_box
        contact_gate_box_down = pya.Box(gate_box.center().x - contact_gate_width / 2,
                                        -polylicon_spc_diff - contact_gate_height,
                                        gate_box.center().x + contact_gate_width / 2, -polylicon_spc_diff)
        neck_box_down = pya.Box(diffusion_width_small, -polylicon_spc_diff, channel_length + diffusion_width_small,
                                -poly_diff_min_enc)
        # licon_box_down = pya.Box(contact_gate_box_down.center().x - licon_size/2, contact_gate_box_down.center().y-(licon_size/2),contact_gate_box_down.center().x + licon_size/2,contact_gate_box_down.center().y + licon_size/2)
        npc_box_down = pya.Box(contact_gate_box_down.p1.x - npc_enc_gate, contact_gate_box_down.p1.y - npc_enc_gate,
                               contact_gate_box_down.p2.x + npc_enc_gate, contact_gate_box_down.p2.y + npc_enc_gate)
        li_box_down = pya.Box(diff_box.p1.x, contact_gate_box_down.p1.y,
                              diff_box.p1.x + multipliers * diffusion_total_width + (
                                      2 * multipliers - 2) * npsdm_enc_diff + (multipliers - 1) * npsdm_spc,
                              contact_gate_box_down.p2.y)
        num_hori_licon_diff, free_space_licon_diff_hor = self.number_spc_contacts(diffusion_width_big, liconpoly_spc,
                                                                                  licon_size, licon_size)

        sh1 = 0
        for hor_licon_diff in range(num_hori_licon_diff):
            licon_between_fingers = pya.Box(free_space_licon_diff_hor / 2 + sh1,
                                            free_space_diff_licon / 2, free_space_licon_diff_hor / 2 + licon_size + sh1,
                                            free_space_diff_licon / 2 + licon_size)
            licon_between_fingers_cell.shapes(l_licon).insert(licon_between_fingers)
            sh1 += 2 * licon_size

        print(num_hori_licon_diff, free_space_licon_diff_hor, diffusion_width_big)

        num_hori_mcon_diff, free_space_mcon_diff_hor = self.number_spc_contacts(diffusion_width_big, 0, mcon_spc,
                                                                                mcon_size)
        sh2 = 0
        for hor_mcon_diff in range(num_hori_mcon_diff):
            mcon_between_fingers = pya.Box(free_space_mcon_diff_hor / 2 + sh2,
                                           free_spc_mcon_diff / 2,
                                           free_space_mcon_diff_hor / 2 + sh2 + mcon_size,
                                           free_spc_mcon_diff / 2 + mcon_size)
            mcon_between_fingers_cell.shapes(l_mcon).insert(mcon_between_fingers)
            sh2 += mcon_size + mcon_spc

        li_between_fingers_path = pya.Path([pya.Point(diffusion_width_big / 2, diff_box.p1.y),
                                            pya.Point(diffusion_width_big / 2, diff_box.p2.y)],
                                           diffusion_width_big)
        met1_between_fingers_path = pya.Path([pya.Point(diffusion_width_big / 2, diff_box.p1.y - mcon_m1_enc),
                                              pya.Point(diffusion_width_big / 2, diff_box.p2.y + mcon_m1_enc)],
                                             diffusion_width_big)

        contact_gate_box_up = pya.Box(gate_box.center().x - contact_gate_width / 2, channel_width + polylicon_spc_diff,
                                      gate_box.center().x + contact_gate_width / 2,
                                      channel_width + polylicon_spc_diff + contact_gate_height)
        neck_box_up = pya.Box(diffusion_width_small, channel_width + poly_diff_min_enc,
                              channel_length + diffusion_width_small,
                              channel_width + polylicon_spc_diff)
        licon_box_up = pya.Box(contact_gate_box_up.center().x - licon_size / 2,
                               contact_gate_box_up.center().y - (licon_size / 2),
                               contact_gate_box_up.center().x + licon_size / 2,
                               contact_gate_box_up.center().y + licon_size / 2)
        npc_box_up = pya.Box(contact_gate_box_up.p1.x - 1.6 * npc_enc_gate, contact_gate_box_up.p1.y - npc_enc_gate,
                             contact_gate_box_up.p2.x + 1.6 * npc_enc_gate, contact_gate_box_up.p2.y + npc_enc_gate)
        li_path_up = pya.Path(
            [pya.Point(diff_box.p1.x, licon_box_up.center().y), pya.Point(diff_box.p2.x, licon_box_up.center().y)],
            li_width)

        licon_diff_contact_left = pya.Box(diff_box.p1.x + diff_licon_enc_horzintal, free_space_diff_licon / 2,
                                          diff_licon_enc_horzintal + licon_size, free_space_diff_licon / 2 + licon_size)
        li_diff_left = pya.Path([pya.Point(licon_diff_contact_left.center().x, diff_box.p1.y),
                                 pya.Point(licon_diff_contact_left.center().x, diff_box.p2.y)], li_width)
        met1_diff_left = pya.Path([pya.Point(licon_diff_contact_left.center().x, diff_box.p1.y - mcon_m1_enc),
                                   pya.Point(licon_diff_contact_left.center().x, diff_box.p2.y + mcon_m1_enc)],
                                  m1_width + 2 * mcon_m1_enc)

        mcon_diff_left = pya.Box(licon_diff_contact_left.p1.x, 0, licon_diff_contact_left.p1.x + mcon_size, mcon_size)

        licon_diff_contact_right = pya.Box(diff_box.p2.x - diff_licon_enc_horzintal - licon_size,
                                           free_space_diff_licon / 2,
                                           diff_box.p2.x - diff_licon_enc_horzintal,
                                           free_space_diff_licon / 2 + licon_size)
        li_diff_right = pya.Path([pya.Point(licon_diff_contact_right.center().x, diff_box.p1.y),
                                  pya.Point(licon_diff_contact_right.center().x, diff_box.p2.y)], li_width)
        mcon_diff_right = pya.Box(licon_diff_contact_right.p1.x, 0, licon_diff_contact_right.p1.x + mcon_size,
                                  mcon_size)
        met1_diff_right = pya.Path([pya.Point(licon_diff_contact_right.center().x, diff_box.p1.y - mcon_m1_enc),
                                    pya.Point(licon_diff_contact_right.center().x, diff_box.p2.y + mcon_m1_enc)],
                                   m1_width + 2 * mcon_m1_enc)

        nmos_cell.shapes(l_diff).insert(diff_box)
        nmos_cell.shapes(l_psdm).insert(nsdm_box)
        # gate_cell.shapes(l_poly).insert(gate_box)
        # nmos_cell.shapes(l_li).insert(li_diff_left)
        # nmos_cell.shapes(l_li).insert(li_diff_right)
        # nmos_cell.shapes(l_met1).insert(met1_diff_left)
        # nmos_cell.shapes(l_met1).insert(met1_diff_right)

        num_ver_mcon_gates, free_spc_mcon_gates_v = self.number_spc_contacts(li_box_down.height(), mcon_m1_enc,
                                                                             mcon_spc,
                                                                             mcon_size)
        num_hor_mcon_gates, free_spc_mcon_gates_h = self.number_spc_contacts(li_box_down.width(), mcon_m1_enc, mcon_spc,
                                                                             mcon_size)
        shift_distance = (self.n) * (diffusion_width_big + channel_length)  # shift distance for alternate mode

        if self.connection == 1 or self.connection == 2:
            down_gate_connection.shapes(l_poly).insert(contact_gate_box_down)
            down_gate_connection.shapes(l_poly).insert(neck_box_down)

            y_sh = 0

            p1_x = contact_gate_box_down.p1.x + free_spc_licon_gate / 2
            p1_y = contact_gate_box_down.p1.y + liconpoly_enc_vertical
            p2_x = contact_gate_box_down.p1.x + free_spc_licon_gate / 2 + licon_size
            p2_y = contact_gate_box_down.p1.y + liconpoly_enc_vertical + licon_size
            for licon_ct in range(num_horizontal_licon_gate):
                licon_box_down = pya.Box(p1_x, p1_y, p2_x, p2_y)

                down_gate_connection.shapes(l_licon).insert(licon_box_down)
                p1_y += 2 * licon_size
                p2_y += 2 * licon_size
                licon_box_down = pya.Box(p1_x, p1_y, p2_x, p2_y)
                down_gate_connection.shapes(l_licon).insert(licon_box_down)
                p1_y -= 2 * licon_size
                p2_y -= 2 * licon_size

                p1_x += 2 * licon_size
                p2_x += 2 * licon_size
                # licon_box_down.p1.y = licon_box_down.p1.y + 2*licon_size
                # licon_box_down.p2.y = licon_box_down.p2.y+2*licon_size
                # y_sh += 2*licon_size
                # down_gate_connection.shapes(l_licon).insert(licon_box_down)
                # y_sh -=  2*licon_size

            self.cell.shapes(l_li).insert(li_box_down)
            self.cell.shapes(l_met1).insert(li_box_down)
            down_gate_connection.shapes(l_npc).insert(npc_box_down)

            x_mcon_gates = li_box_down.p1.x + free_spc_mcon_gates_h / 2
            y_mcon_gates = li_box_down.p1.y + free_spc_mcon_gates_v / 2
            y1_mcon_gates = y_mcon_gates + mcon_size

            for mcon in range(num_hor_mcon_gates):
                x1_mcon_gates = x_mcon_gates + mcon_size
                mcon_box_gate = pya.Box(x_mcon_gates, y_mcon_gates, x1_mcon_gates, y1_mcon_gates)
                self.cell.shapes(l_mcon).insert(mcon_box_gate)
                for mcon1 in range(num_ver_mcon_gates - 1):
                    y_mcon_gates += mcon_size + mcon_spc
                    y1_mcon_gates += mcon_size + mcon_spc
                    mcon_box_gate = pya.Box(x_mcon_gates, y_mcon_gates, x1_mcon_gates, y1_mcon_gates)
                    self.cell.shapes(l_mcon).insert(mcon_box_gate)
                y_mcon_gates -= (num_ver_mcon_gates - 1) * mcon_size + (num_ver_mcon_gates - 1) * mcon_spc
                y1_mcon_gates -= (num_ver_mcon_gates - 1) * mcon_size + (num_ver_mcon_gates - 1) * mcon_spc
                x_mcon_gates += mcon_size + mcon_spc
                x1_mcon_gates += mcon_size + mcon_spc

        if self.connection == 0 or self.connection == 2:
            if self.connection == 0:
                shift_distance = 0
            up_gate_connection.shapes(l_poly).insert(contact_gate_box_up)
            up_gate_connection.shapes(l_poly).insert(neck_box_up)
            p1_x = contact_gate_box_up.p1.x + free_spc_licon_gate / 2
            p1_y = contact_gate_box_up.p1.y + liconpoly_enc_vertical
            p2_x = contact_gate_box_up.p1.x + free_spc_licon_gate / 2 + licon_size
            p2_y = contact_gate_box_up.p1.y + liconpoly_enc_vertical + licon_size
            li_box_up = pya.Box(diff_box.p1.x, contact_gate_box_up.p1.y,
                                diff_box.p1.x + multipliers * diffusion_total_width + (
                                        2 * multipliers - 2) * npsdm_enc_diff + (
                                        multipliers - 1) * npsdm_spc, contact_gate_box_up.p2.y)
            self.cell.shapes(l_li).insert(li_box_up)
            self.cell.shapes(l_met1).insert(li_box_up)
            for licon_ct in range(num_horizontal_licon_gate):
                licon_box_up = pya.Box(p1_x, p1_y, p2_x, p2_y)

                up_gate_connection.shapes(l_licon).insert(licon_box_up)
                p1_y += 2 * licon_size
                p2_y += 2 * licon_size
                licon_box_up = pya.Box(p1_x, p1_y, p2_x, p2_y)
                up_gate_connection.shapes(l_licon).insert(licon_box_up)
                p1_y -= 2 * licon_size
                p2_y -= 2 * licon_size

                p1_x += 2 * licon_size
                p2_x += 2 * licon_size
                # licon_box_down.p1.y = licon_box_down.p1.y + 2*licon_size
                # licon_box_down.p2.y = licon_box_down.p2.y+2*licon_size
                # y_sh += 2*licon_size
                # down_gate_connection.shapes(l_licon).insert(licon_box_down)
                # y_sh -=  2*licon_size
            x_mcon_gates = li_box_up.p1.x + free_spc_mcon_gates_h / 2
            y_mcon_gates = li_box_up.p1.y + free_spc_mcon_gates_v / 2
            y1_mcon_gates = y_mcon_gates + mcon_size

            for mcon in range(num_hor_mcon_gates):
                x1_mcon_gates = x_mcon_gates + mcon_size
                mcon_box_gate = pya.Box(x_mcon_gates, y_mcon_gates, x1_mcon_gates, y1_mcon_gates)
                self.cell.shapes(l_mcon).insert(mcon_box_gate)
                for mcon1 in range(num_ver_mcon_gates - 1):
                    y_mcon_gates += mcon_size + mcon_spc
                    y1_mcon_gates += mcon_size + mcon_spc
                    mcon_box_gate = pya.Box(x_mcon_gates, y_mcon_gates, x1_mcon_gates, y1_mcon_gates)
                    self.cell.shapes(l_mcon).insert(mcon_box_gate)
                y_mcon_gates -= (num_ver_mcon_gates - 1) * mcon_size + (num_ver_mcon_gates - 1) * mcon_spc
                y1_mcon_gates -= (num_ver_mcon_gates - 1) * mcon_size + (num_ver_mcon_gates - 1) * mcon_spc
                x_mcon_gates += mcon_size + mcon_spc
                x1_mcon_gates += mcon_size + mcon_spc
            # up_gate_connection.shapes(l_licon).insert(licon_box_up)
            up_gate_connection.shapes(l_npc).insert(npc_box_up)
            # nmos_cell.shapes(l_li).insert(li_path_up)

        # licon_cell.shapes(l_licon).insert(licon_diff_contact_left)
        # licon_cell.shapes(l_licon).insert(licon_diff_contact_right)

        # licon_cell.shapes(l_licon).insert(licon_between_fingers)
        # hor_licon_diff_arr = pya.CellInstArray(licon_cell.cell_index(),pya.Trans(pya.Point(0,0)),pya.Vector(2*licon_size,0),pya.Vector(0,0),num_hori_licon_diff,0)

        # licon_between_fingers_cell.insert(hor_licon_diff_arr)

        # mcon_tran_sides_cell.shapes(l_mcon).insert(mcon_diff_left)
        # mcon_tran_sides_cell.shapes(l_mcon).insert(mcon_diff_right)
        mcon_between_fingers_cell.shapes(l_mcon).insert(mcon_between_fingers)

        li_between_fingers_cell.shapes(l_li).insert(li_between_fingers_path)
        li_between_fingers_cell.shapes(l_met1).insert(met1_between_fingers_path)

        down_iteration = self.n
        up_iteration = self.n
        down_iteration_distance = diffusion_width_big + channel_length  # distance to iterate down gate connection
        up_iteration_distance = down_iteration_distance
        iteration_distance_group = 2 * self.n * (diffusion_width_big + channel_length)
        if self.connection == 1:  # for gate_connection_down_only
            down_iteration = nf
            up_iteration = 0
            down_iteration_distance = diffusion_width_big + channel_length
            iteration_distance_group = 0

        elif self.connection == 0:  # for gate_connection_up_only
            up_iteration = nf
            down_iteration = 0
            up_iteration_distance = diffusion_width_big + channel_length
            shift_distance = 0
            iteration_distance_group = 0
        bottom_connection = pya.CellInstArray(down_gate_connection.cell_index(), pya.Trans(pya.Point(0, 0)),
                                              pya.Vector(down_iteration_distance, 0),
                                              pya.Vector(iteration_distance_group, 0), down_iteration,
                                              math.ceil(nf / (2 * self.n)))
        nmos_cell.insert(bottom_connection)

        upper_connection = pya.CellInstArray(up_gate_connection.cell_index(), pya.Trans(pya.Point(shift_distance, 0)),
                                             pya.Vector(up_iteration_distance, 0),
                                             pya.Vector(iteration_distance_group, 0), up_iteration,
                                             max(1, nf / self.n - math.ceil(nf / (2 * self.n))))
        nmos_cell.insert(upper_connection)

        # fingers = pya.CellInstArray(gate_cell.cell_index(), pya.Trans(pya.Point(0, 0)),
        # pya.Vector(diffusion_width_big + channel_length, 0), pya.Vector(0, 0), nf, 0)
        # nmos_cell.insert(fingers)

        # iteration_distance_licon = diffusion_width_small  - diff_licon_enc_horzintal + channel_length + (diffusion_width_big-licon_size)/2

        if nf :
            licon_between_fingers_arr = pya.CellInstArray(licon_between_fingers_cell.cell_index(),
                                                          pya.Trans(pya.Point(0, 0)),
                                                          pya.Vector(0, 2 * licon_size),
                                                          pya.Vector(diffusion_width_big + channel_length, 0),
                                                          num_ver_licon,
                                                          nf + 1)
            nmos_cell.insert(licon_between_fingers_arr)

        # licon_diff_contact = pya.CellInstArray(licon_cell.cell_index(), pya.Trans(pya.Point(0, 0)), pya.Vector(0, 0),
        # pya.Vector(0, 2 * licon_size), 0, num_ver_licon)
        # nmos_cell.insert(licon_diff_contact)

        if nf :
            licon_between_fingers_arr = pya.CellInstArray(li_between_fingers_cell.cell_index(),
                                                          pya.Trans(pya.Point(0, 0)),
                                                          pya.Vector(diffusion_width_big + channel_length, 0),
                                                          pya.Vector(0, 0),
                                                          nf + 1, 1)
            nmos_cell.insert(licon_between_fingers_arr)

        # mcon_diff_sides_arr = pya.CellInstArray(mcon_tran_sides_cell.cell_index(),
        # pya.Trans(pya.Point(0, free_spc_mcon_diff / 2)),
        # pya.Vector(0, mcon_spc + mcon_size), pya.Vector(0, 0), num_ver_mcon, 0)
        # nmos_cell.insert(mcon_diff_sides_arr)

        if nf :
            mcon_diff_bet_fing = pya.CellInstArray(mcon_between_fingers_cell.cell_index(), pya.Trans(pya.Point(0, 0)),
                                                   pya.Vector(diffusion_width_big + channel_length, 0),
                                                   pya.Vector(0, mcon_spc + mcon_size), nf + 1, num_ver_mcon)
            nmos_cell.insert(mcon_diff_bet_fing)

        multiple_transistors = pya.CellInstArray(nmos_cell.cell_index(), pya.Trans(pya.Point(0, 0)),
                                                 pya.Vector(diffusion_total_width + 2 * npsdm_enc_diff + npsdm_spc, 0),
                                                 pya.Vector(0, 0), multipliers, 1)

        self.cell.insert(multiple_transistors)

        tap_width = 0.26 * PERCISION
        if self.gr:
            if self.connection == 0:  # gate_up
                guard_up = contact_gate_box_up.p2.y
                guard_down = diff_box.p1.y
            elif self.connection == 2:  # alternate_mode
                guard_up = contact_gate_box_up.p2.y
                guard_down = contact_gate_box_down.p1.y

            else:  # gate_down
                guard_down = contact_gate_box_down.p1.y
                guard_up = diff_box.p2.y

            guard_ring_lower_left = pya.Point(diff_box.p1.x - 2 * npsdm_enc_diff - npsdm_spc_opposite - tap_width / 2,
                                              guard_down - 2 * npsdm_enc_diff - npsdm_spc_opposite - tap_width / 2)
            guard_ring_upper_left = pya.Point(guard_ring_lower_left.x,
                                              guard_up + 2 * npsdm_enc_diff + npsdm_spc_opposite + tap_width / 2)
            guard_ring_upper_right = pya.Point(
                multipliers * diffusion_total_width + 2 * multipliers * npsdm_enc_diff + (
                        multipliers - 1) * npsdm_spc + npsdm_spc_opposite + tap_width / 2, guard_ring_upper_left.y)
            guard_ring_lower_right = pya.Point(guard_ring_upper_right.x, guard_ring_lower_left.y)

            guard_ring_path = pya.Path(
                [guard_ring_lower_left, guard_ring_upper_left, guard_ring_upper_right, guard_ring_lower_right,
                 guard_ring_lower_left], tap_width, tap_width / 2, 0)
            psdm_guard_ring_path = pya.Path(
                [guard_ring_lower_left, guard_ring_upper_left, guard_ring_upper_right, guard_ring_lower_right,
                 guard_ring_lower_left], tap_width + 2 * npsdm_enc_diff, (tap_width + 2 * npsdm_enc_diff) / 2, 0)
            gurad_ring_metal1_upper = pya.Path([guard_ring_upper_left, guard_ring_upper_right], tap_width,
                                               tap_width / 2, tap_width / 2)
            self.cell.shapes(l_met1).insert(gurad_ring_metal1_upper)
            gurad_ring_metal1_lower = pya.Path([guard_ring_lower_left, guard_ring_lower_right], tap_width,
                                               tap_width / 2, tap_width / 2)
            self.cell.shapes(l_met1).insert(gurad_ring_metal1_lower)
            gurad_ring_metal1_right = pya.Path([guard_ring_lower_right, guard_ring_upper_right], tap_width,
                                               tap_width / 2, tap_width / 2)
            self.cell.shapes(l_met1).insert(gurad_ring_metal1_right)
            gurad_ring_metal1_left = pya.Path([guard_ring_lower_left, guard_ring_upper_left], tap_width, tap_width / 2,
                                              tap_width / 2)
            self.cell.shapes(l_met1).insert(gurad_ring_metal1_left)

            self.cell.shapes(l_met2).insert(gurad_ring_metal1_upper)
            self.cell.shapes(l_met2).insert(gurad_ring_metal1_lower)
            self.cell.shapes(l_met2).insert(gurad_ring_metal1_right)
            self.cell.shapes(l_met2).insert(gurad_ring_metal1_left)

            self.cell.shapes(l_tap).insert(guard_ring_path)
            self.cell.shapes(l_nsdm).insert(psdm_guard_ring_path)
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

            num_mcon_guard_vert, free_spc_mcon_guard_left = self.number_spc_contacts(distance_cont_guard_vert,
                                                                                     mcon_m1_enc,
                                                                                     mcon_spc, mcon_size)

            mcon_guard_p1_x_left = guard_ring_lower_left.x - mcon_size / 2
            mcon_guard_p1_x_right = guard_ring_lower_right.x - mcon_size / 2
            mcon_guard_p1_y = guard_ring_lower_left.y + free_spc_mcon_guard_left / 2
            mcon_guard_p2_x_left = mcon_guard_p1_x_left + mcon_size
            mcon_guard_p2_x_right = mcon_guard_p1_x_right + mcon_size
            mcon_guard_p2_y = mcon_guard_p1_y + licon_size

            for mcon in range(num_mcon_guard_vert):
                mcon_guard_box_left = pya.Box(mcon_guard_p1_x_left, mcon_guard_p1_y, mcon_guard_p2_x_left,
                                              mcon_guard_p2_y)
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

                self.cell.shapes(l_nwell).insert(
                    psdm_guard_ring_path.bbox().enlarge(nwell_extension , nwell_extension))

