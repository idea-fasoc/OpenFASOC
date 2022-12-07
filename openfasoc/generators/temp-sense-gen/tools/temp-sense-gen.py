#!/usr/bin/python3

import json
import os
import re
import shutil
import subprocess as sp
import sys
import time

import TEMP_netlist
from readparamgen import args, check_search_done, designName
from simulation import generate_runs

genDir = os.path.join(os.path.dirname(os.path.relpath(__file__)), "../")
srcDir = genDir + "src/"
flowDir = genDir + "flow/"
designDir = genDir + "designs/src/tempsense/"
simDir = genDir + "simulations/"
commonDir = genDir + "../../common/"
platformDir = genDir + "../../common/platforms/" + args.platform + "/"
objDir = flowDir + "objects/" + args.platform + "/tempsense/"

# ------------------------------------------------------------------------------
# Clean the workspace
# ------------------------------------------------------------------------------
print("#----------------------------------------------------------------------")
print("# Cleaning the workspace...")
print("#----------------------------------------------------------------------")
if args.clean:
    p = sp.Popen(["make", "clean_all"], cwd=genDir)
    p.wait()

p = sp.Popen(["git", "checkout", platformDir + "cdl/sky130_fd_sc_hd.spice"])
p.wait()

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


temp, power, error, ninv, nhead, hist = check_search_done()

print("Error : ", error)
print("Inv : ", ninv)
print("Header : ", nhead)
print("History : ", hist)
print("INV:{0}\nHEADER:{1}\n".format(ninv, nhead))

if args.ninv:
    print("target number of inverters: " + args.ninv)
    ninv = int(args.ninv)

if args.nhead:
    print("target number of headers: " + args.nhead)
    nhead = int(args.nhead)


print("#----------------------------------------------------------------------")
print("# Verilog Generation")
print("#----------------------------------------------------------------------")


if args.platform == "sky130hd":
    aux1 = "sky130_fd_sc_hd__nand2_1"
    aux2 = "sky130_fd_sc_hd__inv_1"
    aux3 = "sky130_fd_sc_hd__buf_1"
    aux4 = "sky130_fd_sc_hd__buf_1"
    aux5 = "HEADER"
    aux6 = "SLC"
elif args.platform == "sky130hs":
    aux1 = "sky130_fd_sc_hs__nand2_1"
    aux2 = "sky130_fd_sc_hs__inv_1"
    aux3 = "sky130_fd_sc_hs__buf_1"
    aux4 = "sky130_fd_sc_hs__buf_1"
    aux5 = "HEADER_hs"
    aux6 = "SLC_hs"

ninv = ninv + 1
TEMP_netlist.gen_temp_netlist(ninv, nhead, aux1, aux2, aux3, aux4, aux5, srcDir)

with open(srcDir + "TEMP_ANALOG_hv.nl.v", "r") as rf:
    filedata = rf.read()
header_list = re.findall("HEADER\s+(\w+)\(", filedata)
with open(genDir + "blocks/sky130hd/tempsenseInst_custom_net.txt", "w") as wf:
    wf.write("r_VIN\n")
    for header_cell in header_list:
        wf.write("temp_analog_1." + header_cell + " VIN\n")

with open(srcDir + "TEMP_ANALOG_lv.nl.v", "r") as rf:
    filedata = rf.read()
lv_list = re.findall("\nsky130_fd_sc\w*\s+(\w+)\s+\(", filedata)
with open(genDir + "blocks/sky130hd/tempsenseInst_domain_insts.txt", "w") as wf:
    for lv_cell in lv_list:
        wf.write("temp_analog_0." + lv_cell + "\n")

with open(srcDir + "tempsenseInst.v", "r") as rf:
    filedata = rf.read()
    filedata = re.sub("module\s*(\w+)\s*\n", "module " + designName + "\n", filedata)
with open(srcDir + "tempsenseInst.v", "w") as wf:
    wf.write(filedata)

with open(flowDir + "design/sky130hd/tempsense/config.mk", "r") as rf:
    filedata = rf.read()
    filedata = re.sub(
        "export DESIGN_NAME\s*=\s*(\w+)", "export DESIGN_NAME = " + designName, filedata
    )
with open(flowDir + "design/sky130hd/tempsense/config.mk", "w") as wf:
    wf.write(filedata)

shutil.copyfile(
    srcDir + "TEMP_ANALOG_lv.nl.v", flowDir + "design/src/tempsense/TEMP_ANALOG_lv.nl.v"
)
shutil.copyfile(
    srcDir + "TEMP_ANALOG_hv.nl.v", flowDir + "design/src/tempsense/TEMP_ANALOG_hv.nl.v"
)
shutil.copyfile(
    srcDir + "TEMP_AUTO_def.v", flowDir + "design/src/tempsense/TEMP_AUTO_def.v"
)
shutil.copyfile(
    srcDir + "tempsenseInst.v", flowDir + "design/src/tempsense/" + designName + ".v"
)
shutil.copyfile(srcDir + "counter.v", flowDir + "design/src/tempsense/counter" + ".v")

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
if p.returncode:
    print("[Error] Place and Route failed. Refer to the log file")
    exit(1)

print("#----------------------------------------------------------------------")
print("# Place and Route finished")
print("#----------------------------------------------------------------------")

p = sp.Popen(["make", "magic_drc"], cwd=flowDir)
p.wait()
if p.returncode:
    print("[Error] DRC failed. Refer to the report")
    exit(1)

print("#----------------------------------------------------------------------")
print("# DRC finished")
print("#----------------------------------------------------------------------")

p = sp.Popen(["make", "netgen_lvs"], cwd=flowDir)
p.wait()
if p.returncode:
    print("[Error] LVS failed. Refer to the report")
    exit(1)

print("#----------------------------------------------------------------------")
print("# LVS finished")
print("#----------------------------------------------------------------------")

if os.path.isdir(args.outputDir):
    # shutil.rmtree(genDir + args.outputDir)
    pass
if not args.outputDir.startswith("/"):
    os.mkdir(genDir + args.outputDir)
    outputDir = genDir + args.outputDir
else:
    os.mkdir(args.outputDir)
    outputDir = args.outputDir

#  print("genDir + args.outputDir: {}".format(genDir + args.outputDir))
#  print("flowDir: {}".format(flowDir))
#  print("args.platform: {}".format(args.platform))
#  print("designName: {}".format(designName))
#  subprocess.run(["ls", "-l", flowDir, "results/", args.platform, "/tempsense"])

shutil.copyfile(
    flowDir + "results/" + args.platform + "/tempsense/6_final.gds",
    outputDir + "/" + designName + ".gds",
)
shutil.copyfile(
    flowDir + "results/" + args.platform + "/tempsense/6_final.def",
    outputDir + "/" + designName + ".def",
)
shutil.copyfile(
    flowDir + "results/" + args.platform + "/tempsense/6_final.v",
    outputDir + "/" + designName + ".v",
)
shutil.copyfile(
    flowDir + "results/" + args.platform + "/tempsense/6_1_fill.sdc",
    outputDir + "/" + designName + ".sdc",
)
shutil.copyfile(
    objDir + "netgen_lvs/spice/" + designName + ".spice",
    outputDir + "/" + designName + ".spice",
)
shutil.copyfile(
    objDir + "netgen_lvs/spice/" + designName + "_pex.spice",
    outputDir + "/" + designName + "_pex.spice",
)
shutil.copyfile(
    flowDir + "reports/" + args.platform + "/tempsense/6_final_drc.rpt",
    outputDir + "/6_final_drc.rpt",
)
shutil.copyfile(
    flowDir + "reports/" + args.platform + "/tempsense/6_final_lvs.rpt",
    outputDir + "/6_final_lvs.rpt",
)


print("#----------------------------------------------------------------------")
print("# Macro Generated")
print("#----------------------------------------------------------------------")
print()


print("#----------------------------------------------------------------------")
print("# Generating spice netlists for the macro")
print("#----------------------------------------------------------------------")

stage_var = [int(ninv) - 1]
header_var = [int(nhead)]

# make a temp list, TODO: get from JSON config
temp_start = -20
temp_stop = 100
temp_step = 20
temp_points = int((temp_stop - temp_start) / temp_step)
temp_list = []
for i in range(0, temp_points + 1):
    temp_list.append(temp_start + i * temp_step)

# run PEX and/or prePEX simulations based on the command line flags
if args.prepex:
    prepexDir = generate_runs(
        genDir,
        designName,
        header_var,
        stage_var,
        temp_list,
        jsonConfig,
        args.platform,
        args.mode,
        pdk,
        spiceDir=args.outputDir,
        prePEX=True,
    )
    if args.mode == "full":
        if os.path.isfile(prepexDir + "all_result"):
            shutil.copyfile(
                prepexDir + "all_result", genDir + args.outputDir + "/prePEX_sim_result"
            )
        else:
            print(prepexDir + "prePEX all_result file is not generated successfully")
            sys.exit(1)

if args.pex:
    pexDir = generate_runs(
        genDir,
        designName,
        header_var,
        stage_var,
        temp_list,
        jsonConfig,
        args.platform,
        args.mode,
        pdk,
        spiceDir=args.outputDir,
        prePEX=False,
    )

    if args.mode == "full":
        if os.path.isfile(pexDir + "all_result"):
            shutil.copyfile(
                pexDir + "all_result", genDir + args.outputDir + "/PEX_sim_result"
            )
        else:
            print(pexDir + "PEX all_result file is not generated successfully")
            sys.exit(1)


if args.mode == "full":
    print("#----------------------------------------------------------------------")
    print("# Simulation output Generated")
    print("#----------------------------------------------------------------------")


print("Exiting tool....")
exit()
