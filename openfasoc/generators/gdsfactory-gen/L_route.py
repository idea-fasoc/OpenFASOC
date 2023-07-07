from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.port import Port
from PDK.mappedpdk import MappedPDK
from typing import Optional
from via_gen import via_stack
from gdsfactory.components.rectangle import rectangle
from PDK.util.custom_comp_utils import evaluate_bbox, align_comp_to_port, rename_ports_by_orientation, rename_ports_by_list, print_ports, assert_is_manhattan, assert_ports_perpindicular


@cell
def L_route(
	pdk: MappedPDK,
	edge1: Port,
	edge2: Port,
	vwidth: Optional[float] = None,
	hwidth: Optional[float] = None,
	hglayer: Optional[str] = None,
	vglayer: Optional[str] = None,
	viaoffset: Optional[bool]=True
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
	"""
	# error checking, TODO: validate layers
	assert_is_manhattan([edge1,edge2])
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
	vwidth = vwidth if vwidth else vport.width
	hwidth = hwidth if hwidth else hport.width
	hglayer = hglayer if hglayer else pdk.layer_to_glayer(vport.layer)
	vglayer = vglayer if vglayer else pdk.layer_to_glayer(hport.layer)
	# compute required dimensions
	hdim_center = vport.center[0] - hport.center[0]
	vdim_center = hport.center[1] - vport.center[1]
	hdim = abs(hdim_center) + hwidth/2
	vdim = abs(vdim_center) + vwidth/2
	# create and place vertical and horizontal connections
	hconnect = rectangle(size=(hdim,vwidth),layer=pdk.get_glayer(hglayer))
	vconnect = rectangle(size=(hwidth,vdim),layer=pdk.get_glayer(vglayer))
	#xalign
	valign = ("l","c") if hdim_center > 0 else ("r","c")
	halign = ("c","b") if vdim_center > 0 else ("c","t")
	#yalign
	hconnect_ref = align_comp_to_port(hconnect, vport, valign)
	Lroute.add(hconnect_ref)
	vconnect_ref = align_comp_to_port(vconnect, hport, halign)
	Lroute.add(vconnect_ref)
	# create and place via
	h_to_v_via_ref = Lroute << via_stack(pdk, hglayer, vglayer)
	h_to_v_via_ref.move(destination=(hport.center[0], vport.center[1]))
	if viaoffset:
		viadim_os = evaluate_bbox(h_to_v_via_ref)[0]/2
		viaxofs = abs(hwidth/2-viadim_os)
		viaxofs = viaxofs if hdim_center > 0 else -1*viaxofs
		viayofs = abs(vwidth/2-viadim_os)
		viayofs = viayofs if vdim_center > 0 else -1*viayofs
		h_to_v_via_ref.movex(viaxofs).movey(viayofs)
	return Lroute.flatten()


if __name__ == "__main__":
	from PDK.util.standard_main import pdk
	
	routebetweentop = rectangle(layer=pdk.get_glayer("met1"),size=(1,1)).ref()
	routebetweentop.movey(-4).movex(7)
	routebetweenbottom = rectangle(layer=pdk.get_glayer("met1"), size=(1, 0.5))
	mycomp = L_route(pdk,routebetweentop.ports["e4"],routebetweenbottom.ports["e1"])
	mycomp.unlock()
	mycomp.add(routebetweentop)
	mycomp << routebetweenbottom
	mycomp.flatten().show()
