from glayout.flow.placement.two_transistor_interdigitized import two_nfet_interdigitized, two_pfet_interdigitized
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.spice.netlist import Netlist
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.flow.primitives.fet import nmos, pmos
from glayout.flow.primitives.guardring import tapring
from glayout.flow.pdk.util.port_utils import add_ports_perimeter	
from gdsfactory.component import Component
from typing import Optional, Union 
from gdsfactory.components import text_freetype, rectangle

from glayout.flow.pdk.util.comp_utils import prec_ref_center, prec_center, movey, evaluate_bbox, align_comp_to_port

# def cascode_common_source_netlist(
# 	pdk: MappedPDK, 
# 	width: float,
# 	length: float,
# 	multipliers: int, 
# 	n_or_p_fet: Optional[str] = 'nfet',
# 	subckt_only: Optional[bool] = False,
# 	m1_fingers = int,
# 	m2_fingers = int,
# 	m1_multipliers = int,
# 	m2_multipliers = int
# ) -> Netlist:
# 	if length is None:
# 		length = pdk.get_grule('poly')['min_width']
# 	if width is None:
# 		width = 3 
# 	mtop = multipliers if subckt_only else 1
# 	model = pdk.models[n_or_p_fet]
	
# 	source_netlist = """.subckt {circuit_name} {nodes} """ + f'l={length} w={width} m={mtop} ' + """
# XM1 INT VIN VSS VSS {model} l={{length}} w={{width}} m={{m1_multipliers}}
# XM2 IOUT VBIAS INT VSS {model} l={{length}} w={{width}} m={{m2_multipliers}}"""
# 	source_netlist += "\n.ends {circuit_name}"

# 	instance_format = "X{name} {nodes} {circuit_name} l={length} w={width} m={mult}"
 
# 	return Netlist(
# 		circuit_name='CASCODECOMMONSRC',
# 		nodes=['VIN', 'VBIAS', 'VSS', 'IOUT'], 
# 		source_netlist=source_netlist,
#   		instance_format=instance_format,
# 		parameters={
# 			'model': model,
# 			'width': width,
#    			'length': length,	
# 			'mult': multipliers
#    		}
# 	)
def cascode_common_source_netlist(
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
	
	source_netlist = """.subckt {circuit_name} {nodes} """ + f'l={m1_length} w={m1_width} m={mtop} dm={dmtop}' + """
XM1 INT VIN VSS VSS {model} l={m1_length} w={m1_width} m={mult} dm={m1_multipliers}
XM2 IOUT VBIAS INT VSS {model} l={m2_length} w={m2_width} m={mult} dm={m2_multipliers}"""
	#Adding the dummies
	#for i in range(num_dummies):
	#	source_netlist += """ \nXDUMMY"""+f'{i+1}'+""" B B B B {model} """+f'l={m1_length} w={m1_width} m={1} dm={dmtop}'

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
	if device in ['nmos', 'nfet']:
		fet_M1=nmos(pdk,
					fingers=m1_fingers,
					multipliers = m1_multipliers,
					with_tie=False,
					with_dummy=with_dummy,
					with_substrate_tap=False,
					**kwargs)
		fet_M2=nmos(pdk,
					fingers=m2_fingers,
					multipliers = m2_multipliers,
					with_tie=False,
					with_dummy=with_dummy,
					with_substrate_tap=False,
					**kwargs)
	elif device in ['pmos', 'pfet']:
		fet_M1=pmos(pdk,
					fingers=m1_fingers,
					multipliers = m1_multipliers,
					with_tie=False,
					with_dummy=with_dummy,
					with_substrate_tap=False,
					**kwargs)
		fet_M2=pmos(pdk,
					fingers=m2_fingers,
					multipliers = m2_multipliers,
					with_tie=False,
					with_dummy=with_dummy,
					with_substrate_tap=False,
					**kwargs)
	print("FETS are instantiated now")
	
	# Added references to the two FETs within the component level
	M1_ref = top_level << fet_M1
	M2_ref = top_level << fet_M2
	# Placement
	M1_ref_centre_coord = prec_ref_center(fet_M1)
	M2_ref_centre_coord = prec_ref_center(fet_M2)
	place_devices='V'
	if place_devices in ['lateral', 'horizontal', 'H']:
		M2_ref.movex(0.75*(evaluate_bbox(M1_ref)[1]+evaluate_bbox(M2_ref)[1]))
	if place_devices in ['vertical', 'V']:
		M2_ref.movey(0.75*(evaluate_bbox(M1_ref)[1]+evaluate_bbox(M2_ref)[1]))

	# Routing and Port definitions
	if place_devices in ['lateral', 'horizontal', 'H']:
		top_level << straight_route(pdk, M1_ref.ports["multiplier_0_drain_W"], M2_ref.ports["multiplier_0_source_E"])
	if  place_devices in ['vertical', 'V']:
		top_level << c_route(pdk, M1_ref.ports["multiplier_0_drain_E"], M2_ref.ports["multiplier_0_source_E"])
		

	# ************* Adding the suffix after the routing generates the prefix after routing.
	# top_level.unlock()
	top_level.add_ports(M1_ref.get_ports_list(), prefix="M1_")
	top_level.add_ports(M2_ref.get_ports_list(), prefix="M2_")
	# #Now attach pin names for port
	# top_level.unlock()
	# # *** Adding pins and labels for metal1-5 ***
	# move_info =list()
	# met1_pin=(68,20)
	# met1_label=(68,5)
	# met2_pin = (69,16)
	# met2_label = (69,5)
	# met3_pin = (70,16)
	# met3_label = (70,5)
	# met4_pin = (71,16)
	# met4_label = (71,5)
	# met5_pin = (72,16)
	# met5_label = (72,5)
	# port_size = (0.35,0.35)
	# VIN_label=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
	# VIN_label.add_label(text="VIN", layer=met1_label)
	# move_info.append((VIN_label, top_level.ports['M1_gate_W'], None))

	# VBIAS_label=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
	# VBIAS_label.add_label(text="VBIAS", layer=met1_label)
	# move_info.append((VBIAS_label, top_level.ports['M2_gate_W'], None))

	# VSS_label=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
	# VSS_label.add_label(text="VSS", layer=met1_label)
	# move_info.append((VSS_label, top_level.ports['M1_source_S'], None))

	# IOUT_label=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
	# IOUT_label.add_label(text="IOUT", layer=met1_label)
	# move_info.append((IOUT_label, top_level.ports['M2_drain_N'], None))

	# for comp, prt, alignment in move_info:
	# 	alignment = ('c','b') if alignment is None else alignment
	# 	compref = align_comp_to_port(comp, prt, alignment=alignment)
	# 	top_level.add(compref)

	# top_level.flatten()
	# THIS IS THE ORIGINAL ARGUMENTS FOR THE NETLIST GENERATION FUNCTION 
	# top_level.info['netlist'] = cascode_common_source_netlist(
	# 	pdk, 
  	# 	width=kwargs.get('width', 3), 
	# 	length=kwargs.get('length', 1), 
	# 	multipliers=numcols, 
    # 	n_or_p_fet=device,
	# 	subckt_only=True,
	# 	m1_fingers = m1_fingers,
	# 	m2_fingers = m2_fingers,
	# 	m1_multipliers = m1_multipliers,
	# 	m2_multipliers = m2_multipliers
	# )
	top_level.info['netlist'] = cascode_common_source_netlist(
		pdk, 
  		m1_width=3, #kwargs.get('width', 21), 
		m2_width=3, #kwargs.get('width', 21), 
		m1_length=pdk.get_grule('poly')['min_width'], #kwargs.get('length',14), 
		m2_length=pdk.get_grule('poly')['min_width'], #kwargs.get('length',14),
		multipliers=1, 
    	n_or_p_fet=device,
		subckt_only=True,
		m1_fingers = m1_fingers,
		m2_fingers = m2_fingers,
		m1_multipliers = m1_multipliers,
		m2_multipliers = m2_multipliers
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


def cascode_common_source_labels(CMS: Component) -> Component:
	# Unlock compoonent to attach the labels.
	CMS.unlock()
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
	port_size = (0.35,0.35)
	VIN_label=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
	VIN_label.add_label(text="VIN", layer=met1_label)
	move_info.append((VIN_label, CMS.ports['M1_gate_W'], None))

	VBIAS_label=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
	VBIAS_label.add_label(text="VBIAS", layer=met1_label)
	move_info.append((VBIAS_label, CMS.ports['M2_gate_W'], None))

	VSS_label=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
	VSS_label.add_label(text="VSS", layer=met1_label)
	move_info.append((VSS_label, CMS.ports['M1_source_S'], None))

	IOUT_label=rectangle(layer=met1_pin, size=port_size, centered=True).copy()
	IOUT_label.add_label(text="IOUT", layer=met1_label)
	move_info.append((IOUT_label, CMS.ports['M2_drain_N'], None))

	INT_label = rectangle(layer=met1_pin, size=port_size, centered=True).copy()
	INT_label.add_label(text="INT", layer=met1_label)
	move_info.append((INT_label, CMS.ports['M2_source_E'], None))

	for comp, prt, alignment in move_info:
		alignment = ('c','b') if alignment is None else alignment
		compref = align_comp_to_port(comp, prt, alignment=alignment)
		CMS.add(compref)

	return CMS.flatten()

mapped_pdk_build = sky130
Cascode_cs_component = cascode_common_source(mapped_pdk_build,
												m1_fingers=1,
												m2_fingers=1,
												m1_multipliers=1,
												m2_multipliers=1,
												numcols=1) 
# Add labels to the port definitions
Cascode_cs_component = cascode_common_source_labels(Cascode_cs_component)
Cascode_cs_component.show()
Cascode_cs_component.write_gds("./local_casdcode_overwite.gds")

magic_drc_result = sky130.drc_magic(Cascode_cs_component, Cascode_cs_component.name)
# if magic_drc_result :
#     print("DRC is clean: ", magic_drc_result)
# else:
#     print("DRC failed. Please try again.")

Cascode_cs_component.name = 'cascode_common_source_lvs' 
netgen_lvs_result = mapped_pdk_build.lvs_netgen(Cascode_cs_component, 'cascode_common_source_lvs')

# sky130.lvs_netgen(Cascode_cs_component, 'cascode_common_source_lvs')
# print('LVS success??')
