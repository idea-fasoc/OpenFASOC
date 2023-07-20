from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
from pydantic import validate_arguments
from pdk.mappedpdk import MappedPDK
from math import floor
from typing import Optional, Union
from pdk.util.custom_comp_utils import rename_ports_by_orientation, evaluate_bbox, prec_array, print_ports, to_float, move
from pdk.util.snap_to_grid import component_snap_to_grid, snap_to_2xgrid
from decimal import Decimal
from typing import Literal


@validate_arguments
def __error_check_order_layers(
    pdk: MappedPDK, glayer1: str, glayer2: str
) -> tuple[tuple[int, int], tuple[str, str]]:
    """correctly order layers (level1 should be lower than level2)"""
    pdk.activate()
    # check that the generic layers specfied can be routed between
    if not all([pdk.is_routable_glayer(met) for met in [glayer1, glayer2]]):
        raise ValueError("via_stack: specify between two routable layers")
    level1 = int(glayer1[-1]) if "met" in glayer1 else 0
    level2 = int(glayer2[-1]) if "met" in glayer2 else 0
    if level1 > level2:
        level1, level2 = level2, level1
        glayer1, glayer2 = glayer2, glayer1
    # check that all layers needed between glayer1-glayer2 are present
    required_glayers = [glayer2]
    for level in range(level1,level2):
        via_name = "mcon" if level==0 else "via"+str(level)
        layer_name = glayer1 if level==0 else "met"+str(level)
        required_glayers += [via_name,layer_name]
    pdk.has_required_glayers(required_glayers)
    return ((level1,level2),(glayer1,glayer2))


@validate_arguments
def __get_layer_dim(pdk: MappedPDK, glayer: str, mode: Literal["both","above","below"]="both") -> float:
	"""Returns the required dimension of a routable layer in a via stack
	glayer is the routable glayer
	mode is one of [both,below,above]
	This specfies the vias to consider.
	****enclosure rules of the via above and below are considered by default, via1<->met2<->via2
	****using below specfier only considers the enclosure rules for the via below, via1<->met2
	****using above specfier only considers the enclosure rules for the via above, met2<->via2
	****specfying both or below for active/poly layer is valid, function knows to ignore below
	"""
	# error checking
	if not pdk.is_routable_glayer(glayer):
		raise ValueError("__get_layer_dim: glayer must be a routable layer")
	# split into above rules and below rules
	consider_above = (mode=="both" or mode=="above")
	consider_below = (mode=="both" or mode=="below")
	is_lvl0 = any([hint in glayer for hint in ["poly","active"]])
	layer_dim=0
	if consider_below and not is_lvl0:
		via_below = "mcon" if glayer=="met1" else "via"+str(int(glayer[-1])-1)
		layer_dim = pdk.get_grule(via_below)["width"] + 2*pdk.get_grule(via_below,glayer)["min_enclosure"]
	if consider_above:
		via_above = "mcon" if is_lvl0 else "via"+str(glayer[-1])
		layer_dim = max(layer_dim, pdk.get_grule(via_above)["width"] + 2*pdk.get_grule(via_above,glayer)["min_enclosure"])
	layer_dim = max(layer_dim, pdk.get_grule(glayer)["min_width"])
	return layer_dim


@cell
def via_stack(
    pdk: MappedPDK,
    glayer1: str,
    glayer2: str,
    centered: bool = True,
    fullbottom: bool = False,
    fulltop: bool = False,
    assume_bottom_via: bool = False,
    same_layer_behavior: Literal["lay_nothing","min_square"] = "lay_nothing"
) -> Component:
    """produces a single via stack between two layers that are routable (metal, poly, or active)
    
    args:
    pdk: MappedPDK is the pdk to use
    glayer1: str is the glayer to start on
    glayer2: str is the glayer to end on
    ****NOTE it does not matter what order you pass layers
    fullbottom: if True will lay the bottom layer all over the area of the viastack else makes minimum legal size
    assume_bottom_via: legalize viastack assuming the via underneath bottom met is present, e.g. if bottom met is met3, assume via2 is present
    fulltop: if True will lay the top layer all over the area of the viastack else makes minimum legal size
    ****NOTE: generator can figure out which layer is top and which is bottom (i.e. met5 is higher than met1)
    same_layer_behavior: sometimes (especially when used in other generators) it is unknown what two layers are specfied
    this option provides the generator with guidance on how to handle a case where same layer is given
    by default, (lay_nothing option) nothing is laid and an empty component is returned
    if min_square is specfied, a square of min_width * min_width is laid
    
    PORTS, some ports are not layed when it does not make sense (e.g. empty component):
    top_met_...all edges
    bottom_via_...all edges
    bottom_met_...all edges
    bottom_layer_...all edges (may be different than bottom met if on diff/poly)
    """
    ordered_layer_info = __error_check_order_layers(pdk, glayer1, glayer2)
    level1, level2 = ordered_layer_info[0]
    glayer1, glayer2 = ordered_layer_info[1]
    viastack = Component()
    # if same level return component with min_width rectangle on that layer
    if level1 == level2:
        if same_layer_behavior=="lay_nothing":
            return viastack
        min_square = viastack << rectangle(size=2*[pdk.get_grule(glayer1)["min_width"]],layer=pdk.get_glayer(glayer1), centered=centered)
        # update ports
        if level1==0:# both poly or active
            viastack.add_ports(min_square.get_ports_list(),prefix="bottom_layer_")
        else:# both mets
            viastack.add_ports(min_square.get_ports_list(),prefix="top_met_")
            viastack.add_ports(min_square.get_ports_list(),prefix="bottom_met_")
    else:
        ports_to_add = dict()
        for level in range(level1,level2+1):
            via_name = "mcon" if level==0 else "via"+str(level)
            layer_name = glayer1 if level==0 else "met"+str(level)
            # get layer sizing
            mode = "below" if level==level2 else ("above" if level==level1 else "both")
            mode = "both" if assume_bottom_via and level==level1 else mode
            layer_dim = __get_layer_dim(pdk, layer_name, mode=mode)
            # place met/via, do not place via if on top layer
            if level != level2:
                via_dim = pdk.get_grule(via_name)["width"]
                via_ref = viastack << rectangle(size=[via_dim,via_dim],layer=pdk.get_glayer(via_name), centered=True)
            lay_ref = viastack << rectangle(size=[layer_dim,layer_dim],layer=pdk.get_glayer(layer_name), centered=True)
            # update ports
            if layer_name == glayer1:
                ports_to_add["bottom_layer_"] = lay_ref.get_ports_list()
                ports_to_add["bottom_via_"] = via_ref.get_ports_list()
            if (level1==0 and level==1) or (level1>0 and layer_name==glayer1):
                ports_to_add["bottom_met_"] = lay_ref.get_ports_list()
            if layer_name == glayer2:
                ports_to_add["top_met_"] = lay_ref.get_ports_list()
        # implement fulltop and fullbottom options. update ports_to_add accordingly 
        if fullbottom:
            bot_ref = viastack << rectangle(size=evaluate_bbox(viastack),layer=pdk.get_glayer(glayer1), centered=True)
            if level1!=0:
                ports_to_add["bottom_met_"] = bot_ref.get_ports_list()
            ports_to_add["bottom_layer_"] = bot_ref.get_ports_list()
        if fulltop:
            ports_to_add["top_met_"] = (viastack << rectangle(size=evaluate_bbox(viastack),layer=pdk.get_glayer(glayer2), centered=True)).get_ports_list()
        # add all ports in ports_to_add
        for prefix, ports_list in ports_to_add.items():
            viastack.add_ports(ports_list,prefix=prefix)
        # move SW corner to 0,0 if centered=False
        if not centered:
            viastack = move(viastack,(viastack.xmax,viastack.ymax))
    return rename_ports_by_orientation(viastack.flatten())


@cell
def via_array(
    pdk: MappedPDK,
    glayer1: str,
    glayer2: str,
    size: tuple[float,float] = (4.0, 1.0),
    minus1: bool = False,
    lay_bottom: bool = False
) -> Component:
    """Fill a region with vias. Will automatically decide num rows and columns
    args:
    pdk: MappedPDK is the pdk to use
    glayer1: str is the glayer to start on
    glayer2: str is the glayer to end on
    lay_bottom: bool if true will lay bottom met all over size (by default only lays top met all over size)
    ****NOTE it does not matter what order you pass layers
    ****NOTE will not lay poly or active but will lay metals
    size: tuple is the (width, hieght) of the area to enclose
    ****NOTE: the size will be the dimensions of the top metal
    minus1: if true removes 1 via from rows/cols num vias 
    ****use if you want extra space at the edges of the array
    ports (one port for each edge):
    top_met_...all edges
    bottom_met_...all edges (only if lay_bottom is specified)
    """
    size = snap_to_2xgrid(size)
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
    # error check size
    viadim = 2*Decimal(str(viastack.xmax))
    for i, dim in enumerate(size):
        if Decimal(str(to_float(viadim))) > Decimal(str(to_float(dim))):
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
        absolute_spacing=True
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
    from pdk.util.standard_main import pdk, parser
    from pdk.util.custom_comp_utils import print_ports
    from pathlib import Path

    # default behavoir is to run one design and exit
    parser.add_argument("--all", "-a", action="store_true", help="runs all tests")
    parser.add_argument("--viastack", "-s", action="store_true", help="runs all via_stack tests")
    parser.add_argument("--viaarray", "-v", action="store_true", help="runs all via_array tests")
    parser.add_argument("--write", "-w", help="writes all gds files to directory specfied")
    parser.add_argument("--ports", action="store_true", help="print ports")
    args = parser.parse_args()
    # run comps
    comps = list()
    if args.viaarray or args.all:
        layers = ["poly", "met1", "met2", "met3"]
        for lay1 in layers:
            for lay2 in layers:
                comps.append(via_array(pdk, lay1, lay2, lay_bottom=True))
    elif args.viastack or args.all:
        layers = ["poly", "met1", "met2", "met3"]
        for lay1 in layers:
            for lay2 in layers:
                comps.append(via_stack(pdk, lay1, lay2,fullbottom=True,fulltop=True))
    else:
        myarray = via_array(pdk, "poly", "met2",size=(5,4))
    # show and write (if write is specfied)
    if args.write:
        gds_write_path = Path(args.write)
        if not gds_write_path.is_dir():
            raise ValueError("gds write must be a dir path")
        for comp in comps:
            comp.write_gds(comp.name+".gds")
    for comp in comps:
        comp.show()
    # print_ports
    if args.ports:
        for comp in comps:
            print_ports(myarray)
