import sys
sys.path.append('../../elementary/current_mirror/')
sys.path.append('../../composite/')

from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.flow.pdk.gf180_mapped import gf180_mapped_pdk as gf180

from glayout.flow.primitives.guardring import tapring
from glayout.flow.routing.smart_route import smart_route
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.primitives.via_gen import via_stack

from gdsfactory.cell import cell, clear_cache
from gdsfactory.component import Component, copy
from gdsfactory.component_reference import ComponentReference
from gdsfactory.components.rectangle import rectangle
from glayout.flow.pdk.mappedpdk import MappedPDK
from typing import Optional, Union
from pydantic import validate_arguments

from glayout.flow.placement.two_transistor_interdigitized import two_nfet_interdigitized, two_pfet_interdigitized

from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, prec_center, prec_array, movey, align_comp_to_port, prec_ref_center
from glayout.flow.pdk.util.port_utils import rename_ports_by_orientation, rename_ports_by_list, add_ports_perimeter, print_ports, set_port_orientation, rename_component_ports
#from glayout.flow.pdk.util.comp_utils import evaluate_bbox, prec_ref_center, movex, movey, to_decimal, to_float, move, align_comp_to_port, get_padding_points_cc
#from glayout.flow.pdk.util.port_utils import rename_ports_by_orientation, rename_ports_by_list, add_ports_perimeter, print_ports, set_port_orientation, rename_component_ports
from gdsfactory.components import text_freetype, rectangle
from gdsfactory import Component
from gdsfactory.routing.route_quad import route_quad
from glayout.flow.spice.netlist import Netlist
from typing import Optional, Union 



# @validate_arguments
def generate_current_mirror_netlist(
	pdk: MappedPDK,
	instance_name: str,
	CM_size: tuple[float, float, int],  # (width, length, multipliers)
	drain_net_ref: str,
	drain_net_copy: str,
	source_net_ref: str,
	source_net_copy: str,
	gate_net: str,
	transistor_type: str = "nfet",
	bulk_net: str = None,
	proposed_ground: str = None,  # Proposed ground net
	dummy: bool = True,
	subckt_only: bool = False,
	show_netlist: bool = False,
	**kwargs
	) -> Netlist:
	"""Generate a netlist for a current mirror."""

	if bulk_net is None:
		bulk_net = "VDD" if transistor_type.lower() == "pfet" else "VSS"

	width = CM_size[0]
	length = CM_size[1]
	multipliers = CM_size[2]  
	fingers =  CM_size[3] # Number of fingers of the interdigitized fets
	mtop = multipliers * fingers if subckt_only else 1
	#mtop = multipliers * 2 if dummy else multipliers # Double the multiplier to account for the dummies

	model_name = pdk.models[transistor_type.lower()]

	circuit_name = instance_name
	nodes = list(set([drain_net_ref, gate_net, drain_net_copy, source_net_ref,source_net_copy,bulk_net]))  # Take only unique NET names

	source_netlist = f".subckt {circuit_name} {' '.join(nodes)}\n"

	#source_netlist += f"V{proposed_ground}1 ({proposed_ground} {bulk_net}) 0\n" #Proposed ground connection

	# Generating only two transistors (one on each side):
	source_netlist += f"XA {drain_net_ref} {gate_net} {source_net_ref} {bulk_net} {model_name} l={length} w={width} m={mtop}\n"
	source_netlist += f"XB {drain_net_copy} {gate_net} {source_net_copy} {bulk_net} {model_name} l={length} w={width} m={mtop}\n"
	if dummy:
		source_netlist += f"XDUMMY {bulk_net} {bulk_net} {bulk_net} {bulk_net} {model_name} l={length} w={width} m={mtop}\n"
	source_netlist += ".ends " + circuit_name

	instance_format = "X{name} {nodes} {circuit_name} l={length} w={width} m={mult}"

	topnet=Netlist(
		circuit_name=circuit_name,
		nodes=nodes,
		source_netlist=source_netlist,
		instance_format=instance_format,
		parameters={
			"model": model_name,
			"width": width,
			"length": length,
			'mult': multipliers,},
		)
	if show_netlist:
		generated_netlist_for_lvs = topnet.generate_netlist()
		print(f"Generated netlist :\n", generated_netlist_for_lvs)

		file_path_local_storage = "./gen_netlist.txt"
		try:
			with open(file_path_local_storage, 'w') as file:
				file.write(generated_netlist_for_lvs)
		except:
			print(f"Verify the file availability and type: ", generated_netlist_for_lvs, type(generated_netlist_for_lvs))
	return topnet


# @validate_arguments
def current_mirror_base(
        pdk: MappedPDK,
        Width: float = 1,
        Length: Optional[float] = None,
        num_cols: int = 2,
        fingers: int = 1,
        type: Optional[str] = 'nfet',
        with_substrate_tap: Optional[bool] = False,
        with_tie: Optional[bool] = True,
        with_dummy: Optional[bool] = True,
        show_netlist: Optional[bool] = False,
        **kwargs
    ) -> Component:
    
    """An instantiable current mirror that returns a Component object. 
    The current mirror could be a two transistor interdigitized structure with a shorted source and gate.
    It can be instantiated with either nmos or pmos devices. It can also be instantiated with a dummy device, a substrate tap, and a tie layer, and is centered at the origin.
    Transistor A acts as the reference and Transistor B acts as the mirror fet
    This current mirror is used to generate a exact copy of the reference current.
    [TODO] Needs to be checked for both pfet and nfet configurations.
    [TODO] It will be updated with multi-leg or stackked length parametrization in future.
    [TODO] There will also be a Regulated Cascoded block added to it. 

	Args:
		pdk (MappedPDK): the process design kit to use
        Width (float): width of the interdigitized fets (same for both reference and mirror)
        Length (float): length of the interdigitized fets (same for both reference and mirror) 
        As Default, Set to None to use the minimum length of the technology
		numcols (int): number of columns of the interdigitized fets
        fingers: Number of fingers of interdigitized fets (same for both reference and mirror)
		device (str): nfet or pfet (can only interdigitize one at a time with this option)
		with_dummy (bool): True places dummies on either side of the interdigitized fets
		with_substrate_tap (bool): boolean to decide whether to place a substrate tapring
		with_tie (bool): boolean to decide whether to place a tapring for tielayer
		tie_layers (tuple[str,str], optional): the layers to use for the tie. Defaults to ("met2","met1").
		**kwargs: The keyword arguments are passed to the two_nfet_interdigitized or two_pfet_interdigitized functions and need to be valid arguments that can be accepted by the multiplier 
	Returns:
		Component: a current mirror component object
	"""
    pdk.activate()
    maxmet_sep = pdk.util_max_metal_seperation()
    psize=(0.35,0.35)
    # Create the current mirror component
    CurrentMirror = Component(name="CurrentMirror")
    Length = Length if Length is not None else pdk.get_grule('poly')['min_width']
    
    # Create the interdigitized fets
    if type.lower() =="pfet" or type.lower() =="pmos":
        currm= two_pfet_interdigitized(pdk,numcols=num_cols,width=Width,length=Length,fingers=fingers,
                                       dummy=with_dummy,with_substrate_tap=with_substrate_tap,with_tie=with_tie)
        well, sdglayer = "nwell", "p+s/d"
    elif type.lower() =="nfet" or type.lower() =="nmos":
        currm= two_nfet_interdigitized(pdk,numcols=num_cols,width=Width,length=Length,fingers=fingers,dummy=with_dummy,
                                       with_substrate_tap=with_substrate_tap,with_tie=with_tie)
        well, sdglayer = "pwell", "n+s/d"
    else:
        raise ValueError("type must be either nfet or pfet")
        
    # Add the interdigitized fets to the current mirror top component
    currm_ref = prec_ref_center(currm)
    CurrentMirror.add(currm_ref)
    CurrentMirror.add_ports(currm_ref.get_ports_list(),prefix="currm_")
    
    # for absc in CurrentMirror.ports.keys():
    #     if len(absc.split("_")) <= 5:
    #         if set(["currm","A","W"]).issubset(set(absc.split("_"))):
    #             print(absc+"\n")
    
    #Routing
    viam2m3 = via_stack(pdk, "met2", "met3", centered=True)
    drain_A_via  = CurrentMirror << viam2m3
    drain_A_via.move(CurrentMirror.ports["currm_A_0_drain_W"].center).movex(-1)
    source_A_via  = CurrentMirror << viam2m3
    source_A_via.move(CurrentMirror.ports[f"currm_A_{num_cols-1:d}_source_E"].center).movex(0.5*(num_cols))
    gate_A_via  = CurrentMirror << viam2m3
    gate_A_via.move(CurrentMirror.ports["currm_A_0_gate_W"].center).movex(-1-2*Length)
    
    drain_B_via  = CurrentMirror << viam2m3
    drain_B_via.move(drain_A_via.center).movex(-1+Length).movey(+1+maxmet_sep-Length)
    source_B_via  = CurrentMirror << viam2m3
    source_B_via.move(source_A_via.center).movey(1+maxmet_sep-Length)
    gate_B_via  = CurrentMirror << viam2m3
    gate_B_via.move(gate_A_via.center).movey(-1-maxmet_sep+Length)
    #####################
    CurrentMirror << straight_route(pdk,currm_ref.ports["A_0_drain_E"], drain_A_via.ports["bottom_met_W"])
    CurrentMirror << straight_route(pdk,currm_ref.ports["B_0_drain_E"], drain_B_via.ports["bottom_met_W"])
    ##################### 
    CurrentMirror << straight_route(pdk,currm_ref.ports["A_0_source_E"], source_A_via.ports["bottom_met_W"])
    CurrentMirror << straight_route(pdk,currm_ref.ports["B_0_source_E"], source_B_via.ports["bottom_met_W"])
    
    source_short =  CurrentMirror << straight_route(pdk, source_A_via.ports["top_met_N"], source_B_via.ports["top_met_S"])
    #,extension=1.2*max(Width,Width), width1=psize[0], width2=ps, cwidth=0.32, e1glayer="met3", e2glayer="met3", cglayer="met2")
    #####################
    CurrentMirror << straight_route(pdk,currm_ref.ports["A_0_gate_W"], gate_A_via.ports["bottom_met_W"])
    CurrentMirror << straight_route(pdk,currm_ref.ports["B_0_gate_W"], gate_B_via.ports["bottom_met_W"])
    #####################
    gate_short =  CurrentMirror << straight_route(pdk, gate_A_via.ports["top_met_S"], gate_B_via.ports["top_met_N"])

    # #connecting the Drian of A to gate short
    CurrentMirror << straight_route(pdk,drain_A_via.ports["top_met_S"],gate_short.ports["route_N"])
   
	# # Connecting dummies to the welltie
    # if with_dummy:
    #     try:
    #         CurrentMirror << straight_route(pdk, CurrentMirror.ports["A_0_dummy_L_gsdcon_top_met_W"],CurrentMirror.ports["welltie_W_top_met_W"],glayer2="met1")
    #     except KeyError:
    #         pass
    #     try:
    #         end_col = num_cols - 1
    #         port1 = f'B_{end_col}_dummy_R_gdscon_top_met_E'
    #         CurrentMirror << straight_route(pdk, CurrentMirror.ports[port1], CurrentMirror.ports["welltie_E_top_met_E"], glayer2="met1")
    #     except KeyError:
    #         pass
    
    # # add well
    # CurrentMirror.add_padding(default=pdk.get_grule(well, "active_tap")["min_enclosure"],layers=[pdk.get_glayer(well)])
    # CurrentMirror = add_ports_perimeter(CurrentMirror, layer = pdk.get_glayer(well), prefix="well_")
    #if well == "nwell": 
    #    CurrentMirror.add_padding(layers=(pdk.get_glayer("nwell"),),default= 1 )
    
    
    #Connecting the source of the fets to the bulk ???
    src2bulk=CurrentMirror << straight_route(pdk, source_short.ports["route_N"],CurrentMirror.ports["currm_welltie_N_top_met_E"], glayer2="met2")
    
    ##The default naming scheme of ports in GDSFactory
    ##e1=West, e2=North, e3=East, e4=South. The default naming scheme of ports in GDSFactory

    ###########################################################
    Irefpin = CurrentMirror << rectangle(size=psize,layer=pdk.get_glayer("met3"),centered=True)
    Irefpin.move(drain_A_via.center).movey(0.2*evaluate_bbox(currm_ref)[0])
    CurrentMirror << straight_route(pdk, drain_A_via.ports["top_met_N"],Irefpin.ports["e4"], glayer2="met3")
    
    Icopypin = CurrentMirror << rectangle(size=psize,layer=pdk.get_glayer("met3"),centered=True)
    Icopypin.move(drain_A_via.center).movex(-1+Length).movey(0.2*evaluate_bbox(currm_ref)[0])
    CurrentMirror << straight_route(pdk, drain_B_via.ports["top_met_N"],Icopypin.ports["e4"], glayer2="met3")
    
    bulkpin = CurrentMirror << rectangle(size=psize,layer=pdk.get_glayer("met3"),centered=True)
    bulkpin.move(source_A_via.center).movey(0.2*evaluate_bbox(currm_ref)[0])
    CurrentMirror << straight_route(pdk, src2bulk["route_N"],bulkpin.ports["e4"], glayer2="met3")
    ###########################################################
    
    CurrentMirror.add_ports(drain_A_via.get_ports_list(), prefix="A_drain_")
    CurrentMirror.add_ports(drain_B_via.get_ports_list(), prefix="B_drain_")
    CurrentMirror.add_ports(gate_short.get_ports_list(), prefix="gateshortports_")
    CurrentMirror.add_ports(source_short.get_ports_list(), prefix="sourceshortports_")
    CurrentMirror.add_ports(src2bulk.get_ports_list(), prefix="purposegndport_")
    CurrentMirror.add_ports(Irefpin.get_ports_list(), prefix="refport_")
    CurrentMirror.add_ports(Icopypin.get_ports_list(), prefix="copyport_")
    CurrentMirror.add_ports(bulkpin.get_ports_list(), prefix="bulkport_")

    CurrentMirror = component_snap_to_grid(rename_ports_by_orientation(CurrentMirror))

    CurrentMirror.info["netlist"] = generate_current_mirror_netlist(
                                    pdk=pdk,
                                    instance_name=CurrentMirror.name,
                                    CM_size= (Width, Length, num_cols,fingers),  # (width, length, multipliers, fingers)
                                    transistor_type=type,
                                    drain_net_ref="IREF",  # Input drain connected to IREF
                                    drain_net_copy="ICOPY", # Output drain connected to ICOPY
                                    gate_net="IREF",      # Gate connected to VREF 
                                    source_net_ref="VSS" if type=="nfet" else "VDD",    # Source connected to VSS
                                    source_net_copy="VSS" if type=="nfet" else "VDD",    # Source connected to VSS
                                    bulk_net= "VSS" if type=="nfet" else "VDD", #Proposed ground should also change
                                    subckt_only=True,
                                    show_netlist=show_netlist,
                                    )

    return CurrentMirror


def sky130_add_current_mirror_labels(
    CMS: Component, 
    transistor_type: str = "nfet",
    pdk: MappedPDK =sky130
    ) -> Component:  
    """Add labels to the current mirror layout for LVS, handling both nfet and pfet."""

    #Would be adjusted for pdk agonastic later
    met2_pin = (69, 16)
    met2_label = (69, 5)
    met3_pin = (70, 16)
    met3_label = (70, 5)
    
    CMS.unlock()
    move_info = []
    psize=(0.35,0.35)
    
    
    Iref_label = rectangle(layer=met2_pin, size=psize, centered=True).copy()
    Iref_label.add_label(text="IREF", layer=met2_label)
    move_info.append((Iref_label, CMS.ports["refport_N"], None)) 
    
    Icopy_label = rectangle(layer=met2_pin, size=psize, centered=True).copy()
    Icopy_label.add_label(text="ICOPY", layer=met2_label)
    move_info.append((Icopy_label, CMS.ports["copyport_N"], None))
    
   # VSS/VDD label (for sources/bulk connection)
    if transistor_type.lower() == "nfet":
        bulk_net_name = "VSS"
    else:  # pfet
        bulk_net_name = "VDD"
        
    bulk_label = rectangle(layer=met2_pin, size=psize, centered=True).copy()
    bulk_label.add_label(text=bulk_net_name, layer=met2_label)
    move_info.append((bulk_label, CMS.ports["bulkport_N"], None))

    # Add labels to the component
    for label, port, alignment in move_info:
        if port:
            alignment = ('c', 'b') if alignment is None else alignment
            aligned_label = align_comp_to_port(label, port, alignment=alignment)
            CMS.add(aligned_label)

    return CMS.flatten()


## To Test their primitives
# from current_mirror import current_mirror, current_mirror_netlist

if __name__ == "__main__":
	comp = current_mirror_base(sky130, num_cols=4, Width=3, device='nfet',show_netlist=False)
	# comp.pprint_ports()
	comp = sky130_add_current_mirror_labels(comp, transistor_type='nfet', pdk=sky130)


	# # # Write the current mirror layout to a GDS file
	comp.name = "CM"
	# # delete_files_in_directory("GDS/")
	# # tmpdirname = Path("GDS/").resolve()
	# # delete_files_in_directory("GDS/")
	# # tmp_gds_path = Path(comp.write_gds(gdsdir=tmpdirname)).resolve()
	# comp.write_gds("./CM.gds")
	comp.show()
	# #Generate the netlist for the current mirror
	# print("\n...Generating Netlist...")
	# print(comp.info["netlist"].generate_netlist())
	# # # DRC Checks
	# # #delete_files_in_directory("DRC/")
	print("\n...Running DRC...")
	drc_result = sky130.drc_magic(comp, "CM")
	# #drc_result = sky130.drc_magic(comp, "CM",output_file="DRC/")
	# print(drc_result['result_str'])
	# # # LVS Checks
	# # #delete_files_in_directory("LVS/")
	print("\n...Running LVS...")
	netgen_lvs_result = sky130.lvs_netgen(comp, "CM")  
	# # #netgen_lvs_result = sky130.lvs_netgen(comp, "CM",output_file_path="LVS/")        
	# # # print(netgen_lvs_result['result_str'])

