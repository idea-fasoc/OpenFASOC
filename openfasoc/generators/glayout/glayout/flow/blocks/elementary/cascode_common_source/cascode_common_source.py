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

from glayout.flow.pdk.util.comp_utils import prec_ref_center, prec_center, movey, evaluate_bbox

def cascode_common_source_netlist(
	pdk: MappedPDK, 
	width: float,
	length: float,
	multipliers: int, 
	n_or_p_fet: Optional[str] = 'nfet',
	subckt_only: Optional[bool] = False
) -> Netlist:
	if length is None:
		length = pdk.get_grule('poly')['min_width']
	if width is None:
		width = 3 
	mtop = multipliers if subckt_only else 1
	model = pdk.models[n_or_p_fet]
	
	source_netlist = """.subckt {circuit_name} {nodes} """ + f'l={length} w={width} m={mtop} ' + """
XM1 INT VIN VSS VSS {model} l={{l}} w={{w}} m={{m}}
XM2 IOUT VBIAS INT VSS {model} l={{l}} w={{w}} m={{m}}"""
	source_netlist += "\n.ends {circuit_name}"

	instance_format = "X{name} {nodes} {circuit_name} l={length} w={width} m={mult}"
 
	return Netlist(
		circuit_name='CASCODECOMMONSRC',
		nodes=['VIN', 'VBIAS', 'VSS', 'IOUT'], 
		source_netlist=source_netlist,
  		instance_format=instance_format,
		parameters={
			'model': model,
			'width': width,
   			'length': length,	
			'mult': multipliers
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
		M2_ref.movex(0.5*(evaluate_bbox(M1_ref)[1]+evaluate_bbox(M2_ref)[1]))
	if place_devices in ['vertical', 'V']:
		M2_ref.movey(0.5*(evaluate_bbox(M1_ref)[1]+evaluate_bbox(M2_ref)[1]))

	
	top_level.add_ports(M1_ref.get_ports_list(), prefix="M1_")
	top_level.add_ports(M2_ref.get_ports_list(), prefix="M2_")
	# Routing and Port definitions
	if place_devices in ['lateral', 'horizontal', 'H']:
		top_level << straight_route(pdk, M1_ref.ports["multiplier_0_drain_W"], M2_ref.ports["multiplier_0_source_E"])
	if  place_devices in ['vertical', 'V']:
		top_level << c_route(pdk, M1_ref.ports["multiplier_0_drain_E"], M2_ref.ports["multiplier_0_source_E"])
	#So now I attach pin names for port
	text_pin_labels = list()
	met5pin = rectangle(size=(5,5),layer=(72,16), centered=True)
	for name in ['VIN', 'VBIAS', 'VSS', 'IOUT']:
		pin_w_label = met5pin.copy()
		pin_w_label.add_label(text=name,layer=(72,5),magnification=4)
		text_pin_labels.append(pin_w_label)
	
	
	top_level.info['netlist'] = cascode_common_source_netlist(
		pdk, 
  		width=kwargs.get('width', 3), length=kwargs.get('length', 1), multipliers=numcols, 
    	n_or_p_fet=device,
		subckt_only=True
	)
 
	return top_level


mapped_pdk_build = sky130
Cascode_cs_component = cascode_common_source(mapped_pdk_build,
												m1_fingers=5,
												m2_fingers=5,
												m1_multipliers=1,
												m2_multipliers=1,
												numcols=10) 
Cascode_cs_component.show()

magic_drc_result = sky130.drc_magic(Cascode_cs_component, Cascode_cs_component.name)
if magic_drc_result :
    print("DRC is clean: ", magic_drc_result)
else:
    print("DRC failed. Please try again.")

Cascode_cs_component.name = 'cascode_common_source_lvs' 
netgen_lvs_result = mapped_pdk_build.lvs_netgen(Cascode_cs_component, 'cascode_common_source_lvs')
print(f"LVS results", netgen_lvs_result)

