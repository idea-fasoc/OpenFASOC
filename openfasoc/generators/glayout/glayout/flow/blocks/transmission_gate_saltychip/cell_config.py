from typing import ClassVar, Optional, Any, Union, Literal, Iterable, TypedDict
#from glayout.flow.pdk.gf180_mapped import gf180
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.util.comp_utils import evaluate_bbox
from gdsfactory import Component
from gdsfactory.components import rectangle
from glayout.flow.primitives.fet import pmos
from glayout.flow.primitives.fet import nmos
from glayout.flow.primitives.via_gen import via_stack
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.smart_route import smart_route
from glayout.flow.placement.two_transistor_interdigitized import two_nfet_interdigitized
from glayout.flow.placement.two_transistor_interdigitized import two_pfet_interdigitized
from glayout.flow.pdk.util.comp_utils import prec_ref_center, movey, evaluate_bbox, align_comp_to_port

# Status: W.I.P.
def add_wire(comp, xsize=2, ysize=1, layer=(68, 20), port_label="new_wire", center=(0, 0), position_offset=(1.4, 1.4)):
	c = Component()
	wire_leftBottom_pos = (center[0]-position_offset[0], center[1]-position_offset[1])
	wire_rightBottom_pos = (center[0]+position_offset[0], center[1]-position_offset[1])
	wire_rightTop_pos = (center[0]+position_offset[0], center[1]-position_offset[1]-ysize)
	wire_leftTop_pos = (center[0]-position_offset[0], center[1]-position_offset[1]-ysize)
	c.add_polygon(
		[
			wire_leftBottom_pos,
			wire_rightBottom_pos,
			wire_rightTop_pos,
			wire_leftTop_pos
		],
		layer=layer
	)

	port_W_pos = (c.x-xsize/2, c.y)
	port_E_pos = (c.x+xsize/2, c.y)
	c.add_port(name=f"{port_label}_W", center=port_W_pos, width=ysize, orientation=0, layer=layer)
	c.add_port(name=f"{port_label}_E", center=port_E_pos, width=ysize, orientation=0, layer=layer)
	c.add_label(text=f"{port_label}_W", position=port_W_pos, layer=layer)
	c.add_label(text=f"{port_label}_E", position=port_E_pos, layer=layer)
	return c

def port_with_pin(pdk: MappedPDK, comp: Component, port_list: list[ dict[str, Union[float, str]] ], port_feature: dict[str, str]) -> Component:
	# Add pins and text labels for LVS
	pins_labels_info = list() # list that contains all port and component information
	for port in port_list:
		ref_port_layer = comp.ports[ port["ref_port"] ].layer[0] # To get the layer's data type mapped to the GDS.
														#  [0]: layer mapping, [1]: pin, drawing, label, net, etc.
		print(f"Port: {port}")

		# To create the pin w/ a label
		new_port_layer = pdk.get_glayer(port_feature["layer"])
		new_port_layerPin = (new_port_layer[0], 16) # layer[1]=16 mapped to the "pin" datatype in the GDS
		new_port_layerLabel = (new_port_layer[0], 5) # layer[1]=5 mapped to the "label" datatype in the GDS
		new_port_layerDraw =  pdk.get_glayer(port_feature["layer"])

		new_pin_width = pdk.get_grule(port_feature["layer"])["min_width"]
		new_port = rectangle(layer=new_port_layerPin, size=(new_pin_width, new_pin_width),centered=True).copy() # To set rectangle's centroid to the relative (0, 0)
		new_port.add_label(text=port["new_port_label"], layer=new_port_layerLabel)

		# To align the new port with the designated port existing in the given component
		alignment = port["ref_port_align"]
		comp_ref = align_comp_to_port(custom_comp=new_port, align_to=comp.ports[ port["ref_port"] ], alignment=alignment)
		comp.add(comp_ref)
		comp_ref.movex(port["new_port_move"][0])
		comp_ref.movey(port["new_port_move"][1])

		if port["new_port_via"] == True:
			new_port_via = via_stack(pdk=pdk, glayer1=port["new_port_via_layers"][0], glayer2=port["new_port_via_layers"][1])
			new_port_via_ref = comp.add_ref(new_port_via)
			new_port_via_ref.movex(comp_ref.center[0])
			new_port_via_ref.movey(comp_ref.center[1])

		# To register the new port as an external I/O port of the top-level component
		comp.add_port(name=port["new_port"], center=new_port.center, width=new_pin_width, orientation=0, layer=new_port_layerDraw)
	
	return comp

def port_with_wire(pdk: MappedPDK, comp: Component, port_list: list[ dict[str, Union[float, str]] ], port_feature: dict[str, str]) -> Component:
	new_port_layer = pdk.get_glayer(port_feature["layer"])
	wire_width = comp.xsize
	wire_height = pdk.get_grule(port_feature["layer"])["min_width"]
	new_port_center = comp.center
	new_port_position_offset = (comp.xsize/2, comp.ysize/2+pdk.util_max_metal_seperation())
	wire_spacing = pdk.get_grule(port_feature["layer"])["min_separation"]+wire_height
	port_cnt = 0

	# Add pins and text labels for LVS
	pins_labels_info = list() # list that contains all port and component information
	print(f"port_list: {port_list}")
	for port in port_list:
		# To create the pin where the layer[1] is mapped to 16
		connect_pos = port["connect_pos"] if "connect_pos" in port else "W" 
		new_wire = add_wire(comp=comp, xsize=wire_width, ysize=wire_height, layer=new_port_layer, port_label=port["new_port_label"], center=new_port_center, position_offset=new_port_position_offset)
		new_wire_ref = comp.add_ref(new_wire)
		new_wire_ref.movey(-wire_spacing*port_cnt)
		comp.add_ports(new_wire_ref.get_ports_list()) # To register all the ports in the wire to the underlying component
		edge0 = comp.ports.get(port["ref_port"])
		edge1 = comp.ports.get(port["new_port"]+f"_{connect_pos}")
		comp << smart_route(pdk, edge0, edge1)

		port_cnt = port_cnt + 1 # Increment the index indicating the new port

	return comp

def add_port_lvs(pdk: MappedPDK, comp: Component, port_list: list[ dict[str, Union[float, str]] ], port_feature: dict[str, str]) -> Component:
	'''
    To add external I/O ports onto the cell for LVS

	@ args:
    	# pdk: please refer to the glayout library
    	# comp: please refer to the glayout library
    	# port_list: tuple[ dict[str, Union[float, str]] ] specifying new port's corresponding pin size, and
					 the name of new port and exiting port managed to align with in the given 
					 component, e.g. 
					 	(
							{
								"new_port": "drain_new", 
								"new_port_label": "drain_new_label",
								"pin_width": 0.5, # -> Only being used when "port_feature": "pin" 
								"pin_height": 0.5, # -> Only being used when "port_feature": "pin"
								"ref_port": "multiplier_0_drain_E"
							},
							{
								"new_port": "source_new", 
								"new_port_label": "source_new_label",
								"ref_port": "multiplier_0_source_E",
								"connect_pos": "W" # -> for all connect_pos in {W, E} where the
												   #    connect_pos will be set to "W" if connect_pos=None  
							}
						)
		# port_feature: a "dict"-type primitive specifying the feature of the new port, e.g.
						{"port_type":"pin", "layer":None} -> To create a rectangle as the new port
						{"port_type":"wire", "layer":"met1"} -> To extend the existing port by a wire only
    
		# return: gdsfactory.Component

	@ Limitations:
		# So far, only skywater130 process is validated
	'''
	
	if port_feature["port_type"] == "pin":
		port_type = 0
	elif port_feature["port_type"] == "wire":
		port_type = 1
	else:
		raise ValueError("The port type must be either pin or wire")

	if port_type == 0: # port of which features pin-added type
		port_with_pin(pdk=pdk, comp=comp, port_list=port_list, port_feature=port_feature)
	else: # port_type=1, i.e. port of which features wire_only
		port_with_wire(pdk=pdk, comp=comp, port_list=port_list, port_feature=port_feature)

	return comp