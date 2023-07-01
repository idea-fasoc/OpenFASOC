import sys
import getopt
import math
import subprocess as sp
import fileinput
import re
import shutil
import numpy as np
import argparse
import json
import glob

import operator
import readparamgen
from dcdc_netlist import gen_dcdc_netlist_parameters
import os
import time

# designName is from the json Specfile, args is commandline args, jsonSpec is parsed json Specfile
from readparamgen import designName, args, jsonSpec

# TODO: Find a better way to import modules from parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common.verilog_generation import generate_verilog, COMMON_PLATFORMS_PREFIX_MAP

# paths declaration
genDir = os.path.join(os.path.dirname(os.path.relpath(__file__)), "../")
srcDir = genDir + "src/"
flowDir = genDir + "flow/"
designDir = genDir + "designs/src/dcdc/"
simDir = genDir + "simulations/"
commonDir = genDir + "../../common/"
platformDir = genDir + "../../common/platforms/" + args.platform + "/"

# ------------------------------------------------------------------------------
# Clean the workspace
# ------------------------------------------------------------------------------
print("#----------------------------------------------------------------------")
print("# Cleaning the workspace...")
print("#----------------------------------------------------------------------")
if args.clean:
    p = sp.Popen(["make", "clean_all"], cwd=genDir)
    p.wait()

if args.platform == "sky130hd":
    p = sp.Popen(["git", "checkout", platformDir + "cdl/sky130_fd_sc_hd.spice"])
    p.wait()
elif args.platform == "sky130hs":
    p = sp.Popen(["git", "checkout", platformDir + "cdl/sky130_fd_sc_hs.spice"])
    p.wait()
elif args.platform == "sky130hvl":
    p = sp.Popen(["git", "checkout", platformDir + "cdl/sky130_fd_sc_hvl.spice"])
    p.wait()
elif args.platform == "sky130osu12Ths":
    p = sp.Popen(["git", "checkout", platformDir + "cdl/sky130_osu_sc_12T_hs.spice"])
    p.wait()
elif args.platform == "sky130osu12Tms":
    p = sp.Popen(["git", "checkout", platformDir + "cdl/sky130_osu_sc_12T_ms.spice"])
    p.wait()
elif args.platform == "sky130osu12Tls":
    p = sp.Popen(["git", "checkout", platformDir + "cdl/sky130_osu_sc_12T_ls.spice"])
    p.wait()
elif args.platform == "sky130osu15Ths":
    p = sp.Popen(["git", "checkout", platformDir + "cdl/sky130_osu_sc_15T_hs.spice"])
    p.wait()
elif args.platform == "sky130osu15Tms":
    p = sp.Popen(["git", "checkout", platformDir + "cdl/sky130_osu_sc_15T_ms.spice"])
    p.wait()
elif args.platform == "sky130osu15Tls":
    p = sp.Popen(["git", "checkout", platformDir + "cdl/sky130_osu_sc_15T_ls.spice"])
    p.wait()
elif args.platform == "sky130osu18Ths":
    p = sp.Popen(["git", "checkout", platformDir + "cdl/sky130_osu_sc_18T_hs.spice"])
    p.wait()
elif args.platform == "sky130osu18Tms":
    p = sp.Popen(["git", "checkout", platformDir + "cdl/sky130_osu_sc_18T_ms.spice"])
    p.wait()
elif args.platform == "sky130osu18Tls":
    p = sp.Popen(["git", "checkout", platformDir + "cdl/sky130_osu_sc_18T_ls.spice"])
    p.wait()

# load platform config file

print("Loading platform_config file...")
print()
try:
    with open(genDir + "../../common/platform_config.json") as file:
        jsonConfig = json.load(file)
except ValueError as e:
    print("Error occurred opening or loading json file.")
    print >> sys.stderr, "Exception: %s" % str(e)
    sys.exit(1)

print("PDK_ROOT value: {}".format(os.getenv("PDK_ROOT")))

# environment check/setup
pdk = None
if os.getenv("PDK_ROOT") is not None:
    pdk = os.path.join(os.environ["PDK_ROOT"], "sky130A")
else:
    open_pdks_key = "open_pdks"
    pdk = jsonConfig[open_pdks_key]

if not os.path.isdir(os.path.join(pdk, "libs.ref")):
    print("Cannot find libs.ref folder from open_pdks in " + pdk)
    sys.exit(1)
elif not os.path.isdir(os.path.join(pdk, "libs.tech")):
    print("Cannot find libs.tech folder from open_pdks in " + pdk)
    sys.exit(1)
else:
    sky130A_path = commonDir + "drc-lvs-check/sky130A/"
    if not os.path.isdir(sky130A_path):
        os.mkdir(sky130A_path)
    try:
        sp.Popen(
            [
                "sed -i 's/set PDKPATH \".*/set PDKPATH $env(PDK_ROOT)\/sky130A/' $PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc"
            ],
            shell=True,
        ).wait()
    except:
        pass
    shutil.copy2(os.path.join(pdk, "libs.tech/magic/sky130A.magicrc"), sky130A_path)
    shutil.copy2(os.path.join(pdk, "libs.tech/netgen/sky130A_setup.tcl"), sky130A_path)

print("#----------------------------------------------------------------------")
print("# Verilog Generation")
print("#----------------------------------------------------------------------")
# generate SDC file
Frequency = float(jsonSpec["specifications"]["Clock frequency (kHz)"])

if re.search("sky130", args.platform):  # Update
    period = 1.0e6 / (Frequency * 1000)

clk_tran = period / 20
with open(flowDir + "/design/" + args.platform + "/dcdc/constraint.sdc", "r") as file:
    filedata = file.read()

filedata = re.sub(
    r"create_clock .*",
    r'create_clock [get_ports clk] -name "CLK" -period ' + str(round(period, 2)),
    filedata,
)

with open(flowDir + "/design/" + args.platform + "/dcdc/constraint.sdc", "w") as file:
    file.write(filedata)

# replace designName in flow/design/.../config.mk

with open(flowDir + "design/" + args.platform + "/dcdc/config.mk", "r") as rf:
    filedata = rf.read()
    filedata = re.sub(
        "export DESIGN_NAME\s*=\s*(\w+)", "export DESIGN_NAME = " + designName, filedata
    )
with open(flowDir + "design/" + args.platform + "/dcdc/config.mk", "w") as wf:
    wf.write(filedata)

# generate verilog files
netlist_parameters = gen_dcdc_netlist_parameters(args, jsonSpec, jsonConfig)
verilog_gen_parameters = {
    "design_name": designName,
    "cell_prefix": COMMON_PLATFORMS_PREFIX_MAP[args.platform],
    "cell_suffix": "_1",
    **netlist_parameters
}

generate_verilog(
    parameters=verilog_gen_parameters,
    out_dir=os.path.join('flow', 'design', 'src', 'dcdc')
)

print("#----------------------------------------------------------------------")
print("# Verilog Generated")
print("#----------------------------------------------------------------------")
print()
if args.mode == "verilog":
    print("Exiting tool....")
    exit()

print("#----------------------------------------------------------------------")
print("# Run Synthesis and APR")
print("#----------------------------------------------------------------------")

p = sp.Popen(["make", "finish"], cwd=flowDir)
p.wait()


print("#----------------------------------------------------------------------")
print("# Place and Route finished")
print("#----------------------------------------------------------------------")

time.sleep(2)

p = sp.Popen(["make", "magic_drc"], cwd=flowDir)
p.wait()

print("#----------------------------------------------------------------------")
print("# DRC finished")
print("#----------------------------------------------------------------------")

time.sleep(2)

p = sp.Popen(["make", "netgen_lvs"], cwd=flowDir)
p.wait()


print("#----------------------------------------------------------------------")
print("# LVS finished")
print("#----------------------------------------------------------------------")

if os.path.isdir(args.outputDir):
    shutil.rmtree(genDir + args.outputDir)
os.mkdir(genDir + args.outputDir)

#  print("genDir + args.outputDir: {}".format(genDir + args.outputDir))
#  print("flowDir: {}".format(flowDir))
#  print("args.platform: {}".format(args.platform))
#  print("designName: {}".format(designName))
#  subprocess.run(["ls", "-l", flowDir, "results/", args.platform, "/cryo"])

shutil.copyfile(
    flowDir + "results/" + args.platform + "/dcdc/6_final.gds",
    genDir + args.outputDir + "/" + args.platform + "/" + designName + ".gds",
)
shutil.copyfile(
    flowDir + "results/" + args.platform + "/dcdc/6_final.def",
    genDir + args.outputDir + "/" + args.platform + "/" + designName + ".def",
)
shutil.copyfile(
    flowDir + "results/" + args.platform + "/dcdc/6_final.v",
    genDir + args.outputDir + "/" + args.platform + "/" + designName + ".v",
)
shutil.copyfile(
    flowDir + "results/" + args.platform + "/dcdc/6_1_fill.sdc",
    genDir + args.outputDir + "/" + args.platform + "/" + designName + ".sdc",
)
shutil.copyfile(
    flowDir + designName + ".spice",
    genDir + args.outputDir + "/" + args.platform + "/" + designName + ".spice",
)
shutil.copyfile(
    flowDir + designName + "_pex.spice",
    genDir + args.outputDir + "/" + args.platform + "/" + designName + "_pex.spice",
)
shutil.copyfile(
    flowDir + "reports/" + args.platform + "/dcdc/6_final_drc.rpt",
    genDir + args.outputDir + "/" + args.platform + "/6_final_drc.rpt",
)
shutil.copyfile(
    flowDir + "reports/" + args.platform + "/dcdc/6_final_lvs.rpt",
    genDir + args.outputDir + "/" + args.platform + "/6_final_lvs.rpt",
)


time.sleep(2)

print("#----------------------------------------------------------------------")
print("# Macro Generated")
print("#----------------------------------------------------------------------")
print()
if args.mode == "macro":
    print("Exiting tool....")
    # sys.exit(1)
    exit()

temp_list = []
for i in range(0, temp_points + 1):
    temp_list.append(temp_start + i * temp_step)

generate_runs(
    genDir, designName, header_var, stage_var, temp_list, jsonConfig, args.platform
)

# shutil.copyfile(flowDir + designName + '_pex.spice', runDir + designName + '_pex.spice')
# shutil.copyfile(genDir + "tools/result.py", runDir + "result.py")
# shutil.copyfile(genDir + "tools/result_error.py", runDir + "result_error.py")

runDir = simDir + "run/inv{:d}_header{:d}/".format(stage_var[0], header_var[0])
if os.path.isfile(runDir + "all_result"):
    shutil.copyfile(runDir + "all_result", genDir + args.outputDir + "/sim_result")
else:
    print(runDir + "all_result file is not generated successfully")


# with open(spice_netlist, "r") as rf:
#   filedata = rf.read()
#   filedata = re.sub("(V[0-9]+)", "*\g<1>", filedata)
#   filedata = re.sub("\*(R[0-9]+)", "\g<1>", filedata)
# with open(spice_netlist, "w") as wf:
#   wf.write(filedata)

print("#----------------------------------------------------------------------")
print("# Simulation output Generated")
print("#----------------------------------------------------------------------")
print("Exiting tool....")
exit()
