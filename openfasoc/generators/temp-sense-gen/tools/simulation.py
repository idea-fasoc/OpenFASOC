import glob
import os
import re, math
import shutil
import subprocess as sp
import sys
from itertools import product

# TODO: Find a better way to import modules from parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common.simulation import run_simulations

# note netlist type is either prePEX or postPEX
# function returns the location of simulations
def generate_runs(
    genDir: str,
    designName: str,
    headerList: list[int],
    invList: list[int],
    tempStart: int,
    tempStop: int,
    tempStep: int,
    jsonConfig: dict,
    platform: str,
    pdk: str,
    spiceDir: str = None,
    prePEX: bool = True,
):
    """creates and executes simulations (through run_simulations call)"""
    simDir = genDir + "simulations/"
    platformConfig = jsonConfig["platforms"][platform]
    simTool = jsonConfig["simTool"]
    model_file = pdk + "/libs.tech/ngspice/sky130.lib.spice"
    # avoid breaking function calls to this function by making a defualt option based on genDir
    if not spiceDir:
        spiceDir = genDir + "/work"

    designList = list(product(headerList, invList))

    if not os.path.isdir(simDir + "run/"):
        os.mkdir(simDir + "run/")

    # Iterate over runs
    for design in designList:
        header = design[0]
        inv = design[1]
        if prePEX:
            runDir = "run/prePEX_inv{:d}_header{:d}/".format(inv, header)
        else:
            runDir = "run/PEX_inv{:d}_header{:d}/".format(inv, header)

        runDirPath = os.path.join(simDir, runDir)

        if os.path.isdir(runDirPath):
            shutil.rmtree(runDirPath, ignore_errors=True)
        os.mkdir(runDirPath)

        if prePEX:
            srcNetlist = spiceDir + "/" + designName + ".spice"
        else:
            srcNetlist = spiceDir + "/" + designName + "_pex.spice"
        dstNetlist = os.path.join(runDirPath, designName + ".spice")

        update_netlist(srcNetlist, dstNetlist, jsonConfig["simMode"])

        run_simulations(
            parameters={
                'temp': {'start': tempStart, 'end': tempStop, 'step': tempStep},
                'model_file': model_file,
                'model_corner': platformConfig['model_corner'],
                'nominal_voltage': platformConfig['nominal_voltage'],
                'design_name': designName
            },
            platform=platform,
            simulation_dir=simDir,
            template_path=os.path.join("templates", f"tempsenseInst_{simTool}.sp"),
            runs_dir=runDir,
            sim_tool=simTool,
            netlist_path=dstNetlist
        )

        return runDirPath


def matchNetlistCell(cell_instantiation):
    """returns true if the input contains as a pin (as a substring) one of the identified cells to remove for partial simulations"""
    removeIfFound = """sky130_fd_sc_hd__o211a_1
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
sky130_fd_sc_hd__tapvpwrvgnd_1
SEL_CONV_TIME"""
    removeIfFound = removeIfFound.split("\n")
    # names may not be exactly the same, but as long as part of the name matches then consider true
    # naming will automatically include some portion of the standard cell of origin name in the pin name
    for name in removeIfFound:
        for pin in cell_instantiation:
            if name in pin:
                return True
    # if tested all cells and none are true then false
    return False


def update_netlist(srcNetlist, dstNetlist, simMode):
    """comments cells if simMode is partial so that the simulation netlist only includes the oscillator"""
    with open(srcNetlist, "r") as src:
        netlist = src.read()
        netlist = re.sub("\.end", ".ends", netlist)
        netlist = re.sub("\.endss", ".ends", netlist)
        # search for the tempsense subckt and return it as a match object divided by cells, head, and end
        tempsense_subckt = re.search(
            "(\.SUBCKT tempsense.*\n(\+.*\n)*)((.*\n)*)(\.ENDS.*)",
            netlist,
            re.IGNORECASE,
        )
        if simMode == "partial":
            # netlist = re.sub("\n(X(?!temp_analog).*)", "\n*\g<1>", netlist)
            # the body of the subcky is in match group 3. merge all multiline cell instances for easy commenting
            tempsense_cells_block = tempsense_subckt.group(3)
            netlist = netlist.replace(
                tempsense_cells_block, tempsense_cells_block.replace("\n+", "")
            )
            tempsense_cells_block = tempsense_cells_block.replace("\n+", "")
            # make an array of the cells and comment out the cells that should be removed for partial simuations
            tempsense_cells_array = tempsense_cells_block.split("\n")
            for cell in tempsense_cells_array:
                if cell != "":
                    cellPinout = cell.split(" ")
                    cell_commented = cell
                    if matchNetlistCell(cellPinout):
                        cell_commented = "*" + cell
                    netlist = netlist.replace(cell, cell_commented)
        elif simMode == "full":
            pass
        else:
            print(
                simMode
                + " is not a valid mode for simulation, only partial and full modes are supported"
            )
            sys.exit(1)
        toplevel_pinout = tempsense_subckt.group(1)
        standardized_pinout = """CLK_REF DONE DOUT[0] DOUT[10] DOUT[11]
+ DOUT[12] DOUT[13] DOUT[14] DOUT[15] DOUT[16] DOUT[17] DOUT[18]
+ DOUT[19] DOUT[1] DOUT[20] DOUT[21] DOUT[22] DOUT[23] DOUT[2]
+ DOUT[3] DOUT[4] DOUT[5] DOUT[6] DOUT[7] DOUT[8] DOUT[9] RESET_COUNTERn
+ SEL_CONV_TIME[0] SEL_CONV_TIME[1] SEL_CONV_TIME[2] SEL_CONV_TIME[3]
+ en lc_out out outb VDD VSS
"""
        netlist = netlist.replace(toplevel_pinout.split(" ", 2)[2], standardized_pinout)
    with open(dstNetlist, "w") as wf:
        wf.write(netlist)