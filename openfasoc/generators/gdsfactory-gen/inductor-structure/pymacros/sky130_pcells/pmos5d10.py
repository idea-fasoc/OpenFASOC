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

import pya
import math
from .imported_generators.pmos5v import *

"""
This sample PCell implements a library called "MyLib" with a single PCell that
draws a nmos5d10_gen. It demonstrates the basic implementation techniques for a PCell 
and how to use the "guiding shape" feature to implement a handle for the nmos5d10_gen
radius.

NOTE: after changing the code, the macro needs to be rerun to install the new
implementation. The macro is also set to "auto run" to install the PCell 
when KLayout is run.
"""


class pmos5d10_gen(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the nmos5d10_gen
    """

    def __init__(self):

        # Important: initialize the super class
        # pya.PCellDeclarationHelper.__init__(self)
        super(pmos5d10_gen, self).__init__()

        # declare the parameters
        self.param("w", self.TypeDouble, "Width", default=0.42)
        self.param("l", self.TypeDouble, "Length", default=0.15)
        self.param("nf", self.TypeInt, "Number of Fingers", default=1)
        self.param("gr", self.TypeBoolean, "guard ring", default=1)
        self.param("dsa", self.TypeInt,
                   "drain and source number of contacts", default=1)
        self.param("connection", self.TypeInt, "Connection Option", default=0)
        self.param("n", self.TypeInt,
                   "Alternate Factor(for Alternate Connection)", default=1)
        # connection_option.add_choice("Connection Up",0)
        # connection_option.add_choice("Connection Down",1)
        # connection_option.add_choice("Alternate connection",2)
        self.param("connected_gates", self.TypeBoolean,
                   "Connected Gates", default=1)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        cell_str = "pmos5_w" + str(self.w).replace(".", "p") + "u_l" + str(self.l).replace(".", "p") + "u_nf" + str(
            self.nf) + "_drain_area" + str(self.dsa) + "_gate_connection" + str(self.connection) + "alt" + str(self.n)
        return cell_str

    def coerce_parameters_impl(self):

        # We employ coerce_parameters_impl to decide whether the handle or the
        # numeric parameter has changed (by comparing against the effective
        # radius ru) and set ru to the effective radius. We also update the
        # numerical value or the shape, depending on which on has not changed.
        # rs = None
        # if isinstance(self.s, pya.DPoint):
        #     # compute distance in micron
        #     rs = self.s.distance(pya.DPoint(0, 0))
        # if rs != None and abs(self.r - self.ru) < 1e-6:
        #     self.ru = rs
        #     self.r = rs
        # else:
        #     self.ru = self.r
        #     self.s = pya.DPoint(-self.r, 0)

        # self.rd = 2 * self.r

        # # n must be larger or equal than 4
        # if self.n <= 4:
        #     self.n = 4
        pass

    def can_create_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we can use any shape which
        # has a finite bounding box
        # return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()
        pass

    def parameters_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we set r and l from the shape's
        # bounding box width and layer
        # self.r = self.shape.bbox().width() * self.layout.dbu / 2
        # self.l = self.layout.get_info(self.layer)
        pass

    def transformation_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we use the center of the shape's
        # bounding box to determine the transformation
        return pya.Trans(self.shape.bbox().center())

    def produce_impl(self):
        # This is the main part of the implementation: create the layout
        pmos5_instance = pmos5(w=self.w, l=self.l, nf=self.nf, connection=self.connection,
                               layout=self.layout, gr=self.gr, connection_labels=0, connected_gates=self.connected_gates,dsa=self.dsa)
        pmos_cell = pmos5_instance.draw_pmos5()

        write_cells = pya.CellInstArray(pmos_cell.cell_index(), pya.Trans(pya.Point(0, 0)),
                                        pya.Vector(0, 0), pya.Vector(0, 0), 1, 1)
        
        self.cell.insert(write_cells)
        self.cell.flatten(1)
