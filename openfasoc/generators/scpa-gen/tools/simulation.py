import glob
import os
import re
import shutil

# import TEMP_netlist
import subprocess as sp
import sys
from itertools import product


def generate_runs(
    genDir,
    designName,
    headerList,
    invList,
    tempList,
    jsonConfig,
    platform,
    modeling=False,
) -> None:
    simDir = genDir + "simulations/"
    flowDir = genDir + "flow/"
    platformConfig = jsonConfig["platforms"][platform]
    simTool = jsonConfig["simTool"]
    model_file = jsonConfig["open_pdks"] + "/libs.tech/ngspice/sky130.lib.spice"

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
            srcNetlist = flowDir + designName + ".spice"
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
            w_file.write(wfdata)
            w_file.close()

        run_simulations(
            runDir, designName, tempList, jsonConfig["simTool"], jsonConfig["simMode"]
        )


def update_netlist(srcNetlist, dstNetlist, simMode) -> None:
    with open(srcNetlist, "r") as rf:
        netlist = rf.read()
        netlist = re.sub(
            "(\.INCLUDE.*\n)",
            "\g<1>.SUBCKT tempsenseInst CLK_REF DONE DOUT[0] DOUT[10] DOUT[11]\n+ DOUT[12] DOUT[13] DOUT[14] DOUT[15] DOUT[16] DOUT[17] DOUT[18]\n+ DOUT[19] DOUT[1] DOUT[20] DOUT[21] DOUT[22] DOUT[23] DOUT[2]\n+ DOUT[3] DOUT[4] DOUT[5] DOUT[6] DOUT[7] DOUT[8] DOUT[9] RESET_COUNTERn\n+ SEL_CONV_TIME[0] SEL_CONV_TIME[1] SEL_CONV_TIME[2] SEL_CONV_TIME[3]\n+ VDD VIN VSS en lc_out out outb\n",
            netlist,
        )
        netlist = re.sub("\.end", ".ends", netlist)
        spice_netlist_re = re.search("\.INCLUDE '(.*)'", netlist)
        spice_netlist = spice_netlist_re.group(1)
        if simMode == "partial":
            netlist = re.sub("\n(X(?!temp_analog).*)", "\n*\g<1>", netlist)
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

    with open(spice_netlist, "r") as rf:
        filedata = rf.read()
        filedata = re.sub("\n(R[0-9]+)", "\n*\g<1>", filedata)
        filedata = re.sub("\n\*(V[0-9]+)", "\n\g<1>", filedata)
    with open(spice_netlist, "w") as wf:
        wf.write(filedata)


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
