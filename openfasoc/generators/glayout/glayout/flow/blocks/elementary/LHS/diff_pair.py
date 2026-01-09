from typing import Optional, Union

from gdsfactory.cell import cell
from gdsfactory.component import Component, copy
from gdsfactory.components.rectangle import rectangle
from gdsfactory.routing.route_quad import route_quad
from gdsfactory.routing.route_sharp import route_sharp
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.util.comp_utils import align_comp_to_port, evaluate_bbox, movex, movey
from glayout.flow.pdk.util.port_utils import (
    add_ports_perimeter,
    get_orientation,
    print_ports,
    rename_ports_by_list,
    rename_ports_by_orientation,
    set_port_orientation,
)
from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid
from glayout.flow.placement.common_centroid_ab_ba import common_centroid_ab_ba
from glayout.flow.primitives.fet import nmos, pmos
from glayout.flow.primitives.guardring import tapring
from glayout.flow.primitives.via_gen import via_stack
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.smart_route import smart_route
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.spice import Netlist
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
from gdsfactory.components import text_freetype
try:
    from evaluator_wrapper import run_evaluation
except ImportError:
    print("Warning: evaluator_wrapper not found. Evaluation will be skipped.")
    run_evaluation = None
import json

def add_df_labels(df_in: Component,
                        pdk: MappedPDK
                         ) -> Component:
	
	df_in.unlock()
	met1_pin = (67,16)
	met1_label = (67,5)
	met2_pin = (68,16)
	met2_label = (68,5)
    # list that will contain all port/comp info
	move_info = list()
    # create labels and append to info list
    # vtail
	vtaillabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.27,0.27),centered=True).copy()
	vtaillabel.add_label(text="VTAIL",layer=pdk.get_glayer("met2_label"))
	move_info.append((vtaillabel,df_in.ports["bl_multiplier_0_source_S"],None))
    
    # vdd1
	vdd1label = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.27,0.27),centered=True).copy()
	vdd1label.add_label(text="VDD1",layer=pdk.get_glayer("met2_label"))
	move_info.append((vdd1label,df_in.ports["tl_multiplier_0_drain_N"],None))
    
    # vdd2
	vdd2label = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.27,0.27),centered=True).copy()
	vdd2label.add_label(text="VDD2",layer=pdk.get_glayer("met2_label"))
	move_info.append((vdd2label,df_in.ports["tr_multiplier_0_drain_N"],None))
    
    # VB
	vblabel = rectangle(layer=pdk.get_glayer("met1_pin"),size=(0.5,0.5),centered=True).copy()
	vblabel.add_label(text="B",layer=pdk.get_glayer("met1_label"))
	move_info.append((vblabel,df_in.ports["tap_N_top_met_S"], None))
    
    # VP
	vplabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.27,0.27),centered=True).copy()
	vplabel.add_label(text="VP",layer=pdk.get_glayer("met2_label"))
	move_info.append((vplabel,df_in.ports["br_multiplier_0_gate_S"], None))
    
    # VN
	vnlabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.27,0.27),centered=True).copy()
	vnlabel.add_label(text="VN",layer=pdk.get_glayer("met2_label"))
	move_info.append((vnlabel,df_in.ports["bl_multiplier_0_gate_S"], None))

    # move everything to position
	for comp, prt, alignment in move_info:
		alignment = ('c','b') if alignment is None else alignment
		compref = align_comp_to_port(comp, prt, alignment=alignment)
		df_in.add(compref)
	return df_in.flatten() 

def diff_pair_netlist(fetL: Component, fetR: Component) -> Netlist:
	"""Create netlist for differential pair with robust error handling"""
	diff_pair_netlist_obj = Netlist(circuit_name='DIFF_PAIR', nodes=['VP', 'VN', 'VDD1', 'VDD2', 'VTAIL', 'B'])
	
	def reconstruct_netlist_from_component(component, comp_name):
		"""Helper to safely extract and reconstruct netlist from component"""
		try:
			# Try to get the netlist from info
			netlist = component.info.get('netlist', None)
			
			# If netlist is already a Netlist object, return it
			if isinstance(netlist, Netlist):
				return netlist
			
			# If netlist is a string, we need to reconstruct
			if isinstance(netlist, str):
				# Try to get netlist_data_json (this is what fet.py stores)
				netlist_data_json = component.info.get('netlist_data_json', None)
				
				if netlist_data_json:
					try:
						data = json.loads(netlist_data_json)
						reconstructed = Netlist(
							circuit_name=data.get('circuit_name', 'unknown'),
							nodes=data.get('nodes', ['D', 'G', 'S', 'B'])
						)
						reconstructed.source_netlist = data.get('source_netlist', '')
						if 'parameters' in data:
							reconstructed.parameters = data['parameters']
						return reconstructed
					except (json.JSONDecodeError, KeyError) as e:
						print(f"Debug: JSON decode failed for {comp_name}: {e}")
				
				# Try netlist_data dict
				netlist_data = component.info.get('netlist_data', None)
				if netlist_data and isinstance(netlist_data, dict):
					try:
						reconstructed = Netlist(
							circuit_name=netlist_data.get('circuit_name', 'unknown'),
							nodes=netlist_data.get('nodes', ['D', 'G', 'S', 'B'])
						)
						reconstructed.source_netlist = netlist_data.get('source_netlist', '')
						if 'parameters' in netlist_data:
							reconstructed.parameters = netlist_data['parameters']
						return reconstructed
					except (KeyError, TypeError) as e:
						print(f"Debug: netlist_data parse failed for {comp_name}: {e}")
				
				# If we get here, we couldn't reconstruct
				print(f"Debug: Could not find netlist_data_json or netlist_data for {comp_name}")
				print(f"Debug: component.info type: {type(component.info)}")
				# Try to safely print available keys
				try:
					if hasattr(component.info, '__dict__'):
						print(f"Debug: Info attributes: {list(component.info.__dict__.keys())}")
					elif hasattr(component.info, 'keys'):
						print(f"Debug: Info keys: {list(component.info.keys())}")
				except:
					print(f"Debug: Could not inspect Info object")
				
				raise ValueError(f"No netlist_data found for string netlist in {comp_name} component")
			
			# If netlist is None or something else
			print(f"Debug: Unexpected netlist type for {comp_name}: {type(netlist)}")
			raise ValueError(f"Invalid netlist for {comp_name}")
			
		except Exception as e:
			print(f"Error reconstructing netlist for {comp_name}: {e}")
			raise
	
	# Reconstruct netlists for both FETs
	fetL_netlist = reconstruct_netlist_from_component(fetL, "fetL")
	fetR_netlist = reconstruct_netlist_from_component(fetR, "fetR")
	
	# Connect the netlists
	diff_pair_netlist_obj.connect_netlist(
		fetL_netlist,
		[('D', 'VDD1'), ('G', 'VP'), ('S', 'VTAIL'), ('B', 'B')]
	)
	diff_pair_netlist_obj.connect_netlist(
		fetR_netlist,
		[('D', 'VDD2'), ('G', 'VN'), ('S', 'VTAIL'), ('B', 'B')]
	)
	
	return diff_pair_netlist_obj

@cell
def diff_pair(
	pdk: MappedPDK,
	width: float = 3,
	fingers: int = 4,
	length: Optional[float] = None,
	n_or_p_fet: bool = True,
	plus_minus_seperation: float = 0,
	rmult: int = 1,
	dummy: Union[bool, tuple[bool, bool]] = True,
	substrate_tap: bool=True
) -> Component:
	"""create a diffpair with 2 transistors placed in two rows with common centroid place. Sources are shorted
	width = width of the transistors
	fingers = number of fingers in the transistors (must be 2 or more)
	length = length of the transistors, None or 0 means use min length
	short_source = if true connects source of both transistors
	n_or_p_fet = if true the diffpair is made of nfets else it is made of pfets
	substrate_tap: if true place a tapring around the diffpair (connects on met1)
	"""
	# TODO: error checking
	pdk.activate()
	diffpair = Component()
	# create transistors
	well = None
	if isinstance(dummy, bool):
		dummy = (dummy, dummy)
	if n_or_p_fet:
		fetL = nmos(pdk, width=width, fingers=fingers,length=length,multipliers=1,with_tie=False,with_dummy=(dummy[0], False),with_dnwell=False,with_substrate_tap=False,rmult=rmult)
		fetR = nmos(pdk, width=width, fingers=fingers,length=length,multipliers=1,with_tie=False,with_dummy=(False,dummy[1]),with_dnwell=False,with_substrate_tap=False,rmult=rmult)
		min_spacing_x = pdk.get_grule("n+s/d")["min_separation"] - 2*(fetL.xmax - fetL.ports["multiplier_0_plusdoped_E"].center[0])
		well = "pwell"
	else:
		fetL = pmos(pdk, width=width, fingers=fingers,length=length,multipliers=1,with_tie=False,with_dummy=(dummy[0], False),dnwell=False,with_substrate_tap=False,rmult=rmult)
		fetR = pmos(pdk, width=width, fingers=fingers,length=length,multipliers=1,with_tie=False,with_dummy=(False,dummy[1]),dnwell=False,with_substrate_tap=False,rmult=rmult)
		min_spacing_x = pdk.get_grule("p+s/d")["min_separation"] - 2*(fetL.xmax - fetL.ports["multiplier_0_plusdoped_E"].center[0])
		well = "nwell"

	# CRITICAL FIX: Generate the netlist BEFORE adding components as references
	# This ensures we have access to the original component's info dict
	try:
		diff_pair_netlist_obj = diff_pair_netlist(fetL, fetR)
		print(f"✓ Successfully generated diff_pair netlist")
	except Exception as e:
		import traceback
		print(f"⚠ Warning: Failed to generate diff_pair netlist")
		print(f"  Error: {e}")
		traceback.print_exc()
		
		# Try to safely inspect info without using .keys()
		try:
			if hasattr(fetL.info, '__dict__'):
				print(f"  fetL.info attributes: {list(fetL.info.__dict__.keys())}")
			netlist_data_json = fetL.info.get('netlist_data_json', None)
			if netlist_data_json:
				print(f"  fetL has netlist_data_json (first 100 chars): {netlist_data_json[:100]}")
		except Exception as debug_e:
			print(f"  Could not inspect fetL.info: {debug_e}")
		
		# Create a dummy netlist as fallback
		diff_pair_netlist_obj = Netlist(circuit_name='DIFF_PAIR', nodes=['VP', 'VN', 'VDD1', 'VDD2', 'VTAIL', 'B'])
		print(f"  Created fallback netlist")

	# place transistors
	viam2m3 = via_stack(pdk,"met2","met3",centered=True)
	metal_min_dim = max(pdk.get_grule("met2")["min_width"],pdk.get_grule("met3")["min_width"])
	metal_space = max(pdk.get_grule("met2")["min_separation"],pdk.get_grule("met3")["min_separation"],metal_min_dim)
	gate_route_os = evaluate_bbox(viam2m3)[0] - fetL.ports["multiplier_0_gate_W"].width + metal_space
	min_spacing_y = metal_space + 2*gate_route_os
	min_spacing_y = min_spacing_y - 2*abs(fetL.ports["well_S"].center[1] - fetL.ports["multiplier_0_gate_S"].center[1])
	# TODO: fix spacing where you see +-0.5
	a_topl = (diffpair << fetL).movey(fetL.ymax+min_spacing_y/2+0.5).movex(0-fetL.xmax-min_spacing_x/2)
	b_topr = (diffpair << fetR).movey(fetR.ymax+min_spacing_y/2+0.5).movex(fetL.xmax+min_spacing_x/2)
	a_botr = (diffpair << fetR)
	a_botr.mirror_y()
	a_botr.movey(0-0.5-fetL.ymax-min_spacing_y/2).movex(fetL.xmax+min_spacing_x/2)
	b_botl = (diffpair << fetL)
	b_botl.mirror_y()
	b_botl.movey(0-0.5-fetR.ymax-min_spacing_y/2).movex(0-fetL.xmax-min_spacing_x/2)
	# if substrate tap place substrate tap
	if substrate_tap:
		tapref = diffpair << tapring(pdk,evaluate_bbox(diffpair,padding=1),horizontal_glayer="met1")
		diffpair.add_ports(tapref.get_ports_list(),prefix="tap_")
		try:
			diffpair<<straight_route(pdk,a_topl.ports["multiplier_0_dummy_L_gsdcon_top_met_W"],diffpair.ports["tap_W_top_met_W"],glayer2="met1")
		except KeyError:
			pass
		try:
			diffpair<<straight_route(pdk,b_topr.ports["multiplier_0_dummy_R_gsdcon_top_met_W"],diffpair.ports["tap_E_top_met_E"],glayer2="met1")
		except KeyError:
			pass
		try:
			diffpair<<straight_route(pdk,b_botl.ports["multiplier_0_dummy_L_gsdcon_top_met_W"],diffpair.ports["tap_W_top_met_W"],glayer2="met1")
		except KeyError:
			pass
		try:
			diffpair<<straight_route(pdk,a_botr.ports["multiplier_0_dummy_R_gsdcon_top_met_W"],diffpair.ports["tap_E_top_met_E"],glayer2="met1")
		except KeyError:
			pass
	# route sources (short sources)
	diffpair << route_quad(a_topl.ports["multiplier_0_source_E"], b_topr.ports["multiplier_0_source_W"], layer=pdk.get_glayer("met2"))
	diffpair << route_quad(b_botl.ports["multiplier_0_source_E"], a_botr.ports["multiplier_0_source_W"], layer=pdk.get_glayer("met2"))
	sextension = b_topr.ports["well_E"].center[0] - b_topr.ports["multiplier_0_source_E"].center[0]
	source_routeE = diffpair << c_route(pdk, b_topr.ports["multiplier_0_source_E"], a_botr.ports["multiplier_0_source_E"],extension=sextension, viaoffset=False)
	source_routeW = diffpair << c_route(pdk, a_topl.ports["multiplier_0_source_W"], b_botl.ports["multiplier_0_source_W"],extension=sextension, viaoffset=False)
	# route drains
	# place via at the drain
	drain_br_via = diffpair << viam2m3
	drain_bl_via = diffpair << viam2m3
	drain_br_via.move(a_botr.ports["multiplier_0_drain_N"].center).movey(viam2m3.ymin)
	drain_bl_via.move(b_botl.ports["multiplier_0_drain_N"].center).movey(viam2m3.ymin)
	drain_br_viatm = diffpair << viam2m3
	drain_bl_viatm = diffpair << viam2m3
	drain_br_viatm.move(a_botr.ports["multiplier_0_drain_N"].center).movey(viam2m3.ymin)
	drain_bl_viatm.move(b_botl.ports["multiplier_0_drain_N"].center).movey(-1.5 * evaluate_bbox(viam2m3)[1] - metal_space)
	# create route to drain via
	width_drain_route = b_topr.ports["multiplier_0_drain_E"].width
	dextension = source_routeE.xmax - b_topr.ports["multiplier_0_drain_E"].center[0] + metal_space
	bottom_extension = viam2m3.ymax + width_drain_route/2 + 2*metal_space
	drain_br_viatm.movey(0-bottom_extension - metal_space - width_drain_route/2 - viam2m3.ymax)
	diffpair << route_quad(drain_br_viatm.ports["top_met_N"], drain_br_via.ports["top_met_S"], layer=pdk.get_glayer("met3"))
	diffpair << route_quad(drain_bl_viatm.ports["top_met_N"], drain_bl_via.ports["top_met_S"], layer=pdk.get_glayer("met3"))
	floating_port_drain_bottom_L = set_port_orientation(movey(drain_bl_via.ports["bottom_met_W"],0-bottom_extension), get_orientation("E"))
	floating_port_drain_bottom_R = set_port_orientation(movey(drain_br_via.ports["bottom_met_E"],0-bottom_extension - metal_space - width_drain_route), get_orientation("W"))
	drain_routeTR_BL = diffpair << c_route(pdk, floating_port_drain_bottom_L, b_topr.ports["multiplier_0_drain_E"],extension=dextension, width1=width_drain_route,width2=width_drain_route)
	drain_routeTL_BR = diffpair << c_route(pdk, floating_port_drain_bottom_R, a_topl.ports["multiplier_0_drain_W"],extension=dextension, width1=width_drain_route,width2=width_drain_route)
	# cross gate route top with c_route. bar_minus ABOVE bar_plus
	get_left_extension = lambda bar, a_topl=a_topl, diffpair=diffpair, pdk=pdk : (abs(diffpair.xmin-min(a_topl.ports["multiplier_0_gate_W"].center[0],bar.ports["e1"].center[0])) + pdk.get_grule("met2")["min_separation"])
	get_right_extension = lambda bar, b_topr=b_topr, diffpair=diffpair, pdk=pdk : (abs(diffpair.xmax-max(b_topr.ports["multiplier_0_gate_E"].center[0],bar.ports["e3"].center[0])) + pdk.get_grule("met2")["min_separation"])
	# lay bar plus and PLUSgate_routeW
	bar_comp = rectangle(centered=True,size=(abs(b_topr.xmax-a_topl.xmin), b_topr.ports["multiplier_0_gate_E"].width),layer=pdk.get_glayer("met2"))
	bar_plus = (diffpair << bar_comp).movey(diffpair.ymax + bar_comp.ymax + pdk.get_grule("met2")["min_separation"])
	PLUSgate_routeW = diffpair << c_route(pdk, a_topl.ports["multiplier_0_gate_W"], bar_plus.ports["e1"], extension=get_left_extension(bar_plus))
	# lay bar minus and MINUSgate_routeE
	plus_minus_seperation = max(pdk.get_grule("met2")["min_separation"], plus_minus_seperation)
	bar_minus = (diffpair << bar_comp).movey(diffpair.ymax +bar_comp.ymax + plus_minus_seperation)
	MINUSgate_routeE = diffpair << c_route(pdk, b_topr.ports["multiplier_0_gate_E"], bar_minus.ports["e3"], extension=get_right_extension(bar_minus))
	# lay MINUSgate_routeW and PLUSgate_routeE
	MINUSgate_routeW = diffpair << c_route(pdk, set_port_orientation(b_botl.ports["multiplier_0_gate_E"],"W"), bar_minus.ports["e1"], extension=get_left_extension(bar_minus))
	PLUSgate_routeE = diffpair << c_route(pdk, set_port_orientation(a_botr.ports["multiplier_0_gate_W"],"E"), bar_plus.ports["e3"], extension=get_right_extension(bar_plus))
	# correct pwell place, add ports, flatten, and return
	diffpair.add_ports(a_topl.get_ports_list(),prefix="tl_")
	diffpair.add_ports(b_topr.get_ports_list(),prefix="tr_")
	diffpair.add_ports(b_botl.get_ports_list(),prefix="bl_")
	diffpair.add_ports(a_botr.get_ports_list(),prefix="br_")
	diffpair.add_ports(source_routeE.get_ports_list(),prefix="source_routeE_")
	diffpair.add_ports(source_routeW.get_ports_list(),prefix="source_routeW_")
	diffpair.add_ports(drain_routeTR_BL.get_ports_list(),prefix="drain_routeTR_BL_")
	diffpair.add_ports(drain_routeTL_BR.get_ports_list(),prefix="drain_routeTL_BR_")
	diffpair.add_ports(MINUSgate_routeW.get_ports_list(),prefix="MINUSgateroute_W_")
	diffpair.add_ports(MINUSgate_routeE.get_ports_list(),prefix="MINUSgateroute_E_")
	diffpair.add_ports(PLUSgate_routeW.get_ports_list(),prefix="PLUSgateroute_W_")
	diffpair.add_ports(PLUSgate_routeE.get_ports_list(),prefix="PLUSgateroute_E_")
	diffpair.add_padding(layers=(pdk.get_glayer(well),), default=0)

	component = component_snap_to_grid(rename_ports_by_orientation(diffpair))

	# Generate the diff_pair netlist
	#diff_pair_netlist_obj = diff_pair_netlist(fetL, fetR)

	# Store as string (same pattern as fet.py)
	component.info['netlist'] = diff_pair_netlist_obj.generate_netlist()

	# Optionally store netlist_data as JSON for reconstruction
	component.info['netlist_data_json'] = json.dumps({
		'circuit_name': diff_pair_netlist_obj.circuit_name,
		'nodes': diff_pair_netlist_obj.nodes,
		'source_netlist': diff_pair_netlist_obj.source_netlist,
		'parameters': diff_pair_netlist_obj.parameters if hasattr(diff_pair_netlist_obj, 'parameters') else {}
	})

	return component



@cell
def diff_pair_generic(
	pdk: MappedPDK,
	width: float = 3,
	fingers: int = 4,
	length: Optional[float] = None,
	n_or_p_fet: bool = True,
	plus_minus_seperation: float = 0,
	rmult: int = 1,
	dummy: Union[bool, tuple[bool, bool]] = True,
	substrate_tap: bool=True
) -> Component:
	diffpair = common_centroid_ab_ba(pdk,width,fingers,length,n_or_p_fet,rmult,dummy,substrate_tap)
	diffpair << smart_route(pdk,diffpair.ports["A_source_E"],diffpair.ports["B_source_E"],diffpair, diffpair)
	return diffpair

if __name__=="__main__":
	diff_pair = add_df_labels(diff_pair(sky130_mapped_pdk),sky130_mapped_pdk)
	#diff_pair = diff_pair(sky130_mapped_pdk)
	#diff_pair.show()
	diff_pair.name = "DIFF_PAIR"
	# magic_drc_result = sky130_mapped_pdk.drc_magic(diff_pair, diff_pair.name)
	# netgen_lvs_result = sky130_mapped_pdk.lvs_netgen(diff_pair, diff_pair.name)
	diff_pair_gds = diff_pair.write_gds("diff_pair.gds")
	res = run_evaluation("diff_pair.gds", diff_pair.name, diff_pair)