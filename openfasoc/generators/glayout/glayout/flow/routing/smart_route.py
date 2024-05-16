import warnings
from typing import Optional, Union

from gdsfactory import Component, ComponentReference
from gdsfactory.port import Port
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.util.comp_utils import align_comp_to_port, movex
from glayout.flow.pdk.util.port_utils import (
    assert_port_manhattan,
    ports_inline,
    ports_parallel,
)
from glayout.flow.primitives.via_gen import via_stack
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.straight_route import straight_route


def smart_route(
    pdk: MappedPDK,
    edge1: Port,
	edge2: Port,
    ref_comp: Optional[Union[Component, ComponentReference]]=None,
    top_comp: Optional[Union[Component, ComponentReference]]=None,
    **kwargs
) -> Component:
    # error checks
    assert_port_manhattan([edge1,edge2])
    # determine route type based on preconfiged route utils
    if top_comp is not None and ref_comp is not None:
        if ref_comp.info.get("route_genid") is not None:
            try:
                if ref_comp.info["route_genid"] == "two_transistor_interdigitized":
                    return generic_route_two_transistor_interdigitized(pdk, edge1, edge2, top_comp)
                if ref_comp.info["route_genid"] == "four_transistor_interdigitized":
                    return generic_route_four_transistor_interdigitized(pdk, edge1, edge2, top_comp)
                if ref_comp.info["route_genid"] == "common_centroid_ab_ba":
                    return generic_route_ab_ba_common_centroid(pdk, edge1, edge2, top_comp)
            except ValueError:
                warnings.warn("Attempted a specialized smart route, but failed. Now attempting general smart route...")
    # determine route type based on port orientation and distance
    if ports_parallel(edge1,edge2):
        # croute or straightroute
        if ports_inline(edge1,edge2):
            return straight_route(pdk, edge1, edge2, **kwargs)
        else:
            return c_route(pdk, edge1, edge2, **kwargs)
    else:
        return L_route(pdk, edge1, edge2, **kwargs)


# AorB_source,gate,or drain
def parse_port_name(pname: str) -> str:
    """Parse a port name to extract the device (A or B) and pin (source, drain, or gate)
    returning just that (without directions NESW)
    Args:
        pname (str): The port name to get extract device_pin
    Returns:
        str: A string containing the component and pin type separated by an underscore.
    """
    comp = str()
    pin = str()
    for part in pname.split("_"):
        if part=="A" or part=="B":
            comp = part
        if part=="source" or part=="drain" or part=="gate":
            pin=part
    return comp+"_"+pin


def check_route(name1, name2, pin1, pin2) -> bool:
    # check if this routes between the 2 pins
    cond1 = name1==pin1 and name2==pin2
    cond2 = name2==pin1 and name1==pin2
    return cond1 or cond2


def generic_route_two_transistor_interdigitized(
    pdk: MappedPDK,
    edge1: Port,
    edge2: Port,
    top_comp: Union[Component, ComponentReference]
) -> Component:
    def compensate_for_croutes(top_comp, sample_port: Port, LeftSide: bool, extend_to: Port):
        # top_comp is Component to modify, sample_port is a port name for refernce (we dont know what the prefix should be) side is either west (left) or east
        # adds a metal extension and changes the ports to compensate for the fact that there will be a croute on that side
        # extend_to should be the outside port of croute
        basename = sample_port.name.rstrip("NESW").rstrip("_")
        basename = basename.removesuffix("source").removesuffix("drain").removesuffix("gate").rstrip("_")
        basename = basename.removesuffix("A").removesuffix("B")
        direction = "_W" if LeftSide else "_E"
        #import pdb; pdb.set_trace()
        for dev in ["A_","B_"]:
            specbase = basename + dev
            for pin in ["source","drain","gate"]:
                portcorrection = top_comp.ports[specbase+pin+direction+"_private"]
                rt = top_comp << straight_route(pdk, portcorrection, extend_to, glayer2=pdk.layer_to_glayer(portcorrection.layer))
                top_comp.ports[specbase+pin+direction] = rt.ports["route"+direction]
                top_comp.ports[specbase+pin+direction].name = specbase+pin+direction
        # no return (modifies the top_comp)
    def exchange_ports(top_comp, edge: Port, direction: str) -> Port:
        # gives port which is same except a different edge N,E,S,W
        return top_comp.ports[edge.name.rstrip("NESW")+direction+"_private"]
    #glayer1 = pdk.layer_to_glayer(edge1.layer)
    glayer2 = pdk.layer_to_glayer(edge2.layer)
    name1 = parse_port_name(edge1.name)
    name2 = parse_port_name(edge2.name)
    # order names so that A is first (if only one A)
    if "A" in name2 and not("A" in name1):
        name1, name2 = name2, name1
    # trivial routes
    samecomp = any(l in name1 and l in name2 for l in ["A","B"])
    samepin = any(l in name1 and l in name2 for l in ["gate","source","drain"])
    if samecomp and samepin:
        return Component()
    # easy routes 3/15
    straight_route_width = 1 if edge1.width > 1 else edge1.width
    if check_route(name1,name2,"A_source","B_source"):
        edge = edge1 if "B" in edge1.name else edge2
        return align_comp_to_port(via_stack(pdk,"met1",glayer2),exchange_ports(top_comp,edge,"W"),alignment=("r","c"),rtr_comp_ref=False)
    if check_route(name1,name2,"A_gate","B_gate"):
        return straight_route(pdk,exchange_ports(top_comp,edge1,"S"),exchange_ports(top_comp,edge2,"S"),width=straight_route_width)
    if check_route(name1,name2,"A_drain","B_drain"):
        edge = edge1 if "A" in edge1.name else edge2
        return align_comp_to_port(via_stack(pdk,"met1",glayer2),exchange_ports(top_comp,edge,"E"),alignment=("l","c"),rtr_comp_ref=False)
    # easy self routes (A->A or B->B, and source<->drain) 2/15 (5/15)
    if check_route(name1,name2,"A_drain","A_source"):
        edge = edge1 if "drain" in edge1.name else edge2
        return align_comp_to_port(via_stack(pdk,"met1",glayer2),exchange_ports(top_comp,edge,"W"),alignment=("r","c"),rtr_comp_ref=False)
    if check_route(name1,name2,"B_drain","B_source"):
        edge = edge1 if "source" in edge1.name else edge2
        return align_comp_to_port(via_stack(pdk,"met1",glayer2),exchange_ports(top_comp,edge,"E"),alignment=("l","c"),rtr_comp_ref=False)# B is higher
    # hard self route (A->A or B->B, and source or drain -> gate) 4/15 (9/15)
    viaoffset = not(check_route(name1,name2,"A_gate","A_drain") or check_route(name1,name2,"B_gate","B_drain"))
    edge1, edge2 = (edge2, edge1) if ("drain" in edge2.name or "source" in edge2.name) else (edge1, edge2)
    width2 = edge2.width
    if check_route(name1,name2,"A_gate","A_drain") or check_route(name1,name2,"A_gate","A_source"):
        rt = c_route(pdk,exchange_ports(top_comp,edge1,"W"),exchange_ports(top_comp,edge2,"W"),viaoffset=(viaoffset,True),width2=width2) # A gets W
        compensate_for_croutes(top_comp,edge1,True,rt.ports["con_N"])
        return rt
    if check_route(name1,name2,"B_gate","B_drain") or check_route(name1,name2,"B_gate","B_source"):
        rt = c_route(pdk,exchange_ports(top_comp,edge1,"E"),exchange_ports(top_comp,edge2,"E"),viaoffset=(viaoffset,True),width2=width2) # B gets E
        compensate_for_croutes(top_comp,edge1,False,rt.ports["con_N"])
        return rt
    # inter transistor routes going to the gate of A or B   4/15 (13/15)
    if check_route(name1,name2,"A_gate","B_drain") or check_route(name1,name2,"A_gate","B_source"):
        rt = c_route(pdk,exchange_ports(top_comp,edge1,"W"),exchange_ports(top_comp,edge2,"W"),viaoffset=(not(check_route(name1,name2,"A_gate","B_drain")),True),width2=width2) # A_gate gets W
        compensate_for_croutes(top_comp,edge1,True,rt.ports["con_N"])
        return rt
    if check_route(name1,name2,"B_gate","A_drain") or check_route(name1,name2,"B_gate","A_source"):
        rt = c_route(pdk,exchange_ports(top_comp,edge1,"E"),exchange_ports(top_comp,edge2,"E"),viaoffset=(not(check_route(name1,name2,"B_gate","A_drain")),True),width2=width2) # B_gate gets E
        compensate_for_croutes(top_comp,edge1,False,rt.ports["con_N"])
        return rt
    # inter transistor routes going to from s or d to s or d   2/15 (15/15)
    if check_route(name1,name2,"A_source","B_drain"):
        edge = edge1 if "drain" in edge1.name else edge2
        return align_comp_to_port(via_stack(pdk,"met1",glayer2),exchange_ports(top_comp,edge,"W"),alignment=("r","c"),rtr_comp_ref=False)
    if check_route(name1,name2,"A_drain","B_source"):
        edge = edge1 if "drain" in edge1.name else edge2
        return align_comp_to_port(via_stack(pdk,"met1",glayer2),exchange_ports(top_comp,edge,"E"),alignment=("l","c"),rtr_comp_ref=False)
    raise ValueError("You picked a port that smart_route with interdigitized 2 transistor does not support")


def generic_route_four_transistor_interdigitized(
    pdk: MappedPDK,
    edge1: Port,
    edge2: Port,
    top_comp: Union[Component, ComponentReference]
) -> Component:
    def check_port(pname: str) -> bool:
        # check that this is a source, drain, or gate
        # returns false if the port is source drain or gate
        pname = pname.rstrip("NESW_")
        pin = pname.split("_")[-1]
        return not(pin=="source" or pin=="gate" or pin=="drain")
    def strip_portname(pname: str) -> str:
        # removes upto the two transistor interdigitzed stuff
        pname = pname.rstrip("NESW_")
        pname = pname.removesuffix("source").removesuffix("drain").removesuffix("gate")
        pname = pname.rstrip("_").removesuffix("A").removesuffix("B").rstrip("_")
        return pname
    def exchange_ports(top_comp, edge: Port, direction: str) -> Port:
        # gives port which is same except a different edge N,E,S,W
        return top_comp.ports[edge.name.rstrip("NESW")+direction+"_private"]
    def parse_port_name(pname: str) -> str:
        comp = str()
        pin = str()
        topbot = str()
        for part in pname.split("_"):
            if part=="A" or part=="B":
                comp = part
            if part=="source" or part=="drain" or part=="gate":
                pin=part
            if part=="top" or part=="bottom":
                topbot = part
        return topbot+"_"+comp+"_"+pin
    def compensate_for_croutes(top_comp, sample_port: Port, LeftSide: bool, extend_to: Port):
        # top_comp is Component to modify, sample_port is a port name for refernce (we dont know what the prefix should be) side is either west (left) or east
        # adds a metal extension and changes the ports to compensate for the fact that there will be a croute on that side
        # extend_to should be the outside port of croute
        basename = sample_port.name.rstrip("NESW").rstrip("_")
        basename = basename.removesuffix("source").removesuffix("drain").removesuffix("gate").rstrip("_")
        basename = basename.removesuffix("A").removesuffix("B")
        direction = "_W" if LeftSide else "_E"
        #import pdb; pdb.set_trace()
        for dev in ["A_","B_"]:
            specbase = basename + dev
            for pin in ["source","drain","gate"]:
                portcorrection = top_comp.ports[specbase+pin+direction+"_private"]
                rt = top_comp << straight_route(pdk, portcorrection, extend_to, glayer2=pdk.layer_to_glayer(portcorrection.layer))
                top_comp.ports[specbase+pin+direction] = rt.ports["route"+direction]
                top_comp.ports[specbase+pin+direction].name = specbase+pin+direction
    # check that this function supports the ports specified
    cond1 = check_port(edge1.name) or check_port(edge2.name)
    cond2 = strip_portname(edge1.name).split("_")[-1] != strip_portname(edge2.name).split("_")[-1]
    name1 = parse_port_name(edge1.name)
    name2 = parse_port_name(edge2.name)
    width1 = edge1.width
    width2 = edge2.width
    if "A" in name2 and not("A" in name1):
        name1, name2 = name2, name1
    if cond1:
        raise ValueError("You picked a port that smart_route with interdigitized 4 transistor does not support")
    elif cond2:
        # do your code here

        # if check_route("")

        raise ValueError("these ports will be supported soon")
        # print(f'\nname1: {name1}, name2: {name2}\n"top_A_source", "bottom_A_source"\n')
        
        print('\n result of check_route: ', check_route(name1, name2, "top_A_source", "bottom_A_source"))
        if check_route(name1, name2, "top_A_drain", "bottom_A_drain"):
            rt = c_route(pdk, exchange_ports(top_comp, edge1, "W"), exchange_ports(top_comp, edge2, "W"), viaoffset=(True, True), width1=width1, width2=width2)
            compensate_for_croutes(top_comp, edge1, True, rt.ports["con_N"])
            return rt
        if check_route(name1, name2, "top_A_drain", "bottom_A_source"):
            # print('\n\nin second if condition\n\n')
            rt = c_route(pdk, exchange_ports(top_comp, edge1, "W"), exchange_ports(top_comp, edge2, "W"), viaoffset=(True, True), width1=width1, width2=width2)
            compensate_for_croutes(top_comp, edge1, True, rt.ports["con_N"])
            return rt
        if check_route(name1, name2, "top_A_source", "bottom_A_source"):
            # print('\n\nin third if condition\n\n')
            rt = c_route(pdk, exchange_ports(top_comp, edge1, "W"), exchange_ports(top_comp, edge2, "W"), viaoffset=(True, True), width1=width1, width2=width2, extension=4*width1)
            compensate_for_croutes(top_comp, edge1, True, rt.ports["con_N"])
            return rt
        if check_route(name1, name2, "top_A_source", "bottom_A_drain"):
            # print('\n\nin fourth if condition\n\n')
            rt = c_route(pdk, exchange_ports(top_comp, edge1, "W"), exchange_ports(top_comp, edge2, "W"), viaoffset=(True, True), width1=width1, width2=width2, extension=4*width1)
            compensate_for_croutes(top_comp, edge1, True, rt.ports["con_N"])
            return rt
    else:
        # else return 2 tran route
        return generic_route_two_transistor_interdigitized(pdk, edge1, edge2, top_comp)



def generic_route_ab_ba_common_centroid(
    pdk: MappedPDK,
    edge1: Port,
    edge2: Port,
    top_comp: Union[Component, ComponentReference]
) -> Component:
    # TODO: implement
    name1, name2 = parse_port_name(edge1.name), parse_port_name(edge2.name)
    width1 = edge1.width
    # order names so that A is first (if only one A)
    if "A" in name2 and not("A" in name1):
        name1, name2 = name2, name1
    # same device routes (A->A or B->B) (6/15)
    if check_route(name1,name2,"A_source","A_gate"):
        return straight_route(pdk, top_comp.ports["A_source_E_private"],top_comp.ports["A_gate_route_con_N"],via2_alignment=("right","bottom"))
    if check_route(name1,name2,"A_drain","A_gate"):
        return straight_route(pdk, top_comp.ports["A_drain_E_private"],top_comp.ports["A_gate_route_con_N"],via2_alignment=("right","top"))
    if check_route(name1,name2,"A_source","A_drain"):
        straight_route(pdk, top_comp.ports["br_multiplier_0_source_N"],top_comp.ports["br_multiplier_0_drain_S"],width=min(width1,1))
        return straight_route(pdk, top_comp.ports["tl_multiplier_0_source_S"],top_comp.ports["tl_multiplier_0_drain_N"],width=min(width1,1))
    if check_route(name1,name2,"B_source","B_gate"):
        return straight_route(pdk, top_comp.ports["B_source_W_private"],top_comp.ports["B_gate_route_con_N"],via2_alignment=("left","bottom"))
    if check_route(name1,name2,"B_drain","B_gate"):
        return straight_route(pdk, top_comp.ports["B_drain_W_private"],top_comp.ports["B_gate_route_con_N"],via2_alignment=("left","top"))
    if check_route(name1,name2,"B_source","B_drain"):
        top_comp << straight_route(pdk, top_comp.ports["tr_multiplier_0_source_S"],top_comp.ports["tr_multiplier_0_drain_N"],width=min(width1,1))
        return straight_route(pdk, top_comp.ports["bl_multiplier_0_source_N"],top_comp.ports["bl_multiplier_0_drain_S"],width=min(width1,1))
    # A_src/drain->B_gate or B_src/drain->A_gate (4/15)
    if check_route(name1,name2,"A_source","B_gate"):
        return straight_route(pdk, top_comp.ports["A_source_W_private"],top_comp.ports["B_gate_route_con_N"],via2_alignment=("left","top"))
    if check_route(name1,name2,"A_drain","B_gate"):
        return straight_route(pdk, top_comp.ports["A_drain_W_private"],top_comp.ports["B_gate_route_con_N"],via2_alignment=("left","bottom"))
    if check_route(name1,name2,"B_source","A_gate"):
        return straight_route(pdk, top_comp.ports["B_source_E_private"],top_comp.ports["A_gate_route_con_N"],via2_alignment=("right","top"))
    if check_route(name1,name2,"B_drain","A_gate"):
        return straight_route(pdk, top_comp.ports["B_drain_E_private"],top_comp.ports["A_gate_route_con_N"],via2_alignment=("right","bottom"))
    # A_src/drain->B_src or A_src/drain->B_drain (4/15)
    if check_route(name1,name2,"A_source","B_source"):
        return straight_route(pdk, top_comp.ports["tl_multiplier_0_source_E"],top_comp.ports["tr_multiplier_0_source_W"])
    if check_route(name1,name2,"A_drain","B_source"):
        portmv1 = top_comp.ports["tl_multiplier_0_drain_E"].copy()
        return straight_route(pdk, top_comp.ports["tl_multiplier_0_drain_E"],movex(portmv1,2*pdk.get_grule(pdk.layer_to_glayer(portmv1.layer))["min_separation"]))
    if check_route(name1,name2,"A_source","B_drain"):
        portmv1 = top_comp.ports["tr_multiplier_0_drain_W"].copy()
        return straight_route(pdk, top_comp.ports["tr_multiplier_0_drain_W"],movex(portmv1,-2*pdk.get_grule(pdk.layer_to_glayer(portmv1.layer))["min_separation"]))
    if check_route(name1,name2,"A_drain","B_drain"):
        portmv1 = top_comp.ports["bl_mutliplier_0_drain_N"].copy()
        portmv2 = top_comp.ports["br_multiplier_0_drain_N"].copy()
        top_comp << straight_route(pdk, movex(portmv1,-portmv1.width/2), top_comp.ports["tl_multiplier_0_drain_S"],width=width1)
        return straight_route(pdk, movex(portmv2,portmv2.width/2),top_comp.ports["tr_multiplier_0_drain_S"])
    # A_gate -> B_gate (1/15)
    if check_route(name1,name2,"A_gate","B_gate"):
        return straight_route(pdk,top_comp.ports["br_multiplier_0_gate_W"],top_comp.ports["bl_multiplier_0_gate_E"])
    raise ValueError("You picked a port that smart_route with ab_ba_common_centroid does not support")
