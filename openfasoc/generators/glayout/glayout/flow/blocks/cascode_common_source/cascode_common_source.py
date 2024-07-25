from gdsfactory import Component
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.placement.two_transistor_interdigitized import two_nfet_interdigitized
from glayout.flow.placement.two_transistor_interdigitized import two_pfet_interdigitized
from glayout.flow.primitives.fet import pmos
from glayout.flow.primitives.fet import nmos
from glayout.flow.primitives.guardring import tapring

from glayout.flow.pdk.util.comp_utils import prec_ref_center, prec_center, movey, evaluate_bbox
from glayout.flow.pdk.util.port_utils import remove_ports_with_prefix
from glayout.flow.routing.smart_route import smart_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.straight_route import straight_route

from glayout.flow.pdk.gf180_mapped import gf180_mapped_pdk
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk

def Cascode_CS(pdk: MappedPDK, L1, W1, L2, W2, cs_type="nfet"):
    Cascode_CS = Component(name="Cascode_cs")

    # Add two nfets for the cascode. 
    if (cs_type=="nfet"):
        fet_M1=nmos(pdk, length=L1, width=W1, with_tie=False)#, sd_route_topmet="met3", gate_route_topmet="met3")
        fet_M2=nmos(pdk, length=L2, width=W2, with_tie=False)#, sd_route_topmet="met3", gate_route_topmet="met3")
    elif (cs_type=="pfet"):
        fet_M1=pmos(pdk, length=L1, width=W1)
        fet_M2=pmos(pdk, length=L2, width=W2)

    # Generate a reference to M1, M2 for placement and routing
    M1_ref = prec_ref_center(fet_M1)
    Cascode_CS.add(M1_ref)
    Cascode_CS.add_ports(M1_ref.get_ports_list(), prefix="M1_")
    M2_ref = prec_ref_center(fet_M2)
    Cascode_CS.add(M2_ref)
    Cascode_CS.add_ports(M2_ref.get_ports_list(), prefix="M2_")

    # Get dimensions of M1, M2 for displacing M1 above M2
    M1_dim = prec_ref_center(M1_ref)
    M2_dim = prec_ref_center(M2_ref)
    movey(M2_ref, 0.5*(evaluate_bbox(M1_ref)[1]+evaluate_bbox(M2_ref)[1]) + pdk.util_max_metal_seperation())
    # Remove ports and add them after moving a component as positions need to be updated from the movement
    remove_ports_with_prefix(Cascode_CS, "M2_")
    Cascode_CS.add_ports(M2_ref.get_ports_list(), prefix="M2_")

    # Routing the Source of M2 to drain of M1:
    Cascode_CS << smart_route(pdk,
                                Cascode_CS.ports["M1_multiplier_0_drain_N"],
                                Cascode_CS.ports["M2_multiplier_0_source_S"],
                                M1_ref, M2_ref) 
    
    # Add a guard tap ring around the cascode
    shift_amount = -prec_center(Cascode_CS.flatten())[1]
    tap_ring = tapring(pdk, 
                        enclosed_rectangle=evaluate_bbox(Cascode_CS.flatten(), padding=pdk.util_max_metal_seperation()))
    tap_ring_ref = Cascode_CS << tap_ring
    tap_ring_ref.movey(shift_amount)

    return Cascode_CS

mapped_pdk_build = sky130_mapped_pdk
Cascode_cs_component = Cascode_CS(mapped_pdk_build,2,3,4,6, cs_type="pfet")
Cascode_cs_component.show()

magic_drc_result = sky130_mapped_pdk.drc_magic(Cascode_cs_component, Cascode_cs_component.name)
if magic_drc_result :
    print("DRC is clean: ", magic_drc_result)
else:
    print("DRC failed. Please try again.")