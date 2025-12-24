from gdsfactory import Component
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.flow.primitives.fet import nmos
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route

def create_nmos_latch_layout(pdk):
    latch = Component("nmos_latch")
    # Create and configure NMOS transistors
    m2 = latch << nmos(pdk, width=1, length=0.15)
    m7 = latch << nmos(pdk, width=1, length=0.15)
    m3 = latch << nmos(pdk, width=2, length=0.15)
    m4 = latch << nmos(pdk, width=2, length=0.15)
    m5 = latch << nmos(pdk, width=2, length=0.15)
    m6 = latch << nmos(pdk, width=2, length=0.15)
    m8 = latch << nmos(pdk, width=2, length=0.15)
    
    # Positioning and routing logic
    spacing = pdk.util_max_metal_seperation() + m2.size[0]
    m7.movex(6 * spacing)
    m3.movex(2 * spacing)
    m4.movex(3 * spacing)
    m5.movex(4 * spacing)
    m6.movex(5 * spacing)
    m8.movex(spacing)

    # Routing and connections
    latch << straight_route(pdk, m2.ports["multiplier_0_drain_E"], m8.ports["multiplier_0_source_E"])
    latch << straight_route(pdk, m7.ports["multiplier_0_drain_E"], m6.ports["multiplier_0_source_E"])
    latch << straight_route(pdk, m3.ports["multiplier_0_drain_E"], m4.ports["multiplier_0_drain_E"])
    latch << straight_route(pdk, m4.ports["multiplier_0_drain_E"], m5.ports["multiplier_0_drain_E"])
    latch << straight_route(pdk, m3.ports["multiplier_0_gate_E"], m4.ports["multiplier_0_gate_E"])
    latch << straight_route(pdk, m4.ports["multiplier_0_gate_E"], m5.ports["multiplier_0_gate_E"])
    latch << c_route(pdk, m6.ports["multiplier_0_drain_E"], m8.ports["multiplier_0_gate_E"])
    latch << c_route(pdk, m8.ports["multiplier_0_drain_E"], m6.ports["multiplier_0_gate_E"])
    latch << straight_route(pdk, m6.ports["multiplier_0_source_E"], m5.ports["multiplier_0_drain_E"])
    latch << straight_route(pdk, m8.ports["multiplier_0_source_E"], m5.ports["multiplier_0_drain_E"])

    # Ports for external connections
    latch.add_port("D", port=m2.ports["multiplier_0_source_E"])
    latch.add_port("Dp", port=m7.ports["multiplier_0_source_E"])
    latch.add_port("CLK", port=m2.ports["multiplier_0_gate_E"])
    latch.add_port("CLKN", port=m7.ports["multiplier_0_gate_E"])
    latch.add_port("Q", port=m6.ports["multiplier_0_drain_E"])
    latch.add_port("Qp", port=m8.ports["multiplier_0_drain_E"])
    latch.add_port("VDD", port=m3.ports["multiplier_0_drain_E"])
    latch.add_port("VSS", port=m5.ports["multiplier_0_source_E"])

    return latch
