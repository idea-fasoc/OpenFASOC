from gdsfactory.cell import cell
from gdsfactory.component import Component, copy
from gdsfactory.port import Port
from PDK.mappedpdk import MappedPDK
from typing import Optional, Union
from math import isclose
from via_gen import via_stack
from gdsfactory.routing.route_quad import route_quad
from gdsfactory.components.rectangle import rectangle
from PDK.util.custom_comp_utils import evaluate_bbox, add_ports_perimeter, rename_ports_by_orientation, rename_ports_by_list, print_ports


@cell
def c_route(
	pdk: MappedPDK, 
	edge1: Port, 
	edge2: Port, 
	extension: Optional[float]=0.5, 
	width: Optional[float] = None, 
	eglayer: Optional[str] = None, 
	cglayer: Optional[str] = None, 
	viaoffset: Optional[Union[bool,tuple[Optional[bool],Optional[bool]]]]=(True,True),
	fullbottom: Optional[bool] = False
) -> Component:
	"""creates a C shaped route between two Ports.
	
	edge1--|
	       |
	edge2--|
	
	REQUIRES: ports be parralel vertical or horizontal edges
	****NOTE: does no drc error checking (creates a dumb route)
	args:
	pdk = pdk to use
	edge1 = first port
	edge2 = second port
	width = optional will default to edge1 width if None
	eglayer = glayer for the parts connecting to the ports. Default to layer of edge1
	cglayer = glayer for the connection part (part that goes through a via) defaults to eglayer met+1
	viaoffset = offsets the via so that it is flush with the cglayer (may be needed for drc) i.e. -| vs _|
	- True offsets via towards the other via
	- False offsets via away from the other via
	- None means center (no offset)
	***NOTE: viaoffset pushes both vias towards each other slightly
	"""
	# error checking and figure out args
	if round(edge1.orientation) % 90 or round(edge2.orientation) % 90:
		raise ValueError("Ports must be vertical or horizontal")
	if not isclose(edge1.orientation,edge2.orientation):
		raise ValueError("Ports must be parralel and have same orientation")
	width = width if width else edge1.width
	eglayer = eglayer if eglayer else pdk.layer_to_glayer(edge1.layer)
	eglayer_plusone = "met" + str(int(eglayer[-1])+1)
	cglayer = cglayer if cglayer else eglayer_plusone
	if not "met" in eglayer or not "met" in cglayer:
		raise ValueError("given layers must be metals")
	viaoffset = (None, None) if viaoffset is None else viaoffset
	if isinstance(viaoffset,bool):
		viaoffset = (True,True) if viaoffset else (False,False)
	pdk.has_required_glayers([eglayer,cglayer])
	pdk.activate()
	# create route
	croute = Component()
	viastack = via_stack(pdk,eglayer,cglayer,fullbottom=fullbottom)
	# find extension
	e1_length = extension + evaluate_bbox(viastack)[0]
	e2_length = extension + evaluate_bbox(viastack)[0]
	xdiff = abs(edge1.center[0] - edge2.center[0])
	ydiff = abs(edge1.center[1] - edge2.center[1])
	if not isclose(edge1.center[0],edge2.center[0]):
		if round(edge1.orientation) == 0:# facing east
			if edge1.center[0] > edge2.center[0]:
				e2_length += xdiff
			else:
				e1_length += xdiff
		elif round(edge1.orientation) == 180:# facing west
			if edge1.center[0] < edge2.center[0]:
				e2_length += xdiff
			else:
				e1_length += xdiff
	if not isclose(edge1.center[1],edge2.center[1]):
		if round(edge1.orientation) == 270:# facing south
			if edge1.center[1] < edge2.center[1]:
				e2_length += ydiff
			else:
				e1_length += ydiff
		elif round(edge1.orientation) == 90:#facing north
			if edge1.center[1] > edge2.center[1]:
				e2_length += ydiff
			else:
				e1_length += ydiff
	# move into position
	e1_extension_comp = Component("edge1 extension")
	e2_extension_comp = Component("edge2 extension")
	box_dims = [(e1_length, width),(e2_length, width)]
	if round(edge1.orientation) == 90 or round(edge1.orientation) == 270:
		box_dims = [(width, e1_length),(width, e2_length)]
	rect_c1 = copy(rectangle(size=box_dims[0], layer=pdk.get_glayer(eglayer),centered=True))
	rect_c2 = copy(rectangle(size=box_dims[1], layer=pdk.get_glayer(eglayer),centered=True))
	rect_c1 = rename_ports_by_orientation(rename_ports_by_list(rect_c1,[("e","e_")]))
	rect_c2 = rename_ports_by_orientation(rename_ports_by_list(rect_c2,[("e","e_")]))
	e1_extension = e1_extension_comp << rect_c1
	e2_extension = e2_extension_comp << rect_c2
	e1_extension.move(destination=edge1.center)
	e2_extension.move(destination=edge2.center)
	if round(edge1.orientation) == 0:# facing east
		e1_extension.movex(evaluate_bbox(e1_extension)[0]/2)
		e2_extension.movex(evaluate_bbox(e2_extension)[0]/2)
	elif round(edge1.orientation) == 180:# facing west
		e1_extension.movex(0-evaluate_bbox(e1_extension)[0]/2)
		e2_extension.movex(0-evaluate_bbox(e2_extension)[0]/2)
	elif round(edge1.orientation) == 270:# facing south
		e1_extension.movey(0-evaluate_bbox(e1_extension)[1]/2)
		e2_extension.movey(0-evaluate_bbox(e2_extension)[1]/2)
	else:#facing north
		e1_extension.movey(evaluate_bbox(e1_extension)[1]/2)
		e2_extension.movey(evaluate_bbox(e2_extension)[1]/2)
	# place viastacks
	e1_extension_comp.add_ports(e1_extension.get_ports_list())
	e2_extension_comp.add_ports(e2_extension.get_ports_list())
	me1 = e1_extension_comp << viastack
	me2 = e2_extension_comp << viastack
	route_ports = [None,None]
	via_flush = abs((width - evaluate_bbox(viastack)[0])/2) if viaoffset else 0
	via_flush1 = via_flush if viaoffset[0] else 0-via_flush
	via_flush1 = 0 if viaoffset[0] is None else via_flush1
	via_flush2 = via_flush if viaoffset[1] else 0-via_flush
	via_flush2 = 0 if viaoffset[1] is None else via_flush2
	if round(edge1.orientation) == 0:# facing east
		me1.move(destination=e1_extension.ports["e_E"].center)
		me2.move(destination=e2_extension.ports["e_E"].center)
		via_flush *= 1 if me1.ymax > me2.ymax else -1
		me1.movex(0-viastack.xmax).movey(0-via_flush1)
		me2.movex(0-viastack.xmax).movey(via_flush2)
		route_ports = [me1.ports["top_met_S"],me2.ports["top_met_N"]]
	elif round(edge1.orientation) == 180:# facing west
		me1.move(destination=e1_extension.ports["e_W"].center)
		me2.move(destination=e2_extension.ports["e_W"].center)
		via_flush *= 1 if me1.ymax > me2.ymax else -1
		me1.movex(viastack.xmax).movey(0-via_flush1)
		me2.movex(viastack.xmax).movey(via_flush2)
		route_ports = [me1.ports["top_met_S"],me2.ports["top_met_N"]]
	elif round(edge1.orientation) == 270:# facing south
		me1.move(destination=e1_extension.ports["e_S"].center)
		me2.move(destination=e2_extension.ports["e_S"].center)
		via_flush *= 1 if me1.xmax > me2.xmax else -1
		me1.movey(viastack.xmax).movex(0-via_flush1)
		me2.movey(viastack.xmax).movex(via_flush2)
		route_ports = [me1.ports["top_met_E"],me2.ports["top_met_W"]]
	else:#facing north
		me1.move(destination=e1_extension.ports["e_N"].center)
		me2.move(destination=e2_extension.ports["e_N"].center)
		via_flush *= 1 if me1.xmax > me2.xmax else -1
		me1.movey(0-viastack.xmax).movex(0-via_flush1)
		me2.movey(0-viastack.xmax).movex(via_flush2)
		route_ports = [me1.ports["top_met_E"],me2.ports["top_met_W"]]
		
	croute << e1_extension_comp
	croute << e2_extension_comp
	cconnection = croute << route_quad(route_ports[0],route_ports[1],layer=pdk.get_glayer(cglayer))
	croute.add_ports(cconnection.get_ports_list(),prefix="con_")
	return rename_ports_by_orientation(rename_ports_by_list(croute.flatten(), [("con_","con_")]))

if __name__ == "__main__":
	from PDK.util.standard_main import pdk
	
	routebetweentop = copy(rectangle(layer=pdk.get_glayer("met1"))).ref()
	routebetweentop.movey(10)
	routebetweenbottom = rectangle(layer=pdk.get_glayer("met1"))
	mycomp = c_route(pdk,routebetweentop.ports["e3"],routebetweenbottom.ports["e3"])
	mycomp.unlock()
	mycomp.add(routebetweentop)
	mycomp << routebetweenbottom
	mycomp.flatten().show()
