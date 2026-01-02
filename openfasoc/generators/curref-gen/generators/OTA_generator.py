from decimal import Decimal
from typing import Literal, Optional, Union

#from glayout.flow.primitives.fet import nmos, pmos, multiplier
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
#from glayout.flow.primitives.guardring import tapring
from glayout.flow.pdk.util.comp_utils import (
    add_ports_perimeter,
    align_comp_to_port,
    evaluate_bbox,
    prec_ref_center,
    to_decimal,
    to_float,
)
#from gdsfactory.functions import transformed
from glayout.flow.primitives.via_gen import via_stack
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.straight_route import straight_route
# Import custom functions
#from custom_functions import macro_two_transistor_placement_Onchip
from OTA_building_blocks import *


# To place a port
def place_port(pdk, layer, port_width, port_height, pos_x, pos_y, ref_port): 
  pass

 
 
def main(pdk: MappedPDK): 
  pdk.activate()
  OTA_Core = Component()

  # Creating diff pair 
  print("Placing differential pair...")
  diff_pair = create_differential_pair(pdk)  
  diff_pair_dimentions = evaluate_bbox(diff_pair)
  # Appending Diff Pair
  diff_pair_ref = OTA_Core << diff_pair 

  # Creating Tail transistor
  print("Placing tail transistor...")
  tail_transistor = create_tail_transistor(pdk) 
  tail_transistor_dimentions = evaluate_bbox(tail_transistor)
  # Appending Tail transistor
  tail_transistor_ref = OTA_Core << tail_transistor 
  tail_transistor_ref.movey(  -0.85*diff_pair_dimentions[1] )

  # Creating Output N-Load
  print("Placing cascode output N-Load...")
  n_Load = create_nLoad(pdk)
  n_Load_dimentions = evaluate_bbox(n_Load)
  # Appending Tail transistor
  n_Load_ref = OTA_Core << n_Load 
  n_Load_ref.movex( 0.5*tail_transistor_dimentions[0] + 0.5*n_Load_dimentions[0] + pdk.util_max_metal_seperation() ) 
  n_Load_ref.movey( -0.85*diff_pair_dimentions[1] ) 

  # Creating Output stage P-folded Cascode device
  print("Placing cascode output P-Cascode device...")
  lvtP_cascode = create_lvt_pcascode(pdk)
  lvtP_cascode_dimentions = evaluate_bbox(lvtP_cascode)
  # Appending Tail transistor
  lvtP_cascode_ref = OTA_Core << lvtP_cascode 
  lvtP_cascode_ref.movex( 0.5*diff_pair_dimentions[0] + 0.5*lvtP_cascode_dimentions[0] + pdk.util_max_metal_seperation() ) 
  #lvtP_cascode_ref.movey( 1 ) 

  print("Starting routing...")
  # Routing Tail sources with VSS
  OTA_Core << L_route(pdk, tail_transistor_ref.ports['Tail_route_sources_con_E'], n_Load_ref.ports['M9M10_SA_S'], hglayer="met2")
  # Routing Diff pair sources with tail drains
  OTA_Core << L_route(pdk, diff_pair_ref.ports['Diff_Pair_route_source_con_W'], tail_transistor_ref.ports['Tail_DA_N'], hglayer="met2")
  OTA_Core << L_route(pdk, diff_pair_ref.ports['Diff_Pair_route_source_con_E'], tail_transistor_ref.ports['Tail_DB_N'], hglayer="met2")
  # Routing to connect Diff pair and tail transistor bulks
  OTA_Core << c_route(pdk, diff_pair_ref.ports['Diff_Pair_VDD2_VSS2_W'], tail_transistor_ref.ports['Tail_VDD1_VSS1_W'], cglayer="met3")
  # Routing Diff pair drains with cascode devices.
  OTA_Core << c_route(pdk, diff_pair_ref.ports['Diff_Pair_DA_N'], lvtP_cascode_ref.ports['M7M8_DA_N'], cglayer="met2", extension=0.4*diff_pair_dimentions[1])
  OTA_Core << c_route(pdk, diff_pair_ref.ports['Diff_Pair_DB_N'], lvtP_cascode_ref.ports['M7M8_DB_N'], cglayer="met2", extension=0.4*diff_pair_dimentions[1] - 3*pdk.util_max_metal_seperation())

  
  # Show full layout
  OTA_Core.show() 



if __name__ == "__main__":
  main(sky130)