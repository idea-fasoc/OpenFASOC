import re
import math

def place_inv(fp_dim, array_dim, cell_dim, srcDir, target_instance):
    r_def = open(srcDir + "./2_floorplan.def", "r")
    lines=list(r_def.readlines())
    w_def = open(srcDir + "./2_floorplan_ro.def", "w")
    
    # create a dictionary to store the data
    inv_array_dict = dict()
    other_comp_dict = dict()

    # retrieve parameters
    x, y = array_dim
    p, q = fp_dim
    a, b = cell_dim
    
    # keep track of max and min instance numbers
    max_inst_num = 0
    min_inst_num = 0

    # only take the lines inside of COMPONENTS
    is_component = False
    for line in lines:
        # set is_component based on the line
        if (line.find("END COMPONENTS") == 0):
            is_component = False
        elif (line.find("COMPONENTS") == 0):
            is_component = True
        
        # only process the inv lines that are within COMPONENTS
        if (line.find(target_instance) != -1 and is_component):

            def_component = line.strip().split(" ")[1:3]

            # inst_name is the part after the '.'
            inst_name = def_component[0] .split(".")[1]

            # inst_num is the last set of digits 
            find_last_num = re.findall(r'\d+',inst_name)

            # for inv in array
            if (len(find_last_num) != 0 and line.find("inv") != -1):
                inst_num = int(find_last_num[-1])
                #cell = def_component[1]

                # store the data inside of dict
                inv_array_dict[inst_num] = [line]

                # update max/min instance num
                if inst_num > max_inst_num:
                    max_inst_num = inst_num
                if inst_num < min_inst_num:
                    min_inst_num = inst_num
            # for all other components in ro
            else:
                other_comp_dict[inst_name] = [line]

    # assign positions to each inv in array inside inv_array_dict, remove the old component placements in "lines" on the go 
    # TODO: Take care of odd ninvs?
    for i in range (0, math.ceil(len(inv_array_dict) / 2)):

        inv_sm = i
        inv_lg = max_inst_num - i

        x_index_sm = x - (i // y ) * 2
        x_index_lg = x - ((i // y ) * 2 + 1)

        # for cells on columns that have (x_index_sm / 2) % 2 == 1, their y_indices should be flipped
        # arrange_direction: 1 => reversed, 0 => same as index
        arrange_direction = (x_index_sm / 2) % 2
        
        if arrange_direction:
            y_index = y - (i % y)
            ori_sm = 'E'
            ori_lg = 'W'
        else:
            y_index = i % y + 1
            ori_sm = 'W'
            ori_lg = 'E'

        coord_sm = (math.floor(math.floor(p / a) / (x + 1) ) * (x_index_sm) * a, math.floor(math.floor(q / b) / (y + 1)) * (y_index + 1) * b)
        coord_lg = (math.floor(math.floor(p / a) / (x + 1) ) * (x_index_lg) * a, math.floor(math.floor(q / b) / (y + 1)) * (y_index + 1) * b)

        #print("Inv", inv_sm, "(", x_index_sm, ",", y_index, ")", coord_sm)
        #print("Inv", inv_lg, "(", x_index_lg, ",", y_index, ")", coord_lg)

        # store inside dictionary
        inv_array_dict[inv_sm].extend([ori_sm,coord_sm])
        inv_array_dict[inv_lg].extend([ori_lg, coord_lg])

    # assign positions to each of the other components inside other_comp_dict, remove the old component placements in "lines" on the go 
    coord_nand = (math.floor(math.floor(p / a) / (x + 1) ) * (x - 1) * a, math.floor(math.floor(q / b) / (y + 1)) * (0 + 1) * b)
    coord_invout = (math.floor(math.floor(p / a) / (x + 1) ) * (x + 1) * a, math.floor(math.floor(q / b) / (y + 1)) * (0 + 1) * b)

    # HARD CODED inv_out and nand placement
    other_comp_dict['a_inv_out'].extend(['E', coord_invout])
    other_comp_dict['a_nand_0'].extend(['E', coord_nand])
    
    # remove the placed components from lines
    for key, value in inv_array_dict.items():
        lines.remove(value[0])

    for key, value in other_comp_dict.items():
        lines.remove(value[0])

    # write into def file
    # only take the lines inside of COMPONENTS
    is_component = False
    for line in lines:
        # output the line into file
        w_def.write(line)

        # set is_component based on the line
        if (line.find("END COMPONENTS") == 0):
            is_component = False
        elif (line.find("COMPONENTS") == 0):
            is_component = True

        # if inside component, immediatly write the results previously stored in the dictionaries
        if (is_component):
            for key, value in inv_array_dict.items():
                insertion = ["+", "FIXED", '(', str(round(value[2][0] * 1000)), str(round(value[2][1] * 1000)), ')', value[1], ';']
                new_line = value[0].replace(";", ' '.join(insertion))
                print(new_line)
                w_def.writelines(new_line)

                
            for key, value in other_comp_dict.items():
                insertion = ["+", "FIXED", '(', str(round(value[2][0] * 1000)), str(round(value[2][1] * 1000)), ')', value[1], ';'] 
                new_line = value[0].replace(";", ' '.join(insertion))
                print(new_line)
                w_def.writelines(new_line)

            # make is_component False so that the components are only written once
            is_component = False

if __name__ == "__main__":

    # Notice here the cell is horizontal, swap the ab in cell_dim (The unit dim)
    place_inv((40, 40), (12, 12), (2.72, 0.46), "", "cryo_ro_1")