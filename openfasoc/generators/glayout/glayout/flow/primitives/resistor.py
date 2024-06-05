from glayout.flow.primitives.fet import pmos, nmos
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.smart_route import smart_route
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.primitives.guardring import tapring
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, add_ports_perimeter
from gdsfactory.component import Component
from gdsfactory.cell import cell 
from typing import Optional

@cell
def resistor(
    pdk: MappedPDK,
    width: float = 5,
    length: float = 1,
    num_series: int = 1,
    with_substrate_tap: bool = False,
    with_tie: bool = False,
    with_dnwell: bool = False,
    rmult: Optional[int] = None,
    multipliers: int = 1,
    substrate_tap_layers: tuple[str, str] = ("met2", "met1"),
    tie_layers: tuple[str, str] = ("met2", "met1"),
) -> Component:
    """This cell represents a diode connected pfet which acts as a programmable resistor. The small signal resistance is modelled by (1/gm)||r_0, where gm is the fet's transconductance and r0 is the small signal output impedance. The cell can be instantiated with any choice of width and length. The number of resistors connected in series can be controlled using numseries (**note: they will be placed in a single line, so area saving has to be manually handled). The number of resistors in parallel connnection can be controlled using multipliers. 
    Note that parallel and series resistors can be used simultaneously, but the parallel-ness will be applied to all resistors in series. The cell can be used and routed separately should a more complex combination of resistances be required

    Args:
        pdk (MappedPDK): the process design kit to be used
        width (float, optional): the width of each pfet. Defaults to 5.
        length (float, optional): the length of each pfet. Defaults to 1.
        num_series (int, optional): the number of pfets connected in series. Defaults to 1.
        with_substrate_tap (bool, optional): the presence of substrate tap. Defaults to False.
        with_tie (bool, optional): the presence of tie. Defaults to False.
        with_dnwell (bool, optional): the presence of dnwell. Defaults to False.
        rmult (Optional[int], optional): the routing multiplier (controls routing width). Defaults to None.
        multipliers (int, optional): the number of pfets connected in parallel. Defaults to 1.
        substrate_tap_layers (tuple[str, str], optional): the layers in the substrate tapring. Defaults to ("met2", "met1").
        tie_layers (tuple[str, str], optional): the layers in the tie layer tapring. Defaults to ("met2", "met1").

    Returns:
        Component: an instance of the resistor cell
    """
    toplvl = Component()
    max_sep = pdk.util_max_metal_seperation()
    if num_series == 1:
        pfet_reference = toplvl << pmos(pdk, width=width, length=length, with_substrate_tap=with_substrate_tap, with_tie=with_tie, dnwell=with_dnwell, rmult=rmult, multipliers=multipliers, substrate_tap_layers=substrate_tap_layers, tie_layers=tie_layers, with_dummy=False)
        toplvl.add_ports(pfet_reference.ports, prefix='pfet_')
        
        # short gate and drain 
        diode_connect = toplvl << c_route(pdk, pfet_reference.ports['multiplier_0_gate_W'], pfet_reference.ports['multiplier_0_drain_W'])
        
    else:
        pfet_references = []
        diode_connect_references = []
        pfet_reference_0 = toplvl << pmos(pdk, width=width, length=length, with_substrate_tap=False, with_tie=False, dnwell=False, rmult=rmult, multipliers=multipliers, substrate_tap_layers=substrate_tap_layers, tie_layers=tie_layers, with_dummy=False)
        diode_connect_0 = toplvl << c_route(pdk, pfet_reference_0.ports['multiplier_0_gate_W'], pfet_reference_0.ports['multiplier_0_drain_W'])
        diode_connect_references.append(diode_connect_0)
        
        toplvl.add_ports(pfet_reference_0.ports, prefix='pfet_0_')
        pfet_references.append(pfet_reference_0)
        for i in range(1, num_series):
            pfet_reference = (toplvl << pmos(pdk, width=width, length=length, with_substrate_tap=False, with_tie=False, dnwell=False, rmult=rmult,multipliers=multipliers, substrate_tap_layers=substrate_tap_layers, tie_layers=tie_layers, with_dummy=False)).movey(i * (evaluate_bbox(pfet_reference_0)[1] + max_sep))
            
            pfet_references.append(pfet_reference)
            if i < num_series - 1:
                toplvl.add_ports(pfet_reference.ports, prefix=f'pfet_{i}_')
            
            # short gate and drain 
            diode_connect = toplvl << c_route(pdk, pfet_reference.ports['multiplier_0_gate_W'], pfet_reference.ports['multiplier_0_drain_W'])
            diode_connect_references.append(diode_connect)
            # connect drain and source of previous and present pfet
            if multipliers > 1:
                extension = 1 * ((i % 2) + 1)
            else:
                extension = 0.5 * ((i % 2))
            toplvl << c_route(pdk, pfet_references[i-1].ports['multiplier_0_source_E'], pfet_reference.ports['multiplier_0_drain_E'], extension=extension)
        
        # add tie if tie
        if with_tie:
            tap_separation = max(
                pdk.get_grule("met2")["min_separation"],
                pdk.get_grule("met1")["min_separation"],
                pdk.get_grule("active_diff", "active_tap")["min_separation"],
            )
            tap_separation += pdk.get_grule("n+s/d", "active_tap")["min_enclosure"]
            tap_encloses = (
                (evaluate_bbox(toplvl)[0] + max_sep),
                (evaluate_bbox(toplvl)[1] + max_sep),
            )
            ringtoadd = tapring(
                pdk,
                enclosed_rectangle=tap_encloses,
                sdlayer="n+s/d",
                horizontal_glayer=tie_layers[0],
                vertical_glayer=tie_layers[1],
            )
            tapring_ref = (toplvl << ringtoadd).movey(((evaluate_bbox(pfet_reference_0)[1] + max_sep) * ((num_series - 1)/2) ))
            toplvl.add_ports(tapring_ref.get_ports_list(),prefix="tie_")
            for row in range(multipliers):
                for dummyside, tieside in [("L","W"),("R","E")]:
                    try:
                        toplvl << straight_route(pdk, toplvl.ports[f"multiplier_{row}_dummy_{dummyside}_gsdcon_top_met_W"], toplvl.ports[f"tie_{tieside}_top_met_{tieside}"],glayer2="met1")
                    except KeyError:
                        pass
        
        # add nwell
        nwell_glayer = "dnwell" if with_dnwell else "nwell"
        toplvl.add_padding(
            layers=(pdk.get_glayer(nwell_glayer),),
            default=pdk.get_grule("active_tap", nwell_glayer)["min_enclosure"],
        )
        toplvl = add_ports_perimeter(toplvl, layer=pdk.get_glayer(nwell_glayer),prefix="well_")
        
        # add substrate tap if needed
        if with_substrate_tap:
            substrate_tap_separation = pdk.get_grule("dnwell", "active_tap")[
                "min_separation"
            ]
            substrate_tap_encloses = (
                (evaluate_bbox(toplvl)[0] + max_sep),
                (evaluate_bbox(toplvl)[1] + max_sep),
            )
            ringtoadd = tapring(
                pdk,
                enclosed_rectangle=substrate_tap_encloses,
                sdlayer="p+s/d",
                horizontal_glayer=substrate_tap_layers[0],
                vertical_glayer=substrate_tap_layers[1],
            )
            tapring_ref = (toplvl << ringtoadd).movey(((evaluate_bbox(pfet_reference_0)[1] + max_sep) * ((num_series - 1)/2) ))
            toplvl.add_ports(tapring_ref.get_ports_list(),prefix="guardring_")
            
        toplvl.add_ports(pfet_references[0].get_ports_list(), prefix='port1_')
        toplvl.add_ports(pfet_references[-1].get_ports_list(), prefix='port2_')
        
    return toplvl