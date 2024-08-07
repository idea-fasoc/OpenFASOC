from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.primitives.fet import nmos, pmos
from glayout.flow.primitives.via_gen import via_stack, via_array
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, movex, move, movey, align_comp_to_port, prec_ref_center, center_to_edge_distance
from glayout.flow.pdk.util.port_utils import set_port_orientation, rename_ports_by_orientation, create_private_ports
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.primitives.guardring import tapring
from gdsfactory.components import rectangle
from typing import Union, Optional
from itertools import product

from gdsfactory import Component


def common_centroid_ab_ba(
	pdk: MappedPDK,
	width: float = 3,
	fingers: int = 4,
	length: Optional[float] = None,
	n_or_p_fet: bool = True,
	rmult: int = 1,
	dummy: Union[bool, tuple[bool, bool]] = True,
	substrate_tap: bool=True
) -> Component:
    """create a comcentroid with 2 transistors placed in two rows with common centroid place. Sources are shorted
    width = width of the transistors
    fingers = number of fingers in the transistors (must be 2 or more)
    length = length of the transistors, None or 0 means use min length
    short_source = if true connects source of both transistors
    n_or_p_fet = if true the comcentroid is made of nfets else it is made of pfets
    substrate_tap: if true place a tapring around the comcentroid (connects on met1)
    """
    # TODO: error checking
    pdk.activate()
    comcentroid = Component()
    # create transistors
    well = None
    if isinstance(dummy, bool):
        dummy = (dummy, dummy)
    if n_or_p_fet:
        fetL = nmos(pdk, width=width, fingers=fingers,length=length,multipliers=1,with_tie=False,with_dummy=(dummy[0], False),with_dnwell=False,with_substrate_tap=False,rmult=rmult)
        fetR = nmos(pdk, width=width, fingers=fingers,length=length,multipliers=1,with_tie=False,with_dummy=(False,dummy[1]),with_dnwell=False,with_substrate_tap=False,rmult=rmult)
        well, sdglayer = "pwell", "n+s/d"
    else:
        fetL = pmos(pdk, width=width, fingers=fingers,length=length,multipliers=1,with_tie=False,with_dummy=(dummy[0], False),dnwell=False,with_substrate_tap=False,rmult=rmult)
        fetR = pmos(pdk, width=width, fingers=fingers,length=length,multipliers=1,with_tie=False,with_dummy=(False,dummy[1]),dnwell=False,with_substrate_tap=False,rmult=rmult)
        well, sdglayer = "nwell", "p+s/d"
    fetRdims = evaluate_bbox(fetR.flatten().remove_layers(layers=[pdk.get_glayer(well)]))
    fetLdims = evaluate_bbox(fetL.flatten().remove_layers(layers=[pdk.get_glayer(well)]))
    # place and flip top transistors such that the drains of bottom and top point towards eachother
    a_topl = comcentroid << fetL
    a_topl = rename_ports_by_orientation(a_topl.mirror_y())
    b_topr = comcentroid << fetR
    b_topr = rename_ports_by_orientation(b_topr.mirror_y())
    a_botr = comcentroid << fetR
    b_botl = comcentroid << fetL
    prec_ref_center(a_topl, snapmov2grid=True)
    prec_ref_center(b_topr, snapmov2grid=True)
    prec_ref_center(a_botr, snapmov2grid=True)
    prec_ref_center(b_botl, snapmov2grid=True)
    # setup for routing (need viadims to know how far to seperate transistors)
    glayer1 = pdk.layer_to_glayer(a_topl.ports["multiplier_0_drain_E"].layer)
    glayer2 = glayer1[0:-1] + str(int(glayer1[-1])+1)
    glayer0 = glayer1[0:-1] + str(int(glayer1[-1])-1)
    g1g2via = via_stack(pdk,glayer1,glayer2)
    g0g1via = via_stack(pdk,glayer0,glayer1)
    # move transistors into position
    min_spacing_y = pdk.snap_to_2xgrid(1*(g1g2via.ysize - pdk.get_grule(glayer1)["min_width"])+pdk.get_grule(glayer1)["min_separation"])
    extra_g1g2_spacing = pdk.snap_to_2xgrid(max(pdk.get_grule(glayer2)["min_separation"]-pdk.get_grule(glayer1)["min_separation"],0))
    min_spacing_y += extra_g1g2_spacing
    min_spacing_x = 3*pdk.get_grule(glayer1)["min_separation"] + 2*g0g1via.xsize - 2*pdk.get_grule("active_diff",sdglayer)["min_enclosure"]
    min_spacing_x = pdk.snap_to_2xgrid(max(min_spacing_x, pdk.get_grule(sdglayer)["min_separation"]))
    a_topl.movex(0-fetLdims[0]/2-min_spacing_x/2).movey(pdk.snap_to_2xgrid(fetRdims[1]/2+min_spacing_y/2))
    b_topr.movex(fetLdims[0]/2+min_spacing_x/2).movey(pdk.snap_to_2xgrid(fetLdims[1]/2+min_spacing_y/2))
    a_botr.movex(fetLdims[0]/2+min_spacing_x/2).movey(pdk.snap_to_2xgrid(-fetLdims[1]/2-min_spacing_y/2))
    b_botl.movex(0-fetLdims[0]/2-min_spacing_x/2).movey(pdk.snap_to_2xgrid(-fetLdims[1]/2-min_spacing_y/2))
    comcentroid.add_padding(default=0,layers=[pdk.get_glayer(well)])
    # if substrate tap place substrate tap, and route dummy to substrate tap
    if substrate_tap:
        tapref = comcentroid << tapring(pdk,evaluate_bbox(comcentroid,padding=1))#,horizontal_glayer="met1")
        comcentroid.add_ports(tapref.get_ports_list(),prefix="tap_")
        try:
            comcentroid<<straight_route(pdk,a_topl.ports["multiplier_0_dummy_L_gsdcon_top_met_W"],comcentroid.ports["tap_W_top_met_W"],glayer2="met1")
        except KeyError:
            pass
        try:
            comcentroid<<straight_route(pdk,b_topr.ports["multiplier_0_dummy_R_gsdcon_top_met_W"],comcentroid.ports["tap_E_top_met_E"],glayer2="met1")
        except KeyError:
            pass
        try:
            comcentroid<<straight_route(pdk,b_botl.ports["multiplier_0_dummy_L_gsdcon_top_met_W"],comcentroid.ports["tap_W_top_met_W"],glayer2="met1")
        except KeyError:
            pass
        try:
            comcentroid<<straight_route(pdk,a_botr.ports["multiplier_0_dummy_R_gsdcon_top_met_W"],comcentroid.ports["tap_E_top_met_E"],glayer2="met1")
        except KeyError:
            pass
    # correct pwell place, add ports, flatten, and return
    comcentroid.add_ports(a_topl.get_ports_list(),prefix="tl_")
    comcentroid.add_ports(b_topr.get_ports_list(),prefix="tr_")
    comcentroid.add_ports(b_botl.get_ports_list(),prefix="bl_")
    comcentroid.add_ports(a_botr.get_ports_list(),prefix="br_")
    # route asrc to asrc
    vsrca1 = comcentroid << g1g2via
    vsrca2 = comcentroid << g1g2via
    align_comp_to_port(vsrca1,movey(comcentroid.ports["tl_multiplier_0_drain_W"],-extra_g1g2_spacing),alignment=("right","bottom"))
    align_comp_to_port(vsrca2,movey(comcentroid.ports["br_multiplier_0_drain_W"],extra_g1g2_spacing),alignment=("right","top"))
    comcentroid << L_route(pdk, movey(vsrca1.ports["top_met_W"],extra_g1g2_spacing), vsrca2.ports["top_met_N"])
    # route bsrc to bsrc
    vsrcb1 = comcentroid << g1g2via
    vsrcb2 = comcentroid << g1g2via
    align_comp_to_port(vsrcb1,comcentroid.ports["tr_multiplier_0_drain_E"],alignment=("left","bottom"))
    align_comp_to_port(vsrcb2,comcentroid.ports["bl_multiplier_0_drain_E"],alignment=("left","top"))
    intermediate_port = comcentroid.ports["bl_multiplier_0_source_E"].copy()
    intermediate_port.layer = pdk.get_glayer(pdk.layer_to_glayer(vsrcb1.ports["top_met_E"].layer))
    comcentroid << L_route(pdk, vsrcb1.ports["top_met_S"], intermediate_port)
    comcentroid << L_route(pdk,intermediate_port, vsrcb2.ports["top_met_S"])
    # route adrain to adrain
    vdraina1 = comcentroid << g0g1via # first via
    align_comp_to_port(vdraina1, comcentroid.ports[f"tl_multiplier_0_row0_col{fingers-1}_rightsd_top_met_N"],alignment=("right","top"))
    align_comp_to_port(vdraina1, comcentroid.ports["tl_multiplier_0_drain_E"],alignment=("right","none"))
    vdraina1.movex(pdk.get_grule(glayer1)["min_separation"])
    comcentroid << straight_route(pdk, vdraina1.ports["top_met_W"],comcentroid.ports["tr_multiplier_0_leftsd_top_met_E"],glayer2=glayer1)
    vdraina2 = comcentroid << g0g1via # second via
    align_comp_to_port(vdraina2, comcentroid.ports["tl_multiplier_0_drain_E"],alignment=("right","c"))
    vdraina2.movex(pdk.get_grule(glayer1)["min_separation"])
    vdraina2_mdprt = movex(vdraina2.ports["bottom_met_S"],pdk.get_grule("met2","via1")["min_enclosure"])
    vdraina2_mdprt.width = vdraina2_mdprt.width + 2*pdk.get_grule("met2","via1")["min_enclosure"]
    comcentroid << straight_route(pdk, vdraina2_mdprt, vdraina1.ports["bottom_met_N"])
    comcentroid << L_route(pdk, vdraina2.ports["top_met_N"],comcentroid.ports["bl_multiplier_0_source_E"])
    # route bdrain to bdrain
    vdrainb1 = comcentroid << g0g1via # first via
    align_comp_to_port(vdrainb1, comcentroid.ports["br_multiplier_0_leftsd_top_met_N"],alignment=("left","bottom"))
    align_comp_to_port(vdrainb1, comcentroid.ports["br_multiplier_0_drain_W"],alignment=("left","none"))
    vdrainb1.movex(-pdk.get_grule(glayer1)["min_separation"])
    # TODO: fix slight overhang (both this one and the adrain->bdrain)
    comcentroid << straight_route(pdk, vdrainb1.ports["top_met_W"],comcentroid.ports["br_multiplier_0_leftsd_top_met_E"],glayer2=glayer1)
    vdrainb2 = comcentroid << g0g1via # second via
    align_comp_to_port(vdrainb2, comcentroid.ports["br_multiplier_0_drain_W"],alignment=("left","c"))
    vdrainb2.movex(-pdk.get_grule(glayer1)["min_separation"])
    vdrainb2_mdprt = movex(vdrainb2.ports["bottom_met_N"],-pdk.get_grule("met2","via1")["min_enclosure"])
    vdrainb2_mdprt.width = vdrainb2_mdprt.width + 2*pdk.get_grule("met2","via1")["min_enclosure"]
    comcentroid << straight_route(pdk, vdrainb2_mdprt, vdrainb1.ports["bottom_met_S"])
    comcentroid << L_route(pdk, vdrainb2.ports["top_met_N"],comcentroid.ports["tl_multiplier_0_source_E"])
    # agate to agate
    gate2rt_sep = pdk.get_grule(glayer2)["min_separation"]
    vgatea1 = comcentroid << g1g2via# first via
    align_comp_to_port(vgatea1,comcentroid.ports["tl_multiplier_0_gate_E"],alignment=("right","bottom"))
    vgatea2 = comcentroid << g1g2via# second via
    align_comp_to_port(vgatea2,comcentroid.ports["br_multiplier_0_gate_S"],alignment=("right","bottom"))
    vgatea2.movey(-gate2rt_sep)
    comcentroid << straight_route(pdk, vgatea2.ports["bottom_met_S"], comcentroid.ports["br_multiplier_0_gate_N"])
    g1extension = pdk.util_max_metal_seperation()+pdk.snap_to_2xgrid(comcentroid.ports["tr_multiplier_0_plusdoped_E"].center[0] - vgatea2.ports["top_met_E"].center[0])
    cext1 = comcentroid << c_route(pdk, vgatea2.ports["top_met_E"], vgatea1.ports["top_met_E"], cglayer=glayer2, extension=g1extension)
    comcentroid.add_ports(ports=cext1.get_ports_list(),prefix="A_gate_route_")
    # bgate to bgate
    vgateb1 = comcentroid << g1g2via# first via
    align_comp_to_port(vgateb1,comcentroid.ports["bl_multiplier_0_gate_E"],alignment=("right","top"))
    vgateb2 = comcentroid << g1g2via# second via
    align_comp_to_port(vgateb2,comcentroid.ports["tr_multiplier_0_gate_S"],alignment=("right","top"))
    vgateb2.movey(gate2rt_sep)
    comcentroid << straight_route(pdk, vgateb2.ports["bottom_met_N"], comcentroid.ports["tr_multiplier_0_gate_S"])
    g2extension = pdk.util_max_metal_seperation()+pdk.snap_to_2xgrid(abs(comcentroid.ports["tl_multiplier_0_plusdoped_W"].center[0] - vgateb1.ports["top_met_W"].center[0]))
    cext2 = comcentroid << c_route(pdk, vgateb2.ports["top_met_W"], vgateb1.ports["top_met_W"], cglayer=glayer2, extension=g2extension)
    comcentroid.add_ports(ports=cext2.get_ports_list(),prefix="B_gate_route_")
    # create better toplevel ports
    b_drainENS = comcentroid << straight_route(pdk, comcentroid.ports["tr_multiplier_0_drain_E"], movex(cext1.ports["con_N"],cext2.ports["con_N"].width/2+pdk.util_max_metal_seperation()), glayer2=glayer1)
    a_drainENS = comcentroid << straight_route(pdk, comcentroid.ports["br_multiplier_0_drain_E"], movex(cext1.ports["con_N"],cext2.ports["con_N"].width/2+pdk.util_max_metal_seperation()), glayer2=glayer1)
    b_sourceENS = comcentroid << straight_route(pdk, comcentroid.ports["tr_multiplier_0_source_E"], movex(cext1.ports["con_N"],cext2.ports["con_N"].width/2+pdk.util_max_metal_seperation()), glayer2=glayer1)
    a_sourceENS = comcentroid << straight_route(pdk, comcentroid.ports["br_multiplier_0_source_E"], movex(cext1.ports["con_N"],cext2.ports["con_N"].width/2+pdk.util_max_metal_seperation()), glayer2=glayer1)
    b_drainW = comcentroid << straight_route(pdk, comcentroid.ports["bl_multiplier_0_drain_W"], movex(cext2.ports["con_N"],-cext2.ports["con_N"].width/2-pdk.util_max_metal_seperation()), glayer2=glayer1)
    a_drainW = comcentroid << straight_route(pdk, comcentroid.ports["tl_multiplier_0_drain_W"], movex(cext2.ports["con_N"],-cext2.ports["con_N"].width/2-pdk.util_max_metal_seperation()), glayer2=glayer1)
    b_sourceW = comcentroid << straight_route(pdk, comcentroid.ports["bl_multiplier_0_source_W"], movex(cext2.ports["con_N"],-cext2.ports["con_N"].width/2-pdk.util_max_metal_seperation()), glayer2=glayer1)
    a_sourceW = comcentroid << straight_route(pdk, comcentroid.ports["tl_multiplier_0_source_W"], movex(cext2.ports["con_N"],-cext2.ports["con_N"].width/2-pdk.util_max_metal_seperation()), glayer2=glayer1)
    # add the ports
    def makeNorS(portin, direction: str):
        mdprt = set_port_orientation(movex(portin.copy(),(-1 if portin.name.endswith("E") else 1)*pdk.snap_to_2xgrid(portin.width/2)),direction)
        mdprt.name = (mdprt.name.strip("EW") + direction.strip().capitalize()).removeprefix("route_")
        return movey(mdprt,(1 if direction.endswith("N") else -1)*pdk.snap_to_2xgrid(mdprt.width/2))
    def addENS(topcomp: Component, straightrouteref, device: str, pin: str):
        # device is A or B and pin is source drain or gate
        eastport = straightrouteref.ports["route_E"].copy()
        eastport.name = eastport.name.removeprefix("route_")
        topcomp.add_ports(ports=[eastport,makeNorS(eastport,"N"),makeNorS(eastport,"S")],prefix=device+"_"+pin+"_")
    addENS(comcentroid,b_drainENS,"B","drain")
    addENS(comcentroid,a_drainENS,"A","drain")
    addENS(comcentroid,b_sourceENS,"B","source")
    addENS(comcentroid,a_sourceENS,"A","source")
    def localportrename(portin):
        portin = portin.copy()
        portin.name = portin.name.removeprefix("route_")
        return portin
    comcentroid.add_ports(ports=[localportrename(b_drainW.ports["route_W"])],prefix="B_drain_")
    comcentroid.add_ports(ports=[localportrename(a_drainW.ports["route_W"])],prefix="A_drain_")
    comcentroid.add_ports(ports=[localportrename(b_sourceW.ports["route_W"])],prefix="B_source_")
    comcentroid.add_ports(ports=[localportrename(a_sourceW.ports["route_W"])],prefix="A_source_")
    # better gate routes
    a_gateE = comcentroid << straight_route(pdk, comcentroid.ports["br_multiplier_0_gate_E"], comcentroid.ports["A_drain_E"])
    b_gateE = comcentroid << straight_route(pdk, comcentroid.ports["tr_multiplier_0_gate_E"], comcentroid.ports["A_drain_E"])
    a_gateW = comcentroid << straight_route(pdk, comcentroid.ports["tl_multiplier_0_gate_W"], comcentroid.ports["A_drain_W"])
    b_gateW = comcentroid << straight_route(pdk, comcentroid.ports["bl_multiplier_0_gate_W"], comcentroid.ports["A_drain_W"])
    comcentroid.add_ports(ports=[localportrename(a_gateE.ports["route_E"])],prefix="A_gate_")
    comcentroid.add_ports(ports=[localportrename(b_gateE.ports["route_E"])],prefix="B_gate_")
    comcentroid.add_ports(ports=[localportrename(a_gateW.ports["route_W"])],prefix="A_gate_")
    comcentroid.add_ports(ports=[localportrename(b_gateW.ports["route_W"])],prefix="B_gate_")
    rename_north_portb = vgateb2.ports["top_met_N"].copy()# add B_gate_N
    rename_north_portb.name = "B_gate_N"
    comcentroid.add_ports(ports=[rename_north_portb])
    rename_south_porta = vgatea2.ports["top_met_S"].copy()# add A_gate_S
    rename_south_porta.name = "A_gate_S"
    comcentroid.add_ports(ports=[rename_south_porta])
    rename_south_portb = vgateb1.ports["top_met_S"].copy()# add B_gate_S
    rename_south_portb.name = "B_gate_S"
    comcentroid.add_ports(ports=[rename_south_portb])
    # rename ports and add private ports for smart route
    comcentroid = rename_ports_by_orientation(comcentroid)
    comcentroid.add_ports(create_private_ports(comcentroid,["".join(prtp) for prtp in product(["A_","B_"],["drain","source","gate"])]))
    comcentroid.info["route_genid"]="common_centroid_ab_ba"
    return comcentroid

