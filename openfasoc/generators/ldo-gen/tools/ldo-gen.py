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
parser.add_argument(
    "--specfile",
    required=True,
    help="File containing the specification for the generator",
)
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
    choices=["verilog", "macro", "full", "sim"],
    help="LDO Gen operation mode. Default mode: 'verilog'.",
)
parser.add_argument(
    "--arr_size_in", required=False, help="Debug option to manually set power arr size."
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
    # make clean target cleans flow, work, sim dirs
    sp.Popen(["make", "clean"], cwd=directories["genDir"]).wait()
# misc command line error checks
check_args(args)
# user_specs is a hash table containing user defined specs
# designName, vin, imax
valid_spec_ranges = process_supported_inputs(args, directories)
user_specs = get_spec(args.specfile, valid_spec_ranges)
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


outputDir = directories["genDir"] + args.outputDir

shutil.copyfile(
    directories["flowDir"] + "results/" + args.platform + "/ldo/base/6_final.gds",
    outputDir + "/" + user_specs["designName"] + ".gds",
)
shutil.copyfile(
    directories["flowDir"] + "results/" + args.platform + "/ldo/base/6_final.def",
    outputDir + "/" + user_specs["designName"] + ".def",
)
shutil.copyfile(
    directories["flowDir"] + "results/" + args.platform + "/ldo/base/6_final.v",
    outputDir + "/" + user_specs["designName"] + ".v",
)
shutil.copyfile(
    directories["flowDir"] + "results/" + args.platform + "/ldo/base/6_1_fill.sdc",
    outputDir + "/" + user_specs["designName"] + ".sdc",
)
shutil.copyfile(
    directories["objDir"] + "netgen_lvs/spice/" + user_specs["designName"] + ".spice",
    outputDir + "/" + user_specs["designName"] + ".spice",
)
shutil.copyfile(
    directories["objDir"]
    + "netgen_lvs/spice/"
    + user_specs["designName"]
    + "_pex.spice",
    outputDir + "/" + user_specs["designName"] + "_pex.spice",
)
shutil.copyfile(
    directories["flowDir"] + "reports/" + args.platform + "/ldo/base/6_final_drc.rpt",
    outputDir + "/6_final_drc.rpt",
)
shutil.copyfile(
    directories["flowDir"] + "reports/" + args.platform + "/ldo/base/6_final_lvs.rpt",
    outputDir + "/6_final_lvs.rpt",
)
# ------------------------------------------------------------------------------
# run simulations
# ------------------------------------------------------------------------------
if args.mode == "full" or args.mode == "sim":
    print("#----------------------------------------------------------------------")
    print("# Running Simulation")
    print("#----------------------------------------------------------------------")
    specialized_run_dir = configure_simulations(
        directories,
        user_specs["designName"],
        "prePEX",
        arrSize,
        pdk_path,
        user_specs["vin"],
        jsonConfig["simTool"],
    )
    # run max current solve
    max_load = binary_search_current_at_acceptible_error(
        specialized_run_dir, user_specs["vin"]
    )
    print("Max load current = " + str(max_load) + " Amps\n\n")
    # run functional simulation
    sp.Popen(
        ["ngspice", "-b", "-o", "out.txt", "ldoInst_ngspice.sp"],
        cwd=specialized_run_dir,
    ).wait()
    save_sim_plot(specialized_run_dir, directories["genDir"] + "/work/")
