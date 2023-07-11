from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
from pydantic import validate_arguments
from PDK.mappedpdk import MappedPDK
from math import floor
from typing import Optional, Union
from PDK.util.custom_comp_utils import rename_ports_by_orientation, evaluate_bbox, prec_array
from PDK.util.snap_to_grid import component_snap_to_grid
from decimal import Decimal


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
    lay1, lay2 = glayer1, glayer2
    if level1 > level2:
        level1, level2 = level2, level1
        lay1, lay2 = glayer2, glayer1
    return ((level1,level2),(lay1,lay2))


@cell
def via_stack(
    pdk: MappedPDK, glayer1: str, glayer2: str, centered: Optional[bool] = True, fullbottom: Optional[bool] = False, fulltop: Optional[bool] = False
) -> Component:
    """produces a single via stack between two metal layers
    does not produce via arrays
    args:
    pdk: MappedPDK is the pdk to use
    glayer1: str is the glayer to start on
    glayer2: str is the glayer to end on
    ****NOTE it does not matter what order you pass layers
    ****NOTE will not lay poly or active but will lay metals
    fullbottom: will lay the bottom glayer all over the area of the viastack
    fulltop: will lay the top glayer all over the area of the viastack
    ports (one port for each edge):
    top_met_...all edges
    bottom_via_...all edges
    bottom_met_...all edges
    """
    level1, level2 = __error_check_order_layers(pdk, glayer1, glayer2)[0]
    viastack = Component()
    # if same level return empty component
    if level1 == level2:
        return viastack
    # topmet,bottomvia,bottommet, finalized?,what are they
    port_refs = [[False, None], [False, None], [False, None]]
    # lay mcon if first layer is active or poly
    if not level1:
        pdk.has_required_glayers(["mcon", "met1"])
        mcondim = pdk.get_grule("mcon")["width"]
        port_refs[1][1] = viastack << rectangle(
            size=(mcondim, mcondim), layer=pdk.get_glayer("mcon"), centered=True
        )
        metdim = round(max(
            2 * pdk.get_grule("met1", "mcon")["min_enclosure"] + mcondim,
            pdk.get_grule("met1")["min_width"],
        ),6)
        port_refs[2][1] = viastack << rectangle(
            size=(metdim, metdim), layer=pdk.get_glayer("met1"), centered=True
        )
        port_refs[1][0] = True
        port_refs[2][0] = True
        level1 += 1  # make bottom met so we can use code below
    if level1 == level2:  # re-check same layer
        port_refs[0][1] = port_refs[2][1]
        port_refs[0][0] = True
    elif level1 and level2:  # construct metal stack if both are metals
        for level in range(level1, level2):
            gmetlayer = "met" + str(level)
            gnextvia = "via" + str(level)
            if level != level1:
                gprevvia = "via" + str(level-1)
                gprevvia_rule = 2 * pdk.get_grule(gmetlayer, gprevvia)["min_enclosure"] + pdk.get_grule(gprevvia)["width"]
            else:
                gprevvia_rule=0
            pdk.has_required_glayers([gmetlayer, gnextvia])
            metdim = round(max(
                2 * pdk.get_grule(gmetlayer, gnextvia)["min_enclosure"]
                + pdk.get_grule(gnextvia)["width"],
                pdk.get_grule(gmetlayer)["min_width"],
                gprevvia_rule
            ),6)
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
        metdim = round(max(
            2 * pdk.get_grule(gfinalmet, gprevvia)["min_enclosure"]
            + pdk.get_grule(gprevvia)["width"],
            pdk.get_grule(gfinalmet)["min_width"],
        ),6)
        port_refs[0][1] = viastack << rectangle(
            size=(metdim, metdim), layer=pdk.get_glayer(gfinalmet), centered=True
        )
    # add ports and implement center option
    pre = ["top_met_", "bottom_via_", "bottom_met_"]
    for i in range(3):
        viastack.add_ports(port_refs[i][1].get_ports_list(), prefix=pre[i])
    gprevia = "via"+str(level1-1) if level1 != 1 else "mcon"
    bottomsize = max(2*pdk.get_grule("met"+str(level1),gprevia)["min_enclosure"] + pdk.get_grule(gprevia)["width"], evaluate_bbox(viastack)[0])
    if fullbottom:
        viastack << rectangle(size=2*[bottomsize],layer=pdk.get_glayer("met"+str(level1)), centered=True)
    if fulltop:
        viastack << rectangle(size=2*[bottomsize],layer=pdk.get_glayer("met"+str(level2)), centered=True)
    center_stack = Component()
    viastack_ref = center_stack << viastack
    if not centered:
        viastack_ref.movex(viastack.xmax).movey(viastack.ymax)
    
    center_stack.add_ports(viastack_ref.get_ports_list())
    return rename_ports_by_orientation(center_stack).flatten()


@cell
def via_array(
    pdk: MappedPDK,
    glayer1: str,
    glayer2: str,
    size=(4.0, 1.0),
    minus1: Optional[bool] = False,
    lay_bottom: Optional[bool] = False
) -> Component:
    """Fill a region with vias. Will automatically decide num rows and columns
    args:
    pdk: MappedPDK is the pdk to use
    glayer1: str is the glayer to start on
    glayer2: str is the glayer to end on
    lay_bottom: bool if true will lay bottom met
    ****NOTE it does not matter what order you pass layers
    ****NOTE will not lay poly or active but will lay metals
    size: tuple is the (width, hieght) of the area to enclose
    ****NOTE: the size will be the dimensions of the top metal
    ports (one port for each edge):
    top_met_...all edges
    bottom_met_...all edges (only if lay_bottom is specified)
    """
    tmpsize = list(size)
    for i in range(2):
        if isinstance(size[i],Union[float,int]):
            tmpsize[i] = Decimal(str(size[i]))
    size = tmpsize
    # setup
    layer_ordering = __error_check_order_layers(pdk, glayer1, glayer2)
    level1, level2 = layer_ordering[0]
    glayer1, glayer2 = layer_ordering[1]
    viaarray = Component()
    # if same level return empty component
    if level1 == level2:
        return viaarray
    # figure out min space between via stacks
    viastack = via_stack(pdk, glayer1, glayer2).remove_layers(layers=[pdk.get_glayer(glayer2)])
    via_spacing = [] if level1 else [Decimal(str(pdk.get_grule("mcon")["min_separation"]))]
    level1_met = level1 if level1 else level1 + 1
    get_sep = lambda _pdk, rule, _lay_, comp : 2*(rule/2+Decimal(str(comp.extract(layers=[_pdk.get_glayer(_lay_)]).xmax))-Decimal(str(comp.xmax)))
    outer_enclosure = 0
    for level in range(level1_met, level2):
        met_glayer = "met" + str(level)
        via_glayer = "via" + str(level)
        mrule = Decimal(str(pdk.get_grule(met_glayer)["min_separation"]))
        vrule = Decimal(str(pdk.get_grule(via_glayer)["min_separation"]))
        via_spacing.append(get_sep(pdk, mrule,met_glayer,viastack))
        via_spacing.append(get_sep(pdk, vrule,via_glayer,viastack))
        if level == (level2-1):
            outer_enclosure = Decimal(str(pdk.get_grule(glayer2,via_glayer)["min_enclosure"]))
    via_spacing = max(via_spacing)
    # error check size and get viaspacing_full
    viadim = 2*Decimal(str(viastack.xmax))
    for i, dim in enumerate(size):
        if viadim > dim:
            raise ValueError(f"via_array,size:dim {i}={dim} less than {viadim}")
    viaspacing_full = via_spacing + viadim
    # num_vias[0]=x, num_vias[1]=y
    encsize = [dim - outer_enclosure for dim in size]
    num_vias = [(floor(dim / (viadim + via_spacing)) or 1) for dim in encsize]
    if minus1:
        num_vias = [(dim - 1 if dim > 1 else dim) for dim in num_vias]
    # create array and add to component
    temparray = Component("via array")
    temparray << prec_array(
        viastack,
        columns=num_vias[0],
        rows=num_vias[1],
        spacing=[viaspacing_full, viaspacing_full],
    )
    # center the array
    array_ref = viaarray.add(temparray.ref_center())
    # place bottom metal, top metal, add ports, and return
    if lay_bottom:
        if level1:
            keymetdims = viaarray.extract(layers=[pdk.get_glayer("met"+str(level1_met))]).bbox
            bheight = 2*keymetdims[1][1]
            bwidth = 2*keymetdims[1][0]
        else:
            bviadims = viaarray.extract(layers=[pdk.get_glayer("mcon")]).bbox
            added_enclosure = 2*pdk.get_grule(glayer1,"mcon")["min_enclosure"]
            bheight = 2*bviadims[1][1] + added_enclosure
            bwidth = 2*bviadims[1][0] + added_enclosure
        b_met_dims = [bwidth, bheight]
        bref = viaarray << rectangle(size=b_met_dims, layer=pdk.get_glayer(glayer1), centered=True)
        viaarray.add_ports(bref.get_ports_list(), prefix="bottom_met_")
    top_met_layer = pdk.get_glayer("met" + str(level2))
    tref = viaarray << rectangle(size=(float(size[0]),float(size[1])), layer=top_met_layer, centered=True)
    viaarray.add_ports(tref.get_ports_list(), prefix="top_met_")
    return component_snap_to_grid(rename_ports_by_orientation(viaarray))


if __name__ == "__main__":
    from PDK.util.standard_main import pdk
    from PDK.util.custom_comp_utils import print_ports
    from sys import exit

    test_all = False

    if not test_all:
        myarray = via_array(pdk, "poly", "met2",size=(5,4))
        myarray.show()
        print_ports(myarray, False)
        exit(0)

    layers = ["poly", "met1", "met2", "met3"]
    for lay1 in layers:
        for lay2 in layers:
            via_array(pdk, lay1, lay2, lay_bottom=True).show()
