"""
usage: from sky130_mapped import sky130_mapped_pdk
"""
import sky130

# import mappedpdk from the main pdk dir (parent of this dir)
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from mappedpdk import MappedPDK


sky130_glayer_mapping = {
	"met4":"met3drawing",
	"via3":"via2drawing",
	"met3":"met2drawing",
	"via2":"viadrawing",
	"met2":"met1drawing",
	"via1":"mcondrawing",
	"met1":"li1drawing",
	"mcon":"licon1drawing",
	
	"poly":"polydrawing",
	"active":"diffdrawing",
	"n+s/d":"nsdmdrawing",
	"p+s/d":"psdmdrawing",
	"nwell":"nwelldrawing",
	"pwell":"pwelldrawing",
	"dnwell":"dnwelldrawing",
	}


sky130_mapped_pdk = MappedPDK.from_gf_pdk(sky130.PDK, sky130_glayer_mapping)

