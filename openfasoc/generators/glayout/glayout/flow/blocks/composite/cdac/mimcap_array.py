from typing import List

# Primitives
from glayout.flow.primitives.mimcap import mimcap
from glayout.flow.primitives.mimcap import mimcap_array
from glayout.flow.primitives.via_gen import via_stack, via_array

# Standard
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130

# gdsfactory
from gdsfactory import Component
from gdsfactory.cell import cell
from gdsfactory.components.rectangle import rectangle

# Utility
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, prec_center, prec_array, align_comp_to_port

# Routing
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route

'''
def dac_mimcap_array_netlist(pdk: MappedPDK) -> Netlist:
    return Netlist(
        circuit_name = "DAC_MIMCAP_ARR",

        nodes = ['V1','V2','V3',],
        source_netlist=,
        instance_format=,
        parameters={
            'model': pdk.models['mimcap'],
            'length': size[0]
            'width': size[1]
        }    
    )
'''

def create_6bit_dac_mimcap_array(pdk: MappedPDK):
    """
    Creates a 6-bit DAC using an 8x8 MIM capacitor array with binary weighting.
    """

    # Crate the top-level component
    dac_mim_cap = Component("6bit_DAC_MIMCAP_Array")

    # metal and via layers
    met2 = pdk.get_glayer('met3')
    #print("met2:",met2)
    met3_capmetbottom = pdk.get_glayer('met4')
    #print("met3_capmetbottom:",met3_capmetbottom)
    met4_capmettop = pdk.get_glayer('met5')
    #print("met4_capmettop:",met4_capmettop)
    via3 = pdk.get_glayer('via4')
    mimcap_arr = Component("mimcap_arr")
    mimcap_single_size = 6
    mimcap_single = mimcap(pdk, size=(mimcap_single_size,mimcap_single_size))
    rows_num = 8 
    columns_num = 8
    mimcap_space = 12*pdk.get_grule("capmet")["min_separation"]
    met4_width = pdk.get_grule("met5")["min_width"]
    array_ref = mimcap_arr << prec_array(mimcap_single, rows=rows_num, columns=columns_num, spacing=2*[mimcap_space])
    mimcap_arr.add_ports(array_ref.get_ports_list())
    mim_metal_space = mimcap_space/9
    ################################################
    port_pairs = list()
    port_sides_pairs = list()
    via_refs = list()
    global top_c5_left
    global top_c5_right
    global top_c5_center
    global top_c4_left
    global top_c4_right
    global top_c4_center
    global top_c3_left
    global top_c3_right
    global top_c3_center
    global top_c2_left
    global top_c2_right
    global top_c2_center
    global vertical_sticks
    vertical_sticks = list()
    for rownum in  range(rows_num):
        for colnum in range(columns_num):
            base_mimcap = f"row{rownum}_col{colnum}_"
            right_mimcap = f"row{rownum}_col{colnum+1}_"
            up_mimcap = f"row{rownum+1}_col{colnum}_"
            capmetbottom = "met4"
            capmettop = "met5"
            
            # Bottom Metal
            level = "bottom_met_"
            layer = capmetbottom
            base_east_port = mimcap_arr.ports.get(base_mimcap+level+"E")
            right_west_port = mimcap_arr.ports.get(right_mimcap+level+"W")
            base_north_port = mimcap_arr.ports.get(base_mimcap+level+"N")
            up_south_port = mimcap_arr.ports.get(up_mimcap+level+"S")
            if rownum == rows_num-1 and colnum == columns_num-1:
                pass #continue
            elif rownum == rows_num-1:            
                port_pairs.append((base_east_port,right_west_port,layer))
            elif colnum == columns_num-1:
                port_pairs.append((base_north_port,up_south_port,layer))
            else:
                port_pairs.append((base_east_port,right_west_port,layer))
                port_pairs.append((base_north_port,up_south_port,layer))
            if rownum == 0 and colnum == 7:
                base_south_port = mimcap_arr.ports.get(base_mimcap+level+"S")
                base_south_port_down = base_south_port.copy()
                base_south_port_down.center[1] -= mimcap_single_size
                via_ref = mimcap_arr << straight_route(pdk, base_south_port, base_south_port_down, width=met4_width, glayer1="met4", glayer2="met3", via2_alignment=("c","c"))
                mimcap_arr.add_ports(via_ref.get_ports_list(), prefix="via_commonbottom_") # via_commonbottom_route_X
                via_south_port = mimcap_arr.ports.get("via_commonbottom_route_S")
                via_south_port_down = via_south_port.copy()
                via_south_port_down.layer = met2
                via_south_port_down.center[1] -= mimcap_single_size*2
                mimcap_arr << straight_route(pdk, via_south_port, via_south_port_down, width=met4_width, glayer1="met3", glayer2="met3", via1_alignment=("c","c"))

            # Top metal
            level = "top_met_"
            position_up = "up_"
            position_down = "down_"
            position_right = "right_"
            position_left = "left_"
            layer = capmettop

            base_east_port = mimcap_arr.ports.get(base_mimcap+level+"E")
            base_west_port = mimcap_arr.ports.get(base_mimcap+level+"W")
            met4_distance_from_center = base_east_port.width/2 - 3*pdk.get_grule(layer)["min_width"]
            if base_east_port is not None:
                base_west_port_up = base_west_port.copy()
                base_west_port_up.name = base_mimcap+position_up+level+"W"
                base_west_port_up.center[1] += met4_distance_from_center
                base_west_port_up_space3 = base_west_port_up.copy()
                base_west_port_up_space3.center[0] -= mim_metal_space*3
                base_west_port_down = base_west_port.copy()
                base_west_port_down.name = base_mimcap+position_down+level+"W"
                base_west_port_down.center[1] -= met4_distance_from_center
                base_west_port_down_space3 = base_west_port_down.copy()
                base_west_port_down_space3.center[0] -= mim_metal_space*3
                base_east_port_up = base_east_port.copy()
                base_east_port_up.name = base_mimcap+position_up+level+"E"
                base_east_port_up.center[1] += met4_distance_from_center #(base_east_port_up.width/2 - pdk.get_grule(layer)["min_width"])
                base_east_port_up_space1 = base_east_port_up.copy()
                base_east_port_up_space1.name = base_mimcap+position_up+level+"W"
                base_east_port_up_space1.center[0] += mim_metal_space*1 
                base_east_port_up_space2 = base_east_port_up.copy()
                base_east_port_up_space2.name = base_mimcap+position_up+level+"W"
                base_east_port_up_space2.center[0] += mim_metal_space*2
                base_east_port_up_space3 = base_east_port_up.copy()
                base_east_port_up_space3.name = base_mimcap+position_up+level+"W"
                base_east_port_up_space3.center[0] += mim_metal_space*3
                base_east_port_up_space4 = base_east_port_up.copy()
                base_east_port_up_space4.name = base_mimcap+position_up+level+"W"
                base_east_port_up_space4.center[0] += mim_metal_space*4 
                base_east_port_down = base_east_port.copy()
                base_east_port_down.name = base_mimcap+position_down+level+"E"
                base_east_port_down.center[1] -= met4_distance_from_center #(base_north_port.width/2 - pdk.get_grule(layer)["min_width"])
                base_east_port_down_space1 = base_east_port_down.copy()
                base_east_port_down_space1.name = base_mimcap+position_down+level+"W"
                base_east_port_down_space1.center[0] += mim_metal_space*1 
                base_east_port_down_space2 = base_east_port_down.copy()
                base_east_port_down_space2.name = base_mimcap+position_down+level+"W"
                base_east_port_down_space2.center[0] += mim_metal_space*2
                base_east_port_down_space3 = base_east_port_down.copy()
                base_east_port_down_space3.name = base_mimcap+position_down+level+"W"
                base_east_port_down_space3.center[0] += mim_metal_space*3 
                base_east_port_down_space4 = base_east_port_down.copy()
                base_east_port_down_space4.name = base_mimcap+position_down+level+"W"
                base_east_port_down_space4.center[0] += mim_metal_space*4

            right_west_port = mimcap_arr.ports.get(right_mimcap+level+"W")
            if right_west_port is not None:
                right_west_port_up = right_west_port.copy() 
                right_west_port_up.name = right_mimcap+position_up+level+"W"
                right_west_port_up.center[1] += met4_distance_from_center #(right_west_port_up.width/2 - pdk.get_grule(layer)["min_width"])
                right_west_port_up_space3 = right_west_port_up.copy()
                right_west_port_up_space3.name = right_mimcap+position_up+level+"E"
                right_west_port_up_space3.center[0] -= mim_metal_space*3
                right_west_port_up_space4 = right_west_port_up.copy()
                right_west_port_up_space4.name = right_mimcap+position_up+level+"E"
                right_west_port_up_space4.center[0] -= mim_metal_space*4
                right_west_port_up_space6 = right_west_port_up.copy()
                right_west_port_up_space6.name = right_mimcap+position_up+level+"E"
                right_west_port_up_space6.center[0] -= mim_metal_space*6
                right_west_port_up_space7 = right_west_port_up.copy()
                right_west_port_up_space7.name = right_mimcap+position_up+level+"E"
                right_west_port_up_space7.center[0] -= mim_metal_space*7
                right_west_port_down = right_west_port.copy()
                right_west_port_down.name = right_mimcap+position_down+level+"W"
                right_west_port_down.center[1] -= met4_distance_from_center #(right_west_port_down.width/2 - pdk.get_grule(layer)["min_width"])    
                right_west_port_down_space3 = right_west_port_down.copy()
                right_west_port_down_space3.name = right_mimcap+position_down+level+"E"
                right_west_port_down_space3.center[0] -= mim_metal_space*3
                right_west_port_down_space4 = right_west_port_down.copy()
                right_west_port_down_space4.name = right_mimcap+position_down+level+"E"
                right_west_port_down_space4.center[0] -= mim_metal_space*4
                right_west_port_down_space6 = right_west_port_down.copy()
                right_west_port_down_space6.name = right_mimcap+position_down+level+"E"
                right_west_port_down_space6.center[0] -= mim_metal_space*6
                right_west_port_down_space7 = right_west_port_down.copy()
                right_west_port_down_space7.name = right_mimcap+position_down+level+"E"
                right_west_port_down_space7.center[0] -= mim_metal_space*7

            base_north_port = mimcap_arr.ports.get(base_mimcap+level+"N")
            if base_north_port is not None:
                base_north_port_right = base_north_port.copy()
                base_north_port_right.name = base_mimcap+position_right+level+"N"
                base_north_port_right.center[0] += met4_distance_from_center #(base_north_port_right.width/2 - pdk.get_grule(layer)["min_width"])
                base_north_port_right_space = base_north_port_right.copy()
                base_north_port_right_space.name = base_mimcap+position_right+level+"S"
                base_north_port_right_space.center[1] += mim_metal_space*4
                base_north_port_left = base_north_port.copy()
                base_north_port_left.name = base_mimcap+position_left+level+"N"
                base_north_port_left.center[0] -= met4_distance_from_center #(base_north_port_left.width/2 - pdk.get_grule(layer)["min_width"])
                base_north_port_left_space = base_north_port_left.copy()
                base_north_port_left_space.name = base_mimcap+position_left+level+"S"
                base_north_port_left_space.center[1] += mim_metal_space*4
            
            up_south_port = mimcap_arr.ports.get(up_mimcap+level+"S")
            if up_south_port is not None:
                up_south_port_right = up_south_port.copy()
                up_south_port_right.name = base_mimcap+position_right+level+"S"
                up_south_port_right.center[0] += met4_distance_from_center #(up_south_port_right.width/2 - pdk.get_grule(layer)["min_width"])
                up_south_port_right_space = up_south_port_right.copy()
                up_south_port_right_space.name = base_mimcap+position_right+level+"N"
                up_south_port_right_space.center[1] -= mim_metal_space*4
                up_south_port_left = up_south_port.copy()
                up_south_port_left.name = base_mimcap+position_left+level+"S"
                up_south_port_left.center[0] -= met4_distance_from_center #(up_south_port_left.width/2 - pdk.get_grule(layer)["min_width"])
                up_south_port_left_space = up_south_port_left.copy()
                up_south_port_left_space.name = base_mimcap+position_left+level+"N"
                up_south_port_left_space.center[1] -= mim_metal_space*4

            if rownum == 0:
                # North and South
                if colnum in (2,3,5,6):
                    port_pairs.append((base_north_port_right,base_north_port_right_space,layer))
                    port_pairs.append((base_north_port_left,base_north_port_left_space,layer))
                    port_pairs.append((up_south_port_right,up_south_port_right_space,layer))
                    port_pairs.append((up_south_port_left,up_south_port_left_space,layer))
                else:
                    port_pairs.append((base_north_port_left,up_south_port_left,layer))
                    port_pairs.append((base_north_port_right,up_south_port_right,layer))
                # West and East
                if colnum in (5,6): #(2,6)
                    port_pairs.append((base_east_port_up,base_east_port_up_space2,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space2,layer))
                    mimcap_arr << straight_route(pdk, right_west_port_up, right_west_port_up_space6, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, right_west_port_down, right_west_port_down_space6, width=met4_width, glayer1="met5", glayer2="met3")
                elif colnum == columns_num-1:
                    pass #continue
                else:
                    port_pairs.append((base_east_port_up,right_west_port_up,layer))
                    port_pairs.append((base_east_port_down,right_west_port_down,layer))
                if colnum == 0:
                    mimcap_arr << straight_route(pdk, base_west_port_up, base_west_port_up_space3, width=met4_width*3, glayer1="met5", glayer2="met3", via2_alignment=("c","c"))
                    mimcap_arr << straight_route(pdk, base_west_port_down, base_west_port_down_space3, width=met4_width*3, glayer1="met5", glayer2="met3", via2_alignment=("c","c"))
            elif rownum == 1:                    
                # North and South
                if colnum in (1,2,4,5):
                    port_pairs.append((base_north_port_right,base_north_port_right_space,layer))
                    port_pairs.append((base_north_port_left,base_north_port_left_space,layer))
                    port_pairs.append((up_south_port_right,up_south_port_right_space,layer))
                    port_pairs.append((up_south_port_left,up_south_port_left_space,layer))
                else:
                    port_pairs.append((base_north_port_left,up_south_port_left,layer))
                    port_pairs.append((base_north_port_right,up_south_port_right,layer))
                # West and East
                if colnum in (0,2,3,5): #(4,4)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum in (1,6): #(2,6)
                    port_pairs.append((base_east_port_up,base_east_port_up_space2,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space2,layer))
                    mimcap_arr << straight_route(pdk, right_west_port_up, right_west_port_up_space6, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, right_west_port_down, right_west_port_down_space6, width=met4_width, glayer1="met5", glayer2="met3")
                elif colnum == 4: #(4,3)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    mimcap_arr << straight_route(pdk, right_west_port_up, right_west_port_up_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, right_west_port_down, right_west_port_down_space3, width=met4_width, glayer1="met5", glayer2="met3")
                elif colnum == columns_num-1:
                    pass #continue
                else:
                    port_pairs.append((base_east_port_up,right_west_port_up,layer))
                    port_pairs.append((base_east_port_down,right_west_port_down,layer))
                if colnum == 0:
                    mimcap_arr << straight_route(pdk, base_west_port_up, base_west_port_up_space3, width=met4_width*3, glayer1="met5", glayer2="met3", via2_alignment=("c","c"))
                    mimcap_arr << straight_route(pdk, base_west_port_down, base_west_port_down_space3, width=met4_width*3, glayer1="met5", glayer2="met3", via2_alignment=("c","c"))
            elif rownum == 2:                    
                # North and South
                if colnum in (0,1,2,3,4,5,7):
                    port_pairs.append((base_north_port_right,base_north_port_right_space,layer))
                    port_pairs.append((base_north_port_left,base_north_port_left_space,layer))
                    port_pairs.append((up_south_port_right,up_south_port_right_space,layer))
                    port_pairs.append((up_south_port_left,up_south_port_left_space,layer))
                else:
                    port_pairs.append((base_north_port_left,up_south_port_left,layer))
                    port_pairs.append((base_north_port_right,up_south_port_right,layer))
                # West and East
                if colnum == 4: #(4,4)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum == 5: #(3,4)
                    mimcap_arr << straight_route(pdk, base_east_port_up, base_east_port_up_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, base_east_port_down, base_east_port_down_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum in (0,6): #(2,6)
                    port_pairs.append((base_east_port_up,base_east_port_up_space2,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space2,layer))
                    mimcap_arr << straight_route(pdk, right_west_port_up, right_west_port_up_space6, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, right_west_port_down, right_west_port_down_space6, width=met4_width, glayer1="met5", glayer2="met3")
                elif colnum == 3: #(4,3)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    mimcap_arr << straight_route(pdk, right_west_port_up, right_west_port_up_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, right_west_port_down, right_west_port_down_space3, width=met4_width, glayer1="met5", glayer2="met3")
                elif colnum == columns_num-1:
                    pass #continue
                else:
                    port_pairs.append((base_east_port_up,right_west_port_up,layer))
                    port_pairs.append((base_east_port_down,right_west_port_down,layer))
                if colnum == 0:
                    mimcap_arr << straight_route(pdk, base_west_port_up, base_west_port_up_space3, width=met4_width*3, glayer1="met5", glayer2="met3", via2_alignment=("c","c"))
                    mimcap_arr << straight_route(pdk, base_west_port_down, base_west_port_down_space3, width=met4_width*3, glayer1="met5", glayer2="met3", via2_alignment=("c","c"))
            elif rownum == 3:                    
                # North and South
                if colnum in (0,1,2,3,5,6,7):
                    port_pairs.append((base_north_port_right,base_north_port_right_space,layer))
                    port_pairs.append((base_north_port_left,base_north_port_left_space,layer))
                    port_pairs.append((up_south_port_right,up_south_port_right_space,layer))
                    port_pairs.append((up_south_port_left,up_south_port_left_space,layer))
                else:
                    port_pairs.append((base_north_port_left,up_south_port_left,layer))
                    port_pairs.append((base_north_port_right,up_south_port_right,layer))
                # West and East
                if colnum in (0,1): #(3,4)
                    mimcap_arr << straight_route(pdk, base_east_port_up, base_east_port_up_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, base_east_port_down, base_east_port_down_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum == 2: #(3,3)
                    mimcap_arr << straight_route(pdk, base_east_port_up, base_east_port_up_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, base_east_port_down, base_east_port_down_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, right_west_port_up, right_west_port_up_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, right_west_port_down, right_west_port_down_space3, width=met4_width, glayer1="met5", glayer2="met3")
                elif colnum == 3: #(4,4)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum == columns_num-1:
                    pass #continue
                else:
                    port_pairs.append((base_east_port_up,right_west_port_up,layer))
                    port_pairs.append((base_east_port_down,right_west_port_down,layer))
                if colnum == 7:
                    mimcap_arr << straight_route(pdk, base_east_port_up, base_east_port_up_space3, width=met4_width*3, glayer1="met5", glayer2="met3", via2_alignment=("c","c"))
                    mimcap_arr << straight_route(pdk, base_east_port_down, base_east_port_down_space3, width=met4_width*3, glayer1="met5", glayer2="met3", via2_alignment=("c","c"))
            elif rownum == 4:                    
                # North and South
                if colnum in (0,2,3,4,5,6,7):
                    port_pairs.append((base_north_port_right,base_north_port_right_space,layer))
                    port_pairs.append((base_north_port_left,base_north_port_left_space,layer))
                    port_pairs.append((up_south_port_right,up_south_port_right_space,layer))
                    port_pairs.append((up_south_port_left,up_south_port_left_space,layer))
                else:
                    port_pairs.append((base_north_port_left,up_south_port_left,layer))
                    port_pairs.append((base_north_port_right,up_south_port_right,layer))
                # West and East
                if colnum == 2: #(4,4)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum == 3: #(3,4)
                    mimcap_arr << straight_route(pdk, base_east_port_up, base_east_port_up_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, base_east_port_down, base_east_port_down_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum in (5,6): #(2,6)
                    port_pairs.append((base_east_port_up,base_east_port_up_space2,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space2,layer))
                    mimcap_arr << straight_route(pdk, right_west_port_up, right_west_port_up_space6, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, right_west_port_down, right_west_port_down_space6, width=met4_width, glayer1="met5", glayer2="met3")
                elif colnum == 4: #(4,3)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    mimcap_arr << straight_route(pdk, right_west_port_up, right_west_port_up_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, right_west_port_down, right_west_port_down_space3, width=met4_width, glayer1="met5", glayer2="met3")
                elif colnum == columns_num-1:
                    pass #continue
                else:
                    port_pairs.append((base_east_port_up,right_west_port_up,layer))
                    port_pairs.append((base_east_port_down,right_west_port_down,layer))
                if colnum == 0:
                    mimcap_arr << straight_route(pdk, base_west_port_up, base_west_port_up_space3, width=met4_width*3, glayer1="met5", glayer2="met3", via2_alignment=("c","c"))
                    mimcap_arr << straight_route(pdk, base_west_port_down, base_west_port_down_space3, width=met4_width*3, glayer1="met5", glayer2="met3", via2_alignment=("c","c"))
            elif rownum == 5:                    
                # North and South
                if colnum in (2,3,5,6):
                    port_pairs.append((base_north_port_right,base_north_port_right_space,layer))
                    port_pairs.append((base_north_port_left,base_north_port_left_space,layer))
                    port_pairs.append((up_south_port_right,up_south_port_right_space,layer))
                    port_pairs.append((up_south_port_left,up_south_port_left_space,layer))
                else:
                    port_pairs.append((base_north_port_left,up_south_port_left,layer))
                    port_pairs.append((base_north_port_right,up_south_port_right,layer))
                # West and East
                if colnum == 2: #(4,4)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))

                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum in (3,6): #(3,4)
                    mimcap_arr << straight_route(pdk, base_east_port_up, base_east_port_up_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, base_east_port_down, base_east_port_down_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum == 1: #(2,6)
                    port_pairs.append((base_east_port_up,base_east_port_up_space2,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space2,layer))
                    mimcap_arr << straight_route(pdk, right_west_port_up, right_west_port_up_space6, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, right_west_port_down, right_west_port_down_space6, width=met4_width, glayer1="met5", glayer2="met3")
                elif colnum == 0: #(3,3)
                    mimcap_arr << straight_route(pdk, base_east_port_up, base_east_port_up_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, base_east_port_down, base_east_port_down_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    port_pairs.append((right_west_port_up,right_west_port_up_space3,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space3,layer))
                elif colnum == columns_num-1:
                    pass #continue
                else:
                    port_pairs.append((base_east_port_up,right_west_port_up,layer))
                    port_pairs.append((base_east_port_down,right_west_port_down,layer))
                if colnum == 7:
                    mimcap_arr << straight_route(pdk, base_east_port_up, base_east_port_up_space3, width=met4_width*3, glayer1="met5", glayer2="met3", via2_alignment=("c","c"))
                    mimcap_arr << straight_route(pdk, base_east_port_down, base_east_port_down_space3, width=met4_width*3, glayer1="met5", glayer2="met3", via2_alignment=("c","c"))
            elif rownum == 6:                    
                # North and South
                if colnum in (1,2,4,5):
                    port_pairs.append((base_north_port_right,base_north_port_right_space,layer))
                    port_pairs.append((base_north_port_left,base_north_port_left_space,layer))
                    port_pairs.append((up_south_port_right,up_south_port_right_space,layer))
                    port_pairs.append((up_south_port_left,up_south_port_left_space,layer))
                else:
                    port_pairs.append((base_north_port_left,up_south_port_left,layer))
                    port_pairs.append((base_north_port_right,up_south_port_right,layer))
                # West and East
                if colnum in (2,5): #(3,4)
                    mimcap_arr << straight_route(pdk, base_east_port_up, base_east_port_up_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, base_east_port_down, base_east_port_down_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum in (1,3,4,6): #(4,4)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum == 0: #(3,3)
                    mimcap_arr << straight_route(pdk, base_east_port_up, base_east_port_up_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, base_east_port_down, base_east_port_down_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    port_pairs.append((right_west_port_up,right_west_port_up_space3,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space3,layer))
                elif colnum == columns_num-1:
                    pass #continue
                else:
                    port_pairs.append((base_east_port_up,right_west_port_up,layer))
                    port_pairs.append((base_east_port_down,right_west_port_down,layer))
                if colnum == 7:
                    mimcap_arr << straight_route(pdk, base_east_port_up, base_east_port_up_space3, width=met4_width*3, glayer1="met5", glayer2="met3", via2_alignment=("c","c"))
                    mimcap_arr << straight_route(pdk, base_east_port_down, base_east_port_down_space3, width=met4_width*3, glayer1="met5", glayer2="met3", via2_alignment=("c","c"))
            elif rownum == 7:
                # West and East
                if colnum == 1: #(3,4)
                    mimcap_arr << straight_route(pdk, base_east_port_up, base_east_port_up_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, base_east_port_down, base_east_port_down_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum == 0: #(3,3)
                    mimcap_arr << straight_route(pdk, base_east_port_up, base_east_port_up_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    mimcap_arr << straight_route(pdk, base_east_port_down, base_east_port_down_space3, width=met4_width, glayer1="met5", glayer2="met3")
                    port_pairs.append((right_west_port_up,right_west_port_up_space3,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space3,layer))
                elif colnum == columns_num-1:
                    pass #continue
                else:
                    port_pairs.append((base_east_port_up,right_west_port_up,layer))
                    port_pairs.append((base_east_port_down,right_west_port_down,layer))
                if colnum == 7:
                    mimcap_arr << straight_route(pdk, base_east_port_up, base_east_port_up_space3, width=met4_width*3, glayer1="met5", glayer2="met3", via2_alignment=("c","c"))
                    mimcap_arr << straight_route(pdk, base_east_port_down, base_east_port_down_space3, width=met4_width*3, glayer1="met5", glayer2="met3", via2_alignment=("c","c"))
 
                # metal2
                layer = "met3"
                base_east_port_metal2_up = mimcap_arr.ports.get(base_mimcap+level+"E")
                base_east_port_metal2_up.name = base_mimcap+"east_metal2_up"
                base_east_port_metal2_up.center[0] += mim_metal_space*3
                base_east_port_metal2_up.center[1] += (met4_distance_from_center + met4_width/2)
                base_east_port_metal2_up.orientation = 270
                base_east_port_metal2_up.layer = met2
                base_east_port_metal2_down = base_east_port_metal2_up.copy()
                base_east_port_metal2_down.name = base_mimcap+"east_metal2_down"
                if colnum == 4:
                    base_east_port_metal2_down.center[1] -= (mimcap_single_size*13/2+ mimcap_space*8)
                else:    
                    base_east_port_metal2_down.center[1] -= (mimcap_single_size*17/2 + mimcap_space*8)
                port_pairs.append((base_east_port_metal2_up,base_east_port_metal2_down,layer))
                base_west_port_metal2_up = mimcap_arr.ports.get(base_mimcap+level+"W")
                base_west_port_metal2_up.name = base_mimcap+"west_metal2_up"
                base_west_port_metal2_up.center[0] -= mim_metal_space*3
                base_west_port_metal2_up.center[1] += (met4_distance_from_center + met4_width/2)
                base_west_port_metal2_up.orientation = 270
                base_west_port_metal2_up.layer = met2
                base_west_port_metal2_down = base_west_port_metal2_up.copy()
                base_west_port_metal2_down.name = base_mimcap+"west_metal2_down"
                if colnum in (1,2,6,7):
                    base_west_port_metal2_down.center[1] -= (mimcap_single_size*13/2 + mimcap_space*8)
                else: 
                    base_west_port_metal2_down.center[1] -= (mimcap_single_size*17/2 + mimcap_space*8)
                port_pairs.append((base_west_port_metal2_up,base_west_port_metal2_down,layer))

                vertical_sticks.append({'up': base_west_port_metal2_up.center, 'down': base_west_port_metal2_down.center, 'width': base_west_port_metal2_down.width, 'orientation': base_west_port_metal2_down.orientation, 'layer': base_west_port_metal2_down.layer})
                vertical_sticks.append({'up': base_east_port_metal2_up.center, 'down': base_east_port_metal2_down.center, 'width': base_east_port_metal2_down.width, 'orientation': base_east_port_metal2_down.orientation, 'layer': base_east_port_metal2_down.layer})
                print(f"Up: {base_west_port_metal2_up.center}, Down: {base_west_port_metal2_down.center}")
                print(f"Up: {base_east_port_metal2_up.center}, Down: {base_east_port_metal2_down.center}")

                if colnum == 0: 
                    top_c5_left = base_west_port_metal2_down.copy()
                    top_c5_left.name = "top_c5_left"
                    top_c5_left.orientation = 0
                    top_c5_left.layer = met3_capmetbottom
                    top_c5_left.center[1] += mimcap_single_size*2*(1/6)
                    top_c4_left = base_east_port_metal2_down.copy()
                    top_c4_left.name = "top_c4_left"
                    top_c4_left.orientation = 0
                    top_c4_left.layer = met3_capmetbottom
                    top_c4_left.center[1] += mimcap_single_size*2*(2/6)
                elif colnum == 1:
                    top_c3_left = base_east_port_metal2_down.copy()
                    top_c3_left.name = "top_c3_left"
                    top_c3_left.orientation = 0
                    top_c3_left.layer = met3_capmetbottom
                    top_c3_left.center[1] += mimcap_single_size*2*(3/6)
                elif colnum == 2:
                    top_c2_left = base_east_port_metal2_down.copy()
                    top_c2_left.name = "top_c2_left"
                    top_c2_left.orientation = 0
                    top_c2_left.layer = met3_capmetbottom
                    top_c2_left.center[1] += mimcap_single_size*2*(4/6)
                elif colnum == 5:
                    top_c2_right = base_west_port_metal2_down.copy()
                    top_c2_right.name = "top_c2_right"
                    top_c2_right.orientation = 0
                    top_c2_right.layer = met3_capmetbottom                   
                    top_c2_right.center[1] += mimcap_single_size*2*(4/6)
                    top_c3_right = base_east_port_metal2_down.copy()
                    top_c3_right.name = "top_c3_right"
                    top_c3_right.orientation = 0
                    top_c3_right.layer = met3_capmetbottom
                    top_c3_right.center[1] += mimcap_single_size*2*(3/6)
                elif colnum == 6:
                    top_c4_right = base_east_port_metal2_down.copy()
                    top_c4_right.name = "top_c4_right"
                    top_c4_right.orientation = 0
                    top_c4_right.layer = met3_capmetbottom
                    top_c4_right.center[1] += mimcap_single_size*2*(2/6)
                elif colnum == 7:
                    top_c5_right = base_east_port_metal2_down.copy()
                    top_c5_right.name = "top_c5_right"
                    top_c5_right.orientation = 0
                    top_c5_right.layer = met3_capmetbottom
                    top_c5_right.center[1] += mimcap_single_size*2*(1/6)

                    top_c5_center = base_east_port_metal2_down.copy()
                    top_c5_center.name = "top_c5_center"
                    top_c5_center.orientation = 0
                    top_c5_center.layer = met3_capmetbottom
                    top_c5_center.center[1] += mimcap_single_size*2*(1/6)
                    top_c5_center.center[0] = (top_c5_right.center[0]+top_c5_left.center[0])/2

                    top_c4_center = base_east_port_metal2_down.copy()
                    top_c4_center.name = "top_c4_center"
                    top_c4_center.orientation = 0
                    top_c4_center.layer = met3_capmetbottom
                    top_c4_center.center[1] += mimcap_single_size*2*(2/6)
                    top_c4_center.center[0] = (top_c4_right.center[0]+top_c4_left.center[0])/2

                    top_c3_center = base_east_port_metal2_down.copy()
                    top_c3_center.name = "top_c3_center"
                    top_c3_center.orientation = 0
                    top_c3_center.layer = met3_capmetbottom
                    top_c3_center.center[1] += mimcap_single_size*2*(3/6)
                    top_c3_center.center[0] = (top_c3_right.center[0]+top_c3_left.center[0])/2

                    top_c2_center = base_east_port_metal2_down.copy()
                    top_c2_center.name = "top_c2_center"
                    top_c2_center.orientation = 0
                    top_c2_center.layer = met3_capmetbottom
                    top_c2_center.center[1] += mimcap_single_size*2*(4/6)
                    top_c2_center.center[0] = (top_c2_right.center[0]+top_c2_left.center[0])/2

    mimcap_arr << straight_route(pdk, top_c5_center, top_c5_left, width=met4_width, glayer1="met4", glayer2="met3", via2_alignment=("c","c"))
    mimcap_arr << straight_route(pdk, top_c5_center, top_c5_right, width=met4_width, glayer1="met4", glayer2="met3", via2_alignment=("c","c"))   
    mimcap_arr << straight_route(pdk, top_c4_center, top_c4_left, width=met4_width, glayer1="met4", glayer2="met3", via2_alignment=("c","c"))
    mimcap_arr << straight_route(pdk, top_c4_center, top_c4_right, width=met4_width, glayer1="met4", glayer2="met3", via2_alignment=("c","c"))
    mimcap_arr << straight_route(pdk, top_c3_center, top_c3_left, width=met4_width, glayer1="met4", glayer2="met3", via2_alignment=("c","c"))
    mimcap_arr << straight_route(pdk, top_c3_center, top_c3_right, width=met4_width, glayer1="met4", glayer2="met3", via2_alignment=("c","c"))
    mimcap_arr << straight_route(pdk, top_c2_center, top_c2_left, width=met4_width, glayer1="met4", glayer2="met3", via2_alignment=("c","c"))
    mimcap_arr << straight_route(pdk, top_c2_center, top_c2_right, width=met4_width, glayer1="met4", glayer2="met3", via2_alignment=("c","c"))

    for port_pair in port_pairs:
        mimcap_arr << straight_route(pdk, port_pair[0], port_pair[1], width=met4_width) #via1_alignment=("c","c"))

    cap_ref = dac_mim_cap.add_ref(mimcap_arr)
    #cap_ref.movey(-30)

    dac_mim_cap.add_ports(mimcap_arr.get_ports_list(), prefix="mimcap_arr_")

    #dac_mim_cap.pprint_ports()
    top_level = add_mimCapArray_port(
        pdk=pdk,
        comp=dac_mim_cap,
        cap_num=6,
        port_assignment=["top_c5", "top_c4", "reserved", "top_c3", "reserved", "top_c2", "top_c_dummy", "top_c1", "top_c0", "reserved", "reserved", "reserved", "reserved", "reserved", "reserved", "reserved"],
        port_layer="met3"
    )
    
    return top_level

def add_mimCapArray_port(
    pdk: MappedPDK,
	comp: Component,
    cap_num: int,
	port_assignment: List[str],
	port_layer: str,
) -> Component:
    comp.unlock()
    pin_info = list() # list that contains all port and component information
    li_pin=(pdk.get_glayer("met1")[0], 16)
    li_label=(pdk.get_glayer("met1")[0], 5)
    met1_pin=(pdk.get_glayer("met2")[0], 16)
    met1_label=(pdk.get_glayer("met2")[0], 5)
    met2_pin=(pdk.get_glayer("met3")[0], 16)
    met2_label=(pdk.get_glayer("met3")[0], 5)
    port_size = (0.24, 0.24)

    if port_layer=="met1":
        pin_layer = li_pin
        label_layer = li_label
    elif port_layer=="met2":
        pin_layer = met1_pin
        label_layer = met1_label
    elif port_layer=="met3":
        pin_layer = met2_pin
        label_layer = met2_label

    port_id = 0
    stick_cnt = 0
    for port in port_assignment:
        if port != "reserved":
            comp.add_port(
                name=port,
                center=vertical_sticks[stick_cnt]['down'],
                width=vertical_sticks[stick_cnt]['width'],
                orientation=vertical_sticks[stick_cnt]['orientation'],
                layer=vertical_sticks[stick_cnt]['layer']
            )
            cap_pin=rectangle(layer=pin_layer, size=port_size, centered=True).copy()
            cap_pin.add_label(text=port, layer=label_layer)
            pin_info.append((cap_pin, comp.ports.get(port), ('c', 't')))
            port_id += 1

        stick_cnt += 1
    
    # Move the new ports above to the positions aligned with the existing ports on the top level 
    for c, prt, alignment in pin_info:
        alignment = ('c', 'b') if alignment is None else alignment
        c_ref = align_comp_to_port(c, prt, alignment=alignment)
        comp.add(c_ref)

    return comp

# Create and show the DAC MIM capacitor array layout
#dac_mimcap_component = create_6bit_dac_mimcap_array(sky130)
#dac_mimcap_component.name = "6bit_DAC_MIMCAP_Array"
#dac_mimcap_component.write_gds("mimcap_arr.gds")
#dac_mimcap_component.show()

#print("\n----- Generate Netlist -----")
#print(dac_mimcap_component.info["netlist"].generate_netlist())

# DRC
#drc_result = sky130.drc_magic(dac_mimcap_component,"6bit_DAC_MIMCAP_Array")
#print("\n----- DRC -----")
#print(drc_result)

# LVS
#lvs_result = sky130.lvs_netgen(dac_mimcap_component,"6bit_DAC_MIMCAP_Array")
#print("\n----- LVS -----")
#print(lvs_result)

#magic_drc_result = sky130.drc_magic(layout=dac_mimcap_component, design_name=gate_ctrl_inv.name, output_file=) # layout = /fullpath/*.gds
#magicのdrcを通したら，すぐに次に行く
#glayout/glayout/flow/pdk/mappedpdk.py
#sky130.lvs_netgen()
#ngspice_
#netlist.py
#cace
#glayout/glayout/flow/blocks/elementary/current_mirror/current_mirror.pyOp