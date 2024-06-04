from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
from pydantic import validate_arguments
from glayout.flow.pdk.mappedpdk import MappedPDK
from math import floor
from typing import Optional, Union
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, prec_array, to_float, move, prec_ref_center, to_decimal
from glayout.flow.pdk.util.port_utils import rename_ports_by_orientation, print_ports
from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid
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
	This specfies the vias to consider. (layer dims may be made smaller if its possible to ignore top/bottom vias)
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


@validate_arguments
def __get_viastack_minseperation(pdk: MappedPDK, viastack: Component, ordered_layer_info) -> tuple[float,float]:
    """internal use: return absolute via separation and top_enclosure (top via to top met enclosure)"""
    get_sep = lambda _pdk, rule, _lay_, comp : (rule+2*comp.extract(layers=[_pdk.get_glayer(_lay_)]).xmax)
    level1, level2 = ordered_layer_info[0]
    glayer1, glayer2 = ordered_layer_info[1]
    mcon_rule = pdk.get_grule("mcon")["min_separation"]
    via_spacing = [] if level1 else [get_sep(pdk,mcon_rule,"mcon",viastack)]
    level1_met = level1 if level1 else level1 + 1
    top_enclosure = 0
    for level in range(level1_met, level2):
        met_glayer = "met" + str(level)
        via_glayer = "via" + str(level)
        mrule = pdk.get_grule(met_glayer)["min_separation"]
        vrule = pdk.get_grule(via_glayer)["min_separation"]
        via_spacing.append(get_sep(pdk, mrule,met_glayer,viastack))
        via_spacing.append(get_sep(pdk, vrule,via_glayer,viastack))
        if level == (level2-1):
            top_enclosure = pdk.get_grule(glayer2,via_glayer)["min_enclosure"]
    via_spacing = pdk.snap_to_2xgrid(max(via_spacing),return_type="float")
    top_enclosure = pdk.snap_to_2xgrid(top_enclosure,return_type="float")
    return pdk.snap_to_2xgrid([via_spacing, 2*top_enclosure], return_type="float")


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
    The via_stack produced is always a square (hieght=width)
    
    args:
    pdk: MappedPDK is the pdk to use
    glayer1: str is the glayer to start on
    glayer2: str is the glayer to end on
    ****NOTE it does not matter what order you pass layers
    fullbottom: if True will lay the bottom layer all over the area of the viastack else makes minimum legal size (ignores min area)
    assume_bottom_via: legalize viastack assuming the via underneath bottom met is present, e.g. if bottom met is met3, assume via2 is present
    fulltop: if True will lay the top layer all over the area of the viastack else makes minimum legal size (ignores min area)
    ****NOTE: generator can figure out which layer is top and which is bottom (i.e. met5 is higher than met1)
    same_layer_behavior: sometimes (especially when used in other generators) it is unknown what two layers are specfied
    this option provides the generator with guidance on how to handle a case where same layer is given
    by default, (lay_nothing option) nothing is laid and an empty component is returned
    if min_square is specfied, a square of min_width * min_width is laid
    
    ports, some ports are not layed when it does not make sense (e.g. empty component):
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
    size: Optional[tuple[Optional[float],Optional[float]]] = None,
    minus1: bool = False,
    num_vias: Optional[tuple[Optional[int],Optional[int]]] = None,
    lay_bottom: bool = True,
    fullbottom: bool = False,
    no_exception: bool = False,
    lay_every_layer: bool = False
) -> Component:
    """Fill a region with vias. Will automatically decide num rows and columns
    args:
    pdk: MappedPDK is the pdk to use
    glayer1: str is the glayer to start on
    glayer2: str is the glayer to end on
    lay_bottom: bool if true will lay bottom layer (by default only lays top layer)
    ****NOTE it does not matter what order you pass layers
    ****NOTE will lay bottom only over the minimum area required to make legal
    size: tuple is the (width, hieght) of the area to enclose
    ****NOTE: the size will be the dimensions of the top metal
    minus1: if true removes 1 via from rows/cols num vias 
    ****use if you want extra space at the edges of the array, does not apply to num_vias
    num_vias: number of rows/cols in the via array. Overrides size option
    ****NOTE: you can specify size for one dim and num_vias for another by setting one element to None 
    ****NOTE: num_vias overides size option
    fullbottom: True specifies that the bottom layer should extend over the entire via_array region
    ****NOTE: fullbottom=True implies lay_bottom and overrides if False
    no_exception: True specfies that the function should change size such that min size is met
    lay_every_layer: True specifies that every layer between glayer1 and glayer2 should be layed in full (not just the vias).
    ****NOTE: this implies lay_bottom
    
    ports, some ports are not layed when it does not make sense (e.g. empty component):
    top_met_...all edges
    bottom_lay_...all edges (only if lay_bottom is specified)
    array_...all ports associated with via array
    """
    # setup
    ordered_layer_info = __error_check_order_layers(pdk, glayer1, glayer2)
    level1, level2 = ordered_layer_info[0]
    glayer1, glayer2 = ordered_layer_info[1]
    viaarray = Component()
    # if same level return empty component
    if level1 == level2:
        return viaarray
    # figure out min space between via stacks
    viastack = via_stack(pdk, glayer1, glayer2)
    viadim = evaluate_bbox(viastack)[0]
    via_abs_spacing, top_enclosure = __get_viastack_minseperation(pdk, viastack, ordered_layer_info)
    # error check size and determine num_vias, cnum_vias[0]=x, cnum_vias[1]=y
    cnum_vias = 2*[None]
    for i in range(2):
        if (num_vias[i] if num_vias else False):
            cnum_vias[i] = num_vias[i]
        elif (size[i] if size else False):
            dim = pdk.snap_to_2xgrid(size[i],return_type="float")
            fltnum = floor((dim - top_enclosure) / (via_abs_spacing)) or 1
            fltnum = 1 if fltnum < 1 else fltnum
            cnum_vias[i] = ((fltnum - 1) or 1) if minus1 else fltnum
            if to_decimal(viadim) > to_decimal(dim) and not no_exception:
                raise ValueError(f"via_array,size:dim#{i}={dim} < {viadim}")
        else:
            raise ValueError("give at least 1: num_vias or size for each dim")
    # create array
    viaarray_ref = prec_ref_center(prec_array(viastack, columns=cnum_vias[0], rows=cnum_vias[1], spacing=2*[via_abs_spacing],absolute_spacing=True))
    viaarray.add(viaarray_ref)
    viaarray.add_ports(viaarray_ref.get_ports_list(),prefix="array_")
    # find the what should be used as full dims
    viadims = evaluate_bbox(viaarray)
    if not size:
        size = 2*[None]
    size = [size[i] if size[i] else viadims[i] for i in range(2)]
    size = [viadims[i] if viadims[i]>size[i] else size[i] for i in range(2)]
    # place bottom layer and add bot_lay_ ports
    if lay_bottom or fullbottom or lay_every_layer:
        bdims = evaluate_bbox(viaarray.extract(layers=[pdk.get_glayer(glayer1)]))
        bref = viaarray << rectangle(size=(size if fullbottom else bdims), layer=pdk.get_glayer(glayer1), centered=True)
        viaarray.add_ports(bref.get_ports_list(), prefix="bottom_lay_")
    else:
        viaarray = viaarray.remove_layers(layers=[pdk.get_glayer(glayer1)])
    # place top met
    tref = viaarray << rectangle(size=size, layer=pdk.get_glayer(glayer2), centered=True)
    viaarray.add_ports(tref.get_ports_list(), prefix="top_met_")
    # place every layer in between if lay_every_layer
    if lay_every_layer:
        for i in range(level1+1,level2):
            bdims = evaluate_bbox(viaarray.extract(layers=[pdk.get_glayer(f"met{i}")]))
            viaarray << rectangle(size=bdims, layer=pdk.get_glayer(f"met{i}"), centered=True)
    return component_snap_to_grid(rename_ports_by_orientation(viaarray))


