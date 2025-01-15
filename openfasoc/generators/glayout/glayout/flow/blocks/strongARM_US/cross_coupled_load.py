from gdsfactory.components import rectangle
from gdsfactory import Component
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.primitives.fet import nmos, pmos
from glayout.flow.placement.two_transistor_interdigitized import two_pfet_interdigitized
from four_transistor_interdigitized import generic_4T_interdigitzed
from glayout.flow.pdk.util.comp_utils import prec_ref_center
from glayout.flow.routing.smart_route import smart_route, c_route, straight_route, L_route
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
from glayout.flow.spice import Netlist
from glayout.flow.primitives.guardring import tapring
from glayout.flow.primitives.via_gen import via_stack, via_array

def x_coupled_netlist(nfetA: Component, nfetB: Component, pfetA: Component, pfetB: Component, nfetdum: Component, pfetdum: Component):
    x_coupled_netlist = Netlist(circuit_name ='cross_cpoupled_load', nodes=['VSN1', 'VSN2', 'VSP1', 'VSP2', 'VO1', 'VO2', 'VBULKN', 'VBULKP'])
    x_coupled_netlist.connect_netlist(
        nfetA.info['netlist'],
        [('G','VO1'), ('D','VO2'), ('S','VSN1'), ('B','VBULKN')]
    )
    x_coupled_netlist.connect_netlist(
        nfetdum.info['netlist'],
        [('G','VBULKN'), ('D','VBULKN'), ('S','VBULKN'), ('B','VBULKN')]
    )
    x_coupled_netlist.connect_netlist(
        pfetdum.info['netlist'],
        [('G','VBULKP'), ('D','VBULKP'), ('S','VBULKP'), ('B','VBULKP')]
    )
    x_coupled_netlist.connect_netlist(
        nfetB.info['netlist'],
        [('G','VO2'), ('D','VO1'), ('S','VSN2'), ('B','VBULKN')]
    )
    x_coupled_netlist.connect_netlist(
        pfetA.info['netlist'],
        [('G','VO1'), ('D','VO2'), ('S','VSP1'), ('B','VBULKP')]
    )
    x_coupled_netlist.connect_netlist(
        pfetB.info['netlist'],
        [('G','VO2'), ('D','VO1'), ('S','VSP2'), ('B','VBULKP')]
    )
    return x_coupled_netlist

def cross_coupled_load(pdk: MappedPDK, ccinv_col):
    cross_coupled_load=Component(name="cross_coupled_load")
    cross_couple = generic_4T_interdigitzed(pdk, numcols=ccinv_col, top_row_device="pfet", bottom_row_device="nfet", length=0.4, with_substrate_tap = False)
    cross_couple_ref = prec_ref_center(cross_couple)
    cross_coupled_load.add(cross_couple_ref)
    cross_coupled_load.add_ports(cross_couple_ref.get_ports_list(), prefix="cross_couple_")
    cross_coupled_load << smart_route(pdk,cross_coupled_load.ports["cross_couple_top_A_source_E"],cross_coupled_load.ports["cross_couple_top_B_source_E"],cross_couple_ref,cross_coupled_load)
    cross_coupled_load << c_route(pdk,cross_coupled_load.ports["cross_couple_top_A_drain_E"],cross_coupled_load.ports["cross_couple_top_B_gate_E"])
    cross_coupled_load << c_route(pdk,cross_coupled_load.ports["cross_couple_bottom_A_drain_E"],cross_coupled_load.ports["cross_couple_bottom_B_gate_E"])
    cross_coupled_load << c_route(pdk,cross_coupled_load.ports["cross_couple_top_B_drain_W"],cross_coupled_load.ports["cross_couple_top_A_gate_W"])
    cross_coupled_load << c_route(pdk,cross_coupled_load.ports["cross_couple_bottom_B_drain_W"],cross_coupled_load.ports["cross_couple_bottom_A_gate_W"])
    cross_coupled_load << c_route(pdk,cross_coupled_load.ports["cross_couple_top_B_gate_E"],cross_coupled_load.ports["cross_couple_bottom_A_drain_E"])
    cross_coupled_load << c_route(pdk,cross_coupled_load.ports["cross_couple_top_A_gate_W"],cross_coupled_load.ports["cross_couple_bottom_B_drain_W"])
    
    nfetA = nmos(pdk, width=3*ccinv_col, length=0.4, with_dummy=(False, False))
    nfetB = nmos(pdk, width=3*ccinv_col, length=0.4, with_dummy=(False, False))
    pfetA = pmos(pdk, width=3*ccinv_col, length=0.4, with_dummy=(False, False))
    pfetB = pmos(pdk, width=3*ccinv_col, length=0.4, with_dummy=(False, False))
    nfetdum = nmos(pdk, width=3*2, length=0.4, with_dummy=(False, False))
    pfetdum = pmos(pdk, width=3*2, length=0.4, with_dummy=(False, False))
    cross_coupled_load.info['netlist'] = x_coupled_netlist(nfetA, nfetB, pfetA, pfetB, nfetdum, pfetdum)
    return cross_coupled_load


def add_x_coupled_labels(x_coupled: Component):
    x_coupled.unlock()
    met1_label = (68, 5)
    met1_pin = (68, 16)
    move_info = list()
    #vo1 label
    vo1label = rectangle(layer=met1_pin, size=(0.05,0.05), centered=True).copy()
    vo1label.add_label(text="VO1",layer=met1_label)
    move_info.append((vo1label,x_coupled.ports["cross_couple_top_B_drain_N"],None))
    #vo2 label
    vo2label = rectangle(layer=met1_pin, size=(0.05,0.05), centered=True).copy()
    vo2label.add_label(text="VO2",layer=met1_label)
    move_info.append((vo2label,x_coupled.ports["cross_couple_top_A_drain_N"],None))
    #vsn1 label
    vsn1label = rectangle(layer=met1_pin, size=(0.05,0.05), centered=True).copy()
    vsn1label.add_label(text="VSN1",layer=met1_label)
    move_info.append((vsn1label,x_coupled.ports["cross_couple_bottom_A_source_N"],None))
    #vsn2 label
    vsn2label = rectangle(layer=met1_pin, size=(0.05,0.05), centered=True).copy()
    vsn2label.add_label(text="VSN2",layer=met1_label)
    move_info.append((vsn2label,x_coupled.ports["cross_couple_bottom_B_source_N"],None))
    #vsp1 label
    vsp1label = rectangle(layer=met1_pin, size=(0.05,0.05), centered=True).copy()
    vsp1label.add_label(text="VSP1",layer=met1_label)
    move_info.append((vsp1label,x_coupled.ports["cross_couple_top_A_source_N"],None))
    #vsp2 label
    vsp2label = rectangle(layer=met1_pin, size=(0.05,0.05), centered=True).copy()
    vsp2label.add_label(text="VSP2",layer=met1_label)
    move_info.append((vsp2label,x_coupled.ports["cross_couple_top_B_source_N"],None))
    #vbulk label
    vbulknlabel = rectangle(layer=met1_pin, size=(0.05,0.05), centered=True).copy()
    vbulknlabel.add_label(text="VBULKN",layer=met1_label)
    move_info.append((vbulknlabel,x_coupled.ports["cross_couple_bottom_welltie_N_top_met_N"],None))
    #vbulk label
    vbulkplabel = rectangle(layer=met1_pin, size=(0.05,0.05), centered=True).copy()
    vbulkplabel.add_label(text="VBULKP",layer=met1_label)
    move_info.append((vbulkplabel,x_coupled.ports["cross_couple_top_welltie_N_top_met_N"],None))
    #move everything to position
    for comp, prt, alignment in move_info:
        alignment = ('c','b') if alignment is None else alignment
        compref = align_comp_to_port(comp, prt, alignment=alignment)
        x_coupled.add(compref)
    return x_coupled.flatten()
