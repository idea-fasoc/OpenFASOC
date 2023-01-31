import math
import numpy as np
import os
import re
import shutil
import sys
import subprocess as sp
import matplotlib.pyplot as plt
from cairosvg import svg2png
from PIL import Image
from scipy.interpolate import make_interp_spline
import ltspice

# ------------------------------------------------------------------------------
# Create Sim Directories
# ------------------------------------------------------------------------------
def create_sim_dirs(arrSize, simDir, freq_list):
    """Creates and performs error checking on pre/post PEX sim directories"""
    os.makedirs(simDir + "/run", exist_ok=True)
    prePEX_sim_dir = simDir + "run/" + "prePEX_PT_cells_" + str(arrSize)
    postPEX_sim_dir = simDir + "run/" + "postPEX_PT_cells_" + str(arrSize)
    prePEX_sim_dir = os.path.abspath(prePEX_sim_dir)
    postPEX_sim_dir = os.path.abspath(postPEX_sim_dir)
    sim_dir_structure = dict()
    for freq in freq_list:
        sim_dir_structure[str(round(freq)) + "Hz"] = freq
    try:
        os.mkdir(prePEX_sim_dir)
        os.mkdir(postPEX_sim_dir)
        for dir_name in sim_dir_structure:
            os.mkdir(postPEX_sim_dir + "/" + dir_name)
            os.mkdir(prePEX_sim_dir + "/" + dir_name)
    except OSError as error:
        print(error)
        print(
            'Already ran simulations for this design\nRun "make clean_sims" to clear ALL simulation runs OR manually delete run directories.\n'
        )
        exit(1)
    return [prePEX_sim_dir + "/", postPEX_sim_dir + "/", sim_dir_structure]


# ------------------------------------------------------------------------------
# Prepare the complete LDO design PEX and prePEX spice netlists
# ------------------------------------------------------------------------------
def matchNetlistCell(cell_instantiation, IfFound, remove_mode=True):
    """HELPER FUNCTION:
    returns true if the input contains as a pin (as a substring) one
    of the identified cells to remove for partial simulations"""
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


def process_prePEX_netlist(rawSynthNetlistPath):
    """Comments out identified cells in matchNetlistCell and adds VREF/VREG to toplevel subckt def.
    Return string containing the netlist."""
    with open(rawSynthNetlistPath, "r") as spice_in:
        netlist = spice_in.read()
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
    netlist = netlist.replace("VDD VSS", "VDD VSS VREF", 1)
    return netlist


def process_power_array_netlist(rawSynthNetlistPath):
    """Comments out everything except the power array and adjusts inputs to direct control power array.
    Return string containing the netlist."""
    with open(rawSynthNetlistPath, "r") as spice_in:
        power_spice_netlist = spice_in.read()
    removeIfNotFound = ["Xpt_array_unit", "INCLUDE", "ENDS"]
    cells_array = power_spice_netlist.split("\n")
    for cell in cells_array:
        if cell != "":
            cellPinout = cell.split(" ")
            cell_commented = cell
        if "SUBCKT" in cell:
            power_spice_netlist = power_spice_netlist.replace(
                cell, ".SUBCKT ldoInst VREG VDD VSS\n"
            )
            continue
        elif matchNetlistCell(cellPinout, removeIfNotFound, False):
            cell_commented = "*" + cell
        elif "ctrl1.ctrl_word" in cell:
            for pin in cellPinout:
                if "ctrl1.ctrl_word" in pin:
                    cell_commented = cell_commented.replace(pin, "VSS")
        power_spice_netlist = power_spice_netlist.replace(cell, cell_commented)
    return power_spice_netlist


def process_PEX_netlist(rawExtractedNetlistPath):
    """Prepare PEX netlist for simulations. Return string containing the netlist."""
    with open(rawExtractedNetlistPath, "r") as spice_in:
        netlist = spice_in.read()
    cap_num_connected = int(re.findall(r"\bcapacitor_test_nf_\S*", netlist)[0][18])
    vref_node_to = "capacitor_test_nf_" + str(cap_num_connected) + "/pin0"
    netlist = netlist.replace(
        "r_VREG clk cmp_out", "r_VREG " + vref_node_to + " clk cmp_out", 1
    )
    cells_array = netlist.split("\n")
    i = 0
    while i < len(cells_array):
        if (
            cells_array[i].startswith("C")
            and "vref_gen_nmos_with_trim_0" in cells_array[i]
        ):
            cells_array[i] = "*" + cells_array[i]
        elif "Xvref_gen_nmos_with_trim_0" in cells_array[i]:
            cells_array[i] = "*" + cells_array[i]
            i = i + 1
            while cells_array[i][0] == "+":
                cells_array[i] = "*" + cells_array[i]
                i = i + 1
        i = i + 1
    netlist = "\n".join(cells_array)
    return netlist


# ------------------------------------------------------------------------------
# Prepare Simulation Scripts (add function for each new sim tool)
# ------------------------------------------------------------------------------
prePEX_SPICE_HEADER_GLOBAL_V = """clk cmp_out ctrl_out[0] ctrl_out[1] ctrl_out[2] ctrl_out[3]
+ ctrl_out[4] ctrl_out[5] ctrl_out[6] ctrl_out[7] ctrl_out[8] mode_sel[0] mode_sel[1]
+ reset std_ctrl_in std_pt_in_cnt[0] std_pt_in_cnt[1] std_pt_in_cnt[2] std_pt_in_cnt[3]
+ std_pt_in_cnt[4] std_pt_in_cnt[5] std_pt_in_cnt[6] std_pt_in_cnt[7] std_pt_in_cnt[8]
+ trim1 trim10 trim2 trim3 trim4 trim5 trim6 trim7 trim8 trim9 VDD VSS VREF VREG"""
postPEX_SPICE_HEADER_GLOBAL_V = """VREG VREF clk cmp_out ctrl_out[0] ctrl_out[1] ctrl_out[2] ctrl_out[3]
+ ctrl_out[4] ctrl_out[5] ctrl_out[6] ctrl_out[7] ctrl_out[8] mode_sel[0] mode_sel[1]
+ reset std_ctrl_in std_pt_in_cnt[0] std_pt_in_cnt[1] std_pt_in_cnt[2] std_pt_in_cnt[3]
+ std_pt_in_cnt[4] std_pt_in_cnt[5] std_pt_in_cnt[6] std_pt_in_cnt[7] std_pt_in_cnt[8]
+ trim1 trim10 trim2 trim3 trim4 trim5 trim6 trim7 trim8 trim9 VSS VDD"""


def ngspice_prepare_scripts(
    cap_list,
    templateScriptDir,
    sim_dir,
    sim_dir_structure,
    user_specs,
    arrSize,
    pdk_path,
    model_corner,
    pex=True,
):
    """Specializes ngspice simulations and returns (string) bash to run all sims."""
    designName = user_specs["designName"]
    vref = user_specs["vin"]
    max_load = user_specs["imax"]
    model_file = pdk_path + "/libs.tech/ngspice/sky130.lib.spice"
    with open(templateScriptDir + "ldoInst_ngspice.sp", "r") as sim_spice:
        sim_template = sim_spice.read()
    sim_template = sim_template.replace("@model_file", model_file)
    sim_template = sim_template.replace("@model_corner", model_corner)
    sim_template = sim_template.replace("@design_nickname", designName)
    sim_template = sim_template.replace("@VALUE_REF_VOLTAGE", str(vref))
    sim_template = sim_template.replace("@Res_Value", str(1.2 * vref / max_load))
    if pex:
        sim_template = sim_template.replace(
            "@proper_pin_ordering", postPEX_SPICE_HEADER_GLOBAL_V
        )
    else:
        sim_template = sim_template.replace(
            "@proper_pin_ordering", prePEX_SPICE_HEADER_GLOBAL_V
        )
    # create list of scripts to run (wheretocopy, filename, stringdata, ngspicecommand)
    scripts_to_run = list()
    for freq_dir in sim_dir_structure:
        freq = sim_dir_structure[freq_dir]
        sim_script = sim_template
        sim_script = sim_script.replace("@clk_period", str(1 / freq))
        sim_script = sim_script.replace("@duty_cycle", str(0.5 / freq))
        sim_time = 1.2 * arrSize / freq
        sim_script = sim_script.replace("@sim_time", str(sim_time))
        sim_script = sim_script.replace("@sim_step", str(sim_time / 2000))
        for cap in cap_list:
            sim_script_f = sim_script.replace("@Cap_Value", str(cap))
            output_raw = str(cap) + "_cap_output.raw"
            sim_script_f = sim_script_f.replace("@output_raw", str(output_raw))
            sim_name = "ldoInst_" + str(cap) + ".sp"
            scripts_to_run.append(
                tuple(
                    (
                        sim_dir + freq_dir,
                        sim_name,
                        sim_script_f,
                        "ngspice -b -o " + str(cap) + "_out.txt -i " + sim_name,
                    )
                )
            )
    # add power array script to the list
    with open(templateScriptDir + "/pwrarr_sweep_ngspice.sp", "r") as sim_spice:
        pwr_sim_template = sim_spice.read()
    pwr_sim_template = pwr_sim_template.replace("@model_corner", model_corner)
    pwr_sim_template = pwr_sim_template.replace("@VALUE_REF_VOLTAGE", str(vref))
    pwr_sim_template = pwr_sim_template.replace("@model_file", model_file)
    scripts_to_run.append(
        tuple(
            (
                sim_dir,
                "pwrarr.sp",
                pwr_sim_template,
                "ngspice -b -o pwrout.txt -i pwrarr.sp",
            )
        )
    )
    # write scripts to their respective locations and create simulation bash script
    run_scripts_bash = "#!/usr/bin/env bash\n"
    for script in scripts_to_run:
        with open(script[0] + "/" + script[1], "w") as scriptfile:
            scriptfile.write(script[2])
        run_scripts_bash += (
            "cp "
            + os.path.abspath(templateScriptDir)
            + "/.spiceinit "
            + os.path.abspath(script[0])
            + "\n"
        )
        run_scripts_bash += "cd " + os.path.abspath(script[0]) + "\n"
        run_scripts_bash += script[3] + "\n"
    return [run_scripts_bash, [(str(cap) + "_cap_output.raw") for cap in cap_list]]


# ------------------------------------------------------------------------------
# max current binary search (deprecated, instead use dc linear sweep)
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
        raise ValueError("rtr_sim_data did not find VREG or id in sim output.")
    return rtr_VREG, rtr_I


def run_power_array_sim(run_dir, output_resistance, simTool="ngspice"):
    """Specializes sim template and solves for power array value."""
    if simTool != "ngspice":
        print("run_power_array_sim only supports ngspice. Exiting now.")
        exit(1)
    with open(
        run_dir + "power_array_template_" + simTool + ".sp", "r"
    ) as pwr_array_sim_template:
        specialized_pwr_array_sim = pwr_array_sim_template.read()
    specialized_pwr_array_sim = specialized_pwr_array_sim.replace(
        "@OUTPUT_RESISTANCE", str(output_resistance)
    )
    with open(run_dir + "power_array.sp", "w") as pwr_array_sim:
        pwr_array_sim.write(specialized_pwr_array_sim)
    with open(run_dir + "discard_banner.txt", "w") as discard_banner:
        sp.Popen(
            ["ngspice", "-b", "-o", "load_result.txt", "power_array.sp"],
            cwd=run_dir,
            stdout=discard_banner,
        ).wait()
    return rtr_sim_data(run_dir + "load_result.txt")


# 												  -> stop solving <-
# R=very small----{R is s.t. VREG=VREF-2*max_error}----------------{R is s.t. VREG=VREF-max_error}---{R is s.t. VREG=VREF}----R=very big
def binary_search_max_load(run_dir, VREF):
    """Starts with estimated output resistance range 1-100000 Ohms,
    then performs binary search to find the max load current supported
    with VREG maintained within max_error bounds.
    Smaller max_error results in increase in run time,
    you can configure this within the function
    This functions return a float (result)"""
    max_error = 0.001  # Volts
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
        [VREG_result, i_load_result] = run_power_array_sim(run_dir, r_mid_value)
        if target_min < VREG_result and target_max > VREG_result:
            return i_load_result
        elif VREG_result > target_max:
            range_max = r_mid_value
        elif VREG_result < target_min:
            range_min = r_mid_value
        else:
            raise RuntimeError(
                "function binary_search_max_load failed to compare next step on the "
                + str(i)
                + " iteration."
            )
    # if the for loop is finished, then a solution has not been reached
    raise RuntimeError(
        "function binary_search_max_load failed to solve in 1000 iterations."
    )


# ------------------------------------------------------------------------------
# Process simulation results
# ------------------------------------------------------------------------------
def save_sim_plot(run_dir, workDir):
    """Copy svg sim outputs and convert into PNG."""
    svg2png(
        url=run_dir + "currentplot.svg",
        write_to=workDir + "currentplot.png",
    )
    svg2png(url=run_dir + "vregplot.svg", write_to=workDir + "vregplot.png")


def fig_VREG_results(raw_files, freq_id):
    """Create VREG output plots for all caps at particular freq simulations"""
    figureVREG, axesVREG = plt.subplots(len(raw_files), sharex=True, sharey=True)
    figureVDIF, axesVDIF = plt.subplots(len(raw_files), sharex=True, sharey=True)
    figureRIPL, axesRIPL = plt.subplots(len(raw_files), sharex=True, sharey=True)
    figureOSCL, axesOSCL = plt.subplots(len(raw_files), sharex=True, sharey=True)
    len(axesVREG)  # checks that axes can be indexed
    figureVREG.text(0.5, 0.04, "Time [us]", ha="center")
    figureVREG.text(0.04, 0.5, "Vreg and Vref [V]", va="center", rotation="vertical")
    figureVDIF.text(0.5, 0.04, "Time [us]", ha="center")
    figureVDIF.text(0.04, 0.5, "Vref-Vreg [V]", va="center", rotation="vertical")
    figureRIPL.text(0.5, 0.04, "Time [us]", ha="center")
    figureRIPL.text(0.04, 0.5, "Vref-Vreg [V]", va="center", rotation="vertical")
    figureOSCL.text(0.5, 0.04, "Time [us]", ha="center")
    figureOSCL.text(0.04, 0.5, "VREG_dev_test [V]", va="center", rotation="vertical")
    for i, raw_file in enumerate(raw_files):
        current_cap_sim = str(raw_file).split("/")[-1].split("_")[0] + " "
        data = ltspice.Ltspice(raw_file)
        data.parse()
        time = data.get_time()
        [VREG, VREF] = [data.get_data("v(vreg)"), data.get_data("v(vref)")]
        axesVREG[i].set_title("VREG vs Time " + current_cap_sim + freq_id)
        axesVREG[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
        axesVREG[i].plot(time, VREG, label="VREG")
        axesVREG[i].plot(time, VREF, label="VREF")
        axesVREG[i].legend(loc="lower right")
        axesVDIF[i].set_title("V_difference vs Time " + current_cap_sim + freq_id)
        axesVDIF[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
        axesVDIF[i].plot(time, VREF - VREG, label="VREF-VREG")
        axesVDIF[i].legend(loc="upper right")
        axesRIPL[i].set_title("V_Ripple vs Time " + current_cap_sim + freq_id)
        axesRIPL[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
        axesRIPL[i].plot(time[-10:], VREG[-10:], label="VREF-VREG")
        axesRIPL[i].legend(loc="upper right")
        VREG_sample_dev = VREG[100 + np.where(VREG[100:] >= 1.8)[0][0] :]
        time_sample_dev = time[100 + np.where(VREG[100:] >= 1.8)[0][0] :]
        axesOSCL[i].set_title("VREG Oscillation vs Time " + current_cap_sim + freq_id)
        axesOSCL[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
        axesOSCL[i].plot(time_sample_dev, VREG_sample_dev, label="VREG_dev")
        axesOSCL[i].legend(loc="upper right")
    return [figureVREG, figureVDIF, figureRIPL, figureOSCL]


def fig_comparator_results(raw_files, freq_id):
    """Create cmp_out output plots for all caps at particular freq simulations"""
    figure, axes = plt.subplots(len(raw_files), sharex=True, sharey=True)
    len(axes)  # checks that axes can be indexed
    figure.text(0.5, 0.04, "Time [us]", ha="center")
    figure.text(0.04, 0.5, "Cmp_out [V]", va="center", rotation="vertical")
    for i, raw_file in enumerate(raw_files):
        data = ltspice.Ltspice(raw_file)
        data.parse()
        current_cap_sim = str(raw_file).split("/")[-1].split("_")[0] + " "
        time = data.get_time()
        cmp_out = data.get_data("v(cmp_out)")
        axes[i].set_title("Comp_out vs Time " + current_cap_sim + freq_id)
        axes[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
        axes[i].plot(time, cmp_out, label="cmp_out")
        axes[i].legend(loc="upper left")
    return figure


def fig_controller_results(raw_files, freq_id):
    """Create controller output plots for all caps at particular freq simulations"""
    figure, axes = plt.subplots(len(raw_files), sharex=True, sharey=True)
    len(axes)  # checks that axes can be indexed
    figure.text(0.5, 0.04, "Time [us]", ha="center")
    figure.text(0.04, 0.5, "Cmp_out [V]", va="center", rotation="vertical")
    for i, raw_file in enumerate(raw_files):
        data = ltspice.Ltspice(raw_file)
        data.parse()
        current_cap_sim = str(raw_file).split("/")[-1].split("_")[0] + " "
        time = data.get_time()[100:]
        active_switches = np.copy(data.get_data("v(ctrl_out[0])"))
        for regI in range(1, 9):
            active_switches += (
                data.get_data("v(ctrl_out[" + str(regI) + "])") * 2**regI
            )
        active_switches = (np.rint(active_switches / 3.3)).astype(int)[100:]
        num_smooth_pts = np.linspace(time.min(), time.max(), 1000)
        active_switches = make_interp_spline(time, active_switches)(num_smooth_pts)
        axes[i].set_title("Active Switches vs Time " + current_cap_sim + freq_id)
        axes[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
        axes[i].plot(num_smooth_pts, active_switches, label="active switches")
        axes[i].legend(loc="upper right")
    return figure
