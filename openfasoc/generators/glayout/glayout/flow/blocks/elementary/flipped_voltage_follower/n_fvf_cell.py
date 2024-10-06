from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
from gdsfactory.component import Component
from gdsfactory.cell import cell
from gdsfactory import Component
from glayout.flow.primitives.fet import nmos, pmos, multiplier
from pmos_lvt import pmos_lvt
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, prec_center
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

         netlist = Netlist(circuit_name='Voltage_Shifter_N_FVF_Cell ', nodes=['VCC', 'VIN', 'GND', 'VOUT', 'IBIAS', 'Ib'])
         netlist.connect_netlist(n_fvf.info['netlist'], [('VIN', 'VIN'), ('GND', 'GND'), ('VOUT', 'VOUT'), ('Ib', 'Ib')])
         netlist.connect_netlist(c_mirr.info['netlist'], [('VCC', 'VCC'), ('Iin', 'IBIAS'), ('Iout', 'Ib')])

         return netlist

@cell
def  n_fvf_cell(
        pdk: MappedPDK,
        width: tuple[float,float,float] = (3.756,1.175,1.118),
        length: tuple[float,float,float] = (3,0.6,2.5),
        fingers: tuple[int,int,int] = (1,1,1),
        multipliers: tuple[int,int,int] = (1,1,1),
        dummy_1: tuple[bool,bool] = (True,True),
        dummy_2: tuple[bool,bool] = (True,True),
        substrate_tap: bool = False,
        tie_layers: tuple[str,str] = ("met2","met1"),
        ) -> Component:
   
    #top level component
    top_level = Component("Voltage_Shifter_N_FVF_Cell")

    n_fvf = flipped_voltage_follower(pdk, width=(width[1],width[2]), length=(length[1],length[2]), fingers=(fingers[1],fingers[2]), multipliers=(multipliers[1],multipliers[2]), dummy_1=dummy_1, dummy_2=dummy_2)
    n_fvf_ref = top_level << n_fvf
     

    #Relative move
    ref_dimensions = evaluate_bbox(n_fvf)
    
    #add current bias
    c_mirr = pmos_lvt_cmirror(pdk, width=width[0], length=length[0], fingers=fingers[0], multipliers=multipliers[0])
    c_mirr_ref = top_level << c_mirr
    c_mirr_ref = rename_ports_by_orientation(c_mirr_ref.mirror_y())
    c_mirr_ref.movey(1.2 * ref_dimensions[1] + pdk.util_max_metal_seperation())
    c_mirr_ref.movex(pdk.util_max_metal_seperation()/2)
    top_level << L_route(pdk, c_mirr_ref.ports["B1_drain_top_met_S"], n_fvf_ref.ports["A_multiplier_0_drain_E"])
    top_level << straight_route(pdk, c_mirr_ref.ports["B_2_multiplier_0_source_E"], c_mirr_ref.ports["tie_E_top_met_E"], glayer1='met1')
    
    top_level.add_ports(n_fvf_ref.get_ports_list(), prefix="n_fvf_")
    top_level.add_ports(c_mirr_ref.get_ports_list(), prefix="mirror_")
    
    #add dnwell
    top_level.add_padding(layers=(pdk.get_glayer("dnwell"),),default=pdk.get_grule("pwell", "dnwell")["min_enclosure"]+1, )
    
    component = component_snap_to_grid(rename_ports_by_orientation(top_level))

    correctionxy = prec_center(component)
    component.movex(correctionxy[0]).movey(correctionxy[1])             

    component.info['netlist'] = n_fvf_cell_netlist(n_fvf, c_mirr)

    print(component.info['netlist'].generate_netlist(only_subcircuits=True))

    #lvs_result = pdk.lvs_netgen(layout=component, design_name="fvf_cell", lvs_schematic_ref_file="/home/spal/layout/fvf.spice", output_file_path="/home/spal/layout/lvs/fvf.rpt")
    
    return component

#n_fvf_cell(sky130_mapped_pdk).show()
