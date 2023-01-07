# -*- coding: utf-8 -*-
# NOTE: NOV 19, 2022,
# This script takes the generated CDL file from openroad (which converts verilog to netlist)
# and modifies it so that a spice file is produced which is able to pass LVS
# This makes up for openroad issues in including VREG -> r_VREG short in cdl
# The execution of this script replaces all instances of VREG with r_VREG
# and removes both VREG and r_VREG from top level subckt pins

import argparse
import os
import re
import sys

parser = argparse.ArgumentParser(description="formulate input cdl netlist")
parser.add_argument("--inputCdl", "-i", required=True, help="input CDL netlist")
parser.add_argument("--powerConn", "-p", required=False, help="power connection")
parser.add_argument("--stdCdl", "-s", required=True, help="standard cells CDL netlist")
parser.add_argument("--outputCdl", "-o", required=True, help="output CDL netlist")

args = parser.parse_args()

# The input Cdl netlist (inputz/6_final.cdl). read that entire file into "filedata" i.e. overwrite filedata
with open(args.inputCdl, "r") as rf:
    filedata = rf.read()
    filedata = filedata.replace(" VREG", "", 1)
    filedata = filedata.replace(" r_VREG", "", 1)
    filedata = filedata.replace(" r_VREG", " VREG")


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
