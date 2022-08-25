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
## Mabrains rectangualr_shielding Generator for Skywaters 130nm
########################################################################################################################
from .layers_definiations import *
import pya
import math
import pandas as pd

"""
Mabrains Via Generator for Skywaters 130nm
"""


class triangular_shielding_Generator(pya.PCellDeclarationHelper):
    """
    Mabrains Via Generator for Skywaters 130nm
    """

    def __init__(self):
        ## Initialize super class.
        super(triangular_shielding_Generator, self).__init__()

        # declare the parameters
        self.param("W", self.TypeDouble, "Width of the conductors", default=2)
        self.param("S", self.TypeDouble, "Spacing between conductors", default=4)
        self.param("Louter", self.TypeDouble, "outer dimension", default=40)

        # self.param("via", self.TypeLayer, "via_layer", default = pya.LayerInfo(via_lay_num,via_lay_dt), hidden = True)

        # Below shows how to create hidden parameter is used to determine whether the radius has changed
        # or the "s" handle has been moved
        ## self.param("ru", self.TypeDouble, "Radius", default = 0.0, hidden = True)
        ## self.param("rd", self.TypeDouble, "Double radius", readonly = True)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "( triangular_shielding spacing" + str(self.S) + " width = " + str(self.W) + ")"

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
        # self.w = self.shape.bbox().width() * self.layout.dbu
        # self.l = self.shape.bbox().length() * self.layout.dbu
        self.ls = self.layout.get_info(self.layer)

    def transformation_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we use the center of the shape's
        # bounding box to determine the transformation
        return pya.Trans(self.shape.bbox().p1())

    def produce_impl(self):

        PERCISION = 1000

        met1 = self.layout.layer(met1_lay_num, met1_lay_dt)
        met2 = self.layout.layer(met2_lay_num, met2_lay_dt)
        met3 = self.layout.layer(met3_lay_num, met3_lay_dt)
        met4 = self.layout.layer(met4_lay_num, met4_lay_dt)
        met5 = self.layout.layer(met5_lay_num, met5_lay_dt)

        via = self.layout.layer(via_lay_num, via_lay_dt)
        via2 = self.layout.layer(via2_lay_num, via2_lay_dt)
        via3 = self.layout.layer(via3_lay_num, via3_lay_dt)
        via4 = self.layout.layer(via4_lay_num, via4_lay_dt)

        diff = self.layout.layer(diff_lay_num, diff_lay_dt)
        psdm = self.layout.layer(psdm_lay_num, psdm_lay_dt)
        licon1 = self.layout.layer(licon_lay_num, licon_lay_dt)
        li1 = self.layout.layer(li_lay_num, li_lay_dt)
        mcon = self.layout.layer(mcon_lay_num, mcon_lay_dt)
        nwell = self.layout.layer(nwell_lay_num, nwell_lay_dt)
        nsdm = self.layout.layer(nsdm_lay_num, nsdm_lay_dt)

        W = self.W * PERCISION  # width of the conductors
        S = self.S * PERCISION  # minimum spacing between the conductors is 1.27*PERCISION due to the N_well
        S_min = 1.27 * PERCISION
        Lver = self.Louter * PERCISION  # Lver==Lhor because it's assumed that the overall shape is square
        Lhor = self.Louter * PERCISION
        N_Conductors = int((Lhor + S) / (S + W))  # number of conductors
        xcor = 0
        ycor = 0
        xcor2 = 0
        ycor2 = 0
        y_check = 0
        x_check = 0
        Shielding_with_diffusion = 1
        all_hole_points = []
        print(N_Conductors)
        Diffusion_Width = 0.15 * PERCISION
        Diffusion_Spacing = 0.27 * PERCISION
        Diffusion_Encloses_Licon = 0.06 * PERCISION

        Nwell_width = 0.84 * PERCISION
        Nwell_Spacing = 1.27 * PERCISION

        nsdm_Width = 0.38 * PERCISION
        nsdm_Spacing = 0.38 * PERCISION
        nsdm_Encloses_Diffusion = 0.125 * PERCISION
        nsdm_Area_min = 0.265 * PERCISION * PERCISION

        Met1_Width = 0.14 * PERCISION
        Met1_Spacing = 0.14 * PERCISION
        Met1_Encloses_Mcon = 0.03 * PERCISION
        Met1_Encloses_Mcon_Two_Sides = 0.06 * PERCISION
        Met1_Area_min = 0.083 * PERCISION * PERCISION

        Psdm_Width = 0.38 * PERCISION
        Psdm_Spacing = 0.38 * PERCISION
        Psdm_Encloses_Diffusion = 0.125 * PERCISION
        Psdm_Area_min = 0.255 * PERCISION * PERCISION

        Licon_Width_Length = 0.17 * PERCISION
        Licon_Spacing = 0.17 * PERCISION

        Li_Width = 0.17 * PERCISION
        Li_Spacing = 0.17 * PERCISION
        Li_Area_min = 0.0561 * PERCISION * PERCISION
        Li_Encloses_Licon_Two_Sides = 0.08 * PERCISION

        Mcon_Width_Length = 0.17 * PERCISION
        Mcon_Spacing = 0.19 * PERCISION

        # find the number of licon needed for the horizontal distance
        N_Licon_hor = int((W - 2 * Li_Encloses_Licon_Two_Sides + Licon_Spacing) / (Licon_Width_Length + Licon_Spacing))
        Remaining_Licon_hor = W - 2 * Li_Encloses_Licon_Two_Sides - N_Licon_hor * Licon_Width_Length - (
                    N_Licon_hor - 1) * Licon_Spacing

        N_Licon_ver = int(
            (Lver - 2 * Li_Encloses_Licon_Two_Sides + Licon_Spacing) / (Licon_Width_Length + Licon_Spacing))
        Remaining_Licon_ver = Lver - 2 * Li_Encloses_Licon_Two_Sides - N_Licon_ver * Licon_Width_Length - (
                    N_Licon_ver - 1) * Licon_Spacing

        xcor_Licon = 0
        ycor_Licon = 0
        # print(N_Licon_hor,N_Licon_ver)
        # find the number of mcon needed for the horizontal distance
        N_Mcon_hor = int((W - 2 * Met1_Encloses_Mcon_Two_Sides + Mcon_Spacing) / (Mcon_Width_Length + Mcon_Spacing))
        Remaining_Mcon_hor = W - 2 * Met1_Encloses_Mcon_Two_Sides - N_Mcon_hor * Mcon_Width_Length - (
                    N_Mcon_hor - 1) * Mcon_Spacing

        N_Mcon_ver = int((Lver - 2 * Met1_Encloses_Mcon_Two_Sides + Mcon_Spacing) / (Mcon_Width_Length + Mcon_Spacing))
        Remaining_Mcon_ver = Lver - 2 * Met1_Encloses_Mcon_Two_Sides - N_Mcon_ver * Mcon_Width_Length - (
                    N_Mcon_ver - 1) * Mcon_Spacing

        xcor_Mcon = 0
        ycor_Mcon = 0

        # print(N_Mcon_hor,N_Mcon_ver)
        Slope = Lver / Lhor

        if N_Conductors % 2 == 0:  # draw odd numbers of conductors
            N_Conductors = N_Conductors - 1
        N_of_half_Conductors = int(N_Conductors / 2)

        for i in range(N_of_half_Conductors):  # draw the vertical conductors
            xcor = - Lhor / 2 + i * (W + S)
            ycor = -Lver / 2
            self.cell.shapes(met1).insert(
                pya.Box(xcor, ycor, xcor + W, ycor + (i + 1) * (W + S) * Slope))  # left down vertical conductors
            self.cell.shapes(met1).insert(
                pya.Box(-xcor, ycor, -xcor - W, ycor + (i + 1) * (W + S) * Slope))  # right down vertical conductors
            self.cell.shapes(met1).insert(pya.Box(xcor, ycor + Lver, xcor + W, ycor + Lver - (i + 1) * (
                        W + S) * Slope))  # left up vertical conductors
            self.cell.shapes(met1).insert(pya.Box(-xcor, ycor + Lver, -xcor - W, ycor + Lver - (i + 1) * (
                        W + S) * Slope))  # right up vertical conductors

            if Shielding_with_diffusion == 1:
                self.cell.shapes(nwell).insert(
                    pya.Box(xcor, ycor, xcor + W, ycor + (i + 1) * (W + S) * Slope))  # left down vertical conductors
                self.cell.shapes(nwell).insert(
                    pya.Box(-xcor, ycor, -xcor - W, ycor + (i + 1) * (W + S) * Slope))  # right down vertical conductors
                self.cell.shapes(nwell).insert(pya.Box(xcor, ycor + Lver, xcor + W,
                                                       ycor + Lver - (i + 1) * (
                                                                   W + S) * Slope))  # left up vertical conductors
                self.cell.shapes(nwell).insert(pya.Box(-xcor, ycor + Lver, -xcor - W,
                                                       ycor + Lver - (i + 1) * (
                                                                   W + S) * Slope))  # right up vertical conductors

                self.cell.shapes(li1).insert(
                    pya.Box(xcor, ycor, xcor + W, ycor + (i + 1) * (W + S) * Slope))  # left down vertical conductors
                self.cell.shapes(li1).insert(
                    pya.Box(-xcor, ycor, -xcor - W, ycor + (i + 1) * (W + S) * Slope))  # right down vertical conductors
                self.cell.shapes(li1).insert(pya.Box(xcor, ycor + Lver, xcor + W,
                                                     ycor + Lver - (i + 1) * (
                                                                 W + S) * Slope))  # left up vertical conductors
                self.cell.shapes(li1).insert(pya.Box(-xcor, ycor + Lver, -xcor - W,
                                                     ycor + Lver - (i + 1) * (
                                                                 W + S) * Slope))  # right up vertical conductors

                self.cell.shapes(nsdm).insert(
                    pya.Box(xcor, ycor, xcor + W, ycor + (i + 1) * (W + S) * Slope))  # left down vertical conductors
                self.cell.shapes(nsdm).insert(
                    pya.Box(-xcor, ycor, -xcor - W, ycor + (i + 1) * (W + S) * Slope))  # right down vertical conductors
                self.cell.shapes(nsdm).insert(pya.Box(xcor, ycor + Lver, xcor + W,
                                                      ycor + Lver - (i + 1) * (
                                                                  W + S) * Slope))  # left up vertical conductors
                self.cell.shapes(nsdm).insert(pya.Box(-xcor, ycor + Lver, -xcor - W,
                                                      ycor + Lver - (i + 1) * (
                                                                  W + S) * Slope))  # right up vertical conductors

                N_Licon_hor = int(
                    (W - 2 * Li_Encloses_Licon_Two_Sides + Licon_Spacing) / (Licon_Width_Length + Licon_Spacing))
                Remaining_Licon_hor = W - 2 * Li_Encloses_Licon_Two_Sides - N_Licon_hor * Licon_Width_Length - (
                        N_Licon_hor - 1) * Licon_Spacing

                N_Licon_ver = int(((i + 1) * (W + S) * Slope - 2 * Li_Encloses_Licon_Two_Sides + Licon_Spacing) / (
                            Licon_Width_Length + Licon_Spacing))
                Remaining_Licon_ver = (i + 1) * (
                            W + S) * Slope - 2 * Li_Encloses_Licon_Two_Sides - N_Licon_ver * Licon_Width_Length - (
                                              N_Licon_ver - 1) * Licon_Spacing
                for u in range(N_Licon_ver):
                    ycor_Licon = Li_Encloses_Licon_Two_Sides + Remaining_Licon_ver / 2 + u * (
                                Licon_Width_Length + Licon_Spacing)
                    for k in range(N_Licon_hor):
                        xcor_Licon = Li_Encloses_Licon_Two_Sides + Remaining_Licon_hor / 2 + k * (
                                    Licon_Width_Length + Licon_Spacing)
                        self.cell.shapes(licon1).insert(pya.Box(xcor + xcor_Licon, ycor + ycor_Licon,
                                                                xcor + xcor_Licon + Licon_Width_Length,
                                                                ycor + ycor_Licon + Licon_Width_Length))
                        self.cell.shapes(licon1).insert(pya.Box(-xcor - xcor_Licon, ycor + ycor_Licon,
                                                                -xcor - xcor_Licon - Licon_Width_Length,
                                                                ycor + ycor_Licon + Licon_Width_Length))
                        self.cell.shapes(licon1).insert(pya.Box(xcor + xcor_Licon, ycor + Lver - ycor_Licon,
                                                                xcor + xcor_Licon + Licon_Width_Length,
                                                                ycor + Lver - ycor_Licon - Licon_Width_Length))
                        self.cell.shapes(licon1).insert(pya.Box(-xcor - xcor_Licon, ycor + Lver - ycor_Licon,
                                                                -xcor - xcor_Licon - Licon_Width_Length,
                                                                ycor + Lver - ycor_Licon - Licon_Width_Length))
                N_Mcon_hor = int(
                    (W - 2 * Met1_Encloses_Mcon_Two_Sides + Mcon_Spacing) / (Mcon_Width_Length + Mcon_Spacing))
                Remaining_Mcon_hor = W - 2 * Met1_Encloses_Mcon_Two_Sides - N_Mcon_hor * Mcon_Width_Length - (
                        N_Mcon_hor - 1) * Mcon_Spacing

                N_Mcon_ver = int(((i + 1) * (W + S) * Slope - 2 * Met1_Encloses_Mcon_Two_Sides + Mcon_Spacing) / (
                            Mcon_Width_Length + Mcon_Spacing))
                Remaining_Mcon_ver = (i + 1) * (
                            W + S) * Slope - 2 * Met1_Encloses_Mcon_Two_Sides - N_Mcon_ver * Mcon_Width_Length - (
                                             N_Mcon_ver - 1) * Mcon_Spacing

                for u in range(N_Mcon_ver):
                    ycor_Mcon = Met1_Encloses_Mcon_Two_Sides + Remaining_Mcon_ver / 2 + u * (
                                Mcon_Width_Length + Mcon_Spacing)
                    for k in range(N_Mcon_hor):
                        xcor_Mcon = Met1_Encloses_Mcon_Two_Sides + Remaining_Mcon_hor / 2 + k * (
                                    Mcon_Width_Length + Mcon_Spacing)
                        self.cell.shapes(mcon).insert(pya.Box(xcor + xcor_Mcon, ycor + ycor_Mcon,
                                                              xcor + xcor_Mcon + Mcon_Width_Length,
                                                              ycor + ycor_Mcon + Mcon_Width_Length))
                        self.cell.shapes(mcon).insert(pya.Box(-xcor - xcor_Mcon, ycor + ycor_Mcon,
                                                              -xcor - xcor_Mcon - Mcon_Width_Length,
                                                              ycor + ycor_Mcon + Mcon_Width_Length))
                        self.cell.shapes(mcon).insert(pya.Box(xcor + xcor_Mcon, ycor + Lver - ycor_Mcon,
                                                              xcor + xcor_Mcon + Mcon_Width_Length,
                                                              ycor + Lver - ycor_Mcon - Mcon_Width_Length))
                        self.cell.shapes(mcon).insert(pya.Box(-xcor - xcor_Mcon, ycor + Lver - ycor_Mcon,
                                                              -xcor - xcor_Mcon - Mcon_Width_Length,
                                                              ycor + Lver - ycor_Mcon - Mcon_Width_Length))

            if i == N_of_half_Conductors - 1:
                y_check = ycor + (i + 1) * (W + S) * Slope

        # drawing the rest of spaces for the vertical conductor
        xcor = xcor + (W + S)
        self.cell.shapes(met1).insert(pya.Box(xcor, ycor, -xcor, -S / 2))
        self.cell.shapes(met1).insert(pya.Box(xcor, ycor + Lver, -xcor, S / 2))
        if Shielding_with_diffusion == 1:
            self.cell.shapes(nwell).insert(pya.Box(xcor, ycor, -xcor, -S / 2))
            self.cell.shapes(nwell).insert(pya.Box(xcor, ycor + Lver, -xcor, S / 2))
            self.cell.shapes(li1).insert(pya.Box(xcor, ycor, -xcor, -S / 2))
            self.cell.shapes(li1).insert(pya.Box(xcor, ycor + Lver, -xcor, S / 2))
            self.cell.shapes(nsdm).insert(pya.Box(xcor, ycor, -xcor, -S / 2))
            self.cell.shapes(nsdm).insert(pya.Box(xcor, ycor + Lver, -xcor, S / 2))
            N_Licon_hor = int(
                (-2 * xcor - 2 * Li_Encloses_Licon_Two_Sides + Licon_Spacing) / (Licon_Width_Length + Licon_Spacing))
            Remaining_Licon_hor = -2 * xcor - 2 * Li_Encloses_Licon_Two_Sides - N_Licon_hor * Licon_Width_Length - (
                    N_Licon_hor - 1) * Licon_Spacing

            N_Licon_ver = int(((-ycor - S / 2) - 2 * Li_Encloses_Licon_Two_Sides + Licon_Spacing) / (
                    Licon_Width_Length + Licon_Spacing))
            Remaining_Licon_ver = (
                                              -ycor - S / 2) - 2 * Li_Encloses_Licon_Two_Sides - N_Licon_ver * Licon_Width_Length - (
                                          N_Licon_ver - 1) * Licon_Spacing
            for u in range(N_Licon_ver):
                ycor_Licon = Li_Encloses_Licon_Two_Sides + Remaining_Licon_ver / 2 + u * (
                            Licon_Width_Length + Licon_Spacing)
                for k in range(N_Licon_hor):
                    xcor_Licon = Li_Encloses_Licon_Two_Sides + Remaining_Licon_hor / 2 + k * (
                                Licon_Width_Length + Licon_Spacing)
                    self.cell.shapes(licon1).insert(pya.Box(xcor + xcor_Licon, ycor + ycor_Licon,
                                                            xcor + xcor_Licon + Licon_Width_Length,
                                                            ycor + ycor_Licon + Licon_Width_Length))
                    self.cell.shapes(licon1).insert(pya.Box(xcor + xcor_Licon, ycor + Lver - ycor_Licon,
                                                            xcor + xcor_Licon + Licon_Width_Length,
                                                            ycor + Lver - ycor_Licon - Licon_Width_Length))

            N_Mcon_hor = int(
                (-2 * xcor - 2 * Met1_Encloses_Mcon_Two_Sides + Mcon_Spacing) / (Mcon_Width_Length + Mcon_Spacing))
            Remaining_Mcon_hor = -2 * xcor - 2 * Met1_Encloses_Mcon_Two_Sides - N_Mcon_hor * Mcon_Width_Length - (
                    N_Mcon_hor - 1) * Mcon_Spacing

            N_Mcon_ver = int(((-ycor - S / 2) - 2 * Met1_Encloses_Mcon_Two_Sides + Mcon_Spacing) / (
                    Mcon_Width_Length + Mcon_Spacing))
            Remaining_Mcon_ver = (-ycor - S / 2) - 2 * Met1_Encloses_Mcon_Two_Sides - N_Mcon_ver * Mcon_Width_Length - (
                    N_Mcon_ver - 1) * Mcon_Spacing

            for u in range(N_Mcon_ver):
                ycor_Mcon = Met1_Encloses_Mcon_Two_Sides + Remaining_Mcon_ver / 2 + u * (
                            Mcon_Width_Length + Mcon_Spacing)
                for k in range(N_Mcon_hor):
                    xcor_Mcon = Met1_Encloses_Mcon_Two_Sides + Remaining_Mcon_hor / 2 + k * (
                                Mcon_Width_Length + Mcon_Spacing)
                    self.cell.shapes(mcon).insert(pya.Box(xcor + xcor_Mcon, ycor + ycor_Mcon,
                                                          xcor + xcor_Mcon + Mcon_Width_Length,
                                                          ycor + ycor_Mcon + Mcon_Width_Length))
                    self.cell.shapes(mcon).insert(pya.Box(xcor + xcor_Mcon, ycor + Lver - ycor_Mcon,
                                                          xcor + xcor_Mcon + Mcon_Width_Length,
                                                          ycor + Lver - ycor_Mcon - Mcon_Width_Length))

        for j in range(N_of_half_Conductors - 1):  # For loop for horizontal conductors
            xcor2 = -Lhor / 2
            ycor2 = -Lver / 2
            self.cell.shapes(met1).insert(
                pya.Box(xcor2, ycor2 + (j + 1) * (W + S) * Slope + S, xcor2 + (j + 1) * (W + S) * Slope - S
                        , ycor2 + (j + 1) * (W + S) * Slope + S + W))  # left down horizontal conductors

            self.cell.shapes(met1).insert(
                pya.Box(xcor2, ycor2 + Lver - (j + 1) * (W + S) * Slope - S, xcor2 + (j + 1) * (W + S) * Slope - S
                        , ycor2 + Lver - (j + 1) * (W + S) * Slope - S - W))  # left up horizontal conductors

            self.cell.shapes(met1).insert(pya.Box(xcor2 + Lhor, ycor2 + (j + 1) * (W + S) * Slope + S,
                                                  xcor2 + Lhor - (j + 1) * (W + S) * Slope + S
                                                  , ycor2 + (j + 1) * (
                                                              W + S) * Slope + S + W))  # right down horizontal conductors

            self.cell.shapes(met1).insert(pya.Box(xcor2 + Lhor, ycor2 + Lver - (j + 1) * (W + S) * Slope - S,
                                                  xcor2 + Lhor - (j + 1) * (W + S) * Slope + S
                                                  , ycor2 + Lver - (j + 1) * (
                                                              W + S) * Slope - S - W))  # right up horizontal conductors
            if Shielding_with_diffusion == 1:
                self.cell.shapes(nwell).insert(
                    pya.Box(xcor2, ycor2 + (j + 1) * (W + S) * Slope + S, xcor2 + (j + 1) * (W + S) * Slope - S
                            , ycor2 + (j + 1) * (W + S) * Slope + S + W))  # left down horizontal conductors

                self.cell.shapes(nwell).insert(
                    pya.Box(xcor2, ycor2 + Lver - (j + 1) * (W + S) * Slope - S, xcor2 + (j + 1) * (W + S) * Slope - S
                            , ycor2 + Lver - (j + 1) * (W + S) * Slope - S - W))  # left up horizontal conductors

                self.cell.shapes(nwell).insert(
                    pya.Box(xcor2 + Lhor, ycor2 + (j + 1) * (W + S) * Slope + S,
                            xcor2 + Lhor - (j + 1) * (W + S) * Slope + S
                            , ycor2 + (j + 1) * (W + S) * Slope + S + W))  # left down horizontal conductors

                self.cell.shapes(nwell).insert(pya.Box(xcor2 + Lhor, ycor2 + Lver - (j + 1) * (W + S) * Slope - S,
                                                       xcor2 + Lhor - (j + 1) * (W + S) * Slope + S
                                                       , ycor2 + Lver - (j + 1) * (
                                                               W + S) * Slope - S - W))  # left up horizontal conductors

                self.cell.shapes(li1).insert(
                    pya.Box(xcor2, ycor2 + (j + 1) * (W + S) * Slope + S, xcor2 + (j + 1) * (W + S) * Slope - S
                            , ycor2 + (j + 1) * (W + S) * Slope + S + W))  # left down horizontal conductors

                self.cell.shapes(li1).insert(
                    pya.Box(xcor2, ycor2 + Lver - (j + 1) * (W + S) * Slope - S, xcor2 + (j + 1) * (W + S) * Slope - S
                            , ycor2 + Lver - (j + 1) * (W + S) * Slope - S - W))  # left up horizontal conductors

                self.cell.shapes(li1).insert(
                    pya.Box(xcor2 + Lhor, ycor2 + (j + 1) * (W + S) * Slope + S,
                            xcor2 + Lhor - (j + 1) * (W + S) * Slope + S
                            , ycor2 + (j + 1) * (W + S) * Slope + S + W))  # left down horizontal conductors

                self.cell.shapes(li1).insert(pya.Box(xcor2 + Lhor, ycor2 + Lver - (j + 1) * (W + S) * Slope - S,
                                                     xcor2 + Lhor - (j + 1) * (W + S) * Slope + S
                                                     , ycor2 + Lver - (j + 1) * (
                                                             W + S) * Slope - S - W))  # left up horizontal conductors

                self.cell.shapes(nsdm).insert(
                    pya.Box(xcor2, ycor2 + (j + 1) * (W + S) * Slope + S, xcor2 + (j + 1) * (W + S) * Slope - S
                            , ycor2 + (j + 1) * (W + S) * Slope + S + W))  # left down horizontal conductors

                self.cell.shapes(nsdm).insert(
                    pya.Box(xcor2, ycor2 + Lver - (j + 1) * (W + S) * Slope - S, xcor2 + (j + 1) * (W + S) * Slope - S
                            , ycor2 + Lver - (j + 1) * (W + S) * Slope - S - W))  # left up horizontal conductors

                self.cell.shapes(nsdm).insert(
                    pya.Box(xcor2 + Lhor, ycor2 + (j + 1) * (W + S) * Slope + S,
                            xcor2 + Lhor - (j + 1) * (W + S) * Slope + S
                            , ycor2 + (j + 1) * (W + S) * Slope + S + W))  # left down horizontal conductors

                self.cell.shapes(nsdm).insert(pya.Box(xcor2 + Lhor, ycor2 + Lver - (j + 1) * (W + S) * Slope - S,
                                                      xcor2 + Lhor - (j + 1) * (W + S) * Slope + S
                                                      , ycor2 + Lver - (j + 1) * (
                                                              W + S) * Slope - S - W))  # left up horizontal conductors

                N_Licon_hor = int(((j + 1) * (W + S) * Slope - S - 2 * Li_Encloses_Licon_Two_Sides + Licon_Spacing) / (
                            Licon_Width_Length + Licon_Spacing))
                Remaining_Licon_hor = (j + 1) * (
                            W + S) * Slope - S - 2 * Li_Encloses_Licon_Two_Sides - N_Licon_hor * Licon_Width_Length - (
                                              N_Licon_hor - 1) * Licon_Spacing

                N_Licon_ver = int((W - 2 * Li_Encloses_Licon_Two_Sides + Licon_Spacing) / (
                        Licon_Width_Length + Licon_Spacing))
                Remaining_Licon_ver = W - 2 * Li_Encloses_Licon_Two_Sides - N_Licon_ver * Licon_Width_Length - (
                        N_Licon_ver - 1) * Licon_Spacing
                for u in range(N_Licon_ver):
                    ycor_Licon = Li_Encloses_Licon_Two_Sides + Remaining_Licon_ver / 2 + u * (
                            Licon_Width_Length + Licon_Spacing)
                    for k in range(N_Licon_hor):
                        xcor_Licon = Li_Encloses_Licon_Two_Sides + Remaining_Licon_hor / 2 + k * (
                                Licon_Width_Length + Licon_Spacing)
                        self.cell.shapes(licon1).insert(
                            pya.Box(xcor2 + xcor_Licon, ycor2 + (j + 1) * (W + S) * Slope + S + ycor_Licon,
                                    xcor2 + xcor_Licon + Licon_Width_Length,
                                    ycor2 + (j + 1) * (W + S) * Slope + S + ycor_Licon + Licon_Width_Length))
                        self.cell.shapes(licon1).insert(
                            pya.Box(xcor2 + xcor_Licon, ycor2 + Lver - (j + 1) * (W + S) * Slope - S - ycor_Licon,
                                    xcor2 + xcor_Licon + Licon_Width_Length,
                                    ycor2 + Lver - (j + 1) * (W + S) * Slope - S - ycor_Licon - Licon_Width_Length))
                        self.cell.shapes(licon1).insert(
                            pya.Box(xcor2 + Lhor - xcor_Licon, ycor2 + (j + 1) * (W + S) * Slope + S + ycor_Licon,
                                    xcor2 + Lhor - xcor_Licon - Licon_Width_Length,
                                    ycor2 + (j + 1) * (W + S) * Slope + S + ycor_Licon + Licon_Width_Length))
                        self.cell.shapes(licon1).insert(
                            pya.Box(xcor2 + Lhor - xcor_Licon,
                                    ycor2 + Lver - (j + 1) * (W + S) * Slope - S - ycor_Licon,
                                    xcor2 + Lhor - xcor_Licon - Licon_Width_Length,
                                    ycor2 + Lver - (j + 1) * (W + S) * Slope - S - ycor_Licon - Licon_Width_Length))
                N_Mcon_hor = int(((j + 1) * (W + S) * Slope - S - 2 * Met1_Encloses_Mcon_Two_Sides + Mcon_Spacing) / (
                            Mcon_Width_Length + Mcon_Spacing))
                Remaining_Mcon_hor = (j + 1) * (
                            W + S) * Slope - S - 2 * Met1_Encloses_Mcon_Two_Sides - N_Mcon_hor * Mcon_Width_Length - (
                                             N_Mcon_hor - 1) * Mcon_Spacing

                N_Mcon_ver = int((W - 2 * Met1_Encloses_Mcon_Two_Sides + Mcon_Spacing) / (
                        Mcon_Width_Length + Mcon_Spacing))
                Remaining_Mcon_ver = W - 2 * Met1_Encloses_Mcon_Two_Sides - N_Mcon_ver * Mcon_Width_Length - (
                        N_Mcon_ver - 1) * Mcon_Spacing
                for u in range(N_Mcon_ver):
                    ycor_Mcon = Met1_Encloses_Mcon_Two_Sides + Remaining_Mcon_ver / 2 + u * (
                                Mcon_Width_Length + Mcon_Spacing)
                    for k in range(N_Mcon_hor):
                        xcor_Mcon = Met1_Encloses_Mcon_Two_Sides + Remaining_Mcon_hor / 2 + k * (
                                Mcon_Width_Length + Mcon_Spacing)
                        self.cell.shapes(mcon).insert(
                            pya.Box(xcor2 + xcor_Mcon, ycor2 + (j + 1) * (W + S) * Slope + S + ycor_Mcon,
                                    xcor2 + xcor_Mcon + Mcon_Width_Length,
                                    ycor2 + (j + 1) * (W + S) * Slope + S + ycor_Mcon + Mcon_Width_Length))
                        self.cell.shapes(mcon).insert(
                            pya.Box(xcor2 + xcor_Mcon, ycor2 + Lver - (j + 1) * (W + S) * Slope - S - ycor_Mcon,
                                    xcor2 + xcor_Mcon + Mcon_Width_Length,
                                    ycor2 + Lver - (j + 1) * (W + S) * Slope - S - ycor_Mcon - Mcon_Width_Length))
                        self.cell.shapes(mcon).insert(
                            pya.Box(xcor2 + Lhor - xcor_Mcon, ycor2 + (j + 1) * (W + S) * Slope + S + ycor_Mcon,
                                    xcor2 + Lhor - xcor_Mcon - Mcon_Width_Length,
                                    ycor2 + (j + 1) * (W + S) * Slope + S + ycor_Mcon + Mcon_Width_Length))
                        self.cell.shapes(mcon).insert(
                            pya.Box(xcor2 + Lhor - xcor_Mcon, ycor2 + Lver - (j + 1) * (W + S) * Slope - S - ycor_Mcon,
                                    xcor2 + Lhor - xcor_Mcon - Mcon_Width_Length,
                                    ycor2 + Lver - (j + 1) * (W + S) * Slope - S - ycor_Mcon - Mcon_Width_Length))

            # y_check is used for drawing the rest of spaces for the horizontal conductors
            if j == N_of_half_Conductors - 2:
                x_check = xcor2 + (j + 1) * (W + S) * Slope + W
        if (-y_check * 2) >= (2 * S + 0.14):
            self.cell.shapes(met1).insert(pya.Box(xcor2, y_check + S, x_check, -y_check - S))
            self.cell.shapes(met1).insert(pya.Box(xcor2 + Lhor, y_check + S, -x_check, -y_check - S))
            if Shielding_with_diffusion == 1:
                self.cell.shapes(nwell).insert(pya.Box(xcor2, y_check + S, x_check, -y_check - S))
                self.cell.shapes(nwell).insert(pya.Box(xcor2 + Lhor, y_check + S, -x_check, -y_check - S))
                self.cell.shapes(li1).insert(pya.Box(xcor2, y_check + S, x_check, -y_check - S))
                self.cell.shapes(li1).insert(pya.Box(xcor2 + Lhor, y_check + S, -x_check, -y_check - S))
                self.cell.shapes(nsdm).insert(pya.Box(xcor2, y_check + S, x_check, -y_check - S))
                self.cell.shapes(nsdm).insert(pya.Box(xcor2 + Lhor, y_check + S, -x_check, -y_check - S))
                N_Licon_hor = int(((x_check - xcor2) - 2 * Li_Encloses_Licon_Two_Sides + Licon_Spacing) / (
                        Licon_Width_Length + Licon_Spacing))
                Remaining_Licon_hor = (
                                                  x_check - xcor2) - 2 * Li_Encloses_Licon_Two_Sides - N_Licon_hor * Licon_Width_Length - (
                                              N_Licon_hor - 1) * Licon_Spacing

                N_Licon_ver = int((-y_check * 2 - 2 * S - 2 * Li_Encloses_Licon_Two_Sides + Licon_Spacing) / (
                        Licon_Width_Length + Licon_Spacing))
                Remaining_Licon_ver = -y_check * 2 - 2 * S - 2 * Li_Encloses_Licon_Two_Sides - N_Licon_ver * Licon_Width_Length - (
                        N_Licon_ver - 1) * Licon_Spacing
                for u in range(N_Licon_ver):
                    ycor_Licon = Li_Encloses_Licon_Two_Sides + Remaining_Licon_ver / 2 + u * (
                            Licon_Width_Length + Licon_Spacing)
                    for k in range(N_Licon_hor):
                        xcor_Licon = Li_Encloses_Licon_Two_Sides + Remaining_Licon_hor / 2 + k * (
                                Licon_Width_Length + Licon_Spacing)
                        self.cell.shapes(licon1).insert(
                            pya.Box(xcor2 + xcor_Licon, y_check + S + ycor_Licon,
                                    xcor2 + xcor_Licon + Licon_Width_Length,
                                    y_check + S + ycor_Licon + Licon_Width_Length))

                        self.cell.shapes(licon1).insert(
                            pya.Box(xcor2 + Lhor - xcor_Licon, y_check + S + ycor_Licon,
                                    xcor2 + Lhor - xcor_Licon - Licon_Width_Length,
                                    y_check + S + ycor_Licon + Licon_Width_Length))

                N_Mcon_hor = int(((x_check - xcor2) - 2 * Met1_Encloses_Mcon_Two_Sides + Mcon_Spacing) / (
                        Mcon_Width_Length + Mcon_Spacing))
                Remaining_Mcon_hor = (
                                                 x_check - xcor2) - 2 * Met1_Encloses_Mcon_Two_Sides - N_Mcon_hor * Mcon_Width_Length - (
                                             N_Mcon_hor - 1) * Mcon_Spacing

                N_Mcon_ver = int((-y_check * 2 - 2 * S - 2 * Met1_Encloses_Mcon_Two_Sides + Mcon_Spacing) / (
                        Mcon_Width_Length + Mcon_Spacing))
                Remaining_Mcon_ver = -y_check * 2 - 2 * S - 2 * Met1_Encloses_Mcon_Two_Sides - N_Mcon_ver * Mcon_Width_Length - (
                        N_Mcon_ver - 1) * Mcon_Spacing

                for u in range(N_Mcon_ver):
                    ycor_Mcon = Met1_Encloses_Mcon_Two_Sides + Remaining_Mcon_ver / 2 + u * (
                                Mcon_Width_Length + Mcon_Spacing)
                    for k in range(N_Mcon_hor):
                        xcor_Mcon = Met1_Encloses_Mcon_Two_Sides + Remaining_Mcon_hor / 2 + k * (
                                Mcon_Width_Length + Mcon_Spacing)
                        self.cell.shapes(mcon).insert(
                            pya.Box(xcor2 + xcor_Mcon, y_check + S + ycor_Mcon,
                                    xcor2 + xcor_Mcon + Mcon_Width_Length,
                                    y_check + S + ycor_Mcon + Mcon_Width_Length))

                        self.cell.shapes(mcon).insert(
                            pya.Box(xcor2 + Lhor - xcor_Mcon, y_check + S + ycor_Mcon,
                                    xcor2 + Lhor - xcor_Mcon - Mcon_Width_Length,
                                    y_check + S + ycor_Mcon + Mcon_Width_Length))


