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
from glayout.flow.primitives.guardring import tapring
from glayout.flow.pdk.util.port_utils import add_ports_perimeter,rename_ports_by_orientation	
from gdsfactory.component import Component
from typing import Optional, Union 
from gdsfactory.components import text_freetype, rectangle

from glayout.flow.pdk.util.comp_utils import prec_ref_center, prec_center, movey, evaluate_bbox, align_comp_to_port

def regulated_cascode_netlist(
    fet_M1: Component, 
    fet_M2: Component,
    name: str = 'REGCASCODE',
    nodes: Optional[list[str]] = ['I_IN', 'IBIAS', 'VSS', 'IOUT'],
) -> Netlist:
	"""Generates a netlist for a regulated cascode."""
	reg_casc_netlist = Netlist(circuit_name=name, nodes=nodes)

	reg_casc_netlist.connect_netlist(
		fet_M1.info['netlist'],
		[('D', 'IOUT'), ('G', 'IBIAS'), ('S', 'I_IN'), ('B', 'I_IN')]
	)

	reg_casc_netlist.connect_netlist(
		fet_M2.info['netlist'],
		[('D', 'IBIAS'), ('G', 'I_IN'), ('S', 'VSS'), ('B', 'VSS')]
	)

	return reg_casc_netlist


# def regulated_cascode_netlist(
# 	pdk: MappedPDK, 
# 	m1_width: float,
# 	m2_width: float,
# 	m1_length: float,
# 	m2_length: float,
# 	multipliers: int, 
# 	n_or_p_fet: Optional[str] = 'nfet',
# 	subckt_only: Optional[bool] = False,
# 	m1_fingers = int,
# 	m2_fingers = int,
# 	m1_multipliers = int,
# 	m2_multipliers = int
# ) -> Netlist:
# 	if m1_length is None:
# 		m1_length = pdk.get_grule('poly')['min_length']
# 	if m1_width is None:
# 		m1_width = pdk.get_grule('poly')['min_width']
# 	m2_length = m2_length or pdk.get_grule('poly')['min_length']
# 	m2_width = m2_width or pdk.get_grule('poly')['min_width']

# 	mtop = multipliers if subckt_only else 1
# 	model = pdk.models[n_or_p_fet]
# 	m1_multipliers = m1_multipliers or 1
# 	m2_multipliers = m2_multipliers or 1
# 	dmtop = m1_fingers*m1_multipliers
# 	num_dummies = 4
	
# 	circuit_name='CASCODECOMMONSRC'
# 	nodes=['VIN', 'VBIAS', 'VSS', 'IOUT', "INT"]
# 	model= model
# 	m1_width= m1_width
# 	m2_width= m2_width
# 	m1_length= m1_length
# 	m2_length= m2_length
# 	mult= m1_multipliers*m1_fingers
# 	m1_multipliers= m1_multipliers
# 	m2_multipliers= m2_multipliers

# 	source_netlist = f".subckt {circuit_name} {' '.join(nodes)}\n" 
# 	# source_netlist = f".subckt {circuit_name} {' '.join(nodes)}\n"
# 	# source_netlist += f'l={m1_length} w={m1_width} m={mtop}' + """
# 	source_netlist += f"XM1 INT VIN VSS VSS {model} l={m1_length} w={m1_width} m={mult}\n"
# 	source_netlist += f"XM2 IOUT VBIAS INT VSS {model} l={m2_length} w={m2_width} m={mult}"
# 	#Adding the dummies
# 	# for i in range(num_dummies):
# 	# 	source_netlist += """ \nXDUMMY"""+f'{i+1}'+""" VSS VSS VSS VSS {model} """+f'l={m1_length} w={m1_width} m={1} dm={dmtop}'

# 	source_netlist += "\n.ends {circuit_name}"

# 	instance_format = "X{name} {nodes} {circuit_name} l={length} w={width} m={mult}"
 
# 	return Netlist(
# 		circuit_name='CASCODECOMMONSRC',
# 		nodes=['VIN', 'VBIAS', 'VSS', 'IOUT', "INT"], 
# 		source_netlist=source_netlist,
#   		instance_format=instance_format,
# 		parameters={
# 			'model': model,
# 			'm1_width': m1_width,
# 			'm2_width': m2_width,
#    			'm1_length': m1_length,	
# 			'm2_length': m2_length,	
# 			'mult': m1_multipliers*m1_fingers,#multipliers,
# 			'm1_multipliers': m1_multipliers,
# 			'm2_multipliers': m2_multipliers,
#    		}
# 	)



#@cell
def regulated_cascode(
    pdk: MappedPDK,
    width: float = 3,
    length: Optional[float] = None, 
    numcols: int = 3,
    device: str = 'nfet',
	m1_fingers: int = 1,
	m1_multipliers: int = 1,
	m2_fingers: int = 1,
	m2_multipliers: int = 1,
    with_dummy: Optional[bool] = True,
    with_substrate_tap: Optional[bool] =True,
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
		Component: a regulated cascode component object
	"""
	top_level = Component("regulated cascode")
	# Create the transistors
	print(f"Creating ", device, " devices with these parameters: ",m1_fingers,m1_multipliers, m2_fingers, m2_multipliers)
 
	if device in ['nmos', 'nfet']:
		fet_M1=nmos(pdk,
					width=width,
                    length=length,
					fingers=m1_fingers,
					multipliers = m1_multipliers,
     				with_dummy=with_dummy,
					with_tie=False,
					with_substrate_tap=False,
					**kwargs)
		fet_M2=nmos(pdk,
					width=width,
                    length=length,
					fingers=m2_fingers,
					multipliers = m2_multipliers,
					with_dummy=with_dummy,
					with_tie=False,
					with_substrate_tap=False,
					**kwargs)
		min_spacing_x = pdk.get_grule("n+s/d")["min_separation"] - 2*(fet_M1.xmax - fet_M1.ports["multiplier_0_plusdoped_E"].center[0])
		well, sdglayer = "pwell", "n+s/d"
	elif device in ['pmos', 'pfet']:
		fet_M1=pmos(pdk,
					width=width,
                    length=length,
					fingers=m1_fingers,
					multipliers = m1_multipliers,
					with_dummy=with_dummy,
					with_tie=False,
					with_substrate_tap=False,
					**kwargs)
		fet_M2=pmos(pdk,
					width=width,
                    length=length,
					fingers=m2_fingers,
					multipliers = m2_multipliers,
					with_dummy=with_dummy,
					with_tie=False,
					with_substrate_tap=False,
					**kwargs)
		min_spacing_x = pdk.get_grule("p+s/d")["min_separation"] - 2*(fet_M1.xmax - fet_M1.ports["multiplier_0_plusdoped_E"].center[0])
		well, sdglayer = "nwell", "p+s/d"
	print("FETS are instantiated now")
	

    # place and flip top transistors such that the drains of bottom and top point towards eachother
	M1_ref = top_level << fet_M1
	#a_topl = rename_ports_by_orientation(a_topl.mirror_y())
	M2_ref = top_level << fet_M2
	#M2_ref  = rename_ports_by_orientation(M2_ref .mirror_x())

	top_level.add(M1_ref)
	top_level.add(M2_ref)
 
	# Placement
	M1_ref_centre_coord = prec_ref_center(M1_ref, snapmov2grid=True)
	M2_ref_centre_coord = prec_ref_center(M2_ref, snapmov2grid=True)
 
	# Place the devices Horizontally ('H') or Vertically('V') based on placement selection
	place_devices='V' 
	if place_devices in ['lateral', 'horizontal', 'H']:
		M2_ref.movex(0.75*(evaluate_bbox(M1_ref)[0]+evaluate_bbox(M2_ref)[0]))
	if place_devices in ['vertical', 'V']:
		M2_ref.movey(0.5*(evaluate_bbox(M1_ref)[1]+evaluate_bbox(M2_ref)[1]))
 
	 #### top_level.unlock()
	top_level.add_ports(M1_ref.get_ports_list(), prefix="M1_")
	top_level.add_ports(M2_ref.get_ports_list(), prefix="M2_")
     
    # add well
	top_level.add_padding(default=pdk.get_grule(well, "active_tap")["min_enclosure"],layers=[pdk.get_glayer(well)])
	top_level = add_ports_perimeter(top_level, layer = pdk.get_glayer(well), prefix="well_")
 
	# if substrate tap place substrate tap, and route dummy to substrate tap
	if with_substrate_tap:
		tapref = top_level << tapring(pdk,(evaluate_bbox(top_level,padding=pdk.get_grule(well, "active_tap")["min_enclosure"])),horizontal_glayer="met1")
		tapref.movey(0.5*((evaluate_bbox(M2_ref)[1])))
		top_level.add_ports(tapref.get_ports_list(),prefix="tap_")
  
		try:
			top_level<<straight_route(pdk,top_level.ports["M1_multiplier_0_dummy_L_gsdcon_top_met_W"],top_level.ports["tap_W_top_met_W"],glayer2="met1")
		except KeyError:
			pass
		try:
			top_level<<straight_route(pdk,top_level.ports["M1_multiplier_0_dummy_R_gsdcon_top_met_W"],top_level.ports["tap_E_top_met_E"],glayer2="met1")
		except KeyError:
			pass

		try:
			top_level<<straight_route(pdk,top_level.ports["M2_multiplier_0_dummy_L_gsdcon_top_met_W"],top_level.ports["tap_W_top_met_W"],glayer2="met1")
		except KeyError:
			pass
		try:
			top_level<<straight_route(pdk,top_level.ports["M2_multiplier_0_dummy_R_gsdcon_top_met_W"],top_level.ports["tap_E_top_met_E"],glayer2="met1")
		except KeyError:
			pass
        	
	# Routing and Port definitions
	# if place_devices in ['lateral', 'horizontal', 'H']:
	# 	top_level << straight_route(pdk, M1_ref.ports["multiplier_0_drain_W"], M2_ref.ports["multiplier_0_source_E"])
	# if  place_devices in ['vertical', 'V']:
	# 	top_level << c_route(pdk, M1_ref.ports["multiplier_0_drain_E"], M2_ref.ports["multiplier_0_source_E"])
		

	##************* Adding the suffix after the routing generates the prefix after routing.
	maxmet_sep = pdk.util_max_metal_seperation()
	# Shorting the Drain of M2/B to the Gate of M1/A.
	net_short_AG_BD = top_level << smart_route(pdk, 
											top_level.ports["M2_drain_E"], 
											top_level.ports["M1_gate_E"], 
											extension=2*maxmet_sep,
											viaoffset=False)
    # Shorting the Source of M1/A to the Gate of M2/B.
	net_short_AS_BG = top_level << c_route(pdk, 
											top_level.ports["M1_source_W"], 
											top_level.ports["M2_gate_W"], 
											extension=2*maxmet_sep, 
											viaoffset=False)
 
 
	top_level.add_ports(net_short_AG_BD.get_ports_list(), prefix="AG_BD_")
	top_level.add_ports(net_short_AS_BG.get_ports_list(), prefix="AS_BG_")

	# Connecting the source of the M2 FET to the BULK
	srcM2bulk=top_level << straight_route(pdk, top_level.ports["M2_source_E"], 
												top_level.ports["tap_W_top_met_W"], glayer2="met2")
	#bulk2bulk=top_level << straight_route(pdk, top_level.ports["M1_tie_W_top_met_E"], 
	 											#top_level.ports["M2_tie_W_top_met_E"], glayer2="met3") #M2_tie_W_top_met_E M2_tie_S_top_met_S M2_tie_E_top_met_E, only met3 
	
 	### Adding Port Pins for the cascode common source
	## I_IN input pin placement
	pin_size = (0.35,0.35)
	Iin_pin = top_level << rectangle(size=pin_size, layer=pdk.get_glayer("met3"), centered=True)
	Iin_pin.movey(top_level.ymin)
	Iin_pin.movex(evaluate_bbox(Iin_pin)[0]-0.5*evaluate_bbox(M1_ref)[0])
	## I_IN input pin routing from A Source - B Gate Short
	top_level << smart_route(pdk, top_level.ports["AS_BG_con_N"], Iin_pin.ports["e1"], viaoffset=False)
	## I_IN input pin add label for port
	top_level.add_ports(Iin_pin.get_ports_list(), prefix="I_IN_")

	## IBIAS input pin
	Ibias_pin = top_level << rectangle(size=pin_size, layer=pdk.get_glayer("met3"), centered=True)
	Ibias_pin.movey(top_level.ymin)
	Ibias_pin.movex(evaluate_bbox(Ibias_pin)[0]+0.5*evaluate_bbox(M1_ref)[0])
	## IBIAS input pin routing from B Drain - A Gate Short
	top_level << smart_route(pdk, top_level.ports["AG_BD_con_N"], Ibias_pin.ports["e1"], viaoffset=False)
	## VBIAS input pin add label for port
	top_level.add_ports(Ibias_pin.get_ports_list(), prefix="IBIAS_")


	## IOUT pin
	Iout_pin = top_level << rectangle(size=pin_size, layer=pdk.get_glayer("met3"), centered=True)
	Iout_pin.movey(top_level.ymax)
	Iout_pin.movex(+evaluate_bbox(Iin_pin)[0]+0.5*evaluate_bbox(M1_ref)[0])
	## IOUT output pin routing from A Source
	top_level << smart_route(pdk, top_level.ports["M1_drain_E"], Iout_pin.ports["e2"], viaoffset=False)
	## IOUT output pin add label for port
	top_level.add_ports(Iout_pin.get_ports_list(), prefix="IOUT_")

	## VSS pin
	vss_pin = top_level << rectangle(size=pin_size, layer=pdk.get_glayer("met3"), centered=True)
	vss_pin.movey(top_level.ymax)
	vss_pin.movex(evaluate_bbox(Iin_pin)[0]-0.5*evaluate_bbox(M2_ref)[0])
	## VSS pin routing from M2 Source
	top_level << smart_route(pdk, top_level.ports["M2_source_W"], vss_pin.ports["e2"], viaoffset=False)
	## VSS ad label for port
	top_level.add_ports(vss_pin.get_ports_list(), prefix="VSS_")

	top_level.info['netlist'] = regulated_cascode_netlist(fet_M1, fet_M2,
     										name = top_level.name,
               								nodes = ['I_IN', 'IBIAS', 'VSS', 'IOUT']
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


def regulated_cascode_labels(CMS: Component) -> Component:
	# Unlock component to attach the labels.
	CMS.unlock()
	#CMS.pprint_ports()
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

 
	I_IN_label=rectangle(layer=met2_pin, size=port_size, centered=True).copy()
	I_IN_label.add_label(text="I_IN", layer=met2_label)
	# move_info.append((VIN_label, CMS.ports['M1_gate_E'], None)) # WORKS From W to E
	# move_info.append((VIN_label, CMS.ports['VIN'], None)) # VINe1, e2, e3, e4
	# move_info.append((VIN_label, CMS.ports['VINe4'], None)) # VINe1, e2, e3, e4
	move_info.append((I_IN_label, CMS.ports['I_IN_e2'], None))

	IBIAS_label=rectangle(layer=met2_pin, size=port_size, centered=True).copy()
	IBIAS_label.add_label(text="IBIAS", layer=met2_label)
	# move_info.append((VBIAS_label, CMS.ports['M2_gate_W'], None)) #WORKS
	# move_info.append((VBIAS_label, CMS.ports['VBIAS'], None))
	move_info.append((IBIAS_label, CMS.ports['IBIAS_e2'], None))
 
	IOUT_label=rectangle(layer=met2_pin, size=port_size, centered=True).copy()
	IOUT_label.add_label(text="I_OUT", layer=met2_label)
	# move_info.append((IOUT_label, CMS.ports['M2_drain_E'], None)) # WORKS From N to E
	# move_info.append((IOUT_label, CMS.ports['IOUT'], None)) # From N to E
	move_info.append((IOUT_label, CMS.ports['IOUT_e2'], None)) # From N to E

	VSS_label=rectangle(layer=met2_pin, size=port_size, centered=True).copy()
	VSS_label.add_label(text="VSS", layer=met2_label)
	# move_info.append((VSS_label, CMS.ports['M1_source_W'], None)) #WORKS From S to W
	# move_info.append((VSS_label, CMS.ports['VSS'], None)) # From S to W
	move_info.append((VSS_label, CMS.ports['VSS_e2'], None)) # From S to W

	for label, port, alignment in move_info:
		alignment = ('c','b') if alignment is None else alignment
		aligned_label = align_comp_to_port(label, port, alignment=alignment)
		CMS.add(aligned_label)

	return CMS.flatten()

mapped_pdk_build = sky130
Cascode_reg_component = regulated_cascode(mapped_pdk_build,
												m1_fingers=1,
												m2_fingers=1,
												m1_multipliers=1,
												m2_multipliers=1,
												numcols=1) 

#Cascode_reg_component.pprint_ports()
## Add labels to the port definitions on the nets
Cascode_reg_component = regulated_cascode_labels(Cascode_reg_component)
Cascode_reg_component.show()
Cascode_reg_component.write_gds("./local_casdcode_overwite.gds")

# for absc in top_level.ports.keys():
# 	if len(absc.split("_")) <=9:
# 		if set(["M1","gsdcon","top","met"]).issubset(set(absc.split("_"))):
# 			print(absc)
# print("------")
# for absc in top_level.ports.keys():
# 		if len(absc.split("_")) <=9:
# 			if set(["M2","gsdcon","top","met"]).issubset(set(absc.split("_"))):
# 				print(absc)



magic_drc_result = sky130.drc_magic(Cascode_reg_component, Cascode_reg_component.name)
#magic_drc_result = sky130.drc_magic(Cascode_cs_component, Cascode_cs_component.name, output_file_path="DRC/")
if magic_drc_result :
    print("DRC is clean: ", magic_drc_result['result_str'])
else:
    print("DRC failed. Please try again.")

#Cascode_reg_component.name = 'regulated_cascode_lvs' 
#netgen_lvs_result = mapped_pdk_build.lvs_netgen(Cascode_reg_component, 'regulated_cascode_lvs')
#netgen_lvs_result = mapped_pdk_build.lvs_netgen(Cascode_reg_component, 'regulated_cascode_lvs', output_file_path="LVS/")


# sky130.lvs_netgen(Cascode_cs_component, 'cascode_common_source_lvs')
# print('LVS success??')
