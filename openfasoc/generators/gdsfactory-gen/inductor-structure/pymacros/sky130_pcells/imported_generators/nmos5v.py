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
# Mabrains NMOS 5v Generator for Skywaters 130nm
########################################################################################################################
from .layers_definiations import *
from .nmos18 import *
import pya
import math
import os
import sys


class nmos5(nmos18_device):
    diff_hvntm_enc = 0.185
    hvi_extension = 0.06

    def __init__(self, w=0.5, l=0.5, nf=1, gr=1,
                 dsa=1,
                 connection=0,
                 n=1,
                 x_offest=0,
                 y_offest=0,
                 connection_labels=1,
                 conn_num="0",
                 gate_connection="gate_connection_",
                 gate_connection_up="gate_connection_up_",
                 gate_connection_down="gate_connection_down_",
                 drain_connection="drain_connection_",
                 source_connection="source_connection_",
                 connected_gates = 1,
                 layout=None):
        super().__init__(w=w, l=l, nf=nf, gr=gr, dsa=dsa, connection=connection, 
                        n=n, x_offest=x_offest, y_offest=y_offest, conn_num=conn_num, gate_connection=gate_connection,
                         gate_connection_up=gate_connection_up, gate_connection_down=gate_connection_down, drain_connection=drain_connection, 
                         source_connection=source_connection, layout=layout,connection_labels=connection_labels,connected_gates=connected_gates)
        self.l_hvntm = self.layout.layer(hvntm_lay_num, hvntm_lay_dt)
        self.l_hvi = self.layout.layer(hvi_lay_num, hvi_lay_dt)
        self.cell_str = "nmos5_w" + str(self.w).replace(".", "p") + "u_l" + str(self.l).replace(".", "p") + "u_nf" + str(
            self.nf) + "_drain_area" + str(self.dsa) + "_gate_connection" + str(self.connection) + "alt" + str(self.n)
        self.percision = 1/self.layout.dbu

    def draw_guard_ring(self, layout, x, y, guard_width, guard_height, precision, cell, tap_width=0.29):
        return super().draw_guard_ring(layout, x, y, guard_width, guard_height, precision, tap_width=tap_width, cell=cell)

    def draw_nmos5(self):
        self.nmos_cell = super().draw_nmos()
        self.nmos_cell.shapes(self.l_hvntm).insert(
            self.diff_box.enlarge(nmos5.diff_hvntm_enc*1000, nmos5.diff_hvntm_enc*1000))
        self.nmos_cell.shapes(self.l_hvi).insert(self.nmos_cell.bbox().enlarge(
            nmos5.hvi_extension*1000, nmos5.hvi_extension*1000))

        return self.nmos_cell


# layout_obj = pya.Layout()
# nmos_5_instance = nmos5(layout=layout_obj)
# cell_name = nmos_5_instance.draw_nmos5()
# top_cell = top_cell = layout_obj.create_cell("TOP")

# write_cells = pya.CellInstArray(cell_name.cell_index(), pya.Trans(pya.Point(3000, 0)),
#                                 pya.Vector(0, 0), pya.Vector(0, 0), 1, 1)

# top_cell.insert(write_cells)

# layout_obj.write("nmos_5v.gds")
