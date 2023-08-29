from gdsfactory.cell import cell, clear_cache
from gdsfactory.component import Component, copy
from gdsfactory.component_reference import ComponentReference
from gdsfactory.components.rectangle import rectangle
from pygen.pdk.mappedpdk import MappedPDK
from typing import Optional, Union
from pygen.fet import nmos, pmos, multiplier
from pygen.diff_pair import diff_pair
from pygen.guardring import tapring
from pygen.mimcap import mimcap_array, mimcap
from pygen.routing.L_route import L_route
from pygen.routing.c_route import c_route
from pygen.via_gen import via_stack, via_array
from gdsfactory.routing.route_quad import route_quad
from pygen.pdk.util.comp_utils import evaluate_bbox, prec_ref_center, movex, movey, to_decimal, to_float, move, align_comp_to_port, get_padding_points_cc
from pygen.pdk.util.port_utils import rename_ports_by_orientation, rename_ports_by_list, add_ports_perimeter, print_ports, set_port_orientation, rename_component_ports
from pygen.routing.straight_route import straight_route
from pygen.pdk.util.snap_to_grid import component_snap_to_grid
from pydantic import validate_arguments
from pygen.common.two_transistor_interdigitized import two_nfet_interdigitized




@validate_arguments
def __add_diff_pair_and_bias(pdk: MappedPDK, opamp_top: Component, diffpair_params: tuple[float, float, int], diffpair_bias: tuple[float, float, int], rmult: int) -> Component:
    # create and center diffpair
    diffpair_i_ = Component("temp diffpair and current source")
    center_diffpair_comp = diff_pair(
        pdk,
        width=diffpair_params[0],
        length=diffpair_params[1],
        fingers=diffpair_params[2],
        rmult=rmult
    )
    diffpair_i_.add(prec_ref_center(center_diffpair_comp))
    diffpair_i_.add_ports(center_diffpair_comp.get_ports_list())
    # create and position tail current source
    cmirror = two_nfet_interdigitized(
        pdk,
        width=diffpair_bias[0],
        length=diffpair_bias[1],
        numcols=diffpair_bias[2],
        with_tie=False,
        with_substrate_tap=False,
        gate_route_topmet="met3",
        sd_route_topmet="met3",
        rmult=rmult
    )
    # cmirror routing
    metal_sep = pdk.util_max_metal_seperation()
    gate_short = cmirror << c_route(pdk, cmirror.ports["A_gate_E"],cmirror.ports["B_gate_E"],extension=3*metal_sep,viaoffset=None)
    cmirror << L_route(pdk, gate_short.ports["con_N"],cmirror.ports["A_drain_E"],viaoffset=False,fullbottom=False)
    srcshort = cmirror << c_route(pdk, cmirror.ports["A_source_W"],cmirror.ports["B_source_W"],extension=metal_sep,viaoffset=False)
    cmirror.add_ports(srcshort.get_ports_list(),prefix="purposegndports")
    # add cmirror
    tailcurrent_ref = diffpair_i_ << cmirror
    tailcurrent_ref.movey(
        -0.5 * (center_diffpair_comp.ymax - center_diffpair_comp.ymin)
        - abs(tailcurrent_ref.ymax) - metal_sep
    )
    purposegndPort = tailcurrent_ref.ports["purposegndportscon_S"].copy()
    purposegndPort.name = "ibias_purposegndport"
    diffpair_i_.add_ports([purposegndPort])
    diffpair_i_.add_ports(tailcurrent_ref.get_ports_list(), prefix="ibias_")
    diffpair_i_ref = prec_ref_center(diffpair_i_)
    opamp_top.add(diffpair_i_ref)
    opamp_top.add_ports(diffpair_i_ref.get_ports_list(),prefix="diffpair_")
    return opamp_top

@validate_arguments
def __add_common_source_nbias_transistors(pdk: MappedPDK, opamp_top: Component, half_common_source_nbias: tuple[float, float, int, int], rmult: int) -> Component:
    # create each half of the nmos bias transistor for the common source stage and place them
    x_dim_center = opamp_top.xmax
    for i in range(2):
        cmirror_output = nmos(
            pdk,
            width=half_common_source_nbias[0],
            length=half_common_source_nbias[1],
            fingers=half_common_source_nbias[2],
            multipliers=half_common_source_nbias[3],
            with_tie=True,
            with_dnwell=False,
            with_substrate_tap=False,
            with_dummy=True,
            sd_route_left = bool(i),
            rmult=rmult
        )
        cmirrorref = nmos(
            pdk,
            width=half_common_source_nbias[0],
            length=half_common_source_nbias[1],
            fingers=half_common_source_nbias[2],
            multipliers=1,
            with_tie=True,
            with_dnwell=False,
            with_substrate_tap=False,
            with_dummy=True,
            sd_route_left = bool(i),
            rmult=rmult
        )
        cmirrorref_ref = cmirrorref.ref_center()
        cmirrorout_ref = cmirror_output.ref_center()
        # xtranslation
        direction = (-1) ** i
        xtranslationO = direction * abs(x_dim_center + cmirrorout_ref.xmax + pdk.util_max_metal_seperation())
        xtranslationR = direction * abs(x_dim_center + cmirrorref_ref.xmax + pdk.util_max_metal_seperation())
        xtranslationO, xtranslationR = pdk.snap_to_2xgrid([xtranslationO, xtranslationR])
        cmirrorout_ref.movex(xtranslationO)
        cmirrorref_ref.movex(xtranslationR)
        # ytranslation
        cmirrorout_ref.movey(opamp_top.ports["diffpair_bl_multiplier_0_gate_S"].center[1])
        cmirrorref_ref.movey(cmirrorout_ref.ymin - evaluate_bbox(cmirrorref_ref)[1]/2 - pdk.util_max_metal_seperation())
        # add ports
        opamp_top.add(cmirrorref_ref)
        opamp_top.add(cmirrorout_ref)
        side = "R" if i==0 else "L"
        opamp_top.add_ports(cmirrorout_ref.get_ports_list(), prefix="commonsource_cmirror_output_"+side+"_")
        opamp_top.add_ports(cmirrorref_ref.get_ports_list(), prefix="commonsource_cmirror_ref_"+side+"_")
        opamp_top << straight_route(pdk, opamp_top.ports["commonsource_cmirror_output_"+side+"_tie_S_top_met_S"], opamp_top.ports["commonsource_cmirror_ref_"+side+"_tie_N_top_met_N"],width=2)
    return opamp_top

@validate_arguments
def __route_bottom_ncomps_except_drain_nbias(pdk: MappedPDK, opamp_top: Component, gndpin: Union[Component,ComponentReference], halfmultn_num_mults: int) -> tuple:
    # route diff pair cmirror
    opamp_top << L_route(pdk, opamp_top.ports["diffpair_ibias_purposegndport"],gndpin.ports["e1"])
    # common source
    # route to gnd the sources of cmirror
    _cref = opamp_top << c_route(pdk, opamp_top.ports["commonsource_cmirror_output_R_multiplier_0_source_con_S"], opamp_top.ports["commonsource_cmirror_output_L_multiplier_0_source_con_S"], extension=abs(gndpin.ports["e2"].center[1]-opamp_top.ports["commonsource_cmirror_output_R_multiplier_0_source_con_S"].center[1]),fullbottom=True)
    opamp_top << straight_route(pdk, opamp_top.ports["commonsource_cmirror_ref_R_multiplier_0_source_E"],_cref.ports["con_E"],glayer2="met3",via2_alignment=('c','c'))
    opamp_top << straight_route(pdk, opamp_top.ports["commonsource_cmirror_ref_L_multiplier_0_source_W"],_cref.ports["con_W"],glayer2="met3",via2_alignment=('c','c'))
    # connect cmirror ref drain to cmirror output gate, then short cmirror ref drain and gate
    Ldrainport = opamp_top.ports["commonsource_cmirror_ref_L_multiplier_0_drain_W"]
    Lgateport = opamp_top.ports["commonsource_cmirror_output_L_multiplier_0_gate_W"]
    Rdrainport = opamp_top.ports["commonsource_cmirror_ref_R_multiplier_0_drain_E"]
    Rgateport = opamp_top.ports["commonsource_cmirror_output_R_multiplier_0_gate_E"]
    extension = max(abs(opamp_top.xmin-Ldrainport.center[0]),abs(opamp_top.xmin-Lgateport.center[0])) + 2*pdk.util_max_metal_seperation()
    draintogate_L = opamp_top << c_route(pdk, Ldrainport, Lgateport, extension=extension, width2=Lgateport.width)
    draintogate_R = opamp_top << c_route(pdk, Rdrainport, Rgateport, extension=extension, width2=Rgateport.width)
    Lcmirrorrefgate = opamp_top.ports["commonsource_cmirror_ref_L_multiplier_0_gate_W"]
    Rcmirrorrefgate = opamp_top.ports["commonsource_cmirror_ref_R_multiplier_0_gate_E"]
    opamp_top << L_route(pdk, Lcmirrorrefgate, draintogate_L.ports["con_S"])
    opamp_top << L_route(pdk, Rcmirrorrefgate, draintogate_R.ports["con_S"])
    # connect gates and drains of cmirror output
    halfMultn_left_gate_port = opamp_top.ports["commonsource_cmirror_output_R_multiplier_"+str(halfmultn_num_mults-2)+"_gate_con_N"]
    halfMultn_right_gate_port = opamp_top.ports["commonsource_cmirror_output_L_multiplier_"+str(halfmultn_num_mults-2)+"_gate_con_N"]
    halfmultn_gate_routeref = opamp_top << c_route(pdk, halfMultn_left_gate_port, halfMultn_right_gate_port, extension=abs(opamp_top.ymax-halfMultn_left_gate_port.center[1])+1,fullbottom=True, viaoffset=(False,False))
    halfMultn_left_drain_port = opamp_top.ports["commonsource_cmirror_output_R_multiplier_"+str(halfmultn_num_mults-2)+"_drain_con_N"]
    halfMultn_right_drain_port = opamp_top.ports["commonsource_cmirror_output_L_multiplier_"+str(halfmultn_num_mults-2)+"_drain_con_N"]
    halfmultn_drain_routeref = opamp_top << c_route(pdk, halfMultn_left_drain_port, halfMultn_right_drain_port, extension=abs(opamp_top.ymax-halfMultn_left_drain_port.center[1])+1,fullbottom=True)
    # route to gnd the guardring of cmirror output
    opamp_top << straight_route(pdk,opamp_top.ports["commonsource_cmirror_ref_R_tie_S_top_met_S"],movey(gndpin.ports["e1"],evaluate_bbox(gndpin)[1]/4),width=2,glayer1="met3",fullbottom=True)
    opamp_top << straight_route(pdk,opamp_top.ports["commonsource_cmirror_ref_L_tie_S_top_met_S"],movey(gndpin.ports["e3"],evaluate_bbox(gndpin)[1]/4),width=2,glayer1="met3",fullbottom=True)
    # diffpair
    # route source of diffpair to drain of diffpair cmirror
    opamp_top << L_route(pdk,opamp_top.ports["diffpair_source_routeW_con_N"],opamp_top.ports["diffpair_ibias_B_drain_W"])
    opamp_top << L_route(pdk,opamp_top.ports["diffpair_source_routeE_con_N"],opamp_top.ports["diffpair_ibias_B_drain_E"])
    return opamp_top, halfmultn_drain_routeref, halfmultn_gate_routeref, _cref



@validate_arguments
def __create_sharedgatecomps(pdk: MappedPDK, rmult: int) -> tuple:
    # add diffpair current mirror loads (this is a pmos current mirror split into 2 for better matching/compensation)
    shared_gate_comps = Component("shared gate components")
    # create the 2*2 multiplier transistors (placed twice later)
    twomultpcomps = Component("2 multiplier shared gate comps")
    pcompR = multiplier(pdk, "p+s/d", width=6, length=1, fingers=6, dummy=(False, True),rmult=rmult)
    pcompL = multiplier(pdk, "p+s/d", width=6, length=1, fingers=6, dummy=(True, False),rmult=rmult)
    pcomp_AB_spacing = max(2*pdk.util_max_metal_seperation() + 6*pdk.get_grule("met4")["min_width"],pdk.get_grule("p+s/d")["min_separation"])
    _prefL = (twomultpcomps << pcompL).movex(-1 * pcompL.xmax - pcomp_AB_spacing/2)
    _prefR = (twomultpcomps << pcompR).movex(-1 * pcompR.xmin + pcomp_AB_spacing/2)
    twomultpcomps.add_ports(_prefL.get_ports_list(),prefix="L_")
    twomultpcomps.add_ports(_prefR.get_ports_list(),prefix="R_")
    twomultpcomps << route_quad(_prefL.ports["gate_W"], _prefR.ports["gate_E"], layer=pdk.get_glayer("met2"))
    # center
    relative_dim_comp = multiplier(
        pdk, "p+s/d", width=6, length=1, fingers=4, dummy=False, rmult=rmult
    )
    # TODO: figure out single dim spacing rule then delete both test delete and this
    single_dim = to_decimal(relative_dim_comp.xmax) + to_decimal(0.1)
    LRplusdopedPorts = list()
    LRgatePorts = list()
    LRdrainsPorts = list()
    LRsourcesPorts = list()
    for i in [-2, -1, 1, 2]:
        dummy = False
        extra_t = 0
        if i == -2:
            dummy = [True, False]
            pcenterfourunits = multiplier(
                pdk, "p+s/d", width=6, length=1, fingers=4, dummy=dummy, rmult=rmult
            )
            extra_t = -1 * single_dim
        elif i == 2:
            dummy = [False, True]
            pcenterfourunits = multiplier(
                pdk, "p+s/d", width=6, length=1, fingers=4, dummy=dummy, rmult=rmult
            )
            extra_t = single_dim
        else:
            pcenterfourunits = relative_dim_comp
        pref_ = (shared_gate_comps << pcenterfourunits).movex(to_float(i * single_dim + extra_t))
        LRplusdopedPorts += [pref_.ports["plusdoped_W"] , pref_.ports["plusdoped_E"]]
        LRgatePorts += [pref_.ports["gate_W"],pref_.ports["gate_E"]]
        LRdrainsPorts += [pref_.ports["source_W"],pref_.ports["source_E"]]
        LRsourcesPorts += [pref_.ports["drain_W"],pref_.ports["drain_E"]]
    # combine the two multiplier top and bottom with the 4 multiplier center row
    ytranslation_pcenter = 2 * pcenterfourunits.ymax + 5*pdk.util_max_metal_seperation()
    ptop_AB = (shared_gate_comps << twomultpcomps).movey(ytranslation_pcenter)
    pbottom_AB = (shared_gate_comps << twomultpcomps).movey(-1 * ytranslation_pcenter)
    return shared_gate_comps, ptop_AB, pbottom_AB, LRplusdopedPorts, LRgatePorts, LRdrainsPorts, LRsourcesPorts

def __route_sharedgatecomps(pdk: MappedPDK, shared_gate_comps, via_location, ptop_AB, pbottom_AB, LRplusdopedPorts, LRgatePorts, LRdrainsPorts, LRsourcesPorts) -> Component:
    _max_metal_seperation_ps = pdk.util_max_metal_seperation()
    # connect p+s/d layer of the transistors
    shared_gate_comps << route_quad(LRplusdopedPorts[0],LRplusdopedPorts[-1],layer=pdk.get_glayer("p+s/d"))
    # connect drain of the left 2 and right 2, short sources of all 4
    shared_gate_comps << route_quad(LRdrainsPorts[0],LRdrainsPorts[3],layer=LRdrainsPorts[0].layer)
    shared_gate_comps << route_quad(LRdrainsPorts[4],LRdrainsPorts[7],layer=LRdrainsPorts[0].layer)
    shared_gate_comps << route_quad(LRsourcesPorts[0],LRsourcesPorts[-1],layer=LRsourcesPorts[0].layer)
    pcomps_2L_2R_sourcevia = shared_gate_comps << via_stack(pdk,pdk.layer_to_glayer(LRsourcesPorts[0].layer), "met4")
    pcomps_2L_2R_sourcevia.movey(evaluate_bbox(pcomps_2L_2R_sourcevia.parent.extract(layers=[LRsourcesPorts[0].layer,]))[1]/2 + LRsourcesPorts[0].center[1])
    shared_gate_comps.add_ports(pcomps_2L_2R_sourcevia.get_ports_list(),prefix="2L2Rsrcvia_")
    # short all the gates
    shared_gate_comps << route_quad(LRgatePorts[0],LRgatePorts[-1],layer=pdk.get_glayer("met2"))
    shared_gate_comps.add_ports(ptop_AB.get_ports_list(),prefix="ptopAB_")
    shared_gate_comps.add_ports(pbottom_AB.get_ports_list(),prefix="pbottomAB_")
    # short all gates of shared_gate_comps
    pcenter_gate_route_extension = shared_gate_comps.xmax - min(ptop_AB.ports["R_gate_E"].center[0], LRgatePorts[-1].center[0]) - pdk.get_grule("active_diff")["min_width"]
    pcenter_l_croute = shared_gate_comps << c_route(pdk, ptop_AB.ports["L_gate_W"], pbottom_AB.ports["L_gate_W"],extension=pcenter_gate_route_extension)
    pcenter_r_croute = shared_gate_comps << c_route(pdk, ptop_AB.ports["R_gate_E"], pbottom_AB.ports["R_gate_E"],extension=pcenter_gate_route_extension)
    shared_gate_comps << straight_route(pdk, LRgatePorts[0], pcenter_l_croute.ports["con_N"])
    shared_gate_comps << straight_route(pdk, LRgatePorts[-1], pcenter_r_croute.ports["con_N"])
    # connect drain of A to the shorted gates
    shared_gate_comps << L_route(pdk,ptop_AB.ports["L_source_W"],pcenter_l_croute.ports["con_N"])
    shared_gate_comps << straight_route(pdk,pbottom_AB.ports["R_source_E"],pcenter_r_croute.ports["con_N"])
    # connect source of A to the drain of 2L
    pcomps_route_A_drain_extension = shared_gate_comps.xmax-max(ptop_AB.ports["R_drain_E"].center[0], LRdrainsPorts[-1].center[0])+_max_metal_seperation_ps
    pcomps_route_A_drain = shared_gate_comps << c_route(pdk, ptop_AB.ports["L_drain_W"], LRdrainsPorts[0], extension=pcomps_route_A_drain_extension)
    row_rectangle_routing = rectangle(layer=ptop_AB.ports["L_drain_W"].layer,size=(pbottom_AB.ports["R_source_N"].width,pbottom_AB.ports["R_source_W"].width)).copy()
    Aextra_top_connection = align_comp_to_port(row_rectangle_routing, pbottom_AB.ports["R_source_N"], ('c','t')).movey(row_rectangle_routing.ymax + _max_metal_seperation_ps)
    shared_gate_comps.add(Aextra_top_connection)
    shared_gate_comps << straight_route(pdk,Aextra_top_connection.ports["e4"],pbottom_AB.ports["R_drain_N"])
    shared_gate_comps << L_route(pdk,pcomps_route_A_drain.ports["con_S"], Aextra_top_connection.ports["e1"],viaoffset=(False,True))
    # connect source of B to drain of 2R
    pcomps_route_B_source_extension = shared_gate_comps.xmax-max(LRsourcesPorts[-1].center[0],ptop_AB.ports["R_source_E"].center[0])+_max_metal_seperation_ps
    mimcap_connection_ref = shared_gate_comps << c_route(pdk, ptop_AB.ports["R_source_E"], LRdrainsPorts[-1],extension=pcomps_route_B_source_extension,viaoffset=(True,False))
    bottom_pcompB_floating_port = set_port_orientation(movey(movex(pbottom_AB.ports["L_source_E"].copy(),5*_max_metal_seperation_ps), destination=Aextra_top_connection.ports["e1"].center[1]+Aextra_top_connection.ports["e1"].width+_max_metal_seperation_ps),"S")
    pmos_bsource_2Rdrain_v = shared_gate_comps << L_route(pdk,pbottom_AB.ports["L_source_E"],bottom_pcompB_floating_port,vglayer="met3")
    shared_gate_comps << c_route(pdk, LRdrainsPorts[-1], set_port_orientation(bottom_pcompB_floating_port,"E"),extension=pcomps_route_B_source_extension,viaoffset=(True,False))
    pmos_bsource_2Rdrain_v_center = via_stack(pdk,"met2","met3",fulltop=True)
    shared_gate_comps.add(align_comp_to_port(pmos_bsource_2Rdrain_v_center, bottom_pcompB_floating_port,('r','t')))
    # connect drain of B to each other directly over where the diffpair top left drain will be
    pmos_bdrain_diffpair_v = shared_gate_comps << via_stack(pdk, "met2","met5",fullbottom=True)
    pmos_bdrain_diffpair_v = align_comp_to_port(pmos_bdrain_diffpair_v, movex(pbottom_AB.ports["L_gate_S"].copy(),destination=via_location))
    pmos_bdrain_diffpair_v.movey(0-_max_metal_seperation_ps)
    pcomps_route_B_drain_extension = shared_gate_comps.xmax-ptop_AB.ports["R_drain_E"].center[0]+_max_metal_seperation_ps
    shared_gate_comps << c_route(pdk, ptop_AB.ports["R_drain_E"], pmos_bdrain_diffpair_v.ports["bottom_met_E"],extension=pcomps_route_B_drain_extension +_max_metal_seperation_ps)
    shared_gate_comps << c_route(pdk, pbottom_AB.ports["L_drain_W"], pmos_bdrain_diffpair_v.ports["bottom_met_W"],extension=pcomps_route_B_drain_extension +_max_metal_seperation_ps)
    shared_gate_comps.add_ports(pmos_bdrain_diffpair_v.get_ports_list(),prefix="minusvia_")
    shared_gate_comps.add_ports(mimcap_connection_ref.get_ports_list(),prefix="mimcap_connection_")
    return shared_gate_comps

def __add_common_source_Pamp_and_finish_pcomps(pdk: MappedPDK, pmos_comps: Component, pamp_hparams, rmult) -> Component:
    x_dim_center = max(abs(pmos_comps.xmax),abs(pmos_comps.xmin))
    for direction in [-1, 1]:
        halfMultp = pmos(
            pdk,
            width=pamp_hparams[0],
            length=pamp_hparams[1],
            fingers=pamp_hparams[2],
            multipliers=pamp_hparams[3],
            with_tie=True,
            dnwell=False,
            with_substrate_tap=False,
            sd_route_left=bool(direction-1),
            rmult=rmult
        )
        halfMultp_ref = pmos_comps << halfMultp
        halfMultp_ref.movex(direction * abs(x_dim_center + halfMultp_ref.xmax+1))
        label = "L_" if direction==-1 else "R_"
        # this special marker is used to rename these ports in the opamp to commonsource_Pamp_
        pmos_comps.add_ports(halfMultp_ref.get_ports_list(),prefix="halfpspecialmarker_"+label)
    # add npadding and add ports
    nwellbbox = pmos_comps.extract(layers=[pdk.get_glayer("poly"),pdk.get_glayer("active_diff"),pdk.get_glayer("active_tap"), pdk.get_glayer("nwell"),pdk.get_glayer("dnwell")]).bbox
    nwellspacing = pdk.get_grule("nwell", "active_tap")["min_enclosure"]
    nwell_points = get_padding_points_cc(nwellbbox, default=nwellspacing, pdk_for_snap2xgrid=pdk)
    pmos_comps.add_polygon(nwell_points, layer=pdk.get_glayer("nwell"))
    tapcenter_rect = [(evaluate_bbox(pmos_comps)[0] + 1), (evaluate_bbox(pmos_comps)[1] + 1)]
    topptap = tapring(pdk, tapcenter_rect, "p+s/d").ref_center(position=pmos_comps.center)
    pmos_comps.add(topptap)
    pmos_comps.add_ports(topptap.get_ports_list(),prefix="top_ptap_")
    return pmos_comps
    


@validate_arguments
def __create_and_route_pins(
    pdk: MappedPDK,
    opamp_top: Component,
    pmos_comps_ref: ComponentReference,
    halfmultn_drain_routeref: ComponentReference,
    halfmultn_gate_routeref: ComponentReference
) -> tuple:
    _max_metal_seperation_ps = pdk.util_max_metal_seperation()
    # route halfmultp source, drain, and gate together, place vdd pin in the middle
    halfmultp_Lsrcport = opamp_top.ports["commonsource_Pamp_L_multiplier_0_source_con_N"]
    halfmultp_Rsrcport = opamp_top.ports["commonsource_Pamp_R_multiplier_0_source_con_N"]
    opamp_top << c_route(pdk, halfmultp_Lsrcport, halfmultp_Rsrcport, extension=opamp_top.ymax-halfmultp_Lsrcport.center[1], fullbottom=True,viaoffset=(False,False))
    # place vdd pin
    vddpin = opamp_top << rectangle(size=(5,3),layer=pdk.get_glayer("met4"),centered=True)
    vddpin.movey(opamp_top.ymax)
    # route vdd to source of 2L/2R
    opamp_top << straight_route(pdk, opamp_top.ports["pcomps_2L2Rsrcvia_top_met_N"], vddpin.ports["e4"])
    # drain route above vdd pin
    halfmultp_Ldrainport = opamp_top.ports["commonsource_Pamp_L_multiplier_0_drain_con_N"]
    halfmultp_Rdrainport = opamp_top.ports["commonsource_Pamp_R_multiplier_0_drain_con_N"]
    halfmultp_drain_routeref = opamp_top << c_route(pdk, halfmultp_Ldrainport, halfmultp_Rdrainport, extension=opamp_top.ymax-halfmultp_Ldrainport.center[1]+pdk.get_grule("met5")["min_separation"], fullbottom=True)
    halfmultp_Lgateport = opamp_top.ports["commonsource_Pamp_L_multiplier_0_gate_con_S"]
    halfmultp_Rgateport = opamp_top.ports["commonsource_Pamp_R_multiplier_0_gate_con_S"]
    ptop_halfmultp_gate_route = opamp_top << c_route(pdk, halfmultp_Lgateport, halfmultp_Rgateport, extension=abs(pmos_comps_ref.ymin-halfmultp_Lgateport.center[1])+pdk.get_grule("met5")["min_separation"],fullbottom=True,viaoffset=(False,False))
    # halfmultn to halfmultp drain to drain route
    extensionL = min(halfmultn_drain_routeref.ports["con_W"].center[0],halfmultp_drain_routeref.ports["con_W"].center[0])
    extensionR = max(halfmultn_drain_routeref.ports["con_E"].center[0],halfmultp_drain_routeref.ports["con_E"].center[0])
    opamp_top << c_route(pdk, halfmultn_drain_routeref.ports["con_W"], halfmultp_drain_routeref.ports["con_W"],extension=abs(opamp_top.xmin-extensionL)+2,cwidth=2)
    n_to_p_output_route = opamp_top << c_route(pdk, halfmultn_drain_routeref.ports["con_E"], halfmultp_drain_routeref.ports["con_E"],extension=abs(opamp_top.xmax-extensionR)+2,cwidth=2)
    # top nwell taps to vdd, top p substrate taps to gnd
    opamp_top << L_route(pdk, opamp_top.ports["pcomps_top_ptap_bl_top_met_S"], opamp_top.ports["commonsource_cmirror_output_L_tie_N_top_met_W"],hwidth=2)
    opamp_top << L_route(pdk, opamp_top.ports["pcomps_top_ptap_br_top_met_S"], opamp_top.ports["commonsource_cmirror_output_R_tie_N_top_met_E"],hwidth=2)
    L_toptapn_route = opamp_top.ports["commonsource_Pamp_L_tie_N_top_met_N"]
    R_toptapn_route = opamp_top.ports["commonsource_Pamp_R_tie_N_top_met_N"]
    opamp_top << straight_route(pdk, movex(vddpin.ports["e4"],destination=L_toptapn_route.center[0]), L_toptapn_route, glayer1="met3")
    opamp_top << straight_route(pdk, movex(vddpin.ports["e4"],destination=R_toptapn_route.center[0]), R_toptapn_route, glayer1="met3")
    # bias pins for first two stages
    vbias1 = opamp_top << rectangle(size=(5,3),layer=pdk.get_glayer("met3"),centered=True)
    vbias1.movey(opamp_top.ymin - _max_metal_seperation_ps - vbias1.ymax)
    opamp_top << straight_route(pdk, vbias1.ports["e2"], opamp_top.ports["diffpair_ibias_B_gate_S"],width=1,fullbottom=False)
    vbias2 = opamp_top << rectangle(size=(5,3),layer=pdk.get_glayer("met5"),centered=True)
    vbias2.movex(1+opamp_top.xmax+evaluate_bbox(vbias2)[0]+pdk.util_max_metal_seperation()).movey(opamp_top.ymin+vbias2.ymax)
    opamp_top << L_route(pdk, halfmultn_gate_routeref.ports["con_E"], vbias2.ports["e2"],hwidth=2)
    # out pin
    #output = opamp_top << rectangle(size=(5,3),layer=pdk.get_glayer("met5"),centered=True)
    #output.movex(opamp_top.xmax).movey(opamp_top.ymin+output.ymax)
    #opamp_top << L_route(pdk, output.ports["e2"], set_port_orientation(n_to_p_output_route.ports["con_S"],"E"))
    # route + and - pins
    plus_pin = opamp_top << rectangle(size=(5,2),layer=pdk.get_glayer("met4"),centered=True)
    plus_pin.movex(opamp_top.xmin).movey(_max_metal_seperation_ps + plus_pin.ymax + halfmultn_drain_routeref.ports["con_W"].center[1] + halfmultn_drain_routeref.ports["con_W"].width/2)
    route_to_pluspin = opamp_top << L_route(pdk, opamp_top.ports["diffpair_MINUSgateroute_W_con_N"], plus_pin.ports["e3"])
    minus_pin = opamp_top << rectangle(size=(5,2),layer=pdk.get_glayer("met4"),centered=True)
    minus_pin.movex(opamp_top.xmin + minus_pin.xmax).movey(_max_metal_seperation_ps + plus_pin.ymax + minus_pin.ymax)
    opamp_top << L_route(pdk, opamp_top.ports["diffpair_PLUSgateroute_E_con_N"], minus_pin.ports["e3"])
    # route top center components to diffpair
    opamp_top << straight_route(pdk,opamp_top.ports["diffpair_tr_multiplier_0_drain_N"], opamp_top.ports["pcomps_pbottomAB_R_gate_S"], glayer1="met5",width=3*pdk.get_grule("met5")["min_width"],via1_alignment_layer="met2",via1_alignment=('c','c'))
    opamp_top << straight_route(pdk,opamp_top.ports["diffpair_tl_multiplier_0_drain_N"], opamp_top.ports["pcomps_minusvia_top_met_S"], glayer1="met5",width=3*pdk.get_grule("met5")["min_width"],via1_alignment_layer="met2",via1_alignment=('c','c'))
    # route minus transistor drain to output
    outputvia_diff_pcomps = opamp_top << via_stack(pdk,"met5","met4")
    outputvia_diff_pcomps.movex(opamp_top.ports["diffpair_tl_multiplier_0_drain_N"].center[0]).movey(ptop_halfmultp_gate_route.ports["con_E"].center[1])
    # add pin ports
    opamp_top.add_ports(vddpin.get_ports_list(), prefix="pin_vdd_")
    opamp_top.add_ports(vbias1.get_ports_list(), prefix="pin_diffpairibias_")
    opamp_top.add_ports(vbias2.get_ports_list(), prefix="pin_commonsourceibias_")
    opamp_top.add_ports(plus_pin.get_ports_list(), prefix="pin_plus_")
    opamp_top.add_ports(minus_pin.get_ports_list(), prefix="pin_minus_")
    #opamp_top.add_ports(output.get_ports_list(), prefix="pin_output_")
    return opamp_top, n_to_p_output_route



@validate_arguments
def __add_mimcap_arr(pdk: MappedPDK, opamp_top: Component, mim_cap_size, mim_cap_rows, ymin: float, n_to_p_output_route) -> Component:
    mim_cap_size = pdk.snap_to_2xgrid(mim_cap_size, return_type="float")
    max_metalsep = pdk.util_max_metal_seperation()
    mimcaps_ref = opamp_top << mimcap_array(pdk,mim_cap_rows,2,size=mim_cap_size,rmult=6)
    displace_fact = max(max_metalsep,pdk.get_grule("capmet")["min_separation"])
    mimcaps_ref.movex(pdk.snap_to_2xgrid(opamp_top.xmax + displace_fact + mim_cap_size[0]/2))
    mimcaps_ref.movey(pdk.snap_to_2xgrid(ymin + mim_cap_size[1]/2))
    # connect mimcap to gnd
    port1 = opamp_top.ports["pcomps_mimcap_connection_con_N"]
    port2 = mimcaps_ref.ports["row"+str(int(mim_cap_rows)-1)+"_col0_bottom_met_N"]
    cref2_extension = max_metalsep + opamp_top.ymax - max(port1.center[1], port2.center[1])
    opamp_top << c_route(pdk,port1,port2, extension=cref2_extension, fullbottom=True)
    opamp_top << L_route(pdk, mimcaps_ref.ports["row0_col0_top_met_S"], set_port_orientation(n_to_p_output_route.ports["con_S"],"E"), hwidth=3)
    opamp_top.add_ports(mimcaps_ref.get_ports_list(),prefix="mimcap_")
    return opamp_top




@validate_arguments
def __add_output_stage(
    pdk: MappedPDK,
    opamp_top: Component,
    amplifierParams: tuple[float, float, int],
    biasParams: list,
    rmult: int,
    n_to_p_output_route: Union[Component, ComponentReference]
) -> Component:
    '''add output stage to opamp_top, args:
    pdk = pdk to use
    opamp_top = component to add output stage to
    amplifierParams = [width,length,fingers,mults] for amplifying FET
    biasParams = [width,length,fingers,mults] for bias FET
    '''
    # Instantiate output amplifier
    amp_fet_ref = opamp_top << nmos(
	    pdk,
	    width=amplifierParams[0],
        length=amplifierParams[1],
        fingers=amplifierParams[2],
        multipliers=1,
        sd_route_topmet="met3",
        gate_route_topmet="met3",
        rmult=rmult,
        with_dnwell=False
    )
    # Instantiate bias FET
    cmirror_ibias = opamp_top << two_nfet_interdigitized(
        pdk,
        numcols=biasParams[2],
        width=biasParams[0],
        length=biasParams[1],
        fingers=1,
        gate_route_topmet="met3",
        sd_route_topmet="met3",
        rmult=rmult
    )
    metal_sep = pdk.util_max_metal_seperation()
    # Locate output stage relative position
    # x-coordinate: Center of SW capacitor in array
    # y-coordinate: Top of NMOS blocks
    x_cord = opamp_top.ports["mimcap_row0_col0_bottom_met_S"].center[0]
    y_cord = opamp_top.ports["commonsource_cmirror_output_R_tie_tr_top_met_N"].center[1]
    dims = evaluate_bbox(amp_fet_ref)
    center = [x_cord + dims[0]/2, y_cord - dims[1]/2]
    amp_fet_ref.move(center)
    amp_fet_ref.movey(pdk.get_grule("active_tap", "p+s/d")["min_enclosure"])
    dims = evaluate_bbox(cmirror_ibias)
    cmirror_ibias.movex(amp_fet_ref.xmin + dims[0]/2)
    cmirror_ibias.movey(amp_fet_ref.ymin - dims[1]/2 - metal_sep)
    # route input of output_stage to output of previous stage
    opamp_top << L_route(pdk, n_to_p_output_route.ports["con_S"], amp_fet_ref.ports["multiplier_0_gate_W"])
    # route drain of amplifier to vdd
    opamp_top << L_route(pdk, opamp_top.ports["commonsource_Pamp_R_tie_bl_top_met_W"], amp_fet_ref.ports["multiplier_0_drain_N"],hwidth=2)
    # route drain of cmirror to source of amplifier
    opamp_top << c_route(pdk, cmirror_ibias.ports["B_drain_E"],amp_fet_ref.ports["multiplier_0_source_E"],extension=metal_sep)
    # route cmirror: A gate, B gate and A drain together. Then A source and B source to ground
    gate_short = opamp_top << c_route(pdk, cmirror_ibias.ports["A_gate_E"],cmirror_ibias.ports["B_gate_E"],extension=3*metal_sep,viaoffset=None)
    opamp_top << L_route(pdk, gate_short.ports["con_N"],cmirror_ibias.ports["A_drain_E"],viaoffset=False,fullbottom=False)
    srcshort = opamp_top << c_route(pdk, cmirror_ibias.ports["A_source_W"],cmirror_ibias.ports["B_source_W"],extension=metal_sep)
    opamp_top << straight_route(pdk, srcshort.ports["con_N"], cmirror_ibias.ports["welltie_N_top_met_S"],via2_alignment_layer="met2")
    # Route all tap rings together and ground them
    opamp_top << straight_route(pdk, amp_fet_ref.ports["tie_N_top_met_N"],amp_fet_ref.ports["guardring_N_top_met_S"],width=2)
    opamp_top << straight_route(pdk, cmirror_ibias.ports["welltie_N_top_met_N"],cmirror_ibias.ports["substratetap_N_top_met_S"],width=2)
    opamp_top << straight_route(pdk, amp_fet_ref.ports["guardring_bl_top_met_S"],cmirror_ibias.ports["substratetap_tr_top_met_N"])
    opamp_top << straight_route(pdk, amp_fet_ref.ports["guardring_tl_top_met_W"], opamp_top.ports["commonsource_cmirror_output_R_tie_tr_top_met_E"])
    # add ports, add bias/output pin, and return
    psuedo_out_port = movex(amp_fet_ref.ports["multiplier_0_source_E"].copy(),6*metal_sep)
    output_pin = opamp_top << straight_route(pdk, amp_fet_ref.ports["multiplier_0_source_E"], psuedo_out_port)
    opamp_top.add_ports(amp_fet_ref.get_ports_list(),prefix="outputstage_amp_")
    opamp_top.add_ports(cmirror_ibias.get_ports_list(),prefix="outputstage_bias_")
    opamp_top.add_ports(output_pin.get_ports_list(),prefix="pin_output_")
    bias_pin = opamp_top << rectangle(size=(5,3),layer=pdk.get_glayer("met3"),centered=True)
    bias_pin.movex(cmirror_ibias.center[0]).movey(cmirror_ibias.ports["B_gate_S"].center[1]-bias_pin.ymax-5*metal_sep)
    opamp_top << straight_route(pdk, bias_pin.ports["e2"], cmirror_ibias.ports["B_gate_S"],width=1)
    opamp_top.add_ports(bias_pin.get_ports_list(),prefix="pin_outputibias_")
    return opamp_top


@cell
def opamp(
    pdk: MappedPDK,
    diffpair_params: tuple[float, float, int] = (6, 1, 4),
    diffpair_bias: tuple[float, float, int] = (6, 2, 4),
    half_common_source_params: tuple[float, float, int, int] = (7, 1, 10, 3),
    half_common_source_bias: tuple[float, float, int, int] = (6, 2, 8, 2),
    output_stage_params: tuple[float, float, int] = (5, 1, 16),
    output_stage_bias: tuple[float, float, int] = (6, 2, 4),
    mim_cap_size=(12, 12),
    mim_cap_rows=3,
    rmult: int = 2
) -> Component:
    """create an opamp, args:
    pdk=pdk to use
    diffpair_params = diffpair (width,length,fingers)
    diffpair_bias = bias transistor for diffpair nmos (width,length,fingers). The ref and output of the cmirror are identical
    half_common_source_params = pmos top component amp (width,length,fingers,mults)
    half_common_source_bias = bottom L/R large nmos current mirror (width,length,fingers,mults). The ref of the cmirror always has 1 multplier.
    ****NOTE: change the multiplier option to change the relative sizing of the current mirror ref/output
    output_stage_amp_params = output amplifier transistor params (width, length, fingers)
    output_stage_bias = output amplifier current mirror params (width, length, fingers). The ref and output of the cmirror are identical
    mim_cap_size = width,length of individual mim_cap
    mim_cap_rows = number of rows in the mimcap array (always 2 cols)
    rmult = routing multiplier (larger = wider routes)
    """
    _max_metal_seperation_ps = pdk.util_max_metal_seperation()
    opamp_top = Component()
    # place nmos components
    clear_cache()
    diffpair_and_bias = __add_diff_pair_and_bias(pdk, opamp_top, diffpair_params, diffpair_bias, rmult)
    # create and position each half of the nmos bias transistor for the common source stage symetrically
    clear_cache()
    opamp_top = __add_common_source_nbias_transistors(pdk, opamp_top, half_common_source_bias, rmult)
    opamp_top.add_padding(layers=(pdk.get_glayer("pwell"),),default=0)
    # add ground pin
    gndpin = opamp_top << rectangle(size=(5,3),layer=pdk.get_glayer("met4"),centered=True)
    gndpin.movey(opamp_top.ymin-pdk.util_max_metal_seperation()-gndpin.ymax)
    # route bottom ncomps except drain of nbias (still need to place common source pmos amp)
    clear_cache()
    opamp_top, halfmultn_drain_routeref, halfmultn_gate_routeref, _cref = __route_bottom_ncomps_except_drain_nbias(pdk, opamp_top, gndpin, half_common_source_bias[3])
    opamp_top.add_ports(gndpin.get_ports_list(), prefix="pin_gnd_")
    # place pmos components
    #TODO: report as bug
    clear_cache()
    pmos_comps, ptop_AB, pbottom_AB, LRplusdopedPorts, LRgatePorts, LRdrainsPorts, LRsourcesPorts = __create_sharedgatecomps(pdk, rmult)
    clear_cache()
    pmos_comps = __route_sharedgatecomps(pdk, pmos_comps, opamp_top.ports["diffpair_tl_multiplier_0_drain_N"].center[0], ptop_AB, pbottom_AB, LRplusdopedPorts, LRgatePorts, LRdrainsPorts, LRsourcesPorts)
    clear_cache()
    pmos_comps = __add_common_source_Pamp_and_finish_pcomps(pdk, pmos_comps, half_common_source_params, rmult)
    ydim_ncomps = opamp_top.ymax
    pmos_comps_ref = opamp_top << pmos_comps
    pmos_comps_ref.movey(round(ydim_ncomps + pmos_comps_ref.ymax+8))
    opamp_top.add_ports(pmos_comps_ref.get_ports_list(),prefix="pcomps_")
    rename_func = lambda name_, port_ : name_.replace("pcomps_halfpspecialmarker","commonsource_Pamp") if name_.startswith("pcomps_halfpspecialmarker") else name_
    opamp_top = rename_component_ports(opamp_top, rename_function=rename_func)
    # create pins and route
    clear_cache()
    opamp_top, n_to_p_output_route = __create_and_route_pins(pdk, opamp_top, pmos_comps_ref, halfmultn_drain_routeref, halfmultn_gate_routeref)
    # place mimcaps and route
    clear_cache()
    opamp_top = __add_mimcap_arr(pdk, opamp_top, mim_cap_size, mim_cap_rows, pmos_comps_ref.ymin, n_to_p_output_route)
    # add output amplfier stage
    opamp_top = __add_output_stage(pdk, opamp_top, output_stage_params, output_stage_bias, rmult, n_to_p_output_route)
    # return
    opamp_top.add_ports(_cref.get_ports_list(), prefix="gnd_route_")
    return rename_ports_by_orientation(component_snap_to_grid(opamp_top))


if __name__ == "__main__":
	from . pdk.util.standard_main import pdk

	iterate=False
    # TO TRY:
	#pdk = pdk to use
	#diffpair_params = diffpair (width,length,fingers)
	#diffpair_bias = bias transistor for diffpair nmos (width,length,fingers)
	#half_common_source_nbias = west current mirror (width,length,fingers,mults), two halves
	#pamp_hparams = pmos top component amp (width,length,fingers,mults)
	#mim_cap_size = width,length of individual mim_cap
	if iterate: # 486 versions
		# construct all diffpairs to try
		diffpairs = list()
		for width in [4,6,8]:
			for length in [0,1]:
				for fingers in [3,4,5]:
					diffpairs.append((width,length,fingers))
		# construct all bias1 (diffpair bias) transistors to try
		bias1s = list()
		for width in [4,6,8]:
			for length in [1,2,4]:
				for fingers in [3,4,5]:
					bias1s.append((width,length,fingers))
		cap_arrays = [1,3]
		opamps = list()
		for diffpair_v in diffpairs:
			for bias1_v in bias1s:
				for cap_array_v in cap_arrays:
					comp = opamp(pdk,diffpair_params=diffpair_v,diffpair_bias=bias1_v,mim_cap_rows=cap_array_v)
					opamps.append(comp)
		for i,comp in enumerate(opamps):
			comp.write_gds(str(i)+".gds")
	else:
		opamp(
			pdk,
			diffpair_params = (6, 1, 4),
			diffpair_bias = (6, 2, 4),
			half_common_source_nbias = (6, 2, 8, 3),
			pamp_hparams = (7, 1, 10, 3),
			mim_cap_size = (12, 12),
			mim_cap_rows = 3,
			rmult = 2
		).show()
		


def benchmark(pdk: MappedPDK, save_file: Optional[str]="./oPamp_Runtime_second.txt") -> float:
    """get runtime of opamp in seconds (note running this with sky130 results in longer runtime due to addition of NPC)"""
    import time
    start = time.time()
    opamp(pdk)
    end = time.time()
    elapsed_time = end - start
    print(elapsed_time)
    if save_file:
        from pathlib import Path
        save_file = Path(save_file).resolve()
        try:
            with open(save_file,"w") as resultfile:
                resultfile.write(str(elapsed_time))
        except Exception:
            print("benchmark was not able to write to savefile")
    return elapsed_time
