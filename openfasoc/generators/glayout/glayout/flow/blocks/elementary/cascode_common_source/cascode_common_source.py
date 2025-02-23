import sys
from os import path, rename, environ, listdir, remove

# environ['OPENBLAS_NUM_THREADS'] = '1'
from pathlib import Path

from gdsfactory.components import text_freetype, rectangle
from gdsfactory import Component
from gdsfactory.routing.route_quad import route_quad
from glayout.flow.spice.netlist import Netlist
from typing import Optional, Union 


from glayout.flow.placement.two_transistor_interdigitized import two_nfet_interdigitized, two_pfet_interdigitized
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.smart_route import smart_route
from glayout.flow.spice.netlist import Netlist
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.flow.primitives.fet import nmos, pmos
from glayout.flow.primitives.fet import fet_netlist
from glayout.flow.primitives.guardring import tapring
from glayout.flow.pdk.util.port_utils import add_ports_perimeter	
from gdsfactory.component import Component
from typing import Optional, Union 
from gdsfactory.components import text_freetype, rectangle

from glayout.flow.pdk.util.comp_utils import prec_ref_center, prec_center, movey, evaluate_bbox, align_comp_to_port

from glayout.flow.primitives.via_gen import via_array

# from glayout.flow.spice.netlist import connect_node
# from glayout.flow.primitives.fet import fet_netlist

# Netlist for LVS and SPICE simulations
def cascode_common_source_netlist_works(
	pdk: MappedPDK, 
	m1_width: float,
	m2_width: float,
	m1_length: float,
	m2_length: float,
	multipliers: int, 
	n_or_p_fet: Optional[str] = 'nfet',
	subckt_only: Optional[bool] = False,
	m1_fingers = int,
	m2_fingers = int,
	m1_multipliers = int,
	m2_multipliers = int
) -> Netlist:
	if m1_length is None:
		m1_length = pdk.get_grule('poly')['min_length']
	if m1_width is None:
		m1_width = pdk.get_grule('poly')['min_width']
	m2_length = m2_length or pdk.get_grule('poly')['min_length']
	m2_width = m2_width or pdk.get_grule('poly')['min_width']

	mtop = multipliers if subckt_only else 1
	model = pdk.models[n_or_p_fet]
	m1_multipliers = m1_multipliers or 1
	m2_multipliers = m2_multipliers or 1
	dmtop = m1_fingers*m1_multipliers
	num_dummies = 4
	
	circuit_name='CASCODECOMMONSRC'
	nodes=['VIN', 'VBIAS', 'VSS', 'IOUT', "INT"]
	model= model
	m1_width= m1_width
	m2_width= m2_width
	m1_length= m1_length
	m2_length= m2_length
	mult= m1_multipliers*m1_fingers
	m1_multipliers= m1_multipliers
	m2_multipliers= m2_multipliers

	source_netlist = f".subckt {circuit_name} {' '.join(nodes)}\n" 
	# M1 and M2 transistor NETLIST
	source_netlist += f"XM1 INT VIN VSS VSS {model} l={m1_length} w={m1_width} m={mult}\n"
	source_netlist += f"XM2 IOUT VBIAS INT VSS {model} l={m2_length} w={m2_width} m={mult}"
	#Adding the dummies
	# for i in range(num_dummies):
	# 	source_netlist += """ \nXDUMMY"""+f'{i+1}'+""" VSS VSS VSS VSS {model} """+f'l={m1_length} w={m1_width} m={1} dm={dmtop}'

	source_netlist += "\n.ends {circuit_name}"

	instance_format = "X{name} {nodes} {circuit_name} l={length} w={width} m={mult}"
 
	return Netlist(
		circuit_name='CASCODECOMMONSRC',
		nodes=['VIN', 'VBIAS', 'VSS', 'IOUT', "INT"], 
		source_netlist=source_netlist,
  		instance_format=instance_format,
		parameters={
			'model': model,
			'm1_width': m1_width,
			'm2_width': m2_width,
   			'm1_length': m1_length,	
			'm2_length': m2_length,	
			'mult': m1_multipliers*m1_fingers,#multipliers,
			'm1_multipliers': m1_multipliers,
			'm2_multipliers': m2_multipliers,
   		}
	)

def cascode_common_source_netlist(
	pdk: MappedPDK,  
	fetM1: Component,
	fetM2: Component,
	n_or_p_fet: Optional[str] = 'nfet',
) -> Netlist:
	# fet_class = nmos if 'n' in n_or_p_fet else pmos
	# fet_type = 'nfet' if 'n' in n_or_p_fet else 'pfet'
	csrc_netlist=Netlist(circuit_name='CASCODECOMMONSRC',
							nodes=['VIN', 'VBIAS', 'VSS', 'IOUT', 'INT'])
	m1_ref = csrc_netlist.connect_netlist(fetM1.info['netlist'], 
												[("D","INT"),
												("G","VIN"),
												("S", "VSS"),
												("B","VSS")])
	m2_ref = csrc_netlist.connect_netlist(fetM1.info['netlist'], 
												[("D","IOUT"),
												("G","VBIAS"),
												("S", "INT"),
												("B","VSS")])										
	
	
	return csrc_netlist
	



#@cell
def cascode_common_source(
    pdk: MappedPDK, 
    numcols: int = 3,
    device: str = 'nfet',
	m1_fingers: int = 1,
	m1_multipliers: int = 1,
	m2_fingers: int = 1,
	m2_multipliers: int = 1,
    with_dummy: Optional[bool] = True,
    with_substrate_tap: Optional[bool] = False,
    with_tie: Optional[bool] = True,
    tie_layers: tuple[str,str]=("met2","met1"),
    **kwargs
) -> Component:
	"""An instantiable cascode common source amplifier that returns a Component object. 
	The cascode common source amplifier could be a two transistor interdigitized structure with a shorted source and gate. 
	It can be instantiated with either nmos or pmos devices. It can also be instantiated with a dummy device, a substrate tap, and a tie layer, and is centered at the origin. 
	Transistor A acts as the reference and Transistor B acts as the mirror fet
	Transistor M1 acts as the input transistor and Transistor M2 acts as the cascoded output transistor fet which determines the output impedance.

	Args:
		pdk (MappedPDK): the process design kit to use
		numcols (int): number of columns of the interdigitized fets
		device (str): nfet or pfet (can only interdigitize one at a time with this option)
		m1_fingers: Number of fingers of M1 transistor
		m1_multiplier: Number of multipliers of M1 transistor
		with_dummy (bool): True places dummies on either side of the interdigitized fets
		with_substrate_tap (bool): boolean to decide whether to place a substrate tapring
		with_tie (bool): boolean to decide whether to place a tapring for tielayer
		tie_layers (tuple[str,str], optional): the layers to use for the tie. Defaults to ("met2","met1").
		**kwargs: The keyword arguments are passed to the two_nfet_interdigitized or two_pfet_interdigitized functions and need to be valid arguments that can be accepted by the multiplier function

	Returns:
		Component: a cascode common source amplifier component object
	"""
	top_level = Component("cascode common source amplifier")
	# Create the transistors
	print(f"Creating ", device, " devices with these parameters: ",m1_fingers,m1_multipliers, m2_fingers, m2_multipliers)
	if device in ['nmos', 'nfet']:
		fet_M1=nmos(pdk,
					fingers=m1_fingers,
					multipliers = m1_multipliers,
					with_tie=True,
					with_dummy=False, #with_dummy,
					with_substrate_tap=False,
					**kwargs)
		fet_M2=nmos(pdk,
					fingers=m2_fingers,
					multipliers = m2_multipliers,
					with_tie=True,
					with_dummy=False, #with_dummy,
					with_substrate_tap=False,
					**kwargs)
	elif device in ['pmos', 'pfet']:
		fet_M1=pmos(pdk,
					fingers=m1_fingers,
					multipliers = m1_multipliers,
					with_tie=True,
					with_dummy=False, #with_dummy,
					with_substrate_tap=False,
					**kwargs)
		fet_M2=pmos(pdk,
					fingers=m2_fingers,
					multipliers = m2_multipliers,
					with_tie=True,
					with_dummy=False, #with_dummy,
					with_substrate_tap=False,
					**kwargs)
	
	# Added references to the two FETs within the component level
	M1_ref = top_level << fet_M1
	M2_ref = top_level << fet_M2

	top_level.add(M1_ref)
	top_level.add(M2_ref)
	# Placement
	M1_ref_centre_coord = prec_ref_center(fet_M1)
	M2_ref_centre_coord = prec_ref_center(fet_M2)

	# Place the devices Horizontally ('H') or Vertically('V') based on placement selection
	place_devices='V' 
	if place_devices in ['lateral', 'horizontal', 'H']:
		M2_ref.movex(0.75*(evaluate_bbox(M1_ref)[0]+evaluate_bbox(M2_ref)[0]))
	if place_devices in ['vertical', 'V']:
		M2_ref.movey(0.5*(evaluate_bbox(M1_ref)[1]+evaluate_bbox(M2_ref)[1]))
		
	maxmet_sep = pdk.util_max_metal_seperation()

	# Routing and Port definitions
	# if place_devices in ['lateral', 'horizontal', 'H']:
	# 	top_level << straight_route(pdk, M1_ref.ports["multiplier_0_drain_W"], M2_ref.ports["multiplier_0_source_E"])
	# if  place_devices in ['vertical', 'V']:
	# 	top_level << c_route(pdk, M1_ref.ports["multiplier_0_drain_E"], M2_ref.ports["multiplier_0_source_E"])
		

	# ************* Adding the suffix after the routing generates the prefix after routing.
	#### top_level.unlock()
	top_level.add_ports(M1_ref.get_ports_list(), prefix="M1_")
	top_level.add_ports(M2_ref.get_ports_list(), prefix="M2_")

	# Shorting the Source of M2 to the Drain of M1.
	int_net_short = top_level << c_route(pdk, 
											top_level.ports["M2_source_E"], 
											top_level.ports["M1_drain_E"], 
											extension=4*maxmet_sep, 
											viaoffset=False)
	top_level.add_ports(int_net_short.get_ports_list(), prefix="INT")

	# add well
	# if device in ['nmos', 'nfet']:
	# 	print(f"NMOS device")
	# 	# add a pwell 
	# 	top_level.add_padding(layers = (pdk.get_glayer("pwell"),), default = pdk.get_grule("pwell", "active_tap")["min_enclosure"], )
	# 	top_level = add_ports_perimeter(top_level, layer = pdk.get_glayer("pwell"), prefix="well_")
	# elif device in ['pmos', 'pfet']:
	# 	# add a nwell 
	# 	top_level.add_padding(layers = (pdk.get_glayer("nwell"),), default = pdk.get_grule("nwell", "active_tap")["min_enclosure"], )
	# 	top_level = add_ports_perimeter(top_level, layer = pdk.get_glayer("nwell"), prefix="well_")
	# else:
	# 	raise ValueError("type must be either nfet or pfet")
	device_well = "nwell" if 'p' in device else "pwell"
	top_level.add_padding(layers = (pdk.get_glayer(device_well),), default = pdk.get_grule(device_well, "active_tap")["min_enclosure"], )
	top_level = add_ports_perimeter(top_level, layer = pdk.get_glayer(device_well), prefix="well_")


	# Connecting the source of the FETs to the BULK
	srcM1bulk=top_level << straight_route(pdk, top_level.ports["M1_source_E"], 
												top_level.ports["M1_tie_W_top_met_E"], glayer2="met2") #E
	srcM2bulk=top_level << straight_route(pdk, top_level.ports["M1_tie_W_top_met_E"], 
												top_level.ports["M2_tie_W_top_met_E"], glayer2="met3") 
												#M2_tie_W_top_met_E M2_tie_S_top_met_S M2_tie_E_top_met_E, only met3 matches
	# srcM3bulk=top_level << straight_route(pdk, top_level.ports["INTcon_S"], 
	# 											top_level.ports["M2_tie_E_bottom_lay_E"], glayer2="met2")	#M2_tie_S_top_met_E	, M2_tie_S_top_met_S		M2_tie_E_top_met_E				M2_source_E			
	# srcM3bulk=top_level << straight_route(pdk, top_level.ports["M2_tie_E_top_met_E"], 
	# 											top_level.ports["M2_tie_E_bottom_lay_E"], glayer2="met1")	#M2_tie_S_top_met_E	, M2_tie_S_top_met_S		M2_tie_E_top_met_E				M2_source_E			
	
	srcM4bulk=top_level << straight_route(pdk, top_level.ports["M2_source_W"], 
												top_level.ports["M2_tie_W_top_met_E"], glayer2="met2") 
												#M2_tie_W_top_met_E M2_tie_S_top_met_S M2_tie_E_top_met_E, only met3 matches
	
	# add via_array to vdd pin
	# vddarray = via_array(pdk, "met1","met3",size=(0.45,0.45))
	# via_array_ref = top_level << vddarray

	# top_level.add_ports(srcM1bulk.get_ports_list(), prefix="VSS")
	# top_level.add_ports(srcM2bulk.get_ports_list(), prefix="VSS")

	### Adding Port Pins for the cascode common source
	## VIN input pin placement
	pin_size = (0.35,0.35)
	vin_pin = top_level << rectangle(size=pin_size, layer=pdk.get_glayer("met3"), centered=True)
	vin_pin.movey(top_level.ymin+0.5*evaluate_bbox(vin_pin)[1])
	vin_pin.movex(-evaluate_bbox(vin_pin)[0]-0.5*evaluate_bbox(M1_ref)[0])
	## VIN input pin routing from M1 Gate
	top_level << smart_route(pdk, top_level.ports["M1_gate_W"], vin_pin.ports["e4"], viaoffset=False)
	## VIN input pin add label for port
	top_level.add_ports(vin_pin.get_ports_list(), prefix="VIN")

	## VBIAS input pin
	vbias_pin = top_level << rectangle(size=pin_size, layer=pdk.get_glayer("met3"), centered=True)
	vbias_pin.movey(evaluate_bbox(M2_ref)[1])
	vbias_pin.movex(-evaluate_bbox(vin_pin)[0]-0.5*evaluate_bbox(M2_ref)[0])
	## VBIAS input pin routing from M1 Gate
	top_level << smart_route(pdk, top_level.ports["M2_gate_W"], vbias_pin.ports["e4"], viaoffset=False)
	## VBIAS input pin add label for port
	top_level.add_ports(vbias_pin.get_ports_list(), prefix="VBIAS")


	## IOUT pin
	iout_pin = top_level << rectangle(size=pin_size, layer=pdk.get_glayer("met3"), centered=True)
	iout_pin.movey(top_level.ymax-0.5*evaluate_bbox(iout_pin)[1])
	iout_pin.movex(evaluate_bbox(vin_pin)[0]+0.5*evaluate_bbox(M2_ref)[0])
	## IOUT output pin routing from M1 Gate
	top_level << smart_route(pdk, top_level.ports["M2_drain_W"], iout_pin.ports["e1"], viaoffset=False)
	## IOUT output pin add label for port
	top_level.add_ports(iout_pin.get_ports_list(), prefix="IOUT")

	## VSS pin
	vss_pin = top_level << rectangle(size=pin_size, layer=pdk.get_glayer("met3"), centered=True)
	vss_pin.movey(top_level.ymin+0.5*evaluate_bbox(vss_pin)[1])
	vss_pin.movex(evaluate_bbox(vin_pin)[0]+0.5*evaluate_bbox(M1_ref)[0])
	## VSS pin routing from M1 Gate
	top_level << smart_route(pdk, top_level.ports["M1_source_W"], vss_pin.ports["e1"], viaoffset=False)
	## VSS ad label for port
	top_level.add_ports(vss_pin.get_ports_list(), prefix="VSS")

	## Bulk connections of both FETs to VSS
	# top_level << smart_route(pdk, top_level.ports["M1_well_E"],  top_level.ports["M2_well_E"], viaoffset=False)
	unavailable_layer_stack=[]
	available_layer_stack=[]
	for key,val in top_level.ports.items():
		# print(f"\nKEYS: ",key, " VALUES:",val, val.center, val.layer)
		try:
			top_level.add_label(key, val.center, val.layer)
			available_layer_stack.append(val.layer)
		except:
			# print(f"{val.layer} is not found in the stack.")
			unavailable_layer_stack.append(val.layer)
	print(f"{set(unavailable_layer_stack)} is not found in the stack.")
	print(f"{set(available_layer_stack)} is found in the stack.")

	# top_level.info['netlist'] = cascode_common_source_netlist(
	# 	pdk, 
  	# 	m1_width=3, #kwargs.get('width', 21), 
	# 	m2_width=3, #kwargs.get('width', 21), 
	# 	m1_length=pdk.get_grule('poly')['min_width'], #kwargs.get('length',14), 
	# 	m2_length=pdk.get_grule('poly')['min_width'], #kwargs.get('length',14),
	# 	multipliers=1, 
    # 	n_or_p_fet=device,
	# 	subckt_only=True,
	# 	m1_fingers = m1_fingers,
	# 	m2_fingers = m2_fingers,
	# 	m1_multipliers = m1_multipliers,
	# 	m2_multipliers = m2_multipliers
	# )
	top_level.info['netlist'] = cascode_common_source_netlist(
		pdk, 
		fetM1=fet_M1,
		fetM2=fet_M2,
		n_or_p_fet=device
	)

	

	generated_netlist_for_lvs = top_level.info['netlist'].generate_netlist()
	print(f"Type of generated netlist is :", generated_netlist_for_lvs)
	file_path_local_storage = "./gen_netlist.txt"
	try:
		with open(file_path_local_storage, 'w') as file:
			file.write(generated_netlist_for_lvs)
	except:
		print(f"Verify the file availability and type: ", generated_netlist_for_lvs, type(generated_netlist_for_lvs))
	return top_level

# Function to add labels to the port definitions
def cascode_common_source_labels(CMS: Component) -> Component:
	# Unlock component to attach the labels.
	CMS.unlock()
	# CMS.pprint_ports()
	# *** Adding pins and labels for metal1-5 ***
	move_info =list()
	met1_pin=(68,20)
	met1_label=(68,5)
	met2_pin = (69,16)
	met2_label = (69,5)
	met3_pin = (70,16)
	met3_label = (70,5)
	met4_pin = (71,16)
	met4_label = (71,5)
	met5_pin = (72,16)
	met5_label = (72,5)
	port_size = (0.3,0.3)
	VIN_label=rectangle(layer=met2_pin, size=port_size, centered=True).copy()
	VIN_label.add_label(text="VIN", layer=met2_label)
	# move_info.append((VIN_label, CMS.ports['M1_gate_E'], None)) # WORKS From W to E
	# move_info.append((VIN_label, CMS.ports['VIN'], None)) # VINe1, e2, e3, e4
	# move_info.append((VIN_label, CMS.ports['VINe4'], None)) # VINe1, e2, e3, e4
	move_info.append((VIN_label, CMS.ports['VINe2'], None))

	VBIAS_label=rectangle(layer=met2_pin, size=port_size, centered=True).copy()
	VBIAS_label.add_label(text="VBIAS", layer=met2_label)
	# move_info.append((VBIAS_label, CMS.ports['M2_gate_W'], None)) #WORKS
	# move_info.append((VBIAS_label, CMS.ports['VBIAS'], None))
	move_info.append((VBIAS_label, CMS.ports['VBIASe4'], None))

	VSS_label=rectangle(layer=met2_pin, size=port_size, centered=True).copy()
	VSS_label.add_label(text="VSS", layer=met2_label)
	# move_info.append((VSS_label, CMS.ports['M1_source_W'], None)) #WORKS From S to W
	# move_info.append((VSS_label, CMS.ports['VSS'], None)) # From S to W
	move_info.append((VSS_label, CMS.ports['VSSe1'], None)) # From S to W

	IOUT_label=rectangle(layer=met2_pin, size=port_size, centered=True).copy()
	IOUT_label.add_label(text="IOUT", layer=met2_label)
	# move_info.append((IOUT_label, CMS.ports['M2_drain_E'], None)) # WORKS From N to E
	# move_info.append((IOUT_label, CMS.ports['IOUT'], None)) # From N to E
	move_info.append((IOUT_label, CMS.ports['IOUTe4'], None)) # From N to E

	INT_label = rectangle(layer=met2_pin, size=port_size, centered=True).copy()
	INT_label.add_label(text="INT", layer=met2_label)
	# move_info.append((INT_label, CMS.ports['M2_source_E'], None)) #MET1_PIN
	move_info.append((INT_label, CMS.ports['INTcon_N'], None))
	# move_info.append((INT_label, CMS.ports['INT'], None))

	for label, port, alignment in move_info:
		alignment = ('c','b') if alignment is None else alignment
		aligned_label = align_comp_to_port(label, port, alignment=alignment)
		CMS.add(aligned_label)
	
	for items in move_info:
		print("\n",items)

	# for key, val in CMS.ports.items():
	# 	# print(f"\nKEYS: ",key, " VALUES:",f"{val}", val.center, val.layer)
	# 	move_info.append((key, CMS.ports[key], None))
	
	# for label, port, alignment in move_info:
	# 	alignment = ('c','b') if alignment is None else alignment
	# 	aligned_label = align_comp_to_port(label, port, alignment=alignment)
	# 	CMS.add(aligned_label)
	# Add a label to all ports in the layout
	# for key,val in CMS.ports.items():
	# # 	print(f"\nKEYS: ",key, " VALUES:",val, val.center, val.layer)
	# 	CMS.add_label(key, val.center, val.layer)
	# 	# CMS.add_label(key,val.center,val.layer)
	# 	alignment = ('c','b') if alignment is None else alignment
	# 	aligned_label = align_comp_to_port(key, CMS.ports[val.name], alignment=alignment)
	# 	CMS.add(aligned_label)

	return CMS.flatten()

mapped_pdk_build = sky130
Cascode_cs_component = cascode_common_source(mapped_pdk_build,
												m1_fingers=2,
												m2_fingers=2,
												m1_multipliers=1,
												m2_multipliers=1,
												numcols=1) 
# Add labels to the port definitions on the nets
Cascode_cs_component = cascode_common_source_labels(Cascode_cs_component)
Cascode_cs_component.show()
Cascode_cs_component.write_gds("./local_casdcode_overwite.gds")

magic_drc_result = sky130.drc_magic(Cascode_cs_component, Cascode_cs_component.name)
# magic_drc_result = sky130.drc_magic(Cascode_cs_component, Cascode_cs_component.name, output_file_path="DRC/")
if magic_drc_result :
    print("DRC is clean: ", magic_drc_result)
else:
    print("DRC failed. Please try again.")

Cascode_cs_component.name = 'cascode_common_source_lvs' 
netgen_lvs_result = mapped_pdk_build.lvs_netgen(Cascode_cs_component, 'cascode_common_source_lvs')
# netgen_lvs_result = mapped_pdk_build.lvs_netgen(Cascode_cs_component, 'cascode_common_source_lvs', output_file_path="LVS/")


# sky130.lvs_netgen(Cascode_cs_component, 'cascode_common_source_lvs')
# print('LVS success??')
