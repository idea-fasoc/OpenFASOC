# by Ali B Hammoud : Nov 1, 2022
# Templatized LVS work around for "signal" type connections between two voltage domains
# __open_generator_name__ must be set for this script to run edits
# To use this script with a new generator, see bottom if/elif block
# Also, refer to this PR: https://github.com/idea-fasoc/OpenFASOC/pull/121
import sys
import re
import argparse


def get_all_instantiations(cell_name, netlist):
    """returns a list of strings of all instantiations of a cell EXACTLY as they appear
    i.e. multiline instances using \"+\" are returned exactly as they appear"""
    cell_instantiations_list = list()
    netlist_lines = netlist.splitlines()
    index = 0
    while index < len(netlist_lines):
        if netlist_lines[index].endswith(cell_name):
            cell_instantiation = netlist_lines[index]
            temp_index = index
            while netlist_lines[temp_index].startswith("+"):
                temp_index = temp_index - 1
                cell_instantiation = (
                    netlist_lines[temp_index] + "\n" + cell_instantiation
                )
            cell_instantiations_list.insert(0, cell_instantiation)
        index = index + 1
    return cell_instantiations_list


def voltage_cell_process(netlist, voltage_cell_name, pins_to_remove):
    """remove proxy pins in the cell which produces the different voltage (if they are present) and correct every instance of such cell, takes and returns a string"""
    # return a match to only the pinout of the voltage cell definition, only non case sensitive on .subckt
    voltage_cell_pinout_m = re.search(
        "(?i)\.SUBCKT (?-i:" + voltage_cell_name + ".*\n(\+.*\n)*)", netlist
    )
    # convert match object to string
    voltage_cell_pinout = voltage_cell_pinout_m.group(0)
    # remove proxy pins
    correct_voltage_cell_pinout = voltage_cell_pinout
    for pin in pins_to_remove:
        correct_voltage_cell_pinout = correct_voltage_cell_pinout.replace(" " + pin, "")
    # swap out for the new voltage cell definition
    netlist = netlist.replace(voltage_cell_pinout, correct_voltage_cell_pinout)
    # *****NOW: correct the inputs for every instantiation of the voltage cell*****
    # find the position of the removed pins
    # make the original voltage cell pinout one line + del extra /n
    voltage_cell_pinout = voltage_cell_pinout.replace("\n+", "").replace("\n", "")
    voltage_cell_pinout_arr = voltage_cell_pinout.split(" ")

    # find the indices in the pinout of pins to remove
    indices = list()
    for pin in pins_to_remove:
        if pin in voltage_cell_pinout_arr:
            indices.append(voltage_cell_pinout_arr.index(pin))
    # sort from biggest to smallest because last pin should be removed first to not invalidate other indices
    indices.sort(reverse=True)
    # get all voltage cell instances and one line them
    # voltage_cell_instances_m = re.findall(".*"+voltage_cell_name+"$", netlist,flags=re.MULTILINE)# edit here
    voltage_cell_instances = get_all_instantiations(voltage_cell_name, netlist)
    for instance in voltage_cell_instances:
        netlist = netlist.replace(
            instance, instance.replace("\n+", "").replace("\n", "")
        )
    # update voltage_cell_instances after we have flattend everything (easier to implement than reference for loop)
    voltage_cell_instances = get_all_instantiations(voltage_cell_name, netlist)
    # loop through voltage cell instances correcting the inputs
    for voltage_cell_instance in voltage_cell_instances:
        voltage_cell_instance_arr = voltage_cell_instance.split(" ")
        # voltage cell instance must have name pin1 pin2 ... pinN voltage_cell_name
        # delete pins at index positions in the pin order
        for pin_position in indices:
            voltage_cell_instance_arr.pop(pin_position - 1)
        correct_voltage_cell_instance = " ".join(voltage_cell_instance_arr)
        netlist = netlist.replace(voltage_cell_instance, correct_voltage_cell_instance)
    return netlist


def toplevel_process(netlist, toplevel_name, rpin_name, pin_name):
    """remove r_VIN and VIN pins in the toplevel cell def (if they are present), takes 2 and returns 1 string"""
    # construct a regular expression to ONLY match the subckt with the inputted name toplevel
    reg_ex = "(?i)\.SUBCKT (?-i:" + toplevel_name  # only non case sensitive on .subckt
    reg_ex = reg_ex + ".*\n(\+.*\n)*)"
    # return a match to the entire toplevel cell definition from .subckt name to .ENDS, non case sensitive
    toplevel_pinout_m = re.search(reg_ex, netlist, re.IGNORECASE)
    # take only the toplevel pinout
    toplevel_pinout = toplevel_pinout_m.group(0)
    # remove rpin_name if present
    if rpin_name:
        correct_toplevel_pinout = toplevel_pinout.replace(" " + rpin_name, "")
    # remove pin_name if present
    if pin_name:
        correct_toplevel_pinout = correct_toplevel_pinout.replace(" " + pin_name, "")
    # swap out for the new toplevel pinout
    netlist = netlist.replace(toplevel_pinout, correct_toplevel_pinout)
    return netlist


# *****START READING HERE*****

# arg parse
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
    # make edits to the if/elif block below to add a new generator
    # insert new generator pin name here and cell pins to remove with no extra spaces or chars
    # follow the template below
    if args.generator == "temp-sense-gen":
        # set the proxy pins to remove from HEADER
        voltage_cell_name = "HEADER"
        pins_to_remove = [
            "sky130_fd_sc_hd__tap_1_0/VPB",
            "sky130_fd_sc_hd__tap_1_1/VPB",
        ]
        # set remove pins for this generator
        rpin_name = "r_VIN"
        pin_name = "VIN"
    elif args.generator == "ldo-gen":
        voltage_cell_name = "LDO_COMPARATOR_LATCH"
        pins_to_remove = ["a_512_1261#"]
        rpin_name = "r_VREG"
        pin_name = "VREG"

    # end edits

    # edit the voltage cells to remove proxy pins
    extracted_spice = voltage_cell_process(
        extracted_spice, voltage_cell_name, pins_to_remove
    )

    # remove the rpin and pin pins in the toplevel cell after checking if a toplevel name was passed to the script
    if args.toplevel:
        extracted_spice = toplevel_process(
            extracted_spice, args.toplevel, rpin_name, pin_name
        )

    with open(args.lvsmag, "w") as wf:
        wf.write(extracted_spice)
else:
    print(
        "\nprocess_extracted_pins.py was called with no specfic task.\nA generator must be specified to use this script.\n"
    )
