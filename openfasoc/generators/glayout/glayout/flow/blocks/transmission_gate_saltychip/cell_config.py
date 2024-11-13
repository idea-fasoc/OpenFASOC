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

def add_port_lvs(pdk: MappedPDK, comp: Component, port_list: list[ dict[str, Union[float, str]] ]) -> Component:
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
    
		# return: gdsfactory.Component

	@ Limitations:
		# So far, only skywater130 process is validated
	'''

	# Add pins and text labels for LVS
	pins_labels_info = list() # list that contains all port and component information
	print(f"port_list: {port_list}")
	for port in port_list:
		# To get the layer's data type mapped to the GDS
		ref_port_layer = comp.ports[ port["ref_port"] ].layer[0] # [0]: layer mapping, [1]: pin, drawing, label, net, etc.

		# To create the pin w/ label where the layer[1] is mapped to 16
		new_port_pin = rectangle(layer=(ref_port_layer, 16), size=(port["pin_width"], port["pin_height"]),centered=True).copy() # True set rectangle's centroid to the relative (0, 0)
		new_port_pin.add_label(text=port["new_port_label"], layer=(ref_port_layer, 5)) # layer[1]=5 mapped to the "label" datatype in the GDS

		# To align the new port with the designated port existing in the given component
		alignment = ('c', 'b')
		comp_ref = align_comp_to_port(new_port_pin, comp.ports[ port["ref_port"] ], alignment=alignment)
		comp.add(comp_ref)

	return comp