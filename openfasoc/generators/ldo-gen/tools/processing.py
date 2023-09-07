import math
import numpy as np
import os
import re
import shutil
import sys
import subprocess as sp
import matplotlib.pyplot as plt
import argparse
from cairosvg import svg2png
from PIL import Image
from scipy.interpolate import make_interp_spline
import ltspice
import pandas as pd
from configure_workspace import *
from generate_verilog import *
from simulations import *

parser = argparse.ArgumentParser(description="processing simulations")
parser.add_argument("--file_path","-f", help="sim path")
parser.add_argument("--vref","-v", help="vrefspec")
parser.add_argument("--iload","-i", help="iloadspec")
parser.add_argument("--odir","-od", help="output dir")
parser.add_argument("--figs","-fg", help="figures")
parser.add_argument("--simType","-sim", help="simulations Type")

args = parser.parse_args()

output_file_names = []
sim_dir = args.file_path
vrefspec = args.vref
iloadspec = args.iload
odir = args.odir
simtype = args.simType

ext = ('.raw',)
for files in os.scandir(sim_dir):
    if files.path.endswith(ext) and "cap" in files.name:
       output_file_names.append(files.name)


def fig_VREG_results(raw_files, vrefspec):
    """Create VREG output plots for all caps at particular freq simulations"""
    figureVREG, axesVREG = plt.subplots(len(raw_files),figsize=(30, 15))
    figureVDIF, axesVDIF = plt.subplots(len(raw_files),figsize=(30, 15))
    figureRIPL, axesRIPL = plt.subplots(len(raw_files),figsize=(30, 15))
    #len(axesVREG)  # checks that axes can be indexed
    figureVREG.text(0.5, 0.04, "Time [us]", ha="center",fontsize ='large')
    figureVREG.text(0.04, 0.5, "Vreg and Vref [V]", va="center", rotation="vertical",fontsize =15)
    figureVDIF.text(0.5, 0.04, "Time [us]", ha="center",fontsize ='large')
    figureVDIF.text(0.04, 0.5, "Vref-Vreg [V]", va="center", rotation="vertical",fontsize =15)
    figureRIPL.text(0.5, 0.04, "Time [us]", ha="center",fontsize ='large')
    figureRIPL.text(0.04, 0.5, "V_ripple [V]", va="center", rotation="vertical",fontsize =15)
    for i, raw_file in enumerate(raw_files):
        cap_id = str(raw_file).split("/")[-1].split("_")[2] + " "
        freq_id = str(raw_file).split("/")[-1].split("_")[1] + " "
        data = ltspice.Ltspice(raw_file)
        data.parse()
        time = data.get_time()
        [VREG, VREF] = [data.get_data("v(vreg)"), data.get_data("v(vref)")]
        axesVREG[i].set_title("VREG vs Time " + cap_id + freq_id, fontsize=15)
        axesVREG[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
        axesVREG[i].plot(time, VREG)
        axesVREG[i].plot(time, VREF)
        axesVDIF[i].set_title("V_difference vs Time " + cap_id + freq_id,fontsize=15)
        axesVDIF[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
        axesVDIF[i].plot(time, VREF - VREG)
        VREG_sample_dev = VREG[100 + np.where(VREG[100:] >= vrefspec)[0][0] :]
        time_sample_dev = time[100 + np.where(VREG[100:] >= vrefspec)[0][0] :]
        axesRIPL[i].set_title("V_ripple vs Time " + cap_id + freq_id,fontsize=15)
        axesRIPL[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
        axesRIPL[i].plot(time_sample_dev, VREG_sample_dev)
    return [figureVREG, figureVDIF, figureRIPL]


def fig_comparator_results(raw_files):
    """Create cmp_out output plots for all caps at particular freq simulations"""
    figure, axes = plt.subplots(len(raw_files),figsize=(30, 15))
    len(axes)  # checks that axes can be indexed
    figure.text(0.5, 0.04, "Time [us]", ha="center",fontsize ='large')
    figure.text(0.04, 0.5, "Cmp_out [V]", va="center", rotation="vertical",fontsize =15)
    for i, raw_file in enumerate(raw_files):
        data = ltspice.Ltspice(raw_file)
        data.parse()
        cap_id = str(raw_file).split("/")[-1].split("_")[2] + " "
        freq_id = str(raw_file).split("/")[-1].split("_")[1] + " "
        time = data.get_time()
        cmp_out = data.get_data("v(cmp_out)")
        axes[i].set_title("Comp_out vs Time " + cap_id + freq_id,fontsize=15)
        axes[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
        axes[i].plot(time, cmp_out)
    return figure


def fig_controller_results(raw_files):
    """Create controller output plots for all caps at particular freq simulations"""
    figure, axes = plt.subplots(len(raw_files),figsize=(30, 15))
    len(axes)  # checks that axes can be indexed
    figure.text(0.5, 0.04, "Time [us]", ha="center",fontsize ='large')
    figure.text(0.04, 0.5, "Active Switches", va="center", rotation="vertical",fontsize =15)
    for i, raw_file in enumerate(raw_files):
        data = ltspice.Ltspice(raw_file)
        data.parse()
        cap_id = str(raw_file).split("/")[-1].split("_")[2] + " "
        freq_id = str(raw_file).split("/")[-1].split("_")[1] + " "
        time = data.get_time()[100:]
        active_switches = np.copy(data.get_data("v(ctrl_out[0])"))
        for regI in range(1, 9):
            active_switches += (
                data.get_data("v(ctrl_out[" + str(regI) + "])") * 2**regI
            )
        active_switches = (np.rint(active_switches / 3.3)).astype(int)[100:]
        num_smooth_pts = np.linspace(time.min(), time.max(), 250)
        active_switches = make_interp_spline(time, active_switches)(num_smooth_pts)
        axes[i].set_title("Active Switches vs Time " + cap_id + freq_id,fontsize=15)
        axes[i].ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
        axes[i].plot(num_smooth_pts, active_switches)
    return figure


def fig_dc_results(raw_file):
    figure, axes = plt.subplots(1, sharex=True, sharey=True)
    figure.text(0.5, 0.04, "iload [A]", ha="center")
    figure.text(
        0.04,
        0.5,
        "Max VREG (All Active Switches) [V]",
        va="center",
        rotation="vertical",
    )
    data = ltspice.Ltspice(raw_file)
    data.parse()
    current_load = data.get_data("i(r1)")
    VREF = data.get_data("v(vref)")
    VREG = data.get_data("v(vreg)")
    intersect = np.argwhere(np.diff(np.sign(VREG - VREF))).flatten()
    intersect = intersect[0] if isinstance(intersect, (np.ndarray, list)) else intersect
    axes.set_title(
        "Completely Active Array, DC imax="
        + str(round(current_load[intersect] * 1000, 3))
        + "mA"
    )
    axes.ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
    axes.plot(current_load, VREG, label="VREG")
    axes.plot(current_load, VREF, label="VREF")
    plt.plot(current_load[intersect], VREG[intersect], "ro")
    axes.legend(loc="lower left")
    return figure

def fig_load_change_results(raw_file,load):
    figure, axes = plt.subplots(1, sharex=True, sharey=True)
    figure.text(0.5, 0.04, "Time [us]", ha="center")
    figure.text(
        0.04,
        0.5,
        "VREG [V]",
        va="center",
        rotation="vertical",
    )
    data = ltspice.Ltspice(raw_file)
    data.parse()
    VREG = data.get_data("v(vreg)")
    Time = data.get_time()
    axes.set_title("Load change sim from 1mA to "+ str(load)+ "mA")
    axes.ticklabel_format(style="sci", axis="x", scilimits=(-6, -6))
    axes.plot(Time, VREG)
    return figure
def raw_to_csv(raw_files, vrefspec,odir):
    time_settle = []
    vripple = []
    freq = []
    cap = []
    load = []
    csv1 = odir + "/"+simtype+ "/csv_data"
    os.system("mkdir -p "+csv1)
    for i,raw_file in enumerate(raw_files):
        data = ltspice.Ltspice(raw_file)
        data.parse()
        VREG = data.get_data("v(vreg)")
        VREF = data.get_data("v(vref)")
        cmp_out = data.get_data("v(cmp_out)")
        time = data.get_time()
        test_conditions = str(raw_file).split("/")[-1].strip("cap_output.raw") + "p"
        iload = test_conditions[0:5]
        load.append(iload)
        frequency = test_conditions[6:12]
        freq.append(frequency)
        cap_value = test_conditions[13:]
        cap.append(cap_value)
        VREG_sample_dev = VREG[100 + np.where(VREG[100:] >= vrefspec)[0][0] :]
        VREG_min = min(VREG_sample_dev)
        VREG_max = max(VREG_sample_dev)
        vripple.append(VREG_max-VREG_min)
        time_sample_dev = time[100 + np.where(VREG[100:] >= vrefspec)[0][0] :]
        time_settle.append((time_sample_dev[0]))
        df = pd.DataFrame({"Time" : time , "VREG" : VREG,"VREF" :VREF, "cmp_out" : cmp_out})
        df.to_csv(csv1 + "/" + test_conditions +"_.csv",index=False)
    df2 = pd.DataFrame({"Iload":load,"Frequency":freq,"Cap_Value":cap, "VREG_Ripple" : vripple,"Settling Time" : time_settle})
    df2.to_csv(csv1 + "/" + "parameters.csv" , index=False)

raw_files = [(sim_dir + ofile) for ofile in output_file_names]
raw_to_csv(raw_files,float(vrefspec),odir)

if args.figs == "True":
    figures = list()
    figure_names = list()
    figure_names.extend(["VREG_output", "VDIF", "VREG_ripple"])
    figures.extend(fig_VREG_results(raw_files, float(vrefspec)))
    figure_names.append("cmp_out")
    figures.append(fig_comparator_results(raw_files))
    figure_names.append("active_switches")
    figures.append(fig_controller_results(raw_files))
    # save results to png files
    current_freq_results = odir + "/" +simtype+ "/output_plots"
    try:
        os.mkdir(current_freq_results)
    except OSError as error:
        if args.mode != "post":
            print(error)
            exit(1)
    assert len(figures) == len(figure_names)
    for i, figure in enumerate(figures):
        figure.savefig(current_freq_results + "/" + figure_names[i] + ".png")
        fig_dc_results(sim_dir + "/isweep.raw").savefig(odir + "/" +simtype+"/dc.png")
        max_load = float(iloadspec)
        load = max_load*1000
        fig_load_change_results(sim_dir + "/" + str(load) + "mA_output_load_change.raw",load).savefig(odir +"/" +simtype+ "/load_change.png")