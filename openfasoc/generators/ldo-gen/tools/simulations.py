import math
import os
import re
import shutil
import sys
import subprocess as sp


def configure_simulation(
    directories,
    designName,
    simType,
    arrSize,
    pdk_path,
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
    os.mkdir(
        specialized_run_dir
    )  # throws if these simulations (i.e. dir) already exist
    # copy spice file and template
    flow_spice_dir = (
        directories["flowDir"] + "/objects/sky130hvl/ldo/base/netgen_lvs/spice/"
    )
    if simType == "prePEX":
        target_spice = designName + ".spice"
    elif simType == "postPEX":
        print("Unsupported simtype.")
        exit(1)
        # target_spice = designName+"_lvsmag.spice"
    else:
        print("Invalid simtype, specify either prePEX or postPEX.")
        exit(1)
    shutil.copyfile(
        flow_spice_dir + target_spice, specialized_run_dir + "/ldo_sim.spice"
    )
    template_sim_spice = "ldoInst_" + simTool + ".sp"
    shutil.copy(
        directories["simDir"] + "/templates/" + template_sim_spice, specialized_run_dir
    )
    # configure sim template
    with open(specialized_run_dir + "/" + template_sim_spice, "r") as sim_spice:
        sim_template = sim_spice.read()
    sim_template = sim_template.replace(
        "@model_file", pdk_path + "/libs.tech/" + simTool + "/sky130.lib.spice"
    )
    sim_template = sim_template.replace("@model_corner", model_corner)
    sim_template = sim_template.replace("@design_nickname", designName)
    with open(specialized_run_dir + "/" + template_sim_spice, "w") as sim_spice:
        sim_spice.write(sim_template)
