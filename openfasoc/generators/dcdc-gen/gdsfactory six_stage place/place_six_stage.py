import re
import math
import gdsfactory as gf

# r_def = open("./results/sky130hs/dcdc/2_1_floorplan.def", "r")
# lines = list(r_def.readlines())
# w_def = open("2_1_floorplan_six_stage_placed.def", "w")

r_def = open("./2_1_floorplan.def", "r")
lines = list(r_def.readlines())
# dbu = 1000

# w_macro_place = open("./results/sky130hs/dcdc/six_stage.macro_placment.cfg", "w")

# create a dictionary to store the data
six_stages = dict()
other_components_for_apr = set()

# create a gf component
six_stage_gf_com = gf.Component("six_stage_conv")


def label(loc, layer, text):
    six_stage_gf_com.add_label(text=text, position=loc, layer=(layer, 5))
    six_stage_gf_com.add_polygon(
        [
            (loc[0] - 0.01, loc[1] - 0.01),
            (loc[0] + 0.01, loc[1] - 0.01),
            (loc[0] + 0.01, loc[1] + 0.01),
            (loc[0] - 0.01, loc[1] + 0.01),
        ],
        layer=(layer, 16),
    )


# read in Cell gds files and obtain bbox
conv21_cell_com = gf.import_gds("./DCDC_CONV2TO1.gds")
conv21_cell_placeholder_com = gf.import_gds("./DCDC_CONV2TO1_placeholder.gds")
conv21_cell_adapter_com = gf.import_gds("./DCDC_CONV2TO1_adapter.gds")
cap_cell_adapter_com_0 = gf.import_gds("./DCDC_CAP_UNIT_adapter_0.gds")
cap_cell_adapter_com_1 = gf.import_gds("./DCDC_CAP_UNIT_adapter_1.gds")
cap_cell_com = gf.import_gds("./DCDC_CAP_UNIT.gds")
mux_cell_com = gf.import_gds("./DCDC_MUX.gds")
inter_stage_com = gf.import_gds("./inter_stage.gds")
inter_stage_vbus_com = gf.import_gds("./inter_stage_vbus.gds")
mux_adapter_com = gf.import_gds("./DCDC_MUX_adapter.gds")

conv21_cell_bbox = conv21_cell_com.bbox
cap_cell_bbox = cap_cell_com.bbox
mux_cell_bbox = mux_cell_com.bbox
conv21_cell_adapter_bbox = conv21_cell_adapter_com.bbox
inter_stage_bbox = inter_stage_com.bbox

conv21_cell_w = conv21_cell_bbox[1][0] - conv21_cell_bbox[0][0]
conv21_cell_h = conv21_cell_bbox[1][1] - conv21_cell_bbox[0][1]
cap_cell_w = cap_cell_bbox[1][0] - cap_cell_bbox[0][0]
cap_cell_h = cap_cell_bbox[1][1] - cap_cell_bbox[0][1]
mux_cell_w = mux_cell_bbox[1][0] - mux_cell_bbox[0][0]
mux_cell_h = mux_cell_bbox[1][1] - mux_cell_bbox[0][1]
conv21_cell_adapter_w = conv21_cell_adapter_bbox[1][0] - conv21_cell_adapter_bbox[0][0]
conv21_cell_adapter_h = conv21_cell_adapter_bbox[1][1] - conv21_cell_adapter_bbox[0][1]
inter_stage_w = inter_stage_bbox[1][0] - inter_stage_bbox[0][0]
inter_stage_h = conv21_cell_h

sel_h_offset = (0.5, 6)
sel_l_offset = (0.5, 1)

# conv21_cell_w = 18.88 + 10
# conv21_cell_h = 36.96 + 10
# cap_cell_w = 8
# cap_cell_h = 20
# mux_cell_w = 8.6 + 2
# mux_cell_h = 30.24

offset_x = 0
offset_y = 0

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

if conv21_height_ref > 200:
    conv21_height_ref = 200

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
            -(cell_array_coord[1] + 1) * cap_cell_h,
        )

        # save the max offset
        if (cell_array_coord[1] + 2) * cap_cell_h > cap_section_offset:
            cap_section_offset = (cell_array_coord[1] + 2) * cap_cell_h

        # place cell using gdsfactory
        gf_ref = six_stage_gf_com << cap_cell_com
        gf_ref.move(cell_actual_coord)

        # if first row, place apapters
        if cell_array_coord[1] == 0:
            gf_ref = six_stage_gf_com << cap_cell_adapter_com_0
            gf_ref.move((cell_actual_coord[0], 0))

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
            -(cell_array_coord[1] + 1) * cap_cell_h,
        )

        # place cell using gdsfactory
        gf_ref = six_stage_gf_com << cap_cell_com
        gf_ref.move(cell_actual_coord)

        # if first row, place apapters
        if cell_array_coord[1] == 0:
            gf_ref = six_stage_gf_com << cap_cell_adapter_com_1
            gf_ref.move((cell_actual_coord[0], 0))

        # store placement into dictionary
        six_stages[stage_num]["DCDC_CAP_UNIT_R"][cell_num].extend(
            [cell_actual_coord[0], cell_actual_coord[1]]
        )

    # calculate coord for each cell
    grid_count = conv21_height_ref * conv21_array_dim_x
    for cell_num in range(grid_count):
        # place cells (x, y) in a tuple
        cell_array_coord = (
            cell_num % conv21_array_dim_x,
            cell_num // conv21_array_dim_x,
        )
        cell_actual_coord = (
            cell_array_coord[0] * conv21_cell_w + stage_offset_x,
            cell_array_coord[1] * conv21_cell_h,
        )

        # place adapter for last row
        if cell_array_coord[1] + 1 == conv21_height_ref:
            # place cell using gdsfactory
            adapter_array_coord = (cell_array_coord[0], cell_array_coord[1] + 1)
            adapter_actual_coord = (
                adapter_array_coord[0] * conv21_cell_w + stage_offset_x,
                adapter_array_coord[1] * conv21_cell_h,
            )

            gf_ref = six_stage_gf_com << conv21_cell_adapter_com
            gf_ref.move(adapter_actual_coord)

        if cell_num < len(six_stages[stage_num]["DCDC_CONV2TO1"]):
            # place cell using gdsfactory
            gf_ref = six_stage_gf_com << conv21_cell_com
            gf_ref.move(cell_actual_coord)

            # store placement into dictionary
            six_stages[stage_num]["DCDC_CONV2TO1"][cell_num].extend(
                [cell_actual_coord[0], cell_actual_coord[1]]
            )
        else:
            # place cell using gdsfactory
            gf_ref = six_stage_gf_com << conv21_cell_placeholder_com
            gf_ref.move(cell_actual_coord)

    for cell_num in range(len(six_stages[stage_num]["DCDC_MUX"])):
        # place cells (x, y) in a tuple
        mux_x_dim = (conv21_array_dim_x * conv21_cell_w) // mux_cell_w
        cell_array_coord = (cell_num % mux_x_dim, cell_num // mux_x_dim)

        # cell_actual_coord_mux_adapter = (cell_array_coord[0] * mux_cell_w + stage_offset_x,cell_array_coord[1] * mux_cell_h + conv21_height_ref * conv21_cell_h)
        cell_actual_coord_mux = (
            cell_array_coord[0] * mux_cell_w + stage_offset_x,
            cell_array_coord[1] * mux_cell_h
            + conv21_height_ref * conv21_cell_h
            + conv21_cell_adapter_h,
        )

        # place cell using gdsfactory
        gf_ref = six_stage_gf_com << mux_cell_com
        gf_ref.move(cell_actual_coord_mux)

        # place mux adapter
        if cell_array_coord[1] == 0:
            gf_ref = six_stage_gf_com << mux_adapter_com
            gf_ref.move(cell_actual_coord_mux)

        # store placement into dictionary
        six_stages[stage_num]["DCDC_MUX"][cell_num].extend(
            [cell_actual_coord_mux[0], cell_actual_coord_mux[1]]
        )

    # place sel_h and sel_l labels
    # six_stage_gf_com.add_label(text=f"SEL_H[{stage_num}]", position=(stage_offset_x + sel_h_offset[0], conv21_height_ref * conv21_cell_h + conv21_cell_adapter_h + sel_h_offset[1]), layer=(70, 5))
    # six_stage_gf_com.add_label(text=f"SEL_L[{stage_num}]", position=(stage_offset_x + sel_l_offset[0], conv21_height_ref * conv21_cell_h + conv21_cell_adapter_h + sel_l_offset[1]), layer=(70, 5))
    label(
        (
            stage_offset_x + sel_h_offset[0],
            conv21_height_ref * conv21_cell_h + conv21_cell_adapter_h + sel_h_offset[1],
        ),
        70,
        f"SEL_H[{stage_num}]",
    )
    label(
        (
            stage_offset_x + sel_l_offset[0],
            conv21_height_ref * conv21_cell_h + conv21_cell_adapter_h + sel_l_offset[1],
        ),
        70,
        f"SEL_L[{stage_num}]",
    )

    # update offset for next stage
    stage_offset_x += (conv21_array_dim_x) * conv21_cell_w

    # place inter-stage connectors
    if stage_num < 6 - 1:
        for i in range(conv21_height_ref):
            gf_ref = six_stage_gf_com << inter_stage_com
            gf_ref.move((stage_offset_x, i * inter_stage_h))

        # place inter-stage vbus connectors
        gf_ref = six_stage_gf_com << inter_stage_vbus_com
        gf_ref.move((stage_offset_x, conv21_height_ref * inter_stage_h))

    # update offset for next stage`
    stage_offset_x += inter_stage_w

# TEMPORARY: CLK and VDD VSS Label placement
# six_stage_gf_com.add_label(text=f"clk0", position=(0.5, 28.2), layer=(68, 5))
# six_stage_gf_com.add_label(text=f"clk1", position=(0.5, 27.3), layer=(68, 5))
# six_stage_gf_com.add_label(text=f"clk0b", position=(0.5, 8.8), layer=(68, 5))
# six_stage_gf_com.add_label(text=f"clk1b", position=(0.5, 9.6), layer=(68, 5))

# six_stage_gf_com.add_label(text=f"VPWR", position=(0.5, 18), layer=(70, 5))
# six_stage_gf_com.add_label(text=f"VGND", position=(0.5, 18.9), layer=(70, 5))

# six_stage_gf_com.add_label(text=f"OUT", position=(stage_offset_x - inter_stage_w - 0.5, conv21_height_ref * inter_stage_h + 10), layer=(70, 5))

label((0.5, 28.2), 68, f"clk0")
label((0.5, 27.3), 68, f"clk1")
label((0.5, 8.8), 68, f"clk0b")
label((0.5, 9.6), 68, f"clk1b")

label((0.5, 18), 70, f"VPWR")
label((0.5, 18.9), 70, f"VGND")

label(
    (stage_offset_x - inter_stage_w - 0.5, conv21_height_ref * inter_stage_h + 10),
    70,
    f"OUT",
)
label((0.5, conv21_height_ref * inter_stage_h + 14), 70, f"IN_GND")

# output gds
six_stage_gf_com.write_gds("out.gds")

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
                    # print(complete_line)
                    # w_def.write("    "+complete_line)
                    # w_macro_place.write(complete_line)

        # # write other components
        # for com in other_components_for_apr:
        #     w_def.write(com)
