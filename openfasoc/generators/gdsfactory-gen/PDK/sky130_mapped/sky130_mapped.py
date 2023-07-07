"""
usage: from sky130_mapped import sky130_mapped_pdk
"""
import sky130

from PDK.mappedpdk import MappedPDK
from PDK.sky130_mapped.grules import grulesobj
from pathlib import Path

sky130.PDK.layers["capm3"] = (89, 44)

# use mimcap over metal 3
sky130_glayer_mapping = {
    "capmet": "capm3",
    "met5": "met4drawing",
    "via4": "via3drawing",
    "met4": "met3drawing",
    "via3": "via2drawing",
    "met3": "met2drawing",
    "via2": "viadrawing",
    "met2": "met1drawing",
    "via1": "mcondrawing",
    "met1": "li1drawing",
    "mcon": "licon1drawing",
    "poly": "polydrawing",
    "active_diff": "diffdrawing",
    "active_tap": "tapdrawing",
    "n+s/d": "nsdmdrawing",
    "p+s/d": "psdmdrawing",
    "nwell": "nwelldrawing",
    "pwell": "pwelldrawing",
    "dnwell": "dnwelldrawing",
}


sky130_lydrc_file_path = Path(__file__).resolve().parent / "sky130.lydrc"


sky130_mapped_pdk = MappedPDK.from_gf_pdk(
    sky130.PDK,
    glayers=sky130_glayer_mapping,
    grules=grulesobj,
    klayout_lydrc_file=sky130_lydrc_file_path,
)
# set the grid size
sky130_mapped_pdk.gds_write_settings.precision = 5*10**-9
sky130_mapped_pdk.cell_decorator_settings.cache=False
