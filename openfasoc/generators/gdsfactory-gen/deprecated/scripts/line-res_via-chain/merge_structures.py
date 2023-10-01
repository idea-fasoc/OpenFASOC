import gdsfactory as gf
import sys
import argparse

from gdsfactory.cell import Settings, cell
from gdsfactory.component import Component

from gdsfactory.generic_tech import get_generic_pdk

gf.config.rich_output()
PDK = get_generic_pdk()
PDK.activate()

parser = argparse.ArgumentParser(description="Via-chain Generator")
parser.add_argument("--output_dir", default=".", help="GDS output directory")
args = parser.parse_args()

gds_outdir = str(args.output_dir)

# ARRAY
@cell
def create_Carray() -> Component:
    Carray = gf.Component()

    counter_x = 0
    counter_y = 0

    layers = [68, 69, 70, 71, 72]

    for layer in layers:
        Cstructure = gf.import_gds(
            gds_outdir + "/" + str(layer) + "_line_res.gds", flatten=True
        )
        Cstructure.name = str(layer) + "_line_res"
        Rstructure = Carray << Cstructure
        Rstructure.move([counter_x * 100, counter_y * 240])
        counter_x += 1

    counter_x = 0
    counter_y += 1
    for layer in layers:
        Cstructure = gf.import_gds(
            gds_outdir + "/" + str(layer) + "_via_chain.gds", flatten=True
        )
        Cstructure.name = str(layer) + "_via_chain"
        Rstructure = Carray << Cstructure
        Rstructure.move([counter_x * 100, counter_y * 240])
        counter_x += 1

    counter_x = 0
    counter_y += 1

    for layer in layers:
        Cstructure = gf.import_gds(
            gds_outdir + "/" + str(layer) + "_thick_line_res.gds",
            flatten=True,
        )
        Cstructure.name = str(layer) + "_thick_line_res"
        Rstructure = Carray << Cstructure
        Rstructure.move([counter_x * 100, counter_y * 240])
        counter_x += 1

    counter_x = 0
    counter_y += 1

    return Carray


Carray = create_Carray()

# OUTPUT
Carray.write_gds(gds_outdir + "/" + "merged_line_res_via_chain.gds")
