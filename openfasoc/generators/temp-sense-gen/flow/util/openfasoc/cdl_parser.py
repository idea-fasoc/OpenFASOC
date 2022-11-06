# -*- coding: utf-8 -*-
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

parser = argparse.ArgumentParser(description="formulate input cdl netlist")
parser.add_argument("--inputCdl", "-i", required=True, help="input CDL netlist")
parser.add_argument("--stdCdl", "-s", required=True, help="standard cells CDL netlist")
parser.add_argument("--powerConn", "-p", required=False, help="power connection")
parser.add_argument("--outputCdl", "-o", required=True, help="output CDL netlist")

args = parser.parse_args()

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


# The input Cdl netlist (inputz/6_final.cdl). read that entire file into "filedata" i.e. overwrite filedata
with open(args.inputCdl, "r") as rf:
    filedata = rf.read()
    filedata = filedata.replace(
        "VIN ", "", 1
    )  # replace VIN with nothing one time (i.e. delete the pin in toplevel)

    # If only one connection point for the r_VIN route is specified, then the pin is r_VIN
    # If multiple connection points are specified for VIN, the pins are r_VIN(0), r_VIN(1) etc., and they also appear in the toplevel subckt of inputCdl
    if int(os.environ["VIN_ROUTE_CONNECTION_POINTS"]) == 1:
        filedata = filedata.replace(
            "r_VIN", "", 1
        )  # if there is only one r_VIN connection pin, replace r_VIN with nothing one time (i.e. delete the pin in toplevel)
    elif int(os.environ["VIN_ROUTE_CONNECTION_POINTS"]) > 1:
        for i in range(int(os.environ["VIN_ROUTE_CONNECTION_POINTS"])):
            filedata = filedata.replace(
                "r_VIN({})".format(i), "", 1
            )  # if there are N r_VIN connection pins, replace all pins r_VIN(i) with nothing one time (i.e. delete the pins in toplevel)

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
        ordered_cell = ckt_cell_list  # cell list is correct so no process is needed
        wf.write(" ".join(ordered_cell))  # convert tuple into string
        wf.write("\n")
    wf.write(ckt_end)  # the proper toplevel subckt ending
