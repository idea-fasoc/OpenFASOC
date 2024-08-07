from pydantic import validate_arguments
from gdsfactory.typings import Component, ComponentReference
from gdsfactory.components.rectangle import rectangle
from gdsfactory.port import Port
from typing import Callable, Union, Optional
from decimal import Decimal
from pathlib import Path
import pickle
from PrettyPrint import PrettyPrintTree
import math


@validate_arguments
def parse_direction(direction: Union[int, str]) -> int:
	"""returns 1,2,3,4 (W,N,E,S)

	Args:
		direction (int | str): a direction description either string or int
		****direction descrption could be north/south/east/west or left/right/up/down, etc.

	Returns:
		int: 1=W, 2=N, 3=E, 4=S
	"""
	if isinstance(direction, int):
		if direction<1 or direction>4:
			raise ValueError(f"direction was specified as int {direction}, but int directions are 1,2,3, or 4")
		else:
			return direction
	else:# direction is a string
		cmp = direction.strip().lower()[0]
		if cmp=="l" or cmp=="w" or cmp=="1":
			return 1
		elif cmp=="u" or cmp=="n" or cmp=="2":
			return 2
		elif cmp=="r" or cmp=="e" or cmp=="3":
			return 3
		elif cmp=="d" or cmp=="s" or cmp=="4":
			return 4
		else:
			raise ValueError(f"failed to parse direction string {direction}")


def proc_angle(angle: float) -> int:
	"""round an angle in degrees to nearest int and converts to an angle [-180,180]

	Args:
		angle (float): angle in degrees

	Returns:
		float: angle in degrees [-180,180]
	"""
	angle = round(angle)
	angle = angle % 360
	if angle > 180:
	    angle -= 360
	return angle


@validate_arguments
def ports_parallel(edge1: Port, edge2: Port) -> bool:
	"""returns True if the provided ports are parralel (same or 180degree opposite directions)
	Requires ports are manhattan
	Args:
		edge1 (Port)
		edge2 (Port)
	Returns:
		bool: True if the provided ports are parralel
	"""
	assert_port_manhattan([edge1,edge2])
	e1orientation = abs(proc_angle(edge1.orientation))
	e2orientation = abs(proc_angle(edge2.orientation))
	if e1orientation==e2orientation:
		return True
	if (e1orientation==180 and e2orientation==0) or (e1orientation==0 and e2orientation==180):
		return True
	return False


@validate_arguments
def ports_inline(edge1: Port, edge2: Port, abstolerance: float=0.1) -> bool:
	"""Check if two ports are inline within a tolerance.

	Args:
		edge1 (Port): The first port.
		edge2 (Port): The second port.
		abstolerance (float, optional): The absolute tolerance for inline check.. Defaults to 0.1.

	Returns:
		bool: True if the ports are inline within the given tolerance.
	"""
	# trivial cases and error checking
	assert_port_manhattan([edge1, edge2])
	if not(ports_parallel(edge1, edge2)):
		return False
	# given ports are parallel, determine coordinates of value
	e1orientation = abs(proc_angle(edge1.orientation))
	if e1orientation == 90:
		centers = sorted([edge1.center[0], edge2.center[0]])
	else:
		centers = sorted([edge1.center[1], edge2.center[1]])
	# determine if ports are inline within tolerance bounds
	return not(centers[0] < (centers[1] - abstolerance))



@validate_arguments
def rename_component_ports(custom_comp: Union[Component, ComponentReference], rename_function: Callable[[str, Port], str]) -> Union[Component, ComponentReference]:
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
	if not "_" in old_name and not any(old_name==edge for edge in ["e1","e2","e3","e4"]):
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
	# handle special case where no underscore and name is e1/2/3/4
	if any(old_name==edge for edge in ["e1","e2","e3","e4"]):
		return new_suffix
	# construct new name
	old_str_split = old_name.rsplit("_", 1)
	old_str_split[1] = new_suffix
	new_name = "_".join(old_str_split)
	return new_name

@validate_arguments
def rename_ports_by_orientation(custom_comp: Union[Component, ComponentReference]) -> Union[Component, ComponentReference]:
    """replaces the last part of the port name 
    (after the last underscore, unless name is e1/2/3/4) with a direction
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
				inst_id = self.replace_history[keyword]
				replace_name = newname + str(inst_id if inst_id else "")
				self.replace_history[keyword] += 1
				return replace_name
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


def remove_ports_with_prefix(custom_comp: Component, prefix: str) -> Component:
	"""remove all ports in custom_comp which begin with prefix"""
	# determine which ports to remove
	remove_list = list()
	for prt in custom_comp.ports.keys():
		if prt.startswith(prefix):
			remove_list.append(prt)
	# remove the ports
	for prt in remove_list:
		custom_comp.ports.pop(prt)
	return custom_comp


@validate_arguments
def add_ports_perimeter(custom_comp: Component, layer: tuple[int, int], prefix: Optional[str] = "_") -> Component:
	"""adds ports to the outside perimeter of a cell
	custom_comp = component to add ports to (returns the modified component)
	layer = will extract this layer and take it as the bbox, ports will also be on this layer
	prefix = prefix to add to the port names. Adds an underscore by default
	returns ports named by orientation
	"""
	if "_" not in prefix:
		raise ValueError("you need underscore char in prefix")
	compbbox = custom_comp.extract(layers=(layer,)).bbox
	width = compbbox[1][0] - compbbox[0][0]
	height = compbbox[1][1] - compbbox[0][1]
	custom_comp.add_port(name=prefix+"W",width=height,orientation=180,center=(compbbox[0][0],compbbox[0][1]+height/2),layer=layer,port_type="electrical")
	custom_comp.add_port(name=prefix+"N",width=width,orientation=90,center=(compbbox[0][0]+width/2,compbbox[1][1]),layer=layer,port_type="electrical")
	custom_comp.add_port(name=prefix+"E",width=height,orientation=0,center=(compbbox[1][0],compbbox[0][1]+height/2),layer=layer,port_type="electrical")
	custom_comp.add_port(name=prefix+"S",width=width,orientation=270,center=(compbbox[0][0]+width/2,compbbox[0][1]),layer=layer,port_type="electrical")
	return custom_comp


@validate_arguments
def get_orientation(orientation: Union[int,float,str], int_only: bool=False) -> Union[float,int,str]:
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
def assert_port_manhattan(edges: Union[list[Port],Port]) -> bool:
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
def set_port_orientation(custom_comp: Port, orientation: Union[float, int, str], flip180: Optional[bool]=False) -> Port:
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


def create_private_ports(custom_comp: Union[Component, ComponentReference], port_paths: Optional[Union[str,list[str]]] = None) -> list[Port]:
	"""returns a list with a copy ports for children of the port_paths specified
	the ports have _private appended
	Args:
		custom_comp (Component): comp to consider PortTree for
		port_paths (str, list[str], optional): path along the PortTree to consider. Defaults to None (all ports are copied)
		****NOTE: if a list is provided, then it will consider all paths in the list
	Returns:
		list[Port]: copies of all ports along port_path, these ports end with _private
	"""
	# arg setup
	bypass = port_paths is None
	if bypass:
		port_paths = []
	else:
		if isinstance(port_paths, str):
			port_paths = [port_paths]
	# find all matching ports
	ports_to_add = list()
	for port in custom_comp.get_ports_list():
		if any([port.name.startswith(port_path) for port_path in port_paths]) or bypass:
			ports_to_add.append(port.copy(name=port.name+"_private"))
	return ports_to_add

class PortTree:
	"""PortTree helps a glayout.flow.programmer visualize the ports in a component
	\"_\" should represent a level of hiearchy (much like a directory). think of this like psuedo directories
	Initialize a PortTree from a Component or ComponentReference
	then use self.ls to list all ports/subdirectories in a directory
	you can use self.print to prettyprint a port tree (uses pypi prettyprinttree package)

	You should not need to access the internal dictionary for the tree, but if you do:
	PortTree internally uses tuple[str, dict] = name:children as the node type
	since the PortTree is not a node type (PortTree is not a real tree class), the root node is: (self.name, self.tree)
	"""

	@validate_arguments
	def __init__(self, custom_comp: Union[Component, ComponentReference], name: Optional[str]=None):
		"""creates the tree structure from the ports where _ represent subdirectories
		credit -> chatGPT
		"""
		file_list = custom_comp.ports.keys()
		directory_tree = {}
		for file_path in file_list:
			path_components = file_path.split('_')
			current_dir = directory_tree
			for path_component in path_components:
				if path_component not in current_dir:
					current_dir[path_component] = {}
				current_dir = current_dir[path_component]
		self.tree = directory_tree
		self.name = name if name else custom_comp.name
	
	@validate_arguments
	def ls(self, file_path: Optional[str] = None) -> list[str]:
		"""tries to traverse the tree along the given path and prints all subdirectories in a psuedo directory
		if the path given is not found in the tree, raises KeyError
		path should not end with \"_\" char
		"""
		if file_path is None or len(file_path)==0:
			return list(self.tree.keys())
		path_components = file_path.split('_')
		current_dir = self.tree
		for path_component in path_components:
			if path_component not in current_dir:
				raise KeyError("Port path was not found")
			current_dir = current_dir[path_component]
		return list(current_dir.keys())
	
	@validate_arguments
	def save_to_disk(self, savedir: Union[Path, str]="./"):
		savedir = Path(savedir).resolve()
		savedir.mkdir(exist_ok=True,parents=True)
		if not savedir.is_dir():
			raise ValueError("no dir named" + str(savedir))
		with open(savedir / "porttree.pkl", 'wb') as outfile:
			pickle.dump(self, outfile)
	
	@classmethod
	def read_from_disk(cls, pklfile: Union[Path, str]):
		pklfile = Path(pklfile).resolve()
		if not pklfile.is_file():
			raise ValueError("no file named" + str(pklfile))
		with open(str(pklfile), 'rb') as infile:
			return pickle.load(infile)
	
	def get_children(self, node: tuple[str, dict]) -> list[tuple[str, dict]]:
		"""access children of internal tree node (node might be a PortTree)"""
		node_dict = node[1] if isinstance(node, tuple) else self.tree
		return node_dict.items()
		
	
	def get_val(self, node: tuple[str, dict]) -> str:
		"""returns value of a node, (node might be a PortTree)"""
		return node[0] if isinstance(node, tuple) else self.name
	
	def get_node(self, port_path: Optional[str] = None) -> tuple[str, dict]:
		"""get a node name and children from a port_path
		Args:
			port_path (str, optional): psuedo path to a node in this PortTree. Defaults to None (returns root of the tree)
		Returns:
			list[tuple[str, dict]]: name and children of the specified node
		"""
		if port_path is None:
			return self.name, self.tree
		else:
			current_children = self.tree
			current_name = self.name
			for node in port_path.split("_"):
				current_children = current_children[node]
				current_name = node
		return current_name, current_children

	
	def print(self, savetofile: bool=True, default_opts: bool=True, depth: Optional[int]=None, outfile_name: Optional[str]=None, **kwargs):
		"""prints output to terminal directly using prettyprinttree pypi package
		args:
		depth = max depth to print. this is a kwarg but since it so common, it should be specfied from depth arg
		savetofile = saves print output to a txt file rather than printing to terminal (easier to view, but without nice formatting)
		default_opts = bool=True results in using glayout.flow.recommended default print arguments
		kwargs -> kwargs are prettyprint options passed directly to prettyprint.
		****NOTE: kwargs override all other options
		"""
		depth = int(depth) if (depth is not None and depth>0) else -1
		extra_kwargs = {}
		if default_opts:
			extra_kwargs.update({"default_orientation": True})
		if savetofile:
			extra_kwargs.update({"return_instead_of_print":savetofile, "color":None, "border":True, "default_orientation": True})
		extra_kwargs.update(kwargs)
		pt = PrettyPrintTree(self.get_children, self.get_val, max_depth=depth, **extra_kwargs)
		rtrstr = pt(self)
		if rtrstr:
			outfile_name = "outputtree.txt" if outfile_name is None else outfile_name
			with open(outfile_name,"w") as outputfile:
				outputfile.write(rtrstr)


def print_port_tree_all_cells() -> list:
	"""print the PortTree for most of the glayout.flow.cells and save as a text file.
	returns a list of components
	"""
	from glayout.flow.primitives.via_gen import via_stack, via_array
	from glayout.flow.opamp import opamp
	from glayout.flow.primitives.mimcap import mimcap
	from glayout.flow.primitives.mimcap import mimcap_array
	from glayout.flow.primitives.guardring import tapring
	from glayout.flow.primitives.fet import multiplier, nmos, pmos
	from glayout.flow.diff_pair import diff_pair
	from glayout.flow.routing.straight_route import straight_route
	from glayout.flow.routing.c_route import c_route
	from glayout.flow.routing.L_route import L_route
	from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as pdk
	from gdsfactory.port import Port
	print("saving via_stack, via_array, opamp, mimcap, mimcap_array, tapring, multiplier, nmos, pmos, diff_pair, straight_route, c_route, L_route Ports to txt files")
	celllist = list()
	celllist.append(["via_stack",via_stack(pdk, "active_diff","met5")])
	celllist.append(["viaarray", via_array(pdk, "active_diff","met5", num_vias=(2,3))])
	celllist.append(["mimcap",mimcap(pdk)])
	celllist.append(["mimcap_array",mimcap_array(pdk, 2, 3)])
	celllist.append(["tapring",tapring(pdk)])
	celllist.append(["multiplier",multiplier(pdk,"n+s/d")])
	celllist.append(["nmos", nmos(pdk,fingers=2,multipliers=2)])
	celllist.append(["pmos", pmos(pdk,fingers=2,multipliers=2)])
	celllist.append(["diff_pair",diff_pair(pdk)])
	psuedo_porta = Port("bottom",90,(0,0),2,layer=pdk.get_glayer("met2"))
	psuedo_portb = Port("top",0,(5,10),2.5,layer=pdk.get_glayer("met5"))
	psuedo_porta = Port("right",90,(10,10),2,layer=pdk.get_glayer("met2"))
	celllist.append(["straight_route",straight_route(pdk,psuedo_porta,psuedo_portb)])
	celllist.append(["L_route",L_route(pdk, psuedo_porta, psuedo_portb)])
	celllist.append(["c_route",c_route(pdk, psuedo_porta, psuedo_porta,extension=2)])
	celllist.append(["opamp",opamp(pdk)])
	for name, py_cell in celllist:
		from glayout import __version__ as glayoutinfo
		vglayout = str(glayoutinfo)
		PortTree(py_cell,name=name).print(depth=5,outfile_name=name+"_v"+vglayout+"_tree.txt",default_orientation=True)
	return celllist
