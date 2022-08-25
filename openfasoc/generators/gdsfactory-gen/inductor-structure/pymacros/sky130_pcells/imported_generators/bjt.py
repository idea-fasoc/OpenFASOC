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
########################################################################################################################


import pya
import nmos18 as nmos
from .layers_definiations import *
import os
repo_path = os.environ['automation_repo']
gds_path = repo_path+"/generators/klayout/"
class bjt(nmos.nmos18_device):
    
    n_well_diffusion_spacing = 0.34
    tap_width = 0.26

    def __init__(self, layout, device_name,guard_ring = 1):
        self.layout = layout
        self.device_name = device_name
        self.percision = 1/layout.dbu
        self.l_guard = self.layout.layer(
            psdm_lay_num, psdm_lay_dt)

        self.gr = guard_ring

    def add_labels (self):
        pass

    

    def draw_bjt(self):
        if self.device_name == "npn_w1_l1":
            self.layout.read(gds_path+self.device_name+".gds")
            self.cell_name = "sky130_fd_pr__rf_npn_05v5_W1p00L1p00"
        elif self.device_name == "npn_w1_l2":
            self.layout.read(gds_path+self.device_name+".gds")
            self.cell_name = "sky130_fd_pr__rf_npn_05v5_W1p00L2p00"

        enlarge_value = int((bjt.n_well_diffusion_spacing +
                         bjt.tap_width/2)*self.percision)
        self.bjt_bbox = self.layout.cell(self.cell_name).bbox().enlarge(enlarge_value,enlarge_value)
        # print('--->',(self.bjt_bbox.p1.x-1000*enlarge_value)/self.percision)
        # print('--->',self.bjt_bbox.p1.x-1*enlarge_value)
        if self.gr:
            self.draw_guard_ring(layout=self.layout,
                                x=(self.bjt_bbox.p1.x),
                                y=(self.bjt_bbox.p1.y),
                                guard_width=self.bjt_bbox.width()/self.percision,
                                guard_height=self.bjt_bbox.height()/self.percision,
                                tap_width=bjt.tap_width, cell=self.layout.cell(self.cell_name),
                                precision=self.percision)

        return self.layout.cell(self.cell_name)


