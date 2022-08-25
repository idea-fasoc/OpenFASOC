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
# Mabrains Company LLC
##
# Mabrains NMOS 1.8V Generator for Skywaters 130nm
########################################################################################################################
from .layers_definiations import *
import pya
import math
import os
import sys
# path = os.path.abspath("layers_definiations")
# sys.path.insert(1, path)


# cell_extend_layer = layout.layer(1, 1)
# fill_shape = pya.Box(0,0,100*1000,100*1000)
# top_cell.shapes(cell_extend_layer).insert(fill_shape)


#########################################################################################################################
# Exceptions
#########################################################################################################################
class Error(Exception):
    """Base class for other exceptions"""
    pass


class small_channel_length(Error):
    """Raised When the channel length is < 0.15u"""
    pass


class small_channel_width(Error):
    """Raised When the channel width is < 0.42u"""
    pass


class small_drain_source_area(Error):
    """Raised When the dsa < 1"""
    pass


class gate_connection_error(Error):
    """Raised when the connection value is not 0,1,2"""
    pass


class alternate_connection_error(Error):
    """Raised when the n factor don't play well with alternate factor"""
    pass


class nf_error(Error):
    """Raised when the nf < 1"""
    pass


class layout_not_defined(Error):
    """layout is not defined"""
    pass


class max_drain_source_area(Error):
    """Max Drain Source Area"""


class no_subcircuit_in_netlist(Error):
    """no subcircuit inn netlist"""
#########################################################################################################################


# Drawing functions
#########################################################################################################################
class nmos18_device:

    def __init__(self, w=0.42, l=0.15, nf=1, gr=1,
                 dsa=2,
                 connection=0,
                 n=1,
                 x_offest=0,
                 y_offest=0,
                 conn_num=0,
                 gate_connection="gate_connection_",
                 gate_connection_up="gate_connection_up_",
                 gate_connection_down="gate_connection_down_",
                 drain_connection="drain_connection_",
                 source_connection="source_connection_",
                 layout=None):
        self.w = w
        self.l = l
        self.nf = nf
        self.gr = gr
        self.dsa = dsa
        self.connection = connection
        self.n = n
        self.x_offest = x_offest
        self.y_offest = y_offest
        self.conn_num = str(conn_num)
        self.gate_connection = gate_connection
        self.gate_connection_up = gate_connection_up
        self.gate_connection_down = gate_connection_down
        self.drain_connection = drain_connection
        self.source_connection = source_connection
        self.layout = layout
        self.l_diff_implant = self.layout.layer(nsdm_lay_num, nsdm_lay_dt)
        self.l_guard = self.layout.layer(
            psdm_lay_num, psdm_lay_dt)  # guard ring implant layer
        self.cell_str = "nmos18_w" + str(self.w).replace(".", "p") + "u_l" + str(self.l).replace(".", "p") + "u_nf" + str(
            self.nf) + "_drain_area" + str(self.dsa) + "_gate_connection" + str(self.connection) + "alt" + str(self.n)
        self.percision = 1/self.layout.dbu
        self.mcon_size = 0.17 * self.percision
        # psdm source drain impaln
        self.l_psdm = layout.layer(psdm_lay_num, psdm_lay_dt)
        self.l_nsdm = layout.layer(nsdm_lay_num, nsdm_lay_dt)
        # licon local interconnect
        self.l_licon = layout.layer(licon_lay_num, licon_lay_dt)
        self.l_li = layout.layer(li_lay_num, li_lay_dt)
        self.l_mcon = layout.layer(mcon_lay_num, mcon_lay_dt)
        self.l_met1 = layout.layer(met1_lay_num, met1_lay_dt)
        self.l_tap = layout.layer(tap_lay_num, tap_lay_dt)
        self.l_via = layout.layer(via_lay_num, via_lay_dt)
        self.l_met2 = layout.layer(met2_lay_num, met2_lay_dt)
        self.l_diff = self.layout.layer(diff_lay_num, diff_lay_dt)  # Diffusion
        self.l_poly = self.layout.layer(poly_lay_num, poly_lay_dt)  # Poly

        self.poly_diff_min_enc = 0.13 * self.percision
        self.licon_size = 0.17 * self.percision
        self.licon_spc = 0.17 * self.percision

        self.diff_licon_enc_vertical = 0.08 * self.percision
        self.diff_licon_enc_horzintal = 0.04 * self.percision
        self.liconpoly_enc_vertical = 0.05 * self.percision
        self.liconpoly_enc_horizontal = 0.08 * self.percision
        self.polylicon_spc_diff = 0.22 * self.percision
        self.npc_enc_gate = 0.1 * self.percision
        # the extension of n+ or p+ layer beyond diff to define it's type
        self.npsdm_enc_diff = .125 * self.percision

        # the spacing of different regions of doping
        self.npsdm_spc_opposite = 0.135 * self.percision

        # the spacing of the same type regions of doping
        self.npsdm_spc = 0.38 * self.percision

        self.l_prbndry = self.layout.layer(prbndry_lay_num, prbndry_lay_dt)

    def number_spc_contacts(self, box_width, min_enc, cont_spc, cont_width):
        """ Calculate number of cantacts in a given dimensions and the free space for symmetry.

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
        free_spc = box_width - (num_cont * cont_width +
                                (num_cont - 1) * cont_spc)
        return num_cont, free_spc

    def draw_guard_ring(self, layout, x, y, guard_width, guard_height, precision, tap_width=0.26, cell=None, guard_label=''):
        # psdm source drain impaln
        l_psdm = layout.layer(psdm_lay_num, psdm_lay_dt)
        l_nsdm = layout.layer(nsdm_lay_num, nsdm_lay_dt)
        # licon local interconnect
        l_licon = layout.layer(licon_lay_num, licon_lay_dt)
        l_li = layout.layer(li_lay_num, li_lay_dt)
        l_mcon = layout.layer(mcon_lay_num, mcon_lay_dt)
        l_met1 = layout.layer(met1_lay_num, met1_lay_dt)
        l_tap = layout.layer(tap_lay_num, tap_lay_dt)
        l_via = layout.layer(via_lay_num, via_lay_dt)
        l_met2 = layout.layer(met2_lay_num, met2_lay_dt)
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
        tap_width = tap_width * PERCISION
        guard_ring_lower_left = pya.Point(x, y)
        guard_ring_upper_left = pya.Point(x, y+guard_height)
        guard_ring_upper_right = pya.Point(x+guard_width, y+guard_height)
        guard_ring_lower_right = pya.Point(
            guard_ring_upper_right.x, guard_ring_lower_left.y)
        guard_ring_path = pya.Path(
            [guard_ring_lower_left, guard_ring_upper_left, guard_ring_upper_right, guard_ring_lower_right,
             guard_ring_lower_left], tap_width, tap_width / 2, 0)
        psdm_guard_ring_path = pya.Path(
            [guard_ring_lower_left, guard_ring_upper_left, guard_ring_upper_right, guard_ring_lower_right,
             guard_ring_lower_left], tap_width + 2 * npsdm_enc_diff, (tap_width + 2 * npsdm_enc_diff) / 2, 0)
        gurad_ring_metal1_upper = pya.Path([guard_ring_upper_left, guard_ring_upper_right], tap_width, tap_width / 2,
                                           tap_width / 2)
        cell.shapes(l_met1).insert(gurad_ring_metal1_upper)
        gurad_ring_metal1_lower = pya.Path([guard_ring_lower_left, guard_ring_lower_right], tap_width, tap_width / 2,
                                           tap_width / 2)
        cell.shapes(l_met1).insert(gurad_ring_metal1_lower)
        gurad_ring_metal1_right = pya.Path([guard_ring_lower_right, guard_ring_upper_right], tap_width, tap_width / 2,
                                           tap_width / 2)
        cell.shapes(l_met1).insert(gurad_ring_metal1_right)
        gurad_ring_metal1_left = pya.Path([guard_ring_lower_left, guard_ring_upper_left], tap_width, tap_width / 2,
                                          tap_width / 2)
        cell.shapes(l_met1).insert(gurad_ring_metal1_left)
        cell.shapes(l_met2).insert(gurad_ring_metal1_upper)
        cell.shapes(l_met2).insert(gurad_ring_metal1_lower)
        cell.shapes(l_met2).insert(gurad_ring_metal1_right)
        cell.shapes(l_met2).insert(gurad_ring_metal1_left)
        cell.shapes(l_tap).insert(guard_ring_path)
        # if type == 'p':
        #     cell.shapes(l_psdm).insert(psdm_guard_ring_path)
        # if type == 'n':
        cell.shapes(self.l_guard).insert(psdm_guard_ring_path)
        cell.shapes(l_li).insert(guard_ring_path)
        # top_nmos_cell.shapes(l_met1).insert(guard_ring_path)

        distance_cont_guard_vert_licon = guard_ring_upper_left.y - \
            guard_ring_lower_left.y - licon_size - 2*licon_size
        num_licon_guard_vert, free_spc_licon_guard_left = self.number_spc_contacts(distance_cont_guard_vert_licon,
                                                                                   mcon_m1_enc,
                                                                                   licon_size, licon_size)
        licon_guard_p1_x_left = guard_ring_lower_left.x - licon_size / 2
        licon_guard_p1_x_right = guard_ring_lower_right.x - licon_size / 2
        licon_guard_p1_y = guard_ring_lower_left.y + \
            free_spc_licon_guard_left / 2 + licon_size/2 + licon_size
        licon_guard_p2_x_left = licon_guard_p1_x_left + licon_size
        licon_guard_p2_x_right = licon_guard_p1_x_right + licon_size
        licon_guard_p2_y = licon_guard_p1_y + licon_size
        # drawing vertical licon in guard_ring
        for licon in range(num_licon_guard_vert):
            licon_guard_box_left = pya.Box(licon_guard_p1_x_left, licon_guard_p1_y, licon_guard_p2_x_left,
                                           licon_guard_p2_y)
            licon_guard_box_right = pya.Box(licon_guard_p1_x_right, licon_guard_p1_y, licon_guard_p2_x_right,
                                            licon_guard_p2_y)
            cell.shapes(l_licon).insert(licon_guard_box_left)
            cell.shapes(l_licon).insert(licon_guard_box_right)
            licon_guard_p1_y += 2 * licon_size
            licon_guard_p2_y += 2 * licon_size
        distance_cont_guard_vert_mcon = guard_ring_upper_left.y - \
            guard_ring_lower_left.y - mcon_size - 2*mcon_spc
        num_mcon_guard_vert, free_spc_mcon_guard_left = self.number_spc_contacts(distance_cont_guard_vert_mcon, mcon_m1_enc,
                                                                                 mcon_spc, mcon_size)
        mcon_guard_p1_x_left = guard_ring_lower_left.x - mcon_size / 2
        mcon_guard_p1_x_right = guard_ring_lower_right.x - mcon_size / 2
        mcon_guard_p1_y = guard_ring_lower_left.y + \
            free_spc_mcon_guard_left / 2 + mcon_size/2 + mcon_spc
        mcon_guard_p2_x_left = mcon_guard_p1_x_left + mcon_size
        mcon_guard_p2_x_right = mcon_guard_p1_x_right + mcon_size
        mcon_guard_p2_y = mcon_guard_p1_y + licon_size
        for mcon in range(num_mcon_guard_vert):
            mcon_guard_box_left = pya.Box(
                mcon_guard_p1_x_left, mcon_guard_p1_y, mcon_guard_p2_x_left, mcon_guard_p2_y)
            mcon_guard_box_right = pya.Box(mcon_guard_p1_x_right, mcon_guard_p1_y, mcon_guard_p2_x_right,
                                           mcon_guard_p2_y)
            cell.shapes(l_mcon).insert(mcon_guard_box_left)
            cell.shapes(l_mcon).insert(mcon_guard_box_right)
            mcon_guard_p1_y += mcon_size + mcon_spc
            mcon_guard_p2_y += mcon_size + mcon_spc
        distance_cont_guard_vert_via = guard_ring_upper_left.y - \
            guard_ring_lower_left.y - via_size - 2*via_spc
        num_via_guard_vert, free_spc_via_guard_left = self.number_spc_contacts(distance_cont_guard_vert_via,
                                                                               via_met_enc,
                                                                               via_spc, via_size)
        via_guard_p1_x_left = guard_ring_lower_left.x - via_size / 2
        via_guard_p1_x_right = guard_ring_lower_right.x - via_size / 2
        via_guard_p1_y = guard_ring_lower_left.y + \
            free_spc_via_guard_left / 2 + via_size/2 + via_spc
        via_guard_p2_x_left = via_guard_p1_x_left + via_size
        via_guard_p2_x_right = via_guard_p1_x_right + via_size
        via_guard_p2_y = via_guard_p1_y + via_size
        for via in range(num_via_guard_vert):
            via_guard_box_left = pya.Box(via_guard_p1_x_left, via_guard_p1_y, via_guard_p2_x_left,
                                         via_guard_p2_y)
            via_guard_box_right = pya.Box(via_guard_p1_x_right, via_guard_p1_y, via_guard_p2_x_right,
                                          via_guard_p2_y)
            cell.shapes(l_via).insert(via_guard_box_left)
            cell.shapes(l_via).insert(via_guard_box_right)
            via_guard_p1_y += via_size + via_spc
            via_guard_p2_y += via_size + via_spc
        distance_cont_guard_hori = (
            guard_ring_upper_right.x - guard_ring_upper_left.x) - 2 * mcon_spc
        num_licon_guard_hori, free_spc_licon_guard_hori = self.number_spc_contacts(distance_cont_guard_hori,
                                                                                   mcon_m1_enc,
                                                                                   licon_size, licon_size)
        licon_guard_p1_x_hori = guard_ring_lower_left.x + \
            free_spc_licon_guard_hori / 2 + mcon_spc
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
            cell.shapes(l_licon).insert(licon_guard_box_upper)
            cell.shapes(l_licon).insert(licon_guard_box_lower)
            licon_guard_p1_x_hori += 2 * licon_size
            licon_guard_p2_x_hori += 2 * licon_size
            num_mcon_guard_hori, free_spc_mcon_guard_hori = self.number_spc_contacts(distance_cont_guard_hori,
                                                                                     mcon_m1_enc,
                                                                                     mcon_spc, mcon_size)
            mcon_guard_p1_x_hori = guard_ring_lower_left.x + \
                free_spc_mcon_guard_hori / 2 + mcon_spc
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
                cell.shapes(l_mcon).insert(mcon_guard_box_upper)
                cell.shapes(l_mcon).insert(mcon_guard_box_lower)
                mcon_guard_p1_x_hori += mcon_size + mcon_spc
                mcon_guard_p2_x_hori += mcon_size + mcon_spc
            num_via_guard_hori, free_spc_via_guard_hori = self.number_spc_contacts(distance_cont_guard_hori,
                                                                                   via_met_enc,
                                                                                   via_spc, via_size)
            via_guard_p1_x_hori = guard_ring_lower_left.x + \
                free_spc_via_guard_hori / 2 + via_spc
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
                cell.shapes(l_via).insert(via_guard_box_upper)
                cell.shapes(l_via).insert(via_guard_box_lower)
                via_guard_p1_x_hori += via_size + via_spc
                via_guard_p2_x_hori += via_size + via_spc

            gurad_ring_metal1_right_bbox = gurad_ring_metal1_right.bbox()
            if guard_label != '':
                guard_connection_text = pya.Text(guard_label,
                                                 gurad_ring_metal1_right_bbox.center().x,
                                                 gurad_ring_metal1_right_bbox.center().y,)
                cell.shapes(self.l_met2_label).insert(guard_connection_text)

    def draw_diffusion_box(self):
        """ Draw the diffusion box with it's surronding type layer
        """
        # Diffusion width of single drain or source
        self.diffusion_width = self.dsa * self.mcon_size + \
            (self.dsa - 1) * self.mcon_spc + 2 * self.liconpoly_spc
        self.channel_length = self.l * self.percision

        # total diffusion width including gates
        self.diffusion_total_width = self.nf * self.channel_length + \
            (self.nf - 1) * self.diffusion_width + 2 * self.diffusion_width
        self.channel_width = self.w * self.percision
        self.diff_box = pya.Box(
            0, 0, self.diffusion_total_width, self.channel_width)
        self.npsdm_enc_diff = .125 * self.percision
        # the box that gives the diffusion box it's type
        self.nsdm_box = self.diff_box.bbox().enlarge(
            self.npsdm_enc_diff, self.npsdm_enc_diff)
        self.nmos_cell.shapes(self.l_diff_implant).insert(self.nsdm_box)
        self.nmos_cell.shapes(self.l_diff).insert(self.diff_box)

    def draw_gates(self):
        x = 0
        self.multipliers = 1
        # draw the gate fingers
        for finger in range(self.nf):
            gate_box = pya.Box(self.diffusion_width + x, -self.poly_diff_min_enc, self.channel_length + self.diffusion_width + x,
                               self.channel_width + self.poly_diff_min_enc)

            self.nmos_cell.shapes(self.l_poly).insert(gate_box)

            x += self.channel_length + self.diffusion_width

        gate_box = pya.Box(self.diffusion_width, -self.poly_diff_min_enc, self.channel_length + self.diffusion_width,
                           self.channel_width + self.poly_diff_min_enc)
        #########################################################################################################################
        # connection of gate box dimensions
        #########################################################################################################################

        contact_gate_width = 2 * self.liconpoly_enc_horizontal + self.licon_size
        contact_gate_height = 2 * self.liconpoly_enc_vertical + 3 * self.licon_size
        num_horizontal_licon_gate = 1

        free_spc_licon_gate = contact_gate_width - \
            (2 * num_horizontal_licon_gate - 1) * self.licon_size
        if self.channel_length > contact_gate_width:
            # calculate number of horizontal licon in gate connection todo use function to do
            contact_gate_width = self.channel_length
            num_horizontal_licon_gate, free_spc_licon_gate = self.number_spc_contacts(
                self.channel_length, self.liconpoly_enc_horizontal, self.licon_size, self.licon_size)
        elif self.channel_length < contact_gate_width and self.nf != 1 and self.dsa == 1:
            self.connection = 2

        if self.connection == 0 or self.connection == 2:
            up_gate_connection = self.layout.create_cell("up_gate_connection")
        if self.connection == 1 or self.connection == 2:
            down_gate_connection = self.layout.create_cell(
                "down_gate_connection")

        # contacte_gate_box
        contact_gate_box_down = pya.Box(gate_box.center().x - contact_gate_width / 2,
                                        -self.polylicon_spc_diff - contact_gate_height,
                                        gate_box.center().x + contact_gate_width / 2, -self.polylicon_spc_diff)
        neck_box_down = pya.Box(self.diffusion_width, -self.polylicon_spc_diff, self.channel_length + self.diffusion_width,
                                -self.poly_diff_min_enc)
        # licon_box_down = pya.Box(contact_gate_box_down.center().x - self.licon_size/2, contact_gate_box_down.center().y-(self.licon_size/2),contact_gate_box_down.center().x + self.licon_size/2,contact_gate_box_down.center().y + self.licon_size/2)
        npc_box_down = pya.Box(contact_gate_box_down.p1.x - self.npc_enc_gate, contact_gate_box_down.p1.y - self.npc_enc_gate,
                               contact_gate_box_down.p2.x + self.npc_enc_gate, contact_gate_box_down.p2.y + self.npc_enc_gate)
        li_box_down = pya.Box(self.diff_box.p1.x, contact_gate_box_down.p1.y,
                              self.diff_box.p1.x + self.multipliers * self.diffusion_total_width + (
                                  2 * self.multipliers - 2) * self.npsdm_enc_diff + (self.multipliers - 1) * self.npsdm_spc,
                              contact_gate_box_down.p2.y)

        self.gate_connection_text_down = pya.Text(self.gate_connection_text_up, li_box_down.center().x,
                                                  li_box_down.center().y)

        self.contact_gate_box_up = pya.Box(gate_box.center().x - contact_gate_width / 2, self.channel_width + self.polylicon_spc_diff,
                                           gate_box.center().x + contact_gate_width / 2,
                                           self.channel_width + self.polylicon_spc_diff + contact_gate_height)
        self.neck_box_up = pya.Box(self.diffusion_width, self.channel_width + self.poly_diff_min_enc,
                                   self.channel_length + self.diffusion_width,
                                   self.channel_width + self.polylicon_spc_diff)
        self.licon_box_up = pya.Box(self.contact_gate_box_up.center().x - self.licon_size / 2,
                                    self.contact_gate_box_up.center().y - (self.licon_size / 2),
                                    self.contact_gate_box_up.center().x + self.licon_size / 2,
                                    self.contact_gate_box_up.center().y + self.licon_size / 2)
        self.npc_box_up = pya.Box(self.contact_gate_box_up.p1.x - 1.6 * self.npc_enc_gate, self.contact_gate_box_up.p1.y - self.npc_enc_gate,
                                  self.contact_gate_box_up.p2.x + 1.6 * self.npc_enc_gate, self.contact_gate_box_up.p2.y + self.npc_enc_gate)

    def between_fingers_connection(self):
        if self.nf:
            licon_between_fingers_arr = pya.CellInstArray(self.licon_between_fingers_cell.cell_index(),
                                                          pya.Trans(
                pya.Point(0, 0)),
                pya.Vector(
                0, 2 * self.licon_size),
                pya.Vector(
                self.diffusion_width + self.channel_length, 0),
                self.num_ver_licon,
                self.nf + 1)
            self.nmos_cell.insert(licon_between_fingers_arr)

        self.nmos_cell.flatten(True)

        if self.nf:
            li_between_fingers_arr = pya.CellInstArray(self.li_between_fingers_cell.cell_index(),
                                                       pya.Trans(
                                                           pya.Point(0, 0)),
                                                       pya.Vector(
                self.diffusion_width + self.channel_length, 0),
                pya.Vector(0, 0),
                self.nf + 1, 1)

            self.nmos_cell.insert(li_between_fingers_arr)

        self.nmos_cell.flatten(True)

        if self.nf:
            mcon_diff_bet_fing = pya.CellInstArray(self.mcon_between_fingers_cell.cell_index(), pya.Trans(pya.Point(0, 0)),
                                                   pya.Vector(
                self.diffusion_width + self.channel_length, 0),
                pya.Vector(0, self.mcon_spc + self.mcon_size), self.nf + 1, self.num_ver_mcon)
            self.nmos_cell.insert(mcon_diff_bet_fing)

        self.nmos_cell.flatten(True)

    def guard_ring_points(self):
        tap_width = 0.26 * self.percision
        if self.connection == 0:  # gate_up
            guard_up = self.contact_gate_box_up.p2.y
            guard_down = self.diff_box.p1.y
        elif self.connection == 2:  # alternate_mode
            guard_up = self.contact_gate_box_up.p2.y
            guard_down = self.contact_gate_box_down.p1.y

        else:  # gate_down
            guard_down = self.contact_gate_box_down.p1.y
            guard_up = self.diff_box.p2.y

        guard_ring_lower_left = pya.Point(self.diff_box.p1.x - 2 * self.npsdm_enc_diff - self.npsdm_spc_opposite - tap_width / 2,
                                          guard_down - 2 * self.npsdm_enc_diff - self.npsdm_spc_opposite - tap_width / 2)
        guard_ring_upper_left = pya.Point(guard_ring_lower_left.x,
                                          guard_up + 2 * self.npsdm_enc_diff + self.npsdm_spc_opposite + tap_width / 2)
        guard_ring_upper_right = pya.Point(
            self.multipliers * self.diffusion_total_width + 2 * self.multipliers * self.npsdm_enc_diff + (
                self.multipliers - 1) * self.npsdm_spc + self.npsdm_spc_opposite + tap_width / 2, guard_ring_upper_left.y)
        guard_ring_lower_right = pya.Point(
            guard_ring_upper_right.x, guard_ring_lower_left.y)
        # primitive_boundry
        prbndry_box = pya.Box(guard_ring_lower_left, guard_ring_upper_right)
        guard_ring_width = (guard_ring_lower_right.x -
                            guard_ring_lower_left.x)/self.percision
        guard_ring_height = (guard_ring_upper_right.y -
                             guard_ring_lower_right.y)/self.percision
        self.nmos_cell.shapes(self.l_prbndry).insert(prbndry_box)

        if self.gr:
            pass
            self.draw_guard_ring(layout=self.layout, x=guard_ring_lower_left.x, y=guard_ring_lower_left.y,
                                 guard_width=guard_ring_width, guard_height=guard_ring_height, precision=self.percision, cell=self.nmos_cell)


    def choose_gate_connection_top_bottom(self):
        shift_distance = self.n * (self.diffusion_width + self.channel_length)

        if self.connection == 1 or self.connection == 2:
            down_gate_connection.shapes(l_poly).insert(contact_gate_box_down)
            down_gate_connection.shapes(l_poly).insert(neck_box_down)

            y_sh = 0

            self.nmos_cell.shapes(self.l_met1_label).insert(
                gate_connection_text_down)
            p1_x = contact_gate_box_down.p1.x + free_spc_licon_gate / 2
            p1_y = contact_gate_box_down.p1.y + liconpoly_enc_vertical
            p2_x = contact_gate_box_down.p1.x + free_spc_licon_gate / 2 + licon_size
            p2_y = contact_gate_box_down.p1.y + liconpoly_enc_vertical + licon_size
            for licon_ct in range(num_horizontaself.l_licon_gate):
                licon_box_down = pya.Box(p1_x, p1_y, p2_x, p2_y)

                down_gate_connection.shapes(self.l_licon).insert(licon_box_down)
                p1_y += 2 * licon_size
                p2_y += 2 * licon_size
                licon_box_down = pya.Box(p1_x, p1_y, p2_x, p2_y)
                down_gate_connection.shapes(self.l_licon).insert(licon_box_down)
                p1_y -= 2 * licon_size
                p2_y -= 2 * licon_size

                p1_x += 2 * licon_size
                p2_x += 2 * licon_size

            self.nmos_cell.shapes(self.l_li).insert(li_box_down)
            self.nmos_cell.shapes(self.l_met1).insert(li_box_down)
            down_gate_connection.shapes(l_npc).insert(npc_box_down)

            x_mcon_gates = li_box_down.p1.x + free_spc_mcon_gates_h / 2
            y_mcon_gates = li_box_down.p1.y + free_spc_mcon_gates_v / 2
            y1_mcon_gates = y_mcon_gates + mcon_size

            for mcon in range(num_hor_mcon_gates):
                x1_mcon_gates = x_mcon_gates + mcon_size
                mcon_box_gate = pya.Box(
                    x_mcon_gates, y_mcon_gates, x1_mcon_gates, y1_mcon_gates)
                self.nmos_cell.shapes(self.l_mcon).insert(mcon_box_gate)
                for mcon1 in range(num_ver_mcon_gates - 1):
                    y_mcon_gates += mcon_size + mcon_spc
                    y1_mcon_gates += mcon_size + mcon_spc
                    mcon_box_gate = pya.Box(
                        x_mcon_gates, y_mcon_gates, x1_mcon_gates, y1_mcon_gates)
                    self.nmos_cell.shapes(self.l_mcon).insert(mcon_box_gate)
                y_mcon_gates -= (num_ver_mcon_gates - 1) * \
                    mcon_size + (num_ver_mcon_gates - 1) * mcon_spc
                y1_mcon_gates -= (num_ver_mcon_gates - 1) * \
                    mcon_size + (num_ver_mcon_gates - 1) * mcon_spc
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

            gate_connection_text_up = pya.Text(gate_connection_text_up, li_box_up.center().x,
                                               li_box_up.center().y)
            self.nmos_cell.shapes(self.l_met1_label).insert(gate_connection_text_up)

            self.nmos_cell.shapes(self.l_li).insert(li_box_up)
            self.nmos_cell.shapes(self.l_met1).insert(li_box_up)
            for licon_ct in range(num_horizontaself.l_licon_gate):
                licon_box_up = pya.Box(p1_x, p1_y, p2_x, p2_y)

                up_gate_connection.shapes(self.l_licon).insert(licon_box_up)
                p1_y += 2 * licon_size
                p2_y += 2 * licon_size
                licon_box_up = pya.Box(p1_x, p1_y, p2_x, p2_y)
                up_gate_connection.shapes(self.l_licon).insert(licon_box_up)
                p1_y -= 2 * licon_size
                p2_y -= 2 * licon_size

                p1_x += 2 * licon_size
                p2_x += 2 * licon_size

            x_mcon_gates = li_box_up.p1.x + free_spc_mcon_gates_h / 2
            y_mcon_gates = li_box_up.p1.y + free_spc_mcon_gates_v / 2
            y1_mcon_gates = y_mcon_gates + mcon_size

            for mcon in range(num_hor_mcon_gates):
                x1_mcon_gates = x_mcon_gates + mcon_size
                mcon_box_gate = pya.Box(
                    x_mcon_gates, y_mcon_gates, x1_mcon_gates, y1_mcon_gates)
                self.nmos_cell.shapes(self.l_mcon).insert(mcon_box_gate)
                for mcon1 in range(num_ver_mcon_gates - 1):
                    y_mcon_gates += mcon_size + mcon_spc
                    y1_mcon_gates += mcon_size + mcon_spc
                    mcon_box_gate = pya.Box(
                        x_mcon_gates, y_mcon_gates, x1_mcon_gates, y1_mcon_gates)
                    self.nmos_cell.shapes(self.l_mcon).insert(mcon_box_gate)
                y_mcon_gates -= (num_ver_mcon_gates - 1) * \
                    mcon_size + (num_ver_mcon_gates - 1) * mcon_spc
                y1_mcon_gates -= (num_ver_mcon_gates - 1) * \
                    mcon_size + (num_ver_mcon_gates - 1) * mcon_spc
                x_mcon_gates += mcon_size + mcon_spc
                x1_mcon_gates += mcon_size + mcon_spc
            up_gate_connection.shapes(l_npc).insert(npc_box_up)

        self.mcon_between_fingers_cell.shapes(self.l_mcon).insert(self.mcon_between_fingers)

        self.li_between_fingers_cell.shapes(self.l_li).insert(self.li_between_fingers_path)
        self.li_between_fingers_cell.shapes(
            self.l_met1).insert(self.met1_between_fingers_path)

        down_iteration = self.n
        up_iteration = self.n
        # distance to iterate down gate connection
        down_iteration_distance = self.diffusion_width + self.channel_length
        up_iteration_distance = down_iteration_distance
        iteration_distance_group = 2 * self.n * \
            (self.diffusion_width + self.channel_length)
        if self.connection == 1:  # for gate_connection_down_only
            down_iteration = self.nf
            up_iteration = 0
            down_iteration_distance = self.diffusion_width + self.channel_length
            iteration_distance_group = 0
            bottom_connection = pya.CellInstArray(down_gate_connection.cell_index(), pya.Trans(pya.Point(0, 0)),
                                                  pya.Vector(
                down_iteration_distance, 0),
                pya.Vector(
                iteration_distance_group, 0), down_iteration,
                math.ceil(self.nf / (2 * self.n)))
            self.nmos_cell.insert(bottom_connection)

        elif self.connection == 0:  # for gate_connection_up_only
            up_iteration = self.nf
            down_iteration = 0
            up_iteration_distance = self.diffusion_width + self.channel_length
            shift_distance = 0
            iteration_distance_group = 0

            repition_b = self.nf / self.n - math.ceil(self.nf / (2 * self.n))

            if self.nf == 1:
                repition_b = 1

            upper_connection = pya.CellInstArray(self.up_gate_connection.cell_index(), pya.Trans(pya.Point(shift_distance, 0)),
                                                 pya.Vector(
                up_iteration_distance, 0),
                pya.Vector(iteration_distance_group, 0), up_iteration, repition_b)

            self.nmos_cell.insert(upper_connection)

        else:
            bottom_connection = pya.CellInstArray(self.down_gate_connection.cell_index(), pya.Trans(pya.Point(0, 0)),
                                                  pya.Vector(
                down_iteration_distance, 0),
                pya.Vector(
                iteration_distance_group, 0), down_iteration,
                math.ceil(self.nf / (2 * self.n)))
            self.nmos_cell.insert(bottom_connection)

            upper_connection = pya.CellInstArray(self.up_gate_connection.cell_index(), pya.Trans(pya.Point(shift_distance, 0)),
                                                 pya.Vector(
                up_iteration_distance, 0),
                pya.Vector(
                iteration_distance_group, 0), up_iteration,
                self.nf / self.n - math.ceil(self.nf / (2 * self.n)))

            self.nmos_cell.insert(upper_connection)

    def draw_drain_source_connection(self):
        # number of vertical licon's diff
        self.num_ver_licon, self.free_space_diff_licon = self.number_spc_contacts(self.channel_width, self.diff_licon_enc_vertical, self.licon_spc,
                                                                                  self.licon_size)
        # number of vertical mcon diff
        num_ver_mcon, free_spc_mcon_diff = self.number_spc_contacts(
            self.channel_width, self.mcon_m1_enc, self.mcon_spc, self.mcon_size)
        num_hori_licon_diff, free_space_licon_diff_hor = self.number_spc_contacts(self.diffusion_width, self.liconpoly_spc, self.licon_size,
                                                                                  self.licon_size)

        sh1 = 0
        for hor_licon_diff in range(num_hori_licon_diff):
            licon_between_fingers = pya.Box(free_space_licon_diff_hor / 2 + sh1,
                                            self.free_space_diff_licon / 2, free_space_licon_diff_hor / 2 + self.licon_size + sh1,
                                            self.free_space_diff_licon / 2 + self.licon_size)
            self.licon_between_fingers_cell.shapes(
                self.l_licon).insert(licon_between_fingers)
            sh1 += 2 * self.licon_size

        # print(num_hori_licon_diff,free_space_licon_diff_hor,diffusion_width)

        num_hori_mcon_diff, free_space_mcon_diff_hor = self.number_spc_contacts(
            self.diffusion_width, 0, self.mcon_spc, self.mcon_size)
        sh2 = 0
        for hor_mcon_diff in range(num_hori_mcon_diff):
            mcon_between_fingers = pya.Box(free_space_mcon_diff_hor / 2 + sh2,
                                           free_spc_mcon_diff / 2,
                                           free_space_mcon_diff_hor / 2 + sh2 + mcon_size,
                                           free_spc_mcon_diff / 2 + self.mcon_size)
            self.mcon_between_fingers_cell.shapes(
                self.l_mcon).insert(mcon_between_fingers)
            sh2 += self.mcon_size + self.mcon_spc

        li_between_fingers_path = pya.Path([pya.Point(self.diffusion_width / 2, self.diff_box.p1.y),
                                            pya.Point(self.diffusion_width / 2, self.diff_box.p2.y)],
                                           self.diffusion_width - self.li_width_reduction)
        met1_between_fingers_path = pya.Path([pya.Point(self.diffusion_width / 2, self.diff_box.p1.y - self.mcon_m1_enc),
                                              pya.Point(self.diffusion_width / 2, self.diff_box.p2.y + self.mcon_m1_enc)],
                                             self.diffusion_width)
        met1_diff_left = pya.Path([pya.Point(self.licon_diff_contact_left.center().x, self.diff_box.p1.y - self.mcon_m1_enc),
                                   pya.Point(self.licon_diff_contact_left.center().x, self.diff_box.p2.y + self.mcon_m1_enc)],
                                  self.m1_width + 2 * self.mcon_m1_enc)
        # drain_connection
        x_offset_drain = 0
        met1_diff_left_bbox = met1_diff_left.bbox()
        for drain in range(math.ceil((self.nf + 1) / 2)):
            drain_connection_text = pya.Text(self.drain_connection_text_input,
                                             met1_diff_left_bbox.center().x + self.x_offest + x_offset_drain,
                                             met1_diff_left_bbox.center().y + self.y_offest)
            self.nmos_cell.shapes(self.l_met1_label).insert(drain_connection_text)
            x_offset_drain = x_offset_drain + 2 * \
                (self.channel_length + self.diffusion_width)

        # source connection
        x_offset_source = self.channel_length + self.diffusion_width
        for source in range(((self.nf + 1) - math.ceil((self.nf + 1) / 2))):
            source_connection_text = pya.Text(self.source_connection_text_input,
                                              met1_diff_left_bbox.center().x + self.x_offest + x_offset_source,
                                              met1_diff_left_bbox.center().y + self.y_offest)
            self.nmos_cell.shapes(self.l_met1_label).insert(source_connection_text)
            x_offset_source = x_offset_source + 2 * \
                (self.channel_length + self.diffusion_width)

        mcon_diff_left = pya.Box(self.licon_diff_contact_left.p1.x,
                                 0, self.licon_diff_contact_left.p1.x + self.mcon_size, self.mcon_size)

        licon_diff_contact_right = pya.Box(self.diff_box.p2.x - self.diff_licon_enc_horzintal - self.licon_size,
                                           self.free_space_diff_licon / 2,
                                           self.diff_box.p2.x - self.diff_licon_enc_horzintal,
                                           self.free_space_diff_licon / 2 + self.licon_size)
        li_diff_right = pya.Path([pya.Point(licon_diff_contact_right.center().x, self.diff_box.p1.y),
                                  pya.Point(licon_diff_contact_right.center().x, self.diff_box.p2.y)], self.li_width)
        mcon_diff_right = pya.Box(licon_diff_contact_right.p1.x, 0, licon_diff_contact_right.p1.x + self.mcon_size,
                                  self.mcon_size)
        met1_diff_right = pya.Path([pya.Point(licon_diff_contact_right.center().x, self.diff_box.p1.y - self.mcon_m1_enc),
                                    pya.Point(licon_diff_contact_right.center().x, self.diff_box.p2.y + self.mcon_m1_enc)],
                                   self.m1_width + 2 * self.mcon_m1_enc)

    def draw_nmos(self):
        """
        Draw nmos 1.8v 

        Parameters
        ----------
        w : double
            Channel width of the transistor 
        l : double 
            Channel length of the transistor 
        nf : integer 
            number of fingers
        gr : bool
            guard ring option 
        dsa : integer max 8
            Area of drain and source 
        connection : 0 , 1 , 2
            0 : gate connection up 
            1 : gate connection down 
            2 : gate connection alternate by factor n
        n : integer
            Alternate factor flip the gates every n in case of alternate option 
        x_offest : offset of the origin in the x_direction
        y_offest : offset of the origin in the y_direction
        conn_num : number of the connection 
        """
        # Netnames
        if self.gate_connection_up == "gate_connection_up_":
            self.gate_connection_text_up = self.gate_connection_up + \
                str(self.conn_num)
        else:
            self.gate_connection_text_up = self.gate_connection_up

        if self.gate_connection_down == "gate_connection_down_":
            self.gate_connection_text_down = self.gate_connection_down + \
                str(self.conn_num)
        else:
            self.gate_connection_text_down = self.gate_connection_down

        if self.gate_connection == "gate_connection_":
            self.gate_connection_text_down = self.gate_connection + \
                str(self.conn_num)
            self.gate_connection_text_up = self.gate_connection + \
                str(self.conn_num)
        else:
            self.gate_connection_text_down = self.gate_connection
            self.gate_connection_text_up = self.gate_connection

        if self.drain_connection == "drain_connection_":
            self.drain_connection_text_input = self.drain_connection + self.conn_num
        else:
            self.drain_connection_text_input = self.drain_connection

        if self.source_connection == "source_connection_":
            self.source_connection_text_input = self.source_connection + self.conn_num
        else:
            self.source_connection_text_input = self.source_connection
        # Exceptions
        if self.w < 0.42:
            raise small_channel_width

        if self.l < 0.15:
            raise small_channel_length

        if self.nf < 1:
            raise nf_error

        if self.dsa < 1:
            raise small_drain_source_area

        if self.dsa > 8:
            raise max_drain_source_area

        if self.connection != 1 and self.connection != 0 and self.connection != 2:
            raise gate_connection_error

        if self.connection == 2 and self.nf % self.n != 0:
            raise alternate_connection_error

        if self.layout is None:
            raise layout_not_defined

        conn_num = str(self.conn_num)
        # layout = pya.Layout()

        # precision value for scaling

        PERCISION = 1 / self.layout.dbu
        liconpoly_spc = 0.055 * PERCISION

        # 1 for source_shared 0 for no nf turned into no of multipliers
        source_shared = 1
        multipliers = 1
        diff_spc = 0.27 * PERCISION

        # the extension of n+ or p+ layer beyond diff to define it's type
        npsdm_enc_diff = .125 * PERCISION

        # the spacing of different regions of doping
        npsdm_spc_opposite = 0.135 * PERCISION

        # the spacing of the same type regions of doping
        npsdm_spc = 0.38 * PERCISION

        # mcon _contact_size
        mcon_size = 0.17 * PERCISION

        # mcon_spacing
        mcon_spc = 0.19 * PERCISION

        # and the channel length is low todo find the length in code

        diffusion_width = self.dsa * mcon_size + \
            (self.dsa - 1) * mcon_spc + 2 * liconpoly_spc

        channel_length = self.l * PERCISION

        if source_shared == 0:
            # if no source sharing nf = 1 and repetition become multiplier
            self.nf = 1

        if self.nf == 1:
            # if self.nf = 1 alternative doesn't make sense so the default is up
            if self.connection == 2:
                self.connection = 0
            # todo :correct the diffusion_total_width of singel finger

        diffusion_total_width = self.nf * channel_length + \
            (self.nf - 1) * diffusion_width + 2 * diffusion_width
        channel_width = self.w * PERCISION

        diff_min_width = 0.28
        poly_min_width = 0.15
        poly_diff_min_enc = 0.13 * PERCISION
        polylicon_spc_diff = 0.22 * PERCISION

        licon_size = 0.17 * PERCISION
        licon_spc = 0.17 * PERCISION

        diff_licon_enc_vertical = 0.08 * PERCISION
        diff_licon_enc_horzintal = 0.04 * PERCISION
        liconpoly_enc_vertical = 0.05 * PERCISION
        liconpoly_enc_horizontal = 0.08 * PERCISION
        li_licon_enc = 0.08 * PERCISION
        npc_enc_gate = 0.1 * PERCISION
        m1_width = 0.17 * PERCISION
        mcon_m1_enc = 0.03 * PERCISION
        mcon_m1_enc_adjacent = 0.06 * PERCISION
        via_size = 0.15 * PERCISION
        via_spc = 0.17 * PERCISION
        via_met_enc = 0.085 * PERCISION
        li_width = 0.17 * PERCISION
        nwell_extension = 0.18 * PERCISION

        # number of vertical licon's diff
        num_ver_licon, free_space_diff_licon = self.number_spc_contacts(channel_width, diff_licon_enc_vertical, licon_spc,
                                                                        licon_size)
        # number of vertical mcon diff
        num_ver_mcon, free_spc_mcon_diff = self.number_spc_contacts(
            channel_width, mcon_m1_enc, mcon_spc, mcon_size)

        # layers_definations
        l_diff = self.layout.layer(diff_lay_num, diff_lay_dt)  # Diffusion
        l_poly = self.layout.layer(poly_lay_num, poly_lay_dt)  # Poly
        # nsdm source drain impalnt
        l_nsdm = self.layout.layer(nsdm_lay_num, nsdm_lay_dt)
        # psdm source drain impaln
        l_psdm = self.layout.layer(psdm_lay_num, psdm_lay_dt)
        # licon local interconnect
        l_licon = self.layout.layer(licon_lay_num, licon_lay_dt)
        l_npc = self.layout.layer(npc_lay_num, npc_lay_dt)
        l_li = self.layout.layer(li_lay_num, li_lay_dt)
        l_mcon = self.layout.layer(mcon_lay_num, mcon_lay_dt)
        l_met1 = self.layout.layer(met1_lay_num, met1_lay_dt)
        l_tap = self.layout.layer(tap_lay_num, tap_lay_dt)
        l_nwell = self.layout.layer(nwell_lay_num, nwell_lay_dt)
        l_via = self.layout.layer(via_lay_num, via_lay_dt)
        l_met2 = self.layout.layer(met2_lay_num, met2_lay_dt)
        l_prbndry = self.layout.layer(prbndry_lay_num, prbndry_lay_dt)
        l_poly_label = self.layout.layer(poly_label_lay_num, poly_label_lay_dt)
        l_met1_label = self.layout.layer(met1_label_lay_num, met1_label_lay_dt)
        self.l_met2_label = self.layout.layer(
            met2_label_lay_num, met2_label_lay_dt)

        ##cells##
        # top_nmos_cell = layout.create_cell("top_nmos_"+str(w)+"_"+str(l))

        self.nmos_cell = self.layout.create_cell(self.cell_str)
        self.licon_between_fingers_cell = self.layout.create_cell(
            "licon_between_fingers")

        self.li_between_fingers_cell = self.layout.create_cell(
            "li_between_fingers")
        self.mcon_between_fingers_cell = self.layout.create_cell(
            "mcon_between_fingers")

        self.draw_diffusion_box()
        self.draw_gates()
        self.between_fingers_connection()
        self.draw_drain_source_connection()
        
        ##

        diff_box = self.diff_box

        # main diff box

        # source drain implant diff
        x = 0

        # # draw the gate fingers
        # for finger in range(self.nf):
        #     gate_box = pya.Box(diffusion_width + x, -poly_diff_min_enc, channel_length + diffusion_width + x,
        #                        channel_width + poly_diff_min_enc)

        #     self.nmos_cell.shapes(l_poly).insert(gate_box)

        #     x += channel_length + diffusion_width

        # gate_box = pya.Box(diffusion_width, -poly_diff_min_enc, channel_length + diffusion_width,
        #                    channel_width + poly_diff_min_enc)
        # #########################################################################################################################
        # # connection of gate box dimensions
        # #########################################################################################################################

        # contact_gate_width = 2 * liconpoly_enc_horizontal + licon_size
        # contact_gate_height = 2 * liconpoly_enc_vertical + 3 * licon_size
        # num_horizontal_licon_gate = 1

        # free_spc_licon_gate = contact_gate_width - \
        #     (2 * num_horizontal_licon_gate - 1) * licon_size
        # if channel_length > contact_gate_width:
        #     # calculate number of horizontal licon in gate connection todo use function to do
        #     contact_gate_width = channel_length
        #     spc_for_licon_gate = channel_length - 2 * liconpoly_enc_horizontal
        #     num_horizontal_licon_gate = int(
        #         ((spc_for_licon_gate / licon_size) + 1) / 2)
        #     free_spc_licon_gate = channel_length - \
        #         (2 * num_horizontal_licon_gate - 1) * licon_size
        # elif channel_length < contact_gate_width and self.nf != 1 and self.dsa == 1:
        #     self.connection = 2

        # if self.connection == 0 or self.connection == 2:
        #     up_gate_connection = self.layout.create_cell("up_gate_connection")
        # if self.connection == 1 or self.connection == 2:
        #     down_gate_connection = self.layout.create_cell(
        #         "down_gate_connection")

        # # contacte_gate_box
        # contact_gate_box_down = pya.Box(gate_box.center().x - contact_gate_width / 2,
        #                                 -polylicon_spc_diff - contact_gate_height,
        #                                 gate_box.center().x + contact_gate_width / 2, -polylicon_spc_diff)
        # neck_box_down = pya.Box(diffusion_width, -polylicon_spc_diff, channel_length + diffusion_width,
        #                         -poly_diff_min_enc)
        # # licon_box_down = pya.Box(contact_gate_box_down.center().x - licon_size/2, contact_gate_box_down.center().y-(licon_size/2),contact_gate_box_down.center().x + licon_size/2,contact_gate_box_down.center().y + licon_size/2)
        # npc_box_down = pya.Box(contact_gate_box_down.p1.x - npc_enc_gate, contact_gate_box_down.p1.y - npc_enc_gate,
        #                        contact_gate_box_down.p2.x + npc_enc_gate, contact_gate_box_down.p2.y + npc_enc_gate)
        # li_box_down = pya.Box(diff_box.p1.x, contact_gate_box_down.p1.y,
        #                       diff_box.p1.x + multipliers * diffusion_total_width + (
        #                           2 * multipliers - 2) * npsdm_enc_diff + (multipliers - 1) * npsdm_spc,
        #                       contact_gate_box_down.p2.y)

        # gate_connection_text_down = pya.Text(self.gate_connection_text_up, li_box_down.center().x,
        #                                      li_box_down.center().y)

        # num_hori_licon_diff, free_space_licon_diff_hor = self.number_spc_contacts(diffusion_width, liconpoly_spc, licon_size,
        #                                                                           licon_size)

        # sh1 = 0
        # for hor_licon_diff in range(num_hori_licon_diff):
        #     licon_between_fingers = pya.Box(free_space_licon_diff_hor / 2 + sh1,
        #                                     free_space_diff_licon / 2, free_space_licon_diff_hor / 2 + licon_size + sh1,
        #                                     free_space_diff_licon / 2 + licon_size)
        #     licon_between_fingers_cell.shapes(
        #         l_licon).insert(licon_between_fingers)
        #     sh1 += 2 * licon_size

        # # print(num_hori_licon_diff,free_space_licon_diff_hor,diffusion_width)

        # num_hori_mcon_diff, free_space_mcon_diff_hor = self.number_spc_contacts(
        #     diffusion_width, 0, mcon_spc, mcon_size)
        # sh2 = 0
        # for hor_mcon_diff in range(num_hori_mcon_diff):
        #     mcon_between_fingers = pya.Box(free_space_mcon_diff_hor / 2 + sh2,
        #                                    free_spc_mcon_diff / 2,
        #                                    free_space_mcon_diff_hor / 2 + sh2 + mcon_size,
        #                                    free_spc_mcon_diff / 2 + mcon_size)
        #     mcon_between_fingers_cell.shapes(
        #         l_mcon).insert(mcon_between_fingers)
        #     sh2 += mcon_size + mcon_spc

        # if channel_length < 0.17 * PERCISION:
        #     li_width_reduction = 0.17 * PERCISION - channel_length
        # else:
        #     li_width_reduction = 0

        # li_between_fingers_path = pya.Path([pya.Point(diffusion_width / 2, diff_box.p1.y),
        #                                     pya.Point(diffusion_width / 2, diff_box.p2.y)],
        #                                    diffusion_width - li_width_reduction)
        # met1_between_fingers_path = pya.Path([pya.Point(diffusion_width / 2, diff_box.p1.y - mcon_m1_enc),
        #                                       pya.Point(diffusion_width / 2, diff_box.p2.y + mcon_m1_enc)],
        #                                      diffusion_width)

        # contact_gate_box_up = pya.Box(gate_box.center().x - contact_gate_width / 2, channel_width + polylicon_spc_diff,
        #                               gate_box.center().x + contact_gate_width / 2,
        #                               channel_width + polylicon_spc_diff + contact_gate_height)
        # neck_box_up = pya.Box(diffusion_width, channel_width + poly_diff_min_enc,
        #                       channel_length + diffusion_width,
        #                       channel_width + polylicon_spc_diff)
        # licon_box_up = pya.Box(contact_gate_box_up.center().x - licon_size / 2,
        #                        contact_gate_box_up.center().y - (licon_size / 2),
        #                        contact_gate_box_up.center().x + licon_size / 2,
        #                        contact_gate_box_up.center().y + licon_size / 2)
        # npc_box_up = pya.Box(contact_gate_box_up.p1.x - 1.6 * npc_enc_gate, contact_gate_box_up.p1.y - npc_enc_gate,
        #                      contact_gate_box_up.p2.x + 1.6 * npc_enc_gate, contact_gate_box_up.p2.y + npc_enc_gate)
        # li_path_up = pya.Path(
        #     [pya.Point(diff_box.p1.x, licon_box_up.center().y),
        #      pya.Point(diff_box.p2.x, licon_box_up.center().y)],
        #     li_width)

        # licon_diff_contact_left = pya.Box(diff_box.p1.x + diff_licon_enc_horzintal, free_space_diff_licon / 2,
        #                                   diff_licon_enc_horzintal + licon_size, free_space_diff_licon / 2 + licon_size)
        # li_diff_left = pya.Path([pya.Point(licon_diff_contact_left.center().x, diff_box.p1.y),
        #                         pya.Point(licon_diff_contact_left.center().x, diff_box.p2.y)], li_width)

        # shift distance for alternate mode
        # shift_distance = self.n * (diffusion_width + channel_length)

        # if self.connection == 1 or self.connection == 2:
        #     down_gate_connection.shapes(l_poly).insert(contact_gate_box_down)
        #     down_gate_connection.shapes(l_poly).insert(neck_box_down)

        #     y_sh = 0

        #     self.nmos_cell.shapes(l_met1_label).insert(
        #         gate_connection_text_down)
        #     p1_x = contact_gate_box_down.p1.x + free_spc_licon_gate / 2
        #     p1_y = contact_gate_box_down.p1.y + liconpoly_enc_vertical
        #     p2_x = contact_gate_box_down.p1.x + free_spc_licon_gate / 2 + licon_size
        #     p2_y = contact_gate_box_down.p1.y + liconpoly_enc_vertical + licon_size
        #     for licon_ct in range(num_horizontal_licon_gate):
        #         licon_box_down = pya.Box(p1_x, p1_y, p2_x, p2_y)

        #         down_gate_connection.shapes(l_licon).insert(licon_box_down)
        #         p1_y += 2 * licon_size
        #         p2_y += 2 * licon_size
        #         licon_box_down = pya.Box(p1_x, p1_y, p2_x, p2_y)
        #         down_gate_connection.shapes(l_licon).insert(licon_box_down)
        #         p1_y -= 2 * licon_size
        #         p2_y -= 2 * licon_size

        #         p1_x += 2 * licon_size
        #         p2_x += 2 * licon_size

        #     self.nmos_cell.shapes(l_li).insert(li_box_down)
        #     self.nmos_cell.shapes(l_met1).insert(li_box_down)
        #     down_gate_connection.shapes(l_npc).insert(npc_box_down)

        #     x_mcon_gates = li_box_down.p1.x + free_spc_mcon_gates_h / 2
        #     y_mcon_gates = li_box_down.p1.y + free_spc_mcon_gates_v / 2
        #     y1_mcon_gates = y_mcon_gates + mcon_size

        #     for mcon in range(num_hor_mcon_gates):
        #         x1_mcon_gates = x_mcon_gates + mcon_size
        #         mcon_box_gate = pya.Box(
        #             x_mcon_gates, y_mcon_gates, x1_mcon_gates, y1_mcon_gates)
        #         self.nmos_cell.shapes(l_mcon).insert(mcon_box_gate)
        #         for mcon1 in range(num_ver_mcon_gates - 1):
        #             y_mcon_gates += mcon_size + mcon_spc
        #             y1_mcon_gates += mcon_size + mcon_spc
        #             mcon_box_gate = pya.Box(
        #                 x_mcon_gates, y_mcon_gates, x1_mcon_gates, y1_mcon_gates)
        #             self.nmos_cell.shapes(l_mcon).insert(mcon_box_gate)
        #         y_mcon_gates -= (num_ver_mcon_gates - 1) * \
        #             mcon_size + (num_ver_mcon_gates - 1) * mcon_spc
        #         y1_mcon_gates -= (num_ver_mcon_gates - 1) * \
        #             mcon_size + (num_ver_mcon_gates - 1) * mcon_spc
        #         x_mcon_gates += mcon_size + mcon_spc
        #         x1_mcon_gates += mcon_size + mcon_spc

        # if self.connection == 0 or self.connection == 2:
        #     if self.connection == 0:
        #         shift_distance = 0
        #     up_gate_connection.shapes(l_poly).insert(contact_gate_box_up)
        #     up_gate_connection.shapes(l_poly).insert(neck_box_up)
        #     p1_x = contact_gate_box_up.p1.x + free_spc_licon_gate / 2
        #     p1_y = contact_gate_box_up.p1.y + liconpoly_enc_vertical
        #     p2_x = contact_gate_box_up.p1.x + free_spc_licon_gate / 2 + licon_size
        #     p2_y = contact_gate_box_up.p1.y + liconpoly_enc_vertical + licon_size
        #     li_box_up = pya.Box(diff_box.p1.x, contact_gate_box_up.p1.y,
        #                         diff_box.p1.x + multipliers * diffusion_total_width + (
        #                             2 * multipliers - 2) * npsdm_enc_diff + (
        #                             multipliers - 1) * npsdm_spc, contact_gate_box_up.p2.y)

        #     gate_connection_text_up = pya.Text(gate_connection_text_up, li_box_up.center().x,
        #                                        li_box_up.center().y)
        #     self.nmos_cell.shapes(l_met1_label).insert(gate_connection_text_up)

        #     self.nmos_cell.shapes(l_li).insert(li_box_up)
        #     self.nmos_cell.shapes(l_met1).insert(li_box_up)
        #     for licon_ct in range(num_horizontal_licon_gate):
        #         licon_box_up = pya.Box(p1_x, p1_y, p2_x, p2_y)

        #         up_gate_connection.shapes(l_licon).insert(licon_box_up)
        #         p1_y += 2 * licon_size
        #         p2_y += 2 * licon_size
        #         licon_box_up = pya.Box(p1_x, p1_y, p2_x, p2_y)
        #         up_gate_connection.shapes(l_licon).insert(licon_box_up)
        #         p1_y -= 2 * licon_size
        #         p2_y -= 2 * licon_size

        #         p1_x += 2 * licon_size
        #         p2_x += 2 * licon_size

        #     x_mcon_gates = li_box_up.p1.x + free_spc_mcon_gates_h / 2
        #     y_mcon_gates = li_box_up.p1.y + free_spc_mcon_gates_v / 2
        #     y1_mcon_gates = y_mcon_gates + mcon_size

        #     for mcon in range(num_hor_mcon_gates):
        #         x1_mcon_gates = x_mcon_gates + mcon_size
        #         mcon_box_gate = pya.Box(
        #             x_mcon_gates, y_mcon_gates, x1_mcon_gates, y1_mcon_gates)
        #         self.nmos_cell.shapes(l_mcon).insert(mcon_box_gate)
        #         for mcon1 in range(num_ver_mcon_gates - 1):
        #             y_mcon_gates += mcon_size + mcon_spc
        #             y1_mcon_gates += mcon_size + mcon_spc
        #             mcon_box_gate = pya.Box(
        #                 x_mcon_gates, y_mcon_gates, x1_mcon_gates, y1_mcon_gates)
        #             self.nmos_cell.shapes(l_mcon).insert(mcon_box_gate)
        #         y_mcon_gates -= (num_ver_mcon_gates - 1) * \
        #             mcon_size + (num_ver_mcon_gates - 1) * mcon_spc
        #         y1_mcon_gates -= (num_ver_mcon_gates - 1) * \
        #             mcon_size + (num_ver_mcon_gates - 1) * mcon_spc
        #         x_mcon_gates += mcon_size + mcon_spc
        #         x1_mcon_gates += mcon_size + mcon_spc
        #     up_gate_connection.shapes(l_npc).insert(npc_box_up)

        # self.mcon_between_fingers_cell.shapes(l_mcon).insert(self.mcon_between_fingers)

        # self.li_between_fingers_cell.shapes(l_li).insert(li_between_fingers_path)
        # self.li_between_fingers_cell.shapes(
        #     l_met1).insert(met1_between_fingers_path)

        # down_iteration = self.n
        # up_iteration = self.n
        # # distance to iterate down gate connection
        # down_iteration_distance = diffusion_width + channel_length
        # up_iteration_distance = down_iteration_distance
        # iteration_distance_group = 2 * self.n * \
        #     (diffusion_width + channel_length)
        # if self.connection == 1:  # for gate_connection_down_only
        #     down_iteration = self.nf
        #     up_iteration = 0
        #     down_iteration_distance = diffusion_width + channel_length
        #     iteration_distance_group = 0
        #     bottom_connection = pya.CellInstArray(down_gate_connection.cell_index(), pya.Trans(pya.Point(0, 0)),
        #                                           pya.Vector(
        #         down_iteration_distance, 0),
        #         pya.Vector(
        #         iteration_distance_group, 0), down_iteration,
        #         math.ceil(self.nf / (2 * self.n)))
        #     self.nmos_cell.insert(bottom_connection)

        # elif self.connection == 0:  # for gate_connection_up_only
        #     up_iteration = self.nf
        #     down_iteration = 0
        #     up_iteration_distance = diffusion_width + channel_length
        #     shift_distance = 0
        #     iteration_distance_group = 0

        #     repition_b = self.nf / self.n - math.ceil(self.nf / (2 * self.n))

        #     if self.nf == 1:
        #         repition_b = 1

        #     upper_connection = pya.CellInstArray(self.up_gate_connection.cell_index(), pya.Trans(pya.Point(shift_distance, 0)),
        #                                          pya.Vector(
        #         up_iteration_distance, 0),
        #         pya.Vector(iteration_distance_group, 0), up_iteration, repition_b)

        #     self.nmos_cell.insert(upper_connection)

        # else:
        #     bottom_connection = pya.CellInstArray(self.down_gate_connection.cell_index(), pya.Trans(pya.Point(0, 0)),
        #                                           pya.Vector(
        #         down_iteration_distance, 0),
        #         pya.Vector(
        #         iteration_distance_group, 0), down_iteration,
        #         math.ceil(self.nf / (2 * self.n)))
        #     self.nmos_cell.insert(bottom_connection)

        #     upper_connection = pya.CellInstArray(self.up_gate_connection.cell_index(), pya.Trans(pya.Point(shift_distance, 0)),
        #                                          pya.Vector(
        #         up_iteration_distance, 0),
        #         pya.Vector(
        #         iteration_distance_group, 0), up_iteration,
        #         self.nf / self.n - math.ceil(self.nf / (2 * self.n)))

        #     self.nmos_cell.insert(upper_connection)

        # self.nmos_cell.flatten(True)

        # multiple_transistors = pya.CellInstArray(nmos_cell.cell_index(), pya.Trans(pya.Point(0, 0)),
        #                                             pya.Vector(diffusion_total_width + 2 * npsdm_enc_diff + npsdm_spc, 0),
        #                                             pya.Vector(0, 0), multipliers, 1)

        # top_nmos_cell.insert(multiple_transistors)

        return self.nmos_cell
