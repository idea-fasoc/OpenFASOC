from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.port import Port
from pdk.mappedpdk import MappedPDK
from typing import Optional
from via_gen import via_stack, via_array
from gdsfactory.components.rectangle import rectangle
from pdk.util.custom_comp_utils import evaluate_bbox, align_comp_to_port,assert_is_manhattan, set_orientation


@cell
def straight_route(
	pdk: MappedPDK,
	edge1: Port,
	edge2: Port,
	glayer1: Optional[str] = None,
	width: Optional[float] = None,
	glayer2: Optional[str] = None,
	fullbottom: Optional[bool] = False
) -> Component:
	"""extends a route from edge1 until perpindicular with edge2, then places a via
	This depends on the orientation of edge1 and edge2
	if edge1 has the same orientation as edge2, the generator will rotate edge2 180 degrees
	Will not modify edge1 or edge2
	
	DOES NOT REQUIRE:
	edge2 is directly inline with edge1
	
	example:
	           edge2
	             
	edge1--------
	
	args:
	pdk to use
	edge1, edge2 Ports
	glayer1 = defaults to edge1.layer, layer of the route.
	****If not edge1.layer, a via will be placed
	glayer2 = defaults to edge2.layer, end layer of the via
	width = defaults to edge1.width
	"""
	#TODO: error checking
	width = width if width else edge1.width
	glayer1 = glayer1 if glayer1 else pdk.layer_to_glayer(edge1.layer)
	front_via = None
	if glayer1 != pdk.layer_to_glayer(edge1.layer):
		front_via = via_stack(pdk,glayer1,pdk.layer_to_glayer(edge1.layer),fullbottom=fullbottom)
	glayer2 = glayer2 if glayer2 else pdk.layer_to_glayer(edge2.layer)
	assert_is_manhattan([edge1,edge2])
	if edge1.orientation == edge2.orientation:
		edge2 = set_orientation(edge2,edge2.orientation,flip180=True)
	pdk.activate()
	# find extension length and direction
	edge1_is_EW = bool(round(edge1.orientation + 90) % 180)
	if edge1_is_EW:
		startx = edge1.center[0]
		endx = edge2.center[0]
		extension = endx-startx
		viaport_name = "e3" if extension > 0 else "e1"
		alignment = ("r","c") if extension > 0 else ("l","c")
		size = (abs(extension),width)
	else:
		starty = edge1.center[1]
		endy = edge2.center[1]
		extension = endy-starty
		viaport_name = "e2" if extension > 0 else "e4"
		alignment = ("c","t") if extension > 0 else ("c","b")
		size = (width,abs(extension))
	# create route and via
	route = rectangle(layer=pdk.get_glayer(glayer1),size=size,centered=True)
	out_via = via_stack(pdk,glayer1,glayer2,fullbottom=fullbottom)
	# place route and via
	straightroute = Component()
	route_ref = align_comp_to_port(route,edge1,alignment=alignment)
	straightroute.add(route_ref)
	straightroute.add(align_comp_to_port(out_via,route_ref.ports[viaport_name],alignment=("c","c")))
	if front_via is not None:
		straightroute.add(align_comp_to_port(front_via,edge1,alignment=("c","c")))
	return straightroute.flatten()


if __name__ == "__main__":
	from pdk.util.standard_main import pdk
	
	routebetweentop = rectangle(layer=pdk.get_glayer("met3"),size=(1,1)).ref()
	routebetweentop.movex(20).movey(-3)
	routebetweenbottom = rectangle(layer=pdk.get_glayer("met1"), size=(1, 1))
	mycomp = straight_route(pdk,routebetweentop.ports["e3"],routebetweenbottom.ports["e1"])
	mycomp.unlock()
	mycomp.add(routebetweentop)
	mycomp << routebetweenbottom
	mycomp.flatten().show()
