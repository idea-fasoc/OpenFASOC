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


def create_interdigitized_fets(pdk: MappedPDK, device: str, numcols: int, with_dummy: bool, **kwargs) -> Component:
    """Creates the interdigitized FET structure.

    Args:
        pdk (MappedPDK): The process design kit to use.
        device (str): 'nfet' or 'pfet'.
        numcols (int): Number of columns for interdigitation.
        with_dummy (bool): Whether to include dummy transistors.
        **kwargs: Keyword arguments passed to `two_nfet_interdigitized` or `two_pfet_interdigitized`.

    Returns:
        Component: The interdigitized FET component.
    """
    if device in ['nmos', 'nfet']:
        return two_nfet_interdigitized(
            pdk,
            numcols=numcols,
            dummy=with_dummy,
            with_substrate_tap=False,
            with_tie=False,
            **kwargs
        )
    
    elif device in ['pmos', 'pfet']:
        return two_pfet_interdigitized(
            pdk,
            numcols=numcols,
            dummy=with_dummy,
            with_substrate_tap=False,
            with_tie=False,
            **kwargs
        )
    else:
        raise ValueError(f"Invalid device type: {device}. Must be 'nfet' or 'pfet'.")


def _route_interdigitized_fets(pdk: MappedPDK, interdigitized_fets: Component) -> Component:
    """Routes the interdigitized FETs to create the current mirror connections.

    Shorts the sources and gates, and connects drain of FET A to the gate short.

    Args:
        interdigitized_fets (Component): The interdigitized FET component.
    Returns:
        Component: The routed interdigitized FET component.
    """
    max_metal_separation = pdk.util_max_metal_seperation()
    extension_length = 3 * max_metal_separation

    # Short source of the fets
    source_short = interdigitized_fets << c_route(
        pdk,
        interdigitized_fets.ports['A_source_E'],
        interdigitized_fets.ports['B_source_E'],
        extension=extension_length,
        viaoffset=False
    )

    # Short gates of the fets
    gate_short = interdigitized_fets << c_route(interdigitated
        pdk,
        interdigitized_fets.ports['A_gate_W'],
        interdigitized_fets.ports['B_gate_W'],
        extension=extension_length,
        viaoffset=False
    )

    # Short gate and drain of the reference (FET A)
    interdigitized_fets << L_route(
        pdk,
        interdigitized_fets.ports['A_drain_W'],
        gate_short.ports['con_N'],
        viaoffset=False,
        fullbottom=False
    )
    return interdigitized_fets  


def _add_well_tie(pdk: MappedPDK, component: Component, interdigitized_fets_bbox, tie_layers: tuple[str, str], numcols: int) -> Component:
    """Adds a well tie (tap ring) to the component.

    Args:
        interdigitized_fets_bbox: Bounding box of the interdigitized FETs to enclose.
        tie_layers (tuple[str,str]): Layers for the tie ring.
        numcols (int): Number of columns (used for port name calculation, fragile).

    Returns:
        Component: The component with the well tie added.
    """
    max_metal_separation = pdk.util_max_metal_seperation()
    tap_sep = max(
        max_metal_separation,
        pdk.get_grule("active_diff", "active_tap")["min_separation"],
    )
    tap_sep += pdk.get_grule("p+s/d", "active_tap")["min_enclosure"]
    tap_encloses = (
        2 * (tap_sep + interdigitized_fets_bbox.xmax),
        2 * (tap_sep + interdigitized_fets_bbox.ymax),
    )
    tie_ref = component << tapring(pdk, enclosed_rectangle=tap_encloses, sdlayer="p+s/d", horizontal_glayer=tie_layers[0], vertical_glayer=tie_layers[1])
    component.add_ports(tie_ref.get_ports_list(), prefix="welltie_")


    try: 
        component << straight_route(pdk, component.ports["fet_A_0_dummy_L_gsdcon_top_met_W"], component.ports["welltie_W_top_met_W"], glayer2="met1")
    except KeyError:
        pass

    try: 
        end_col = numcols - 1
        port1 = f'fet_B_{end_col}_dummy_R_gdscon_top_met_E'
        component << straight_route(pdk, component.ports[port1], component.ports["welltie_E_top_met_E"], glayer2="met1")
    except KeyError:
        pass

    return component 

def _add_substrate_tap(pdk: MappedPDK, component: Component, interdigitized_fets_bbox) -> Component:
    """Adds a substrate tap ring to the component.

    Args:
        component (Component): The component to add the substrate tap to.
    Returns:
        Component: The component with the substrate tap added.
    """
    subtap_sep = pdk.get_grule("dnwell", "active_tap")["min_separation"]
    subtap_enclosure = (
        2.5 * (subtap_sep + interdigitized_fets_bbox.xmax), 
        2.5 * (subtap_sep + interdigitized_fets_bbox.ymax), 
    )
    subtap_ring = component << tapring(pdk, enclosed_rectangle=subtap_enclosure, sdlayer="p+s/d", horizontal_glayer="met2", vertical_glayer="met1")
    component.add_ports(subtap_ring.get_ports_list(), prefix="substrate_tap_")
    return component


def current_mirror(
    pdk: MappedPDK,
    numcols: int = 3,
    device: str = 'nfet',
    with_dummy: bool = True,
    with_substrate_tap: bool = False,
    with_tie: bool = True,
    tie_layers: tuple[str, str] = ("met2", "met1"),
    **kwargs
) -> Component:
    """An instantiable current mirror Component.

    This function creates a current mirror layout based on interdigitized transistors.
    It supports nmos/pfet, dummy transistors, substrate taps, and well ties.

    Args:
        pdk (MappedPDK): The process design kit to use.
        numcols (int): Number of columns of the interdigitized fets.
        device (str): 'nfet' or 'pfet'.
        with_dummy (bool): True to place dummy transistors.
        with_substrate_tap (bool): True to place a substrate tapring.
        with_tie (bool): True to place a well tie ring.
        tie_layers (tuple[str,str], optional): Layers for the well tie ring. Defaults to ("met2","met1").
        **kwargs: Keyword arguments passed to transistor placement functions.

    Returns:
        Component: A current mirror component object.
    """
    top_level = Component("current_mirror")

    # Input validation
    assert device in ['nfet', 'pfet', 'nmos', 'pmos'], f"Invalid device type: {device}"
    assert isinstance(numcols, int) and numcols > 0, f"numcols must be a positive integer, got {numcols}"


    # 1. Create interdigitized FETs
    interdigitized_fets = create_interdigitized_fets(pdk, device, numcols, with_dummy, **kwargs)
    top_level.add_ports(interdigitized_fets.get_ports_list(), prefix="fet_")
    top_level << interdigitized_fets 

    # 2. Route interdigitized FETs
    _route_interdigitized_fets(pdk, interdigitized_fets)


    # 3. Add well tie if requested
    if with_tie:
        _add_well_tie(pdk, top_level, interdigitized_fets.bbox, tie_layers, numcols)

    # 4. Add pwell padding and port
    pwell_enclosure_rule = pdk.get_grule("pwell", "active_tap")["min_enclosure"]
    top_level.add_padding(layers=(pdk.get_glayer("pwell"),), default=pwell_enclosure_rule)
    top_level = add_ports_perimeter(top_level, layer=pdk.get_glayer("pwell"), prefix="well_")


    # 5. Add substrate tap if requested
    if with_substrate_tap:
        _add_substrate_tap(pdk, top_level, interdigitized_fets.bbox)


    # 6. Add purpose ground ports
    top_level.add_ports(interdigitized_fets.ports, prefix='purposegndports') 

    # 7. Add netlist information
    top_level.info['netlist'] = current_mirror_netlist(
        pdk,
        width=kwargs.get('width', 3), length=kwargs.get('length', 1), multipliers=numcols,
        n_or_p_fet=device,
        subckt_only=True
    )

    return top_level
