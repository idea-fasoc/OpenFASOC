"""
usage: from gf180_mapped import gf180_mapped_pdk
"""

from gf180.layers import LAYER  # , LAYER_VIEWS
from ..gf180_mapped.grules import grulesobj
from ..mappedpdk import MappedPDK
from pathlib import Path

LAYER = LAYER.dict()
#LAYER["fusetop"]=(75, 0)
LAYER["CAP_MK"] = (117,5)

gf180_glayer_mapping = {
    "met5": "metal5",
    "via4": "via4",
    "met4": "metal4",
    "via3": "via3",
    "met3": "metal3",
    "via2": "via2",
    "met2": "metal2",
    "via1": "via1",
    "met1": "metal1",
    "mcon": "contact",
    "poly": "poly2",
    "active_diff": "comp",
    "active_tap": "comp",
    "n+s/d": "nplus",
    "p+s/d": "pplus",
    "nwell": "nwell",
    "pwell": "lvpwell",
    "dnwell": "dnwell",
    "capmet": "CAP_MK"
}

# note for DRC, there is mim_option 'A'. This is the one configured for use

gf180_lydrc_file_path = Path(__file__).resolve().parent / "gf180mcu_drc.lydrc"


gf180_mapped_pdk = MappedPDK(
    name="gf180",
    glayers=gf180_glayer_mapping,
	models={
        'nfet': 'nfet_03v3',
		'pfet': 'pfet_03v3',
		'mimcap': 'mimcap_1p0fF'
    },
    layers=LAYER,
    klayout_lydrc_file=gf180_lydrc_file_path,
    grules=grulesobj,
)

# configure the grid size and other settings
gf180_mapped_pdk.gds_write_settings.precision = 5*10**-9
gf180_mapped_pdk.cell_decorator_settings.cache=False
