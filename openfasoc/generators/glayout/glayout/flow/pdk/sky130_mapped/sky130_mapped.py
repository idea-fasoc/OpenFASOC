"""
usage: from sky130_mapped import sky130_mapped_pdk
"""

from ..mappedpdk import MappedPDK, SetupPDKFiles
from ..sky130_mapped.grules import grulesobj
from pathlib import Path
from ..sky130_mapped.sky130_add_npc import sky130_add_npc

# use mimcap over metal 3
sky130_glayer_mapping = {
    "capmet": (89, 44),
    "met5": (71,20),
    "via4": (70,44),
    "met4": (70,20),
    "via3": (69,44),
    "met3": (69,20),
    "via2": (68,44),
    "met2": (68,20),
    "via1": (67,44),
    "met1": (67,20),
    "mcon": (66,44),
    "poly": (66,20),
    "active_diff": (65,20),
    "active_tap": (65,20),
    "n+s/d": (93,44),
    "p+s/d": (94,20),
    "nwell": (64,20),
    "pwell": (64,44),
    "dnwell": (64,18),
}

openfasoc_dir = Path(__file__).resolve().parent.parent.parent.parent.parent.parent.parent

klayout_drc_file = Path(__file__).resolve().parent / "sky130.lydrc"
pdk_root = Path('/usr/bin/miniconda3/share/pdk/')
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
    grules=grulesobj,
    pdk_files=pdk_files,
    default_decorator=sky130_add_npc
)
# set the grid size
sky130_mapped_pdk.gds_write_settings.precision = 5*10**-9
sky130_mapped_pdk.cell_decorator_settings.cache=False
sky130_mapped_pdk.gds_write_settings.flatten_invalid_refs=False