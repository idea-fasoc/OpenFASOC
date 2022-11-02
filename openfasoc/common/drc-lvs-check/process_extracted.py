# by Ali B Hammoud : Nov 1, 2022
# Templatized LVS work around for "signal" type connections between two voltage domains
import sys
import re
import argparse

# -----
# Define any generator specific funcs here. See tempsense example below which processes the HEADER cells.
# Call these funcs before calling toplevel_process in if/else block labeled below
# -----


def HEADER_process(netlist):
    """remove proxy pins in the header cell (if they are present) and correct every instance of HEADER, takes and returns a string"""
    # return a match to only the pinout of the header cell definition, only non case sensitive on .subckt
    HEADER_pinout_m = re.search("(?i)\.SUBCKT (?-i:HEADER.*\n(\+.*\n)*)", netlist)
    # convert match object to string
    HEADER_pinout = HEADER_pinout_m.group(0)
    # remove proxy pins
    correct_HEADER_pinout = HEADER_pinout.replace(" sky130_fd_sc_hd__tap_1_0/VPB", "")
    correct_HEADER_pinout = correct_HEADER_pinout.replace(
        " sky130_fd_sc_hd__tap_1_1/VPB", ""
    )
    # swap out for the new HEADER definition
    netlist = netlist.replace(HEADER_pinout, correct_HEADER_pinout)
    # *****NOW: correct the inputs for every instantiation of the HEADER cell*****
    # find the position of the removed pins
    HEADER_pinout = HEADER_pinout.replace("\n+", "").replace(
        "\n", ""
    )  # make the original HEADER pinout one line + del extra /n
    HEADER_pinout_arr = HEADER_pinout.split(" ")
    index_0 = index_1 = -1
    if "sky130_fd_sc_hd__tap_1_0/VPB" in HEADER_pinout_arr:
        index_0 = HEADER_pinout_arr.index(
            "sky130_fd_sc_hd__tap_1_0/VPB"
        )  # first removed pin
    if "sky130_fd_sc_hd__tap_1_1/VPB" in HEADER_pinout_arr:
        index_1 = HEADER_pinout_arr.index(
            "sky130_fd_sc_hd__tap_1_1/VPB"
        )  # first removed pin
    # swap (or dont) index_0 and index_1 so that index_0 > index_1 (remove pins from the end first)
    if index_0 < index_1:
        temp = index_0
        index_0 = index_1
        index_1 = temp
    # find every line that contains the word "HEADER"
    HEADER_instances_m = re.findall(".*HEADER.*", netlist)
    # loop through HEADER instances correcting the inputs
    first_loop = 1
    for HEADER_instance in HEADER_instances_m:
        # skip the first instance of HEADER becuase that is the cell definition
        if first_loop:
            first_loop = 0
            continue
        HEADER_instance_arr = HEADER_instance.split(" ")
        # HEADER instance must have name pin1 pin2 pin3 pin4 pin5 pin6 HEADER
        # delete item at index_0-2 and index_1-2 position in the pin order
        if (
            index_0 + 1
        ):  # check if the index was defined to something (cannot be -1 and -1+1=false)
            HEADER_instance_arr.pop(index_0 - 1)
        if index_1 + 1:
            HEADER_instance_arr.pop(index_1 - 1)
        correct_HEADER_instance = " ".join(HEADER_instance_arr)
        netlist = netlist.replace(HEADER_instance, correct_HEADER_instance)
    return netlist


def toplevel_process(netlist, toplevel_name, generator_name):
    """remove r_VIN and VIN pins in the toplevel cell def (if they are present), takes 2 and returns 1 string"""
    # construct a regular expression to ONLY match the subckt with the inputted name toplevel
    reg_ex = "(?i)\.SUBCKT (?-i:" + toplevel_name  # only non case sensitive on .subckt
    reg_ex = reg_ex + ".*\n(\+.*\n)*)"
    # return a match to the entire toplevel cell definition from .subckt name to .ENDS, non case sensitive
    toplevel_pinout_m = re.search(reg_ex, netlist, re.IGNORECASE)
    # take only the toplevel pinout
    toplevel_pinout = toplevel_pinout_m.group(0)

    # insert new generator pin name here with no extra spaces or chars
    # follow the template below
    if args.generator == "temp-sense-gen":
        rpin_name = "r_VIN"
        pin_name = "VIN"
    elif args.generator == "ldo-gen":
        rpin_name = "r_VREG"
        pin_name = "VREG"

    # remove r_VIN if present
    correct_toplevel_pinout = toplevel_pinout.replace(" " + rpin_name, "")
    # remove VIN if present
    correct_toplevel_pinout = correct_toplevel_pinout.replace(" " + pin_name, "")
    # swap out for the new toplevel pinout
    netlist = netlist.replace(toplevel_pinout, correct_toplevel_pinout)
    return netlist


# *****START READING HERE*****

# arg parse
# add a required input argument for the extracted spice file
parser = argparse.ArgumentParser(
    description="remove the proxy pins from extracted HEADER cell definition"
)
parser.add_argument(
    "--lvsmag",
    "-l",
    required=True,
    help="extracted spice file from GDS (i.e. extract 6_final.gds)",
)
parser.add_argument(
    "--toplevel", "-t", required=False, help="name of toplevel module to look for"
)  # there may not be a toplevel
parser.add_argument(
    "--generator",
    "-g",
    required=False,
    help='name of generator i.e. "temp-sense-gen" for tempsense. If not specified this script does nothing',
)

try:
    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(2)

# process extracted
# only process if name of generator is specified
if args.generator:
    # read the entire extracted spice into "extracted_spice"
    with open(args.lvsmag, "r") as rf:
        extracted_spice = rf.read()

    # generator specific funcs
    if args.generator == "temp-sense-gen":
        # modify "extracted_spice" HEADER cell definition to remove proxy pins
        extracted_spice = HEADER_process(extracted_spice)
    elif args.generator == "ldo-gen":
        print("No gen specific tasks for this ldo.")

    # remove the r_VIN and VIN pins in the toplevel cell after checking if a toplevel name was input
    if args.toplevel:
        # gen specific signal pin must be specified within this func
        extracted_spice = toplevel_process(
            extracted_spice, args.toplevel, args.generator
        )

    with open(args.lvsmag, "w") as wf:
        wf.write(extracted_spice)
else:
    print(
        "\nprocess_extracted.py was called with no specfic task.\nA generator must be specified to use this script.\n"
    )
