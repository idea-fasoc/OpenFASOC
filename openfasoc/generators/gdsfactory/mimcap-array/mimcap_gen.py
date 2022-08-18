import argparse

import gdsfactory as gf

parser = argparse.ArgumentParser(description="Via-chain Generator")
parser.add_argument("--input_file", required=True)
parser.add_argument("--pitch", required=True)
parser.add_argument("--wtop", required=True, help="Top metal width")
parser.add_argument("--wbot", required=True, help="Bottom metal width")
parser.add_argument("--lyrtop", required=True, help="Top metal layer number")
args = parser.parse_args()

pitch = float(args.pitch)
top_width = float(args.wtop)
bot_width = float(args.wbot)
top_layer = int(args.lyrtop)

# ARRAY
Carray = gf.Component("single_mimcap_array")

file = args.input_file
Cstructure_in = gf.import_gds(file, name=str(file), flatten=True)

# position generation
i = 0
j = 0
position_list = []

while i <= 36 - Cstructure_in.xsize:
    j = 0
    while j <= 36 - Cstructure_in.ysize:
        position_list.append((i, j))
        j += pitch
    i += pitch

# place cells
for pos in position_list:
    Cstructure = Cstructure_in.copy(suffix="_" + str(pos[0]) + "_" + str(pos[1]))
    Rstructure = Carray << Cstructure
    Rstructure.move(origin=Rstructure.center, destination=pos)

# generate connecting mesh
i = 0
j = 0

# length
if 36 % pitch == 0:
    length = 36 - pitch
else:
    length = 36 // pitch * pitch

# cross section of wires and segments
Xmesh = gf.CrossSection()
Xmesh.add(width=top_width, offset=0, layer=(top_layer, 20))

while i <= length:
    pt1 = (i - Cstructure_in.xsize / 2 + top_width / 2, 0 - Cstructure_in.ysize / 2)
    pt2 = (
        i - Cstructure_in.xsize / 2 + top_width / 2,
        length + Cstructure_in.xsize / 2,
    )

    # create a path
    Pmesh = gf.Path([pt1, pt2])

    # extrude onto two metal layers
    Cmesh = gf.path.extrude(Pmesh, Xmesh)

    # reference the path extrusion to component
    Carray << Cmesh

    i += pitch

while j <= length:
    pt1 = (0 - Cstructure_in.xsize / 2, j + Cstructure_in.xsize / 2 - top_width / 2)
    pt2 = (
        length + Cstructure_in.xsize / 2,
        j + Cstructure_in.xsize / 2 - top_width / 2,
    )

    # create a path
    Pmesh = gf.Path([pt1, pt2])

    # extrude onto two metal layers
    Cmesh = gf.path.extrude(Pmesh, Xmesh)

    # reference the path extrusion to component
    Carray << Cmesh

    j += pitch

i = 0
j = 0

# cross section of wires and segments
Xmesh = gf.CrossSection()
Xmesh.add(width=bot_width, offset=0, layer=(top_layer - 1, 20))

while i <= length:
    pt1 = (i + Cstructure_in.xsize / 2 - bot_width / 2, 0 - Cstructure_in.ysize / 2)
    pt2 = (
        i + Cstructure_in.xsize / 2 - bot_width / 2,
        length + Cstructure_in.xsize / 2,
    )

    # create a path
    Pmesh = gf.Path([pt1, pt2])

    # extrude onto two metal layers
    Cmesh = gf.path.extrude(Pmesh, Xmesh)

    # reference the path extrusion to component
    Carray << Cmesh

    i += pitch

while j <= length:
    pt1 = (0 - Cstructure_in.xsize / 2, j - Cstructure_in.xsize / 2 + bot_width / 2)
    pt2 = (
        length + Cstructure_in.ysize / 2,
        j - Cstructure_in.xsize / 2 + bot_width / 2,
    )

    # create a path
    Pmesh = gf.Path([pt1, pt2])

    # extrude onto two metal layers
    Cmesh = gf.path.extrude(Pmesh, Xmesh)

    # reference the path extrusion to component
    Carray << Cmesh

    j += pitch

# create pad ring
Cstructure = gf.Component(str(top_layer - 1) + "_" + str(top_layer) + "_mimcap")
Carray20 = gf.Component(str(top_layer - 1) + "_" + str(top_layer) + "_mimcap_array20")
Crail = gf.Component("rails")

# import and place pads and arrays
Cpad = gf.import_gds("./pad_forty_met1_met5.GDS")

i = 0
for i in range(20):
    Rpad = Cstructure << Cpad
    Rpad.move([i * 60, 0])
    Rarray = Carray20 << Carray
    Rarray.move(origin=Rarray.center, destination=[i * 60 + 20, 60])
    Rpad = Cstructure << Cpad
    Rpad.move([i * 60, 80])

# top and bottom rails
# use bbox of Carray20 to aid the rail generation

top_edge = Carray20.ymax
bot_edge = Carray20.ymin
left_edge = Carray20.xmin
right_edge = Carray20.xmax

allowed_space = (40 - (top_edge - bot_edge)) / 2

top_rail_pts = [
    (left_edge, top_edge - top_width),
    (right_edge, top_edge - top_width),
    (right_edge, top_edge + allowed_space - top_width),
    (left_edge, top_edge + allowed_space - top_width),
]
bot_rail_pts = [
    (left_edge, bot_edge + bot_width),
    (right_edge, bot_edge + bot_width),
    (right_edge, bot_edge - allowed_space + bot_width),
    (left_edge, bot_edge - allowed_space + bot_width),
]

Crail.add_polygon(top_rail_pts, layer=(top_layer, 20))
Crail.add_polygon(bot_rail_pts, layer=(top_layer - 1, 20))

# add top rail connector
connector_width = top_rail_pts[-1][1] - top_rail_pts[1][1]
connector_pts = [
    (left_edge, top_edge - top_width + 1 / 2 * connector_width),
    (left_edge - 6, top_edge - top_width + 1 / 2 * connector_width),
    (left_edge - 6, bot_edge - 5),
    (left_edge, bot_edge - 5),
]

Xmesh = gf.CrossSection()
Xmesh.add(width=connector_width, offset=0, layer=(top_layer, 20))

Ctail = gf.path.extrude(gf.Path(connector_pts), Xmesh)

# move Instances into center of Cstructure

center_pt = Cstructure.center

Rarray20 = Cstructure << Carray20
Rtail = Cstructure << Ctail
Rrail = Cstructure << Crail
translation = (center_pt[0] - Rarray20.center[0], center_pt[1] - Rarray20.center[1])
Rarray20.move(translation)
Rtail.move(translation)
Rrail.move(translation)

# add bot rail connector
bot_rail_cn_pts = [(60, 40), (100, 40), (100, 40 + bot_width), (60, 40 + bot_width)]
Cstructure.add_polygon(bot_rail_cn_pts, layer=(top_layer - 1, 20))

# OUTPUT
Cstructure.write_gds(
    "merged_" + str(top_layer - 1) + "_" + str(top_layer) + "_cap_array.GDS"
)
