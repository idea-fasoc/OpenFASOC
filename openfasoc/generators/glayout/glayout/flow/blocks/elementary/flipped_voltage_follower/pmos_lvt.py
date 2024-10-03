from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components import rectangle
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.primitives.fet import pmos
from glayout.flow.pdk.util.comp_utils import evaluate_bbox
from glayout.flow.pdk.util.port_utils import rename_ports_by_orientation
from glayout.flow.spice.netlist import Netlist
from gdsfactory import Component
from typing import Optional, Union

def pfet_lvt_netlist(
	pdk: MappedPDK,
	circuit_name: str,
	model: str,
	width: float,
	length: float,
	fingers: int,
	multipliers: int,
	with_dummy: Union[bool, tuple[bool, bool]]
	) -> Netlist:
	
	     # add spice netlist
	    num_dummies = 0
	    if with_dummy == False or with_dummy == (False, False):
	        num_dummies = 0
	    elif with_dummy == (True, False) or with_dummy == (False, True):
	        num_dummies = 1
	    elif with_dummy == True or with_dummy == (True, True):
	        num_dummies = 2

	    if length is None:
	        length = pdk.get_grule('poly')['min_width']
        
	    ltop = length
	    wtop = width
	    mtop = multipliers * fingers
    
	    source_netlist=""".subckt {circuit_name} {nodes} """+f'l={ltop} w={wtop} m={mtop} '+"""\nXMAIN   D G S B {model} l={{l}} w={{w}} m={{m}}"""

	    for i in range(num_dummies):
	        source_netlist += "\nXDUMMY" + str(i+1) + " B B B B {model} l={{l}} w={{w}} m={{1}}"

	    source_netlist += "\n.ends {circuit_name}"

	    return Netlist(
	        circuit_name=circuit_name,
	        nodes=['D', 'G', 'S', 'B'],
	        source_netlist=source_netlist,
	        instance_format="X{name} {nodes} {circuit_name} l={length} w={width} m={mult} dm={dummy_mult}",
	        parameters={
	            'model': model,
	            'length': ltop,
	            'width': wtop,
	            'mult': mtop ,
	            'dummy_mult': 1
	        }
 	   )

@cell
def pmos_lvt(
        pdk: MappedPDK,
        width: float = 3,
        length: float = None,
        fingers: int = 1,
        multipliers: int = 1,
        dummy: tuple[bool,bool] = (False,False),
        substrate_tap: bool = False,
        with_tie: bool = False,
        tie_layers: tuple[str,str] = ("met2","met1"),
             ) -> Component:

     top_level = Component("pmos_lvt")
     
     pfet = pmos(pdk, width=width, fingers=fingers, multipliers=multipliers, with_dummy=(dummy[0],dummy[1]), with_tie=with_tie, with_substrate_tap=substrate_tap, length=length)
     pfet_ref = top_level << pfet

     lvt_layer = (125,44)
     
     E_edge_center = pfet_ref.ports["multiplier_0_drain_E"].center
     W_edge_center = pfet_ref.ports["multiplier_0_source_W"].center
     S_edge_center = pfet_ref.ports["multiplier_0_gate_S"].center
     x_length = E_edge_center[0] - W_edge_center[0]
     y_length = E_edge_center[1] - S_edge_center[1]
     
     lvt_rectangle = rectangle(layer=lvt_layer, size=(x_length+0.1, y_length-0.8))
     lvt_rectangle_ref = top_level << lvt_rectangle
     lvt_rectangle_ref.movex(destination=W_edge_center[0]-0.05)
     lvt_rectangle_ref.movey(destination= S_edge_center[1] +0.4)
     top_level.add_ports(pfet_ref.get_ports_list())
     component = rename_ports_by_orientation(top_level).flatten()

     component.info['netlist'] = pfet_lvt_netlist(
				         pdk,
				         circuit_name="PMOS_LVT",
				         model="sky130_fd_pr__pfet_01v8_lvt",
				         width=width,
				         length=length,
				         fingers=fingers,
				         multipliers=multipliers,
				         with_dummy=dummy
				         )

     return component
