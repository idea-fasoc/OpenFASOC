from gdsfactory.typings import Component
from pydantic import validate_arguments
from typing import Optional
from gdsfactory.pdk import get_grid_size
from tempfile import TemporaryDirectory
from pathlib import Path
from gdsfactory.read.import_gds import import_gds

@validate_arguments
def component_snap_to_grid(comp: Component, nm: Optional[int]=None) -> Component:
	"""snaps all polygons in component to grid and correctly updates ports
	comp = the component to snap to grid
	NOTE this function will flatten the component
	nm the grid to snap to, defaults to active pdk grid size"""
	# flatten the component
	comp = comp.flatten()
	# figure out nm
	if nm is None:
		nm = int(get_grid_size() * 1000)
	elif nm == 0:
		return comp
	elif nm < 0:
		raise ValueError("nm must be an integer tolerance value greater than zero")
	# iterate through ports and snap to grid
	comp.snap_ports_to_grid(nm=nm)
	save_ports = comp.get_ports_list()
	save_name = comp.name
	with TemporaryDirectory() as tmpdirname:
		tmp_gds_path = Path(comp.write_gds(gdsdir=tmpdirname)).resolve()
		comp = import_gds(gdspath=tmp_gds_path).copy()
	comp.add_ports(save_ports)
	comp.name = save_name
	return comp


"""
from PDK.util.snap_to_grid import component_snap_to_grid
from PDK.util.standard_main import pdk
from gdsfactory.components.rectangle import rectangle

mycomp = rectangle(layer=pdk.get_glayer("met1"))
mycomp = component_snap_to_grid(mycomp)
mycomp.show()
"""
