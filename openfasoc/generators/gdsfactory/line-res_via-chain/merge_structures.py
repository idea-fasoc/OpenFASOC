import gdsfactory as gf

layers = [68, 69, 70, 71, 72]

# ARRAY
Carray = gf.Component("merged_line_Res_via_chain_array")

counter_x = 0
counter_y = 0

for layer in layers:
    Cstructure = gf.import_gds(
        str(layer) + "_line_res.gds", name=str(layer) + "_line_res", flatten=True
    )
    Rstructure = Carray << Cstructure
    Rstructure.move([counter_x * 100, counter_y * 240])
    counter_x += 1

counter_x = 0
counter_y += 1

for layer in layers:
    Cstructure = gf.import_gds(
        str(layer) + "_via_chain.gds", name=str(layer) + "_via_chain", flatten=True
    )
    Rstructure = Carray << Cstructure
    Rstructure.move([counter_x * 100, counter_y * 240])
    counter_x += 1

counter_x = 0
counter_y += 1

for layer in layers:
    Cstructure = gf.import_gds(
        str(layer) + "_thick_line_res.gds",
        name=str(layer) + "_thick_line_res",
        flatten=True,
    )
    Rstructure = Carray << Cstructure
    Rstructure.move([counter_x * 100, counter_y * 240])
    counter_x += 1

counter_x = 0
counter_y += 1

# OUTPUT
Carray.write_gds("merged_line_res_via_chain.gds")
