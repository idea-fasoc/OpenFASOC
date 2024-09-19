from gdsfactory.components import rectangle
from gdsfactory import Component
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.primitives.fet import nmos
from glayout.flow.placement.two_transistor_interdigitized import two_pfet_interdigitized
from glayout.flow.placement.four_transistor_interdigitized import generic_4T_interdigitzed
from glayout.flow.placement.two_transistor_interdigitized import two_nfet_interdigitized
from glayout.flow.pdk.util.comp_utils import prec_ref_center, movey, evaluate_bbox, movex, align_comp_to_port
from glayout.flow.routing.smart_route import smart_route, c_route, straight_route, L_route
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
from glayout.flow.spice import Netlist

def diffPair_netlist(fetL: Component, fetR: Component):
    diffPair_netlist = Netlist(circuit_name ='diffPair', nodes=['VIP', 'VIM', 'VD1', 'VD2', 'VTAIL', 'VBULK'])
    diffPair_netlist.connect_netlist(
        fetL.info['netlist'],
        [('G','VIP'), ('D','VD1'), ('S','VTAIL'), ('B','VBULK')]
    )
    diffPair_netlist.connect_netlist(
        fetR.info['netlist'],
        [('G','VIM'), ('D','VD2'), ('S','VTAIL'), ('B','VBULK')]
    )
    return diffPair_netlist

def diffPair(pdk: MappedPDK, width, length):
    diffPair=Component(name="diffPair")
    diffp = two_nfet_interdigitized(pdk, numcols=2, dummy=True, with_substrate_tap=False, with_tie=True, width=width, length=length, rmult=1)
    diffp_ref = prec_ref_center(diffp)
    diffPair.add(diffp_ref)
    diffPair.add_ports(diffp_ref.get_ports_list(), prefix="diffp_")
    diffPair << smart_route(pdk,diffPair.ports["diffp_A_source_E"],diffPair.ports["diffp_B_source_E"],diffp_ref,diffPair)
    #add labels
    met1_label = (68, 5)
    met1_pin = (68, 16)
    move_info = list()
    diffPair.unlock()
    #inp label
    vinplabel = rectangle(layer=met1_pin, size=(0.5,0.5), centered=True).copy()
    vinplabel.add_label(text="VIP",layer=met1_label)
    move_info.append((vinplabel,diffPair.ports["diffp_A_gate_N"],None))
    #inm label
    vinmlabel = rectangle(layer=met1_pin, size=(0.05,0.05), centered=True).copy()
    vinmlabel.add_label(text="Vim",layer=met1_label)
    move_info.append((vinmlabel,diffPair.ports["diffp_B_gate_N"],None))
    #vtail label
    vtaillabel = rectangle(layer=met1_pin, size=(0.05,0.05), centered=True).copy()
    vtaillabel.add_label(text="Vtail",layer=met1_label)
    move_info.append((vtaillabel,diffPair.ports["diffp_A_source_N"],None))
    #vd1 label
    vd1label = rectangle(layer=met1_pin, size=(0.05,0.05), centered=True).copy()
    vd1label.add_label(text="Vd1",layer=met1_label)
    move_info.append((vd1label,diffPair.ports["diffp_A_drain_N"],None))
    #vd2 label
    vd2label = rectangle(layer=met1_pin, size=(0.05,0.05), centered=True).copy()
    vd2label.add_label(text="Vd2",layer=met1_label)
    move_info.append((vd2label,diffPair.ports["diffp_B_drain_N"],None))
    #vbulk label
    vbulklabel = rectangle(layer=met1_pin, size=(0.05,0.05), centered=True).copy()
    vbulklabel.add_label(text="Vbulk",layer=met1_label)
    move_info.append((vbulklabel,diffPair.ports["diffp_welltie_N_bottom_lay_S"],None))
    #move everything to position
    for comp, prt, alignment in move_info:
        alignment = ('c','b') if alignment is None else alignment
        compref = align_comp_to_port(comp, prt, alignment=alignment)
        diffPair.add(compref)
    
    diffPair.flatten()
    diffPair.write_gds("./strong.gds")
    #spice netlist
    fetL = nmos(pdk, width=2*width, length=length, with_dummy=(True, False))
    fetR = nmos(pdk, width=2*width, length=length, with_dummy=(False, True))
    diffPair.info['netlist'] = diffPair_netlist(fetL, fetR)
    #print(diffPair.info['netlist'].generate_netlist())
    #print(diffPair.get_ports_list())
    lvs_result = sky130_mapped_pdk.lvs_netgen(diffPair,'diffPair')
    return diffPair

diffPair(sky130_mapped_pdk,2,0.4).show()


def cross_coupled_load(pdk: MappedPDK, ccinv_col):
    cross_coupled_load=Component(name="cross_coupled_load")
    cross_couple = generic_4T_interdigitzed(pdk, numcols=ccinv_col, top_row_device="pfet", bottom_row_device="nfet", length=0.4)
    cross_couple_ref = prec_ref_center(cross_couple)
    cross_coupled_load.add(cross_couple_ref)
    cross_coupled_load.add_ports(cross_couple_ref.get_ports_list(), prefix="cross_couple_")
    cross_coupled_load << smart_route(pdk,cross_coupled_load.ports["cross_couple_top_A_source_E"],cross_coupled_load.ports["cross_couple_top_B_source_E"],cross_couple_ref,cross_coupled_load)
    cross_coupled_load << smart_route(pdk,cross_coupled_load.ports["cross_couple_bottom_A_source_E"],cross_coupled_load.ports["cross_couple_bottom_B_source_E"],cross_couple_ref,cross_coupled_load)
    cross_coupled_load << smart_route(pdk,cross_coupled_load.ports["cross_couple_top_A_drain_E"],cross_coupled_load.ports["cross_couple_top_B_gate_E"],cross_couple_ref,cross_coupled_load)
    cross_coupled_load << smart_route(pdk,cross_coupled_load.ports["cross_couple_bottom_A_drain_E"],cross_coupled_load.ports["cross_couple_bottom_B_gate_E"],cross_couple_ref,cross_coupled_load)
    cross_coupled_load << smart_route(pdk,cross_coupled_load.ports["cross_couple_top_B_drain_E"],cross_coupled_load.ports["cross_couple_top_A_gate_E"],cross_couple_ref,cross_coupled_load)
    cross_coupled_load << smart_route(pdk,cross_coupled_load.ports["cross_couple_bottom_B_drain_E"],cross_coupled_load.ports["cross_couple_bottom_A_gate_E"],cross_couple_ref,cross_coupled_load)
    cross_coupled_load << smart_route(pdk,cross_coupled_load.ports["cross_couple_top_B_gate_E"],cross_coupled_load.ports["cross_couple_bottom_B_gate_E"],cross_couple_ref,cross_coupled_load)
    cross_coupled_load << smart_route(pdk,cross_coupled_load.ports["cross_couple_top_A_gate_W"],cross_coupled_load.ports["cross_couple_bottom_A_gate_W"],cross_couple_ref,cross_coupled_load)
    return cross_coupled_load

#cross_coupled_load(gf180_mapped_pdk,2,0.5).show()

def mystrongARM(pdk: MappedPDK, diffp_w, diffp_l, ccinv_col, clk_fing, reset_w, reset_l):
    mystrongARM=Component(name="mystrongARM")
    diffp = diffPair(pdk, diffp_w, diffp_l)
    diffp_ref = prec_ref_center(diffp)
    mystrongARM.add(diffp_ref)
    

    cross_couple = cross_coupled_load(pdk, ccinv_col)
    cross_couple_ref = prec_ref_center(cross_couple)
    mystrongARM.add(cross_couple_ref)
    

    clk_nmos = nmos(pdk, width=4, fingers=clk_fing, rmult=1, with_substrate_tap=False, with_dnwell=False)
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
    mystrongARM.add_ports(diffp_ref.get_ports_list(), prefix="strongARM_")
    mystrongARM.add_ports(cross_couple_ref.get_ports_list(), prefix="strongARM_")
    mystrongARM.add_ports(clk_nmos_ref.get_ports_list(), prefix="strongARM_clk_nmos_")
    mystrongARM.add_ports(reset_pmos_ref1.get_ports_list(), prefix="strongARM_clk_reset_pmos_r_")
    mystrongARM.add_ports(reset_pmos_ref2.get_ports_list(), prefix="strongARM_clk_reset_pmos_l_")

    mystrongARM << c_route(pdk, mystrongARM.ports["strongARM_diffp_A_drain_W"], mystrongARM.ports["strongARM_cross_couple_bottom_A_source_W"], extension = 1.25)
    mystrongARM << c_route(pdk, mystrongARM.ports["strongARM_diffp_B_drain_E"], mystrongARM.ports["strongARM_cross_couple_bottom_B_source_E"], extension = 1.25)
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_diffp_A_source_W"], mystrongARM.ports["strongARM_clk_nmos_drain_W"], clk_nmos_ref, mystrongARM)
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_diffp_A_source_E"], mystrongARM.ports["strongARM_clk_nmos_drain_E"], clk_nmos_ref, mystrongARM)
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_r_A_source_E"], mystrongARM.ports["strongARM_clk_reset_pmos_r_B_source_E"],reset_pmos_ref1,mystrongARM)
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_l_A_source_E"], mystrongARM.ports["strongARM_clk_reset_pmos_l_B_source_E"],reset_pmos_ref2,mystrongARM)
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_r_A_drain_E"], mystrongARM.ports["strongARM_cross_couple_bottom_B_drain_E"])
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_r_B_drain_E"], mystrongARM.ports["strongARM_cross_couple_bottom_B_source_E"], extension = 1.25)
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_l_A_drain_W"], mystrongARM.ports["strongARM_cross_couple_bottom_A_drain_W"])
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_l_B_drain_W"], mystrongARM.ports["strongARM_cross_couple_bottom_A_source_W"], extension = 1.25)
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_r_A_gate_W"], mystrongARM.ports["strongARM_clk_reset_pmos_r_B_gate_W"],reset_pmos_ref1,mystrongARM)
    mystrongARM << smart_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_l_A_gate_E"], mystrongARM.ports["strongARM_clk_reset_pmos_l_B_gate_E"],reset_pmos_ref2,mystrongARM)
    
    mystrongARM << c_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_r_A_gate_E"], mystrongARM.ports["strongARM_clk_nmos_gate_E"], extension = 3)
    mystrongARM << c_route(pdk, mystrongARM.ports["strongARM_clk_reset_pmos_l_A_gate_W"], mystrongARM.ports["strongARM_clk_nmos_gate_W"], extension = 3)
    return mystrongARM

#mystrongARM(gf180_mapped_pdk, 8, 0.4, 2, 4, 3, 0.4).show()
