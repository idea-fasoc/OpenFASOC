import argparse
import os
import re
import sys

parser = argparse.ArgumentParser(description="formulate input cdl netlist")
parser.add_argument("--inputCdl", "-i", required=True, help="input CDL netlist")
parser.add_argument(
    "--stdLef",
    "-l",
    required=True,
    help="input standard LEF, showing pin order used in OpenROAD",
)
parser.add_argument("--stdCdl", "-s", required=True, help="standard cells CDL netlist")
parser.add_argument("--powerConn", "-p", required=False, help="power connection")
parser.add_argument("--outputCdl", "-o", required=True, help="output CDL netlist")

args = parser.parse_args()

# pin order from input stdCdl netlist
with open(args.stdCdl, "r") as rf:
    filedata = rf.read()

std_pin_order_dict = {}
std_cells_re = re.findall("\.subckt (.*)", filedata)
for std_cell in std_cells_re:
    std_cell_info = std_cell.split(" ")
    std_pin_order_dict[std_cell_info[0]] = std_cell_info[1:]

# pin order from inputCdl netlist
with open(args.stdLef, "r") as rf:
    filedata = rf.read()

pin_order_dict = {}
all_std_cells = re.findall("MACRO (.*)", filedata)
for std_cell in all_std_cells:
    std_cell_re = re.search("MACRO " + std_cell + "(.*\n)*END " + std_cell, filedata)
    std_cell_info = std_cell_re.group(0)
    pin_order_list = re.findall("PIN (.*)", std_cell_info)
    pin_order_dict[std_cell] = pin_order_list[::-1]

with open(args.inputCdl, "r") as rf:
    filedata = rf.read()
    filedata = re.sub("r_VIN", "VIN", filedata)

with open(args.outputCdl, "w") as wf:
    ckt_re = re.search("(\.SUBCKT.*\n(\+.*\n)*)((.*\n)*)(\.ENDS.*)", filedata)
    ckt_head = ckt_re.group(1)
    ckt_cells = ckt_re.group(3)
    ckt_end = ckt_re.group(5)
    ckt_cells = ckt_cells.replace("\n+", "").split("\n")

    wf.write(".INCLUDE '" + os.path.abspath(args.stdCdl) + "'\n")
    # wf.write(ckt_head)

    for ckt_cell in ckt_cells:
        if not ckt_cell or re.search("FILLER", ckt_cell):
            continue
        ckt_cell_list = ckt_cell.split(" ")
        ordered_cell = [ckt_cell_list[0]]

        pwr_net = ckt_cell_list[1 + pin_order_dict[ckt_cell_list[-1]].index("VPWR")]
        gnd_net = ckt_cell_list[1 + pin_order_dict[ckt_cell_list[-1]].index("VGND")]
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

        wf.write(" ".join(ordered_cell))
        wf.write("\n")
    wf.write(".end")
