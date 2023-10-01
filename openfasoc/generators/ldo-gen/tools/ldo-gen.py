import argparse
import math
import os
import sys
import subprocess as sp

from configure_workspace import *
from generate_verilog import *
from simulations import *

# TODO: Find a better way to import modules from parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common.verilog_generation import generate_verilog

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
    choices=["verilog", "macro", "full", "sim", "dump", "post"],
    help="LDO Gen operation mode. Default mode: 'verilog'.",
)
parser.add_argument(
    "--arr_size_in", help="Debug option to manually set power arr size."
)
parser.add_argument("--clean", action="store_true", help="Clean the workspace.")
parser.add_argument(
    "--simtype",
    choices=["postPEX", "prePEX"],
    help="Simulations type prePEX or postPEX",
)
parser.add_argument("--pex", help="enable postPEX along with prePEX")
args = parser.parse_args()


print("#---------------------------------------------------------------------")
print("# Configuring Workspace")
print("#---------------------------------------------------------------------")
# directories is a hash table containing all neccessary dirs
# genDir, flowDir, simDir, verilogDir, blocksDir, commonDir, supportedInputs
directories = get_directories()
clean_work_dir = args.mode != "sim" and args.mode != "dump" and args.mode != "post"
if clean_work_dir:
    sp.Popen(["make", "clean"], cwd=directories["genDir"]).wait()
# misc command line error checks
JSON_spec = check_args(args, clean_work_dir)
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
# convert from float to int and round up (to meet spec, at least arrSize PMOS are required)
arrSize = int(math.ceil(arrSize))
print("# LDO - Power Transistor array Size = " + str(arrSize))

# Update the ldo_domain_insts.txt as per power transistor array size
update_ldo_domain_insts(directories["blocksDir"], arrSize)
# Update the ldo_place.txt as per power transistor array size
update_ldo_place_insts(directories["blocksDir"], arrSize)
# Update connections to VREG
update_custom_nets(directories["blocksDir"], arrSize)

# Get the estimate of the area based on power transistor array size
designArea = polynomial_output_at_point_from_coefficients(jsonModel["area"], arrSize)
print("# LDO - Design Area = " + str(designArea) + " um^2")

# Update place density according to power transistor array size
update_area_and_place_density(directories["flowDir"], arrSize)

# Generate the Behavioral Verilog
verilog_gen_dir = os.path.join('flow', 'design', 'src', 'ldo')
ctrlWdRst = get_ctrl_wd_rst(arrSize)

generate_verilog(
    parameters={
        "design_name": user_specs["designName"],
        "arrSize": arrSize,
        "ctrlWdRst": ctrlWdRst
    },
    out_dir=verilog_gen_dir
)

if clean_work_dir:
    print("# LDO - Behavioural Verilog Generated")
    print("#----------------------------------------------------------------------")
    print("# Verilog Generated")
    print("#----------------------------------------------------------------------")


# ------------------------------------------------------------------------------
# if args mode is macro or full then run flow
# ------------------------------------------------------------------------------
if args.mode != "verilog" and clean_work_dir:
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

    # simulations are ran for the following configurations:
    cap_list = ["1p", "5p"]  # additional capacitance at node VREG
    freq_list = [0.1 * 10**6, 1 * 10**6, 10 * 10**6]  # clock frequency

    # prepare sim directories and copy files
    # sim_dir_structure is a dictionary containing the tree file path structure of both prepex/pex directories
    [prePEX_sim_dir, postPEX_sim_dir] = create_sim_dirs(
        arrSize, directories["simDir"], args.mode
    )
    # create sim netlists (return as strings)
    spice_dir = directories["flowDir"] + "/objects/sky130hvl/ldo/base/netgen_lvs/spice/"
    rawPEXPath = spice_dir + user_specs["designName"] + "_pex.spice"
    rawSynthPath = spice_dir + user_specs["designName"] + ".spice"
    [processedPEXnetlist, head] = process_PEX_netlist(
        rawPEXPath, jsonConfig["simTool"], user_specs["designName"]
    )
    processedSynthNetlist = process_prePEX_netlist(rawSynthPath)
    powerArrayNetlist = process_power_array_netlist(rawSynthPath)
    # create list of netlists (wheretocopy, filename, stringdata) then write to their respective locations
    netlists = list()
    netlists.append(tuple((postPEX_sim_dir, "ldo_sim.spice", processedPEXnetlist)))
    netlists.append(tuple((prePEX_sim_dir, "ldo_sim.spice", processedSynthNetlist)))
    netlists.append(tuple((prePEX_sim_dir, "power_array.spice", powerArrayNetlist)))
    netlists.append(tuple((postPEX_sim_dir, "power_array.spice", powerArrayNetlist)))
    for netlist in netlists:
        with open(netlist[0] + "/" + netlist[1], "w") as simfile:
            simfile.write(netlist[2])

    # prepare simulation scripts, passing prePEX_sim_dir and pex=false to function *_prepare_scripts() runs preprex sims
    # there should be one output file name specified for each cap value. outputs sent to sim_dir_structure directories
    if args.simtype == "postPEX" or args.pex == "True":
        if jsonConfig["simTool"] == "ngspice":
            [sim, output_file_names] = ngspice_prepare_scripts(
                head,
                cap_list,
                directories["simDir"] + "/templates/",
                postPEX_sim_dir,
                user_specs,
                arrSize,
                pdk_path,
                freq_list,
                "tt",
                pex=True,
            )
        elif jsonConfig["simTool"] == "Xyce":
            [sim, output_file_names] = xyce_prepare_scripts(
                head,
                cap_list,
                directories["simDir"] + "/templates/",
                postPEX_sim_dir,
                user_specs,
                arrSize,
                pdk_path,
                freq_list,
                "tt",
                pex=True,
            )
        else:
            print("simtool not supported")
            exit(1)

    if args.simtype == "prePEX":
        if jsonConfig["simTool"] == "ngspice":
            [sim, output_file_names] = ngspice_prepare_scripts(
                head,
                cap_list,
                directories["simDir"] + "/templates/",
                prePEX_sim_dir,
                user_specs,
                arrSize,
                pdk_path,
                freq_list,
                "tt",
                pex=False,
            )
        elif jsonConfig["simTool"] == "Xyce":
            [sim, output_file_names] = xyce_prepare_scripts(
                head,
                cap_list,
                directories["simDir"] + "/templates/",
                prePEX_sim_dir,
                user_specs,
                arrSize,
                pdk_path,
                freq_list,
                "tt",
                pex=False,
            )
        else:
            print("simtool not supported")
            exit(1)

    print("#----------------------------------------------------------------------")
    print("# Spice netlists created successfully")
    print("#----------------------------------------------------------------------")

# ------------------------------------------------------------------------------
# run simulations
# ------------------------------------------------------------------------------
if args.mode == "full" or args.mode == "sim" or args.mode == "post":
    print("#----------------------------------------------------------------------")
    print("# Running Simulations")
    print("#----------------------------------------------------------------------")
    # run sims
    processes = []
    # assert len(output_file_names) == len(cap_list)*len(freq_list)
    if args.mode != "post":
       if args.simtype == "postPEX" or args.pex == "True":
          run_dir = directories["genDir"] + "tools/"
          vref = user_specs["vin"]
          iload = user_specs["imax"]
          odir = os.path.abspath(args.outputDir)
          for s in range (len(sim)):
              p = sp.Popen(sim[s],cwd=postPEX_sim_dir,shell=True)
              processes.append(p)

          for p in processes:
              p.wait()

          p = sp.Popen(["python3","processing.py","--file_path",postPEX_sim_dir,"--vref",str(vref),"--iload",str(iload),"--odir",odir, "--figs", "True", "--simType", "postPEX"],cwd=run_dir)
          p.wait()

       if args.simtype == "prePEX":
          run_dir = directories["genDir"] + "tools/"
          vref = user_specs["vin"]
          iload = user_specs["imax"]
          odir = os.path.abspath(args.outputDir)
          for s in range (len(sim)):
              p = sp.Popen(sim[s],cwd=prePEX_sim_dir,shell=True)
              processes.append(p)

          for p in processes:
              p.wait()

          p = sp.Popen(["python3","processing.py","--file_path",prePEX_sim_dir,"--vref",str(vref),"--iload",str(iload),"--odir",odir, "--figs", "True", "--simType", "prePEX"],cwd=run_dir)
          p.wait()
       """
          for s in range (len(sim)):
              p = sp.Popen(sim[s],cwd=prePEX_sim_dir,shell=True)
              processes.append(p)

          for p in processes:
              p.wait()

          # perform post processing on simulation results and save figures to work dir
          raw_files = [(prePEX_sim_dir + ofile) for ofile in output_file_names]
          raw_to_csv(raw_files,user_specs["vin"],args.outputDir)
          figures = list()
          figure_names = list()
          figure_names.extend(["VREG_output", "VDIF", "VREG_ripple"])
          figures.extend(fig_VREG_results(raw_files, user_specs["vin"]))
          figure_names.append("cmp_out")
          figures.append(fig_comparator_results(raw_files))
          figure_names.append("active_switches")
          figures.append(fig_controller_results(raw_files))
          # save results to png files
          current_freq_results = args.outputDir + "/" + "output_plots"
          try:
             os.mkdir(current_freq_results)
          except OSError as error:
              if args.mode != "post":
                 print(error)
                 exit(1)
          assert len(figures) == len(figure_names)
          for i, figure in enumerate(figures):
              figure.savefig(current_freq_results + "/" + figure_names[i] + ".png")
              fig_dc_results(prePEX_sim_dir + "/isweep.raw").savefig(args.outputDir + "/dc.png")
              max_load = user_specs["imax"]
              load = max_load*1000
              fig_load_change_results(prePEX_sim_dir + "/" + str(load) + "mA_output_load_change.raw",load).savefig(args.outputDir + "/load_change.png")
              """
