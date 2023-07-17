from gdsfactory.cell import cell, clear_cache
from gdsfactory.component import Component, copy
from gdsfactory.components.rectangle import rectangle
from PDK.mappedpdk import MappedPDK
from typing import Optional
from fet import nmos, pmos, multiplier
from diff_pair import diff_pair
from guardring import tapring
from mimcap import mimcap_array, mimcap
from L_route import L_route
from c_route import c_route
from via_gen import via_stack, via_array
from gdsfactory.routing.route_quad import route_quad
from PDK.util.custom_comp_utils import rename_ports_by_orientation, rename_ports_by_list, add_ports_perimeter, print_ports, evaluate_bbox, prec_ref_center, movex, movey, set_orientation, to_decimal, to_float, move, align_comp_to_port
from sys import exit
from straight_route import straight_route
from PDK.util.snap_to_grid import component_snap_to_grid


@cell
def opamp(
    pdk: MappedPDK,
    diffpair_params: Optional[tuple[float, float, int]] = (6, 1, 4),
    diffpair_bias: Optional[tuple[float, float, int]] = (6, 2, 4),
    houtput_bias: Optional[tuple[float, float, int, int]] = (6, 2, 8, 3),
    pamp_hparams: Optional[tuple[float, float, int, int]] = (7, 1, 10, 3),
    mim_cap_size=(12, 12),
    mim_cap_rows=3
) -> Component:
    """create an opamp, args:
    pdk=pdk to use
    diffpair_params = diffpair (width,length,fingers)
    diffpair_bias = bias transistor for diffpair nmos (width,length,fingers)
    houtput_bias = west current mirror (width,length,fingers,mults), two halves
    pamp_hparams = pmos top component amp (width,length,fingers,mults)
    mim_cap_size = width,length of individual mim_cap
    """
    _max_metal_seperation_ps = max([pdk.get_grule("met"+str(i))["min_separation"] for i in range(1,5)])
    opamp_top = Component()
    # place nmos components
    # create and center diffpair
    diffpair_i_ = Component("temp diffpair and current source")
    center_diffpair_comp = diff_pair(
        pdk,
        width=diffpair_params[0],
        length=diffpair_params[1],
        fingers=diffpair_params[2],
    )
    diffpair_i_.add(prec_ref_center(center_diffpair_comp))
    diffpair_i_.add_ports(center_diffpair_comp.get_ports_list())
    # create and position tail current source
    tailcurrent_comp = nmos(
        pdk,
        width=diffpair_bias[0],
        length=diffpair_bias[1],
        fingers=diffpair_bias[2],
        multipliers=1,
        with_tie=False,
        with_dnwell=False,
        with_substrate_tap=False,
        gate_route_topmet="met3",
        sd_route_topmet="met3"
    )
    tailcurrent_ref = diffpair_i_ << tailcurrent_comp
    tailcurrent_ref.movey(
        -0.5 * (center_diffpair_comp.ymax - center_diffpair_comp.ymin)
        - abs(tailcurrent_ref.ymax) - _max_metal_seperation_ps
    )
    diffpair_i_.add_ports(tailcurrent_ref.get_ports_list())
    # add diff pair and tailcurrent_comp to opamp
    diffpair_i_ref = prec_ref_center(diffpair_i_)
    opamp_top.add(diffpair_i_ref)
    opamp_top.add_ports(diffpair_i_ref.get_ports_list(),prefix="centerNcomps_")
    # create and position current mirror symetrically
    x_dim_center = opamp_top.xmax
    src_gnd_port = [None,None]
    for i, dummy in enumerate([(False, True), (True, False)]):
        halfMultn = nmos(
            pdk,
            width=houtput_bias[0],
            length=houtput_bias[1],
            fingers=houtput_bias[2],
            multipliers=houtput_bias[3],
            with_tie=True,
            with_dnwell=False,
            with_substrate_tap=False,
            with_dummy=dummy,
            sd_route_left = bool(i)
        )
        halfMultn_ref = opamp_top << halfMultn
        direction = (-1) ** i
        halfMultn_ref.movex(direction * abs(x_dim_center + halfMultn_ref.xmax + _max_metal_seperation_ps))
        opamp_top.add_ports(halfMultn_ref.get_ports_list(), prefix="nfet_Isrc_"+str(i)+"_")
    opamp_top.add_padding(layers=(pdk.get_glayer("pwell"),),default=0)
    # add ground pin
    gndpin = opamp_top << rectangle(size=(5,3),layer=pdk.get_glayer("met4"),centered=True)
    gndpin.movey(opamp_top.ymin-_max_metal_seperation_ps-gndpin.ymax)
    # route tailcurrent_comp
    opamp_top << c_route(pdk, opamp_top.ports["centerNcomps_multiplier_0_source_W"],gndpin.ports["e1"],width2=3,cglayer="met5",fullbottom=True,cwidth=3*pdk.get_grule("met5")["min_width"])
    opamp_top << c_route(pdk, opamp_top.ports["centerNcomps_multiplier_0_source_E"],gndpin.ports["e3"],width2=3,cglayer="met5",fullbottom=True,cwidth=3*pdk.get_grule("met5")["min_width"])
    # route to gnd the sources of halfMultn
    _cref = opamp_top << c_route(pdk, opamp_top.ports["nfet_Isrc_0_multiplier_0_source_con_S"], opamp_top.ports["nfet_Isrc_1_multiplier_0_source_con_S"], extension=abs(gndpin.ports["e2"].center[1]-opamp_top.ports["nfet_Isrc_0_multiplier_0_source_con_S"].center[1]),fullbottom=True)
    # connect gates and drains of halfMultn
    halfMultn_left_gate_port = opamp_top.ports["nfet_Isrc_0_multiplier_"+str(houtput_bias[3]-2)+"_gate_con_N"]
    halfMultn_right_gate_port = opamp_top.ports["nfet_Isrc_1_multiplier_"+str(houtput_bias[3]-2)+"_gate_con_N"]
    halfmultn_gate_routeref = opamp_top << c_route(pdk, halfMultn_left_gate_port, halfMultn_right_gate_port, extension=abs(opamp_top.ymax-halfMultn_left_gate_port.center[1])+1,fullbottom=True, viaoffset=(False,False))
    halfMultn_left_drain_port = opamp_top.ports["nfet_Isrc_0_multiplier_"+str(houtput_bias[3]-2)+"_drain_con_N"]
    halfMultn_right_drain_port = opamp_top.ports["nfet_Isrc_1_multiplier_"+str(houtput_bias[3]-2)+"_drain_con_N"]
    halfmultn_drain_routeref = opamp_top << c_route(pdk, halfMultn_left_drain_port, halfMultn_right_drain_port, extension=abs(opamp_top.ymax-halfMultn_left_drain_port.center[1])+1,fullbottom=True)
    # route to gnd the guardring of halfMultn
    opamp_top << straight_route(pdk,opamp_top.ports["nfet_Isrc_0_tie_S_top_met_S"],movey(gndpin.ports["e1"],evaluate_bbox(gndpin)[1]/4),width=2,glayer1="met3",fullbottom=True)
    opamp_top << straight_route(pdk,opamp_top.ports["nfet_Isrc_1_tie_S_top_met_S"],movey(gndpin.ports["e3"],evaluate_bbox(gndpin)[1]/4),width=2,glayer1="met3",fullbottom=True)
    # route source of diffpair to drain of tailcurrent_comp
    opamp_top << L_route(pdk,opamp_top.ports["centerNcomps_source_routeW_con_N"],opamp_top.ports["centerNcomps_multiplier_0_drain_W"])
    opamp_top << L_route(pdk,opamp_top.ports["centerNcomps_source_routeE_con_N"],opamp_top.ports["centerNcomps_multiplier_0_drain_E"])
    # place pmos components
    pmos_comps = Component("pmos_section_top")
    # center and position
    shared_gate_comps = Component("pmos_shared_gates")
    #TODO: report as bug
    clear_cache()
    pcompR = multiplier(pdk, "p+s/d", width=6, length=1, fingers=6, dummy=(False, True))
    pcompL = multiplier(pdk, "p+s/d", width=6, length=1, fingers=6, dummy=(True, False))
    pcomp_AB_spacing = max(2*_max_metal_seperation_ps + 6*pdk.get_grule("met4")["min_width"],pdk.get_grule("p+s/d")["min_separation"])
    _prefL = (shared_gate_comps << pcompL).movex(-1 * pcompL.xmax - pcomp_AB_spacing/2)
    _prefR = (shared_gate_comps << pcompR).movex(-1 * pcompR.xmin + pcomp_AB_spacing/2)
    shared_gate_comps.add_ports(_prefL.get_ports_list(),prefix="L_")
    shared_gate_comps.add_ports(_prefR.get_ports_list(),prefix="R_")
    shared_gate_comps << route_quad(_prefL.ports["gate_W"], _prefR.ports["gate_E"], layer=pdk.get_glayer("met2"))
    # center
    relative_dim_comp = multiplier(
        pdk, "p+s/d", width=6, length=1, fingers=4, dummy=False
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
                pdk, "p+s/d", width=6, length=1, fingers=4, dummy=dummy
            )
            extra_t = -1 * single_dim
        elif i == 2:
            dummy = [False, True]
            pcenterfourunits = multiplier(
                pdk, "p+s/d", width=6, length=1, fingers=4, dummy=dummy
            )
            extra_t = single_dim
        else:
            pcenterfourunits = relative_dim_comp
        pref_ = (pmos_comps << pcenterfourunits).movex(to_float(i * single_dim + extra_t))
        LRplusdopedPorts += [pref_.ports["plusdoped_W"] , pref_.ports["plusdoped_E"]]
        LRgatePorts += [pref_.ports["gate_W"],pref_.ports["gate_E"]]
        LRdrainsPorts += [pref_.ports["source_W"],pref_.ports["source_E"]]
        LRsourcesPorts += [pref_.ports["drain_W"],pref_.ports["drain_E"]]
    # connect p+s/d layer of the transistors
    pmos_comps << route_quad(LRplusdopedPorts[0],LRplusdopedPorts[-1],layer=pdk.get_glayer("p+s/d"))
    # connect drain of the left 2 and right 2, short sources of all 4
    pmos_comps << route_quad(LRdrainsPorts[0],LRdrainsPorts[3],layer=LRdrainsPorts[0].layer)
    pmos_comps << route_quad(LRdrainsPorts[4],LRdrainsPorts[7],layer=LRdrainsPorts[0].layer)
    pmos_comps << route_quad(LRsourcesPorts[0],LRsourcesPorts[-1],layer=LRsourcesPorts[0].layer)
    pcomps_2L_2R_sourcevia = pmos_comps << via_stack(pdk,pdk.layer_to_glayer(LRsourcesPorts[0].layer), "met4")
    pcomps_2L_2R_sourcevia.movey(evaluate_bbox(pcomps_2L_2R_sourcevia.parent.extract(layers=[LRsourcesPorts[0].layer,]))[1]/2 + LRsourcesPorts[0].center[1])
    pmos_comps.add_ports(pcomps_2L_2R_sourcevia.get_ports_list(),prefix="2L2Rsrcvia_")
    # short all the gates
    pmos_comps << route_quad(LRgatePorts[0],LRgatePorts[-1],layer=pdk.get_glayer("met2"))
    ytranslation_pcenter = 2 * pcenterfourunits.ymax + 4*_max_metal_seperation_ps
    ptop_AB = (pmos_comps << shared_gate_comps).movey(ytranslation_pcenter)
    pbottom_AB = (pmos_comps << shared_gate_comps).movey(-1 * ytranslation_pcenter)
    pmos_comps.add_ports(ptop_AB.get_ports_list(),prefix="ptopAB_")
    pmos_comps.add_ports(pbottom_AB.get_ports_list(),prefix="pbottomAB_")
    # short all gates of pmos_comps
    pcenter_gate_route_extension = pmos_comps.xmax - min(ptop_AB.ports["R_gate_E"].center[0], LRgatePorts[-1].center[0]) - pdk.get_grule("active_diff")["min_width"]
    pcenter_l_croute = pmos_comps << c_route(pdk, ptop_AB.ports["L_gate_W"], pbottom_AB.ports["L_gate_W"],extension=pcenter_gate_route_extension)
    pcenter_r_croute = pmos_comps << c_route(pdk, ptop_AB.ports["R_gate_E"], pbottom_AB.ports["R_gate_E"],extension=pcenter_gate_route_extension)
    pmos_comps << straight_route(pdk, LRgatePorts[0], pcenter_l_croute.ports["con_N"])
    pmos_comps << straight_route(pdk, LRgatePorts[-1], pcenter_r_croute.ports["con_N"])
    # connect drain of A to the shorted gates
    pmos_comps << L_route(pdk,ptop_AB.ports["L_source_W"],pcenter_l_croute.ports["con_N"])
    pmos_comps << straight_route(pdk,pbottom_AB.ports["R_source_E"],pcenter_r_croute.ports["con_N"])
    # connect source of A to the drain of 2L
    pcomps_route_A_drain_extension = pmos_comps.xmax-max(ptop_AB.ports["R_drain_E"].center[0], LRdrainsPorts[-1].center[0])+_max_metal_seperation_ps
    pcomps_route_A_drain = pmos_comps << c_route(pdk, ptop_AB.ports["L_drain_W"], LRdrainsPorts[0], extension=pcomps_route_A_drain_extension)
    row_rectangle_routing = rectangle(layer=ptop_AB.ports["L_drain_W"].layer,size=(pbottom_AB.ports["R_source_N"].width,pbottom_AB.ports["R_source_W"].width)).copy()
    Aextra_top_connection = align_comp_to_port(row_rectangle_routing, pbottom_AB.ports["R_source_N"], ('c','t')).movey(row_rectangle_routing.ymax + _max_metal_seperation_ps)
    pmos_comps.add(Aextra_top_connection)
    pmos_comps << straight_route(pdk,Aextra_top_connection.ports["e4"],pbottom_AB.ports["R_drain_N"])
    pmos_comps << L_route(pdk,pcomps_route_A_drain.ports["con_S"], Aextra_top_connection.ports["e1"],viaoffset=(False,True))
    # connect source of B to drain of 2R
    pcomps_route_B_source_extension = pmos_comps.xmax-max(LRsourcesPorts[-1].center[0],ptop_AB.ports["R_source_E"].center[0])+_max_metal_seperation_ps
    pmos_comps << c_route(pdk, ptop_AB.ports["R_source_E"], LRdrainsPorts[-1],extension=pcomps_route_B_source_extension,viaoffset=(True,False))
    bottom_pcompB_floating_port = set_orientation(movey(movex(pbottom_AB.ports["L_source_E"].copy(),4*_max_metal_seperation_ps), destination=Aextra_top_connection.ports["e1"].center[1]+Aextra_top_connection.ports["e1"].width+_max_metal_seperation_ps),"S")
    pmos_bsource_2Rdrain_v = pmos_comps << L_route(pdk,pbottom_AB.ports["L_source_E"],bottom_pcompB_floating_port,vglayer="met3")
    pmos_comps << c_route(pdk, LRdrainsPorts[-1], set_orientation(bottom_pcompB_floating_port,"E"),extension=pcomps_route_B_source_extension,viaoffset=(True,False))
    pmos_bsource_2Rdrain_v_center = via_stack(pdk,"met2","met3",fulltop=True)
    pmos_comps.add(align_comp_to_port(pmos_bsource_2Rdrain_v_center, bottom_pcompB_floating_port,('r','t')))
    # connect drain of B to each other directly over where the diffpair top left drain will be
    pmos_bdrain_diffpair_v = pmos_comps << via_stack(pdk, "met2","met5",fullbottom=True)
    align_comp_to_port(pmos_bdrain_diffpair_v, movex(pbottom_AB.ports["L_gate_S"].copy(),destination=opamp_top.ports["centerNcomps_tl_multiplier_0_drain_N"].center[0])).movey(0-_max_metal_seperation_ps)
    pcomps_route_B_drain_extension = pmos_comps.xmax-ptop_AB.ports["R_drain_E"].center[0]+_max_metal_seperation_ps
    pmos_comps << c_route(pdk, ptop_AB.ports["R_drain_E"], pmos_bdrain_diffpair_v.ports["bottom_met_E"],extension=pcomps_route_B_drain_extension +_max_metal_seperation_ps)
    pmos_comps << c_route(pdk, pbottom_AB.ports["L_drain_W"], pmos_bdrain_diffpair_v.ports["bottom_met_W"],extension=pcomps_route_B_drain_extension +_max_metal_seperation_ps)
    pmos_comps.add_ports(pmos_bdrain_diffpair_v.get_ports_list(),prefix="minusvia_")
    # pcore to output
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
            sd_route_left=bool(direction-1)
        )
        halfMultp
        halfMultp_ref = pmos_comps << halfMultp
        halfMultp_ref.movex(direction * abs(x_dim_center + halfMultp_ref.xmax+1))
        label = "l_" if direction==-1 else "r_"
        pmos_comps.add_ports(halfMultp_ref.get_ports_list(),prefix="halfp_"+label)
    # finish place central
    ydim_ncomps = opamp_top.ymax
    # TODO: use remove layers and make padding only around transistors (ignore the bottom routes)
    pmos_comps.add_padding(
        layers=[pdk.get_glayer("nwell")],
        default=pdk.get_grule("nwell", "active_tap")["min_enclosure"],
    )
    tapcenter_rect = [(evaluate_bbox(pmos_comps)[0] + 1), (evaluate_bbox(pmos_comps)[1] + 1)]
    topptap = pmos_comps << tapring(pdk, tapcenter_rect, "p+s/d")
    pmos_comps.add_ports(topptap.get_ports_list(),prefix="top_ptap_")
    pmos_comps_ref = opamp_top << pmos_comps
    pmos_comps_ref.movey(round(ydim_ncomps + pmos_comps_ref.ymax+8))
    opamp_top.add_ports(pmos_comps_ref.get_ports_list(),prefix="pcomps_")
    # route halfmultp source, drain, and gate together, place vdd pin in the middle
    halfmultp_Lsrcport = opamp_top.ports["pcomps_halfp_l_multiplier_0_source_con_N"]
    halfmultp_Rsrcport = opamp_top.ports["pcomps_halfp_r_multiplier_0_source_con_N"]
    opamp_top << c_route(pdk, halfmultp_Lsrcport, halfmultp_Rsrcport, extension=opamp_top.ymax-halfmultp_Lsrcport.center[1], fullbottom=True,viaoffset=(False,False))
    # place vdd pin
    vddpin = opamp_top << rectangle(size=(5,3),layer=pdk.get_glayer("met4"),centered=True)
    vddpin.movey(opamp_top.ymax)
    # route vdd to source of 2L/2R
    opamp_top << straight_route(pdk, opamp_top.ports["pcomps_2L2Rsrcvia_top_met_N"], vddpin.ports["e4"])
    # drain route above vdd pin
    halfmultp_Ldrainport = opamp_top.ports["pcomps_halfp_l_multiplier_0_drain_con_N"]
    halfmultp_Rdrainport = opamp_top.ports["pcomps_halfp_r_multiplier_0_drain_con_N"]
    halfmultp_drain_routeref = opamp_top << c_route(pdk, halfmultp_Ldrainport, halfmultp_Rdrainport, extension=opamp_top.ymax-halfmultp_Ldrainport.center[1]+pdk.get_grule("met5")["min_separation"], fullbottom=True)
    halfmultp_Lgateport = opamp_top.ports["pcomps_halfp_l_multiplier_0_gate_con_S"]
    halfmultp_Rgateport = opamp_top.ports["pcomps_halfp_r_multiplier_0_gate_con_S"]
    ptop_halfmultp_gate_route = opamp_top << c_route(pdk, halfmultp_Lgateport, halfmultp_Rgateport, extension=abs(pmos_comps_ref.ymin-halfmultp_Lgateport.center[1])+pdk.get_grule("met5")["min_separation"],fullbottom=True,viaoffset=(False,False))
    # halfmultn to halfmultp drain to drain route
    extensionL = min(halfmultn_drain_routeref.ports["con_W"].center[0],halfmultp_drain_routeref.ports["con_W"].center[0])
    extensionR = max(halfmultn_drain_routeref.ports["con_E"].center[0],halfmultp_drain_routeref.ports["con_E"].center[0])
    opamp_top << c_route(pdk, halfmultn_drain_routeref.ports["con_W"], halfmultp_drain_routeref.ports["con_W"],extension=abs(opamp_top.xmin-extensionL)+2,cwidth=2)
    n_to_p_output_route = opamp_top << c_route(pdk, halfmultn_drain_routeref.ports["con_E"], halfmultp_drain_routeref.ports["con_E"],extension=abs(opamp_top.xmax-extensionR)+2,cwidth=2)
    # top nwell taps to vdd, top p substrate taps to gnd
    opamp_top << L_route(pdk, opamp_top.ports["pcomps_top_ptap_bl_top_met_S"], opamp_top.ports["nfet_Isrc_1_tie_N_top_met_W"],hwidth=2)
    opamp_top << L_route(pdk, opamp_top.ports["pcomps_top_ptap_br_top_met_S"], opamp_top.ports["nfet_Isrc_0_tie_N_top_met_E"],hwidth=2)
    L_toptapn_route = opamp_top.ports["pcomps_halfp_l_tie_N_top_met_N"]
    R_toptapn_route = opamp_top.ports["pcomps_halfp_r_tie_N_top_met_N"]
    opamp_top << straight_route(pdk, movex(vddpin.ports["e4"],destination=L_toptapn_route.center[0]), L_toptapn_route, glayer1="met3")
    opamp_top << straight_route(pdk, movex(vddpin.ports["e4"],destination=R_toptapn_route.center[0]), R_toptapn_route, glayer1="met3")
    # vbias1 and vbias2 pins
    vbias1 = opamp_top << rectangle(size=(5,3),layer=pdk.get_glayer("met3"),centered=True)
    vbias1.movey(opamp_top.ymin - _max_metal_seperation_ps - vbias1.ymax)
    opamp_top << straight_route(pdk, opamp_top.ports["centerNcomps_multiplier_0_gate_S"], vbias1.ports["e2"],width=1,fullbottom=False)
    vbias2 = opamp_top << rectangle(size=(5,3),layer=pdk.get_glayer("met3"),centered=True)
    vbias2.movex(opamp_top.xmin-2).movey(opamp_top.ymin+vbias2.ymax)
    opamp_top << L_route(pdk, halfmultn_gate_routeref.ports["con_W"], vbias2.ports["e2"],hwidth=2)
    # out pin
    output = opamp_top << rectangle(size=(5,3),layer=pdk.get_glayer("met5"),centered=True)
    output.movex(opamp_top.xmax).movey(opamp_top.ymin+output.ymax)
    opamp_top << L_route(pdk, output.ports["e2"], set_orientation(n_to_p_output_route.ports["con_S"],"E"))
    # route + and - pins
    plus_pin = opamp_top << rectangle(size=(5,2),layer=pdk.get_glayer("met4"),centered=True)
    plus_pin.movex(opamp_top.xmin).movey(_max_metal_seperation_ps + plus_pin.ymax + halfmultn_drain_routeref.ports["con_W"].center[1] + halfmultn_drain_routeref.ports["con_W"].width/2)
    route_to_pluspin = opamp_top << L_route(pdk, opamp_top.ports["centerNcomps_MINUSgateroute_W_con_N"], plus_pin.ports["e3"])
    minus_pin = opamp_top << rectangle(size=(5,2),layer=pdk.get_glayer("met4"),centered=True)
    minus_pin.movex(opamp_top.xmin + minus_pin.xmax).movey(_max_metal_seperation_ps + plus_pin.ymax + minus_pin.ymax)
    opamp_top << L_route(pdk, opamp_top.ports["centerNcomps_PLUSgateroute_E_con_N"], minus_pin.ports["e3"])
    # route top center components to diffpair
    opamp_top << straight_route(pdk,movey(opamp_top.ports["centerNcomps_tr_multiplier_0_drain_N"],0.05), opamp_top.ports["pcomps_pbottomAB_R_gate_S"], glayer1="met5",width=3*pdk.get_grule("met5")["min_width"])
    opamp_top << straight_route(pdk,movey(opamp_top.ports["centerNcomps_tl_multiplier_0_drain_N"],0.05), opamp_top.ports["pcomps_minusvia_top_met_S"], glayer1="met5",width=3*pdk.get_grule("met5")["min_width"])
    # route minus transistor drain to output
    outputvia_diff_pcomps = opamp_top << via_stack(pdk,"met5","met4")
    outputvia_diff_pcomps.movex(opamp_top.ports["centerNcomps_tl_multiplier_0_drain_N"].center[0]).movey(ptop_halfmultp_gate_route.ports["con_E"].center[1])
    # place mimcaps
    mimcaps_ref = opamp_top << mimcap_array(pdk,mim_cap_rows,2,size=mim_cap_size,rmult=6)
    displace_fact = max(_max_metal_seperation_ps,pdk.get_grule("capmet")["min_separation"])
    mimcaps_ref.movex(opamp_top.xmax + displace_fact + mim_cap_size[0]/2)
    mimcaps_ref.movey(pmos_comps_ref.ymin + mim_cap_size[1]/2)
    # connect mimcap to gnd
    gnd_pin_mimcap_route = opamp_top << L_route(pdk,mimcaps_ref.ports["row0_col1_top_met_S"],_cref.ports["con_E"],hwidth=3)
    opamp_top << L_route(pdk, mimcaps_ref.ports["row0_col0_bottom_met_S"], set_orientation(n_to_p_output_route.ports["con_S"],"E"), hwidth=3)
    # return
    opamp_top.add_ports(gnd_pin_mimcap_route.get_ports_list(), prefix="gnd_pin_")
    opamp_top.add_ports(vddpin.get_ports_list(), prefix="vdd_pin_")
    opamp_top.add_ports(vbias1.get_ports_list(), prefix="vbias1_pin_")
    opamp_top.add_ports(vbias2.get_ports_list(), prefix="vbias2_pin_")
    opamp_top.add_ports(plus_pin.get_ports_list(), prefix="plus_pin_")
    opamp_top.add_ports(minus_pin.get_ports_list(), prefix="minus_pin_")
    opamp_top.add_ports(output.get_ports_list(), prefix="output_pin_")
    return rename_ports_by_orientation(component_snap_to_grid(opamp_top))


if __name__ == "__main__":
	from PDK.util.standard_main import pdk

	iterate=False
# TO TRY:
	#pdk = pdk to use
	#diffpair_params = diffpair (width,length,fingers)
	#diffpair_bias = bias transistor for diffpair nmos (width,length,fingers)
	#houtput_bias = west current mirror (width,length,fingers,mults), two halves
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
		opamp(pdk).show()
		
		
#[0.7,1,0.02]
#bias_points = list()
#for bias1_point in bias1_points:
#	for bias2_point in bias2_points:
#		run design
#		bias_points.append(bias_point)

#best_bias = max(bias_points)
#0.8
#0.78,0.82,0.005

"""
for row in range(4):
	for col in range(8):
		ref = mycomp << opamps[8*row+col]
		ref.movex(150*col).movey(150*row)
"""
