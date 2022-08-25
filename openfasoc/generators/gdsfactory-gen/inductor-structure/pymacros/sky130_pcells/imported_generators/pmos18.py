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
#########################################################################################################################
# Copyright (C) 2018-2021 Mabrains Company LLC <contact@mabrains.com>
##
# This file is authored by:
#           - <Mina Maksimous> <mina_maksimous@mabrains.com>
##
########################################################################################################################

########################################################################################################################
# Mabrains Company LLC
##
# Mabrains PMOS 1.8V Generator for Skywaters 130nm
########################################################################################################################

from .nmos18 import *


class pmos18_device(nmos18_device):
    

    def __init__(self, w=0.42, l=0, nf=1, gr=1,
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
                 connection_labels=1,
                 connected_gates=1,
                 layout=None):
        super().__init__(w=w, l=l, nf=nf, gr=gr, dsa=dsa, connection=connection, 
                        n=n, x_offest=x_offest, y_offest=y_offest, conn_num=conn_num, 
                        gate_connection=gate_connection,
                        gate_connection_up=gate_connection_up, gate_connection_down=gate_connection_down, drain_connection=drain_connection, 
                        source_connection=source_connection, layout=layout,connection_labels=connection_labels,connected_gates=connected_gates)

        self.layout = layout
        self.percision = 1/self.layout.dbu
        self.l_diff_implant = self.layout.layer(psdm_lay_num, psdm_lay_dt)
        self.l_guard = self.layout.layer(
            nsdm_lay_num, nsdm_lay_dt)  # guard ring implant layer
        self.cell_str = "pmos18_w" + str(self.w).replace(".", "p") + "u_l" + str(self.l).replace(".", "p") + "u_nf" + str(
            self.nf) + "_drain_area" + str(self.dsa) + "_gate_connection" + str(self.connection) + "alt" + str(self.n)
        self.l_nwell = self.layout.layer(nwell_lay_num, nwell_lay_dt)
        self.nwell_extension = 0.18 * self.percision
    # def draw_guard_ring(self, layout, x, y, guard_width, guard_height, precision, tap_width=0.26, cell=None, type='n'):
    #     return super().draw_guard_ring(layout, x, y, guard_width, guard_height, precision, tap_width=tap_width, cell=cell, type=type)

    def draw_nmos(self):
        self.pmos_cell = super().draw_nmos()
        self.pmos_cell.shapes(self.l_nwell).insert(
            self.pmos_cell.bbox().enlarge(self.nwell_extension, self.nwell_extension))
        return self.pmos_cell
