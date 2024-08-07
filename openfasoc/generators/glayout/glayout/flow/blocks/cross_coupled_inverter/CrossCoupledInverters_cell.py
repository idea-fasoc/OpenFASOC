####
# Compiled Glayout
# Apache License
# Version 2.0, January 2004
# http://www.apache.org/licenses/
# 2024-06-01 00:36:26.578529

from glayout.flow.pdk.mappedpdk import MappedPDK
from gdsfactory import Component
from glayout.flow.pdk.util.comp_utils import move, movex, movey, prec_ref_center, evaluate_bbox, center_to_edge_distance
from glayout.flow.pdk.util.port_utils import remove_ports_with_prefix
from glayout.flow.primitives.fet import nmos
from glayout.flow.primitives.fet import pmos
from glayout.flow.primitives.guardring import tapring
from glayout.flow.primitives.mimcap import mimcap
from glayout.flow.primitives.mimcap import mimcap_array
from glayout.flow.primitives.via_gen import via_stack
from glayout.flow.primitives.via_gen import via_array
from glayout.flow.placement.two_transistor_interdigitized import two_nfet_interdigitized
from glayout.flow.placement.four_transistor_interdigitized import generic_4T_interdigitzed
from glayout.flow.placement.two_transistor_interdigitized import two_pfet_interdigitized
from glayout.flow.blocks.diff_pair import diff_pair_generic
from glayout.flow.routing.smart_route import smart_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.straight_route import straight_route

def CrossCoupledInverters_cell(
	pdk: MappedPDK,
	ccinvs_length: float, 
	ccinvs_fingers: int, 
):
	pdk.activate()
	CrossCoupledInverters = Component(name="CrossCoupledInverters")
	maxmetalsep = pdk.util_max_metal_seperation()
	double_maxmetalsep = 2*pdk.util_max_metal_seperation()
	triple_maxmetalsep = 3*pdk.util_max_metal_seperation()
	quadruple_maxmetalsep = 4*pdk.util_max_metal_seperation()
	# placing ccinvs centered at the origin
	ccinvs = generic_4T_interdigitzed(pdk,**{'numcols': ccinvs_fingers, 'length': ccinvs_length, 'top_row_device': "pfet", 'bottom_row_device': "nfet"})
	ccinvs_ref = prec_ref_center(ccinvs)
	CrossCoupledInverters.add(ccinvs_ref)
	CrossCoupledInverters.add_ports(ccinvs_ref.get_ports_list(),prefix="ccinvs_")
	CrossCoupledInverters << smart_route(pdk,CrossCoupledInverters.ports["ccinvs_top_A_source_E"],CrossCoupledInverters.ports["ccinvs_top_B_source_E"],ccinvs_ref,CrossCoupledInverters,**{})
	CrossCoupledInverters << smart_route(pdk,CrossCoupledInverters.ports["ccinvs_bottom_A_source_E"],CrossCoupledInverters.ports["ccinvs_bottom_B_source_E"],ccinvs_ref,CrossCoupledInverters,**{})
	CrossCoupledInverters << smart_route(pdk,CrossCoupledInverters.ports["ccinvs_top_A_drain_E"],CrossCoupledInverters.ports["ccinvs_top_B_gate_E"],ccinvs_ref,CrossCoupledInverters,**{})
	CrossCoupledInverters << smart_route(pdk,CrossCoupledInverters.ports["ccinvs_bottom_A_drain_E"],CrossCoupledInverters.ports["ccinvs_bottom_B_gate_E"],ccinvs_ref,CrossCoupledInverters,**{})
	CrossCoupledInverters << smart_route(pdk,CrossCoupledInverters.ports["ccinvs_top_B_drain_E"],CrossCoupledInverters.ports["ccinvs_top_A_gate_E"],ccinvs_ref,CrossCoupledInverters,**{})
	CrossCoupledInverters << smart_route(pdk,CrossCoupledInverters.ports["ccinvs_bottom_B_drain_E"],CrossCoupledInverters.ports["ccinvs_bottom_A_gate_E"],ccinvs_ref,CrossCoupledInverters,**{})
	CrossCoupledInverters << smart_route(pdk,CrossCoupledInverters.ports["ccinvs_top_B_gate_E"],CrossCoupledInverters.ports["ccinvs_bottom_B_gate_E"],ccinvs_ref,CrossCoupledInverters,**{})
	CrossCoupledInverters << smart_route(pdk,CrossCoupledInverters.ports["ccinvs_top_A_gate_W"],CrossCoupledInverters.ports["ccinvs_bottom_A_gate_W"],ccinvs_ref,CrossCoupledInverters,**{})
	return CrossCoupledInverters
