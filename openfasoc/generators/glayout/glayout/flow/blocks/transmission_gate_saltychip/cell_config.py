from typing import ClassVar, Optional, Any, Union, Literal, Iterable, TypedDict
#from glayout.flow.pdk.gf180_mapped import gf180
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.util.comp_utils import evaluate_bbox
from gdsfactory import Component
from gdsfactory.components import rectangle
from glayout.flow.primitives.fet import pmos
from glayout.flow.primitives.fet import nmos
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.smart_route import smart_route
from glayout.flow.placement.two_transistor_interdigitized import two_nfet_interdigitized
from glayout.flow.placement.two_transistor_interdigitized import two_pfet_interdigitized
from glayout.flow.pdk.util.comp_utils import prec_ref_center, movey, evaluate_bbox, align_comp_to_port

def add_wire(comp, xsize=2, ysize=1, layer=(68, 20), label="new_wire", center=(0, 0), position_offset=(1.4, 1.4)):
	c = Component()
	c.add_polygon(
		[
			(center[0]-position_offset[0], center[1]-position_offset[1]),
			(center[0]+position_offset[0], center[1]-position_offset[1]),
			(center[0]+position_offset[0], center[1]-position_offset[1]-ysize),
			(center[0]-position_offset[0], center[1]-position_offset[1]-ysize)
		],
		layer=layer
	)
	comp.add_port(name=f"{label}_W", center=[0, ysize / 2], width=ysize, orientation=0, layer=layer)
	comp.add_port(name=f"{label}_E", center=[xsize, ysize / 2], width=ysize, orientation=0, layer=layer)
	c.add_label(text=f"{label}_W", position=(c.x-xsize/2, c.y), layer=layer)
	c.add_label(text=f"{label}_E", position=(c.x+xsize/2, c.y), layer=layer)
	
	return c

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
								"pin_width": 0.5, 
								"pin_height": 0.5, 
								"ref_port": "multiplier_0_drain_E"
							},
							{
								"new_port": "source_new", 
								"new_port_label": "source_new_label",
								"pin_width": 1.5, 
								"pin_height": 1.5, 
								"ref_port": "multiplier_0_source_E"
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
		new_port_layer = pdk.get_glayer(port_feature["layer"])
		port_type = 1
		wire_width = comp.xsize
		wire_height = pdk.get_grule(port_feature["layer"])["min_width"]
		new_port_center = comp.center
		new_port_position_offset = (comp.xsize/2, comp.ysize/2+pdk.util_max_metal_seperation())
		wire_spacing = pdk.get_grule(port_feature["layer"])["min_separation"]+wire_height
		port_cnt = 0
	else:
		raise ValueError("The port type must be either pin or wire")

	if port_type == 0: # port of which features pin-added type
		# Add pins and text labels for LVS
		pins_labels_info = list() # list that contains all port and component information
		print(f"port_list: {port_list}")
		for port in port_list:
			# To get the layer's data type mapped to the GDS
			ref_port_layer = comp.ports[ port["ref_port"] ].layer[0] # [0]: layer mapping, [1]: pin, drawing, label, net, etc.

			# To create the pin w/ a label where the layer[1] is mapped to 16
			new_port = rectangle(layer=(ref_port_layer, 16), size=(port["pin_width"], port["pin_height"]),centered=True).copy() # True set rectangle's centroid to the relative (0, 0)
			new_port.add_label(text=port["new_port_label"], layer=(ref_port_layer, 5)) # layer[1]=5 mapped to the "label" datatype in the GDS

			# To align the new port with the designated port existing in the given component
			alignment = ('c', 'b')
			comp_ref = align_comp_to_port(new_port, comp.ports[ port["ref_port"] ], alignment=alignment)
			comp.add(comp_ref)

	else: # port_type=1, i.e. port of which features wire_only
		# Add pins and text labels for LVS
		pins_labels_info = list() # list that contains all port and component information
		print(f"port_list: {port_list}")
		for port in port_list:
			# To create the pin where the layer[1] is mapped to 16
			new_port = add_wire(comp=comp, xsize=wire_width, ysize=wire_height, layer=new_port_layer, label=port["new_port_label"], center=new_port_center, position_offset=new_port_position_offset)
			new_port_ref = comp.add_ref(new_port)
			new_port_ref.movey(-wire_spacing*port_cnt)
			comp << smart_route(pdk, comp.ports.get(port["ref_port"]), comp.ports.get(port["new_port"]+"_E"))
			
			port_cnt = port_cnt + 1 # Increment the index indicating the new port

	return comp