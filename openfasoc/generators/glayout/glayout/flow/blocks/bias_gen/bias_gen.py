# Primitives
from glayout.flow.primitives.fet import pmos
from glayout.flow.primitives.fet import nmos

from glayout.flow.primitives.guardring import tapring

# Standard
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.gf180_mapped import gf180_mapped_pdk
from gdsfactory import Component

# Utility
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, prec_center

# Routing
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route

def bias_gen(pdk: MappedPDK):
    # Create a top level component
    bias_gen = Component()

    # Bias Generator requires two NFETs of different thresholds. Retain dummies on east and west sides
    nfet_M1 = nmos(pdk, with_substrate_tap=False, with_dummy=(True, True))
    nfet_M2 = nmos(pdk, with_substrate_tap=False, with_dummy=(True, True))
    bias_gen_M1 = bias_gen << nfet_M1
    bias_gen_M2 = bias_gen << nfet_M2

    # Relative Movement of the M1 transistor so that it doesn't overlap on M2
    M2_dimension = evaluate_bbox(nfet_M2)
    bias_gen_M1.movex(-M2_dimension[0]-pdk.util_max_metal_seperation())
    

    # Routing 
    ## Route the Gate from M1 to M2
    bias_gen << straight_route(pdk, bias_gen_M1.ports["multiplier_0_gate_E"], bias_gen_M2.ports["multiplier_0_gate_W"])
    ## Route the Drain to Gate of M2
    bias_gen << c_route(pdk, bias_gen_M2.ports["multiplier_0_drain_E"], bias_gen_M2.ports["multiplier_0_gate_E"])
    ## Calculate the centre of the bias_gen component so that the tapring could be centered around the component. 
    shift_amount = -prec_center(bias_gen.flatten())[0]

    tap_ring = tapring(pdk, enclosed_rectangle=evaluate_bbox(bias_gen.flatten(), padding=pdk.util_max_metal_seperation()))
    tap_ring_ref = bias_gen << tap_ring
    tap_ring_ref.movex(shift_amount)

    return bias_gen

bias_gen(gf180_mapped_pdk).show()
