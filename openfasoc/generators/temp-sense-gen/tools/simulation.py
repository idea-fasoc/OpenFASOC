import glob
import os
import re
import shutil
import subprocess as sp
import sys
from itertools import product

import TEMP_netlist

# note netlist type is either prePEX or (anything else) postPEX
def generate_runs(
    genDir,
    designName,
    headerList,
    invList,
    tempList,
    jsonConfig,
    platform,
    modeling=False,
    spiceDir=None,
    netlistType = "prePEX"
):
    """creates and executes simulations (through run_simulations call)"""
    simDir = genDir + "simulations/"
    flowDir = genDir + "flow/"
    platformConfig = jsonConfig["platforms"][platform]
    simTool = jsonConfig["simTool"]
    model_file = jsonConfig["open_pdks"] + "/libs.tech/ngspice/sky130.lib.spice"
    # avoid breaking function calls to this function by making a defualt option based on genDir
    if not spiceDir:
        spiceDir = genDir + "/work"

    platformSpice = glob.glob(
        genDir + "../../common/platforms/%s/cdl/*.spice" % (platform)
    )

    designList = list(product(headerList, invList))

    if not os.path.isdir(simDir + "run/"):
        os.mkdir(simDir + "run/")

    # Update simulation testbench, depending on platform config and if running modeling
    with open(simDir + "templates/tempsenseInst_%s.sp" % (simTool), "r") as rf:
        simTestbench = rf.read()
        simTestbench = re.sub("@model_file", model_file, simTestbench)
        simTestbench = re.sub(
            "@model_corner", platformConfig["model_corner"], simTestbench
        )
        simTestbench = re.sub(
            "@voltage", str(platformConfig["nominal_voltage"]), simTestbench
        )

    if not modeling:
        simTestbench = re.sub("\*@verification", "", simTestbench)
        if jsonConfig["simMode"] == "full":
            simTestbench = re.sub("\*@full", "", simTestbench)
        elif jsonConfig["simMode"] == "partial":
            simTestbench = re.sub("\*@partial", "", simTestbench)
        else:
            print("simulation mode - " + jsonConfig["simMode"] + "is not supported")
            sys.exit(1)
    else:
        simTestbench = re.sub("\*@modeling", "", simTestbench)
        simTestbench = re.sub("\*@partial", "", simTestbench)

    # Iterate over runs
    for design in designList:
        header = design[0]
        inv = design[1]
        runDir = simDir + "run/inv{:d}_header{:d}/".format(inv, header)

        if os.path.isdir(runDir):
            shutil.rmtree(runDir, ignore_errors=True)
        os.mkdir(runDir)

        shutil.copyfile(genDir + "tools/result.py", runDir + "result.py")
        shutil.copyfile(genDir + "tools/result_error.py", runDir + "result_error.py")

        if modeling:
            srcNetlist = genDir + "tools/TEMP_sensor_template.sp"
            dstNetlist = runDir + "TEMP_sensor_inv%d_header%d.spice" % (inv, header)
            simTestbench = re.sub(
                "@netlist",
                os.path.abspath(
                    runDir + "TEMP_sensor_inv%d_header%d.spice" % (inv, header)
                ),
                simTestbench,
            )
            TEMP_netlist.gen_modeling_netlist(srcNetlist, dstNetlist, inv, header)
            with open(dstNetlist, "r") as rf:
                filedata = rf.read()
            for spice in platformSpice:
                filedata = ".INCLUDE '%s'\n" % os.path.abspath(spice) + filedata
            with open(dstNetlist, "w") as wf:
                filedata = wf.write(filedata)
        else:
            if netlistType is "prePEX":
            	srcNetlist = spiceDir + "/" + designName + ".spice"
            else:
            	srcNetlist = spiceDir + "/" + designName + "_pex.spice"
            dstNetlist = runDir + designName + ".spice"
            simTestbench = re.sub(
                "@netlist",
                os.path.abspath(runDir + designName + ".spice"),
                simTestbench,
            )
            update_netlist(srcNetlist, dstNetlist, jsonConfig["simMode"])

        for temp in tempList:
            w_file = open(runDir + "/%s_sim_%d.sp" % (designName, temp), "w")
            wfdata = re.sub("@temp", str(temp), simTestbench)
            wfdata = re.sub("@design_nickname", designName, wfdata)
            w_file.write(wfdata)
            w_file.close()

        run_simulations(
            runDir, designName, tempList, jsonConfig["simTool"], jsonConfig["simMode"]
        )

def matchNetlistCell(cell_to_test):
    """returns true if the cell name contains (as a substring) one of the identified cells to remove for partial simulations"""
    removeCells="""sky130_fd_sc_hd__o211a_1
sky130_fd_sc_hd__o311a_1
sky130_fd_sc_hd__o2111a_2
sky130_fd_sc_hd__a221oi_4
sky130_fd_sc_hd__nor3_2
sky130_fd_sc_hd__nor3_1
sky130_fd_sc_hd__nor2_1
sky130_fd_sc_hd__or3_1
sky130_fd_sc_hd__or3b_2
sky130_fd_sc_hd__or2b_1
sky130_fd_sc_hd__or2_2
sky130_fd_sc_hd__nand3b_1
sky130_fd_sc_hd__mux4_2
sky130_fd_sc_hd__mux4_1
sky130_fd_sc_hd__o221ai_1
sky130_fd_sc_hd__dfrtn_1
sky130_fd_sc_hd__dfrtp_1
sky130_fd_sc_hd__conb_1
sky130_fd_sc_hd__decap_4
sky130_fd_sc_hd__tapvpwrvgnd_1"""
    removeCells=removeCells.split("\n")
    # names may not be exactly the same, but as long as part of the name matches then consider true
    for cell in removeCells:
    	if cell in cell_to_test:
    		return True
    # if tested all cells and none are true then false
    return False

def update_netlist(srcNetlist, dstNetlist, simMode):
    """comments cells if simMode is partial so that the simulation netlist only includes the oscillator"""
    with open(srcNetlist, "r") as src:
        netlist = src.read()
        netlist = re.sub("\.end", ".ends", netlist)
        netlist = re.sub("\.endss", ".ends", netlist)
        if simMode == "partial":
            # netlist = re.sub("\n(X(?!temp_analog).*)", "\n*\g<1>", netlist)
            # search for the tempsense subckt and return it as a match object divided by cells, head, and end
            tempsense_subckt = re.search("(\.SUBCKT tempsense.*\n(\+.*\n)*)((.*\n)*)(\.ENDS.*)", netlist, re.IGNORECASE)
            # the body of the subcky is in match group 3. merge all multiline cell instances for easy commenting
            tempsense_cells_block = tempsense_subckt.group(3)
            netlist = netlist.replace(tempsense_cells_block,tempsense_cells_block.replace("\n+", ""))
            tempsense_cells_block = tempsense_cells_block.replace("\n+", "")
            # make an array of the cells and comment out the cells that should be removed for partial simuations
            tempsense_cells_array = tempsense_cells_block.split("\n")
            for cell in tempsense_cells_array:
            	if cell != '':
            		cellPinout=cell.split(" ")
            		cell_commented=cell
            		if matchNetlistCell(cellPinout[-1]):
            			cell_commented="*"+cell
            		netlist = netlist.replace(cell,cell_commented)
        elif simMode == "full":
            pass
        else:
            print(
                simMode
                + " is not a valid mode for simulation, only partial and full modes are supported"
            )
            sys.exit(1)
    with open(dstNetlist, "w") as wf:
        wf.write(netlist)

def run_simulations(runDir, designName, temp_list, simTool, simMode) -> None:
    if simTool == "finesim":
        with open(runDir + "run_sim", "w") as wf:
            for temp in temp_list:
                wf.write(
                    "finesim -spice %s_sim_%d.sp -o %s_sim_%d &\n"
                    % (designName, temp, designName, temp)
                )

        with open(runDir + "cal_result", "w") as wf:
            for temp in temp_list:
                wf.write(
                    "python result.py --tool finesim --inputFile %s_sim_%d.log\n"
                    % (designName, temp)
                )
            wf.write("python result_error.py --mode %s\n" % (simMode))

        processes = []
        for temp in temp_list:
            p = sp.Popen(
                [
                    "finesim",
                    "-spice",
                    "%s_sim_%d.sp" % (designName, temp),
                    "-o",
                    "%s_sim_%d" % (designName, temp),
                ],
                cwd=runDir,
            )
            processes.append(p)

        for p in processes:
            p.wait()

        for temp in temp_list:
            if not os.path.isfile(runDir + "%s_sim_%d.log" % (designName, temp)):
                print(
                    "simulation output: %s_sim_%d.log is not generated"
                    % (designName, temp)
                )
                sys.exit(1)
            p = sp.Popen(
                [
                    "python",
                    "result.py",
                    "--tool",
                    "finesim",
                    "--inputFile",
                    "%s_sim_%d.log" % (designName, temp),
                ],
                cwd=runDir,
            )
            p.wait()

        p = sp.Popen(["python", "result_error.py", "--mode", simMode], cwd=runDir)
        p.wait()

    elif simTool == "ngspice":
        with open(runDir + "run_sim", "w") as wf:
            for temp in temp_list:
                wf.write(
                    "ngspice -b -o %s_sim_%d.log %s_sim_%d.sp\n"
                    % (designName, temp, designName, temp)
                )

        with open(runDir + "cal_result", "w") as wf:
            for temp in temp_list:
                wf.write(
                    "python result.py --tool ngspice --inputFile %s_sim_%d.log\n"
                    % (designName, temp)
                )
            wf.write("python result_error.py --mode %s\n" % (simMode))

        processes = []
        for temp in temp_list:
            p = sp.Popen(
                [
                    "ngspice",
                    "-b",
                    "-o",
                    "%s_sim_%d.log" % (designName, temp),
                    "%s_sim_%d.sp" % (designName, temp),
                ],
                cwd=runDir,
            )
            processes.append(p)

        for p in processes:
            p.wait()

        for temp in temp_list:
            if not os.path.isfile(runDir + "%s_sim_%d.log" % (designName, temp)):
                print(
                    "simulation output: %s_sim_%d.log is not generated"
                    % (designName, temp)
                )
                sys.exit(1)
            p = sp.Popen(
                [
                    "python",
                    "result.py",
                    "--tool",
                    "ngspice",
                    "--inputFile",
                    "%s_sim_%d.log" % (designName, temp),
                ],
                cwd=runDir,
            )
            p.wait()

        p = sp.Popen(["python", "result_error.py", "--mode", simMode], cwd=runDir)
        p.wait()
