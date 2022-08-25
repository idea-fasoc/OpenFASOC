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
from .imported_generators.mimcap_m4 import *



class mimcap_2_gen(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the mimcap_1
    """

    def __init__(self):

        # Important: initialize the super class
        super(mimcap_2_gen, self).__init__()

        # declare the parameters
        self.param("l", self.TypeDouble, "Length", default=1,unit="um")
        self.param("w", self.TypeDouble, "Width", default=1,unit="um")
        self.param("array_x", self.TypeInt, "elements in x_direction", default=1)
        self.param("array_y", self.TypeInt, "elements in y_direction", default=1)
        self.param("x_spacing", self.TypeDouble, "spacing in x_direction", default=1,unit="um")
        self.param("y_spacing", self.TypeDouble, "spacing in y_direction", default=1,unit="um")
        self.param("totalcap", self.TypeDouble, "Total Capcitance",unit="fF",readonly=True)
        
        


    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "sky130_fd_pr__cap_mim_m3_1_w"+str(self.w)+"_l"+str(self.l)

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
        self.totalcap = self.w * self.l * self.array_x * self.array_y * 2

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
        pass

    def produce_impl(self):
       
        self.percision = 1/self.layout.dbu
        mimcap_instance = mimcap_m4(layout=self.layout,w=self.w,l=self.l,connection_labels=0)
        mimcap_cell = mimcap_instance.draw_cap()
        write_cells = pya.CellInstArray(mimcap_cell.cell_index(), pya.Trans(pya.Point(0, 0)),
                              pya.Vector(self.x_spacing*self.percision, 0), pya.Vector(0, self.y_spacing*self.percision),self.array_x , self.array_y)
        
        self.cell.flatten(1)
        self.cell.insert(write_cells)
