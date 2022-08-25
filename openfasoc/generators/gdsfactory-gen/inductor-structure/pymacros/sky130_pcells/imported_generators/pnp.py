########################################################################################################################
##
# Mabrains Company LLC ("Mabrains Company LLC") CONFIDENTIAL
##
# Copyright (C) 2018-2021 Mabrains Company LLC <contact@mabrains.com>
##
# This file is authored by:
#           - <Mina Maksimous> <mina_maksimous@mabrains.com>
##
########################################################################################################################


import pya

from .layers_definiations import *
import os
USER = os.environ['USER']
gds_path = "/home/"+USER+"/.klayout/tech/sky130/pymacros/sky130_pcells/imported_generators/"

class pnp():

    def __init__(self, layout, device_name):
        self.layout = layout
        self.percision = 1/layout.dbu
        self.device_name = device_name

    def add_labels(self):
        pass

    def draw_pnp(self):
        if self.device_name == "pnp_w3p4_l3p4":
            self.layout.read( gds_path +
                             self.device_name+".gds")
            self.cell_name = "sky130_fd_pr__rf_pnp_05v5_W3p40L3p40"
        elif self.device_name == "pnp_w0p68_l0p68":
            self.layout.read( gds_path +
                             self.device_name+".gds")
            self.cell_name = "sky130_fd_pr__rf_pnp_05v5_W0p68L0p68"
        return self.layout.cell(self.cell_name)
