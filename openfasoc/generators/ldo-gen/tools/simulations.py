import math
import os
import re
import shutil
import sys
import subprocess as sp
import csv
import matplotlib.pyplot as plt


# ------------------------------------------------------------------------------
# Prepare simulation directory and model spice
# ------------------------------------------------------------------------------


def matchNetlistCell(cell_instantiation, IfFound, remove_mode=True):
    """returns true if the input contains as a pin (as a substring) one of the identified cells to remove for partial simulations"""
    if type(IfFound) is not list:
        raise TypeError(
            'Function matchNetlistCell requires a list "IfFound" of strings to match.'
        )
    # names may not be exactly the same, but as long as part of the name matches then consider true
    # naming will automatically include some portion of the standard cell of origin name in the pin name
    found_status = False
    for name in IfFound:
        for pin in cell_instantiation:
            if name in pin:
                found_status = True
                break
        if found_status:
            break
    # if tested all cells and none are true then found_status=false (set by default)
    # if remove_mode then return true for found else return false for found
    if remove_mode:
        return found_status
    else:
        return not found_status


def partial_remove_from_spice(netlist):
    """Comments out identified cells in matchNetlistCell and adds VREF/VREG to toplevel subckt def."""
    # comment out identified cells
    cells_array = netlist.split("\n")
    for cell in cells_array:
        if cell != "":
            cellPinout = cell.split(" ")
            cell_commented = cell
        if matchNetlistCell(cellPinout, ["vref_gen_nmos_with_trim"]):
            cell_commented = "*" + cell
        netlist = netlist.replace(cell, cell_commented)
    # prepare toplevel subckt def (assumes VDD VSS last two in pin out)
    netlist = netlist.replace("VDD VSS", "VDD VSS VREF VREG", 1)
    return netlist


def complete_remove_from_spice(netlist):
    """Comments out everything except the power array and adjusts inputs to direct control power array."""
    removeIfNotFound = ["Xpt_array_unit", "INCLUDE", "ENDS"]
    cells_array = netlist.split("\n")
    for cell in cells_array:
        if cell != "":
            cellPinout = cell.split(" ")
            cell_commented = cell
        if "SUBCKT" in cell:
            netlist = netlist.replace(cell, ".SUBCKT ldoInst VREG VDD VSS\n")
            continue
        elif matchNetlistCell(cellPinout, removeIfNotFound, False):
            cell_commented = "*" + cell
        elif "ctrl1.ctrl_word" in cell:
            for pin in cellPinout:
                if "ctrl1.ctrl_word" in pin:
                    cell_commented = cell_commented.replace(pin, "VSS")
        netlist = netlist.replace(cell, cell_commented)
    return netlist


def configure_simulations(
    directories,
    designName,
    simType,
    arrSize,
    pdk_path,
    vref,
    simTool="ngspice",
    model_corner="tt",
):
    """Prepare simulation run by configuring sim template."""
    # ensure specialized run directories are present
    try:
        os.mkdir(directories["simDir"] + "/run")
    except OSError as error:
        print("mkdir returned the following error:")
        print(error)
        print("Ignoring this error and continuing.")
    specialized_run_name = simType + "_PT_cells_" + str(arrSize)
    specialized_run_dir = directories["simDir"] + "/run/" + specialized_run_name
    try:
        # throws if these simulations (i.e. dir) already exist
        os.mkdir(specialized_run_dir)
    except OSError as error:
        print(error)
        print(
            "Directory "
            + specialized_run_dir
            + ' already exists.\nRun "make clean_sims" to clear simulation runs.'
        )
        exit(1)
    # copy spice file and template
    flow_spice_dir = (
        directories["flowDir"] + "/objects/sky130hvl/ldo/base/netgen_lvs/spice/"
    )
    if simType == "prePEX":
        target_spice = designName + ".spice"
    elif simType == "postPEX":
        print("Unsupported simtype. postPEX currently not supported.")
        exit(1)
        # target_spice = designName+"_lvsmag.spice"
    else:
        print("Invalid simtype, specify either prePEX or postPEX.")
        exit(1)
    # read spice files and prepare for sims
    with open(flow_spice_dir + target_spice, "r") as spice_in:
        power_spice_out = spice_out = spice_in.read()
    # prepare functional sim spice file
    spice_out = partial_remove_from_spice(spice_out)
    # prepare power array sim spice file
    power_spice_out = complete_remove_from_spice(spice_out)
    # write outputs
    with open(specialized_run_dir + "/ldo_sim.spice", "w") as spice_prep:
        spice_prep.write(spice_out)
    with open(specialized_run_dir + "/power_array.spice", "w") as spice_prep:
        spice_prep.write(power_spice_out)
    # prepare spice control scripts
    template_sim_spice = "ldoInst_" + simTool + ".sp"
    template_pwr_array_spice = "power_array_template_" + simTool + ".sp"
    shutil.copy(
        directories["simDir"] + "/templates/" + template_sim_spice, specialized_run_dir
    )
    shutil.copy(
        directories["simDir"] + "/templates/" + template_pwr_array_spice,
        specialized_run_dir,
    )
    # copy spiceinit into run dir
    if simTool == "ngspice":
        shutil.copy(
            directories["simDir"] + "/templates/.spiceinit", specialized_run_dir
        )
    # configure sim template
    with open(specialized_run_dir + "/" + template_sim_spice, "r") as sim_spice:
        sim_template = sim_spice.read()
    sim_template = sim_template.replace(
        "@model_file", pdk_path + "/libs.tech/" + simTool + "/sky130.lib.spice"
    )
    sim_template = sim_template.replace("@model_corner", model_corner)
    sim_template = sim_template.replace("@design_nickname", designName)
    sim_template = sim_template.replace("@VALUE_REF_VOLTAGE", str(vref))
    with open(specialized_run_dir + "/" + template_sim_spice, "w") as sim_spice:
        sim_spice.write(sim_template)
    # configure power array sim_template
    with open(specialized_run_dir + "/" + template_pwr_array_spice, "r") as sim_spice:
        pwr_sim_template = sim_spice.read()
    pwr_sim_template = pwr_sim_template.replace("@model_corner", model_corner)
    pwr_sim_template = pwr_sim_template.replace("@VALUE_REF_VOLTAGE", str(vref))
    pwr_sim_template = pwr_sim_template.replace(
        "@model_file", pdk_path + "/libs.tech/" + simTool + "/sky130.lib.spice"
    )
    with open(specialized_run_dir + "/" + template_pwr_array_spice, "w") as sim_spice:
        sim_spice.write(pwr_sim_template)
    return specialized_run_dir + "/"


# ------------------------------------------------------------------------------
# Run max current simulations
# ------------------------------------------------------------------------------


def rtr_sim_data(fname):
    """Read Id and VREG from sim output file."""
    with open(fname, "r") as result:
        entire_result = result.readlines()
    rtr_I = None
    rtr_VREG = None
    for line in entire_result:
        if "vreg" in line[0:6]:
            for num in line.split():
                try:
                    rtr_VREG = float(num)
                # Only the last word is a float
                except ValueError:
                    pass
        if "id" in line[0:4]:
            for num in line.split():
                try:
                    rtr_I = float(num)
                # Only the last word is a float
                except ValueError:
                    pass
        if rtr_I is not None and rtr_VREG is not None:
            break
    # final error check
    if rtr_I is None or rtr_VREG is None:
        raise ValueError(
            "Function rtr_sim_data did not find VREG and/or id in sim output file."
        )
    return rtr_VREG, rtr_I


def run_power_array_sim(specialized_run_dir, output_resistance, simTool="ngspice"):
    """Specializes sim template and solves for power array value."""
    if simTool != "ngspice":
        print(
            "\nFunction run_power_array_sim only support sim tool ngspice.\nExiting now.\n"
        )
        exit(1)
    with open(
        specialized_run_dir + "power_array_template_" + simTool + ".sp", "r"
    ) as pwr_array_sim_template:
        specialized_pwr_array_sim = pwr_array_sim_template.read()
    specialized_pwr_array_sim = specialized_pwr_array_sim.replace(
        "@OUTPUT_RESISTANCE", str(output_resistance)
    )
    with open(specialized_run_dir + "power_array.sp", "w") as pwr_array_sim:
        pwr_array_sim.write(specialized_pwr_array_sim)
    with open(specialized_run_dir + "discard_banner.txt", "w") as discard_banner:
        sp.Popen(
            ["ngspice", "-b", "-o", "load_result.txt", "power_array.sp"],
            cwd=specialized_run_dir,
            stdout=discard_banner,
        ).wait()
    return rtr_sim_data(specialized_run_dir + "load_result.txt")


# 												  -> stop solving <-
# R=very small----{R is s.t. VREG=VREF-2*max_error}----------------{R is s.t. VREG=VREF-max_error}---{R is s.t. VREG=VREF}----R=very big
def binary_search_current_at_acceptible_error(specialized_run_dir, VREF):
    """Starts with estimated output resistance range 1-4000 Ohms,
    then performs binary search to find the max load current supported
    with VREG maintained within max_error bounds.
    Smaller max_error results in increase in run time,
    you can configure this within the function
    This functions return a float (result)"""
    max_error = 0.0001  # Volts
    range_min = float(1)
    range_max = float(100000)
    # TODO: add min and max range checking
    target_min = VREF - 2 * max_error
    target_max = VREF - max_error
    # check that max and min are actually bounds to our range
    # loop and divide search space by 2 on each iteration
    # perform no more than 1000 iterations
    for i in range(1, 1000):
        r_mid_value = (range_max + range_min) / 2
        print("Run load simulation, Rout = " + str(r_mid_value) + " Ohms.")
        VREG_result, i_load_result = run_power_array_sim(
            specialized_run_dir, r_mid_value
        )
        if target_min < VREG_result and target_max > VREG_result:
            return i_load_result
        elif VREG_result > target_max:
            range_max = r_mid_value
        elif VREG_result < target_min:
            range_min = r_mid_value
        else:
            raise RuntimeError(
                "function binary_search_current_at_acceptible_error failed to compare next step on the "
                + str(i)
                + " iteration."
            )
    # if the for loop is finished, then a solution has not been reached
    raise RuntimeError(
        "function binary_search_current_at_acceptible_error failed to solve in 1000 iterations."
    )


# ------------------------------------------------------------------------------
# Process simulation results
# ------------------------------------------------------------------------------


def plot_copy_csv(specialized_run_dir, workDir, VREF):
    """Copies a csv called VREG_I.csv from specialized_run_dir to work and plots associated data."""
    # perform file copy
    shutil.copy(specialized_run_dir + "VREG_I.csv", workDir)
    # read csv
    VREG_I = specialized_run_dir + "VREG_I.csv"
    with open(VREG_I) as sim_data:
        sim_data_lines = csv.reader(sim_data, delimiter=" ")
        R1_value = 3600
        time = []
        VREF_value = []
        VREG_value = []
        output_current = []
        for row in sim_data_lines:
            # print(row)
            try:
                timeval = float(row[1])
                VREG_val_current = float(row[3])
                VREF_value.append(float(VREF))
            except Exception as e:
                break
            time.append(timeval)
            # handle VREG calculations
            VREG_value.append(VREG_val_current)
            output_current.append(VREG_val_current / R1_value)
    # plt.plot(x, y, color = 'g', linestyle = 'dashed',marker = 'o',label = "Weather Data")
    plt.plot(time, VREF_value, label="VREF")
    plt.plot(time, VREG_value, label="VREG")
    plt.xlabel("time (s)")
    plt.ylabel("Voltage (V)")
    plt.title("DLDO Transient Simulation", fontsize=20)
    plt.grid()
    plt.legend()
    plt.show()
    plt.savefig("VREG_voltage.png")
    # TODO: add current plot
