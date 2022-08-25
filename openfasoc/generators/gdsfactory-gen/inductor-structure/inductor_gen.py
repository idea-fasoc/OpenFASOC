# Ryan W & Chandru R 2022

import pya
import os, sys
import argparse, json

import gdsfactory as gf
from gdsfactory.layers import lyp_to_dataclass

import sky130

from sky130 import cells as sky130_cells
from sky130 import tech as sky130_tech

# Local pymacros
local_pymacros = os.path.relpath("./pymacros")

# gdsfactory tech
gdsfactory_tech = os.path.relpath("./sky130_tech.lyp")
PATH_TO_PAD_GDSII = "./pad_forty_met1_met5.gds"

sys.path.append(local_pymacros)
sys.path.append(gdsfactory_tech)

from sky130_pcells import *

exec(lyp_to_dataclass(gdsfactory_tech))

# Logger
def consoleOut(m, t="info"):
    if t == "info":
        print("# INFO #  : " + m)
    elif t == "error":
        print("# ERR  #  : " + m)
        sys.exit(1)
    elif t == "warn":
        print("# WARN #  : " + m)
    else:
        print("#      #  : " + m)


# JSON Parser
parser = argparse.ArgumentParser(description="Inductor Generator")
parser.add_argument("--spec_file", required=False)
args = parser.parse_args()
try:
    spec_file = open(args.spec_file, "r")
    spec = json.load(spec_file)
    consoleOut("Configuration File Loaded")
except:
    consoleOut("No Configuration File Found", "warn")

# Create new pcell instantiation
def createPCellInstance(layout, pcell_name, lib_name, params={}, x=0, y=0, name="CELL"):
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
            consoleOut(f"Resorting To Default Cell Param Value: {p.default}", "warn")
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
    return pcell_decl.id()


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


# Main
__layout__ = pya.Layout()
TOP = __layout__.create_cell("TOP")
__output__ = "output.gds"
consoleOut("Generating " + __output__)

# Load Technology
Sky130()
consoleOut("PDK Pcells Loaded")

# Create the Layout
cells = spec["cells"]
consoleOut(f"{len(cells)} Cells Found")

created_cells = []

# Create each cell defined in config
for i in range(len(cells)):
    cellName = list(cells.keys())[i]
    curCell = list(cells.values())[i]
    consoleOut(f"Creating cell '{cellName}' at origin {curCell['position']}")
    created_cells.append(
        createPCellInstance(
            layout=__layout__,
            pcell_name=curCell["pcell"],
            lib_name=curCell["lib"],
            params=curCell["params"],
            x=curCell["position"][0],
            y=curCell["position"][1],
            name=cellName,
        )
    )
    consoleOut(f"Cell Created Successfully: ID-{created_cells[i]}")

# Write cells to GDS file output
__layout__.write(__output__)

# Define ports
consoleOut("Defining Ports")
__top_level__ = gf.Component("InductorTestStructure")
__component__ = gf.import_gds(__output__, "TOP")
for i in range(len(cells)):
    curCell = list(cells.values())[i]
    # If the cell is symmetric
    if (curCell["pcell"] == "diff_octagon_inductor") or (
        curCell["pcell"] == "diff_square_inductor"
    ):
        # Calculate port positions
        center_x = (curCell["params"]["Louter"] / 2) + curCell["position"][0]
        spacing = curCell["params"]["spacing_input"]
        width = curCell["params"]["W"]
        # Add ports
        __component__.add_port(
            name=f"{list(cells.keys())[i]}_{curCell['ports'][0]}",
            center=[((center_x / 2) - (spacing / 2) - (width / 2) - 50), 0],
            width=width,
            orientation=270,
            layer=LAYER.met5drawing,
        )
        __component__.add_port(
            name=f"{list(cells.keys())[i]}_{curCell['ports'][1]}",
            center=[((center_x / 2) + (spacing / 2) + (width / 2) - 50), 0],
            width=width,
            orientation=270,
            layer=LAYER.met5drawing,
        )
        consoleOut(
            f"Defined Ports {curCell['ports'][0]} and {curCell['ports'][1]} for {list(cells.keys())[i]}"
        )
        # Create Pads
        pads_array = []
        if "pads" in curCell:
            consoleOut("Creating Pads")
            PADS = gf.Component("PADS_" + str(i))
            if curCell["pads"]["type"] == "GSGSG":
                for j in range(5):
                    pad = gf.import_gds(PATH_TO_PAD_GDSII)
                    pad.add_port(
                        name=f"io{j}",
                        center=[20, 40],
                        width=40,
                        orientation=90,
                        layer=LAYER.met5drawing,
                    )
                    pad = PADS << pad
                    pad.move(
                        (
                            (
                                (curCell["pads"]["pitch"] * j)
                                - ((2 * curCell["pads"]["pitch"]) + 20)
                            ),
                            (curCell["position"][1] - curCell["pads"]["padding"]),
                        )
                    )
                    pads_array.append(pad)
            PADS = __top_level__ << PADS
            # Routing
            consoleOut("Pads Placed. Routing Pads and Cells")
            routeInput = gf.routing.get_route_electrical(
                __component__.ports[f"{list(cells.keys())[i]}_{curCell['ports'][0]}"],
                pads_array[1].ports["io1"],
                layer=LAYER.met5drawing,
                width=width,
            )
            __top_level__.add(routeInput.references)
            routeOutput = gf.routing.get_route_electrical(
                __component__.ports[f"{list(cells.keys())[i]}_{curCell['ports'][1]}"],
                pads_array[3].ports["io2"],
                layer=LAYER.met5drawing,
                width=width,
            )
            __top_level__.add(routeOutput.references)

        __component__ = __top_level__ << __component__
        __top_level__.show()
        consoleOut("Routing Complete & Rendered")

    else:
        consoleOut("Not yet implemented", "error")

consoleOut("Script Finished.")
