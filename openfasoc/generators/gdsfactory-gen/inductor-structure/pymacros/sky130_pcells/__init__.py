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
## Mabrains Pcells Generators for Klayout for Skywaters 130nm
########################################################################################################################

import pya

# from .via import ViaGenerator
from .via_new import Via_newGenerator
from .nmos18 import NMOS18
from .pmos18 import PMOS18
from .polyres import PolyRes_gen
from .inductor import IndGenerator
from .rectangular_shielding import rectangular_shielding_Generator
from .triangular_shielding import triangular_shielding_Generator
from .diff_square_inductor import diff_squar_ind_Generator
from .single_octagon_ind import single_octagon_ind_Generator
from .new_single_octagon_ind import new_single_octagon_Generator
from .diff_octagon import diff_octagon_ind_Generator
from .nmos5d10 import nmos5d10_gen
from .pmos5d10 import pmos5d10_gen
from .mimcap_1 import mimcap_1_gen
from .mimcap_2 import mimcap_2_gen
from .pnp_gen import pnp_bjt


from .layers_definiations import *

class Sky130(pya.Library):
    """
    The library where we will put the PCell into
    """

    def __init__(self):
        # Set the description
        self.description = "Skywaters 130nm Pcells"

        # Create the PCell declarations
        # self.layout().register_pcell("via", ViaGenerator())
        self.layout().register_pcell("via_new", Via_newGenerator())
        self.layout().register_pcell("nmos18", NMOS18())
        self.layout().register_pcell("pmos18", PMOS18())
        self.layout().register_pcell("poly_res", PolyRes_gen())
        self.layout().register_pcell("inductor", IndGenerator())
        self.layout().register_pcell("rectangular_shielding", rectangular_shielding_Generator())
        self.layout().register_pcell("triangular_shielding", triangular_shielding_Generator())
        self.layout().register_pcell("diff_square_inductor", diff_squar_ind_Generator())
        self.layout().register_pcell("diff_octagon_inductor", diff_octagon_ind_Generator())
        self.layout().register_pcell("single_octagon_ind", single_octagon_ind_Generator())
        self.layout().register_pcell("new_single_octagon_ind", new_single_octagon_Generator())
        self.layout().register_pcell("nmos5d10", nmos5d10_gen())
        self.layout().register_pcell("pmos5d10", pmos5d10_gen())
        self.layout().register_pcell("mimcap_1", mimcap_1_gen())
        self.layout().register_pcell("mimcap_2", mimcap_2_gen())
        self.layout().register_pcell("BNB BJT", pnp_bjt())










        # Register us with the name "MyLib".
        self.register("SKY130")
