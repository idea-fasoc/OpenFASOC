####
# Compiled Glayout
# Apache License
# Version 2.0, January 2004
# http://www.apache.org/licenses/
# 2024-05-16 19:29:27.736502

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
from glayout.flow.components.diff_pair import diff_pair_generic
from glayout.flow.routing.smart_route import smart_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.components.diff_pair import diff_pair
from glayout.flow.placement.four_transistor_interdigitized import generic_4T_interdigitzed
from glayout.flow.components.current_mirror import current_mirror

def opamp_cell(
	pdk: MappedPDK,
	numcols: int, 
	load_pfet_width: float, 
	load_pfet_fingers: int, 
	load_pfet_multipliers: int, 
	load_curr_source_fingers: int, 
	load_curr_source_width_ref: float, 
	load_curr_source_width_mirr: float, 
	mim_cap_size: tuple, 
	mim_cap_rows: int, 
):
	pdk.activate()
	opamp = Component(name="opamp")
	maxmetalsep = pdk.util_max_metal_seperation()
	double_maxmetalsep = 2*pdk.util_max_metal_seperation()
	triple_maxmetalsep = 3*pdk.util_max_metal_seperation()
	quadruple_maxmetalsep = 4*pdk.util_max_metal_seperation()
	# placing mydiffload centered at the origin
	mydiffload = generic_4T_interdigitzed(pdk,**{'numcols': numcols, 'top_kwargs': { "tie_layers" : ( "met3" , "met2" ) }, 'top_row_device': "pfet", 'bottom_row_device': "pfet"})
	mydiffload_ref = prec_ref_center(mydiffload)
	opamp.add(mydiffload_ref)
	opamp.add_ports(mydiffload_ref.get_ports_list(),prefix="mydiffload_")
	# placing mydiff centered at the origin
	mydiff = diff_pair(pdk,**{'width': 5, 'fingers': numcols, 'dummy': True, 'substrate_tap': True})
	mydiff_ref = prec_ref_center(mydiff)
	opamp.add(mydiff_ref)
	opamp.add_ports(mydiff_ref.get_ports_list(),prefix="mydiff_")
	# move mydiffload north mydiff
	relativemovcorrection_0 = 1*(maxmetalsep + center_to_edge_distance(mydiff_ref,2) + center_to_edge_distance(mydiffload_ref,4))
	movey(mydiffload_ref,destination=(relativemovcorrection_0 + mydiff_ref.center[1]))
	remove_ports_with_prefix(opamp,"mydiffload_")
	opamp.add_ports(mydiffload_ref.get_ports_list(),prefix="mydiffload_")
	opamp << smart_route(pdk,opamp.ports["mydiffload_top_A_source_W"],opamp.ports["mydiffload_top_B_source_W"],mydiffload_ref,opamp,**{})
	opamp << c_route(pdk,opamp.ports["mydiffload_top_A_gate_W"],opamp.ports["mydiffload_top_B_gate_W"],**{'extension': 2})
	opamp << c_route(pdk,opamp.ports["mydiffload_bottom_A_gate_W"],opamp.ports["mydiffload_bottom_B_gate_W"],**{'extension': 2})
	opamp << smart_route(pdk,opamp.ports["mydiffload_bottom_A_gate_E"],opamp.ports["mydiffload_top_A_gate_E"],mydiffload_ref,opamp,**{})
	opamp << smart_route(pdk,opamp.ports["mydiffload_bottom_A_gate_E"],opamp.ports["mydiffload_top_A_gate_E"],mydiffload_ref,opamp,**{})
	opamp << smart_route(pdk,opamp.ports["mydiffload_top_A_drain_W"],opamp.ports["mydiffload_bottom_A_source_W"],mydiffload_ref,opamp,**{})
	opamp << c_route(pdk,opamp.ports["mydiffload_top_B_drain_E"],opamp.ports["mydiffload_bottom_B_source_E"],**{'extension': 2})
	opamp << smart_route(pdk,opamp.ports["mydiffload_bottom_B_drain_W"],opamp.ports["mydiffload_bottom_B_gate_W"],mydiffload_ref,opamp,**{})
	opamp << c_route(pdk,opamp.ports["mydiffload_top_A_drain_W"],opamp.ports["mydiff_bl_multiplier_0_drain_W"],**{'extension': 4})
	opamp << c_route(pdk,opamp.ports["mydiffload_top_B_drain_E"],opamp.ports["mydiff_br_multiplier_0_drain_E"],**{'extension': 4})
	# placing mycurrmirror centered at the origin
	mycurrmirror = current_mirror(pdk,**{'numcols': numcols, 'device': "nfet", 'with_dummy': False})
	mycurrmirror_ref = prec_ref_center(mycurrmirror)
	opamp.add(mycurrmirror_ref)
	opamp.add_ports(mycurrmirror_ref.get_ports_list(),prefix="mycurrmirror_")
	# move mycurrmirror south mydiff
	relativemovcorrection_0 = -1*(maxmetalsep + center_to_edge_distance(mydiff_ref,4) + center_to_edge_distance(mycurrmirror_ref,2))
	movey(mycurrmirror_ref,destination=(relativemovcorrection_0 + mydiff_ref.center[1]))
	remove_ports_with_prefix(opamp,"mycurrmirror_")
	opamp.add_ports(mycurrmirror_ref.get_ports_list(),prefix="mycurrmirror_")
	opamp << c_route(pdk,opamp.ports["mydiff_bl_multiplier_0_source_W"],opamp.ports["mycurrmirror_fet_B_0_source_W"],**{'extension': 3})
	# placing load_pfet_left centered at the origin
	load_pfet_left = pmos(pdk,**{'width': load_pfet_width, 'fingers': load_pfet_fingers, 'multipliers': load_pfet_multipliers})
	load_pfet_left_ref = prec_ref_center(load_pfet_left)
	opamp.add(load_pfet_left_ref)
	opamp.add_ports(load_pfet_left_ref.get_ports_list(),prefix="load_pfet_left_")
	# move load_pfet_left left mydiff
	relativemovcorrection_0 = -1*(maxmetalsep + center_to_edge_distance(mydiff_ref,1) + center_to_edge_distance(load_pfet_left_ref,3))
	movex(load_pfet_left_ref,destination=(relativemovcorrection_0 + mydiff_ref.center[0]))
	remove_ports_with_prefix(opamp,"load_pfet_left_")
	opamp.add_ports(load_pfet_left_ref.get_ports_list(),prefix="load_pfet_left_")
	# move load_pfet_left north mydiff
	relativemovcorrection_0 = 1*(maxmetalsep + center_to_edge_distance(mydiff_ref,2) + center_to_edge_distance(load_pfet_left_ref,4))
	movey(load_pfet_left_ref,destination=(relativemovcorrection_0 + mydiff_ref.center[1]))
	remove_ports_with_prefix(opamp,"load_pfet_left_")
	opamp.add_ports(load_pfet_left_ref.get_ports_list(),prefix="load_pfet_left_")
	# move load_pfet_left left mydiffload
	relativemovcorrection_0 = -1*(maxmetalsep + center_to_edge_distance(mydiffload_ref,1) + center_to_edge_distance(load_pfet_left_ref,3))
	movex(load_pfet_left_ref,destination=(relativemovcorrection_0 + mydiffload_ref.center[0]))
	remove_ports_with_prefix(opamp,"load_pfet_left_")
	opamp.add_ports(load_pfet_left_ref.get_ports_list(),prefix="load_pfet_left_")
	# placing load_pfet_right centered at the origin
	load_pfet_right = pmos(pdk,**{'width': load_pfet_width, 'fingers': load_pfet_fingers, 'multipliers': load_pfet_multipliers})
	load_pfet_right_ref = prec_ref_center(load_pfet_right)
	opamp.add(load_pfet_right_ref)
	opamp.add_ports(load_pfet_right_ref.get_ports_list(),prefix="load_pfet_right_")
	# move load_pfet_right right mydiff
	relativemovcorrection_0 = 1*(maxmetalsep + center_to_edge_distance(mydiff_ref,3) + center_to_edge_distance(load_pfet_right_ref,1))
	movex(load_pfet_right_ref,destination=(relativemovcorrection_0 + mydiff_ref.center[0]))
	remove_ports_with_prefix(opamp,"load_pfet_right_")
	opamp.add_ports(load_pfet_right_ref.get_ports_list(),prefix="load_pfet_right_")
	# move load_pfet_right north mydiff
	relativemovcorrection_0 = 1*(maxmetalsep + center_to_edge_distance(mydiff_ref,2) + center_to_edge_distance(load_pfet_right_ref,4))
	movey(load_pfet_right_ref,destination=(relativemovcorrection_0 + mydiff_ref.center[1]))
	remove_ports_with_prefix(opamp,"load_pfet_right_")
	opamp.add_ports(load_pfet_right_ref.get_ports_list(),prefix="load_pfet_right_")
	# move load_pfet_right right mydiffload
	relativemovcorrection_0 = 1*(maxmetalsep + center_to_edge_distance(mydiffload_ref,3) + center_to_edge_distance(load_pfet_right_ref,1))
	movex(load_pfet_right_ref,destination=(relativemovcorrection_0 + mydiffload_ref.center[0]))
	remove_ports_with_prefix(opamp,"load_pfet_right_")
	opamp.add_ports(load_pfet_right_ref.get_ports_list(),prefix="load_pfet_right_")
	opamp << c_route(pdk,opamp.ports["load_pfet_right_multiplier_0_gate_con_N"],opamp.ports["load_pfet_left_multiplier_0_gate_con_N"],**{'extension': 18, 'width1': 0.8, 'width2': 0.8})
	opamp << c_route(pdk,opamp.ports["load_pfet_right_multiplier_0_drain_con_N"],opamp.ports["load_pfet_left_multiplier_0_drain_con_N"],**{'extension': 8, 'width1': 0.8, 'width2': 0.8})
	opamp << c_route(pdk,opamp.ports["load_pfet_right_multiplier_0_source_con_N"],opamp.ports["load_pfet_left_multiplier_0_source_con_N"],**{'extension': 5.5, 'viaoffset': ( True , False ), 'fullbottom': True, 'width1': 0.8, 'width2': 0.8})
	# placing load_curr_source_ref centered at the origin
	load_curr_source_ref = nmos(pdk,**{'width': load_curr_source_width_ref, 'fingers': load_curr_source_fingers, 'multipliers': 2})
	load_curr_source_ref_ref = prec_ref_center(load_curr_source_ref)
	opamp.add(load_curr_source_ref_ref)
	opamp.add_ports(load_curr_source_ref_ref.get_ports_list(),prefix="load_curr_source_ref_")
	# move load_curr_source left mydiff
	relativemovcorrection_0 = -1*(maxmetalsep + center_to_edge_distance(mydiff_ref,1) + center_to_edge_distance(load_curr_source_ref,3))
	movex(load_curr_source_ref,destination=(relativemovcorrection_0 + mydiff_ref.center[0]))
	remove_ports_with_prefix(opamp,"load_curr_source_")
	opamp.add_ports(load_curr_source_ref.get_ports_list(),prefix="load_curr_source_")
	# move load_curr_source_ref south mydiff
	relativemovcorrection_0 = -1*(maxmetalsep + center_to_edge_distance(mydiff_ref,4) + center_to_edge_distance(load_curr_source_ref_ref,2))
	movey(load_curr_source_ref_ref,destination=(relativemovcorrection_0 + mydiff_ref.center[1]))
	remove_ports_with_prefix(opamp,"load_curr_source_ref_")
	opamp.add_ports(load_curr_source_ref_ref.get_ports_list(),prefix="load_curr_source_ref_")
	# move load_curr_source_ref left mycurrmirror
	relativemovcorrection_0 = -1*(maxmetalsep + center_to_edge_distance(mycurrmirror_ref,1) + center_to_edge_distance(load_curr_source_ref_ref,3))
	movex(load_curr_source_ref_ref,destination=(relativemovcorrection_0 + mycurrmirror_ref.center[0]))
	remove_ports_with_prefix(opamp,"load_curr_source_ref_")
	opamp.add_ports(load_curr_source_ref_ref.get_ports_list(),prefix="load_curr_source_ref_")
	# placing load_curr_source_mirr centered at the origin
	load_curr_source_mirr = nmos(pdk,**{'width': load_curr_source_width_mirr, 'fingers': load_curr_source_fingers, 'multipliers': 2})
	load_curr_source_mirr_ref = prec_ref_center(load_curr_source_mirr)
	opamp.add(load_curr_source_mirr_ref)
	opamp.add_ports(load_curr_source_mirr_ref.get_ports_list(),prefix="load_curr_source_mirr_")
	# move load_curr_source_mirr right mydiff
	relativemovcorrection_0 = 1*(maxmetalsep + center_to_edge_distance(mydiff_ref,3) + center_to_edge_distance(load_curr_source_mirr_ref,1))
	movex(load_curr_source_mirr_ref,destination=(relativemovcorrection_0 + mydiff_ref.center[0]))
	remove_ports_with_prefix(opamp,"load_curr_source_mirr_")
	opamp.add_ports(load_curr_source_mirr_ref.get_ports_list(),prefix="load_curr_source_mirr_")
	# move load_curr_source_mirr south mydiff
	relativemovcorrection_0 = -1*(maxmetalsep + center_to_edge_distance(mydiff_ref,4) + center_to_edge_distance(load_curr_source_mirr_ref,2))
	movey(load_curr_source_mirr_ref,destination=(relativemovcorrection_0 + mydiff_ref.center[1]))
	remove_ports_with_prefix(opamp,"load_curr_source_mirr_")
	opamp.add_ports(load_curr_source_mirr_ref.get_ports_list(),prefix="load_curr_source_mirr_")
	# move load_curr_source_mirr right mycurrmirror
	relativemovcorrection_0 = 1*(maxmetalsep + center_to_edge_distance(mycurrmirror_ref,3) + center_to_edge_distance(load_curr_source_mirr_ref,1))
	movex(load_curr_source_mirr_ref,destination=(relativemovcorrection_0 + mycurrmirror_ref.center[0]))
	remove_ports_with_prefix(opamp,"load_curr_source_mirr_")
	opamp.add_ports(load_curr_source_mirr_ref.get_ports_list(),prefix="load_curr_source_mirr_")
	opamp << c_route(pdk,opamp.ports["load_curr_source_ref_multiplier_0_gate_con_S"],opamp.ports["load_curr_source_mirr_multiplier_0_gate_con_S"],**{'extension': 3, 'width1': 0.8, 'width2': 0.8})
	opamp << c_route(pdk,opamp.ports["load_curr_source_ref_multiplier_0_drain_con_S"],opamp.ports["load_curr_source_mirr_multiplier_0_drain_con_S"],**{'extension': 12, 'viaoffset': ( False , True ), 'width1': 0.8, 'width2': 0.8})
	opamp << c_route(pdk,opamp.ports["load_curr_source_ref_multiplier_0_source_con_S"],opamp.ports["load_curr_source_mirr_multiplier_0_source_con_S"],**{'extension': 14, 'width1': 0.8, 'width2': 0.8})
	opamp << c_route(pdk,opamp.ports["load_curr_source_ref_multiplier_0_gate_E"],opamp.ports["load_curr_source_ref_multiplier_0_drain_E"],**{'extension': 3})
	opamp << L_route(pdk,opamp.ports["mydiff_tr_multiplier_0_drain_W"],opamp.ports["load_pfet_right_multiplier_0_gate_con_S"],**{})
	opamp << L_route(pdk,opamp.ports["load_pfet_right_multiplier_0_drain_con_S"],opamp.ports["load_curr_source_mirr_multiplier_0_drain_W"],**{})
	# placing load_miller_cap centered at the origin
	load_miller_cap = mimcap_array(pdk,**{'rows': mim_cap_rows, 'columns': 2, 'size': mim_cap_size})
	load_miller_cap_ref = prec_ref_center(load_miller_cap)
	opamp.add(load_miller_cap_ref)
	opamp.add_ports(load_miller_cap_ref.get_ports_list(),prefix="load_miller_cap_")
	# move load_miller_cap right mydiff
	relativemovcorrection_0 = 1*(maxmetalsep + center_to_edge_distance(mydiff_ref,3) + center_to_edge_distance(load_miller_cap_ref,1))
	movex(load_miller_cap_ref,destination=(relativemovcorrection_0 + mydiff_ref.center[0]))
	remove_ports_with_prefix(opamp,"load_miller_cap_")
	opamp.add_ports(load_miller_cap_ref.get_ports_list(),prefix="load_miller_cap_")
	# move load_miller_cap north mydiff
	relativemovcorrection_0 = 1*(maxmetalsep + center_to_edge_distance(mydiff_ref,2) + center_to_edge_distance(load_miller_cap_ref,4))
	movey(load_miller_cap_ref,destination=(relativemovcorrection_0 + mydiff_ref.center[1]))
	remove_ports_with_prefix(opamp,"load_miller_cap_")
	opamp.add_ports(load_miller_cap_ref.get_ports_list(),prefix="load_miller_cap_")
	# move load_miller_cap right load_pfet_right
	relativemovcorrection_0 = 1*(maxmetalsep + center_to_edge_distance(load_pfet_right_ref,3) + center_to_edge_distance(load_miller_cap_ref,1))
	movex(load_miller_cap_ref,destination=(relativemovcorrection_0 + load_pfet_right_ref.center[0]))
	remove_ports_with_prefix(opamp,"load_miller_cap_")
	opamp.add_ports(load_miller_cap_ref.get_ports_list(),prefix="load_miller_cap_")
	opamp << c_route(pdk,opamp.ports["mydiffload_top_B_0_drain_N"],opamp.ports["load_miller_cap_row0_col0_top_met_N"],**{'extension': 15})
	opamp << c_route(pdk,opamp.ports["load_pfet_right_multiplier_0_drain_con_S"],opamp.ports["load_miller_cap_row0_col0_top_met_S"],**{'width1': 1.2, 'width2': 1.2})
	return opamp
