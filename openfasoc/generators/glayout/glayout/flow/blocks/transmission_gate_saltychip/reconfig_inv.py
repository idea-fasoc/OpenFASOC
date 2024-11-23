from typing import ClassVar, Optional, Any, Union, Literal, Iterable, TypedDict
#from glayout.flow.pdk.gf180_mapped import gf180
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.util.comp_utils import prec_ref_center, movex, movey, evaluate_bbox, align_comp_to_port
from gdsfactory import Component
from gdsfactory.components import rectangle
from glayout.flow.primitives.fet import pmos
from glayout.flow.primitives.fet import nmos
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.smart_route import smart_route

import comp_dc

#@cell
def short_channel_inv(
	pdk: MappedPDK,
	component_name,
	pmos_width,
	pmos_length,
	nmos_width,
	nmos_length,
	orientation,
	add_pin: bool = True, # For LVS
	**kwargs
) -> Component:
	# Create a top level component
	top_level = Component(component_name)
	# To prepare one PMOS and one NMOS for the subsequent inverter cell construction
	pfet = pmos(pdk=pdk, gate_rmult=2, with_substrate_tap=False, with_dummy=(False, True), width=pmos_width, length=pmos_length)
	nfet = nmos(pdk=pdk, gate_rmult=2, with_dnwell=False, with_substrate_tap=False, with_dummy=(True, False), width=nmos_width, length=nmos_length)
	pfet.name="pmos"
	nfet.name="nmos"
	
	# Instantiation of above PMOS and NMOS under the top level
	pfet_ref = prec_ref_center(pfet)
	nfet_ref = prec_ref_center(nfet)
	top_level.add(pfet_ref)
	top_level.add(nfet_ref)
	
	# Placement (relative move)
	mos_spacing = pdk.util_max_metal_seperation(metal_levels=("met1", "met2", "met3", "met4", "met5"))
	if(orientation=="horizontal"):
		pfet_ref.rotate(90)
		nfet_ref.rotate(90)
	else:
		pass
	pfet_ref.movey(evaluate_bbox(nfet)[1] + mos_spacing)

	# Routing
	top_level << straight_route(pdk, pfet_ref.ports["multiplier_0_drain_E"], nfet_ref.ports["multiplier_0_drain_E"], glayer1="met2") # connected by li1
	input_route = top_level << straight_route(pdk, pfet_ref.ports["multiplier_0_gate_W"], nfet_ref.ports["multiplier_0_gate_W"]  , glayer1="met2") # connected by li1

	# To add the ports
	top_level.add_ports(pfet_ref.get_ports_list(), prefix="pmos_")
	top_level.add_ports(nfet_ref.get_ports_list(), prefix="nmos_")

	if add_pin == True:
		# Add pins w/ labels for LVS
		top_level.unlock()
		pin_info = list() # list that contains all port and component information
		met1_pin=(pdk.get_glayer("met1")[0], 20)
		met1_label=(pdk.get_glayer("met1")[0], 5)
		port_size = (0.24, 0.24)
		# --- Port: A, i.e. input of the inverter
		A_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		A_pin.add_label(text="A", layer=met1_label)
		pin_info.append((A_pin, top_level.ports.get(f"nmos_gate_E"), None))
		# --- Port: Y, i.e. output of the inverver
		Y_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		Y_pin.add_label(text="Y", layer=met1_label)
		pin_info.append((Y_pin, top_level.ports.get(f"nmos_drain_E"), None))
		# --- Port: VDD
		VDD_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		VDD_pin.add_label(text="VDD", layer=met1_label)
		pin_info.append((VDD_pin, top_level.ports.get(f"pmos_drain_E"), None))
		# --- Port: VSS
		VSS_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		VSS_pin.add_label(text="VSS", layer=met1_label)
		pin_info.append((VSS_pin, top_level.ports.get(f"nmos_source_W"), ('r', 't')))

		# Move everythin to position
		for comp, prt, alignment in pin_info:
			alignment = ('c', 'b') if alignment is None else alignment
			comp_ref = align_comp_to_port(comp, prt, alignment=alignment)
			top_level.add(comp_ref)

	return top_level

#@cell
def long_channel_inv(
	pdk: MappedPDK,
	component_name,
	pmos_width,
	pmos_length,
	nmos_width,
	nmos_length,
	orientation_config: dict[str, Union[int, str]],
	add_pin: bool = True, # For LVS
	**kwargs
) -> Component:
	# Create a top level component
	top_level = Component(component_name)
	# To prepare one PMOS and one NMOS for the subsequent inverter cell construction
	pfet = pmos(pdk=pdk, gate_rmult=1, with_substrate_tap=False, with_dummy=(False, False), width=pmos_width, length=pmos_length)
	nfet = nmos(pdk=pdk, gate_rmult=1, with_dnwell=False, with_substrate_tap=False, with_dummy=(False, False), width=nmos_width, length=nmos_length)
	pfet.name="pmos"
	nfet.name="nmos"
	
	# Instantiation of above PMOS and NMOS under the top level
	pfet_ref = prec_ref_center(pfet)
	nfet_ref = prec_ref_center(nfet)
	top_level.add(pfet_ref)
	top_level.add(nfet_ref)
	
	# Placement (relative move)
	mos_spacing = pdk.util_max_metal_seperation(metal_levels=("met1", "met2", "met3", "met4", "met5"))
	if orientation_config["pmos_degree"] != None:
		pfet_ref.rotate(orientation_config["pmos_degree"])
	if orientation_config["nmos_degree"] != None:
		nfet_ref.rotate(orientation_config["nmos_degree"])
	pfet_ref.movey(evaluate_bbox(nfet)[1] + mos_spacing)

	# Routing
	top_level << c_route(pdk, pfet_ref.ports["multiplier_0_drain_E"], nfet_ref.ports["multiplier_0_drain_W"], cglayer="met3") # connected by li1
	top_level << smart_route(pdk, pfet_ref.ports["multiplier_0_gate_S"], nfet_ref.ports["multiplier_0_gate_S"]) # connected by li1

	# To add the ports
	top_level.add_ports(pfet_ref.get_ports_list(), prefix="pmos_")
	top_level.add_ports(nfet_ref.get_ports_list(), prefix="nmos_")

	if add_pin == True:
		# Add pins w/ labels for LVS
		top_level.unlock()
		pin_info = list() # list that contains all port and component information
		met1_pin=(pdk.get_glayer("met1")[0], 20)
		met1_label=(pdk.get_glayer("met1")[0], 5)
		port_size = (0.24, 0.24)
		# --- Port: A, i.e. input of the inverter
		A_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		A_pin.add_label(text="A", layer=met1_label)
		pin_info.append((A_pin, top_level.ports.get(f"nmos_gate_S"), None))
		# --- Port: Y, i.e. output of the inverver
		Y_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		Y_pin.add_label(text="Y", layer=met1_label)
		pin_info.append((Y_pin, top_level.ports.get(f"nmos_drain_E"), None))
		# --- Port: VDD
		VDD_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		VDD_pin.add_label(text="VDD", layer=met1_label)
		pin_info.append((VDD_pin, top_level.ports.get(f"pmos_drain_E"), None))
		# --- Port: VSS
		VSS_pin=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
		VSS_pin.add_label(text="VSS", layer=met1_label)
		pin_info.append((VSS_pin, top_level.ports.get(f"nmos_source_W"), ('r', 't')))

		# Move everythin to position
		for comp, prt, alignment in pin_info:
			alignment = ('c', 'b') if alignment is None else alignment
			comp_ref = align_comp_to_port(comp, prt, alignment=alignment)
			top_level.add(comp_ref)

	return top_level

#@cell
def reconfig_inv(
	pdk,
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
	elif pmos_width >= comp_dc.inv_fet_width_base: # Long-channel PMOS and NMOS
		inv = long_channel_inv(
			pdk=pdk,
			component_name=component_name,
			orientation_config={"pmos_degree":0, "nmos_degree":180},
			pmos_width=pmos_width,
			pmos_length=pmos_length,
			nmos_width=nmos_width,
			nmos_length=nmos_length,
			add_pin=True
		)
	else: # Short-channel PMOS and NMOS
		inv = short_channel_inv(
			pdk=pdk,
			component_name=component_name,
			orientation="horizontal",
			pmos_width=pmos_width,
			pmos_length=pmos_length,
			nmos_width=nmos_width,
			nmos_length=nmos_length,
			add_pin=True
		)

	return inv