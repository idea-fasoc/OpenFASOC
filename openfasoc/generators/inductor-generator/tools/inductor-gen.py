import pya
import os, sys
import gdsfactory as gf
import sky130
import argparse
import pdb
import yaml
from sky130.layers import LAYER, LAYER_COLORS, LAYER_STACK
from sky130 import cells as sky130_cells
from sky130 import tech as sky130_tech

parser = argparse.ArgumentParser(description="Inductor Generator")
parser.add_argument("--spec_file", required=True)
parser.add_argument("--output_dir", required=False, default="outputs")

args = parser.parse_args()
# Pass Specs to the script when decided (Can wrap into Makefile if needed)
spec_file = open(args.spec_file, "r")
tdict = yaml.load(spec_file)

# -------------------------------------------------------------------------------
# Import Sky130 pcells (ATTN SAI Where should these reside, they might not be pip installable yet
# -------------------------------------------------------------------------------
# MABRAINS github repo
technology_macros_path = os.path.abspath(
    "/home/chandru/Tools/sky130_klayout_pdk/pymacros/"
)
# Skywater 130 gdsfactory repo
gdsfactory_sky130_tech_path = os.path.dirname("/home/chandru/Tools/skywater130/sky130")
sys.path.append(technology_macros_path)
sys.path.append(gdsfactory_sky130_tech_path)

from sky130_pcells import Sky130

# -------------------------------------------------------------------------------
# createPCellInstance
# -------------------------------------------------------------------------------
def createPCellInstance(
    layout, pcell_name="CIRCLE", lib_name="Basic", params={}, x=0, y=0
):
    # Get PCell Library
    lib = pya.Library.library_by_name(lib_name)
    # The PCell Declaration. This one will create PCell variants.
    pcell_decl = lib.layout().pcell_declaration(pcell_name)

    # Get the top cell. Assuming only one top cell exists
    top_cell = layout.top_cell()

    # translate to array (to pv)
    pv = []
    for p in pcell_decl.get_parameters():
        if p.name in params:
            pv.append(params[p.name])
        else:
            pv.append(p.default)

    # create the PCell variant cell
    pcell_var = layout.add_pcell_variant(lib, pcell_decl.id(), pv)

    # Insert first instances
    # Need multiplication by database units
    top_cell.insert(
        pya.CellInstArray(pcell_var, pya.Trans(pya.Trans.R0, x * 1e3, y * 1e3))
    )

    ## Insert & move the second instance (Move so we can see it)
    # top_cell.insert(pya.CellInstArray(pcell_var,pya.Trans(1000,2000)))


# -------------------------------------------------------------------------------
# printPcellParams
# -------------------------------------------------------------------------------


def printPcellParams(layout, pcell_name="CIRCLE", lib_name="Basic"):
    # Get PCell Library
    lib = pya.Library.library_by_name(lib_name)

    # The PCell Declaration. This one will create PCell variants.
    pcell_decl = lib.layout().pcell_declaration(pcell_name)

    print(
        "The following Parameters are found in the Pcell: ",
        pcell_name,
        " Library",
        lib_name,
    )

    # Print all Parameters in the Pcell
    for p in pcell_decl.get_parameters():
        print("Parameter : ", p.name, " Default: ", p.default)


# -------------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------------

# create a layout
layout = pya.Layout()
top = layout.create_cell("TOP")
# Can pass params to the name of gds to maintain many cells parallely
output_file = "inductor_cell.gds"

# load the sky130 pcells
Sky130()
print("## Skywaters 131nm PDK Pcells loaded.")
# Inductor
# ------------

# ------------------
# Octagon Inductor
# ------------------
# Instantiate an inductor

# printPcellParams(layout, 'inductor', 'SKY130')

inductor_params = {
    "N": 8,
    "W": 5,
    "S": 3.5,
    "distance_input": 30,
    "spacing_input": 15,
    "Louter": 200,
    "shielding": 200,
    "W_shielding": 2,
    "S_shielding": 4,
    "diffusion_shielding": 0,
}

printPcellParams(layout, "diff_octagon_inductor", "SKY130")

createPCellInstance(
    layout=layout,
    pcell_name="diff_octagon_inductor",
    lib_name="SKY130",
    params=inductor_params,
    x=0,
    y=0,
)

# createPCellInstance(layout=layout, pcell_name='diff_square_inductor', lib_name='SKY130', params=inductor_params, x=300,
#                    y=0)
#
# createPCellInstance(layout=layout, pcell_name='inductor', lib_name='SKY130', params=inductor_params, x=500,
#                    y=0)


params_via = {"starting_metal": 3, "ending_metal": 4, "width": 100, "length": 100}

layout.write(output_file)

# VIA DROP USING MABRAIN PCELL if Needed
# p_n_spacing = 8
# for i in range(5):
#    createPCellInstance(layout=layout, pcell_name='via_new', lib_name='SKY130', params=params_via, x=-290+(120*i), y=-100)
# createPCellInstance(layout=layout, pcell_name='via_new', lib_name='SKY130', params=params_via, x=+60+(i*120), y=-100)

# --------------------------------------------------------------------------------------------
# Write Output of Inductor to gds to be read back in to connect the design in gdsfactory
# --------------------------------------------------------------------------------------------
# Read GDS Input
add_ports_m5 = gf.partial(
    gf.add_ports.add_ports_from_labels,
    port_layer=LAYER.met5drawing,
    layer_label=LAYER.met5label,
    port_type="electrical",
    port_width=0.2,
    get_name_from_label=True,
    guess_port_orientation=True,
)
inductor_in = gf.import_gds(
    output_file, cellname="diff_octagon_inductor", decorator=add_ports_m5, flatten=False
)
# for shp in inductor_in.paths:
#    print(shp.points)
#    #print(shp)

# exit()
# Create Top level Component
pad = gf.Component("Octagon Ind with GSGSG Pads")
pad1 = gf.components.pad(size=(100, 100), layer="met5drawing")
# Created a Pad Array
pt = pad << gf.components.pad_array(
    orientation=270, columns=5, spacing=(120.0, 0.0), pad=pad1
)
# Instantiate Inductor in component
lc = pad << inductor_in
# Move Inductor
lc_xoffset = 240
lc.move([(0 + lc_xoffset), 100])
# TODO Need to Figure out the placement of Ports for the ind cells
# lc_out = inductor_in.add_port(name='P', width=100, layer="met5label", orientation=0,
#                              center=(240, 200), port_type="electrical")
# print(inductor_in.ports)
# pdb.set_trace()
# print("Ind y min", lc.x, lc.y)
# print(lc.ports)
# exit()
# Routing of Pad to Inductor (once the port has been figured out)
routep = gf.routing.get_route_electrical(
    lc.ports["Outp"], pt.ports["e12"], layer="met5drawing"
)
routen = gf.routing.get_route_electrical(
    lc.ports["Outn"], pt.ports["e14"], layer="met5drawing"
)
# Routing diff pair
for i in [routep, routen]:
    pad.add(i.references)
# Routing using gdsfactory
# Output gds name
gf_gds_out = "output_pad.gds"
pad.write_gds(gf_gds_out)
print(__file__.split(".")[0])

# Write out GDS
# ------------------
# write the layout to the gds file
# exit()
# pya.MainWindow.instance().load_layout('t.gds',1)
