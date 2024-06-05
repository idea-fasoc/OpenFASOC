from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.port import Port
from glayout.flow.pdk.mappedpdk import MappedPDK
from typing import Optional
from glayout.flow.primitives.via_gen import via_stack, via_array
from gdsfactory.components.rectangle import rectangle
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, align_comp_to_port
from glayout.flow.pdk.util.port_utils import assert_port_manhattan, set_port_orientation, add_ports_perimeter
from gdstk import rectangle as primitive_rectangle


@cell
def straight_route(
	pdk: MappedPDK,
	edge1: Port,
	edge2: Port,
	glayer1: Optional[str] = None,
	width: Optional[float] = None,
	glayer2: Optional[str] = None,
	via1_alignment: Optional[tuple[str, str]] = None,
	via1_alignment_layer: Optional[str] = None,
	via2_alignment: Optional[tuple[str, str]] = None,
	via2_alignment_layer: Optional[str] = None,
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
	via1_alignment = alignment of the via on edge1
	via2_alignment = alignment of the via on edge2
	****defaults to an orientation that is aligned to the orientation of the port.
	
	Ports:
	route_...all edges of the rectangle path
	"""
	#TODO: error checking
	width = width if width else edge1.width
	glayer1 = glayer1 if glayer1 else pdk.layer_to_glayer(edge1.layer)
	front_via = None
	if glayer1 != pdk.layer_to_glayer(edge1.layer):
		front_via = via_stack(pdk,glayer1,pdk.layer_to_glayer(edge1.layer),fullbottom=fullbottom)
	glayer2 = glayer2 if glayer2 else pdk.layer_to_glayer(edge2.layer)
	assert_port_manhattan([edge1,edge2])
	if edge1.orientation == edge2.orientation:
		edge2 = set_port_orientation(edge2,edge2.orientation,flip180=True)
	pdk.activate()
	# find extension length and direction
	edge1_is_EW = bool(round(edge1.orientation + 90) % 180)
	if edge1_is_EW:
		startx = edge1.center[0]
		endx = edge2.center[0]
		extension = endx-startx
		viaport_name = "route_E" if extension > 0 else "route_W"
		alignment = ("r","c") if extension > 0 else ("l","c")
		size = (abs(extension),width)
	else:
		starty = edge1.center[1]
		endy = edge2.center[1]
		extension = endy-starty
		viaport_name = "route_N" if extension > 0 else "route_S"
		alignment = ("c","t") if extension > 0 else ("c","b")
		size = (width,abs(extension))
	# create route and via
	route = Component()
	route.add_polygon(primitive_rectangle((0,0),size,*pdk.get_glayer(glayer1)))
	add_ports_perimeter(route,layer=pdk.get_glayer(glayer1),prefix="route_")
	out_via = via_stack(pdk,glayer1,glayer2,fullbottom=fullbottom) if glayer1 != glayer2 else None
	# place route and via
	straightroute = Component()
	for i, edge in enumerate([edge1,edge2]):
		temp = via1_alignment if i == 0 else via2_alignment
		if temp is None:
			if round(edge.orientation) == 0:# facing east
				temp = ("l", "c")
			elif round(edge.orientation) == 180:# facing west
				temp = ("r", "c")
			elif round(edge.orientation) == 270:# facing south
				temp = ("c", "t")
			elif round(edge.orientation) == 90:#facing north
				temp = ("c", "b")
			else:
				raise ValueError("port must be vertical or horizontal")
		via1_alignment = temp if i == 0 else via1_alignment
		via2_alignment = temp if i == 1 else via2_alignment
	route_ref = align_comp_to_port(route,edge1,alignment=alignment)
	straightroute.add_ports(route_ref.get_ports_list())
	straightroute.add(route_ref)
	if out_via is not None:
		alignlayer2 = pdk.get_glayer(glayer1) if via2_alignment_layer is None else pdk.get_glayer(via2_alignment_layer)
		straightroute.add(align_comp_to_port(out_via,route_ref.ports[viaport_name],layer=alignlayer2,alignment=via2_alignment))
	if front_via is not None:
		alignlayer1 = pdk.get_glayer(glayer1) if via1_alignment_layer is None else pdk.get_glayer(via1_alignment_layer)
		straightroute.add(align_comp_to_port(front_via,edge1,layer=alignlayer1,alignment=via1_alignment))
	return straightroute.flatten()


