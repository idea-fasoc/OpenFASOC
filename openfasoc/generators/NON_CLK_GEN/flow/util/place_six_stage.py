import re
import math

# import gdsfactory as gf

# r_def = open("./results/sky130hs/dcdc/2_1_floorplan.def", "r")
# lines = list(r_def.readlines())
# w_def = open("2_1_floorplan_six_stage_placed.def", "w")

r_def = open("./results/sky130hs/dcdc/2_1_floorplan.def", "r")
lines = list(r_def.readlines())
# dbu = 1000

w_macro_place = open("./results/sky130hs/dcdc/six_stage.macro_placment.cfg", "w")

# create a dictionary to store the data
six_stages = dict()
other_components_for_apr = set()

# create a gf component
# six_stage_gf_com = gf.Component("six_stage_conv")

# read in Cell gds files and obtain bbox
# conv21_cell_com = gf.import_gds("../../blocks/sky130hs/gds/DCDC_CONV2TO1.gds")
# cap_cell_com = gf.import_gds("../../blocks/sky130hs/gds/DCDC_CAP_UNIT.gds")
# mux_cell_com = gf.import_gds("../../blocks/sky130hs/gds/DCDC_MUX.gds")

# conv21_cell_bbox = conv21_cell_com.bbox
# cap_cell_bbox = cap_cell_com.bbox
# mux_cell_bbox = mux_cell_com.bbox

# conv21_cell_w = conv21_cell_bbox[1][0] - conv21_cell_bbox[0][0]
# conv21_cell_h = conv21_cell_bbox[1][1] - conv21_cell_bbox[0][1]
# cap_cell_w = cap_cell_bbox[1][0] - cap_cell_bbox[0][0]
# cap_cell_h = cap_cell_bbox[1][1] - cap_cell_bbox[0][1]
# mux_cell_w = mux_cell_bbox[1][0] - mux_cell_bbox[0][0]
# mux_cell_h = mux_cell_bbox[1][1] - mux_cell_bbox[0][1]

conv21_cell_w = 30
conv21_cell_h = 40
cap_cell_w = 8
cap_cell_h = 20
mux_cell_w = 30
mux_cell_h = 30

offset_x = 50
offset_y = 50

# list to store lines outside of COMPONENTS
lines_no_com = []

# parse the input DEF file
# only take the lines inside of COMPONENTS
is_component = False
for line in lines:
    # set is_component based on the line
    if line.find("END COMPONENTS") == 0:
        is_component = False
    elif line.find("COMPONENTS") == 0:
        is_component = True
        lines_no_com.append(line)
        continue

    if not is_component:
        lines_no_com.append(line)
    else:
        # extract module name on line
        line_split = line.strip().split(" ")[:-1]
        module_name = line_split[-1]

        # For different cells, different cases
        stage_num = -1
        inst_num_in_stage = -1

        instance_split = re.split(r"\\\[|\\\]", line_split[1])

        stage_num = int(instance_split[1])
        inst_num_in_stage = int(instance_split[3])

        # check if dict key-value pair is empty
        if stage_num not in six_stages:
            six_stages[stage_num] = dict()

        if module_name == "DCDC_CONV2TO1":
            # handle dict initialization
            if "DCDC_CONV2TO1" not in six_stages[stage_num]:
                six_stages[stage_num]["DCDC_CONV2TO1"] = dict()
            six_stages[stage_num]["DCDC_CONV2TO1"][inst_num_in_stage] = line_split
        elif module_name == "DCDC_CAP_UNIT":
            # handle dict initialization
            if "DCDC_CAP_UNIT_R" not in six_stages[stage_num]:
                six_stages[stage_num]["DCDC_CAP_UNIT_R"] = dict()
            if "DCDC_CAP_UNIT_L" not in six_stages[stage_num]:
                six_stages[stage_num]["DCDC_CAP_UNIT_L"] = dict()
            if instance_split[-1].find("1") != -1:  # left 0 right 1
                cap_name = "DCDC_CAP_UNIT_R"
            else:
                cap_name = "DCDC_CAP_UNIT_L"
            # use different names for left and right caps
            six_stages[stage_num][cap_name][inst_num_in_stage] = line_split
        elif module_name == "DCDC_MUX":
            # handle dict initialization
            if "DCDC_MUX" not in six_stages[stage_num]:
                six_stages[stage_num]["DCDC_MUX"] = dict()
            six_stages[stage_num]["DCDC_MUX"][inst_num_in_stage] = line_split
        else:
            # place component into set to bypass processing
            other_components_for_apr.add(line)

# obtain the height of the second stage as a reference (The number of conv21 in second stags)
conv21_height_ref = len(six_stages[1]["DCDC_CONV2TO1"])

# store stage offsets as an accumulative value
stage_offset_x = 0

cap_section_offset = 0

for stage_num in range(0, 6):
    # calculate grid dimension at current stage
    conv21_array_dim_x = math.ceil(
        len(six_stages[stage_num]["DCDC_CONV2TO1"]) / conv21_height_ref
    )

    for cell_num in range(len(six_stages[stage_num]["DCDC_CAP_UNIT_L"])):
        # place cells (x, y) in a tuple
        cell_array_coord = (
            cell_num % conv21_array_dim_x,
            cell_num // conv21_array_dim_x,
        )
        cell_actual_coord = (
            cell_array_coord[0] * conv21_cell_w
            + stage_offset_x
            + conv21_cell_w / 4
            - cap_cell_w / 2,
            -(cell_array_coord[1] + 2) * cap_cell_h,
        )

        # save the max offset
        if (cell_array_coord[1] + 2) * cap_cell_h > cap_section_offset:
            cap_section_offset = (cell_array_coord[1] + 2) * cap_cell_h

        # place cell using gdsfactory
        # gf_ref = six_stage_gf_com << cap_cell_com
        # gf_ref.move(cell_actual_coord)

        # store placement into dictionary
        six_stages[stage_num]["DCDC_CAP_UNIT_L"][cell_num].extend(
            [cell_actual_coord[0], cell_actual_coord[1]]
        )

    for cell_num in range(len(six_stages[stage_num]["DCDC_CAP_UNIT_R"])):
        # place cells (x, y) in a tuple
        cell_array_coord = (
            cell_num % conv21_array_dim_x,
            cell_num // conv21_array_dim_x,
        )
        cell_actual_coord = (
            cell_array_coord[0] * conv21_cell_w
            + stage_offset_x
            + conv21_cell_w * 3 / 4
            - cap_cell_w / 2,
            -(cell_array_coord[1] + 2) * cap_cell_h,
        )

        # place cell using gdsfactory
        # gf_ref = six_stage_gf_com << cap_cell_com
        # gf_ref.move(cell_actual_coord)

        # store placement into dictionary
        six_stages[stage_num]["DCDC_CAP_UNIT_R"][cell_num].extend(
            [cell_actual_coord[0], cell_actual_coord[1]]
        )

    # calculate coord for each cell
    for cell_num in range(len(six_stages[stage_num]["DCDC_CONV2TO1"])):
        # place cells (x, y) in a tuple
        cell_array_coord = (
            cell_num % conv21_array_dim_x,
            cell_num // conv21_array_dim_x,
        )
        cell_actual_coord = (
            cell_array_coord[0] * conv21_cell_w + stage_offset_x,
            cell_array_coord[1] * conv21_cell_h,
        )

        # place cell using gdsfactory
        # gf_ref = six_stage_gf_com << conv21_cell_com
        # gf_ref.move(cell_actual_coord)

        # store placement into dictionary
        six_stages[stage_num]["DCDC_CONV2TO1"][cell_num].extend(
            [cell_actual_coord[0], cell_actual_coord[1]]
        )

    for cell_num in range(len(six_stages[stage_num]["DCDC_MUX"])):
        # place cells (x, y) in a tuple
        mux_x_dim = (conv21_array_dim_x * conv21_cell_w) // mux_cell_w
        cell_array_coord = (cell_num % mux_x_dim, cell_num // mux_x_dim)
        cell_actual_coord = (
            cell_array_coord[0] * mux_cell_w + stage_offset_x,
            cell_array_coord[1] * mux_cell_h + conv21_height_ref * conv21_cell_h,
        )

        # place cell using gdsfactory
        # gf_ref = six_stage_gf_com << mux_cell_com
        # gf_ref.move(cell_actual_coord)

        # store placement into dictionary
        six_stages[stage_num]["DCDC_MUX"][cell_num].extend(
            [cell_actual_coord[0], cell_actual_coord[1]]
        )

    # update offset for next stage
    stage_offset_x += (conv21_array_dim_x) * conv21_cell_w

# output gds
# six_stage_gf_com.write_gds("out.gds")

# DEF manipulation
# remove all cells that have been stored in py
is_component = False
for line in lines_no_com:

    # output the line into file
    # w_def.write(line)

    # set is_component based on the line
    if line.find("END COMPONENTS") == 0:
        is_component = False
    elif line.find("COMPONENTS") == 0:
        is_component = True

    # if inside component, immediatly write the results previously stored in the dictionaries
    if is_component:
        # write six-stage auxcells
        for stage_num in range(0, 6):
            for auxcell in six_stages[stage_num]:
                for inst in six_stages[stage_num][auxcell]:
                    value = six_stages[stage_num][auxcell][inst]
                    complete_line_split = []
                    complete_line_split.append(value[1])
                    complete_line_split.extend(
                        [
                            "R0",
                            "{:.3f}".format(value[3] + offset_x),
                            "{:.3f}".format(value[4] + cap_section_offset + offset_y),
                            "\n",
                        ]
                    )
                    # complete_line_split.extend(["+", "PLACED", "(", str(value[3]), str(value[4] + cap_section_offset*dbu), ")", "N", ";", "\n"])
                    complete_line = " ".join(complete_line_split)
                    complete_line = complete_line.replace("\\", r"\\")
                    print(complete_line)
                    # w_def.write("    "+complete_line)
                    w_macro_place.write(complete_line)

        # # write other components
        # for com in other_components_for_apr:
        #     w_def.write(com)
