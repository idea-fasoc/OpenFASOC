from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
from gdsfactory.cell import cell
from gdsfactory.component import Component
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

def fvf_netlist(fet_1: Component, fet_2: Component) -> Netlist:

         netlist = Netlist(circuit_name='FLIPPED_VOLTAGE_FOLLOWER', nodes=['VIN', 'GND', 'VOUT', 'Ib'])
         netlist.connect_netlist(fet_1.info['netlist'], [('D', 'Ib'), ('G', 'VIN'), ('S', 'VOUT'), ('B', 'VOUT')])
         netlist.connect_netlist(fet_2.info['netlist'], [('D', 'VOUT'), ('G', 'Ib'), ('S', 'GND'), ('B', 'GND')])

         return netlist

@cell
def  flipped_voltage_follower(
        pdk: MappedPDK,
        device_type: str = "nmos",
        width: tuple[float,float] = (3,3),
        length: tuple[float,float] = (None,1),
        fingers: tuple[int,int] = (1,1),
        multipliers: tuple[int,int] = (1,1),
        dummy_1: tuple[bool,bool] = (True,True),
        dummy_2: tuple[bool,bool] = (True,True),
        substrate_tap: bool = False,
        tie_layers: tuple[str,str] = ("met2","met1"),
        ) -> Component:
   
    #top level component
    top_level = Component(name="flipped_voltage_follower")

    #two fets
    if device_type == "nmos":
        fet_1 = nmos(pdk, width=width[0], fingers=fingers[0], multipliers=multipliers[0], with_dummy=dummy_1, with_dnwell=False,  with_substrate_tap=False, length=length[0])
        fet_2 = nmos(pdk, width=width[1], fingers=fingers[1], multipliers=multipliers[1], with_dummy=dummy_2, with_dnwell=False,  with_substrate_tap=False, length=length[1])
        well = "pwell"
    elif device_type == "pmos":
        fet_1 = pmos(pdk, width=width[0], fingers=fingers[0], multipliers=multipliers[0], with_dummy=dummy_1, with_substrate_tap=False, length=length[0])
        fet_2 = pmos(pdk, width=width[1], fingers=fingers[1], multipliers=multipliers[1], with_dummy=dummy_2, with_substrate_tap=False, length=length[1])
        well = "nwell"
    fet_1_ref = top_level << fet_1
    fet_2_ref = top_level << fet_2 

    #Relative move
    ref_dimensions = max(evaluate_bbox(fet_1), evaluate_bbox(fet_2))
    fet_2_ref.movex(ref_dimensions[0] + pdk.util_max_metal_seperation())
    
    #Routing
    viam2m3 = via_stack(pdk, "met2", "met3", centered=True)
    drain_1_via = top_level << viam2m3
    source_1_via = top_level << viam2m3
    drain_2_via = top_level << viam2m3
    gate_2_via = top_level << viam2m3
    drain_1_via.move(fet_1_ref.ports["multiplier_0_drain_W"].center).movex(-4)
    source_1_via.move(fet_1_ref.ports["multiplier_0_source_E"].center).movex(0.3)
    drain_2_via.move(fet_2_ref.ports["multiplier_0_drain_W"].center).movex(-0.3)
    gate_2_via.move(fet_2_ref.ports["multiplier_0_gate_S"].center).movey(-0.3)

    top_level << straight_route(pdk, fet_1_ref.ports["multiplier_0_source_E"], source_1_via.ports["bottom_met_W"])
    top_level << straight_route(pdk, fet_2_ref.ports["multiplier_0_drain_W"], drain_2_via.ports["bottom_met_E"])
    top_level << c_route(pdk, source_1_via.ports["top_met_N"], drain_2_via.ports["top_met_N"], extension=1.2, width1=0.32, width2=0.32, cwidth=0.32, e1glayer="met3", e2glayer="met3", cglayer="met2")
    top_level << straight_route(pdk, fet_1_ref.ports["multiplier_0_drain_W"], drain_1_via.ports["bottom_met_E"])
    top_level << c_route(pdk, drain_1_via.ports["top_met_S"], gate_2_via.ports["top_met_S"], extension=1, cglayer="met2")
    top_level << straight_route(pdk, fet_2_ref.ports["multiplier_0_gate_S"], gate_2_via.ports["bottom_met_N"])
    top_level << straight_route(pdk, fet_1_ref.ports["multiplier_0_source_W"], fet_1_ref.ports["tie_W_top_met_W"], glayer1=tie_layers[1])
    top_level << straight_route(pdk, fet_2_ref.ports["multiplier_0_source_W"], fet_2_ref.ports["tie_W_top_met_W"], glayer1=tie_layers[1])
    
    #Renaming Ports
    top_level.add_ports(fet_1_ref.get_ports_list(), prefix="A_")
    top_level.add_ports(fet_2_ref.get_ports_list(), prefix="B_")
    top_level.add_ports(drain_1_via.get_ports_list(), prefix="A_drain_")
    top_level.add_ports(source_1_via.get_ports_list(), prefix="A_source_")
    top_level.add_ports(drain_2_via.get_ports_list(), prefix="B_drain_")
    top_level.add_ports(gate_2_via.get_ports_list(), prefix="B_gate_")
    #add dnwell
    top_level.add_padding(layers=(pdk.get_glayer("dnwell"),),default=pdk.get_grule("pwell", "dnwell")["min_enclosure"]+1, )

    #substrate tap
    if substrate_tap:
            if well == "pwell":
                tapref = top_level << tapring(pdk,evaluate_bbox(top_level,padding=1),sdlayer="n+s/d", horizontal_glayer="met1")
            else:
                tapref = top_level << tapring(pdk,evaluate_bbox(top_level,padding=1),sdlayer="p+s/d", horizontal_glayer="met1")
            tapref.movex(ref_dimensions[0]/2)
            top_level.add_ports(tapref.get_ports_list(),prefix="tap_")
            try:
                top_level<<straight_route(pdk,fet_1_ref.ports["multiplier_0_dummy_A_gsdcon_top_met_W"],top_level.ports["tap_W_top_met_W"],glayer2="met1")
            except KeyError:
                pass
            try:     
                top_level<<straight_route(pdk,fet_2_ref.ports["multiplier_0_dummy_B_gsdcon_top_met_W"],top_level.ports["tap_E_top_met_E"],glayer2="met1")
            except KeyError:
                pass
    
    
    top_level = component_snap_to_grid(rename_ports_by_orientation(top_level))
    comp = Component()
    compref = comp << top_level
    correctionxy = prec_center(compref)
    compref.movex(correctionxy[0]).movey(correctionxy[1])
    comp.add_ports(compref.get_ports_list())         

    comp.info['netlist'] = fvf_netlist(fet_1, fet_2)

    #print(component.info['netlist'].generate_netlist(only_subcircuits=True))
    
    #component.write_gds("/home/spal/layout/fcell.gds")

    #lvs_result = pdk.lvs_netgen(layout=component, design_name="fvf", lvs_schematic_ref_file="/home/spal/layout/fvf.spice", output_file_path="/home/spal/layout/lvs/fvf.rpt")
    
    return component_snap_to_grid(rename_ports_by_orientation(comp))

flipped_voltage_follower(sky130_mapped_pdk).show()
