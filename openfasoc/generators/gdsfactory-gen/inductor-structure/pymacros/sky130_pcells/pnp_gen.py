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

import pya
import math
from .imported_generators.pnp import *

"""
This sample PCell implements a library called "MyLib" with a single PCell that
draws a circle. It demonstrates the basic implementation techniques for a PCell 
and how to use the "guiding shape" feature to implement a handle for the circle
radius.

NOTE: after changing the code, the macro needs to be rerun to install the new
implementation. The macro is also set to "auto run" to install the PCell 
when KLayout is run.
"""


class pnp_bjt(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the circle
    """

    def __init__(self):

        # Important: initialize the super class
        super(pnp_bjt, self).__init__()
        self.Type_handle = self.param("Type", self.TypeList, "Type")
        self.Type_handle.add_choice("pnp_w3p4_l3p4", "pnp_w3p4_l3p4")
        self.Type_handle.add_choice("pnp_w0p68_l0p68", "pnp_w0p68_l0p68")
        self.param("Model", self.TypeString, "Model", default="sky130_fd_pr__pnp_05v5",readonly=True)
        self.param("array_x", self.TypeInt, "Elements in x_direction", default=1)
        self.param("array_y", self.TypeInt, "Elements in y_direction", default=1)
        self.param("x_spacing", self.TypeDouble, "Spacing in x_direction", default=1,unit="um")
        self.param("y_spacing", self.TypeDouble, "Spacing in y_direction", default=1,unit="um")
        

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return str(self.Type)

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

        # n must be larger or equal than 4
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
        # return pya.Trans(self.shape.bbox().center())
        pass
    def produce_impl(self):

        # This is the main part of the implementation: create the layout

        # fetch the parameters
        # ru_dbu = self.ru / self.layout.dbu

        # # compute the circle
        # pts = []
        # da = math.pi * 2 / self.n
        # for i in range(0, self.n):
        #     pts.append(pya.Point.from_dpoint(pya.DPoint(ru_dbu * math.cos(i * da), ru_dbu * math.sin(i * da))))

        # # create the shape
        # self.cell.shapes(self.l_layer).insert(pya.Polygon(pts))


        self.percision = 1/self.layout.dbu
        pnp_instance = pnp(layout=self.layout,device_name=self.Type)
        pnp_cell = pnp_instance.draw_pnp()
        write_cells = pya.CellInstArray(pnp_cell.cell_index(), pya.Trans(pya.Point(0, 0)),
                              pya.Vector(self.x_spacing*self.percision, 0), pya.Vector(0, self.y_spacing*self.percision),self.array_x , self.array_y)
        
        self.cell.flatten(1)
        self.cell.insert(write_cells)
        self.layout.cleanup()
