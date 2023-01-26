import argparse
import json
import math
import os
import re
import shutil
import sys
import subprocess as sp

from configure_workspace import *
from generate_verilog import *
from simulations import *

print("#---------------------------------------------------------------------")
print("# Parsing command line arguments...")
print("#---------------------------------------------------------------------")
print(sys.argv)
parser = argparse.ArgumentParser(description="Digital LDO design generator")
# If no spec file is provided, try to read the spec command line arguments
# If some/all are missing command line arguments, fill in the blanks by reading specifications.json
parser.add_argument(
    "--specfile",
    help="File containing the specifications for the generator",
)
parser.add_argument("--name", help="Module name if no spec file.")
parser.add_argument("--imax", help="imax if no spec file.")
parser.add_argument("--vref", help="vref if no spec file.")
parser.add_argument(
    "--outputDir", required=True, help="Output directory for generator results"
)
parser.add_argument(
    "--platform", required=True, help="PDK/process kit for cadre flow (.e.g tsmc16)"
)
# note that sim mode is a test option allowing only simulations to be ran
parser.add_argument(
    "--mode",
    default="verilog",
    choices=["verilog", "macro", "full", "sim", "dump"],
    help="LDO Gen operation mode. Default mode: 'verilog'.",
)
parser.add_argument(
    "--arr_size_in", help="Debug option to manually set power arr size."
)
parser.add_argument("--clean", action="store_true", help="Clean the workspace.")
args = parser.parse_args()


print("#---------------------------------------------------------------------")
print("# Configuring Workspace")
print("#---------------------------------------------------------------------")
# directories is a hash table containing all neccessary dirs
# genDir, flowDir, simDir, verilogDir, blocksDir, commonDir, supportedInputs
directories = get_directories()
if args.mode != "sim":
    sp.Popen(["make", "clean"], cwd=directories["genDir"]).wait()
# misc command line error checks
JSON_spec = check_args(args)
# user_specs is a hash table containing user defined specs
# designName, vin, imax
valid_spec_ranges = process_supported_inputs(args, directories)
user_specs = get_spec(args, JSON_spec, valid_spec_ranges)
if args.mode == "dump":
    print("JSON specs dumped to " + str(dump_JSON_specs(user_specs)))
    sys.exit()
# jsonConfig contains simTool, simMode, open_pdks..., and platforms info
jsonConfig = get_config(args.mode, directories["genDir"])
# copies LVS/DRC files to common dir from pdk and performs error checking on pdk path provided
pdk_path = get_setup_pdk(jsonConfig, directories["commonDir"])
# set model file to the one in the repo
model_file = directories["genDir"] + "models/model.json"
jsonModel = check_JSON(model_file)
# print config info
print("Config:")
print('Mode - "' + args.mode + '"')
print('Model File - "' + model_file + '"')
if args.mode != "verilog":
    print('Digital Flow Directory - "' + directories["flowDir"] + '"')
    print('Simulation Tool - "' + jsonConfig["simTool"] + '"')
    print('Simulation Directory - "' + directories["simDir"] + '"')
print('LDO Instance Name - "' + user_specs["designName"] + '"')

if args.mode != "sim":
    print("#----------------------------------------------------------------------")
    print("# Generating Verilog")
    print("#----------------------------------------------------------------------")
# find number of required PT unit cells to meet spec (based on model file)
if args.arr_size_in is None:
    arrSize = polynomial_output_at_point_from_coefficients(
        jsonModel["Iload,max"][str(user_specs["vin"])], 1.3 * user_specs["imax"]
    )
else:
    arrSize = int(args.arr_size_in)
# convert from float to int and round up (to meet spec, at least arrSize PT cells are required)
arrSize = int(math.ceil(arrSize))
print("# LDO - Power Transistor array Size = " + str(arrSize))

# Update the ldo_domain_insts.txt as per power transistor array size
update_ldo_domain_insts(directories["blocksDir"], arrSize)
# Update connections to VREG
update_custom_nets(directories["blocksDir"], arrSize)

# Get the estimate of the area based on power transistor array size
designArea = polynomial_output_at_point_from_coefficients(jsonModel["area"], arrSize)
print("# LDO - Design Area Estimate = " + str(designArea))

# Update place density according to power transistor array size
update_area_and_place_density(directories["flowDir"], arrSize)

# Generate the Behavioral Verilog
generate_LDO_verilog(directories, args.outputDir, user_specs["designName"], arrSize)
generate_controller_verilog(directories, args.outputDir, arrSize)
if args.mode != "sim":
    print("# LDO - Behavioural Verilog Generated")
    print("#----------------------------------------------------------------------")
    print("# Verilog Generated")
    print("#----------------------------------------------------------------------")


# ------------------------------------------------------------------------------
# if args mode is macro or full then run flow
# ------------------------------------------------------------------------------
if args.mode != "verilog" and args.mode != "sim":
    print("#----------------------------------------------------------------------")
    print("# Run Synthesis and APR")
    print("#----------------------------------------------------------------------")
    p = sp.Popen(["make", "finish"], cwd=directories["flowDir"])
    p.wait()
    if p.returncode:
        print("[Error] Place and Route failed. Refer to the log file")
        exit(1)

    print("#----------------------------------------------------------------------")
    print("# Run DRC")
    print("#----------------------------------------------------------------------")
    # TODO: look at drc after this PR
    p = sp.Popen(["make", "magic_drc"], cwd=directories["flowDir"])
    p.wait()
    # if p.returncode:
    # 	print("[Error] DRC failed. Refer to the report")
    # 	exit(1)

    print("#----------------------------------------------------------------------")
    print("# Run LVS")
    print("#----------------------------------------------------------------------")
    p = sp.Popen(["make", "netgen_lvs"], cwd=directories["flowDir"])
    p.wait()
    if p.returncode:
        print("[Error] LVS failed. Refer to the report")
        exit(1)

    print("#----------------------------------------------------------------------")
    print("# LVS and DRC finished successfully")
    print("#----------------------------------------------------------------------")
    # function defined in configure_workspace.py
    copy_outputs(directories, args.outputDir, args.platform, user_specs["designName"])


# ------------------------------------------------------------------------------
# run simulations
# ------------------------------------------------------------------------------
if args.mode == "full" or args.mode == "sim":
    print("#----------------------------------------------------------------------")
    print("# Running Simulation")
    print("#----------------------------------------------------------------------")
    # prepare sim directories and copy files
    [prePEX_specialized_run_dir, postPEX_specialized_run_dir] = create_sim_dirs(
        arrSize, directories["simDir"]
    )

    filestocopy = list()  # list of tuples (wheretocopy, filename, stringdata)
    # create sim netlists (return as strings)
    rawNetlistDir = (
        directories["flowDir"] + "/objects/sky130hvl/ldo/base/netgen_lvs/spice/"
    )
    processedPEXnetlist = prepare_post_pex_netlist(
        rawNetlistDir + user_specs["designName"] + "_pex.spice"
    )
    processedSynthNetlist = prepare_pre_pex_netlist(
        rawNetlistDir + user_specs["designName"] + ".spice"
    )
    powerArrayNetlist = prepare_power_array_netlist(
        rawNetlistDir + user_specs["designName"] + ".spice"
    )
    filestocopy.append(
        tuple((postPEX_specialized_run_dir, "ldo_sim.spice", processedPEXnetlist))
    )
    filestocopy.append(
        tuple((prePEX_specialized_run_dir, "ldo_sim.spice", processedSynthNetlist))
    )
    filestocopy.append(
        tuple((prePEX_specialized_run_dir, "power_array.spice", powerArrayNetlist))
    )

    shutil.copy(
        directories["simDir"] + "/templates/.spiceinit", prePEX_specialized_run_dir
    )
    shutil.copy(
        directories["simDir"] + "/templates/.spiceinit", postPEX_specialized_run_dir
    )

    # write all the files to their respective locations
    for filetocopy in filestocopy:
        with open(filetocopy[0] + "/" + filetocopy[1], "w") as simfile:
            simfile.write(filetocopy[2])

    # prepare simulation scripts and run simulations (return as strings)
    if jsonConfig["simTool"] == "ngspice":
        [prePEXscript, PEXscript, PWRARRscript] = prepare_scripts_and_run_ngspice(
            directories["simDir"] + "/templates/",
            prePEX_specialized_run_dir,
            postPEX_specialized_run_dir,
            pdk_path,
            arrSize,
            "tt",
            user_specs["designName"],
            user_specs["vin"],
            prePEX=False,
        )
    # elif jsonConfig["simTool"] == "Xyce":
    else:
        print("simtool not supported")
        exit(1)

    # run max current solve
    max_load = binary_search_current_at_acceptible_error(
        prePEX_specialized_run_dir, user_specs["vin"]
    )
    print("Max load current = " + str(max_load) + " Amps\n\n")

    # save_sim_plot(postPEX_specialized_run_dir, directories["genDir"] + "/work/")
    freq_list = ["0.1MHz", "1MHz", "10MHz"]
    for f in range(len(freq_list)):
        shutil.copy(
            directories["simDir"] + "/templates/post_processing.py",
            postPEX_specialized_run_dir + freq_list[f] + "/",
        )
        sp.Popen(
            ["python3", "post_processing.py"],
            cwd=postPEX_specialized_run_dir + freq_list[f] + "/",
        ).wait()
