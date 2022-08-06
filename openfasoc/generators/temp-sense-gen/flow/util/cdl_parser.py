# NOTE: AUG 2, 2022,
# This script takes the generated CDL file from openroad (which converts verilog to netlist)
# and modifies it so that a spice file is produced which is able to pass LVS
# This makes up for openroad issues in properly converting the verilog to netlist
# The execution of this file does as follow:
# 1) read 6_final.cdl and...
# 2) Add VDD VDD to the end of the HEADER pins (because when extracted from GDS you get proxy pins)
# 3) ASSUME OpenROAD v2.0-4508-ge036ecfac: The top level subckt has last pin being r_vin
# 3.1) delete the other “VIN” pin (because both r_VIN and VIN are actually the same thing)
# 4) replace all instance of VIN with r_VIN, so that the pin name is uniform
# 5) write this output into module_name.spice

import argparse
import os
import re
import sys

# /home/labtob/Documents/workFasoc/OpenFASOCtestcase/openfasoc/generators/temp-sense-gen/blocks/sky130hd/cdl
parser = argparse.ArgumentParser(description="formulate input cdl netlist")
parser.add_argument("--inputCdl", "-i", required=True, help="input CDL netlist")
parser.add_argument(
    "--stdLef",
    "-l",
    required=True,
    help="input standard LEF, showing pin order used in OpenROAD",
)
parser.add_argument("--stdCdl", "-s", required=True, help="standard cells CDL netlist")
# parser.add_argument("--headercdl", "-h", required=True, help="HEADER cell CDL netlist")
# parser.add_argument("--cdlslc", "-c", required=True, help="SLC cell CDL netlist")
parser.add_argument("--powerConn", "-p", required=False, help="power connection")
parser.add_argument("--outputCdl", "-o", required=True, help="output CDL netlist")

args = parser.parse_args()  # example arguments below:
# -i inputz/6_final.cdl -s inputz/sky130_fd_sc_hd.spice -l inputz/merged_spacing.lef -o output.spice

# pin order from input stdCdl netlist (inputz/sky130_fd_sc_hd.spice) read that entire file into "filedata"
with open(args.stdCdl, "r") as rf:
    filedata = rf.read()

std_pin_order_dict = {}  # map object, see notes in the for each loop below
std_cells_re = re.findall(
    "\.subckt (.*)", filedata
)  # "\.subckt (.*)" means all lines where ".subckt " occurs. Breakdown below
# The "\." is used to indicate "." without invoking special meaning, so look for ".subckt "
# The "." matches any char !except newline!, the "*" make the resulting Reg Exp match repetitions of the preceding RE
# () must be used with special chars. So basically (.*) means after the Reg Exp specified by "\.subckt ", match the rest of the line

for std_cell in std_cells_re:
    std_cell_info = std_cell.split(" ")
    # std_cell example: "sky130_fd_sc_hd__a2111o_1 A1 A2 B1 C1 D1 VGND VNB VPB VPWR X"
    std_pin_order_dict[std_cell_info[0]] = std_cell_info[1:]
    # std_cell_info array example ['sky130_fd_sc_hd__a2111o_1', 'A1', 'A2', 'B1', 'C1', 'D1', 'VGND', 'VNB', 'VPB', 'VPWR', 'X']
    # Example key:val std_pin_order_dict {'sky130_fd_sc_hd__a2111o_1': ['A1', 'A2', 'B1', 'C1', 'D1', 'VGND', 'VNB', 'VPB', 'VPWR', 'X']}

# pin order from the input standard LEF (inputz/merged_spacing.lef). read that entire file into "filedata" i.e. overwrite filedata
with open(args.stdLef, "r") as rf:
    filedata = rf.read()

pin_order_dict = {}  # map object, see notes in the for each loop below
all_std_cells = re.findall(
    "MACRO (.*)", filedata
)  # "MACRO (.*)" means all lines where "MACRO " occurs

# all_std_cells is an array containing the name of the MACROs
for std_cell in all_std_cells:
    # std_cell is a single cell name such as "sky130_ef_sc_hd__fakediode_2"
    std_cell_re = re.search("MACRO " + std_cell + "(.*\n)*END " + std_cell, filedata)
    # std_cell_re is a match object containg the entire cell i.e. from the line cell_name_here to END cell_name_here
    std_cell_info = std_cell_re.group(0)  # group(0) returns the whole match
    # std_cell_info is a string containg the entire cell i.e. from the line cell_name_here to END cell_name_here
    pin_order_list = re.findall("PIN (.*)", std_cell_info)
    # pin_order_list is an array of all pin names such as "['DIODE', 'VGND', 'VPWR', 'VPB', 'VNB']"
    pin_order_dict[std_cell] = pin_order_list[::-1]  # list the pins backwards
    # pin_order_dict is a map containing the pins (listed backwards from order they appear) in each cell
    # an example key:value pair is {'sky130_ef_sc_hd__fakediode_2': ['VNB', 'VPB', 'VPWR', 'VGND', 'DIODE']}

# The input Cdl netlist (inputz/6_final.cdl). read that entire file into "filedata" i.e. overwrite filedata
with open(args.inputCdl, "r") as rf:
    filedata = rf.read()
    filedata = filedata.replace(
        "VIN ", "", 1
    )  # replace VIN with nothing one time (i.e. delete the pin in toplevel)
    filedata = filedata.replace(
        "r_VIN", "", 1
    )  # replace r_VIN with nothing one time (i.e. delete the pin in toplevel)
    filedata = filedata.replace(
        " VIN ", " r_VIN "
    )  # replace all instances of “ VIN “ with “ r_VIN “
    filedata = filedata.replace(
        " VIN", " r_VIN "
    )  # replace all instances of “VIN “ with “ r_VIN “


with open(args.outputCdl, "w") as wf:
    ckt_re = re.search("(\.SUBCKT.*\n(\+.*\n)*)((.*\n)*)(\.ENDS.*)", filedata)
    ckt_head = ckt_re.group(1)
    ckt_cells = ckt_re.group(3)
    ckt_end = ckt_re.group(5)
    ckt_cells = ckt_cells.replace("\n+", "").split("\n")

    wf.write(
        ".INCLUDE '" + os.path.abspath(args.stdCdl) + "'\n"
    )  # .INCLUDE the standard cell spice file
    ckt_head = ckt_head.replace("\n+", "")  # to one line
    wf.write(ckt_head)  # proper top level heading

    for ckt_cell in ckt_cells:
        if not ckt_cell or re.search("FILLER", ckt_cell):
            continue
        ckt_cell_list = ckt_cell.split(" ")
        ordered_cell = [ckt_cell_list[0]]

        pwr_net = ckt_cell_list[1 + pin_order_dict[ckt_cell_list[-1]].index("VPWR")]
        gnd_net = ckt_cell_list[1 + pin_order_dict[ckt_cell_list[-1]].index("VGND")]
        # the loop below does nothing because we overwrite everthing it does (cell list is correct)
        for pin in std_pin_order_dict[ckt_cell_list[-1]]:
            try:
                net_name = ckt_cell_list[
                    1 + pin_order_dict[ckt_cell_list[-1]].index(pin)
                ]
                ordered_cell.append(net_name)
            except:
                if pin == "VNB":
                    ordered_cell.append(gnd_net)
                elif pin == "VPB":
                    ordered_cell.append(pwr_net)
                else:
                    print("cell: " + ckt_cell + " pin: " + pin + " is missing")
                    sys.exit(0)
        ordered_cell.append(ckt_cell_list[-1])
        ordered_cell = ckt_cell_list  # cell list is correct so no process is needed
        wf.write(" ".join(ordered_cell))  # convert tuple into string
        wf.write("\n")
    wf.write(ckt_end)  # the proper toplevel subckt ending
