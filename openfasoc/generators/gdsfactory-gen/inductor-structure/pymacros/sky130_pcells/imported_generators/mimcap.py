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
from .layers_definiations import *
import pya


class mimcap():
    mimcap_drawing_offest = 0.5
    metal3_margin_right = 0.995
    mimcap_enc_metal4 = 0.195
    met4_side_overlap = 0.005
    met4_side_width = 0.48

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

    def __init__(self, layout, w, l, pin0='p0', pin1='n0',connection_labels=1):
        self.layout = layout
        self.l_capm = self.layout.layer(capm_lay_num, capm_lay_dt)
        self.l_met3 = self.layout.layer(met3_lay_num, met3_lay_dt)
        self.l_met4 = self.layout.layer(met4_lay_num, met4_lay_dt)
        self.l_met4_label = self.layout.layer(
            met4_label_lay_num, met4_label_lay_dt)
        self.l_via3 = self.layout.layer(via3_lay_num, via3_lay_dt)
        self.l_prbndry = self.layout.layer(prbndry_lay_num, prbndry_lay_dt)
        self.percision = 1/self.layout.dbu
        self.cell = self.layout.create_cell(
            "sky130_fd_pr__cap_mim_m3_1_w"+str(w)+"_l"+str(l))
        self.w = w * self.percision
        self.l = l * self .percision
        self.pin0 = pin0
        self.pin1 = pin1
        self.connection_labels=connection_labels

    def draw_vias(self, box, via3_cell):
        via3_size = 0.2*self.percision
        met_via3_enc_1 = 0.065*self.percision
        met_via3_enc_2 = 0.09*self.percision
        via3_spc = 0.2*self.percision
        AL_via3 = pya.Box(0, 0, via3_size, via3_size)
        # via3_cell = self.layout.create_cell("via3")
        via3_cell.shapes(self.l_via3).insert(AL_via3)
        num_via3_1, via3_free_spc_1 = self.number_spc_contacts(
            box.width(), met_via3_enc_1, via3_spc, via3_size)
        num_via3_2, via3_free_spc_2 = self.number_spc_contacts(
            box.height(), met_via3_enc_2, via3_spc, via3_size)
        via3_arr = pya.CellInstArray(via3_cell.cell_index(), pya.Trans(
            pya.Point(box.p1.x+via3_free_spc_1 / 2, box.p1.y + via3_free_spc_2 / 2)),
            pya.Vector(via3_spc + via3_size, 0),
            pya.Vector(0, via3_spc + via3_size),
            num_via3_1, num_via3_2)

        return via3_arr

    def draw_cap(self):

        mimcap_box = pya.Box(mimcap.mimcap_drawing_offest*self.percision,
                             mimcap.mimcap_drawing_offest*self.percision,
                             mimcap.mimcap_drawing_offest*self.percision+self.w,
                             mimcap.mimcap_drawing_offest*self.percision+self.l)

        self.cell.shapes(self.l_capm).insert(mimcap_box)
        self.met4_center_box = mimcap_box.enlarge(-1*mimcap.mimcap_enc_metal4*self.percision,

                                                  -1*mimcap.mimcap_enc_metal4*self.percision)
        self.cell.shapes(self.l_met4).insert(self.met4_center_box)
        met3_box = pya.Box(0, 0,
                           mimcap.mimcap_drawing_offest*self.percision +
                           self.w+mimcap.metal3_margin_right*self.percision,
                           2*mimcap.mimcap_drawing_offest*self.percision+self.l)

        self.cell.shapes(self.l_met3).insert(met3_box)
        pin0_text = pya.Text(self.pin0, self.met4_center_box.center().x,
                             self.met4_center_box.center().y)
        prbndry_box = pya.Box(0, 0,
                              2*mimcap.mimcap_drawing_offest*self.percision+self.w,
                              2*mimcap.mimcap_drawing_offest*self.percision+self.l)

        self.cell.shapes(self.l_prbndry).insert(prbndry_box)

        self.met4_side_box = pya.Box(prbndry_box.p2.x-mimcap.met4_side_overlap*self.percision,
                                     prbndry_box.p1.y + 0.06*self.percision,
                                     prbndry_box.p2.x-mimcap.met4_side_overlap *
                                     self.percision+mimcap.met4_side_width*self.percision,
                                     prbndry_box.p2.y - 0.06*self.percision)
        pin1_text = pya.Text(self.pin1, self.met4_side_box.center().x,
                             self.met4_side_box.center().y)
        if self.connection_labels:
            self.cell.shapes(self.l_met4_label).insert(pin0_text)
            self.cell.shapes(self.l_met4_label).insert(pin1_text)

        self.cell.shapes(self.l_met4).insert(self.met4_side_box)

        # print('--->', self.layout.cell("via3"))
        if self.layout.cell("via3") == None:
            via3_cell = self.layout.create_cell("via3")
            # print('--->', self.layout.cell("via3"))
        else:
            via3_cell = self.layout.cell("via3")

        via3_arr = self.draw_vias(self.met4_center_box, via3_cell)

        self.cell.insert(via3_arr)

        via3_arr = self.draw_vias(self.met4_side_box, via3_cell)
        self.cell.insert(via3_arr)
        # For correct drc on magic 
        self.cell.flatten(1)
        return self.cell
