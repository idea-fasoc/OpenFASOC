from gdsfactory.components import rectangle
from gdsfactory import Component
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.primitives.fet import nmos, pmos
from glayout.flow.placement.two_transistor_interdigitized import two_pfet_interdigitized
from glayout.flow.placement.four_transistor_interdigitized import generic_4T_interdigitzed
from glayout.flow.placement.two_transistor_interdigitized import two_nfet_interdigitized
from glayout.flow.pdk.util.comp_utils import prec_ref_center, movey, evaluate_bbox, movex, align_comp_to_port
from glayout.flow.routing.smart_route import smart_route, c_route, straight_route, L_route
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
from glayout.flow.spice import Netlist
from glayout.flow.primitives.guardring import tapring
from glayout.flow.primitives.via_gen import via_stack, via_array
#from glayout.flow.blocks.diff_pair import *
from diff_pair import *
from cross_coupled_load import *

import os

def mystrongARM_netlist(diffpair: Component, cross_couple: Component, nfet_clk: Component, nfet_clk_dum: Component, pfetA: Component, pfetB: Component, pfetC: Component, pfetD: Component):
    mystrongARM_netlist = Netlist(circuit_name ='strongARM', nodes=['VIP', 'VIM', 'VOP', 'VOM', 'VCLK', 'VDD', 'VSS', 'VP', 'VQ', 'VS'])
    mystrongARM_netlist.connect_netlist(
        diffpair.info['netlist'],
        [('VP','VIP'), ('VN','VIM'), ('VDD1','VP'), ('VDD2','VQ'), ('VTAIL','VS'), ('B','VSS')]
    )
    mystrongARM_netlist.connect_netlist(
        cross_couple.info['netlist'],
        [('VSN1','VP'), ('VSN2','VQ'), ('VSP1','VDD'), ('VSP2','VDD'), ('VO1','VOP'), ('VO2','VOM'), ('VBULKN','VSS'), ('VBULKP','VDD')]
    )
    #mystrongARM_netlist.connect_netlist(
    #    clk_nmos.info['netlist'],
    #    [('G','VCLK'), ('S','VSS'), ('D','VS'), ('B','VSS')]
    #)
    mystrongARM_netlist.connect_netlist(
        nfet_clk.info['netlist'],
        [('G','VCLK'), ('S','VSS'), ('D','VS'), ('B','VSS')]
    )
    mystrongARM_netlist.connect_netlist(
        nfet_clk_dum.info['netlist'],
        [('G','VSS'), ('S','VSS'), ('D','VSS'), ('B','VSS')]
    )
    mystrongARM_netlist.connect_netlist(
        pfetA.info['netlist'],
        [('G','VCLK'), ('S','VDD'), ('D','VOP'), ('B','VDD')]
    )
    mystrongARM_netlist.connect_netlist(
        pfetB.info['netlist'],
        [('G','VCLK'), ('S','VDD'), ('D','VOM'), ('B','VDD')]
    )
    mystrongARM_netlist.connect_netlist(
        pfetC.info['netlist'],
        [('G','VCLK'), ('S','VDD'), ('D','VP'), ('B','VDD')]
    )
    mystrongARM_netlist.connect_netlist(
        pfetD.info['netlist'],
        [('G','VCLK'), ('S','VDD'), ('D','VQ'), ('B','VDD')]
    )
    return mystrongARM_netlist
def mystrongARM(pdk: MappedPDK, diffp_w, diffp_l, ccinv_col, clk_fing, reset_w, reset_l):
    mystrongARM=Component(name="mystrongARM")
    diffp = diff_pair(pdk, diffp_w, 2, diffp_l)
    diffp_ref = prec_ref_center(diffp)
    mystrongARM.add(diffp_ref)
    

    cross_couple = cross_coupled_load(pdk, ccinv_col)
    cross_couple_ref = prec_ref_center(cross_couple)
    mystrongARM.add(cross_couple_ref)
    

    clk_nmos = nmos(pdk, width=4, fingers=clk_fing,rmult=1, with_substrate_tap=False, with_dnwell=False)
    clk_nmos_ref = prec_ref_center(clk_nmos)
    mystrongARM.add(clk_nmos_ref)

    reset_pmos_right = two_pfet_interdigitized(pdk, numcols=2, dummy=False, with_substrate_tap=False, with_tie=True, width=reset_w, length=reset_l, rmult=1)
    reset_pmos_ref1 = prec_ref_center(reset_pmos_right)
    mystrongARM.add(reset_pmos_ref1)
    offsety_reset_pmos=evaluate_bbox(cross_couple)[1]/4

    reset_pmos_left = two_pfet_interdigitized(pdk, numcols=2, dummy=False, with_substrate_tap=False, with_tie=True, width=reset_w, length=reset_l, rmult=1)
    reset_pmos_ref2 = prec_ref_center(reset_pmos_left)
    mystrongARM.add(reset_pmos_ref2)
    offsetx_cross = (evaluate_bbox(cross_couple)[0]-evaluate_bbox(reset_pmos_left)[0])/2

    offsety_diffp = (evaluate_bbox(diffp)[1]-evaluate_bbox(clk_nmos)[1])/2
    offsety_cross = (evaluate_bbox(cross_couple)[1]-evaluate_bbox(diffp)[1])/2

    movey(reset_pmos_ref2, evaluate_bbox(clk_nmos_ref)[1]+pdk.util_max_metal_seperation() + offsety_diffp + evaluate_bbox(diffp)[1]+pdk.util_max_metal_seperation() + offsety_cross+offsety_reset_pmos)
    movex(cross_couple_ref, evaluate_bbox(reset_pmos_left)[0]+pdk.util_max_metal_seperation()+offsetx_cross)
    movex(diffp_ref, evaluate_bbox(reset_pmos_left)[0]+pdk.util_max_metal_seperation()+offsetx_cross)
    movex(clk_nmos_ref, evaluate_bbox(reset_pmos_left)[0]+pdk.util_max_metal_seperation()+offsetx_cross)
    movey(cross_couple_ref, evaluate_bbox(clk_nmos_ref)[1]+pdk.util_max_metal_seperation() + offsety_diffp + evaluate_bbox(diffp)[1]+pdk.util_max_metal_seperation() + offsety_cross)
    movey(diffp_ref, evaluate_bbox(clk_nmos_ref)[1]+pdk.util_max_metal_seperation()+offsety_diffp)
    movey(reset_pmos_ref1, evaluate_bbox(clk_nmos_ref)[1]+pdk.util_max_metal_seperation() + offsety_diffp + evaluate_bbox(diffp)[1]+pdk.util_max_metal_seperation() + offsety_cross + offsety_reset_pmos)
    movex(reset_pmos_ref1, evaluate_bbox(reset_pmos_left)[0]+pdk.util_max_metal_seperation() + evaluate_bbox(cross_couple)[0]+pdk.util_max_metal_seperation())
    #print("bbox",evaluate_bbox(clk_nmos_ref)[1])
    #print(diffp_ref.get_ports_list())
    mystrongARM.add_ports(diffp_ref.get_ports_list(), prefix="strongARM_diffp_")
    mystrongARM.add_ports(cross_couple_ref.get_ports_list(), prefix="strongARM_")
    mystrongARM.add_ports(clk_nmos_ref.get_ports_list(), prefix="strongARM_clk_nmos_")
    mystrongARM.add_ports(reset_pmos_ref1.get_ports_list(), prefix="strongARM_clk_reset_pmos_r_")
    mystrongARM.add_ports(reset_pmos_ref2.get_ports_list(), prefix="strongARM_clk_reset_pmos_l_")

    mystrongARM << c_route(pdk, mystrongARM.ports["strongARM_diffp_tl_drain_W"], mystrongARM.ports["strongARM_cross_couple_bottom_A_source_W"], extension = 2)
    mystrongARM << c_route(pdk, mystrongARM.ports["strongARM_diffp_tr_drain_E"], mystrongARM.ports["strongARM_cross_couple_bottom_B_source_E"], extension = 2)
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_diffp_bl_source_W"], mystrongARM.ports["strongARM_clk_nmos_drain_W"], clk_nmos_ref, mystrongARM)
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_diffp_br_source_E"], mystrongARM.ports["strongARM_clk_nmos_drain_E"], clk_nmos_ref, mystrongARM)
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_r_A_source_E"], mystrongARM.ports["strongARM_clk_reset_pmos_r_B_source_E"],reset_pmos_ref1,mystrongARM)
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_l_A_source_E"], mystrongARM.ports["strongARM_clk_reset_pmos_l_B_source_E"],reset_pmos_ref2,mystrongARM)
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_r_A_drain_E"], mystrongARM.ports["strongARM_cross_couple_bottom_A_gate_E"])
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_r_B_drain_E"], mystrongARM.ports["strongARM_cross_couple_bottom_B_source_E"], extension = 1.25)
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_l_A_drain_W"], mystrongARM.ports["strongARM_cross_couple_bottom_B_gate_W"])
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_l_B_drain_W"], mystrongARM.ports["strongARM_cross_couple_bottom_A_source_W"], extension = 1.25)
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_r_A_gate_W"], mystrongARM.ports["strongARM_clk_reset_pmos_r_B_gate_W"],reset_pmos_ref1,mystrongARM)
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_l_A_gate_E"], mystrongARM.ports["strongARM_clk_reset_pmos_l_B_gate_E"],reset_pmos_ref2,mystrongARM)
    
    mystrongARM << c_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_r_A_gate_E"], mystrongARM.ports["strongARM_clk_nmos_gate_E"], extension = 3)
    mystrongARM << c_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_l_A_gate_W"], mystrongARM.ports["strongARM_clk_nmos_gate_W"], extension = 3)
    
    mystrongARM << straight_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_l_A_source_N"], mystrongARM.ports["strongARM_clk_reset_pmos_l_welltie_N_top_met_S"], width = 1,glayer1="met3",fullbottom=True)
    mystrongARM << straight_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_r_A_source_N"], mystrongARM.ports["strongARM_clk_reset_pmos_r_welltie_N_top_met_S"], width = 1,glayer1="met3",fullbottom=True)
    mystrongARM << straight_route(pdk, mystrongARM.ports["strongARM_cross_couple_top_A_source_N"], mystrongARM.ports["strongARM_cross_couple_top_welltie_N_top_met_S"],  width = 1,glayer1="met3",fullbottom=True)
    
    #Gnd tap connections
    mystrongARM << straight_route(pdk, mystrongARM.ports["strongARM_clk_nmos_source_N"], mystrongARM.ports["strongARM_clk_nmos_tie_N_top_met_S"] ,width=0.5,glayer1="met3",fullbottom=True)
    mystrongARM << straight_route(pdk, mystrongARM.ports["strongARM_diffp_tap_S_top_met_S"], mystrongARM.ports["strongARM_clk_nmos_tie_N_top_met_S"] ,width=1,glayer1="met1",fullbottom=True)
    mystrongARM << straight_route(pdk, mystrongARM.ports["strongARM_cross_couple_bottom_welltie_S_top_met_S"], mystrongARM.ports["strongARM_diffp_tap_N_top_met_N"] ,width=1,glayer1="met1",fullbottom=True)
    
    
    
    pfetA = pmos(pdk, width=reset_w, length=reset_l, fingers=2, with_dummy=(False, False))
    pfetB = pmos(pdk, width=reset_w, length=reset_l, fingers=2, with_dummy=(False, False))
    pfetC = pmos(pdk, width=reset_w, length=reset_l, fingers=2, with_dummy=(False, False))
    pfetD = pmos(pdk, width=reset_w, length=reset_l, fingers=2, with_dummy=(False, False))

    nfet_clk = nmos(pdk, width=4*clk_fing, length=0.15, fingers=1, with_dummy=(False, False))
    nfet_clk_dum = nmos(pdk, width=4*2, length=0.15, fingers=1, with_dummy=(False, False))
    mystrongARM.info['netlist'] = mystrongARM_netlist(diffp, cross_couple, nfet_clk, nfet_clk_dum, pfetA, pfetB, pfetC, pfetD)
    
    return mystrongARM

def add_strongARM_labels(pdk: MappedPDK, mystrongARM: Component):
    mystrongARM.unlock()
    met1_label = (68, 5)
    met1_pin = (68, 16)
    met2_label = (69, 5)
    met2_pin = (69, 16)
    move_info = list()

    vddpin = mystrongARM << rectangle(size=(5,1),layer=pdk.get_glayer("met3"),centered=True)
    vddpin.movey(mystrongARM.ymax + 2)
    vddpin.movex((mystrongARM.xmax)/2 - 4)
    #Vdd connections
    mystrongARM << straight_route(pdk, vddpin.ports["e4"] ,mystrongARM.ports["strongARM_cross_couple_top_welltie_N_top_met_N"], width=6,glayer1="met3",fullbottom=True)
    mystrongARM << L_route(pdk, vddpin.ports["e1"] ,mystrongARM.ports["strongARM_clk_reset_pmos_l_welltie_N_top_met_N"], vwidth=1,vglayer="met2",fullbottom=True)
    mystrongARM << L_route(pdk, vddpin.ports["e3"] ,mystrongARM.ports["strongARM_clk_reset_pmos_r_welltie_N_top_met_N"], vwidth=1,vglayer="met2",fullbottom=True)
    
    #vdd label
    vddlabel = rectangle(layer=met2_pin, size=(0.1,0.1), centered=True).copy()
    vddlabel.add_label(text="VDD",layer=met2_label)
    move_info.append((vddlabel,vddpin.ports["e1"],None))
    #inp label
    vinplabel = rectangle(layer=met1_pin, size=(0.1,0.1), centered=True).copy()
    vinplabel.add_label(text="VIP",layer=met1_label)
    move_info.append((vinplabel,mystrongARM.ports["strongARM_diffp_tl_gate_N"],None))
    #inm label
    vinmlabel = rectangle(layer=met1_pin, size=(0.1,0.1), centered=True).copy()
    vinmlabel.add_label(text="VIM",layer=met1_label)
    move_info.append((vinmlabel,mystrongARM.ports["strongARM_diffp_tr_gate_N"],None))
    #vtail label
    vtaillabel = rectangle(layer=met1_pin, size=(0.1,0.1), centered=True).copy()
    vtaillabel.add_label(text="VS",layer=met1_label)
    move_info.append((vtaillabel,mystrongARM.ports["strongARM_diffp_bl_source_E"],None))
    #vd1 label
    vd1label = rectangle(layer=met1_pin, size=(0.1,0.1), centered=True).copy()
    vd1label.add_label(text="VP",layer=met1_label)
    move_info.append((vd1label,mystrongARM.ports["strongARM_diffp_tl_drain_N"],None))
    #vd2 label
    vd2label = rectangle(layer=met1_pin, size=(0.1,0.1), centered=True).copy()
    vd2label.add_label(text="VQ",layer=met1_label)
    move_info.append((vd2label,mystrongARM.ports["strongARM_diffp_tr_drain_N"],None))
    #vclk label
    vclklabel = rectangle(layer=met1_pin, size=(0.1,0.1), centered=True).copy()
    vclklabel.add_label(text="VCLK",layer=met1_label)
    move_info.append((vclklabel,mystrongARM.ports["strongARM_clk_nmos_gate_N"],None))
    #gnd label
    vgndlabel = rectangle(layer=met1_pin, size=(0.1,0.1), centered=True).copy()
    vgndlabel.add_label(text="VSS",layer=met1_label)
    move_info.append((vgndlabel,mystrongARM.ports["strongARM_clk_nmos_tie_N_top_met_S"],None))
    #vo1 label
    vo1label = rectangle(layer=met1_pin, size=(0.1,0.1), centered=True).copy()
    vo1label.add_label(text="VOP",layer=met1_label)
    move_info.append((vo1label,mystrongARM.ports["strongARM_cross_couple_top_B_drain_N"],None))
    #vo2 label
    vo2label = rectangle(layer=met1_pin, size=(0.1,0.1), centered=True).copy()
    vo2label.add_label(text="VOM",layer=met1_label)
    move_info.append((vo2label,mystrongARM.ports["strongARM_cross_couple_top_A_drain_N"],None))
    #move everything to position
    for comp, prt, alignment in move_info:
        alignment = ('c','b') if alignment is None else alignment
        compref = align_comp_to_port(comp, prt, alignment=alignment)
        mystrongARM.add(compref)
    return mystrongARM.flatten()

strong = add_strongARM_labels(sky130_mapped_pdk,mystrongARM(sky130_mapped_pdk, 8, 0.4, 2, 4, 3, 0.4))
strong.write_gds("./mystrongARM.gds")
strong.show()

#magic_drc_result = sky130_mapped_pdk.drc_magic(strong, strong.name)
#lvs_result = sky130_mapped_pdk.lvs_netgen(strong,strong.name,copy_intermediate_files=True)

#fname = f"{strong.name}_lvsmag.spice"
#os.rename(fname, "mystrongARM_lvsmag.spice")

#with open("mystrongARM_lvsmag.spice","r") as file:
#    file_content = file.read()

#new_content = file_content.replace(strong.name,"mystrongARM")

#with open("mystrongARM_lvsmag.spice","w") as file:
#    file.write(new_content)
