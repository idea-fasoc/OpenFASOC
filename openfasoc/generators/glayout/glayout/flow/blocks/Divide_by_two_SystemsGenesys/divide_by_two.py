from gdsfactory import Component
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route
from latch_design import create_nmos_latch_layout

def create_divide_by_two_circuit(pdk):
    divider = Component("divide_by_two")

    # Create two latch instances
    latch1 = divider << create_nmos_latch_layout(pdk)
    latch2 = divider << create_nmos_latch_layout(pdk)

    # Position and connect the latches
    latch2.movey(-latch1.size[1] - pdk.util_max_metal_seperation())
    divider << straight_route(pdk, latch1.ports["Q"], latch2.ports["D"])
    divider << straight_route(pdk, latch1.ports["Qp"], latch2.ports["Dp"])
    divider << c_route(pdk, latch2.ports["Q"], latch1.ports["D"])
    divider << c_route(pdk, latch2.ports["Qp"], latch1.ports["Dp"])

    # Add external ports and connect power
    divider.add_port("CLK", port=latch1.ports["CLK"])
    divider.add_port("CLKN", port=latch1.ports["CLKN"])
    divider.add_port("OUT", port=latch2.ports["Q"])
    divider.add_port("OUT_B", port=latch2.ports["Qp"])
    divider.add_port("VDD", port=latch1.ports["VDD"])
    divider.add_port("VSS", port=latch1.ports["VSS"])
    divider << straight_route(pdk, latch1.ports["VDD"], latch2.ports["VDD"])
    divider << straight_route(pdk, latch1.ports["VSS"], latch2.ports["VSS"])

    return divider
