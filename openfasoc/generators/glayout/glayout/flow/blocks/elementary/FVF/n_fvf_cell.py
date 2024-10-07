from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
from gdsfactory.component import Component
from gdsfactory.cell import cell
from gdsfactory import Component
from gdsfactory.components import text_freetype, rectangle
from glayout.flow.primitives.fet import nmos, pmos, multiplier
from pmos_lvt import pmos_lvt
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, prec_center, align_comp_to_port, prec_ref_center
from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid
from glayout.flow.pdk.util.port_utils import rename_ports_by_orientation
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.primitives.guardring import tapring
from glayout.flow.pdk.util.port_utils import add_ports_perimeter
from glayout.flow.spice.netlist import Netlist
from p_lvt_cmirr import pmos_lvt_cmirror
from fvf import fvf_netlist, flipped_voltage_follower
from glayout.flow.primitives.via_gen import via_stack

def n_fvf_cell_netlist(n_fvf: Component, c_mirr: Component) -> Netlist:

         netlist = Netlist(circuit_name='Voltage_Shifter_N_FVF_Cell ', nodes=['VCC', 'VIN', 'GND', 'VOUT', 'IBIAS'])
         n_fvf_ref=netlist.connect_netlist(n_fvf.info['netlist'], [])
         cmirr_ref=netlist.connect_netlist(c_mirr.info['netlist'], [('Iin', 'IBIAS')])
         netlist.connect_subnets(
                 n_fvf_ref,
                 cmirr_ref,
                 [('Ib', 'Iout')]
                 )

         return netlist

def sky130_add_voltage_shifter_labels(fvf_in: Component) -> Component:
	
    fvf_in.unlock()
    # define layers
    met2_pin = (69,16)
    met2_label = (69,5)
    met3_pin = (70,16)
    met3_label = (70,5)
    met4_pin = (71,16)
    met4_label = (71,5)
    # list that will contain all port/comp info
    move_info = list()
    # create labels and append to info list
    # gnd
    gndlabel = rectangle(layer=met3_pin,size=(1,1),centered=True).copy()
    gndlabel.add_label(text="GND",layer=met3_label)
    move_info.append((gndlabel,fvf_in.ports["pin_ground_top_met_N"],None))
    #currentbias
    ibias1label = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
    ibias1label.add_label(text="IBIAS",layer=met2_label)
    move_info.append((ibias1label,fvf_in.ports["pin_Ibias_top_met_N"],None))
    #ibias2label = rectangle(layer=met4_pin,size=(1,1),centered=True).copy()
    #ibias2label.add_label(text="Ib",layer=met4_label)
    #move_info.append((ibias2label,fvf_in.ports["pin_int_top_met_N"],None))
    #vcc
    vcclabel = rectangle(layer=met3_pin,size=(1,1),centered=True).copy()
    vcclabel.add_label(text="VCC",layer=met3_label)
    move_info.append((vcclabel,fvf_in.ports["pin_VCC_top_met_N"],None))
    # output (3rd stage)
    outputlabel = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
    outputlabel.add_label(text="VOUT",layer=met2_label)
    move_info.append((outputlabel,fvf_in.ports["pin_output_top_met_N"],None))
    # input
    inputlabel = rectangle(layer=met4_pin,size=(1,1),centered=True).copy()
    inputlabel.add_label(text="VIN",layer=met4_label)
    move_info.append((inputlabel,fvf_in.ports["pin_input_top_met_N"], None))
    # move everything to position
    for comp, prt, alignment in move_info:
        alignment = ('c','b') if alignment is None else alignment
        compref = align_comp_to_port(comp, prt, alignment=alignment)
        fvf_in.add(compref)
    return fvf_in.flatten() 

@cell
def  n_fvf_cell(
        pdk: MappedPDK,
        width: tuple[float,float,float] = (3.756,1.175,1.118),
        length: tuple[float,float,float] = (3,0.6,2.5),
        fingers: tuple[int,int,int] = (1,1,1),
        multipliers: tuple[int,int,int] = (1,1,1),
        dummy_1: tuple[bool,bool] = (True,True),
        dummy_2: tuple[bool,bool] = (True,True),
        dnwell: bool = True,
        ) -> Component:
   
    #top level component
    top_level = Component("Voltage_Shifter_N_FVF_Cell")

    n_fvf = flipped_voltage_follower(pdk, width=(width[1],width[2]), length=(length[1],length[2]), fingers=(fingers[1],fingers[2]), multipliers=(multipliers[1],multipliers[2]), dummy_1=dummy_1, dummy_2=dummy_2)
    n_fvf_ref = top_level << n_fvf
     

       
    #add current bias
    c_mirr = pmos_lvt_cmirror(pdk, width=width[0], length=length[0], fingers=fingers[0], multipliers=multipliers[0])
    c_mirr_ref = top_level << c_mirr
    c_mirr_ref = rename_ports_by_orientation(c_mirr_ref.mirror_y())
    
    #Relative move
    ref_dimensions_1 = evaluate_bbox(n_fvf)
    ref_dimensions_2 = evaluate_bbox(c_mirr)
    
    c_mirr_ref.movey(max(ref_dimensions_1[1], ref_dimensions_2[1]) + pdk.util_max_metal_seperation())
    n_fvf_ref.movey(min(ref_dimensions_1[1], ref_dimensions_2[1]) - max(ref_dimensions_1[1], ref_dimensions_2[1]))
    
    top_level << L_route(pdk, c_mirr_ref.ports["B1_drain_top_met_S"], n_fvf_ref.ports["A_multiplier_0_drain_E"])
    
        #add dnwell
    if dnwell:
         top_level.add_padding(layers=(pdk.get_glayer("dnwell"),),default=pdk.get_grule("pwell", "dnwell")["min_enclosure"]+1, )
    
    viam2m3 = via_stack(pdk, "met2", "met3", centered=True)
    #viam1m2 = via_stack(pdk, "met1", "met2", centered=True)
    VCC_via = top_level << viam2m3
    VIN_via = top_level << viam2m3
    GND_via = top_level << viam2m3
    VOUT_via = top_level << viam2m3
    IBIAS_via = top_level << viam2m3
    #Ib_via = top_level << viam2m3
    
    VCC_via.move(c_mirr_ref.ports["tie_W_top_met_W"].center).movex(-2)
    VIN_via.move(n_fvf_ref.ports["A_multiplier_0_gate_E"].center).movex(5)
    GND_via.move(n_fvf_ref.ports["B_tie_E_top_met_E"].center).movex(5)
    VOUT_via.move(n_fvf_ref.ports["B_multiplier_0_drain_E"].center).movex(12)
    IBIAS_via.move(c_mirr_ref.ports["A1_drain_top_met_W"].center).movex(-12)
    #Ib_via.move(c_mirr_ref.ports["B2_drain_top_met_E"].center).movex(1)

    top_level << straight_route(pdk, VCC_via.ports["bottom_met_E"], c_mirr_ref.ports["tie_W_top_met_W"], glayer1='met2', glayer2='met1') 
    top_level << straight_route(pdk, VIN_via.ports["bottom_met_W"], n_fvf_ref.ports["A_multiplier_0_gate_E"], glayer1='met2') 
    top_level << straight_route(pdk, GND_via.ports["bottom_met_W"], n_fvf_ref.ports["B_tie_E_top_met_E"], glayer1='met2', glayer2='met1') 
    top_level << straight_route(pdk, VOUT_via.ports["bottom_met_W"], n_fvf_ref.ports["B_multiplier_0_drain_E"], glayer1='met2') 
    top_level << straight_route(pdk, IBIAS_via.ports["bottom_met_E"], c_mirr_ref.ports["A1_drain_top_met_W"], glayer1='met2')
    #top_level << straight_route(pdk, Ib_via.ports["bottom_met_W"], c_mirr_ref.ports["B2_drain_top_met_E"], glayer1='met2') 
    
    top_level.add_ports(n_fvf_ref.get_ports_list(), prefix="n_fvf_")
    top_level.add_ports(c_mirr_ref.get_ports_list(), prefix="mirror_")
    top_level.add_ports(VCC_via.get_ports_list(), prefix="pin_VCC_")
    top_level.add_ports(VIN_via.get_ports_list(), prefix="pin_input_")
    top_level.add_ports(GND_via.get_ports_list(), prefix="pin_ground_")
    top_level.add_ports(VOUT_via.get_ports_list(), prefix="pin_output_")
    top_level.add_ports(IBIAS_via.get_ports_list(), prefix="pin_Ibias_")
    #top_level.add_ports(Ib_via.get_ports_list(), prefix="pin_int_")
    
    top_level = component_snap_to_grid(rename_ports_by_orientation(top_level))
    comp = Component()
    compref = comp << top_level
    correctionxy = prec_center(compref)
    compref.movex(correctionxy[0]).movey(correctionxy[1])
    comp.add_ports(compref.get_ports_list())         

    
    comp.info['netlist'] = n_fvf_cell_netlist(n_fvf, c_mirr)

    print(comp.info['netlist'].generate_netlist(only_subcircuits=True))

    #lvs_result = pdk.lvs_netgen(layout=component, design_name="fvf_cell", lvs_schematic_ref_file="/home/spal/layout/fvf.spice", output_file_path="/home/spal/layout/lvs/fvf.rpt")
     
    return component_snap_to_grid(rename_ports_by_orientation(comp))

nfvf = sky130_add_voltage_shifter_labels(n_fvf_cell(sky130_mapped_pdk))
nfvf.show()
magic_drc_result = sky130_mapped_pdk.drc_magic(nfvf, nfvf.name)
if magic_drc_result:
     print("DRC is clean: ", magic_drc_result)
else:
     print("DRC failed. Please try again.")
nfvf.name ='nfvf_lvs' 
netgen_lvs_result = sky130_mapped_pdk.lvs_netgen(nfvf, 'nfvf_lvs')
print(f"LVS results", netgen_lvs_result)
