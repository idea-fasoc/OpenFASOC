"""
usage: from gf180_mapped import gf180_mapped_pdk
"""

from ..gf180_mapped.grules import grulesobj
from ..mappedpdk import MappedPDK, SetupPDKFiles
from pathlib import Path


#LAYER["fusetop"]=(75, 0)
LAYER = {
    "metal5": (81, 0),
    "via4": (41, 0),
    "metal4": (46, 0),
    "via3": (40, 0),
    "metal3": (42, 0),
    "via2": (38, 0),
    "metal2": (36, 0),
    "via1": (35, 0),
    "metal1": (34, 0),
    "contact": (33, 0),
    "poly2": (30, 0),
    "comp": (22, 0),
    "nplus": (32, 0),
    "pplus": (31, 0),
    "nwell": (21, 0),
    "lvpwell": (204, 0),
    "dnwell": (12, 0),
    "CAP_MK": (117, 5)
}

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

openfasoc_dir = Path(__file__).resolve().parent.parent.parent.parent.parent.parent.parent
pdk_root = Path('/usr/bin/miniconda3/share/pdk/')
lvs_schematic_ref_file = openfasoc_dir / "common" / "platforms" / "gf180osu9t" / "cdl" / "gf180mcu_osu_sc_9T.spice"
magic_drc_file = pdk_root / "gf180mcuC" / "libs.tech" / "magic" / "gf180mcuC.magicrc"
lvs_setup_tcl_file = pdk_root / "gf180mcuC" / "libs.tech" / "netgen" / "gf180mcuC_setup.tcl"
temp_dir = None


pdk_files = SetupPDKFiles(
    pdk_root=pdk_root,
    klayout_drc_file=gf180_lydrc_file_path,
    lvs_schematic_ref_file=lvs_schematic_ref_file,
    lvs_setup_tcl_file=lvs_setup_tcl_file,
    magic_drc_file=magic_drc_file,
    temp_dir=temp_dir,
    pdk='gf180'
).return_dict_of_files()

gf180_mapped_pdk = MappedPDK(
    name="gf180",
    glayers=gf180_glayer_mapping,
	models={
        'nfet': 'nfet_03v3',
		'pfet': 'pfet_03v3',
		'mimcap': 'mimcap_1p0fF'
    },
    layers=LAYER,
    pdk_files=pdk_files,
    grules=grulesobj,
)

# configure the grid size and other settings
gf180_mapped_pdk.gds_write_settings.precision = 5*10**-9
gf180_mapped_pdk.cell_decorator_settings.cache=False
