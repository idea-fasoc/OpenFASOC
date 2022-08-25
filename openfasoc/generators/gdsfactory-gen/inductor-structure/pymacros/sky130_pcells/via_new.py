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
## Mabrains Company LLC
##
## Mabrains Via Generator for Skywaters 130nm
########################################################################################################################

from .imported_generators.layers_definiations import *
import pya
import math
import pandas as pd


"""
Mabrains Via Generator for Skywaters 130nm
"""



class Via_newGenerator(pya.PCellDeclarationHelper):
    """
    Mabrains Via Generator for Skywaters 130nm
    """
    layers = ["metal1","metal2","metal3","metal4","metal5"]


    def __init__(self):

        ## Initialize super class.
        super(Via_newGenerator, self).__init__()
        # declare the parameters
        #self.param("ls", self.TypeLayer, "Starting Layer", default=pya.LayerInfo(1, 0))
        #self.param("le", self.TypeLayer, "Ending Layer", default=pya.LayerInfo(1, 0))

        #self.param("metal", self.TypeString, "Choose metal type AL or CU", default="AL")

        starting_layer = self.param("starting_metal", self.TypeString, "choose the starting metal",default=-4)
        starting_layer.add_choice("Poly",-4)
        starting_layer.add_choice("Ptap", -3)
        starting_layer.add_choice("Ntap", -2)
        starting_layer.add_choice("li", -1)
        starting_layer.add_choice("metal1", 0)
        starting_layer.add_choice("metal2", 1)
        starting_layer.add_choice("metal3", 2)
        starting_layer.add_choice("metal4", 3)
        starting_layer.add_choice("metal5", 4)

        ending_layer = self.param("ending_metal",self.TypeString,"choose the ending material",default=-4)
        ending_layer.add_choice("ptap", -3)
        ending_layer.add_choice("Ntap", -2)
        ending_layer.add_choice("li", -1)
        ending_layer.add_choice("metal1",0)
        ending_layer.add_choice("metal2",1)
        ending_layer.add_choice("metal3",2)
        ending_layer.add_choice("metal4",3)
        ending_layer.add_choice("metal5",4)

        self.param("width", self.TypeDouble, "width", default=1)
        self.param("length", self.TypeDouble, "length", default=1)
        self.param("hv",self.TypeBoolean,"High Voltage works in case of ptap and ntap",default=False)

        
        #self.param("metal", self.TypeString, "Choose metal type AL or CU", default="AL")
        #self.param("via_type", self.TypeString, "Choose via type", default="via")

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
        return "via_array"

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


    def draw_metals(self,width,length,starting_metal,ending_metal):
        l_poly = self.layout.layer(poly_lay_num,poly_lay_dt)
        l_npc = self.layout.layer(npc_lay_num,npc_lay_dt)
        l_nsdm = self.layout.layer(nsdm_lay_num,nsdm_lay_dt)
        l_psdm = self.layout.layer(psdm_lay_num,psdm_lay_dt)
        l_nwell = self.layout.layer(nwell_lay_num,nwell_lay_dt)
        l_tap = self.layout.layer(tap_lay_num,tap_lay_dt)
        l_li = self.layout.layer(li_lay_num,li_lay_dt)
        l_met1 = self.layout.layer(met1_lay_num, met1_lay_dt)
        l_met2 = self.layout.layer(met2_lay_num, met2_lay_dt)
        l_met3 = self.layout.layer(met3_lay_num, met3_lay_dt)
        l_met4 = self.layout.layer(met4_lay_num, met4_lay_dt)
        l_met5 = self.layout.layer(met5_lay_num, met5_lay_dt)
        l_hvi =  self.layout.layer(hvi_lay_num,hvi_lay_dt)
        persision = 1000
        width = width * persision
        length = length * persision
        npsdm_enc_tap = 0.125*persision
        npc_enc = 0.1*persision
        poly_extension = 0.09*persision
        hv_enc_tap = 0.33*persision
        Pass = 0
        for metal in range(starting_metal,ending_metal+1):
            if metal == -4:
                self.cell.shapes(l_poly).insert(pya.Path([pya.Point(0, 0), pya.Point(length, 0)], width+2*poly_extension))
                self.cell.shapes(l_npc).insert(pya.Path([pya.Point(-npc_enc, 0), pya.Point(length+npc_enc, 0)], width+2*npc_enc))
                Pass = 1
            if metal == -3 and Pass != 1:
                self.cell.shapes(l_tap).insert(pya.Path([pya.Point(0, 0), pya.Point(length, 0)], width))
                self.cell.shapes(l_psdm).insert(pya.Path([pya.Point(-npsdm_enc_tap, 0), pya.Point(length+npsdm_enc_tap, 0)], width+2*npsdm_enc_tap))
                if self.hv :
                    self.cell.shapes(l_hvi).insert(pya.Path([pya.Point(-hv_enc_tap, 0), pya.Point(length+hv_enc_tap, 0)], width+2*hv_enc_tap))
                Pass = 1

            if metal == -2 and Pass != 1:
                self.cell.shapes(l_tap).insert(pya.Path([pya.Point(0, 0), pya.Point(length, 0)], width))
                self.cell.shapes(l_nsdm).insert(pya.Path([pya.Point(-npsdm_enc_tap, 0), pya.Point(length+npsdm_enc_tap, 0)], width+2*npsdm_enc_tap))
                self.cell.shapes(l_nwell).insert(pya.Path([pya.Point(-npsdm_enc_tap, 0), pya.Point(length+npsdm_enc_tap, 0)], width+2*npsdm_enc_tap))
                if self.hv :
                    self.cell.shapes(l_hvi).insert(pya.Path([pya.Point(-hv_enc_tap, 0), pya.Point(length+hv_enc_tap, 0)], width+2*hv_enc_tap))
                    self.cell.shapes(l_nwell).insert(pya.Path([pya.Point(-hv_enc_tap, 0), pya.Point(length+hv_enc_tap, 0)], width+2*hv_enc_tap))
                else :
                    self.cell.shapes(l_nwell).insert(pya.Path([pya.Point(-npsdm_enc_tap, 0), pya.Point(length+npsdm_enc_tap, 0)], width+2*npsdm_enc_tap))

            if metal == -1:
                self.cell.shapes(l_li).insert(pya.Path([pya.Point(0, 0), pya.Point(length, 0)], width))

            if metal == 0 :
                self.cell.shapes(l_met1).insert(pya.Path([pya.Point(0, 0),pya.Point(length,0)],width))
            if metal == 1:
                self.cell.shapes(l_met2).insert(pya.Path([pya.Point(0, 0),pya.Point(length,0)],width))
            if metal == 2:
                self.cell.shapes(l_met3).insert(pya.Path([pya.Point(0, 0),pya.Point(length,0)],width))
            if metal == 3:
                self.cell.shapes(l_met4).insert(pya.Path([pya.Point(0, 0),pya.Point(length,0)],width))
            if metal == 4:
                self.cell.shapes(l_met5).insert(pya.Path([pya.Point(0, 0), pya.Point(length, 0)], width))

        self.cell.flatten(1)


    def draw_vias(self,width,length,starting_metal,ending_metal):
            l_licon = self.layout.layer(licon_lay_num, licon_lay_dt)
            l_mcon = self.layout.layer(mcon_lay_num, mcon_lay_dt)
            l_via = self.layout.layer(via_lay_num, via_lay_dt)
            l_via2 = self.layout.layer(via2_lay_num, via2_lay_dt)
            l_via3 = self.layout.layer(via3_lay_num, via3_lay_dt)
            l_via4 = self.layout.layer(via4_lay_num, via4_lay_dt)
            persision = 1000
            width = width * persision
            length = length * persision
            ru_dbu = 1000
            licon_size = 0.17*persision
            licon_spc = 0.17*persision
            met_licon_enc_1 = 0.04*persision
            met_licon_enc_2 = 0.12*persision
            mcon_size = 0.17*persision
            mcon_spc = 0.19*persision
            met_mcon_enc_1 = 0.03*persision
            met_mcon_enc_2 = 0.06*persision
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
            licon_Via = pya.Box(0, 0, licon_size , licon_size )
            AL_via = pya.Box(0, 0, via_size , via_size )
            AL_via2 = pya.Box(0, 0, via2_size, via2_size )
            AL_via3 = pya.Box(0, 0, via3_size , via3_size)
            AL_via4 = pya.Box(0, 0, via4_size, via4_size)
            if self.layout.cell("licon") == None :
                licon_cell = self.layout.create_cell("licon")
            else:
                licon_cell = self.layout.cell("licon")
            if self.layout.cell("mcon") == None :
                mcon_cell = self.layout.create_cell("mcon")
            else:
                mcon_cell = self.layout.cell("mcon")
            if self.layout.cell("via") == None:
                via_cell = self.layout.create_cell("via")
            else:
                via_cell = self.layout.cell("via")
            if self.layout.cell("via2") == None:
                via2_cell = self.layout.create_cell("via2")
            else:
                via2_cell = self.layout.cell("via2")
            if self.layout.cell("via3") == None:
                via3_cell = self.layout.create_cell("via3")
            else:
                via3_cell = self.layout.cell("via3")
            if self.layout.cell("via4") == None:
                via4_cell = self.layout.create_cell("via4")
            else:
                via4_cell = self.layout.cell("via4")
            if starting_metal == -4:
                met_licon_enc_1 = 0.05*persision
                met_licon_enc_2 = 0.08*persision
            for i in range(starting_metal, ending_metal):
                if i == -2:
                    
                    licon_cell.shapes(l_licon).insert(licon_Via)
                    num_licon_1, licon_free_spc_1 = self.number_spc_contacts(width, met_licon_enc_1, licon_spc, licon_size)
                    num_licon_2, licon_free_spc_2 = self.number_spc_contacts(length, met_licon_enc_2, licon_spc, licon_size)
                    licon_arr = pya.CellInstArray(licon_cell.cell_index(), pya.Trans(
                        pya.Point(licon_free_spc_2 / 2, -width / 2 + licon_free_spc_1 / 2)),
                                                pya.Vector(licon_spc + licon_size, 0), pya.Vector(0, licon_spc + licon_size),
                                                num_licon_2, num_licon_1)

                    self.cell.insert(licon_arr)
                    # licon_cell.clear() 

                if i == -1:
                    
                    mcon_cell.shapes(l_mcon).insert(licon_Via)
                    num_mcon_1, mcon_free_spc_1 = self.number_spc_contacts(width, met_mcon_enc_1, mcon_spc, mcon_size)
                    num_mcon_2, mcon_free_spc_2 = self.number_spc_contacts(length, met_mcon_enc_2, mcon_spc, mcon_size)
                    mcon_arr = pya.CellInstArray(mcon_cell.cell_index(), pya.Trans(
                        pya.Point(mcon_free_spc_2 / 2, -width / 2 + mcon_free_spc_1 / 2)),
                                                pya.Vector(mcon_spc + mcon_size, 0), pya.Vector(0, mcon_spc + mcon_size),
                                                num_mcon_2, num_mcon_1)

                    self.cell.insert(mcon_arr)
                    # mcon_cell.delete()
                if i == 0:
                    
                    via_cell.shapes(l_via).insert(AL_via)
                    num_via_1,via_free_spc_1 = self.number_spc_contacts(width,met_via_enc_1,via_spc,via_size)
                    num_via_2,via_free_spc_2 = self.number_spc_contacts(length,met_via_enc_2,via_spc,via_size)
                    via_arr = pya.CellInstArray(via_cell.cell_index(), pya.Trans(pya.Point(via_free_spc_2/2, -width/2+via_free_spc_1/2)),
                                      pya.Vector(via_spc+via_size, 0), pya.Vector(0, via_spc+via_size),num_via_2,num_via_1)

                    self.cell.insert(via_arr)
                    # via_cell.delete()






                    #self.cell.shapes(l_met2).insert(pya.Path([pya.Point(0, 0), pya.Point(length, 0)], width))
                if i == 1:
                    
                    via2_cell.shapes(l_via2).insert(AL_via2)
                    num_via2_1, via2_free_spc_1 = self.number_spc_contacts(width, met_via2_enc_1, via2_spc, via2_size)
                    num_via2_2, via2_free_spc_2 = self.number_spc_contacts(length, met_via2_enc_2, via2_spc, via2_size)
                    via2_arr = pya.CellInstArray(via2_cell.cell_index(), pya.Trans(
                        pya.Point(via2_free_spc_2 / 2, -width / 2 + via2_free_spc_1 / 2)),
                                                pya.Vector(via2_spc + via2_size, 0), pya.Vector(0, via2_spc + via2_size),
                                                num_via2_2, num_via2_1)

                    self.cell.insert(via2_arr)
                    # via2_cell.delete()
                if i == 2:
                    
                    via3_cell.shapes(l_via3).insert(AL_via3)
                    num_via3_1, via3_free_spc_1 = self.number_spc_contacts(width, met_via3_enc_1, via3_spc, via3_size)
                    num_via3_2, via3_free_spc_2 = self.number_spc_contacts(length, met_via3_enc_2, via3_spc, via3_size)
                    via3_arr = pya.CellInstArray(via3_cell.cell_index(), pya.Trans(
                        pya.Point(via3_free_spc_2 / 2, -width / 2 + via3_free_spc_1 / 2)),
                                                 pya.Vector(via3_spc + via3_size, 0),
                                                 pya.Vector(0, via3_spc + via3_size),
                                                 num_via3_2, num_via3_1)

                    self.cell.insert(via3_arr)
                    # via3_cell.delete()
                    pass
                if i == 3:
                    
                    via4_cell.shapes(l_via4).insert(AL_via4)
                    num_via4_1, via4_free_spc_1 = self.number_spc_contacts(width, met_via4_enc, via4_spc, via4_size)
                    num_via4_2, via4_free_spc_2 = self.number_spc_contacts(length, met_via4_enc, via4_spc, via4_size)
                    via4_arr = pya.CellInstArray(via4_cell.cell_index(), pya.Trans(
                        pya.Point(via4_free_spc_2 / 2, -width / 2 + via4_free_spc_1 / 2)),
                                                 pya.Vector(via4_spc + via4_size, 0),
                                                 pya.Vector(0, via4_spc + via4_size),
                                                 num_via4_2, num_via4_1)
                    self.cell.insert(via4_arr)
                    # via4_cell.delete()

            # via_cell.clear()
            # self.cell.flatten(1)

            self.layout.convert_cell_to_static(licon_cell.cell_index())
            self.layout.convert_cell_to_static(mcon_cell.cell_index())
            self.layout.convert_cell_to_static(via_cell.cell_index())
            self.layout.convert_cell_to_static(via2_cell.cell_index())
            self.layout.convert_cell_to_static(via3_cell.cell_index())
            self.layout.convert_cell_to_static(via4_cell.cell_index())


            
                



    def produce_impl(self):


        # compute the circle
        #pts = []
        #da = math.pi * 2 / 4
        #for i in range(0, 4):
        #pts.append(pya.Point.from_dpoint(pya.DPoint(ru_dbu * math.cos(i * da), ru_dbu * math.sin(i * da))))
        #self.cell.shapes(l_met1).insert(pya.Box(0,0,self.width,self.height))
        # create the shape
        self.draw_metals(self.width,self.length,self.starting_metal,self.ending_metal)
        self.draw_vias(self.width,self.length,self.starting_metal,self.ending_metal)
        self.cell.flatten(1)
        self.layout.cleanup()
        
        



        print(self.ending_metal)
        #CU_via = pya.Box(0,0,0.18*ru_dbu,0.18*ru_dbu)
        # if self.metal == "CU":
        #     self.cell.shapes(l_via).insert(CU_via)
        # else:
        #     if self.via_type == "via":
        #         self.cell.shapes(l_via).insert(AL_via)
        #     elif self.via_type == "via2":
        #         self.cell.shapes(l_via2).insert(AL_via2)
        #     elif self.via_type == "via3":
        #         self.cell.shapes(l_via3).insert(AL_via3)
        #     else :
        #         self.cell.shapes(l_via4).insert(AL_via4)



