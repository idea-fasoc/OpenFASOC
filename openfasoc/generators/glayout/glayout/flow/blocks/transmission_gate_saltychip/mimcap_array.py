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

import copy

def get_mimcap_layerconstruction_info(pdk: MappedPDK) -> tuple[str,str]:
	"""returns the glayer metal below and glayer metal above capmet
	args: pdk
	"""
	capmettop = pdk.layer_to_glayer(pdk.get_grule("capmet")["capmettop"])
	capmetbottom = pdk.layer_to_glayer(pdk.get_grule("capmet")["capmetbottom"])
	pdk.has_required_glayers(["capmet",capmettop,capmetbottom])
	pdk.activate()
	return capmettop, capmetbottom

def create_6bit_dac_mimcap_array(pdk: MappedPDK):
    """
    Creates a 6-bit DAC using an 8x8 MIM capacitor array with binary weighting.
    """
    # Create the top-level component
    dac_mim_cap = Component("6bit_DAC_MIMCAP_Array")

    '''
    # Define unit capacitor size (for example, 2x2 microns)
    unit_size = [5.0, 5.0]
    unit_mimcap = mimcap(pdk, size=unit_size)

    # Define bit weights for binary weighted capacitors
    bit_weights = [32, 16, 8, 4, 2, 1]  # From MSB to LSB
    total_units = sum(bit_weights)
    total_caps = 64  # 8x8 array
    dummy_units = total_caps - total_units  # Extra units as dummy

    # Generate common centroid indices for optimal matching
    cap_indices = [(i, j) for i in range(8) for j in range(8)]
    '''

    # metal and via layers
    met2 = pdk.get_glayer('met3')
    met3_capmetbottom = pdk.get_glayer('met4')
    met4_capmettop = pdk.get_glayer('met5')
    via3 = pdk.get_glayer('via4')
    mimcap_arr = Component("mimcap_arr")
    #test_cap << rectangle(size=(1, 1), layer=via3)
    mimcap_single_size = 5
    mimcap_single = mimcap(pdk, size=(mimcap_single_size,mimcap_single_size))
    rows_num = 8 
    columns_num = 8
    mimcap_space = 10*pdk.get_grule("capmet")["min_separation"]
    met4_width = pdk.get_grule("met5")["min_width"]
    array_ref = mimcap_arr << prec_array(mimcap_single, rows=rows_num, columns=columns_num, spacing=2*[mimcap_space])
    mimcap_arr.add_ports(array_ref.get_ports_list())
    mim_metal_space = mimcap_space/9
    #####################
    port_pairs = list()
    port_sides_pairs = list()
    via_refs = list()
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

            # Top metal
            level = "top_met_"
            position_up = "up_"
            position_down = "down_"
            position_right = "right_"
            position_left = "left_"
            layer = capmettop
            base_east_port = mimcap_arr.ports.get(base_mimcap+level+"E")
            met4_distance_from_center = base_east_port.width/2 - pdk.get_grule(layer)["min_width"]
            if base_east_port is not None: 
                base_east_port_up = base_east_port.copy()
                base_east_port_up.name = base_mimcap+position_up+level+"E"
                base_east_port_up.center[1] += met4_distance_from_center #(base_east_port_up.width/2 - pdk.get_grule(layer)["min_width"])
                base_east_port_up_space1 = base_east_port_up.copy()
                base_east_port_up_space1.name = base_mimcap+position_up+level+"W"
                base_east_port_up_space1.center[0] += mim_metal_space*1 
                base_east_port_up_space4 = base_east_port_up.copy()
                base_east_port_up_space4.name = base_mimcap+position_up+level+"W"
                base_east_port_up_space4.center[0] += mim_metal_space*4 
                base_east_port_down = base_east_port.copy()
                base_east_port_down.name = base_mimcap+position_down+level+"E"
                base_east_port_down.center[1] -= met4_distance_from_center #(base_north_port.width/2 - pdk.get_grule(layer)["min_width"])
                base_east_port_down_space1 = base_east_port_down.copy()
                base_east_port_down_space1.name = base_mimcap+position_down+level+"W"
                base_east_port_down_space1.center[0] += mim_metal_space*1 
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

            '''
            if rownum in (0,1,2,4):
                if colnum == 0:
                    base_west_side_port = mimcap_arr.ports.get(base_mimcap+level+"W")
                    base_west_side_port.name = base_mimcap+level+"westside_"+"W"
                    base_west_side_port.center
                     += met4_distance_from_center 
            else:    
                if colnum == 7:
            '''

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
                if colnum in (5,6): #(1,7)
                    port_pairs.append((base_east_port_up,base_east_port_up_space1,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space1,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space7,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space7,layer))
                    via_mimcap = via_stack(pdk, "met3", capmettop)
                    #via_mimcap = via_array(pdk, "met3", capmettop, size=(met4_width,met4_width), num_vias=(2,2), fullbottom=False)
                    via_refs.append(align_comp_to_port(via_mimcap, right_west_port_up_space7, ("c", "c")))
                elif colnum == columns_num-1:
                    pass #continue
                else:
                    port_pairs.append((base_east_port_up,right_west_port_up,layer))
                    port_pairs.append((base_east_port_down,right_west_port_down,layer))
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
                elif colnum in (1,6): #(1,7)
                    port_pairs.append((base_east_port_up,base_east_port_up_space1,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space1,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space7,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space7,layer))
                elif colnum == 4: #(4,3)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space3,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space3,layer))
                elif colnum == columns_num-1:
                    pass #continue
                else:
                    port_pairs.append((base_east_port_up,right_west_port_up,layer))
                    port_pairs.append((base_east_port_down,right_west_port_down,layer))
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
                if colnum in (4,5): #(4,4)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum in (0,6): #(1,7)
                    port_pairs.append((base_east_port_up,base_east_port_up_space1,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space1,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space7,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space7,layer))
                elif colnum == 3: #(4,3)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space3,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space3,layer))
                elif colnum == columns_num-1:
                    pass #continue
                else:
                    port_pairs.append((base_east_port_up,right_west_port_up,layer))
                    port_pairs.append((base_east_port_down,right_west_port_down,layer))
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
                if colnum in (0,1,2,3): #(4,4)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum == columns_num-1:
                    pass #continue
                else:
                    port_pairs.append((base_east_port_up,right_west_port_up,layer))
                    port_pairs.append((base_east_port_down,right_west_port_down,layer))
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
                if colnum in (2,3): #(4,4)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum in (5,6): #(1,7)
                    port_pairs.append((base_east_port_up,base_east_port_up_space1,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space1,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space7,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space7,layer))
                elif colnum == 4: #(4,3)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space3,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space3,layer))
                elif colnum == columns_num-1:
                    pass #continue
                else:
                    port_pairs.append((base_east_port_up,right_west_port_up,layer))
                    port_pairs.append((base_east_port_down,right_west_port_down,layer))
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
                if colnum in (2,3,6): #(4,4)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum == 1: #(1,7)
                    port_pairs.append((base_east_port_up,base_east_port_up_space1,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space1,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space7,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space7,layer))
                elif colnum == 0: #(4,3)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space3,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space3,layer))
                elif colnum == columns_num-1:
                    pass #continue
                else:
                    port_pairs.append((base_east_port_up,right_west_port_up,layer))
                    port_pairs.append((base_east_port_down,right_west_port_down,layer))
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
                if colnum in (1,2,3,4,5,6): #(4,4)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum == 0: #(4,3)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space3,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space3,layer))
                elif colnum == columns_num-1:
                    pass #continue
                else:
                    port_pairs.append((base_east_port_up,right_west_port_up,layer))
                    port_pairs.append((base_east_port_down,right_west_port_down,layer))
            elif rownum == 7:                    
                # West and East
                if colnum == 1: #(4,4)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space4,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space4,layer))
                elif colnum == 0: #(4,3)
                    port_pairs.append((base_east_port_up,base_east_port_up_space4,layer))
                    port_pairs.append((base_east_port_down,base_east_port_down_space4,layer))
                    port_pairs.append((right_west_port_up,right_west_port_up_space3,layer))
                    port_pairs.append((right_west_port_down,right_west_port_down_space3,layer))
                elif colnum == columns_num-1:
                    pass #continue
                else:
                    port_pairs.append((base_east_port_up,right_west_port_up,layer))
                    port_pairs.append((base_east_port_down,right_west_port_down,layer))

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
                    base_east_port_metal2_down.center[1] -= (mimcap_single_size*15/2 + mimcap_space*8)
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
                    base_west_port_metal2_down.center[1] -= (mimcap_single_size*15/2 + mimcap_space*8)
                else: 
                    base_west_port_metal2_down.center[1] -= (mimcap_single_size*17/2 + mimcap_space*8)
                port_pairs.append((base_west_port_metal2_up,base_west_port_metal2_down,layer))
            
    for port_pair in port_pairs:
        mimcap_arr << straight_route(pdk, port_pair[0], port_pair[1], width=met4_width) 
    for via_ref in via_refs:
        mimcap_arr.add(via_refs)

    cap_ref = dac_mim_cap.add_ref(mimcap_arr)
    #cap_ref.movey(-30)

   
    return dac_mim_cap



# Create and show the DAC MIM capacitor array layout
dac_mimcap_component = create_6bit_dac_mimcap_array(sky130).show()
