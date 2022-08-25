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
## Mabrains poly resistor 1.8V Generator for Skywaters 130nm
########################################################################################################################
from typing import DefaultDict
from pandas.core import series
import pya
import math
from .layers_definiations import *
from .imported_generators.polyres import *



class PolyRes_gen(pya.PCellDeclarationHelper):
    """
    Mabrains poly resistor Generator for Skywaters 130nm
    """

    def __init__(self):
        # Initialize super class.
        super(PolyRes_gen, self).__init__()

        # declare the parameters
        self.param("Model", self.TypeString, "Model", default="sky130_fd_pr__res_xhigh_po",readonly=True)
        self.param("Sheet Resistance", self.TypeInt, "Sheet Resistance", default="2000",unit = "ohm/sq" ,readonly=True)
        self.R = self.param("Rtotal", self.TypeDouble, "Total Resistance", default="2", readonly=True,unit = "Kohm")
        self.width = self.param("w", self.TypeList, "Width",default=0.35)  # Width
        self.width.add_choice("0.35", 0.35)
        self.width.add_choice("0.69", 0.69)
        self.width.add_choice("1.41", 1.41)
        self.width.add_choice("2.85", 2.85)
        self.width.add_choice("5.73", 5.73)
        self.param("l", self.TypeDouble, "Length", default=1)  # Length
        self.param("rx", self.TypeInt, "Repeat X(odd number)", default=1)  # Repeat X"
        self.param("ry", self.TypeInt, "Repeat Y", default=1)  # Repeat Y

        self.param("gr", self.TypeBoolean, "Include Guard Ring", default=0)  # Include Guard Ring
        self.param("series", self.TypeBoolean, "Include series Connection", default=0)  # Include series connection

        # # constants
        # self.licon_enclosure = 0.08
        # self.licon_length = 2
        # self.res_spacing_x = 1.24
        # self.res_spacing_y = 0.52

        # self.gr_half_width = 0.255
        # self.psdm_spacing = 0.38
        # self.psdm_enclosure = 0.11
        # self. urpm_enclosure = 0.2
        # Below shows how to create hidden parameter is used to determine whether the radius has changed
        # or the "s" handle has been moved
        # self.param("ru", self.TypeDouble, "Radius", default = 0.0, hidden = True)
        # self.param("rd", self.TypeDouble, "Double radius", readonly = True)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "POLY_RES(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the
        # numeric parameter has changed (by comparing against the effective
        # radius ru) and set ru to the effective radius. We also update the
        # numerical value or the shape, depending on which on has not changed.
        # print(self.w)
        total_resistance = (self.l / self.w) *self.rx *self.ry* 2
        self.Rtotal = ('%.3f' % total_resistance)

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
        #Implement the "Create PCell from shape" protocol: we use the center of the shape's
        # bounding box to determine the transformation
        # return pya.Trans(self.shape.bbox().center())
        pass

    def produce_impl(self):
        # # precision value for scaling
        # PERCISION = 1/self.layout.dbu


        # # layers_definations
        # self.l_poly = self.layout.layer(poly_lay_num, poly_lay_dt)  # Poly
        # self.l_licon = self.layout.layer(licon_lay_num, licon_lay_dt)  # licon local interconnect
        # self.l_li = self.layout.layer(li_lay_num, li_lay_dt)
        # self.l_mcon = self.layout.layer(mcon_lay_num, mcon_lay_dt)
        # self.l_met1 = self.layout.layer(met1_lay_num, met1_lay_dt)
        # self.l_urpm = self.layout.layer(urpm_lay_num, urpm_lay_dt)
        # self.l_psdm = self.layout.layer(psdm_lay_num, psdm_lay_dt)  # psdm source drain impaln
        # self.l_tap = self.layout.layer(tap_lay_num, tap_lay_dt)
        # self.l_npc = self.layout.layer(npc_lay_num, npc_lay_dt)
        # self.l_poly_res = self.layout.layer(poly_res_lay_num, poly_res_lay_dt)

        # # inputs
        # # self.draw_one_finger(self.w, self.l, 0, 0, PERCISION)
        # # self.draw_metal1_between(0+self.w*PERCISION, 0, PERCISION)
        # lfx = 0
        # lfy = 0
        # lfx_res = lfx + (self.gr_half_width + self.psdm_spacing + self.psdm_enclosure) * PERCISION
        # lfy_res = lfy + (self.gr_half_width + self.psdm_spacing + self.psdm_enclosure) * PERCISION

        # gr_width = 2*self.gr_half_width + 2*self.psdm_spacing + 2*self.psdm_enclosure + \
        #            (self.rx - 1)*self.res_spacing_x + self.rx*self.w
        # gr_height = 2 * self.gr_half_width + 2 * self.psdm_spacing + 2 * self.psdm_enclosure + \
        #            (self.ry - 1) * self.res_spacing_y + self.ry*(4*self.licon_enclosure + 2*self.licon_length + self.l)
        # self.draw_matrix(lfx_res, lfy_res, PERCISION)

        # if self.rx ==1 and self.ry > 1 :
        #     urpm_enclosure = ((1.27 * PERCISION - self.w * PERCISION) / 2)
        #     urpm_lfx = lfx_res - urpm_enclosure
        #     urpm_urx = urpm_lfx + self.w*PERCISION + 2*urpm_enclosure
        #     urpm_lfy = lfy_res - self.urpm_enclosure * PERCISION
        #     urpm_ury = urpm_lfy + (gr_height+2*self.urpm_enclosure - (2 * self.gr_half_width + 2 * self.psdm_spacing + 2 * self.psdm_enclosure)) * PERCISION
        #     self.cell.shapes(self.l_urpm).insert(pya.Box(urpm_lfx, urpm_lfy, urpm_urx, urpm_ury))

        # else:
        #     urpm_lfx = lfx_res - self.urpm_enclosure*PERCISION
        #     urpm_urx = lfx_res + ((self.rx - 1)*self.res_spacing_x + self.rx*self.w + self.urpm_enclosure)*PERCISION
        #     urpm_lfy = lfy_res - self.urpm_enclosure * PERCISION
        #     urpm_ury = urpm_lfy + (gr_height + 2 * self.urpm_enclosure - (
        #                 2 * self.gr_half_width + 2 * self.psdm_spacing + 2 * self.psdm_enclosure)) * PERCISION
        #     self.cell.shapes(self.l_urpm).insert(pya.Box(urpm_lfx, urpm_lfy, urpm_urx, urpm_ury))

        # if self.gr:
        #     self.draw_guard_ring(lfx, lfy, gr_width, gr_height, PERCISION)


        self.percision = 1/self.layout.dbu
        poly_instance = PolyRes(layout=self.layout,w=self.w,
                                l=self.l,rx = self.rx , 
                                ry = self.ry,gr=self.gr,series=self.series,connection_labels = 0)
        polyres_cell = poly_instance.draw_polyres()
        write_cells = pya.CellInstArray(polyres_cell.cell_index(), pya.Trans(pya.Point(0, 0)),
                              pya.Vector(0, 0), pya.Vector(0, 0),1 , 1)
        
        
        self.cell.insert(write_cells)
        self.cell.flatten(1)
        self.layout.cleanup()

    