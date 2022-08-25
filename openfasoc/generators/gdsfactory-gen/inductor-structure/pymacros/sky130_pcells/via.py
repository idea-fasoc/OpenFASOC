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
## Mabrains Via Generator for Skywaters 130nm
########################################################################################################################
from .layers_definiations import *
import pya
import math
import pandas as pd


"""
Mabrains Via Generator for Skywaters 130nm
"""



class ViaGenerator(pya.PCellDeclarationHelper):
    """
    Mabrains Via Generator for Skywaters 130nm
    """
    layers = ["metal1","metal2","metal3","metal4","metal5"]


    def __init__(self):

        ## Initialize super class.
        super(ViaGenerator, self).__init__()
        # declare the parameters
        #self.param("ls", self.TypeLayer, "Starting Layer", default=pya.LayerInfo(1, 0))
        #self.param("le", self.TypeLayer, "Ending Layer", default=pya.LayerInfo(1, 0))

        self.param("metal", self.TypeString, "Choose metal type AL or CU", default="AL")
        ending_layer = self.param("ending_metal",self.TypeString,"choose the ending material",default = "metal1")
        ending_layer.add_choice("metal1", "l_met1")
        ending_layer.add_choice("metal2", "l_met2")
        ending_layer.add_choice("metal3", "l_met3")
        ending_layer.add_choice("metal4", "l_met4")
        ending_layer.add_choice("metal5", "l_met5")
        self.param("width", self.TypeDouble, "width", hidden = True)
        self.param("height", self.TypeDouble, "height", hidden = True)

        self.param("metal", self.TypeString, "Choose metal type AL or CU", default="AL")
        self.param("via_type", self.TypeString, "Choose via type", default="via")

        #self.param("via", self.TypeLayer, "via_layer", default = pya.LayerInfo(via_lay_num,via_lay_dt), hidden = True)

        # Below shows how to create hidden parameter is used to determine whether the radius has changed
        # or the "s" handle has been moved
        ## self.param("ru", self.TypeDouble, "Radius", default = 0.0, hidden = True)
        ## self.param("rd", self.TypeDouble, "Double radius", readonly = True)

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
            free_spc = box_width - (num_cont * cont_width + (num_cont - 1) * cont_spc)
            return num_cont, free_spc
    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "(" + self.via_type + " metal = "+self.metal +")"

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

    def parameters_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we set r and l from the shape's
        # bounding box width and layer
        self.width =  self.shape.bbox().width()
        self.height = self.shape.bbox().height()
        #global layer_number = self.layout.get_info(self.layer).layer

    def transformation_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we use the center of the shape's
        # bounding box to determine the transformation
        return pya.Trans(self.shape.bbox().p1)

    def produce_impl(self):
        ru_dbu = 1000

        # compute the circle
        #pts = []
        #da = math.pi * 2 / 4
        #for i in range(0, 4):
        #pts.append(pya.Point.from_dpoint(pya.DPoint(ru_dbu * math.cos(i * da), ru_dbu * math.sin(i * da))))
        l_met1 = self.layout.layer(met1_lay_num, met1_lay_dt)
        l_met2 = self.layout.layer(met2_lay_num, met2_lay_dt)
        l_met3 = self.layout.layer(met3_lay_num, met3_lay_dt)
        l_met4 = self.layout.layer(met4_lay_num, met4_lay_dt)
        l_met5 = self.layout.layer(met5_lay_num, met5_lay_dt)
        self.cell.shapes(l_met1).insert(pya.Box(0,0,self.width,self.height))
        # create the shape
        l_via = self.layout.layer(via_lay_num, via_lay_dt)
        l_via2 = self.layout.layer(via2_lay_num, via2_lay_dt)
        l_via3 = self.layout.layer(via3_lay_num, via3_lay_dt)
        l_via4 = self.layout.layer(via4_lay_num, via4_lay_dt)


        AL_via = pya.Box(0,0,0.15*ru_dbu,0.15*ru_dbu)
        AL_via2 = pya.Box(0,0,0.2*ru_dbu,0.2*ru_dbu)
        AL_via3 = pya.Box(0,0,0.2*ru_dbu,0.2*ru_dbu)
        AL_via4 = pya.Box(0,0,0.8*ru_dbu,0.8*ru_dbu)

        print(self.ending_metal)
        CU_via = pya.Box(0,0,0.18*ru_dbu,0.18*ru_dbu)
        if self.metal == "CU":
            self.cell.shapes(l_via).insert(CU_via)
        else:
            if self.via_type == "via":
                self.cell.shapes(l_via).insert(AL_via)
            elif self.via_type == "via2":
                self.cell.shapes(l_via2).insert(AL_via2)
            elif self.via_type == "via3":
                self.cell.shapes(l_via3).insert(AL_via3)
            else :
                self.cell.shapes(l_via4).insert(AL_via4)
