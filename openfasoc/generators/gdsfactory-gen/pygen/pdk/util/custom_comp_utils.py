from pydantic import validate_arguments
from gdsfactory.snap import snap_to_grid
from gdsfactory.typings import Component, ComponentReference
from gdsfactory.components.rectangle import rectangle
from gdsfactory.port import Port
from typing import Callable, Union, Optional,Iterable
from decimal import Decimal
from gdsfactory.functions import transformed

@validate_arguments
def rename_component_ports(custom_comp: Component, rename_function: Callable[[str, Port], str]) -> Component:
    """uses rename_function(str, Port) -> str to decide which ports to rename.
    rename_function accepts the current port name (string) and current port (Port) then returns the new port name
    rename_function can return new name = current port name, in which case the name will not change
    rename_function should raise error if custom requirments for rename are not met
    if you want to pass additional args to rename_function, implement a functor
    custom_comp is the components to modify. the modified component is returned
    """
    names_to_modify = list()
    # find ports and get new names
    for pname, pobj in custom_comp.ports.items():
        # error checking
        if not pname == pobj.name:
            raise ValueError("component may have an invalid ports dict")
        
        new_name = rename_function(pname, pobj)
        
        names_to_modify.append((pname,new_name))
    # modify names
    for namepair in names_to_modify:
        if namepair[0] in custom_comp.ports.keys():
            portobj = custom_comp.ports.pop(namepair[0])
            portobj.name = namepair[1]
            custom_comp.ports[namepair[1]] = portobj
        else:
            raise KeyError("name "+str(namepair[0])+" not in component ports")
    # returns modified component/component ref
    return custom_comp


@validate_arguments
def rename_ports_by_orientation__call(old_name: str, pobj: Port) -> str:
	"""internal implementation of port orientation rename"""
	if not "_" in old_name:
		raise ValueError("portname must contain underscore \"_\" " + old_name)
	# get new suffix (port orientation)
	new_suffix = None
	angle = pobj.orientation % 360 if pobj.orientation is not None else 0
	angle = round(angle)
	if angle <= 45 or angle >= 315:
		new_suffix = "E"
	elif angle <= 135 and angle >= 45:
		new_suffix = "N"
	elif angle <= 225 and angle >= 135:
		new_suffix = "W"
	else:
		new_suffix = "S"
	# construct new name
	old_str_split = old_name.rsplit("_", 1)
	old_str_split[1] = new_suffix
	new_name = "_".join(old_str_split)
	return new_name

@validate_arguments
def rename_ports_by_orientation(custom_comp: Component) -> Component:
    """replaces the last part of the port name 
    (after the last underscore) with a direction
    direction is one of N,E,S,W
    returns the modified component
    """
    return rename_component_ports(custom_comp, rename_ports_by_orientation__call)


class rename_ports_by_list__call: 
    def __init__(self, replace_list: list[tuple[str,str]] = []): 
        self.replace_list = dict(replace_list)
        self.replace_history = dict.fromkeys(self.replace_list.keys())
        for keyword in self.replace_history:
            self.replace_history[keyword] = 0
    @validate_arguments
    def __call__(self, old_name: str, pobj: Port) -> str:
        for keyword, newname in self.replace_list.items():
            if keyword in old_name:
                self.replace_history[keyword] += 1
                return newname + str(self.replace_history[keyword])
        return old_name

@validate_arguments
def rename_ports_by_list(custom_comp: Component, replace_list: list[tuple[str,str]]) -> Component:
    """replace_list is a list of tuple(string, string)
    if a port name contains tuple[0], the port will be renamed to tuple[1]
    if tuple[1] is None or empty string raise error
    when anaylzing a single port, if multiple keywords from the replace_list are found, first match is returned
    since we cannot have duplicate port names, different ports that end up with the same name get numbered"""
    rename_func = rename_ports_by_list__call(replace_list)
    return rename_component_ports(custom_comp, rename_func)


@validate_arguments
def add_ports_perimeter(custom_comp: Component, layer: tuple[int, int], prefix: Optional[str] = "_") -> Component:
    """adds ports to the outside perimeter of a cell
    custom_comp = component to add ports to (returns the modified component)
    layer = will extract this layer and take it as the bbox, ports will also be on this layer
    prefix = prefix to add to the port names. Adds an underscore by default
    """
    if "_" not in prefix:
        raise ValueError("you need underscore char in prefix")
    compbbox = custom_comp.extract(layers=(layer,)).bbox
    width = compbbox[1][0] - compbbox[0][0]
    height = compbbox[1][1] - compbbox[0][1]
    size = (width, height)
    temp = Component()
    swref = temp << rectangle(layer=layer,size=size)
    swref.move(destination=(custom_comp.bbox[0]))
    temp.add_ports(swref.get_ports_list(),prefix=prefix)
    temp = rename_ports_by_orientation(temp)
    custom_comp.add_ports(temp.get_ports_list())
    return custom_comp


@validate_arguments
def print_ports(custom_comp: Union[Component, ComponentReference], names_only: Optional[bool] = True) -> None:
    """prints ports in comp in a nice way
    custom_comp = component to use
    names_only = only print names if True else print name and port
    """
    for key,val in custom_comp.ports.items():
        print(key)
        if not names_only:
            print(val)
            print()


@validate_arguments
def evaluate_bbox(custom_comp: Union[Component, ComponentReference], return_decimal: Optional[bool]=False) -> tuple[Union[float,Decimal],Union[float,Decimal]]:
	"""returns the length and height of a component like object"""
	compbbox = custom_comp.bbox
	width = abs(Decimal(str(compbbox[1][0])) - Decimal(str(compbbox[0][0])))
	height = abs(Decimal(str(compbbox[1][1])) - Decimal(str(compbbox[0][1])))
	if return_decimal:
		return (width,height)
	return (float(width),float(height))


@validate_arguments
def move(custom_comp: Union[Port, ComponentReference, Component], offsetxy: Optional[tuple[float,float]] = 0, destination: Optional[tuple[Optional[float],Optional[float]]]=None) -> Union[Port, ComponentReference, Component]:
	"""moves custom_comp by offset[0]=x offset, offset[1]=y offset
	destination (x,y) if not none overrides offset option
	returns the modified custom_comp
	"""
	#xcenter = custom_comp.xmin + evaluate_bbox(custom_comp)[0]/2 if isinstance(custom_comp, Component) else custom_comp.center[0]
	#ycenter = custom_comp.ymin + evaluate_bbox(custom_comp)[1]/2 if isinstance(custom_comp, Component) else custom_comp.center[1]
	if destination is not None:
		xoffset = destination[0] - custom_comp.center[0] if destination[0] is not None else 0
		yoffset = destination[1] - custom_comp.center[1] if destination[1] is not None else 0
	if isinstance(custom_comp, Port):
		if destination is None:
			custom_comp.move(offsetxy)
		else:
			custom_comp.move((xoffset,yoffset))
	elif isinstance(custom_comp, ComponentReference):
		if destination is None:
			custom_comp.movex(offsetxy[0]).movey(offsetxy[1])
		else:
			custom_comp.movex(xoffset).movey(yoffset)
	elif isinstance(custom_comp, Component):
		ref = custom_comp.copy().ref()
		# this is a recursive call but with type=component reference
		ref = move(ref, offsetxy, destination)
		custom_comp = transformed(ref).copy()
	return custom_comp


@validate_arguments
def movex(custom_comp: Union[Port, ComponentReference, Component], offsetx: Optional[float] = 0, destination: Optional[float]=None) -> Union[Port, ComponentReference, Component]:
	"""moves custom_comp by offsetx in the x direction
	returns the modified custom_comp
	"""
	if destination is not None:
		destination = (destination, None)
	return move(custom_comp, (offsetx,0),destination)


@validate_arguments
def movey(custom_comp: Union[Port, ComponentReference, Component], offsety: Optional[float] = 0, destination: Optional[float]=None) -> Union[Port, ComponentReference, Component]:
	"""moves custom_comp by offsety in the y direction
	returns the modified custom_comp
	"""
	if destination is not None:
		destination = (None, destination)
	return move(custom_comp, (0,offsety),destination)


@validate_arguments
def get_orientation(orientation: Union[int,float,str], int_only: Optional[bool]=False) -> Union[float,int,str]:
	"""returns the angle corresponding to port orientation
	orientation must contain N/n,E/e,S/s,W/w
	e.g. all the follwing are valid:
	N/n or N/north,E/e or E/east,S/s or S/south, W/w or W/west
	if int_only, will return int regardless of input type,
	else will return the opposite type of that given
	(i.e. will return str if given int/float and int if given str)
	"""
	if isinstance(orientation,str):
		orientation = orientation.lower()
		if "n" in orientation:
			return 90
		elif "e" in orientation:
			return 0
		elif "w" in orientation:
			return 180
		elif "s" in orientation:
			return 270
		else:
			raise ValueError("orientation must contain N/n,E/e,S/s,W/w")
	else:# must be a float/int
		orientation = int(orientation)
		if int_only:
			return orientation
		orientation_index = int((orientation % 360) / 90)
		orientations = ["E","N","W","S"]
		try:
			orientation = orientations[orientation_index]
		except IndexError as e:
			raise ValueError("orientation must be 0,90,180,270 to use this function")
		return orientation


@validate_arguments
def assert_is_manhattan(edges: Union[list[Port],Port]) -> bool:
	"""raises assertionerror if port is not vertical or horizontal"""
	if isinstance(edges, Port):
		edges = [edges]
	for edge in edges:
		if round(edge.orientation) % 90 != 0:
			raise AssertionError("edge is not vertical or horizontal")
	return True


@validate_arguments
def assert_ports_perpindicular(edge1: Port, edge2: Port) -> bool:
	"""raises assertionerror if edges are not perindicular"""
	or1 = round(edge1.orientation)
	or2 = round(edge2.orientation)
	angle_difference = abs(round(or1-or2))
	if angle_difference != 90 and angle_difference != 270:
		raise AssertionError("edges are not perpindicular")
	return True


@validate_arguments
def set_orientation(custom_comp: Port, orientation: Union[float, int, str], flip180: Optional[bool]=False) -> Port:
	"""creates a new port with the desired orientation and returns the new port"""
	if isinstance(orientation,str):
		orientation = get_orientation(orientation, int_only=True)
	if flip180:
		orientation = (orientation + 180) % 360
	newport = Port(
		name = custom_comp.name,
		center = custom_comp.center,
		orientation = orientation,
		parent = custom_comp.parent,
		port_type = custom_comp.port_type,
		cross_section = custom_comp.cross_section,
		shear_angle = custom_comp.shear_angle,
		layer = custom_comp.layer,
		width = custom_comp.width,
	)
	return newport


@validate_arguments
def set_port_width(custom_comp: Port, width: float) -> Port:
	"""creates a new port with the desired width and returns the new port"""
	newport = Port(
		name = custom_comp.name,
		center = custom_comp.center,
		orientation = custom_comp.orientation,
		parent = custom_comp.parent,
		port_type = custom_comp.port_type,
		cross_section = custom_comp.cross_section,
		shear_angle = custom_comp.shear_angle,
		layer = custom_comp.layer,
		width = width,
	)
	return newport


@validate_arguments
def align_comp_to_port(custom_comp: Union[Component,ComponentReference], align_to: Port, alignment: Optional[tuple[str,str]] = None) -> ComponentReference:
	"""Returns component reference of component aligned to port as specifed
	custom_comp = component to align properly
	align_to = Port to align to
	***NOTE, if left None, function will align component to outside and center of port (based on port orientation)
	alignment = tuple(str,str) = (xalign,yalign)
	****xalign = either l/left or r/right or c/center. component will be flush to right or left side of port or centered
	****yalgin = either t/top or b/bottom or c/center. top or bottom edge or center of component will align with port top/bottom/center
	"""
	if isinstance(custom_comp, Component):
		try:
			custom_comp.is_unlocked()
		except ValueError:
			custom_comp = custom_comp.copy()
	# error checks and decide orientation if None
	if alignment is None:
		if round(align_to.orientation) == 0:# facing east
			xalign = "r"
			yalign = "c"
		elif round(align_to.orientation) == 180:# facing west
			xalign = "l"
			yalign = "c"
		elif round(align_to.orientation) == 270:# facing south
			xalign = "c"
			yalign = "b"
		elif round(align_to.orientation) == 90:#facing north
			xalign = "c"
			yalign = "t"
		else:
			raise ValueError("port must be vertical or horizontal")
	else:
		xalign = alignment[0]
		yalign = alignment[1]
	# setup
	is_EW = bool(round(align_to.orientation + 90) % 180)
	xalign = xalign.lower()
	yalign = yalign.lower()
	if isinstance(custom_comp, Component):
		comp_ref = custom_comp.ref_center()
		comp_ref.move(align_to.center)
	else:
		comp_ref = custom_comp
		move(comp_ref, destination=tuple(align_to.center))
	width = align_to.width
	xdim = evaluate_bbox(custom_comp)[0]
	ydim = evaluate_bbox(custom_comp)[1]
	#xalign
	xmov = 0
	if "l" in xalign:
		if not is_EW:
			xmov = -1 * abs((width - xdim)/2)
		else:
			xmov = -1 * abs(xdim/2)
	elif "r" in xalign:
		if not is_EW:
			xmov = abs((width - xdim)/2)
		else:
			xmov = abs(xdim/2)
	elif "c" in xalign:
		pass
	else:
		raise ValueError("please specify valid x alignment of l/r/c")
	# yalign
	ymov = 0
	if "t" in yalign:
		if not is_EW:
			ymov = abs(ydim/2)
		else:
			ymov = abs((width - ydim)/2)
	elif "b" in yalign:
		if not is_EW:
			ymov = -1 * abs(ydim/2)
		else:
			ymov = -1 * abs((width - ydim)/2)
	elif "c" in yalign:
		pass
	else:
		raise ValueError("please specify valid x alignment of l/r/c")
	# move and return
	return comp_ref.movex(xmov).movey(ymov)


@validate_arguments
def to_decimal(elements: Union[tuple,list,float,int,str]):
	"""converts all elements of list like object into decimals
	or converts single num into decimal"""
	if not isinstance(elements,Iterable):
		return Decimal(str(elements))
	else:
		elements = list(elements)
	for i, element in enumerate(elements):
		if isinstance(element,Union[int,float]):
			elements[i] = Decimal(str(element))
	return elements

@validate_arguments
def to_float(elements: Union[tuple,list,Decimal,float]):
	"""converts all elements of list like object into floats and snaps to grid
	or converts single decimal into floats"""
	if not isinstance(elements,Iterable):
		return snap_to_grid(float(elements))
	else:
		elements = list(elements)
	for i, element in enumerate(elements):
		if isinstance(element, Union[float,Decimal]):
			elements[i] = snap_to_grid(float(element))
	return elements

@validate_arguments
def prec_array(custom_comp: Component, rows: int, columns: int, spacing: tuple[Union[float,Decimal],Union[float,Decimal]], absolute_spacing: Optional[bool]=False) -> Component:
	"""instead of using the component.add_array function, if you are having grid snapping issues try using this function
	works the same way as add_array but uses decimals and snaps to grid to mitigate grid snapping issues
	args
	custom_comp: Component type to make an array from
	columns: num cols in the array
	rows: num rows in the array
	absolute_spacing: the spacing mode of spacing variable
	spacing: IF absolute_spacing spacing BETWEEN elements in the array ELSE spacing BETWEEN ORIGINS of elements in the array
	****NOTE do not use negative spacing, instead specify absolute_spacing=True
	"""
	# make sure to work with decimals
	precspacing = list(spacing)
	for i in range(2):
		if isinstance(spacing[i],Union[int,float]):
			precspacing[i] = Decimal(str(spacing[i]))
	if not absolute_spacing:
		precspacing = [precspacing[i] + evaluate_bbox(custom_comp,True)[i] for i in range(2)]
	# create array
	precarray = Component()
	for colnum in range(columns):
		coldisp = colnum * precspacing[0]
		for rownum in range(rows):
			rowdisp = rownum * precspacing[1]
			cref = precarray << custom_comp
			cref.movex(to_float(coldisp)).movey(to_float(rowdisp))
			precarray.add_ports(cref.get_ports_list(),prefix=f"row{rownum}_col{colnum}_")
	return precarray.flatten()


@validate_arguments
def prec_center(custom_comp: Union[Component,ComponentReference], return_decimal: bool=False) -> tuple[Union[float,Decimal],Union[float,Decimal]]:
	"""instead of using component.ref_center() to get the center of a component,
	use this function which will return the correct offset to center a component
	returns (x,y) corrections
	if return_decimal=True, return in Decimal, otherwise return float"""
	correctmax = [dim/2 for dim in evaluate_bbox(custom_comp, True)]
	currentmax = to_decimal((custom_comp.xmax,custom_comp.ymax))
	correctionxy = [correctmax[i] - currentmax[i] for i in range(2)]
	if return_decimal:
		return correctionxy
	return to_float(correctionxy)

@validate_arguments
def prec_ref_center(custom_comp: Union[Component,ComponentReference], return_decimal: bool=False) -> tuple[Union[float,Decimal],Union[float,Decimal]]:
	"""instead of using component.ref_center() to get a ref to center at origin,
	use this function which will return a centered ref
	you can then run component.add(prec_ref_center(custom_comp)) to add the reference to your component
	returns component reference
	"""
	compref = custom_comp if isinstance(custom_comp, ComponentReference) else custom_comp.ref()
	xcor, ycor = prec_center(compref, False)
	return compref.movex(xcor).movey(ycor)
