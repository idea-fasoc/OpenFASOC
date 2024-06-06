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


def current_mirror_netlist(
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
XA VREF VREF VSS VB {model} l={{l}} w={{w}} m={{m}}
XB VCOPY VREF VSS VB {model} l={{l}} w={{w}} m={{m}}"""
	source_netlist += "\n.ends {circuit_name}"

	instance_format = "X{name} {nodes} {circuit_name} l={length} w={width} m={mult}"
 
	return Netlist(
		circuit_name='CMIRROR',
		nodes=['VREF', 'VCOPY', 'VSS', 'VB'], 
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
def current_mirror(
    pdk: MappedPDK, 
    numcols: int = 3,
    device: str = 'nfet',
    with_dummy: Optional[bool] = True,
    with_substrate_tap: Optional[bool] = False,
    with_tie: Optional[bool] = True,
    tie_layers: tuple[str,str]=("met2","met1"),
    **kwargs
) -> Component:
	"""An instantiable current mirror that returns a Component object. The current mirror is a two transistor interdigitized structure with a shorted source and gate. It can be instantiated with either nmos or pmos devices. It can also be instantiated with a dummy device, a substrate tap, and a tie layer, and is centered at the origin. Transistor A acts as the reference and Transistor B acts as the mirror fet

	Args:
		pdk (MappedPDK): the process design kit to use
		numcols (int): number of columns of the interdigitized fets
		device (str): nfet or pfet (can only interdigitize one at a time with this option)
		with_dummy (bool): True places dummies on either side of the interdigitized fets
		with_substrate_tap (bool): boolean to decide whether to place a substrate tapring
		with_tie (bool): boolean to decide whether to place a tapring for tielayer
		tie_layers (tuple[str,str], optional): the layers to use for the tie. Defaults to ("met2","met1").
		**kwargs: The keyword arguments are passed to the two_nfet_interdigitized or two_pfet_interdigitized functions and need to be valid arguments that can be accepted by the multiplier function

	Returns:
		Component: a current mirror component object
	"""
	top_level = Component("current mirror")
	if device in ['nmos', 'nfet']:
		interdigitized_fets = two_nfet_interdigitized(
			pdk, 
			numcols=numcols, 
			dummy=with_dummy, 
			with_substrate_tap=False, 
			with_tie=False, 
			**kwargs
		)
	elif device in ['pmos', 'pfet']:
		interdigitized_fets = two_pfet_interdigitized(
			pdk, 
			numcols=numcols, 
			dummy=with_dummy, 
			with_substrate_tap=False, 
			with_tie=False, 
			**kwargs
		)
	top_level.add_ports(interdigitized_fets.get_ports_list(), prefix="fet_")
	maxmet_sep = pdk.util_max_metal_seperation()
	# short source of the fets
	source_short = interdigitized_fets << c_route(pdk, interdigitized_fets.ports['A_source_E'], interdigitized_fets.ports['B_source_E'], extension=3*maxmet_sep, viaoffset=False)
	# short gates of the fets
	gate_short = interdigitized_fets << c_route(pdk, interdigitized_fets.ports['A_gate_W'], interdigitized_fets.ports['B_gate_W'], extension=3*maxmet_sep, viaoffset=False)
	# short gate and drain of one of the reference 
	interdigitized_fets << L_route(pdk, interdigitized_fets.ports['A_drain_W'], gate_short.ports['con_N'], viaoffset=False, fullbottom=False)
	
	top_level << interdigitized_fets
	# add the tie layer
	if with_tie:
		tap_sep = max(
            pdk.util_max_metal_seperation(),
            pdk.get_grule("active_diff", "active_tap")["min_separation"],
        )
		tap_sep += pdk.get_grule("p+s/d", "active_tap")["min_enclosure"]
		tap_encloses = (
		2 * (tap_sep + interdigitized_fets.xmax),
		2 * (tap_sep + interdigitized_fets.ymax),
		)
		tie_ref = top_level << tapring(pdk, enclosed_rectangle = tap_encloses, sdlayer = "p+s/d", horizontal_glayer = tie_layers[0], vertical_glayer = tie_layers[1])
		top_level.add_ports(tie_ref.get_ports_list(), prefix="welltie_")
		try:
			top_level << straight_route(pdk, top_level.ports["A_0_dummy_L_gsdcon_top_met_W"],top_level.ports["welltie_W_top_met_W"],glayer2="met1")
		except KeyError:
			pass
		try:
			end_col = numcols - 1
			port1 = f'B_{end_col}_dummy_R_gdscon_top_met_E'
			top_level << straight_route(pdk, top_level.ports[port1], top_level.ports["welltie_E_top_met_E"], glayer2="met1")
		except KeyError:
			pass
	
	# add a pwell 
	top_level.add_padding(layers = (pdk.get_glayer("pwell"),), default = pdk.get_grule("pwell", "active_tap")["min_enclosure"], )
	top_level = add_ports_perimeter(top_level, layer = pdk.get_glayer("pwell"), prefix="well_")
 
	# add the substrate tap if specified
	if with_substrate_tap:
		subtap_sep = pdk.get_grule("dnwell", "active_tap")["min_separation"]
		subtap_enclosure = (
			2.5 * (subtap_sep + interdigitized_fets.xmax),
			2.5 * (subtap_sep + interdigitized_fets.ymax),
		)
		subtap_ring = top_level << tapring(pdk, enclosed_rectangle = subtap_enclosure, sdlayer = "p+s/d", horizontal_glayer = "met2", vertical_glayer = "met1")
		top_level.add_ports(subtap_ring.get_ports_list(), prefix="substrate_tap_")
  
	top_level.add_ports(source_short.get_ports_list(), prefix='purposegndports')
	
	
	top_level.info['netlist'] = current_mirror_netlist(
		pdk, 
  		width=kwargs.get('width', 3), length=kwargs.get('length', 1), multipliers=numcols, 
    	n_or_p_fet=device,
		subckt_only=True
	)
 
	return top_level