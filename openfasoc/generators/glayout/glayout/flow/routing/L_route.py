from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.port import Port
from glayout.flow.pdk.mappedpdk import MappedPDK
from typing import Optional, Union
from glayout.flow.primitives.via_gen import via_stack, via_array
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, align_comp_to_port, to_decimal, to_float, prec_ref_center, get_primitive_rectangle
from glayout.flow.pdk.util.port_utils import rename_ports_by_orientation, rename_ports_by_list, print_ports, assert_port_manhattan, assert_ports_perpindicular
from decimal import Decimal


@cell
def L_route(
	pdk: MappedPDK,
	edge1: Port,
	edge2: Port,
	vwidth: Optional[float] = None,
	hwidth: Optional[float] = None,
	hglayer: Optional[str] = None,
	vglayer: Optional[str] = None,
	viaoffset: Optional[Union[tuple[bool,bool],bool]]=True,
	fullbottom: bool = True
) -> Component:
	"""creates a L shaped route between two Ports.
	
	edge1
	  |
	  ------|edge2
	
	REQUIRES: 
	- ports (a.k.a. edges) be vertical or horizontal
	- edges be perpindicular to each other
	
	DOES NOT REQUIRE:
	- correct 180 degree orientation of the port (e.g. a south facing port may result in north facing route)
	
	****NOTE: does no drc error checking (creates a dumb route)
	args:
	pdk = pdk to use
	edge1 = first port
	edge2 = second port
	vwidth = optional will default to vertical edge width if None
	hwidth = optional will default to horizontal edge width if None
	hglayer = glayer for vertical route. Defaults to the layer of the edge oriented N/S
	vglayer = glayer for horizontal route. Defaults to the layer of the edge oriented E/W
	viaoffset = push the via away from both edges so that inside corner aligns with via corner
	****via offset can also be specfied as a tuple(bool,bool): movex? if viaoffset[0] and movey? if viaoffset[1]
	fullbottom = fullbottom option for via
	"""
	# error checking, TODO: validate layers
	assert_port_manhattan([edge1,edge2])
	assert_ports_perpindicular(edge1,edge2)
	pdk.activate()
	Lroute = Component()
	# figure out which port is vertical
	vport = None
	hport = None
	edge1_is_EW = bool(round(edge1.orientation + 90) % 180)
	if edge1_is_EW:
		vport, hport = edge1, edge2
	else:
		hport, vport = edge1, edge2
	# arg setup
	vwidth = to_decimal(vwidth if vwidth else vport.width)
	hwidth = to_decimal(hwidth if hwidth else hport.width)
	hglayer = hglayer if hglayer else pdk.layer_to_glayer(vport.layer)
	vglayer = vglayer if vglayer else pdk.layer_to_glayer(hport.layer)
	if isinstance(viaoffset,bool):
		viaoffset = (True,True) if viaoffset else (False,False)
	# compute required dimensions
	hdim_center = to_decimal(vport.center[0]) - to_decimal(hport.center[0])
	vdim_center = to_decimal(hport.center[1]) - to_decimal(vport.center[1])
	hdim = abs(hdim_center) + hwidth/2
	vdim = abs(vdim_center) + vwidth/2
	# create and place vertical and horizontal connections
	hconnect = get_primitive_rectangle(size=to_float((hdim,vwidth)),layer=pdk.get_glayer(hglayer))
	vconnect = get_primitive_rectangle(size=to_float((hwidth,vdim)),layer=pdk.get_glayer(vglayer))
	#xalign
	valign = ("l","c") if hdim_center > 0 else ("r","c")
	halign = ("c","b") if vdim_center > 0 else ("c","t")
	#yalign
	hconnect_ref = align_comp_to_port(hconnect, vport, valign)
	Lroute.add(hconnect_ref)
	vconnect_ref = align_comp_to_port(vconnect, hport, halign)
	Lroute.add(vconnect_ref)
	# create and place via (decide between via stack and via array)
	hv_via = via_stack(pdk, hglayer, vglayer,fullbottom=fullbottom,fulltop=True)
	hv_via_dims = evaluate_bbox(hv_via,True)
	use_stack = hv_via_dims[0] > hwidth or hv_via_dims[1] > vwidth
	if not use_stack:
		hv_via = via_array(pdk, hglayer, vglayer, size=to_float((hwidth,vwidth)), lay_bottom=True)
	h_to_v_via_ref = prec_ref_center(hv_via)
	Lroute.add(h_to_v_via_ref)
	h_to_v_via_ref.move(destination=(hport.center[0], vport.center[1]))
	if viaoffset[0] or viaoffset[1]:
		viadim_osx = evaluate_bbox(h_to_v_via_ref,True)[0]/2
		viaxofs = abs(hwidth/2-viadim_osx)
		viaxofs = to_float(viaxofs if hdim_center > 0 else -1*viaxofs)
		viaxofs = viaxofs if viaoffset[0] else 0
		viadim_osy = evaluate_bbox(h_to_v_via_ref,True)[1]/2
		viayofs = abs(vwidth/2-viadim_osy)
		viayofs = to_float(viayofs if vdim_center > 0 else -1*viayofs)
		viayofs = viayofs if viaoffset[1] else 0
		h_to_v_via_ref.movex(viaxofs).movey(viayofs)
	# add ports and return
	Lroute.add_ports(h_to_v_via_ref.get_ports_list())
	return rename_ports_by_orientation(Lroute.flatten())


