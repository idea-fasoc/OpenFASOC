import argparse  # argument parsing
import math
import re


def place_inv(fp_dim, array_dim, cell_dim) -> None:
    r_def = open(args.inputDef, "r")
    lines = list(r_def.readlines())
    w_def = open(args.outputDef, "w")

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
        if line.find("END COMPONENTS") == 0:
            is_component = False
        elif line.find("COMPONENTS") == 0:
            is_component = True

        # only process the inv lines that are within COMPONENTS
        if line.find(target_instance) != -1 and is_component:

            def_component = line.strip().split(" ")[1:3]

            # inst_name is the part after the '.'
            inst_name = def_component[0].split(".")[1]

            # inst_num is the last set of digits
            find_last_num = re.findall(r"\d+", inst_name)

            # for inv in array
            if len(find_last_num) != 0 and line.find("inv") != -1:
                inst_num = int(find_last_num[-1])
                # cell = def_component[1]

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
    for i in range(0, int(math.ceil(len(inv_array_dict) / 1))):

        inv_sm = i
        inv_lg = max_inst_num - i

        y_index_sm = (i // x) * 2
        y_index_lg = (i // x) * 2 + 1

        # for cells on columns that have (x_index_sm / 2) % 2 == 1, their y_indices should be flipped
        # arrange_direction: 1 => reversed, 0 => same as index
        arrange_direction = (y_index_sm / 2) % 2

        if arrange_direction:
            x_index = x - (i % x)
            ori_sm = "FN"
            ori_lg = "FS"
        else:
            x_index = i % x + 1
            ori_sm = "N"
            ori_lg = "S"

        coord_sm = (
            math.floor(math.floor(p / a) / (x + 1)) * (x_index + 1) * a,
            math.floor(math.floor(q / b) / (y)) * (y_index_sm) * b,
        )
        coord_lg = (
            math.floor(math.floor(p / a) / (x + 1)) * (x_index + 1) * a,
            math.floor(math.floor(q / b) / (y)) * (y_index_lg) * b,
        )

        # move the smaller one left by 3 units to avoid overlap
        # new_sm_coord_x = coord_sm[0] - 3 * a
        # coord_sm = (new_sm_coord_x, coord_sm[1])

        print("Inv", inv_sm, "(", x_index, ",", y_index_sm, ")", coord_sm)
        print("Inv", inv_lg, "(", x_index, ",", y_index_lg, ")", coord_lg)

        # store inside dictionary
        inv_array_dict[inv_sm].extend([ori_sm, coord_sm])
        inv_array_dict[inv_lg].extend([ori_lg, coord_lg])

    # assign positions to each of the other components inside other_comp_dict, remove the old component placements in "lines" on the go
    coord_nand = (
        math.floor(math.floor(p / a) / (x + 1)) * (1) * a,
        math.floor(math.floor(q / b) / (y)) * (1) * b,
    )
    coord_invout = (
        math.floor(math.floor(p / a) / (x + 1)) * (1) * a,
        math.floor(math.floor(q / b) / (y)) * (0) * b,
    )

    # HARD CODED inv_out and nand placement
    other_comp_dict["a_inv_out"].extend(["N", coord_invout])
    other_comp_dict["a_nand_0"].extend(["S", coord_nand])

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
        if line.find("END COMPONENTS") == 0:
            is_component = False
        elif line.find("COMPONENTS") == 0:
            is_component = True

        # if inside component, immediatly write the results previously stored in the dictionaries
        if is_component:
            for key, value in inv_array_dict.items():
                # apply offset
                value[2] = tuple(map(sum, zip(value[2], core_die_offset)))

                insertion = [
                    "+",
                    "FIXED",
                    "(",
                    str(round(value[2][0] * 1000)),
                    str(round(value[2][1] * 1000)),
                    ")",
                    value[1],
                    ";",
                ]
                new_line = value[0].replace(";", " ".join(insertion))
                # print(new_line)
                w_def.writelines(new_line)

            for key, value in other_comp_dict.items():
                value[2] = tuple(map(sum, zip(value[2], core_die_offset)))
                insertion = [
                    "+",
                    "FIXED",
                    "(",
                    str(round(value[2][0] * 1000)),
                    str(round(value[2][1] * 1000)),
                    ")",
                    value[1],
                    ";",
                ]
                new_line = value[0].replace(";", " ".join(insertion))
                # print(new_line)
                w_def.writelines(new_line)

            # make is_component False so that the components are only written once
            is_component = False


parser = argparse.ArgumentParser(description="Place Ring Oscillator")
parser.add_argument("--inputDef", "-i", required=True, help="Input Def")
parser.add_argument("--outputDef", "-o", required=True, help="Output Def")
parser.add_argument("--coreDim", "-c", required=True, help="Core Dim")
parser.add_argument("--arrayDim", "-a", required=True, help="Array Dim")
parser.add_argument("--coreDieOffset", "-s", required=True, help="CoreDie Offset")
parser.add_argument("--cellDim", "-d", required=True, help="Cell Dim")
parser.add_argument("--targetInst", "-t", required=True, help="Target Inst")
args = parser.parse_args()


# Notice here the cell is horizontal, swap the ab in cell_dim (The unit dim)
core_dim = tuple(list(map(float, args.coreDim.split(","))))
array_dim = tuple(list(map(int, args.arrayDim.split(","))))
cell_dim = tuple(list(map(float, args.cellDim.split(","))))
core_die_offset = tuple(list(map(float, args.coreDieOffset.split(","))))
target_instance = args.targetInst


place_inv(core_dim, array_dim, cell_dim)
