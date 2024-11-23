from typing import ClassVar, Optional, Any, Union, Literal, Iterable, TypedDict
import math
#from glayout.flow.pdk.gf180_mapped import gf180
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.util.comp_utils import evaluate_bbox
from glayout.flow.pdk.util.port_utils import set_port_orientation, rename_ports_by_orientation, create_private_ports
from gdsfactory import Component
from gdsfactory.components import rectangle
from glayout.flow.primitives.fet import pmos
from glayout.flow.primitives.fet import nmos
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.smart_route import smart_route
from glayout.flow.placement.two_transistor_interdigitized import two_pfet_interdigitized, two_nfet_interdigitized, two_transistor_interdigitized
from glayout.flow.placement.common_centroid_ab_ba import common_centroid_ab_ba
from glayout.flow.pdk.util.comp_utils import prec_ref_center, movey, evaluate_bbox, align_comp_to_port
from glayout.flow.primitives.via_gen import via_stack
from gdsfactory.cell import cell
from glayout.flow.spice import Netlist
from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid

# My own cell library
from reconfig_inv import reconfig_inv
import comp_dc

'''
def tg_netlist(pmos: Component, nmos: Component) -> Netlist:
	# A: tg.input, i.e. PMOS & NMOS source
	# Y: tg.output, i.e. PMOS & NMOS drain
	# C: connected to tg.nmos.gate
	# CBAR: connected to tg.pmos.gate
	# VDD: connected to tg.pmos.body
	# VSS: connected to tg.nmos.body
	netlist = Netlist(circuit_name='tg', nodes=['VDD', 'VSS', 'A', 'Y', 'C', 'CBAR'])
	#netlist.connect_netlist(pmos.info['netlist'], [('D', 'Y'), ('G', 'CBAR'), ('S', 'A'), ('PB', 'VDD')])
	#netlist.connect_netlist(nmos.info['netlist'], [('D', 'Y'), ('G', 'C'), ('S', 'A'), ('NB', 'VSS')])
	netlist.connect_netlist(pmos.info['netlist'], [('D', 'Y'), ('G', 'CBAR'), ('S', 'A')])
	netlist.connect_netlist(nmos.info['netlist'], [('D', 'Y'), ('G', 'C'), ('S', 'A')])
	return netlist
'''

def transmission_gate_netlist(
	pdk: MappedPDK,
	width: float,
	multipliers: int,
	length: float,
	subckt_only: Optional[bool] = False
) -> Netlist:
	if length is None:
		length = pdk.get_grule('poly')['min_width']
	if width is None:
		width = 3
	mtop = multipliers if subckt_only else 1
	model_pmos = pdk.models['pfet']
	model_nmos = pdk.models['nfet']
	print(f"model_pmos: {model_pmos}")
	source_netlist = """.subckt {circuit_name} {nodes} """ + f'l={length} w={width} m={mtop} ' + """
XM1 Y CBAR A {model_pmos} l={{l}} w={{w}} m={{m}}
XM2 Y C A {model_nmos} l={{l}} w={{w}} m={{m}}"""
	source_netlist += "\n.ends {circuit_name}"

	instance_format = "X{name} {nodes} {circuit_name} l={length} w={width} m={mult}"
 
	return Netlist(
		circuit_name='tg',
		nodes=['Y', 'C', 'CBAR', 'A'], 
		source_netlist=source_netlist,
  		instance_format=instance_format,
		parameters={
			'model_pmos': model_pmos,
			'model_nmos': model_nmos,
			'width': width,
   			'length': length,	
			'mult': multipliers
   		}
	)

@cell
def short_width_tg(
	pdk: MappedPDK,
	component_name: str,
	orientation_config:
	dict[str, Union[int, str]],
	pmos_width,
	pmos_length,
	nmos_width,
	nmos_length,
	add_pin: bool = True, # For LVS
	**kwargs
) -> Component:

	# To prepare all necessary cells to construct a transmission gate, i.e.
	# 1) PMOS
	# 2) NMOS
	pfet = pmos(pdk=pdk, gate_rmult=2, with_tie=False, with_substrate_tap=False, with_dummy=(True, False), width=pmos_width, length=pmos_length)
	nfet = nmos(pdk=pdk, gate_rmult=2, with_tie=False, with_dnwell=False, with_substrate_tap=False, with_dummy=(False, True), width=nmos_width, length=nmos_length)

	# Placement and adding ports
	top_level = Component(name=component_name)
	pfet_ref = prec_ref_center(pfet)
	nfet_ref = prec_ref_center(nfet)
	top_level.add(pfet_ref)
	top_level.add(nfet_ref)

	# Placement
	mos_spacing = pdk.util_max_metal_seperation()
	if orientation_config["degree"] != None:
		pfet_ref.rotate(orientation_config["degree"])
		nfet_ref.rotate(orientation_config["degree"])
	pfet_ref.movey(evaluate_bbox(nfet)[1] + mos_spacing)

	# Routing
	# To simplify the routing for the parallel-gate transistors, the layout is realised as follow which is expected to be equivalent to a TG
	#     a) PMOS.source connected to NMOS.source
	#     b) PMOS.drain connected to NMOS.drain 
	top_level << straight_route(pdk, pfet_ref.ports["multiplier_0_source_E"], nfet_ref.ports["multiplier_0_drain_E"], glayer1="met2") # "in" of the TG
	top_level << straight_route(pdk, pfet_ref.ports["multiplier_0_drain_E"], nfet_ref.ports["multiplier_0_source_E"], glayer1="met2") # "out" of the TG

	# Add the ports aligned with the basic PMOS and NMOS
	top_level.add_ports(pfet_ref.get_ports_list(), prefix="pmos_")
	top_level.add_ports(nfet_ref.get_ports_list(), prefix="nmos_")

	if add_pin == True:
		# Add pins w/ labels for LVS
		top_level.unlock()
		pin_info = list() # list that contains all port and component information
		met1_pin=(pdk.get_glayer("met1")[0], 20)
		met1_label=(pdk.get_glayer("met1")[0], 5)
		port_size = (0.24, 0.24)
		# --- Port: A, i.e. input of the transmission gate
		A_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		A_pin.add_label(text="A", layer=met1_label)
		pin_info.append((A_pin, top_level.ports.get(f"nmos_drain_S"), None))
		# --- Port: Y, i.e. output of the transmission gate
		Y_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		Y_pin.add_label(text="Y", layer=met1_label)
		pin_info.append((Y_pin, top_level.ports.get(f"pmos_drain_S"), None))
		# --- Port: C, i.e. gate control to the NMOS
		C_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		C_pin.add_label(text="C", layer=met1_label)
		pin_info.append((C_pin, top_level.ports.get(f"nmos_gate_N"), None))
		# --- Port: CBAR, i.e. gate control to the PMOS
		CBAR_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		CBAR_pin.add_label(text="CBAR", layer=met1_label)
		pin_info.append((CBAR_pin, top_level.ports.get(f"pmos_gate_N"), None))

		# Move everythin to position
		for comp, prt, alignment in pin_info:
			alignment = ('c', 'b') if alignment is None else alignment
			comp_ref = align_comp_to_port(comp, prt, alignment=alignment)
			top_level.add(comp_ref)

	component = component_snap_to_grid(rename_ports_by_orientation(top_level))
	component.info['netlist'] = tg_netlist(pmos=pfet, nmos=nfet)
	return component


@cell
def long_width_tg(
	pdk: MappedPDK,
	component_name: str,
	pmos_width,
	pmos_length,
	nmos_width,
	nmos_length,
	add_pin: bool = True, # For LVS
	**kwargs
) -> Component:
	# To calculate the number of fingers for the underlying PMOS/NMOS layout
	finger_num = math.ceil(pmos_width / comp_dc.tg_fet_width_base)
	mos_width = comp_dc.tg_fet_width_base

	# To prepare all necessary cells to construct a transmission gate, i.e.
	# 1) PMOS
	# 2) NMOS
	pfet = pmos(pdk=pdk, multipliers=1, fingers=finger_num, interfinger_rmult=3, gate_rmult=1, with_tie=False, with_substrate_tap=False, with_dummy=(False, False), width=mos_width, length=pmos_length)
	nfet = nmos(pdk=pdk, multipliers=1, fingers=finger_num, interfinger_rmult=3, gate_rmult=1, with_tie=False, with_dnwell=False, with_substrate_tap=False, with_dummy=(False, False), width=mos_width, length=nmos_length)
	top_level = Component(name=component_name)
	pfet_ref = prec_ref_center(pfet)
	nfet_ref = prec_ref_center(nfet)
	top_level.add(pfet_ref)
	top_level.add(nfet_ref)

	# Placement.step_1:
	#    a) To vertically flip the NMOS such that the its gate point toward the PMOS's gate
	#    b) To move the PMOS above the NMOS
	mos_spacing = pdk.util_max_metal_seperation()
	rename_ports_by_orientation(nfet_ref.mirror_y()) # 
	pfet_ref.movey(evaluate_bbox(nfet)[1] + mos_spacing)

	# Placement.step_2: instantiation of the stacked vias to the source of every PMOS's finger
	fet_source_finger_num = math.ceil((finger_num+1) / 2)
	fet_drain_finger_num = finger_num+1-fet_source_finger_num
	fet_source_fingerL_num = (fet_source_finger_num-1)/2 # excluding the centered one
	fet_drain_fingerL_num = fet_drain_finger_num/2
	finger_col_num = fet_source_finger_num # A half of the fingers belongs to drain
	finger_row_num = math.floor((mos_width*0.5) / (2*pdk.get_grule("met2")["min_width"]))-1 # To pave the stacked vias over all bottom half
	print(f"finger_row_num: {finger_row_num}, finger_col_num: {finger_col_num}")
	pmos_source_sdvias = list()
	nmos_source_sdvias = list()
	pmos_source_sdvias_ref = list()
	nmos_source_sdvias_ref = list()
	sdvias_row = [via_stack(pdk=pdk, glayer1="met2", glayer2="met3", fullbottom=True, fulltop=True) for i in range(finger_col_num)]
	for row in range(finger_row_num):
		pmos_source_sdvias.append(sdvias_row)
		nmos_source_sdvias.append(sdvias_row)

		pmos_temp_ref = list()
		nmos_temp_ref = list()
		for col in range(finger_col_num):
			temp_ref = prec_ref_center(pmos_source_sdvias[row][col])
			pmos_temp_ref.append(temp_ref)
			temp_ref = prec_ref_center(nmos_source_sdvias[row][col])
			nmos_temp_ref.append(temp_ref)

		pmos_source_sdvias_ref.append(pmos_temp_ref)
		nmos_source_sdvias_ref.append(nmos_temp_ref)
		top_level.add(pmos_source_sdvias_ref[row][col] for col in range(finger_col_num))
		top_level.add(nmos_source_sdvias_ref[row][col] for col in range(finger_col_num))

	# Placement.step_3: moving the all the stacked vias associated with the PMOS's source such that
	#                   they are connected to the PMOS's source
	centroid_index = math.floor(fet_source_finger_num/2)
	y_offset = pdk.get_grule("met3")["min_separation"]+pdk.get_grule("met3")["min_width"]
	x_s2d_offset = abs(pfet_ref.ports["multiplier_0_leftsd_array_row0_col0_bottom_via_S"].center[0]-pfet_ref.ports["multiplier_0_row0_col0_rightsd_array_row0_col0_bottom_via_S"].center[0])
	x_offset = x_s2d_offset*2 # Distance between one soure finger to another source finger at its left-/right-hand side is (S-to-D distance)*2
	for row in range(finger_row_num):
		x_spacing = x_offset*centroid_index # initial value
		for col in range(finger_col_num):
			# Moving the positions of the stacked vias associated with the PMOS
			pmos_source_sdvias_ref[row][col].movey(evaluate_bbox(nfet)[1]+mos_spacing-(y_offset*row))
			pmos_source_sdvias_ref[row][col].movex(x_spacing)
			
			# Moving the positions fo the stacked vias associated with NMOS
			nmos_source_sdvias_ref[row][col].movey(y_offset*row) # In NMOS, the row_0 is exactly placed at the center position (0, 0),
			                                                     # thereby no need for moving the stacked vias of row_0, i.e. movey by 0
			nmos_source_sdvias_ref[row][col].movex(x_spacing)
			
			x_spacing = x_spacing-x_offset

	# Routing
	# To simplify the routing for the parallel-gate transistors, the layout is realised as follow which is expected to be equivalent to a TG
	#     a) PMOS.source connected to NMOS.source by placing a large MET2-layered rectangle
	#     b) PMOS.drain connected to NMOS.drain
	source_connection = Component()
	source_connection.add_polygon(
		[
			(nmos_source_sdvias_ref[0][finger_col_num-1].xmin, nmos_source_sdvias_ref[0][finger_col_num-1].ymin),#leftBottom_pos
			(pmos_source_sdvias_ref[0][finger_col_num-1].xmin, pmos_source_sdvias_ref[0][finger_col_num-1].ymax),#leftTop_pos
			(pmos_source_sdvias_ref[0][0].xmax, pmos_source_sdvias_ref[0][0].ymax),#rightTop_pos
			(nmos_source_sdvias_ref[0][0].xmax, nmos_source_sdvias_ref[0][0].ymin) #rightBottom_pos
		],
		layer=pdk.get_glayer("met3")
	)
	source_connection = top_level.add_ref(source_connection)
	top_level << c_route(pdk, pfet_ref.ports["drain_E"], nfet_ref.ports["drain_E"], cglayer="met3") # "out" of the TG

	# Add the ports aligned with the basic PMOS and NMOS
	top_level.add_ports(pfet_ref.get_ports_list(), prefix="pmos_")
	top_level.add_ports(nfet_ref.get_ports_list(), prefix="nmos_")

	if add_pin == True:
		# Add pins w/ labels for LVS
		top_level.unlock()
		pin_info = list() # list that contains all port and component information
		met1_pin=(pdk.get_glayer("met1")[0], 20)
		met1_label=(pdk.get_glayer("met1")[0], 5)
		port_size = (0.24, 0.24)
		# --- Port: A, i.e. input of the transmission gate
		A_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		A_pin.add_label(text="A", layer=met1_label)
		pin_info.append((A_pin, top_level.ports.get(f"nmos_source_S"), None))
		# --- Port: Y, i.e. output of the transmission gate
		Y_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		Y_pin.add_label(text="Y", layer=met1_label)
		pin_info.append((Y_pin, top_level.ports.get(f"nmos_drain_S"), None))
		# --- Port: C, i.e. gate control to the NMOS
		C_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		C_pin.add_label(text="C", layer=met1_label)
		pin_info.append((C_pin, top_level.ports.get(f"nmos_gate_N"), None))
		# --- Port: CBAR, i.e. gate control to the PMOS
		CBAR_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		CBAR_pin.add_label(text="CBAR", layer=met1_label)
		pin_info.append((CBAR_pin, top_level.ports.get(f"pmos_gate_N"), None))

		# Move everythin to position
		for comp, prt, alignment in pin_info:
			alignment = ('c', 'b') if alignment is None else alignment
			comp_ref = align_comp_to_port(comp, prt, alignment=alignment)
			top_level.add(comp_ref)
	
	component = component_snap_to_grid(rename_ports_by_orientation(top_level))

	component.info['netlist'] = transmission_gate_netlist(
		pdk, 
  		width=kwargs.get('width', pmos_width), length=kwargs.get('length', pmos_length), multipliers=1, 
		subckt_only=True
	)
	#component.info['netlist'] = tg_netlist(pmos=pfet, nmos=nfet)
	return component

def reconfig_tg(
	pdk: MappedPDK,
	component_name,
	pmos_width,
	pmos_length,
	nmos_width,
	nmos_length,
	add_pin: bool = True, # For LVS
	**kwargs
) -> Component:
	if pmos_width != nmos_width:
		raise ValueError("PCell constraint: the widths of PMOS and NMOS must be identical")
	elif (pmos_width % comp_dc.tg_fet_width_factor) != 0:
		raise ValueError(f"PCell constraint: the widths of PMOS and NMOS must be multiple of {comp_dc.tg_fet_width_factor} (the given width: {pmos_width})")
	elif pmos_width >= comp_dc.tg_fet_width_base: # Long-width PMOS and NMOS
		tg = long_width_tg(
			pdk=pdk,
			component_name=component_name,
			pmos_width=pmos_width,
			pmos_length=pmos_length,
			nmos_width=nmos_width,
			nmos_length=nmos_length,
			add_pin=True
		)
	else: # Short-width PMOS and NMOS
		tg = short_width_tg(
			pdk=pdk,
			component_name=component_name,
			orientation_config={"degree": 270},
			pmos_width=pmos_width,
			pmos_length=pmos_length,
			nmos_width=nmos_width,
			nmos_length=nmos_length,
			add_pin=True
		)

	return tg