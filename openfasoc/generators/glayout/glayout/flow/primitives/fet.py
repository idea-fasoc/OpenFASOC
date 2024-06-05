from gdsfactory.grid import grid
from gdsfactory.cell import cell
from gdsfactory.component import Component, copy
from gdsfactory.components.rectangle import rectangle
from glayout.flow.pdk.mappedpdk import MappedPDK
from typing import Optional, Union
from glayout.flow.primitives.via_gen import via_array, via_stack
from glayout.flow.primitives.guardring import tapring
from pydantic import validate_arguments
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, to_float, to_decimal, prec_array, prec_center, prec_ref_center, movey, align_comp_to_port
from glayout.flow.pdk.util.port_utils import rename_ports_by_orientation, rename_ports_by_list, add_ports_perimeter, print_ports
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid
from decimal import Decimal
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.spice import Netlist


@validate_arguments
def __gen_fingers_macro(pdk: MappedPDK, rmult: int, fingers: int, length: float, width: float, poly_height: float, sdlayer: str, inter_finger_topmet: str) -> Component:
    """internal use: returns an array of fingers"""
    length = pdk.snap_to_2xgrid(length)
    width = pdk.snap_to_2xgrid(width)
    poly_height = pdk.snap_to_2xgrid(poly_height)
    sizing_ref_viastack = via_stack(pdk, "active_diff", "met1")
    # figure out poly (gate) spacing: s/d metal doesnt overlap transistor, s/d min seperation criteria is met
    sd_viaxdim = rmult*evaluate_bbox(via_stack(pdk, "active_diff", "met1"))[0]
    poly_spacing = 2 * pdk.get_grule("poly", "mcon")["min_separation"] + pdk.get_grule("mcon")["width"]
    poly_spacing = max(sd_viaxdim, poly_spacing)
    met1_minsep = pdk.get_grule("met1")["min_separation"]
    poly_spacing += met1_minsep if length < met1_minsep else 0
    # create a single finger
    finger = Component("finger")
    gate = finger << rectangle(size=(length, poly_height), layer=pdk.get_glayer("poly"), centered=True)
    sd_viaarr = via_array(pdk, "active_diff", "met1", size=(sd_viaxdim, width), minus1=True, lay_bottom=False).copy()
    interfinger_correction = via_array(pdk,"met1",inter_finger_topmet, size=(None, width),lay_every_layer=True, num_vias=(1,None))
    sd_viaarr << interfinger_correction
    sd_viaarr_ref = finger << sd_viaarr
    sd_viaarr_ref.movex((poly_spacing+length) / 2)
    finger.add_ports(gate.get_ports_list(),prefix="gate_")
    finger.add_ports(sd_viaarr_ref.get_ports_list(),prefix="rightsd_")
    # create finger array
    fingerarray = prec_array(finger, columns=fingers, rows=1, spacing=(poly_spacing+length, 1),absolute_spacing=True)
    sd_via_ref_left = fingerarray << sd_viaarr
    sd_via_ref_left.movex(0-(poly_spacing+length)/2)
    fingerarray.add_ports(sd_via_ref_left.get_ports_list(),prefix="leftsd_")
    # center finger array and add ports
    centered_farray = Component()
    fingerarray_ref_center = prec_ref_center(fingerarray)
    centered_farray.add(fingerarray_ref_center)
    centered_farray.add_ports(fingerarray_ref_center.get_ports_list())
    # create diffusion and +doped region
    multiplier = rename_ports_by_orientation(centered_farray)
    diff_extra_enc = 2 * pdk.get_grule("mcon", "active_diff")["min_enclosure"]
    diff_dims =(diff_extra_enc + evaluate_bbox(multiplier)[0], width)
    diff = multiplier << rectangle(size=diff_dims,layer=pdk.get_glayer("active_diff"),centered=True)
    sd_diff_ovhg = pdk.get_grule(sdlayer, "active_diff")["min_enclosure"]
    sdlayer_dims = [dim + 2*sd_diff_ovhg for dim in diff_dims]
    sdlayer_ref = multiplier << rectangle(size=sdlayer_dims, layer=pdk.get_glayer(sdlayer),centered=True)
    multiplier.add_ports(sdlayer_ref.get_ports_list(),prefix="plusdoped_")
    multiplier.add_ports(diff.get_ports_list(),prefix="diff_")
    return component_snap_to_grid(rename_ports_by_orientation(multiplier))

def fet_netlist(
    pdk: MappedPDK,
    circuit_name: str,
    model: str,
    width: float,
    length: float,
    fingers: int,
    multipliers: int,
    with_dummy: Union[bool, tuple[bool, bool]]
) -> Netlist:
     # add spice netlist
    num_dummies = 0
    if with_dummy == False or with_dummy == (False, False):
        num_dummies = 0
    elif with_dummy == (True, False) or with_dummy == (False, True):
        num_dummies = 1
    elif with_dummy == True or with_dummy == (True, True):
        num_dummies = 2

    if length is None:
        length = pdk.get_grule('poly')['min_width']
        
    ltop = length
    wtop = width
    mtop = fingers * multipliers
    dmtop = multipliers
    
    source_netlist=""".subckt {circuit_name} {nodes} """+f'l={ltop} w={wtop} m={mtop} dm={dmtop} '+"""
XMAIN   D G S B {model} l={{l}} w={{w}} m={{m}}"""

    for i in range(num_dummies):
        source_netlist += "\nXDUMMY" + str(i+1) + " B B B B {model} l={{l}} w={{w}} m={{dm}}"

    source_netlist += "\n.ends {circuit_name}"

    return Netlist(
        circuit_name=circuit_name,
        nodes=['D', 'G', 'S', 'B'],
        source_netlist=source_netlist,
        instance_format="X{name} {nodes} {circuit_name} l={length} w={width} m={mult} dm={dummy_mult}",
        parameters={
            'model': model,
            'length': ltop,
            'width': wtop,
            'mult': mtop / 2,
            'dummy_mult': dmtop
        }
    )

# drain is above source
@cell
def multiplier(
    pdk: MappedPDK,
    sdlayer: str,
    width: Optional[float] = 3,
    length: Optional[float] = None,
    fingers: int = 1,
    routing: bool = True,
    inter_finger_topmet: str = "met2",
    dummy: Union[bool, tuple[bool, bool]] = True,
    sd_route_topmet: str = "met2",
    gate_route_topmet: str = "met2",
    rmult: Optional[int]=None,
    sd_rmult: int = 1,
    gate_rmult: int=1,
    interfinger_rmult: int=1,
    sd_route_extension: float = 0,
    gate_route_extension: float = 0,
    dummy_routes: bool=True
) -> Component:
    """Generic poly/sd vias generator
    args:
    pdk = pdk to use
    sdlayer = either p+s/d for pmos or n+s/d for nmos
    width = expands the transistor in the y direction
    length = transitor length (if left None defaults to min length)
    fingers = introduces additional fingers (sharing s/d) of width=width
    routing = true or false, specfies if sd should be connected
    inter_finger_topmet = top metal of the via array laid on the source/drain regions
    ****NOTE: routing metal is layed over the source drain regions regardless of routing option
    dummy = true or false add dummy active/plus doped regions
    sd_rmult = multiplies thickness of sd metal (int only)
    gate_rmult = multiplies gate by adding rows to the gate via array (int only)
    interfinger_rmult = multiplies thickness of source/drain routes between the gates (int only)
    sd_route_extension = float, how far extra to extend the source/drain connections (default=0)
    gate_route_extension = float, how far extra to extend the gate connection (default=0)
    dummy_routes: bool default=True, if true add add vias and short dummy poly,source,drain

    ports (one port for each edge),
    ****NOTE: source is below drain:
    gate_... all edges (top met route of gate connection)
    source_...all edges (top met route of source connections)
    drain_...all edges (top met route of drain connections)
    plusdoped_...all edges (area of p+s/d or n+s/d layer)
    diff_...all edges (diffusion region)
    rowx_coly_...all ports associated with finger array include gate_... and array_ (array includes all ports of the viastacks in the array)
    leftsd_...all ports associated with the left most via array
    dummy_L,R_N,E,S,W ports if dummy_routes=True
    """
    # error checking
    if "+s/d" not in sdlayer:
        raise ValueError("specify + doped region for multiplier")
    if not "met" in sd_route_topmet or not "met" in gate_route_topmet:
        raise ValueError("topmet specified must be metal layer")
    if rmult:
        if rmult<1:
            raise ValueError("rmult must be positive int")
        sd_rmult = rmult
        gate_rmult = 1
        interfinger_rmult = ((rmult-1) or 1)
    if sd_rmult<1 or interfinger_rmult<1 or gate_rmult<1:
        raise ValueError("routing multipliers must be positive int")
    if fingers < 1:
        raise ValueError("number of fingers must be positive int")
    # argument parsing and rule setup
    min_length = pdk.get_grule("poly")["min_width"]
    length = min_length if (length or min_length) <= min_length else length
    length = pdk.snap_to_2xgrid(length)
    min_width = max(min_length, pdk.get_grule("active_diff")["min_width"])
    width = min_width if (width or min_width) <= min_width else width
    width = pdk.snap_to_2xgrid(width)
    poly_height = width + 2 * pdk.get_grule("poly", "active_diff")["overhang"]
    # call finger array
    multiplier = __gen_fingers_macro(pdk, interfinger_rmult, fingers, length, width, poly_height, sdlayer, inter_finger_topmet)
    # route all drains/ gates/ sources
    if routing:
        # place vias, then straight route from top port to via-botmet_N
        sd_N_port = multiplier.ports["leftsd_top_met_N"]
        sdvia = via_stack(pdk, "met1", sd_route_topmet)
        sdmet_hieght = sd_rmult*evaluate_bbox(sdvia)[1]
        sdroute_minsep = pdk.get_grule(sd_route_topmet)["min_separation"]
        sdvia_ports = list()
        for finger in range(fingers+1):
            diff_top_port = movey(sd_N_port,destination=width/2)
            # place sdvia such that metal does not overlap diffusion
            big_extension = sdroute_minsep + sdmet_hieght/2 + sdmet_hieght
            sdvia_extension = big_extension if finger % 2 else sdmet_hieght/2
            sdvia_ref = align_comp_to_port(sdvia,diff_top_port,alignment=('c','t'))
            multiplier.add(sdvia_ref.movey(sdvia_extension + pdk.snap_to_2xgrid(sd_route_extension)))
            multiplier << straight_route(pdk, diff_top_port, sdvia_ref.ports["bottom_met_N"])
            sdvia_ports += [sdvia_ref.ports["top_met_W"], sdvia_ref.ports["top_met_E"]]
            # get the next port (break before this if last iteration because port D.N.E. and num gates=fingers)
            if finger==fingers:
                break
            sd_N_port = multiplier.ports[f"row0_col{finger}_rightsd_top_met_N"]
            # route gates
            gate_S_port = multiplier.ports[f"row0_col{finger}_gate_S"]
            metal_seperation = pdk.util_max_metal_seperation()
            psuedo_Ngateroute = movey(gate_S_port.copy(),0-metal_seperation-gate_route_extension)
            psuedo_Ngateroute.y = pdk.snap_to_2xgrid(psuedo_Ngateroute.y)
            multiplier << straight_route(pdk,gate_S_port,psuedo_Ngateroute)
        # place route met: gate
        gate_width = gate_S_port.center[0] - multiplier.ports["row0_col0_gate_S"].center[0] + gate_S_port.width
        gate = rename_ports_by_list(via_array(pdk,"poly",gate_route_topmet, size=(gate_width,None),num_vias=(None,gate_rmult), no_exception=True, fullbottom=True),[("top_met_","gate_")])
        gate_ref = align_comp_to_port(gate.copy(), psuedo_Ngateroute, alignment=(None,'b'),layer=pdk.get_glayer("poly"))
        multiplier.add(gate_ref)
        # place route met: source, drain
        sd_width = sdvia_ports[-1].center[0] - sdvia_ports[0].center[0]
        sd_route = rectangle(size=(sd_width,sdmet_hieght),layer=pdk.get_glayer(sd_route_topmet),centered=True)
        source = align_comp_to_port(sd_route.copy(), sdvia_ports[0], alignment=(None,'c'))
        drain = align_comp_to_port(sd_route.copy(), sdvia_ports[2], alignment=(None,'c'))
        multiplier.add(source)
        multiplier.add(drain)
        # add ports
        multiplier.add_ports(drain.get_ports_list(), prefix="drain_")
        multiplier.add_ports(source.get_ports_list(), prefix="source_")
        multiplier.add_ports(gate_ref.get_ports_list(prefix="gate_"))
    # create dummy regions
    if isinstance(dummy, bool):
        dummyl = dummyr = dummy
    else:
        dummyl, dummyr = dummy
    if dummyl or dummyr:
        dummy = __gen_fingers_macro(pdk,rmult=interfinger_rmult,fingers=1,length=length,width=width,poly_height=poly_height,sdlayer=sdlayer,inter_finger_topmet="met1")
        dummyvia = dummy << via_stack(pdk,"poly","met1",fullbottom=True)
        align_comp_to_port(dummyvia,dummy.ports["row0_col0_gate_S"],layer=pdk.get_glayer("poly"))
        dummy << L_route(pdk,dummyvia.ports["top_met_W"],dummy.ports["leftsd_top_met_S"])
        dummy << L_route(pdk,dummyvia.ports["top_met_E"],dummy.ports["row0_col0_rightsd_top_met_S"])
        dummy.add_ports(dummyvia.get_ports_list(),prefix="gsdcon_")
        dummy_space = pdk.get_grule(sdlayer)["min_separation"] + dummy.xmax
        sides = list()
        if dummyl:
            sides.append((-1,"dummy_L_"))
        if dummyr:
            sides.append((1,"dummy_R_"))
        for side, name in sides:
            dummy_ref = multiplier << dummy
            dummy_ref.movex(side * (dummy_space + multiplier.xmax))
            multiplier.add_ports(dummy_ref.get_ports_list(),prefix=name)
    # ensure correct port names and return
    return component_snap_to_grid(rename_ports_by_orientation(multiplier))


@validate_arguments
def __mult_array_macro(
    pdk: MappedPDK,
    sdlayer: str,
    width: Optional[float] = 3,
    fingers: Optional[int] = 1,
    multipliers: Optional[int] = 1,
    routing: Optional[bool] = True,
    dummy: Optional[Union[bool, tuple[bool, bool]]] = True,
    length: Optional[float] = None,
    sd_route_topmet: Optional[str] = "met2",
    gate_route_topmet: Optional[str] = "met2",
    sd_route_left: Optional[bool] = True,
    sd_rmult: int = 1,
    gate_rmult: int=1,
    interfinger_rmult: int=1,
    dummy_routes: bool=True
) -> Component:
    """create a multiplier array with multiplier_0 at the bottom
    The array is correctly centered
    """
    # create multiplier array
    pdk.activate()
    # TODO: error checking
    multiplier_arr = Component("temp multiplier array")
    multiplier_comp = multiplier(
        pdk,
        sdlayer,
        width=width,
        fingers=fingers,
        dummy=dummy,
        routing=routing,
        length=length,
        sd_route_topmet=sd_route_topmet,
        gate_route_topmet=gate_route_topmet,
        sd_rmult=sd_rmult,
        gate_rmult=gate_rmult,
        interfinger_rmult=interfinger_rmult,
        dummy_routes=dummy_routes
    )
    _max_metal_seperation_ps = max([pdk.get_grule("met"+str(i))["min_separation"] for i in range(1,5)])
    multiplier_separation = (
        to_decimal(_max_metal_seperation_ps)
        + evaluate_bbox(multiplier_comp, True)[1]
    )
    for rownum in range(multipliers):
        row_displacment = rownum * multiplier_separation - (multiplier_separation/2 * (multipliers-1))
        row_ref = multiplier_arr << multiplier_comp
        row_ref.movey(to_float(row_displacment))
        multiplier_arr.add_ports(
            row_ref.get_ports_list(), prefix="multiplier_" + str(rownum) + "_"
        )
    # TODO: fix extension (both extension are broken. IDK src extension and drain extension IDK metal layer)
    src_extension = to_decimal(0.6)
    drain_extension = src_extension + 3*to_decimal(pdk.get_grule("met4")["min_separation"])
    sd_side = "W" if sd_route_left else "E"
    gate_side = "E" if sd_route_left else "W"
    if routing and multipliers > 1:
        for rownum in range(multipliers-1):
            thismult = "multiplier_" + str(rownum) + "_"
            nextmult = "multiplier_" + str(rownum+1) + "_"
            # route sources left
            srcpfx = thismult + "source_"
            this_src = multiplier_arr.ports[srcpfx+sd_side]
            next_src = multiplier_arr.ports[nextmult + "source_"+sd_side]
            src_ref = multiplier_arr << c_route(pdk, this_src, next_src, viaoffset=(True,False), extension=to_float(src_extension))
            multiplier_arr.add_ports(src_ref.get_ports_list(), prefix=srcpfx)
            # route drains left
            drainpfx = thismult + "drain_"
            this_drain = multiplier_arr.ports[drainpfx+sd_side]
            next_drain = multiplier_arr.ports[nextmult + "drain_"+sd_side]
            drain_ref = multiplier_arr << c_route(pdk, this_drain, next_drain, viaoffset=(True,False), extension=to_float(drain_extension))
            multiplier_arr.add_ports(drain_ref.get_ports_list(), prefix=drainpfx)
            # route gates right
            gatepfx = thismult + "gate_"
            this_gate = multiplier_arr.ports[gatepfx+gate_side]
            next_gate = multiplier_arr.ports[nextmult + "gate_"+gate_side]
            gate_ref = multiplier_arr << c_route(pdk, this_gate, next_gate, viaoffset=(True,False), extension=to_float(src_extension))
            multiplier_arr.add_ports(gate_ref.get_ports_list(), prefix=gatepfx)
    multiplier_arr = component_snap_to_grid(rename_ports_by_orientation(multiplier_arr))
    # add port redirects for shortcut names (source,drain,gate N,E,S,W)
    for pin in ["source","drain","gate"]:
        for side in ["N","E","S","W"]:
            aliasport = pin + "_" + side
            actualport = "multiplier_0_" + aliasport
            multiplier_arr.add_port(port=multiplier_arr.ports[actualport],name=aliasport)
    # recenter
    final_arr = Component()
    marrref = final_arr << multiplier_arr
    correctionxy = prec_center(marrref)
    marrref.movex(correctionxy[0]).movey(correctionxy[1])
    final_arr.add_ports(marrref.get_ports_list())
    return component_snap_to_grid(rename_ports_by_orientation(final_arr))


#@cell
def nmos(
    pdk,
    width: float = 3,
    fingers: Optional[int] = 1,
    multipliers: Optional[int] = 1,
    with_tie: bool = True,
    with_dummy: Union[bool, tuple[bool, bool]] = True,
    with_dnwell: bool = True,
    with_substrate_tap: bool = True,
    length: Optional[float] = None,
    sd_route_topmet: str = "met2",
    gate_route_topmet: str = "met2",
    sd_route_left: bool = True,
    rmult: Optional[int] = None,
    sd_rmult: int=1,
    gate_rmult: int=1,
    interfinger_rmult: int=1,
    tie_layers: tuple[str,str] = ("met2","met1"),
    substrate_tap_layers: tuple[str,str] = ("met2","met1"),
    dummy_routes: bool=True
) -> Component:
    """Generic NMOS generator
    pdk: mapped pdk to use
    width: expands the NMOS in the y direction
    fingers: introduces additional fingers (sharing source/drain) of width=width
    multipliers: number of multipliers (a multiplier is a row of fingers)
    with_tie: true or false, specfies if a bulk tie is required
    with_dummy: tuple(bool,bool) or bool specifying both sides dummy or neither side dummy
    ****using the tuple option, you can specify a single side dummy such as true,false
    with_dnwell: bool use dnwell (multi well)
    with_substrate_tap: add substrate tap on the very outside perimeter of nmos
    length: if None or below min_length will default to min_length
    sd_route_topmet: specify top metal glayer for the source/drain route
    gate_route_topmet: specify top metal glayer for the gate route
    sd_route_left: specify if the source/drain inter-multiplier routes should be on the left side or right side (if false)
    rmult: if not None overrides all other multiplier options to provide a simple routing multiplier (int only)
    sd_rmult: mulitplies the thickness of the source drain route (int only)
    gate_rmult: add additional via rows to the gate route via array (int only)
    interfinger_rmult: multiplies the thickness of the metal routes between the fingers (int only)
    tie_layers: tuple[str,str] specifying (horizontal glayer, vertical glayer) or well tie ring. default=("met2","met1")
    substrate_tap_layers: tuple[str,str] specifying (horizontal glayer, vertical glayer) or substrate tap ring. default=("met2","met1")
    dummy_routes: bool default=True, if true add add vias and short dummy poly,source,drain
    """
    # TODO: glayer checks
    pdk.activate()
    nfet = Component()
    if rmult:
        if rmult<1:
            raise ValueError("rmult must be positive int")
        sd_rmult = rmult
        gate_rmult = 1
        interfinger_rmult = ((rmult-1) or 1)
    # create and add multipliers to nfet
    multiplier_arr = __mult_array_macro(
        pdk,
        "n+s/d",
        width,
        fingers,
        multipliers,
        dummy=with_dummy,
        length=length,
        sd_route_topmet=sd_route_topmet,
        gate_route_topmet=gate_route_topmet,
        sd_route_left=sd_route_left,
        sd_rmult=sd_rmult,
        gate_rmult=gate_rmult,
        interfinger_rmult=interfinger_rmult,
        dummy_routes=dummy_routes
    )
    multiplier_arr_ref = multiplier_arr.ref()
    nfet.add(multiplier_arr_ref)
    nfet.add_ports(multiplier_arr_ref.get_ports_list())
    # add tie if tie
    if with_tie:
        tap_separation = max(
            pdk.util_max_metal_seperation(),
            pdk.get_grule("active_diff", "active_tap")["min_separation"],
        )
        tap_separation += pdk.get_grule("p+s/d", "active_tap")["min_enclosure"]
        tap_encloses = (
            2 * (tap_separation + nfet.xmax),
            2 * (tap_separation + nfet.ymax),
        )
        tiering_ref = nfet << tapring(
            pdk,
            enclosed_rectangle=tap_encloses,
            sdlayer="p+s/d",
            horizontal_glayer=tie_layers[0],
            vertical_glayer=tie_layers[1],
        )
        nfet.add_ports(tiering_ref.get_ports_list(), prefix="tie_")
        for row in range(multipliers):
            for dummyside,tieside in [("L","W"),("R","E")]:
                try:
                    nfet<<straight_route(pdk,nfet.ports[f"multiplier_{row}_dummy_{dummyside}_gsdcon_top_met_W"],nfet.ports[f"tie_{tieside}_top_met_{tieside}"],glayer2="met1")
                except KeyError:
                    pass
    # add pwell
    nfet.add_padding(
        layers=(pdk.get_glayer("pwell"),),
        default=pdk.get_grule("pwell", "active_tap")["min_enclosure"],
    )
    nfet = add_ports_perimeter(nfet,layer=pdk.get_glayer("pwell"),prefix="well_")
    # add dnwell if dnwell
    if with_dnwell:
        nfet.add_padding(
            layers=(pdk.get_glayer("dnwell"),),
            default=pdk.get_grule("pwell", "dnwell")["min_enclosure"],
        )
    # add substrate tap if with_substrate_tap
    if with_substrate_tap:
        substrate_tap_separation = pdk.get_grule("dnwell", "active_tap")[
            "min_separation"
        ]
        substrate_tap_encloses = (
            2 * (substrate_tap_separation + nfet.xmax),
            2 * (substrate_tap_separation + nfet.ymax),
        )
        ringtoadd = tapring(
            pdk,
            enclosed_rectangle=substrate_tap_encloses,
            sdlayer="p+s/d",
            horizontal_glayer=substrate_tap_layers[0],
            vertical_glayer=substrate_tap_layers[1],
        )
        tapring_ref = nfet << ringtoadd
        nfet.add_ports(tapring_ref.get_ports_list(),prefix="guardring_")

    component = rename_ports_by_orientation(nfet).flatten()

    component.info['netlist'] = fet_netlist(
        pdk,
        circuit_name="NMOS",
        model=pdk.models['nfet'],
        width=width,
        length=length,
        fingers=fingers,
        multipliers=multipliers,
        with_dummy=with_dummy
    )

    return component


#@cell
def pmos(
    pdk,
    width: float = 3,
    fingers: Optional[int] = 1,
    multipliers: Optional[int] = 1,
    with_tie: Optional[bool] = True,
    dnwell: Optional[bool] = False,
    with_dummy: Optional[Union[bool, tuple[bool, bool]]] = True,
    with_substrate_tap: Optional[bool] = True,
    length: Optional[float] = None,
    sd_route_topmet: Optional[str] = "met2",
    gate_route_topmet: Optional[str] = "met2",
    sd_route_left: Optional[bool] = True,
    rmult: Optional[int] = None,
    sd_rmult: int=1,
    gate_rmult: int=1,
    interfinger_rmult: int=1,
    tie_layers: tuple[str,str] = ("met2","met1"),
    substrate_tap_layers: tuple[str,str] = ("met2","met1"),
    dummy_routes: bool=True
) -> Component:
    """Generic PMOS generator
    pdk: mapped pdk to use
    width: expands the PMOS in the y direction
    fingers: introduces additional fingers (sharing source/drain) of width=width
    multipliers: number of multipliers (a multiplier is a row of fingers)
    with_tie: true or false, specfies if a bulk tie is required
    dnwell: bool use dnwell if True, or use nwell if False
    with_dummy: tuple(bool,bool) or bool specifying both sides dummy or neither side dummy
    ****using the tuple option, you can specify a single side dummy such as true,false
    with_substrate_tap: add substrate tap on the very outside perimeter of pmos
    length: if None or below min_length will default to min_length
    sd_route_topmet: specify top metal glayer for the source/drain route
    gate_route_topmet: specify top metal glayer for the gate route
    sd_route_left: specify if the source/drain inter-multiplier routes should be on the left side or right side (if false)
    rmult: if not None overrides all other multiplier options to provide a simple routing multiplier (int only)
    sd_rmult: mulitplies the thickness of the source drain route (int only)
    gate_rmult: add additional via rows to the gate route via array (int only)
    interfinger_rmult: multiplies the thickness of the metal routes between the fingers (int only)
    tie_layers: tuple[str,str] specifying (horizontal glayer, vertical glayer) or well tie ring. default=("met2","met1")
    substrate_tap_layers: tuple[str,str] specifying (horizontal glayer, vertical glayer) or substrate tap ring. default=("met2","met1")
    dummy_routes: bool default=True, if true add add vias and short dummy poly,source,drain
    """
    # TODO: glayer checks
    pdk.activate()
    pfet = Component()
    if rmult:
        if rmult<1:
            raise ValueError("rmult must be positive int")
        sd_rmult = rmult
        gate_rmult = 1
        interfinger_rmult = ((rmult-1) or 1)
    # create and add multipliers to nfet
    multiplier_arr = __mult_array_macro(
        pdk,
        "p+s/d",
        width,
        fingers,
        multipliers,
        dummy=with_dummy,
        length=length,
        sd_route_topmet=sd_route_topmet,
        gate_route_topmet=gate_route_topmet,
        sd_route_left=sd_route_left,
        gate_rmult=gate_rmult,
        interfinger_rmult=interfinger_rmult,
        sd_rmult=sd_rmult,
        dummy_routes=dummy_routes
    )
    multiplier_arr_ref = multiplier_arr.ref()
    pfet.add(multiplier_arr_ref)
    pfet.add_ports(multiplier_arr_ref.get_ports_list())
    # add tie if tie
    if with_tie:
        tap_separation = max(
            pdk.get_grule("met2")["min_separation"],
            pdk.get_grule("met1")["min_separation"],
            pdk.get_grule("active_diff", "active_tap")["min_separation"],
        )
        tap_separation += pdk.get_grule("n+s/d", "active_tap")["min_enclosure"]
        tap_encloses = (
            2 * (tap_separation + pfet.xmax),
            2 * (tap_separation + pfet.ymax),
        )
        tapring_ref = pfet << tapring(
            pdk,
            enclosed_rectangle=tap_encloses,
            sdlayer="n+s/d",
            horizontal_glayer=tie_layers[0],
            vertical_glayer=tie_layers[1],
        )
        pfet.add_ports(tapring_ref.get_ports_list(),prefix="tie_")
        for row in range(multipliers):
            for dummyside,tieside in [("L","W"),("R","E")]:
                try:
                    pfet<<straight_route(pdk,pfet.ports[f"multiplier_{row}_dummy_{dummyside}_gsdcon_top_met_W"],pfet.ports[f"tie_{tieside}_top_met_{tieside}"],glayer2="met1")
                except KeyError:
                    pass
    # add nwell
    nwell_glayer = "dnwell" if dnwell else "nwell"
    pfet.add_padding(
        layers=(pdk.get_glayer(nwell_glayer),),
        default=pdk.get_grule("active_tap", nwell_glayer)["min_enclosure"],
    )
    pfet = add_ports_perimeter(pfet,layer=pdk.get_glayer(nwell_glayer),prefix="well_")
    # add substrate tap if with_substrate_tap
    if with_substrate_tap:
        substrate_tap_separation = pdk.get_grule("dnwell", "active_tap")[
            "min_separation"
        ]
        substrate_tap_encloses = (
            2 * (substrate_tap_separation + pfet.xmax),
            2 * (substrate_tap_separation + pfet.ymax),
        )
        pfet << tapring(
            pdk,
            enclosed_rectangle=substrate_tap_encloses,
            sdlayer="p+s/d",
            horizontal_glayer=substrate_tap_layers[0],
            vertical_glayer=substrate_tap_layers[1],
        )
    component =  rename_ports_by_orientation(pfet).flatten()

    component.info['netlist'] = fet_netlist(
        pdk,
        circuit_name="PMOS",
        model=pdk.models['pfet'],
        width=width,
        length=length,
        fingers=fingers,
        multipliers=multipliers,
        with_dummy=with_dummy
    )

    return component


