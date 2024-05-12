from glayout.routing.c_route import c_route
from glayout.routing.L_route import L_route
from glayout.routing.straight_route import straight_route
from glayout.pdk.mappedpdk import MappedPDK
from gdsfactory.port import Port
from gdsfactory import Component, ComponentReference

from typing import Optional, Union
from glayout.pdk.util.port_utils import assert_port_manhattan, ports_parallel, ports_inline
from glayout.primitives.via_gen import via_stack
from glayout.pdk.util.comp_utils import align_comp_to_port
import warnings

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
            except ValueError:
                warnings.warn("attempted a specialized smart route, but failed. Now attempting general smart route")
    # determine route type based on port orientation and distance
    if ports_parallel(edge1,edge2):
        # croute or straightroute
        if ports_inline(edge1,edge2):
            return straight_route(pdk, edge1, edge2, **kwargs)
        else:
            return c_route(pdk, edge1, edge2, **kwargs)
    else:
        return L_route(pdk, edge1, edge2, **kwargs)


def generic_route_two_transistor_interdigitized(
    pdk: MappedPDK,
    edge1: Port,
    edge2: Port,
    top_comp: Union[Component, ComponentReference]
) -> Component:
    def exchange_ports(top_comp, edge: Port, direction: str) -> Port:
        # gives port which is same except a different edge N,E,S,W
        return top_comp.ports[edge.name.rstrip("NESW")+direction]
    #glayer1 = pdk.layer_to_glayer(edge1.layer)
    glayer2 = pdk.layer_to_glayer(edge2.layer)
    def check_route(name1, name2, pin1, pin2) -> bool:
        # check if this routes between the 2 pins
        cond1 = name1==pin1 and name2==pin2
        cond2 = name2==pin1 and name1==pin2
        return cond1 or cond2
    # AorB_source,gate,or drain
    def parse_port_name(pname: str) -> str:
        comp = str()
        pin = str()
        for part in pname.split("_"):
            if part=="A" or part=="B":
                comp = part
            if part=="source" or part=="drain" or part=="gate":
                pin=part
        return comp+"_"+pin
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
    #import pdb;pdb.set_trace()
    straight_route_width = 1 if edge1.width > 1 else edge1.width
    if check_route(name1,name2,"A_gate","B_gate") or check_route(name1,name2,"A_source","B_source") or check_route(name1,name2,"A_drain","B_drain"):
        return straight_route(pdk,edge1,edge2,width=straight_route_width)
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
    if check_route(name1,name2,"A_gate","A_drain") or check_route(name1,name2,"A_gate","A_source"):
        return c_route(pdk,exchange_ports(top_comp,edge1,"W"),exchange_ports(top_comp,edge2,"W"),viaoffset=(viaoffset,True)) # A gets W
    if check_route(name1,name2,"B_gate","B_drain") or check_route(name1,name2,"B_gate","B_source"):
        return c_route(pdk,exchange_ports(top_comp,edge1,"E"),exchange_ports(top_comp,edge2,"E"),viaoffset=(viaoffset,True)) # B gets E
    # inter transistor routes going to the gate of A or B   4/15 (13/15)
    if check_route(name1,name2,"A_gate","B_drain") or check_route(name1,name2,"A_gate","B_source"):
        return c_route(pdk,exchange_ports(top_comp,edge1,"W"),exchange_ports(top_comp,edge2,"W"),viaoffset=(not(check_route(name1,name2,"A_gate","B_drain")),True)) # A_gate gets W
    if check_route(name1,name2,"B_gate","A_drain") or check_route(name1,name2,"B_gate","A_source"):
        return c_route(pdk,exchange_ports(top_comp,edge1,"E"),exchange_ports(top_comp,edge2,"E"),viaoffset=(not(check_route(name1,name2,"B_gate","A_drain")),True)) # B_gate gets E
    # inter transistor routes going to from s or d to s or d   2/15 (15/15)
    if check_route(name1,name2,"A_source","B_drain"):
        edge = edge1 if "drain" in edge1.name else edge2
        return align_comp_to_port(via_stack(pdk,"met1",glayer2),exchange_ports(top_comp,edge,"W"),alignment=("r","c"),rtr_comp_ref=False)
    if check_route(name1,name2,"A_drain","B_source"):
        edge = edge1 if "source" in edge1.name else edge2
        return align_comp_to_port(via_stack(pdk,"met1",glayer2),exchange_ports(top_comp,edge,"W"),alignment=("r","c"),rtr_comp_ref=False)
    raise ValueError("You picked a port that smart_route with interdigitized 2 transistor does not support")