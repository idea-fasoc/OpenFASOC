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

# My own cell library
from reconfig_inv import reconfig_inv
	
#@cell
def tg_cell(
	pdk: MappedPDK,
	flip_config:
	dict[str, Union[int, str]],
	pmos_width,
	pmos_length,
	nmos_width,
	nmos_length,
	**kwargs
) -> Component:
	# To prepare all necessary cells to construct a transmission gate, i.e.
	# 1) PMOS
	# 2) NMOS
	pfet = pmos(pdk=pdk, with_substrate_tap=False, with_dummy=(True, False), width=pmos_width, length=pmos_length)
	nfet = nmos(pdk=pdk, with_substrate_tap=False, with_dummy=(False, True), width=nmos_width, length=nmos_length)

	# Placement and adding ports
	top_level = Component(name="tg_1b")
	pfet_ref = prec_ref_center(pfet)
	nfet_ref = prec_ref_center(nfet)
	top_level.add(pfet_ref)
	top_level.add(nfet_ref)

	# Placement
	mos_spacing = pdk.util_max_metal_seperation()
	if flip_config["degree"] != None:
		pfet_ref.rotate(flip_config["degree"])
		nfet_ref.rotate(flip_config["degree"])
	pfet_ref.movey(evaluate_bbox(nfet)[1] + mos_spacing)

	# Routing
	# To simplify the routing for the parallel-gate transistors, the layout is realised as follow which is expected to be equivalent to a TG
	#     a) PMOS.source connected to NMOS.source
	#     b) PMOS.drain connected to NMOS.drain 
	top_level << straight_route(pdk, pfet_ref.ports["multiplier_0_source_E"], nfet_ref.ports["multiplier_0_drain_E"], glayer1="met2") # "in" of the TG
	top_level << straight_route(pdk, pfet_ref.ports["multiplier_0_drain_W"], nfet_ref.ports["multiplier_0_source_E"], glayer1="met3") # "out" of the TG

	top_level.add_ports(pfet_ref.get_ports_list(), prefix="pmos_")
	top_level.add_ports(nfet_ref.get_ports_list(), prefix="nmos_")

	return top_level

#@cell
def tg_with_ctrl(pdk: MappedPDK, pmos_width, pmos_length, nmos_width, nmos_length):
	# To prepare all necessary cells to construct a transmission gate, i.e.
	# 1) transmission gate
	# 2) Inverter
	tg = tg_cell(pdk=pdk, flip_config={"degree": 270}, pmos_width=pmos_width, pmos_length=pmos_length, nmos_width=nmos_width, nmos_length=nmos_length)
	inv = reconfig_inv(pdk=pdk, component_name="gate_ctrl_inv", pmos_width=pmos_width, pmos_length=pmos_length, nmos_width=nmos_width, nmos_length=nmos_length, orientation="horizontal")

	# Instantiation of the essential cells
	top_level = Component(name="tg_with_inv")
	tg_ref = prec_ref_center(tg)
	inv_ref = prec_ref_center(inv)
	top_level.add(tg_ref)
	top_level.add(inv_ref)

	# Placement
	mos_spacing = pdk.util_max_metal_seperation()
	nwell_min_spacing = pdk.get_grule("nwell")["min_separation"]
	inv_cell_width = inv_ref.xsize # or = evaluate_bbox(inv)[0]
	tg_ref.movex(inv_cell_width + nwell_min_spacing)

	# Routing
	#    1) PMOS of the TG is switched on/off by the inverter's output
	#    2) NMOS of the TG is switched on/off by an external control signal connected to inverter's input port as well
	top_level << smart_route(pdk, inv_ref.ports["pmos_multiplier_0_drain_E"], tg_ref.ports["pmos_multiplier_0_gate_W"])
	top_level << straight_route(pdk, inv_ref.ports["nmos_multiplier_0_gate_S"], tg_ref.ports["nmos_multiplier_0_gate_S"], glayer1="met3")

	# Adding the ports
	top_level.add_ports(tg_ref.get_ports_list(), prefix="tg_")
	top_level.add_ports(inv_ref.get_ports_list(), prefix="inv_")

	return top_level

