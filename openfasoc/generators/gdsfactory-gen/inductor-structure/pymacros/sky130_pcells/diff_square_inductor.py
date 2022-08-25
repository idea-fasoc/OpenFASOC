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
## Mabrains differential_squar_Inductor Generator for Skywaters 130nm
########################################################################################################################
from .layers_definiations import *
import pya
import math
import pandas as pd


"""
Mabrains Via Generator for Skywaters 130nm
"""



class diff_squar_ind_Generator(pya.PCellDeclarationHelper):
    """
    Mabrains Via Generator for Skywaters 130nm
    """


    def __init__(self):
        ## Initialize super class.
        super(diff_squar_ind_Generator, self).__init__()

        # declare the parameters
        self.param("N", self.TypeInt, "number of turns", default=3)
        self.param("W", self.TypeDouble, "Width of the conductors", default=2)
        self.param("S", self.TypeDouble, "Spacing between conductors", default=4)
        self.param("distance_input", self.TypeDouble, "Distance of input conductors", default=10)
        self.param("spacing_input", self.TypeDouble, "Spacing of input inductors conductors", default=8)


        self.param("Louter", self.TypeDouble, "outer dimension", default=60)

        shielding_option = self.param("shielding", self.TypeString, "Shielding Type", default="No shielding")
        shielding_option.add_choice("No shielding", 0)
        shielding_option.add_choice("rectangular_shielding", 1)
        shielding_option.add_choice("triangular_shielding", 2)

        self.param("W_shielding", self.TypeDouble, "Width of the conductors for shielding", default=2)
        self.param("S_shielding", self.TypeDouble, "Spacing between conductors for shielding", default=4)
        #self.param("Lvert_shielding", self.TypeDouble, "vertical dimension for shielding", default=40)
        #self.param("Lhor_shielding", self.TypeDouble, "horizontal dimension for shielding", default=40)
        self.param("diffusion_shielding", self.TypeBoolean, "Diffusion shielding", default=0)



        #self.param("via", self.TypeLayer, "via_layer", default = pya.LayerInfo(via_lay_num,via_lay_dt), hidden = True)

        # Below shows how to create hidden parameter is used to determine whether the radius has changed
        # or the "s" handle has been moved
        ## self.param("ru", self.TypeDouble, "Radius", default = 0.0, hidden = True)
        ## self.param("rd", self.TypeDouble, "Double radius", readonly = True)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "(" + str(self.N) + " midth = "+str(self.W) +")"

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

    def rectangular_shielding(self,W,S,Lver,Lhor,diffusion,input_distance):
        PERCISION = 1000
        input_distance = input_distance*PERCISION
        met1 = self.layout.layer(met1_lay_num, met1_lay_dt)
        diff = self.layout.layer(diff_lay_num, diff_lay_dt)
        psdm = self.layout.layer(psdm_lay_num, psdm_lay_dt)
        licon1 = self.layout.layer(licon_lay_num, licon_lay_dt)
        li1 = self.layout.layer(li_lay_num, li_lay_dt)
        mcon = self.layout.layer(mcon_lay_num, mcon_lay_dt)
        nwell = self.layout.layer(nwell_lay_num, nwell_lay_dt)
        nsdm = self.layout.layer(nsdm_lay_num, nsdm_lay_dt)
        W = W * PERCISION  # width of the conductors
        S = S * PERCISION  # minimum spacing between the conductors is 1.27*PERCISION
        S_min = 1.27 * PERCISION
        Lver = Lver * PERCISION  # the vertical length
        Lhor = Lhor * PERCISION  # the horizontal length
        N_Conductors = int((Lhor + S) / (S + W))  # number of conductors
        xcor = -Lhor/2
        ycor = input_distance
        Shielding_with_diffusion = diffusion
        print("shifty" + str(input_distance))

        # defining different parameters for different layers
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
        # find the number of licon needed for the vertical distance
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
        # find the number of mcon needed for the vertical distance
        N_Mcon_ver = int((Lver - 2 * Met1_Encloses_Mcon_Two_Sides + Mcon_Spacing) / (Mcon_Width_Length + Mcon_Spacing))
        Remaining_Mcon_ver = Lver - 2 * Met1_Encloses_Mcon_Two_Sides - N_Mcon_ver * Mcon_Width_Length - (
                N_Mcon_ver - 1) * Mcon_Spacing

        xcor_Mcon = 0
        ycor_Mcon = 0

        # print(N_Mcon_hor,N_Mcon_ver)

        for i in range(N_Conductors):

            if S < S_min:
                print("Spacing between the Inductors must be greater than 1.27 um ")
                break
            xcor = i * (W + S) -Lhor/2
            ycor = input_distance
            self.cell.shapes(met1).insert(pya.Box(xcor, ycor, xcor + W, ycor + Lver))  # draw the metal conductors
            if Shielding_with_diffusion == 1:  # inserting diffusion layer if it's true
                # self.cell.shapes(diff).insert(pya.Box(xcor, ycor, xcor + W, ycor + Lver))
                self.cell.shapes(li1).insert(pya.Box(xcor, ycor, xcor + W, ycor + Lver))
                # self.cell.shapes(nsdm).insert(pya.Box(xcor-nsdm_Encloses_Diffusion,ycor-nsdm_Encloses_Diffusion
                #    ,xcor+W+nsdm_Encloses_Diffusion,ycor+Lver+nsdm_Encloses_Diffusion))
                self.cell.shapes(nsdm).insert(pya.Box(xcor, ycor, xcor + W, ycor + Lver))
                self.cell.shapes(nwell).insert(pya.Box(xcor, ycor, xcor + W, ycor + Lver))

                # drawing licon and mcon as rows and columns
                for j in range(N_Licon_ver):  # drawing the licon in yaxis
                    ycor_Licon = Li_Encloses_Licon_Two_Sides + Remaining_Licon_ver / 2 + j * (
                            Licon_Width_Length + Licon_Spacing)
                    for k in range(N_Licon_hor):  # drawing the licon in xaxis
                        xcor_Licon = Li_Encloses_Licon_Two_Sides + Remaining_Licon_hor / 2 + k * (
                                Licon_Width_Length + Licon_Spacing)
                        self.cell.shapes(licon1).insert(pya.Box(xcor + xcor_Licon, ycor + ycor_Licon,
                                                                xcor + xcor_Licon + Licon_Width_Length,
                                                                ycor + ycor_Licon + Licon_Width_Length))

                for j in range(N_Mcon_ver):  # drawing the mcon in yaxis
                    ycor_Mcon = Met1_Encloses_Mcon_Two_Sides + Remaining_Mcon_ver / 2 + j * (
                            Mcon_Width_Length + Mcon_Spacing)
                    for k in range(N_Mcon_hor):  # drawing the mcon in xaxis
                        xcor_Mcon = Met1_Encloses_Mcon_Two_Sides + Remaining_Mcon_hor / 2 + k * (
                                Mcon_Width_Length + Mcon_Spacing)
                        self.cell.shapes(mcon).insert(pya.Box(xcor + xcor_Mcon, ycor + ycor_Mcon,
                                                              xcor + xcor_Mcon + Mcon_Width_Length,
                                                              ycor + ycor_Mcon + Mcon_Width_Length))
        if S >= S_min:
            self.cell.shapes(met1).insert(pya.Box(-Lhor/2, Lver / 2 - W / 2+input_distance, Lhor/2, Lver / 2 + W / 2+input_distance))


    def triangular_shielding(self,W,S,Lhor,diffusion,input_distance):
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

        W = W * PERCISION  # width of the conductors
        S = S* PERCISION  # minimum spacing between the conductors is 1.27*PERCISION due to the N_well
        S_min = 1.27 * PERCISION
        Lver = Lhor * PERCISION  # Lver==Lhor because it's assumed that the overall shape is square
        Lhor = Lhor* PERCISION
        input_distance = input_distance*PERCISION
        N_Conductors = int((Lhor + S) / (S + W))  # number of conductors
        xcor = 0
        ycor = 0
        xcor2 = 0
        ycor2 = 0
        y_check = 0
        x_check = 0
        Shielding_with_diffusion = diffusion
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
            ycor = input_distance
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
        self.cell.shapes(met1).insert(pya.Box(xcor, ycor, -xcor, ycor+Lver/2-S / 2))
        self.cell.shapes(met1).insert(pya.Box(xcor, ycor + Lver, -xcor,ycor+Lver/2+ S / 2))
        if Shielding_with_diffusion == 1:
            self.cell.shapes(nwell).insert(pya.Box(xcor, ycor, -xcor, ycor+Lver/2-S / 2))
            self.cell.shapes(nwell).insert(pya.Box(xcor, ycor + Lver, -xcor, ycor+Lver/2+S / 2))
            self.cell.shapes(li1).insert(pya.Box(xcor, ycor, -xcor, ycor+Lver/2-S / 2))
            self.cell.shapes(li1).insert(pya.Box(xcor, ycor + Lver, -xcor, ycor+Lver/2+S / 2))
            self.cell.shapes(nsdm).insert(pya.Box(xcor, ycor, -xcor, ycor+Lver/2-S / 2))
            self.cell.shapes(nsdm).insert(pya.Box(xcor, ycor + Lver, -xcor, ycor+Lver/2+S / 2))
            N_Licon_hor = int(
                (-2 * xcor - 2 * Li_Encloses_Licon_Two_Sides + Licon_Spacing) / (Licon_Width_Length + Licon_Spacing))
            Remaining_Licon_hor = -2 * xcor - 2 * Li_Encloses_Licon_Two_Sides - N_Licon_hor * Licon_Width_Length - (
                    N_Licon_hor - 1) * Licon_Spacing

            N_Licon_ver = int(((Lver/2 - S / 2) - 2 * Li_Encloses_Licon_Two_Sides + Licon_Spacing) / (
                    Licon_Width_Length + Licon_Spacing))
            print(N_Licon_ver)
            Remaining_Licon_ver = (
                                          Lver/2 - S / 2) - 2 * Li_Encloses_Licon_Two_Sides - N_Licon_ver * Licon_Width_Length - (
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

            N_Mcon_ver = int(((Lver/2 - S / 2) - 2 * Met1_Encloses_Mcon_Two_Sides + Mcon_Spacing) / (
                    Mcon_Width_Length + Mcon_Spacing))
            Remaining_Mcon_ver = (Lver/2 - S / 2) - 2 * Met1_Encloses_Mcon_Two_Sides - N_Mcon_ver * Mcon_Width_Length - (
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
            ycor2 = input_distance
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
        y_check2=y_check-Lver/2-input_distance
        print(y_check2,"y_check2")
        if (-y_check2 * 2) >= (2 * S + 0.14):
            self.cell.shapes(met1).insert(pya.Box(xcor2, y_check + S, x_check, y_check-y_check2*2 - S))
            self.cell.shapes(met1).insert(pya.Box(xcor2 + Lhor, y_check + S, -x_check, y_check-y_check2*2 - S))
            if Shielding_with_diffusion == 1:
                self.cell.shapes(nwell).insert(pya.Box(xcor2, y_check + S, x_check, y_check-y_check2*2 - S))
                self.cell.shapes(nwell).insert(pya.Box(xcor2 + Lhor, y_check + S, -x_check, y_check-y_check2*2 - S))
                self.cell.shapes(li1).insert(pya.Box(xcor2, y_check + S, x_check, y_check-y_check2*2 - S))
                self.cell.shapes(li1).insert(pya.Box(xcor2 + Lhor, y_check + S, -x_check, y_check-y_check2*2 - S))
                self.cell.shapes(nsdm).insert(pya.Box(xcor2, y_check + S, x_check, y_check-y_check2*2 - S))
                self.cell.shapes(nsdm).insert(pya.Box(xcor2 + Lhor, y_check + S, -x_check, y_check-y_check2*2 - S))
                N_Licon_hor = int(((x_check - xcor2) - 2 * Li_Encloses_Licon_Two_Sides + Licon_Spacing) / (
                        Licon_Width_Length + Licon_Spacing))
                Remaining_Licon_hor = (
                                              x_check - xcor2) - 2 * Li_Encloses_Licon_Two_Sides - N_Licon_hor * Licon_Width_Length - (
                                              N_Licon_hor - 1) * Licon_Spacing

                N_Licon_ver = int((-y_check2 * 2 - 2 * S - 2 * Li_Encloses_Licon_Two_Sides + Licon_Spacing) / (
                        Licon_Width_Length + Licon_Spacing))
                Remaining_Licon_ver = -y_check2 * 2 - 2 * S - 2 * Li_Encloses_Licon_Two_Sides - N_Licon_ver * Licon_Width_Length - (
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

                N_Mcon_ver = int((-y_check2 * 2 - 2 * S - 2 * Met1_Encloses_Mcon_Two_Sides + Mcon_Spacing) / (
                        Mcon_Width_Length + Mcon_Spacing))
                Remaining_Mcon_ver = -y_check2 * 2 - 2 * S - 2 * Met1_Encloses_Mcon_Two_Sides - N_Mcon_ver * Mcon_Width_Length - (
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

    def draw_vias(self,x_start,y_start,x_end,y_end,via_number):
            l_via = self.layout.layer(via_lay_num, via_lay_dt)
            l_via2 = self.layout.layer(via2_lay_num, via2_lay_dt)
            l_via3 = self.layout.layer(via3_lay_num, via3_lay_dt)
            l_via4 = self.layout.layer(via4_lay_num, via4_lay_dt)
            persision = 1000

            dummy = y_start
            if y_start > y_end:
                y_start = y_end
                y_end = dummy

            dummy1 = x_start
            if x_start > x_end:
                x_start = x_end
                x_end = dummy1
            width = abs(y_end - y_start)
            length = abs(x_end - x_start)
            ru_dbu = 1000
            via_size = 0.15*persision
            via_spc = 0.17*persision
            met_via_enc_1 = 0.055*persision
            met_via_enc_2 = 0.085*persision
            via2_size = 0.2*persision
            via2_spc = 0.2*persision
            met_via2_enc_1 = 0.065 * persision
            met_via2_enc_2 = 0.085 * persision
            via3_size = 0.2*persision
            via3_spc = 0.2*persision
            met_via3_enc_1 = 0.065*persision
            met_via3_enc_2 = 0.09*persision
            via4_size = 0.8*persision
            via4_spc = 0.8*persision
            met_via4_enc = 0.310*persision
            AL_via = pya.Box(0, 0, via_size , via_size )
            AL_via2 = pya.Box(0, 0, via2_size, via2_size )
            AL_via3 = pya.Box(0, 0, via3_size , via3_size)
            AL_via4 = pya.Box(0, 0, via4_size, via4_size)



            if via_number== 1:
                via_cell = self.layout.create_cell("via")
                via_cell.shapes(l_via).insert(AL_via)
                num_via_1,via_free_spc_1 = self.number_spc_contacts(width,met_via_enc_1,via_spc,via_size)
                num_via_2,via_free_spc_2 = self.number_spc_contacts(length,met_via_enc_2,via_spc,via_size)
                via_arr = pya.CellInstArray(via_cell.cell_index(), pya.Trans(pya.Point(via_free_spc_2/2, -width/2+via_free_spc_1/2)),
                                  pya.Vector(via_spc+via_size, 0), pya.Vector(0, via_spc+via_size),num_via_2,num_via_1)

                self.cell.insert(via_arr)






                #self.cell.shapes(l_met2).insert(pya.Path([pya.Point(0, 0), pya.Point(length, 0)], width))
            if via_number == 2:
                via2_cell = self.layout.create_cell("via2")
                via2_cell.shapes(l_via2).insert(AL_via2)
                num_via2_1, via2_free_spc_1 = self.number_spc_contacts(width, met_via2_enc_1, via2_spc, via2_size)
                num_via2_2, via2_free_spc_2 = self.number_spc_contacts(length, met_via2_enc_2, via2_spc, via2_size)
                via2_arr = pya.CellInstArray(via2_cell.cell_index(), pya.Trans(
                    pya.Point(via2_free_spc_2 / 2, -width / 2 + via2_free_spc_1 / 2)),
                                            pya.Vector(via2_spc + via2_size, 0), pya.Vector(0, via2_spc + via2_size),
                                            num_via2_2, num_via2_1)

                self.cell.insert(via2_arr)
            if via_number== 3:
                via3_cell = self.layout.create_cell("via3")
                via3_cell.shapes(l_via3).insert(AL_via3)
                num_via3_1, via3_free_spc_1 = self.number_spc_contacts(width, met_via3_enc_1, via3_spc, via3_size)
                num_via3_2, via3_free_spc_2 = self.number_spc_contacts(length, met_via3_enc_2, via3_spc, via3_size)
                via3_arr = pya.CellInstArray(via3_cell.cell_index(), pya.Trans(
                    pya.Point(x_start+via3_free_spc_2 / 2, y_start + via3_free_spc_1 / 2)),
                                             pya.Vector(via3_spc + via3_size, 0),
                                             pya.Vector(0, via3_spc + via3_size),
                                             num_via3_2, num_via3_1)

                self.cell.insert(via3_arr)
                pass
            if via_number== 4:
                via4_cell = self.layout.create_cell("via4")
                via4_cell.shapes(l_via4).insert(AL_via4)
                num_via4_1, via4_free_spc_1 = self.number_spc_contacts(width, met_via4_enc, via4_spc, via4_size)
                num_via4_2, via4_free_spc_2 = self.number_spc_contacts(length, met_via4_enc, via4_spc, via4_size)
                via4_arr = pya.CellInstArray(via4_cell.cell_index(), pya.Trans(
                    pya.Point(x_start+via4_free_spc_2 / 2,y_start+ via4_free_spc_1 / 2)),
                                             pya.Vector(via4_spc + via4_size, 0),
                                             pya.Vector(0, via4_spc + via4_size),
                                             num_via4_2, num_via4_1)
                self.cell.insert(via4_arr)
    def roundto5 (self, number):
        number = round(number/5)
        return number*5

    def produce_impl(self):
        PERCISION = 1000
        if self.shielding == 1:
            self.rectangular_shielding(self.W_shielding,self.S_shielding,self.Louter,self.Louter,self.diffusion_shielding,self.distance_input)

        if self.shielding == 2:
            self.triangular_shielding(self.W_shielding,self.S_shielding,self.Louter,self.diffusion_shielding,self.distance_input)
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

        # Setting the parameters by the user
        self.cell_metal = met5  # the metal layer used by the inductor at the self.cell
        via_used_between_top_middle_metals = via4  # the via used between the self.cell and middle metal layers
        middle_metal = met4  # the metal layer used by the inductor at the diagonal conductors
        via_used_between_middle_bottom_metals = via3  # the via used between the middle and the bottom metal layers
        bottom_metal = met3  # the metal layer used by the inductor at the output inductors
        N = self.N # number of turns of the inductors
        W = self.W * PERCISION  # width of the conductors
        S = self.S * PERCISION  # spacing between the conductors
        Dist_input = self.distance_input * PERCISION  # the length of the conductor at the two input pairs
        Spacing_input = self.spacing_input * PERCISION  # the spacing between the conductors of the two input pairs
        Louter = self.Louter * PERCISION  # outer dimension of the inductor
        NumOfPoints = int(2 * ((4 * N) + 1))

        all_points_pos = []
        all_points_neg = []
        xcor = 0
        ycor = 0
        xpos = 1  # used to check the horizontal conductor will increase or decrease in xcor
        ypos = 1  # used to check the vertical   conductor will increase or decrease in ycor
        LouterCor = Louter

        for i in range(N):

            for j in range(4):  # 4 equals number of points in each half turn
                if j == 0:  # for the first point of the turn xcor is constant and ycor increases by S+W
                    xcor = Spacing_input / 2
                    ycor = Dist_input + (2 * i + 1) * (W / 2) + i * S
                elif j % 2 == 1:  # odd values of points will change xcor
                    if xpos == 1:  # imagine one turn if we want to draw the first horizontal side we increase x-axis value by the conductor length
                        xcor = xcor + (LouterCor / 2 - (2 * i) * S / 2 - (2 * i + 1) * W / 2 - Spacing_input / 2)
                        xpos = 0
                    else:  # the second horizontal side we decrease the value of x-axis
                        xcor = xcor - (LouterCor / 2 - (2 * i) * S / 2 - (2 * i + 1) * W / 2 - Spacing_input / 2)
                        xpos = 1
                else:  # even values of the point will change ycor
                    ycor = ycor + (LouterCor - (
                                2 * i + 1) * W - 2 * i * S)  # to draw the first vertical in each turn side we increase ycor
                xcor = self.roundto5(xcor)
                ycor = self.roundto5(ycor)
                PointCoordinatesPos = pya.Point(xcor, ycor)
                all_points_pos.append(PointCoordinatesPos)
                PointCoordinatesNeg = pya.Point(-xcor, ycor)
                all_points_neg.append(PointCoordinatesNeg)
            self.cell.shapes(met5).insert(pya.Path(all_points_pos, W))
            self.cell.shapes(met5).insert(pya.Path(all_points_neg, W))
            if i == N - 1:
                if N % 2 == 1:  # if the number of turns odd that means the common conductor is at the self.cell and draw the output
                    ycor = ycor + W / 2
                else:  # if the number of turns even that means the common conductor is at the bottom and draw the output
                    ycor = Dist_input + N * W + (N - 1) * S
                ycor = self.roundto5(ycor)
                self.cell.shapes(met5).insert(pya.Box(Spacing_input / 2, ycor, -Spacing_input / 2, ycor - W))
                self.cell.shapes(met3).insert(pya.Box(W / 2, 0, -W / 2, ycor))
                self.cell.shapes(met4).insert(pya.Box(W / 2, ycor - W, -W / 2, ycor))

                self.draw_vias(W / 2, ycor - W, -W / 2, ycor,3)
                self.draw_vias(W / 2, ycor - W, -W / 2, ycor,4)

                #self.cell.shapes(via4).insert(pya.Box(W / 2, ycor - W, -W / 2, ycor))
                #self.cell.shapes(via3).insert(pya.Box(W / 2, ycor - W, -W / 2, ycor))
            # if the number of turns greater than 1 we want to draw the cross shape
            elif i % 2 == 0:  # if the number of turn is even we draw the upper cross
                ycor = ycor + W / 2
                ycor = self.roundto5(ycor)

                #self.cell.shapes(via4).insert(pya.Box(Spacing_input / 2, ycor, Spacing_input / 2 + W, ycor - W))
                self.draw_vias(Spacing_input / 2, ycor, Spacing_input / 2 + W, ycor - W,4)
                ycor = ycor - W / 2
                ycor = self.roundto5(ycor)

                self.cell.shapes(met4).insert(
                    pya.Path([pya.Point(Spacing_input / 2 + W, ycor), pya.Point(Spacing_input / 2, ycor),
                              pya.Point(-Spacing_input / 2, ycor - W - S),
                              pya.Point(-Spacing_input / 2 - W, ycor - W - S)], W))
                ycor = ycor - S - W / 2
                ycor = self.roundto5(ycor)

                #self.cell.shapes(via4).insert(pya.Box(-Spacing_input / 2, ycor, -Spacing_input / 2 - W, ycor - W))
                self.draw_vias(-Spacing_input / 2, ycor, -Spacing_input / 2 - W, ycor - W,4)
                ycor = ycor - W / 2
                ycor = self.roundto5(ycor)

                self.cell.shapes(met5).insert(pya.Path(
                    [pya.Point(-Spacing_input / 2 - W, ycor + S + W), pya.Point(-Spacing_input / 2, ycor + W + S),
                     pya.Point(Spacing_input / 2, ycor),
                     pya.Point(Spacing_input / 2 + W, ycor)], W))
            else:  # if the number of turn is odd we draw the lower cross
                ycor = Dist_input + (i + 2) * W + (i + 1) * S
                ycor = self.roundto5(ycor)

                #self.cell.shapes(via4).insert(pya.Box(Spacing_input / 2, ycor, Spacing_input / 2 + W, ycor - W))
                self.draw_vias(Spacing_input / 2, ycor, Spacing_input / 2 + W, ycor - W,4)
                ycor = ycor - W / 2
                ycor = self.roundto5(ycor)

                self.cell.shapes(met4).insert(
                    pya.Path([pya.Point(Spacing_input / 2 + W, ycor), pya.Point(Spacing_input / 2, ycor),
                              pya.Point(-Spacing_input / 2, ycor - W - S),
                              pya.Point(-Spacing_input / 2 - W, ycor - W - S)], W))
                ycor = ycor - S - W / 2
                ycor = self.roundto5(ycor)

                #self.cell.shapes(via4).insert(pya.Box(-Spacing_input / 2, ycor, -Spacing_input / 2 - W, ycor - W))
                self.draw_vias(-Spacing_input / 2, ycor, -Spacing_input / 2 - W, ycor - W,4)
                ycor = ycor - W / 2
                ycor = self.roundto5(ycor)

                self.cell.shapes(met5).insert(
                    pya.Path(
                        [pya.Point(-Spacing_input / 2 - W, ycor + S + W), pya.Point(-Spacing_input / 2, ycor + W + S),
                         pya.Point(Spacing_input / 2, ycor),
                         pya.Point(Spacing_input / 2 + W, ycor)], W))

            # return to the original conditions
            LouterCor = LouterCor
            LouterCor = self.roundto5(LouterCor)
            all_points_pos = []
            all_points_neg = []
            xpos = 1

        self.cell.shapes(met5).insert(pya.Box(Spacing_input / 2, ycor, -Spacing_input / 2, ycor - W))

        self.cell.shapes(met5).insert(pya.Box(Spacing_input / 2, 0, Spacing_input / 2 + W, Dist_input))
        self.cell.shapes(met5).insert(pya.Box(-Spacing_input / 2, 0, -Spacing_input / 2 - W, Dist_input))



