"""
usage: from gf180_mapped import gf180_mapped_pdk
"""

from ..gf180_mapped.grules import grulesobj
from ..mappedpdk import MappedPDK, SetupPDKFiles
from pathlib import Path
import gdsfactory.config as gf_config

# Actual Pin definations for GlobalFoundries 180nmMCU from the PDK manual
# Ref: https://gf180mcu-pdk.readthedocs.io/en/latest/

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
    "CAP_MK": (117, 5),
    # _Label Layer Definations
    "metal5_label": (81,10),
    "metal4_label": (46,10),
    "metal3_label": (42,10),
    "metal2_label": (36,10),
    "metal1_label": (34,10),
    "poly2_label": (30,10),
    "comp_label": (22,10),
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
    "capmet": "CAP_MK",
    # _pin layer ampping
    "met5_pin": "metal5_label",
    "met4_pin": "metal4_label",
    "met3_pin": "metal3_label",
    "met2_pin": "metal2_label",
    "met1_pin": "metal1_label",
    "poly_pin": "poly2_label",
    "active_diff_pin": "comp_label",
    # _label layer mapping
    "met5_label": "metal5_label",
    "met4_label": "metal4_label",
    "met3_label": "metal3_label",
    "met2_label": "metal2_label",
    "met1_label": "metal1_label",
    "poly_label": "poly2_label",
    "active_diff_label": "comp_label",
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
        "nfet": "nfet_03v3",
        "pfet": "pfet_03v3",
        "mimcap": "mimcap_1p0fF",
    },
    layers=LAYER,
    pdk_files=pdk_files,
    grules=grulesobj,
)

# set grid size and propagate to gdsfactory config if not already defined
gf180_mapped_pdk.grid_size = 1e-3
if not hasattr(gf_config.CONF, "grid_size"):
    object.__setattr__(gf_config.CONF, "grid_size", gf180_mapped_pdk.grid_size)

# configure gds settings
gf180_mapped_pdk.gds_write_settings.precision = 5*10**-9
# Note: cache setting removed - gdsfactory 7.16.0+ handles caching differently
