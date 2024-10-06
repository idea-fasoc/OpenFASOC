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
from glayout.flow.primitives.via_gen import via_stack

def pmos_lvt_cmirror_netlist(
        pdk: MappedPDK,
        width: float,
        length: float,
        fingers: int,
        multipliers: int
        ) -> Netlist:

         netlist = Netlist(circuit_name='PMOS_lvt_current_mirror', nodes=['VCC', 'Iin', 'Iout'])
         fet_1 = pmos_lvt(pdk, width=width, fingers=fingers, multipliers=2*multipliers, dummy=(True,False), length=length)
         fet_2 = pmos_lvt(pdk, width=width, fingers=fingers, multipliers=2*multipliers, dummy=(False,False), length=length)
         netlist.connect_netlist(fet_1.info['netlist'], [('D', 'Iin'), ('G', 'Iin'), ('S', 'VCC'), ('B', 'VCC')]) 
         netlist.connect_netlist(fet_2.info['netlist'], [('D', 'Iout'), ('G', 'Iin'), ('S', 'VCC'), ('B', 'VCC')]) 

         return netlist                  

@cell
def pmos_lvt_cmirror(     
        pdk: MappedPDK,
        width: float=3,
        length:float=0.15,
        fingers: int=1,
        multipliers: int=1,
        with_tie: bool=True,
        with_substrate_tap: bool=False,
        tie_layers: tuple[str,str]=('met2','met1')             
        ) -> Component:
    

    top_level = Component("A_B_A_B")
    
    fet_A_1 = pmos_lvt(pdk, width=width/2, fingers=fingers, multipliers=multipliers, dummy=(True,False), length=length)
    fet_A_2 = pmos_lvt(pdk, width=width/2, fingers=fingers, multipliers=multipliers, dummy=(False,False), length=length)
    fet_B_1 = pmos_lvt(pdk, width=width/2, fingers=fingers, multipliers=multipliers, dummy=(False,False), length=length)
    fet_B_2 = pmos_lvt(pdk, width=width/2, fingers=fingers, multipliers=multipliers, dummy=(False,True), length=length)
    fet_A_1_ref = top_level << fet_A_1
    fet_A_2_ref = top_level << fet_A_2
    fet_B_1_ref = top_level << fet_B_1
    fet_B_2_ref = top_level << fet_B_2
    
    ref_dimensions_1 = evaluate_bbox(fet_A_1)
    ref_dimensions_2 = evaluate_bbox(fet_A_2)
    fet_B_1_ref.movex(ref_dimensions_1[0]/2 + ref_dimensions_2[0]/2)
    fet_A_2_ref.movex(ref_dimensions_1[0]/2 + 3*ref_dimensions_2[0]/2)
    fet_B_2_ref.movex(ref_dimensions_1[0] + 2*ref_dimensions_2[0])

    top_level << straight_route(pdk, fet_A_1_ref.ports["multiplier_0_source_E"], fet_B_1_ref.ports["multiplier_0_source_W"])
    top_level << straight_route(pdk, fet_B_1_ref.ports["multiplier_0_source_E"], fet_A_2_ref.ports["multiplier_0_source_W"])
    top_level << straight_route(pdk, fet_A_2_ref.ports["multiplier_0_source_E"], fet_B_2_ref.ports["multiplier_0_source_W"])
    top_level << straight_route(pdk, fet_A_1_ref.ports["multiplier_0_gate_E"], fet_B_1_ref.ports["multiplier_0_gate_W"])
    top_level << straight_route(pdk, fet_B_1_ref.ports["multiplier_0_gate_E"], fet_A_2_ref.ports["multiplier_0_gate_W"])
    top_level << straight_route(pdk, fet_A_2_ref.ports["multiplier_0_gate_E"], fet_B_2_ref.ports["multiplier_0_gate_W"])

    top_level.add_ports(fet_A_1.get_ports_list(), prefix='A_1_')
    top_level.add_ports(fet_A_2.get_ports_list(), prefix='A_2_')
    top_level.add_ports(fet_B_1.get_ports_list(), prefix='B_1_')                  
    top_level.add_ports(fet_B_2.get_ports_list(), prefix='B_2_')
    
    viam2m3 = via_stack(pdk,"met2","met3",centered=True)
 
    drain_A1_via = top_level << viam2m3
    drain_A2_via = top_level << viam2m3
    drain_B1_via = top_level << viam2m3
    drain_B2_via = top_level << viam2m3

    drain_A1_via.move(fet_A_1_ref.ports["multiplier_0_drain_W"].center).movex(-1.2)
    drain_A2_via.move(fet_A_2_ref.ports["multiplier_0_drain_W"].center).movex(-0.3)
    drain_B1_via.move(fet_B_1_ref.ports["multiplier_0_drain_W"].center).movex(-0.3)
    drain_B2_via.move(fet_B_2_ref.ports["multiplier_0_drain_E"].center).movex(0.5)

    top_level << straight_route(pdk, fet_A_2_ref.ports["multiplier_0_drain_W"], drain_A2_via.ports["bottom_met_E"])
    top_level << straight_route(pdk, fet_A_1_ref.ports["multiplier_0_drain_E"], drain_A1_via.ports["bottom_met_W"])
    top_level << c_route(pdk, drain_A1_via.ports["top_met_N"], drain_A2_via.ports["top_met_N"], extension=1.5, e1glayer='met3', e2glayer='met3', cglayer='met2')
    top_level << c_route(pdk, drain_A1_via.ports["bottom_met_W"], fet_A_1_ref.ports["multiplier_0_gate_W"], width2=0.3)
 
    top_level << straight_route(pdk, fet_B_1_ref.ports["multiplier_0_drain_W"], drain_B1_via.ports["bottom_met_E"])
    top_level << straight_route(pdk, fet_B_2_ref.ports["multiplier_0_drain_E"], drain_B2_via.ports["bottom_met_W"])
    top_level << c_route(pdk, drain_B1_via.ports["top_met_N"], drain_B2_via.ports["top_met_N"], extension=0.8, cglayer='met2')

    top_level.add_ports(drain_A1_via.get_ports_list(), prefix='A1_drain_')
    top_level.add_ports(drain_A2_via.get_ports_list(), prefix='A2_drain_')
    top_level.add_ports(drain_B1_via.get_ports_list(), prefix='B1_drain_')
    top_level.add_ports(drain_B2_via.get_ports_list(), prefix='B2_drain_')

    tap_separation = max(
            pdk.get_grule("met2")["min_separation"],
            pdk.get_grule("met1")["min_separation"],
            pdk.get_grule("active_diff", "active_tap")["min_separation"],
        )
    tap_separation += pdk.get_grule("n+s/d", "active_tap")["min_enclosure"]
    tap_encloses = (
            1.5 * (tap_separation + top_level.xmax),
            2* (tap_separation + top_level.ymax),
        )
    tapring_ref = top_level << tapring(
            pdk,
            enclosed_rectangle=tap_encloses,
            sdlayer="n+s/d",
            horizontal_glayer=tie_layers[0],
            vertical_glayer=tie_layers[1],
        )
    tapring_ref.movex(ref_dimensions_1[0]/2 + ref_dimensions_2[0])
    top_level.add_ports(tapring_ref.get_ports_list(),prefix="tie_")
    top_level << straight_route(pdk, fet_A_1_ref.ports["multiplier_0_dummy_L_gsdcon_top_met_W"], top_level.ports["tie_W_top_met_W"], glayer1='met1')
    top_level << straight_route(pdk, fet_B_2_ref.ports["multiplier_0_dummy_R_gsdcon_top_met_E"], top_level.ports["tie_E_top_met_E"], glayer1='met1')
    top_level << straight_route(pdk, fet_A_1_ref.ports["multiplier_0_source_W"], top_level.ports["tie_W_top_met_W"], glayer1='met1')

       
    if with_substrate_tap:
      substrate_tap_separation = pdk.get_grule("dnwell", "active_tap")["min_separation"]
      substrate_tap_encloses =(1.5 * (substrate_tap_separation + top_level.xmax), 2 * (substrate_tap_separation + top_level.ymax))
      guardring_ref = top_level << tapring(
            pdk,
            enclosed_rectangle=substrate_tap_encloses,
            sdlayer="p+s/d",
            horizontal_glayer='met2',
            vertical_glayer='met1',
        )
      guardring_ref.movex(ref_dimensions_1[0]/2 + ref_dimensions_2[0])

    top_level.add_padding(
            layers=(pdk.get_glayer("nwell"),),
            default=pdk.get_grule("active_tap", "nwell")["min_enclosure"],
            )


    top_level = component_snap_to_grid(rename_ports_by_orientation(top_level))
    comp = Component()
    compref = comp << top_level
    correctionxy = prec_center(compref)
    compref.movex(correctionxy[0]).movey(correctionxy[1])
    comp.add_ports(compref.get_ports_list())         


    comp.info['netlist'] = pmos_lvt_cmirror_netlist(pdk, width/2, length, fingers, multipliers)

    #print(comp.info['netlist'].generate_netlist(only_subcircuits=True))
    #component.write_gds("/home/spal/layout/pcmirr.gds")

    #lvs_result = pdk.lvs_netgen(layout=component, pdk_root="/home/spal/.volare/", design_name="p_lvt_cmirr", lvs_schematic_ref_file="/home/spal/layout/cmirr.spice", output_file_path="/home/spal/layout/lvs/cmirr.rpt")

    return component_snap_to_grid(rename_ports_by_orientation(comp))
    
pmos_lvt_cmirror(sky130_mapped_pdk).show()
