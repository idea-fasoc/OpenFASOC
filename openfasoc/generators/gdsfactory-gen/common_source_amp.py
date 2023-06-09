import gdsfactory as gf
from gdsfactory.component import Component, ComponentReference

import gf180
from gf180 import layers


GFlayers = {
    "dnwell": layers.layer["dnwell"],
    "pwell": layers.layer["lvpwell"],
    "nwell": layers.layer["nwell"],
    "psd": layers.layer["pplus"],
    "nsd": layers.layer["nplus"],
    "active": layers.layer["comp"],
    "poly": layers.layer["poly2"],
    "mcon": layers.layer["contact"],
    "met1": layers.layer["metal1"],
}


# import sky130
# SKYlayers = {
# 	"dnwell" : sky130.layers.layer["dnwell"],
# 	"pwell" : sky130.layers.layer["pwell"],
# 	"nwell" : sky130.layers.layer["nwell"],
# 	"psd" : sky130.layers.layer["pplus"],
# 	"nsd" : sky130.layers.layer["nplus"],
# 	"active" : sky130.layers.layer["diff"],
# 	"poly" : sky130.layers.layer["poly"],
# 	"mcon" : sky130.layers.layer["licon"],
# 	"met1" : sky130.layers.layer["li"],
# }

GenericLayers = {
    "dnwell": (1, 20),
    "pwell": (3, 20),
    "nwell": (4, 20),
    "psd": (5, 20),
    "nsd": (6, 20),
    "active": (7, 20),
    "poly": (8, 20),
    "mcon": (9, 20),
    "met1": (11, 20),
}


@gf.cell
def conmet(glayers) -> Component:
    conmet = gf.Component("connection")
    conmet << gf.components.rectangle(size=(0.34, 0.34), layer=glayers["met1"])
    mcon = conmet << gf.components.rectangle(size=(0.22, 0.22), layer=glayers["mcon"])
    mcon.movex(0.06).movey(0.06)
    return conmet


@gf.cell
def common_source_amp(glayers) -> Component:
    required_layers = [
        "dnwell",
        "pwell",
        "nwell",
        "psd",
        "nsd",
        "active",
        "poly",
        "mcon",
        "met1",
    ]
    for layer in glayers:
        if layer not in required_layers:
            raise RuntimeError()
    Top_cell = gf.Component("top")
    # power
    metgrd_pwr = gf.components.rectangle(size=(2, 0.23), layer=glayers["met1"])
    metgrd_vdd = Top_cell << metgrd_pwr
    metgrd_vdd.y = 3.7
    metgrd_vss = Top_cell << metgrd_pwr
    # nfet
    dnwell = Top_cell << gf.components.rectangle(size=(2, 1.2), layer=glayers["dnwell"])
    dnwell.y = 1
    pwell = Top_cell << gf.components.rectangle(size=(1.8, 0.9), layer=glayers["pwell"])
    pwell.y = 1
    pwell.x = 1
    nsd = Top_cell << gf.components.rectangle(size=(1.5, 0.7), layer=glayers["nsd"])
    nsd.y = 1
    nsd.x = 1
    activen = Top_cell << gf.components.rectangle(
        size=(1.2, 0.4), layer=glayers["active"]
    )
    activen.y = 1
    activen.x = 1
    gate_n = Top_cell << gf.components.rectangle(
        size=(0.28, 1.3), layer=glayers["active"]
    )
    gate_n.y = 1.3
    gate_n.x = 1
    mcon_n_s = Top_cell << conmet(glayers)
    mcon_n_s.x = 0.6
    mcon_n_s.y = 1
    mcon_n_d = Top_cell << conmet(glayers)
    mcon_n_d.x = 1.4
    mcon_n_d.y = 1
    mcon_n_g = Top_cell << conmet(glayers)
    mcon_n_g.x = 1
    mcon_n_g.y = 1.75
    # pfet
    nwell = Top_cell << gf.components.rectangle(size=(1.8, 0.9), layer=glayers["nwell"])
    nwell.x = 1
    nwell.y = 2.6
    psd = Top_cell << gf.components.rectangle(size=(1.5, 0.7), layer=glayers["psd"])
    psd.x = 1
    psd.y = 2.6
    activep = Top_cell << gf.components.rectangle(
        size=(1.2, 0.4), layer=glayers["active"]
    )
    activep.x = 1
    activep.y = 2.6
    gate_p = Top_cell << gf.components.rectangle(
        size=(0.28, 1.1), layer=glayers["active"]
    )
    gate_p.y = 2.85
    gate_p.x = 1
    mcon_p_s = Top_cell << conmet(glayers)
    mcon_p_s.x = 0.6
    mcon_p_s.y = 2.6
    mcon_p_d = Top_cell << conmet(glayers)
    mcon_p_d.x = 1.4
    mcon_p_d.y = 2.6
    mcon_p_g = Top_cell << conmet(glayers)
    mcon_p_g.x = 1
    mcon_p_g.y = 3.2
    # routing
    route_n_s = Top_cell << gf.components.rectangle(
        size=(0.34, 0.6), layer=glayers["met1"]
    )
    route_n_s.x = 0.6
    route_n_s.y = 0.53
    route_n_d_p = Top_cell << gf.components.rectangle(
        size=(0.34, 1.94), layer=glayers["met1"]
    )
    route_n_d_p.x = 1.74
    route_n_d_p.y = 1.7 + 0.1
    route_p_s = Top_cell << gf.components.rectangle(
        size=(0.34, 1.15), layer=glayers["met1"]
    )
    route_p_s.x = 0.26
    route_p_s.y = 3.01
    # flatten and return component
    return Top_cell.flatten()


myamp = common_source_amp(GFlayers)
myamp.write_gds("gfflat.gds")
print(myamp.metadata)
