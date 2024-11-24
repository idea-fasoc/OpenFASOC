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
from glayout.flow.primitives.guardring import tapring

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
XM1 Y C A VDD {model_pmos} l={{l}} w={{w}} m={{m}}
XM2 Y CBAR A VSS {model_nmos} l={{l}} w={{w}} m={{m}}"""
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

#@cell
def short_width_tg(
	pdk: MappedPDK,
	component_name: str = "tg",
	with_substrate_tap: bool = False,
	fet_min_width: float = 3,
	pmos_width: float = 3,
	pmos_length: float = 0.15,
	nmos_width: float = 3,
	nmos_length: float = 0.15,
	add_pin: bool = True, # For LVS
	**kwargs
) -> Component:

	# To prepare all necessary cells to construct a transmission gate, i.e.
	# 1) PMOS
	# 2) NMOS
	pfet = pmos(pdk=pdk, gate_rmult=1, with_tie=False, with_substrate_tap=False, with_dummy=(True, True), width=pmos_width, length=pmos_length)
	nfet = nmos(pdk=pdk, gate_rmult=1, with_tie=False, with_dnwell=False, with_substrate_tap=False, with_dummy=(True, True), width=nmos_width, length=nmos_length)
	top_level = Component(name=component_name)
	pfet_ref = prec_ref_center(pfet)
	nfet_ref = prec_ref_center(nfet)
	top_level.add(pfet_ref)
	top_level.add(nfet_ref)

	# Placement (1)
	#  a) To vertically flip the NMOS such that the its gate point toward the PMOS's gate
	#  b) To move the PMOS above the NMOS
	mos_spacing = pdk.util_max_metal_seperation()
	rename_ports_by_orientation(nfet_ref.mirror_y())
	pfet_ref.movey(evaluate_bbox(nfet)[1] + mos_spacing)

	# Add the ports aligned with the basic PMOS and NMOS
	top_level.add_ports(pfet_ref.get_ports_list(), prefix="pmos_")
	top_level.add_ports(nfet_ref.get_ports_list(), prefix="nmos_")
	
	# Placement (2):
	#  a) Add a bunch of met1-to-met2 vias attached to the mcron-layered points inside the source of PMOS/NMOS
	#  b) Add a bunch of met1-to-met2 vias attached to the mcron-layered points inside the drain of PMOS/NMOS
	fet_source_finger_num = 1
	fet_drain_finger_num = 1
	finger_col_num = 1
	finger_row_num = math.floor((fet_min_width*0.5) / (2*pdk.get_grule("met2")["min_width"]))-1 # To pave the stacked vias over all bottom half
	pmos_source_sdvias = list()
	nmos_source_sdvias = list()
	pmos_drain_sdvias = list()
	nmos_drain_sdvias = list()
	pmos_source_sdvias_ref = list()
	nmos_source_sdvias_ref = list()
	pmos_drain_sdvias_ref = list()
	nmos_drain_sdvias_ref = list()
	sdvias_row = [via_stack(pdk=pdk, glayer1="met2", glayer2="met3", fullbottom=True, fulltop=True) for i in range(finger_col_num)]
	for row in range(finger_row_num):
		pmos_source_sdvias.append(sdvias_row)
		nmos_source_sdvias.append(sdvias_row)
		pmos_drain_sdvias.append(sdvias_row)
		nmos_drain_sdvias.append(sdvias_row)

		pmos_source_cols_ref = list()
		nmos_source_cols_ref = list()
		pmos_drain_cols_ref = list()
		nmos_drain_cols_ref = list()
		for col in range(finger_col_num):
			# For source terminals of the PMOS and NMOS
			temp_ref = prec_ref_center(pmos_source_sdvias[row][col])
			pmos_source_cols_ref.append(temp_ref)
			temp_ref = prec_ref_center(nmos_source_sdvias[row][col])
			nmos_source_cols_ref.append(temp_ref)
			# For drain terminals of the PMOS and NMOS
			temp_ref = prec_ref_center(pmos_drain_sdvias[row][col])
			pmos_drain_cols_ref.append(temp_ref)
			temp_ref = prec_ref_center(nmos_drain_sdvias[row][col])
			nmos_drain_cols_ref.append(temp_ref)

		pmos_source_sdvias_ref.append(pmos_source_cols_ref)
		nmos_source_sdvias_ref.append(nmos_source_cols_ref)
		pmos_drain_sdvias_ref.append(pmos_drain_cols_ref)
		nmos_drain_sdvias_ref.append(nmos_drain_cols_ref)
		top_level.add(pmos_source_sdvias_ref[row][col] for col in range(finger_col_num))
		top_level.add(nmos_source_sdvias_ref[row][col] for col in range(finger_col_num))
		top_level.add(pmos_drain_sdvias_ref[row][col] for col in range(finger_col_num))
		top_level.add(nmos_drain_sdvias_ref[row][col] for col in range(finger_col_num))

	# Placement (3): 
	#  a) Move all the a part of particular stacked vias such that they are connected to the source of PMOS/NMOS
	#  b) Move all the a part of particular stacked vias such that they are connected to the drain of PMOS/NMOS
	y_offset = pdk.get_grule("met3")["min_separation"]+pdk.get_grule("met3")["min_width"]
	x_offset = abs(top_level.ports["pmos_multiplier_0_leftsd_array_row0_col0_bottom_via_N"].center[0]-pfet_ref.center[0])
	for row in range(finger_row_num):
		# Moving the positions of the stacked vias associated with the PMOS
		pmos_source_sdvias_ref[row][0].movex(-x_offset)
		pmos_source_sdvias_ref[row][0].movey(evaluate_bbox(nfet)[1]+mos_spacing-(y_offset*row))
		pmos_drain_sdvias_ref[row][0].movex(x_offset)
		pmos_drain_sdvias_ref[row][0].movey(evaluate_bbox(nfet)[1]+mos_spacing-(y_offset*row))
		
		# Moving the positions fo the stacked vias associated with NMOS
		nmos_source_sdvias_ref[row][0].movex(-x_offset)
		nmos_source_sdvias_ref[row][0].movey(y_offset*row)
		nmos_drain_sdvias_ref[row][0].movex(x_offset)
		nmos_drain_sdvias_ref[row][0].movey(y_offset*row)

	# Routing
	#   a) PMOS.source connected to NMOS.source by placing a large MET2-layered rectangle
	#   b) PMOS.drain connected to NMOS.drain by placing a large MET2-layered rectangle
	print("nmos_source_sdvias_ref.len: ", nmos_source_sdvias_ref)
	sdvias_connection = Component()
	sdvias_connection.add_polygon(
		[
			(nmos_source_sdvias_ref[0][finger_col_num-1].xmin, nmos_source_sdvias_ref[0][finger_col_num-1].ymin),#leftBottom_pos
			(pmos_source_sdvias_ref[0][finger_col_num-1].xmin, pmos_source_sdvias_ref[0][finger_col_num-1].ymax),#leftTop_pos
			(pmos_source_sdvias_ref[0][0].xmax, pmos_source_sdvias_ref[0][0].ymax),#rightTop_pos
			(nmos_source_sdvias_ref[0][0].xmax, nmos_source_sdvias_ref[0][0].ymin) #rightBottom_pos
		],
		layer=pdk.get_glayer("met3")
	)
	sdvias_connection.add_polygon(
		[
			(nmos_drain_sdvias_ref[0][finger_col_num-1].xmin, nmos_drain_sdvias_ref[0][finger_col_num-1].ymin),#leftBottom_pos
			(pmos_drain_sdvias_ref[0][finger_col_num-1].xmin, pmos_drain_sdvias_ref[0][finger_col_num-1].ymax),#leftTop_pos
			(pmos_drain_sdvias_ref[0][0].xmax, pmos_drain_sdvias_ref[0][0].ymax),#rightTop_pos
			(nmos_drain_sdvias_ref[0][0].xmax, nmos_drain_sdvias_ref[0][0].ymin) #rightBottom_pos
		],
		layer=pdk.get_glayer("met3")
	)
	sdvias_connection_ref = top_level.add_ref(sdvias_connection)

	# Add pins w/ labels for LVS
	if add_pin == True:
		top_level.unlock()
		pin_info = list() # list that contains all port and component information
		met1_pin=(pdk.get_glayer("met1")[0], 20)
		met1_label=(pdk.get_glayer("met1")[0], 5)
		port_size = (0.24, 0.24)
		# --- Port: A, i.e. input of the transmission gate
		A_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		A_pin.add_label(text="A", layer=met1_label)
		pin_info.append((A_pin, top_level.ports.get(f"nmos_source_W"), ('r', 't')))
		# --- Port: Y, i.e. output of the transmission gate
		Y_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		Y_pin.add_label(text="Y", layer=met1_label)
		pin_info.append((Y_pin, top_level.ports.get(f"nmos_drain_E"), ('l', 't')))
		# --- Port: C, i.e. gate control to the NMOS
		C_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		C_pin.add_label(text="C", layer=met1_label)
		pin_info.append((C_pin, top_level.ports.get(f"nmos_gate_S"), None))
		# --- Port: CBAR, i.e. gate control to the PMOS
		CBAR_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		CBAR_pin.add_label(text="CBAR", layer=met1_label)
		pin_info.append((CBAR_pin, top_level.ports.get(f"pmos_gate_N"), None))

		# Move everythin to position
		for comp, prt, alignment in pin_info:
			alignment = ('c', 'b') if alignment is None else alignment
			comp_ref = align_comp_to_port(comp, prt, alignment=alignment)
			top_level.add(comp_ref)

	# Add substrate tap
	if with_substrate_tap:
		substrate_tap = tapring(pdk, enclosed_rectangle=pdk.snap_to_2xgrid(evaluate_bbox(top_level.flatten(),padding=pdk.util_max_metal_seperation())))
		substrate_tap_ref = top_level << movey(substrate_tap,destination=pdk.snap_to_2xgrid(top_level.flatten().center[1],snap4=True))
		top_level.add_ports(substrate_tap_ref.get_ports_list(),prefix="substratetap_")

	top_level = component_snap_to_grid(rename_ports_by_orientation(top_level))
	top_level.info['netlist'] = transmission_gate_netlist(
		pdk, 
  		width=kwargs.get('width', pmos_width), length=kwargs.get('length', pmos_length), multipliers=1, 
		subckt_only=True
	)
	top_level.info['netlist'].generate_netlist()
	return top_level


#@cell
def long_width_tg(
	pdk: MappedPDK,
	component_name: str = "tg",
	fet_min_width: float = 3,
	pmos_width: float = 12,
	pmos_length: float = 0.15,
	nmos_width: float = 12,
	nmos_length: float = 0.15,
	with_substrate_tap: bool = True,
	add_pin: bool = True, # For LVS
	**kwargs
) -> Component:
	# To calculate the number of fingers for the underlying PMOS/NMOS layout
	finger_num = math.ceil(pmos_width / fet_min_width)

	# To prepare all necessary cells to construct a transmission gate, i.e.
	# 1) PMOS
	# 2) NMOS
	pfet = pmos(pdk=pdk, multipliers=1, fingers=finger_num, interfinger_rmult=1, gate_rmult=1, with_tie=False, with_substrate_tap=False, with_dummy=(True, True), width=fet_min_width, length=pmos_length)
	nfet = nmos(pdk=pdk, multipliers=1, fingers=finger_num, interfinger_rmult=1, gate_rmult=1, with_tie=False, with_dnwell=False, with_substrate_tap=False, with_dummy=(True, True), width=fet_min_width, length=nmos_length)
	top_level = Component(name=component_name)
	pfet_ref = prec_ref_center(pfet)
	nfet_ref = prec_ref_center(nfet)
	top_level.add(pfet_ref)
	top_level.add(nfet_ref)

	# Placement (1)
	#  a) To vertically flip the NMOS such that the its gate point toward the PMOS's gate
	#  b) To move the PMOS above the NMOS
	mos_spacing = pdk.util_max_metal_seperation()
	rename_ports_by_orientation(nfet_ref.mirror_y()) # 
	pfet_ref.movey(evaluate_bbox(nfet)[1] + mos_spacing)

	# Placement (2):
	#  a) Add a bunch of met1-to-met2 vias attached to the mcron-layered points inside the source of PMOS/NMOS
	fet_source_finger_num = math.ceil((finger_num+1) / 2)
	fet_drain_finger_num = finger_num+1-fet_source_finger_num
	fet_source_fingerL_num = (fet_source_finger_num-1)/2 # excluding the centered one
	fet_drain_fingerL_num = fet_drain_finger_num/2
	finger_col_num = fet_source_finger_num # A half of the fingers belongs to drain
	finger_row_num = math.floor((fet_min_width*0.5) / (2*pdk.get_grule("met2")["min_width"]))-1 # To pave the stacked vias over all bottom half
#	print(f"finger_row_num: {finger_row_num}, finger_col_num: {finger_col_num}")
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

	# Placement (3): 
	#  a) Move all the a part of particular stacked vias such that they are connected to the source of PMOS/NMOS
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

	# Add pins w/ labels for LVS
	if add_pin == True:
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
		pin_info.append((C_pin, top_level.ports.get(f"nmos_gate_S"), None))
		# --- Port: CBAR, i.e. gate control to the PMOS
		CBAR_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		CBAR_pin.add_label(text="CBAR", layer=met1_label)
		pin_info.append((CBAR_pin, top_level.ports.get(f"pmos_gate_N"), None))

		# Move everythin to position
		for comp, prt, alignment in pin_info:
			alignment = ('c', 'b') if alignment is None else alignment
			comp_ref = align_comp_to_port(comp, prt, alignment=alignment)
			top_level.add(comp_ref)
			
	# Add substrate tap
	if with_substrate_tap:
		substrate_tap = tapring(pdk, enclosed_rectangle=pdk.snap_to_2xgrid(evaluate_bbox(top_level.flatten(),padding=pdk.util_max_metal_seperation())))
		substrate_tap_ref = top_level << movey(substrate_tap,destination=pdk.snap_to_2xgrid(top_level.flatten().center[1],snap4=True))
		top_level.add_ports(substrate_tap_ref.get_ports_list(),prefix="substratetap_")

	top_level = component_snap_to_grid(rename_ports_by_orientation(top_level))
	top_level.info['netlist'] = transmission_gate_netlist(
		pdk, 
  		width=kwargs.get('width', pmos_width), length=kwargs.get('length', pmos_length), multipliers=finger_num, 
		subckt_only=True
	)
	top_level.info['netlist'].generate_netlist()

	return top_level

@cell
def tg_cell(
	pdk: MappedPDK,
	component_name: str = "tg",
	fet_min_width: float = 3,
	pmos_width: float = 12,
	pmos_length: float = 0.15,
	nmos_width: float = 12,
	nmos_length: float = 0.15,
	add_pin: bool = True, # For LVS
	with_substrate_tap: bool = True,
	**kwargs
) -> Component:
	if pmos_width != nmos_width:
		raise ValueError("PCell constraint: the widths of PMOS and NMOS must be identical")
	elif pmos_width > fet_min_width: # Long-width PMOS and NMOS
		if (pmos_width % (fet_min_width*4)) != 0:
			raise ValueError(f"PCell constraint: the widths of PMOS and NMOS must be a multiple of {fet_min_width*4} um, however the given width is {pmos_width} um")
		else:
			tg = long_width_tg(
				pdk=pdk,
				component_name=component_name,
				fet_min_width=fet_min_width,
				pmos_width=pmos_width,
				pmos_length=pmos_length,
				nmos_width=nmos_width,
				nmos_length=nmos_length,
				with_substrate_tap=True,
				add_pin=True
			)
	else: # Short-width PMOS and NMOS
		tg = short_width_tg(
			pdk=pdk,
			component_name=component_name,
			fet_min_width=fet_min_width,
			pmos_width=pmos_width,
			pmos_length=pmos_length,
			nmos_width=nmos_width,
			nmos_length=nmos_length,
			with_substrate_tap=True,
			add_pin=True
		)

	return tg