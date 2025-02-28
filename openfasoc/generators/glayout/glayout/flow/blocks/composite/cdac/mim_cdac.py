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
import cdac_sw as cdac_sw
import mimcap_array as mimcap_arr

def mim_cdac(
	pdk: MappedPDK,
	component_name: str = "cdac_sw_1b",
	with_substrate_tap: dict[str, bool] = {'top_level': False, 'pmos': False, 'nmos': False},
	tap_cell: dict[str, bool]={"pmos": True, "nmos": True},
	fet_min_width: float = 3,
	pmos_width: float = 12,
	pmos_length: float = 0.15,
	nmos_width: float = 12,
	nmos_length: float = 0.15,
	add_pin: bool = True, # For LVS
	**kwargs
) -> Component:
    cdac_bitwidth = 6

    mimcap_arr_inst = mimcap_arr.create_6bit_dac_mimcap_array(pdk)
    cdac_sw_inst = cdac_sw.cdac_sw(
		pdk=pdk,
		component_name="cdac_sw_1b",
		with_substrate_tap={"top_level":False, "pmos":False, "nmos":False},
		tap_cell={"pmos":True, "nmos":True},
		fet_min_width=fet_min_width,
		pmos_width=pmos_width,
		pmos_length=pmos_length,
		nmos_width=nmos_width,
		nmos_length=nmos_length,
		add_pin=True
	)
    
    top_level = Component(name=component_name)
    mimcap_arr_ref = prec_ref_center(mimcap_arr_inst)
    top_level.add(mimcap_arr_ref)

    cdac_sw_ref_list = list()
    mos_spacing = pdk.util_max_metal_seperation()+abs(cdac_sw_inst.ymax-cdac_sw_inst.ymin)
    for i in range(cdac_bitwidth):
        temp = prec_ref_center(cdac_sw_inst)
        cdac_sw_ref_list.append(temp)
        top_level.add(cdac_sw_ref_list[i])
        cdac_sw_ref_list[i].movex(mimcap_arr_ref.xmax+mos_spacing)
        cdac_sw_ref_list[i].movey(mos_spacing*i)
        top_level.add_ports(cdac_sw_ref_list[i].get_ports_list(), prefix=f"cdac_sw{i}_")

	# Placement (1)
	# 	To move the transmission gate cell to the right-hand side of the inverter
	#	To move the NMOS to the right-hand side of the transmission gate
    mimcap_arr_ref.rotate(90)
    
	# Add the ports aligned with the instantiated inv, tg and PMOS cells
    top_level.add_ports(mimcap_arr_ref.get_ports_list(), prefix="mimcap_arr_")

	# Routing (1)
	#	a)
    for i in range(cdac_bitwidth):
        top_level << smart_route(pdk, mimcap_arr_ref.ports[f"top_c{i}"], cdac_sw_ref_list[i].ports["inv_A_W"])
    
    return top_level
