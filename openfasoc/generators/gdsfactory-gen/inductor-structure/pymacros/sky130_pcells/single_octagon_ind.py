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
## Mabrains Inductor Generator for Skywaters 130nm
########################################################################################################################
from .layers_definiations import *
import pya
import math
import pandas as pd


"""
Mabrains Via Generator for Skywaters 130nm
"""



class single_octagon_ind_Generator(pya.PCellDeclarationHelper):
    """
    Mabrains Via Generator for Skywaters 130nm
    """


    def __init__(self):
        ## Initialize super class.
        super(single_octagon_ind_Generator, self).__init__()

        # declare the parameters
        self.param("N", self.TypeInt, "number of turns", default=3)
        self.param("W", self.TypeDouble, "Width of the conductors", default=2)
        self.param("S", self.TypeDouble, "Spacing between conductors", default=4)
        self.param("Louter", self.TypeDouble, "outer dimension", default=40)
        #self.param("distance_input", self.TypeDouble, "Input distance", default=40)




        #self.param("via", self.TypeLayer, "via_layer", default = pya.LayerInfo(via_lay_num,via_lay_dt), hidden = True)

        # Below shows how to create hidden parameter is used to determine whether the radius has changed
        # or the "s" handle has been moved
        ## self.param("ru", self.TypeDouble, "Radius", default = 0.0, hidden = True)
        ## self.param("rd", self.TypeDouble, "Double radius", readonly = True)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "( single_octagon" + str(self.N) + " width = "+str(self.W) +")"

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
        #self.w = self.shape.bbox().width() * self.layout.dbu
        #self.l = self.shape.bbox().length() * self.layout.dbu
        self.ls = self.layout.get_info(self.layer)

    def transformation_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we use the center of the shape's
        # bounding box to determine the transformation
        return pya.Trans(self.shape.bbox().p1())

    def produce_impl(self):
        PERCISION = 1000

        # create the shape

        met1 = self.layout.layer(met1_lay_num, met1_lay_dt)

        met2 = self.layout.layer(met2_lay_num, met2_lay_dt)

        met3 = self.layout.layer(met3_lay_num, met3_lay_dt)

        met4 = self.layout.layer(met4_lay_num, met4_lay_dt)

        met5 = self.layout.layer(met5_lay_num, met5_lay_dt)

        via = self.layout.layer(via_lay_num, via_lay_dt)

        via2 = self.layout.layer(via2_lay_num, via2_lay_dt)

        via3 = self.layout.layer(via3_lay_num, via3_lay_dt)

        via4 = self.layout.layer(via4_lay_num, via4_lay_dt)

        N = self.N  # number of turns
        W = self.W* PERCISION  # width of the conductors
        S = self.S * PERCISION  # spacing between the conductors
        Louter = self.Louter * PERCISION  # outer dimension
        angle = math.pi / 4  # outer angle of the side is 60 degrees (written here in radian)
        X_angle = math.cos(angle)
        Y_angle = math.sin(angle)
        Z_angle = math.tan(math.pi * 3 / 8)
        Side_length = Louter / (1 + 2 * X_angle)
        NumOfPoints = int((8 * N) + 1)
        NumOfSides = 8  # number of sides of the polygon

        all_points = []
        xcor = 0
        ycor = W / 2
        xpos = 1  # to change the horizontal sides
        hor_side = 0
        ypos = 1  # to change the vertical sides
        ver_side = 0
        check1 = 0
        check2 = 0
        LouterCor = Louter
        Side_lengthCor = Side_length
        diagonal = 1
        # editing
        # trying to solve the problem
        for i in range(N):

            for j in range(NumOfSides):
                if j == 0:
                    xcor = xcor
                    ycor = ycor
                elif j == (4 * hor_side + 1):  # if number of conductor 1 (increase )and 4(decrease) in xaxis only
                    if xpos == 1:
                        xcor = xcor + Side_lengthCor
                        xpos = 0
                        hor_side = 1
                    else:
                        xcor = xcor - Side_lengthCor
                        xpos = 1
                        hor_side = 0
                elif j == (4 * ver_side + 3):  # if number of conductor 3 (increase )and 7 (decrease) in yaxis only
                    if ypos == 1:
                        ycor = ycor + Side_lengthCor
                        ypos = 0
                        ver_side = 1
                    else:
                        ycor = ycor - Side_lengthCor + W + S
                        ypos = 1
                        ver_side = 0
                else:  # drawing the side with angle change in xaxis and yaxis
                    if diagonal == 1:
                        xcor = xcor + Side_lengthCor * X_angle
                        ycor = ycor + Side_lengthCor * Y_angle
                        if check1 == 1:
                            xcor = xcor - 2 * Side_lengthCor * X_angle
                        check1 = check1 + 1
                        if check1 == 2:
                            diagonal = 0
                            check1 = 0
                    else:
                        xcor = xcor - Side_lengthCor * X_angle
                        ycor = ycor - Side_lengthCor * Y_angle
                        diagonal = 1
                PointCoordinates = pya.Point(xcor, ycor)
                all_points.append(PointCoordinates)
            xcor = (i + 1) * (W + S) / Z_angle
            ycor = (i + 1) * (W + S) + W / 2
            Side_lengthCor = Side_lengthCor - 2 * (W + S) / Z_angle
            PointCoordinates = pya.Point(xcor, ycor)
            all_points.append(PointCoordinates)
            if i == N - 1:
                xcor = xcor + Side_lengthCor / 2
                PointCoordinates = pya.Point(xcor, ycor)
                all_points.append(PointCoordinates)
                self.cell.shapes(via4).insert(pya.Box(xcor - Side_lengthCor / 4, ycor - W / 2, xcor, ycor + W / 2))
                self.cell.shapes(met4).insert(
                    pya.Box(xcor - Side_lengthCor / 4, ycor - W / 2, xcor + Side_length + Side_length * X_angle,
                            ycor + W / 2))

        self.cell.shapes(met5).insert(pya.Path(all_points, W))


