"""
usage: from sky130_mapped import sky130_mapped_pdk
"""

from ..mappedpdk import MappedPDK, SetupPDKFiles
from ..sky130_mapped.grules import grulesobj
from pathlib import Path
from ..sky130_mapped.sky130_add_npc import sky130_add_npc
import os


# Actual Pin definations for Skywater 130nm from the PDK manual
# Ref: https://skywater-pdk.readthedocs.io/en/main/rules/layers.html#layers-definitions
LAYER = {
    "capm": (89, 44),
    "met4": (71, 20),
    "via3": (70, 44),
    "met3": (70, 20),
    "via2": (69, 44),
    "met2": (69, 20),
    "via" : (68, 44),
    "met1": (68, 20),
    "mcon": (67, 44),
    "li1": (67, 20),
    "licon1": (66, 44),
    "poly": (66, 20),
    "diff": (65, 20),
    "tap" : (65, 44),
    "nsdm": (93, 44),
    "psdm": (94, 20),
    "nwell": (64, 20),
    "pwell": (64, 44),
    "dnwell": (64, 18),
    ## _pin layer definations 
    # (Text type Pin definiaitons are not needed)
    #"met5_pin": (72, 16), # (Text and data) Not Needed
    "met4_pin": (71, 16), # (Text and data)
    "met3_pin": (70, 16), # (Text and data)
    "met2_pin": (69, 16), # (Text and data)
    "met1_pin": (68, 16), # (Text and data)
    "li1_pin": (67, 16), # (Text and data)
    "poly_pin": (66, 16), # (Text and data)
    "diff_pin": (65, 16), # (Text and data)
    #"nwell_pin": (64, 16), # (Text type)
    ##
    #"pad_pin": (76, 16), # (Text and data)
    #"pwell_pin": (122, 16), # (Text and data)
    #"pwelliso_pin": (44, 16), # (Text and data)
    ## _label layer definations
    #"met5_label": (72, 5), # (Text)
    "met4_label": (71, 5), # (Text)
    "met3_label": (70, 5), # (Text)
    "met2_label": (69, 5), # (Text)
    "met1_label": (68, 5), # (Text)
    "li1_label": (67, 5), # (Text)
    "poly_label": (66, 5), # (Text)
    "diff_label": (65, 6), # (Text)
    #"tap_label": (65, 5), #
    #"nwell_label": (64, 5), # (Text)
    ##
    #"pad_label": (76, 5), # (Text)
    #"pwell_label": (64,59), # (Text and data type)
    #"pwelliso_label": (44,5), # (Text)
   
}

sky130_glayer_mapping = {
    "capmet": "capm",
    "met5": "met4",
    "via4": "via3",
    "met4": "met3",
    "via3": "via2",
    "met3": "met2",
    "via2": "via",
    "met2": "met1",
    "via1": "mcon",
    "met1": "li1",
    "mcon": "licon1",
    "poly": "poly",
    "active_diff": "diff",
    "active_tap": "diff", #Wrong Because it should be tap
    "n+s/d": "nsdm",
    "p+s/d": "psdm",
    "nwell": "nwell",
    "pwell": (64,44), # This Layer defination donot exist in the PDK manual, See Pwell label
    "dnwell": "dnwell",
    # _pin layer ampping
    "met5_pin": "met4_pin",
    "met4_pin": "met3_pin",
    "met3_pin": "met2_pin",
    "met2_pin": "met1_pin",
    "met1_pin": "li1_pin",
    "poly_pin": "poly_pin",
    "active_diff_pin": "diff_pin",
    #"nwell_pin": "nwell_pin",
    #"pwell_pin": "pwell_pin",
    # _label layer mapping
    "met5_label": "met4_label",
    "met4_label": "met3_label",
    "met3_label": "met2_label",
    "met2_label": "met1_label",
    "met1_label": "li1_label",
    "poly_label": "poly_label",
    "active_diff_label": "diff_label",
    #"nwell_label": "nwell_label",
    #"pwell_label": "pwell_label",
    
}

openfasoc_dir = Path(__file__).resolve().parent.parent.parent.parent.parent.parent.parent
klayout_drc_file = Path(__file__).resolve().parent / "sky130.lydrc"
# pdk_root = Path('/usr/bin/miniconda3/share/pdk/')
#pdk_root = Path('/usr/bin/miniconda3/share/pdk/')
pdk_root = Path(os.getenv('PDK_ROOT'))
lvs_schematic_ref_file = openfasoc_dir / "common" / "platforms" / "sky130hd" / "cdl" / "sky130_fd_sc_hd.spice"
magic_drc_file = pdk_root / "sky130A" / "libs.tech" / "magic" / "sky130A.magicrc"
lvs_setup_tcl_file = pdk_root / "sky130A" / "libs.tech" / "netgen" / "sky130A_setup.tcl"
temp_dir = None

pdk_files = SetupPDKFiles(
    pdk_root=pdk_root,
    klayout_drc_file=klayout_drc_file,
    lvs_schematic_ref_file=lvs_schematic_ref_file,
    lvs_setup_tcl_file=lvs_setup_tcl_file,
    magic_drc_file=magic_drc_file,
    temp_dir=temp_dir,
    pdk='sky130'
).return_dict_of_files()


sky130_mapped_pdk = MappedPDK(
    name="sky130",
    glayers=sky130_glayer_mapping,
	models={
        'nfet': 'sky130_fd_pr__nfet_01v8',
		'pfet': 'sky130_fd_pr__pfet_01v8',
		'mimcap': 'sky130_fd_pr__cap_mim_m3_1'
    },
    layers=LAYER,
    grules=grulesobj,
    pdk_files=pdk_files,
    default_decorator=sky130_add_npc
)
# set the grid size
sky130_mapped_pdk.gds_write_settings.precision = 5*10**-9
sky130_mapped_pdk.cell_decorator_settings.cache=False
sky130_mapped_pdk.gds_write_settings.flatten_invalid_refs=False