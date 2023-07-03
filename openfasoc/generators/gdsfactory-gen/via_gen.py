from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
from pydantic import validate_arguments
from PDK.mappedpdk import MappedPDK
from math import floor
from typing import Optional


@validate_arguments
def __error_check_order_layers(
    pdk: MappedPDK, glayer1: str, glayer2: str
) -> tuple[int, int]:
    """correctly order layers (level1 should be lower than level2)"""
    pdk.activate()
    # check that the generic layers specfied can be routed between
    if not all([pdk.is_routable_glayer(met) for met in [glayer1, glayer2]]):
        raise ValueError("via_stack: specify between two routable layers")
    level1 = int(glayer1[-1]) if "met" in glayer1 else 0
    level2 = int(glayer2[-1]) if "met" in glayer2 else 0
    if level1 > level2:
        level1, level2 = level2, level1
    return level1, level2


@cell
def via_stack(
    pdk: MappedPDK, glayer1: str, glayer2: str, centered: Optional[bool] = True
) -> Component:
    """produces a single via stack between two metal layers
    does not produce via arrays
    args:
    pdk: MappedPDK is the pdk to use
    glayer1: str is the glayer to start on
    glayer2: str is the glayer to end on
    ****NOTE it does not matter what order you pass layers
    ****NOTE will not lay poly or active but will lay metals
    ports (one port for each edge):
    top_met_...all edges
    bottom_via_...all edges
    bottom_met_...all edges
    """
    level1, level2 = __error_check_order_layers(pdk, glayer1, glayer2)
    viastack = Component()
    # if same level return empty component
    if level1 == level2:
        return viastack
    #topmet,bottomvia,bottommet, finalized?,what are they
    port_refs = [[False,None],[False,None],[False,None]]
    # lay mcon if first layer is active or poly
    if not level1:
        pdk.has_required_glayers(["mcon", "met1"])
        mcondim = pdk.get_grule("mcon")["width"]
        port_refs[1][1] = viastack << rectangle(
            size=(mcondim, mcondim), layer=pdk.get_glayer("mcon"), centered=True
        )
        metdim = max(
            2 * pdk.get_grule("met1", "mcon")["min_enclosure"] + mcondim,
            pdk.get_grule("met1")["min_width"],
        )
        port_refs[2][1] = viastack << rectangle(
            size=(metdim, metdim), layer=pdk.get_glayer("met1"), centered=True
        )
        port_refs[1][0] = True
        port_refs[2][0] = True
        level1 += 1 # make bottom met so we can use code below
    if level1 == level2: # re-check same layer
        port_refs[0][1] = port_refs[2][1]
        port_refs[0][0] = True
    elif level1 and level2: # construct metal stack if both are metals
        for level in range(level1, level2):
            gmetlayer = "met" + str(level)
            gnextvia = "via" + str(level)
            pdk.has_required_glayers([gmetlayer, gnextvia])
            metdim = max(
                2 * pdk.get_grule(gmetlayer, gnextvia)["min_enclosure"]
                + pdk.get_grule(gnextvia)["width"],
                pdk.get_grule(gmetlayer)["min_width"],
            )
            metref = viastack << rectangle(
                size=(metdim, metdim), layer=pdk.get_glayer(gmetlayer), centered=True
            )
            viadim = pdk.get_grule(gnextvia)["width"]
            viaref = viastack << rectangle(
                size=(viadim, viadim), layer=pdk.get_glayer(gnextvia), centered=True
            )
            if not port_refs[2][0]:
                port_refs[2][1] = metref
                port_refs[2][0] = True
            if not port_refs[1][0]:
                port_refs[1][1] = viaref
                port_refs[1][0] = True
        gfinalmet = "met" + str(level2)
        gprevvia = "via" + str(level)
        metdim = max(
            2 * pdk.get_grule(gfinalmet, gprevvia)["min_enclosure"]
            + pdk.get_grule(gprevvia)["width"],
            pdk.get_grule(gfinalmet)["min_width"],
        )
        port_refs[0][1] = viastack << rectangle(
            size=(metdim, metdim), layer=pdk.get_glayer(gfinalmet), centered=True
        )
    # add ports and implement center option
    pre = ["top_met_","bottom_via_","bottom_met_"]
    for i in range(3):
        viastack.add_ports(port_refs[1][1].get_ports_list(),prefix=pre[i])
    center_stack = Component()
    viastack_ref = center_stack << viastack
    if not centered:
        viastack_ref.movex(viastack.xmax).movey(viastack.ymax)
    center_stack.add_ports(viastack_ref.get_ports_list())
    return center_stack.flatten()


@cell
def via_array(
    pdk: MappedPDK,
    glayer1: str,
    glayer2: str,
    size=(4.0, 1.0),
    minus1: Optional[bool] = False,
) -> Component:
    """Fill a region with vias. Will automatically decide num rows and columns
    args:
    pdk: MappedPDK is the pdk to use
    glayer1: str is the glayer to start on
    glayer2: str is the glayer to end on
    ****NOTE it does not matter what order you pass layers
    ****NOTE will not lay poly or active but will lay metals
    size: tuple is the (width, hieght) of the area to enclose
    ****NOTE: the size will be the dimensions of the top metal
    ports (one port for each edge):
    top_met_...all edges
    """
    level1, level2 = __error_check_order_layers(pdk, glayer1, glayer2)
    viaarray = Component()
    # if same level return empty component
    if level1 == level2:
        return viaarray
    # figure out min space between via stacks
    via_spacing = [] if level1 else [pdk.get_grule("mcon")["min_separation"]]
    level1 = level1 if level1 else level1 + 1
    for level in range(level1, level2):
        met_glayer = "met" + str(level)
        via_glayer = "via" + str(level)
        via_spacing.append(pdk.get_grule(met_glayer)["min_separation"])
        via_spacing.append(pdk.get_grule(via_glayer)["min_separation"])
    via_spacing.append(pdk.get_grule("met" + str(level2))["min_separation"])
    via_spacing = max(via_spacing)
    # error check size and get viaspacing_full
    viastack = via_stack(pdk, glayer1, glayer2)
    viadim = max(viastack.xmax - viastack.xmin, viastack.ymax - viastack.ymin)
    for i, dim in enumerate(size):
        if round(viadim, 8) > round(dim, 8):
            raise ValueError(f"via_array,size:dim {i}={dim} less than {viadim}")
    viaspacing_full = via_spacing + viadim
    # num_vias[0]=x, num_vias[1]=y
    num_vias = [(floor(dim / (viadim + via_spacing)) or 1) for dim in size]
    if minus1:
        num_vias = [(dim - 1 if dim > 1 else dim) for dim in num_vias]
    # create array and add to component
    temparray = Component("temp horizontal vias")
    temparray.add_array(
        viastack,
        columns=num_vias[0],
        rows=num_vias[1],
        spacing=[viaspacing_full, viaspacing_full],
    )
    array_ref = viaarray << temparray
    center_offsety = -1 * viaspacing_full * floor(num_vias[1] / 2)
    center_offsetx = -1 * viaspacing_full * floor(num_vias[0] / 2)
    if (num_vias[0] % 2) == 0:  # even num columns
        center_offsetx += viaspacing_full / 2
    if (num_vias[1] % 2) == 0:  # even num rows
        center_offsety += viaspacing_full / 2
    array_ref.movex(center_offsetx)
    array_ref.movey(center_offsety)
    # place top metal and return
    top_met_layer = pdk.get_glayer("met" + str(level2))
    mref = viaarray << rectangle(size=size, layer=top_met_layer, centered=True)
    viaarray.add_ports(mref.get_ports_list(),prefix="top_met_")
    return viaarray.flatten()


if __name__ == "__main__":
    from PDK.util.standard_main import pdk
    from sys import exit

    test_all = False

    if not test_all:
        myarray = via_array(pdk, "active_diff", "met3")
        myarray.show()
        print(myarray.ports)
        exit(0)

    layers = ["poly", "met1", "met2", "met3"]
    for lay1 in layers:
        for lay2 in layers:
            via_array(pdk, lay1, lay2).show()
