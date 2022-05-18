#!/usr/bin/env python3

# ------------------------------------------------------------------------------
# Switched-Cap DC-DC generator
# ------------------------------------------------------------------------------
import sys
import getopt
import math
import subprocess as sp
import fileinput
import re
import os
import shutil
import numpy as np
import argparse
import json
import glob

# ------------------------------------------------------------------------------
# Get the folder/file paths
# ------------------------------------------------------------------------------
genDir = os.path.join(os.path.dirname(os.path.relpath(__file__)), "../")
head_tail_0 = os.path.split(os.path.abspath(genDir))
head_tail_1 = os.path.split(head_tail_0[0])
pvtGenDir = os.path.relpath(
    os.path.join(genDir, "../../", "private", head_tail_1[1], head_tail_0[1])
)
flowDir = os.path.join(pvtGenDir, "./flow")
extDir = os.path.join(pvtGenDir, "./extraction")
simDir = os.path.join(pvtGenDir, "./simulation")
pyModulesDir = os.path.join(pvtGenDir, "./pymodules")
verilogDir = os.path.join(genDir, "./verilog")

# ------------------------------------------------------------------------------
# Parse the command line arguments
# ------------------------------------------------------------------------------
print("#---------------------------------------------------------------------")
print("# Parsing command line arguments...")
print("#---------------------------------------------------------------------")

parser = argparse.ArgumentParser(description="Switched-Cap DC-DC generator")
parser.add_argument(
    "--specfile",
    required=True,
    help="File containing the specification for the generator",
)
parser.add_argument(
    "--output", required=True, help="Output directory for generator results"
)
parser.add_argument(
    "--platform", required=True, help="PDK/process kit for cadre flow (.e.g tsmc16lp)"
)
parser.add_argument(
    "--mode",
    default="verilog",
    choices=["verilog", "macro", "full"],
    help="Switched-Cap DC-DC Gen operation mode. Default mode: 'verilog'.",
)
parser.add_argument("--clean", action="store_true", help="Clean the workspace.")
args = parser.parse_args()

if not os.path.isfile(args.specfile):
    print("Error: specfile does not exist")
    print("File Path: " + args.specfile)
    sys.exit(1)

if args.platform != "tsmc65lp" and args.platform != "gf12lp":
    print("Error: Only supports TSMC65lp and GF12LP.")
    sys.exit(1)

if args.mode != "verilog":
    if os.path.isdir(pvtGenDir):
        sys.path.append(pyModulesDir)
        import clean_up as clc
        import cfg_digital_flow as cfg
        import run_digital_flow as rdf
    else:
        print(
            "Error. Private directory does not exist. "
            + "Please use only 'verilog' mode."
        )
        sys.exit(1)

# Load json spec file
print("Loading specfile...")
try:
    with open(args.specfile) as file:
        jsonSpec = json.load(file)
except ValueError as e:
    print("Error: Input Spec json file has an invalid format. %s" % str(e))
    sys.exit(1)

try:
    generator = jsonSpec["generator"]
except KeyError as e:
    print("Error: Bad Input Specfile. 'generator' variable is missing.")
    sys.exit(1)

if jsonSpec["generator"] != "dcdc-gen":
    print('Error: Generator specification must be "dcdc-gen".')
    sys.exit(1)

# Load json config file
print("Loading platform_config file...")
try:
    with open(genDir + "../../config/platform_config.json") as file:
        jsonConfig = json.load(file)
except ValueError as e:
    print("Error: platform_config.json file has an invalid format. %s" % str(e))
    sys.exit(1)

# Define the design variables
simTool = ""
extTool = ""
netlistTool = ""
calibreRulesDir = ""
designName = ""
Iload = ""
OutVolt = ""
Area = ""
Efficiency = ""
Frequency = ""

# Get the config variable from platfom config file
if args.mode != "verilog":
    simTool = jsonConfig["simTool"]
    if simTool != "hspice" and simTool != "finesim":
        print("Error: Supported simulators are 'hspice' or 'finesim' " + "as of now")
        sys.exit(1)

    if args.mode == "full":
        extTool = jsonConfig["extractionTool"]
        if extTool != "calibre":
            print("Error: Only support calibre extraction now")
            sys.exit(1)

        netlistTool = jsonConfig["netlistTool"]
        if netlistTool != "calibredrv":
            print("Error: Only support calibredrv netlist tool now")
            sys.exit(1)

try:
    platformConfig = jsonConfig["platforms"][args.platform]
except KeyError as e:
    print('Error: "' + args.platform + '" config not available')
    sys.exit(1)

if args.mode == "full":
    calibreRulesDir = platformConfig["calibreRules"]

# Get the design spec & parameters from spec file
try:
    designName = jsonSpec["module_name"]
except KeyError as e:
    print("Error: Bad Input Specfile. 'module_name' variable is missing.")
    sys.exit(1)

try:
    Iload = float(jsonSpec["specifications"]["Iload (mA)"])
except KeyError as e:
    print(
        "Error: Bad Input Specfile. 'Iload (mA)' value is missing under 'specifications'."
    )
    sys.exit(1)
except ValueError as e:
    print(
        "Error: Bad Input Specfile. Please use a float value for 'Iload (mA)' under 'specifications'."
    )
    sys.exit(1)
if Iload > 1.0 or Iload < 0.001:
    print("Error: Only support Iload from 0.001 ~ 1.0 now")
    sys.exit(1)

try:
    OutVolt = float(jsonSpec["specifications"]["Output voltage (V)"])
except KeyError as e:
    print(
        "Error: Bad Input Specfile. 'Output voltage (V)' value is missing under 'specifications'."
    )
    sys.exit(1)
except ValueError as e:
    print(
        "Error: Bad Input Specfile. Please use a float value for 'Output voltage (V) under 'specifications'."
    )
if OutVolt > 1.0 or OutVolt < 0.3:
    print("Error: Only support OutVolt in the range [0.3, 1.0] now")
    sys.exit(1)

# try:
#   Area = float(jsonSpec['specifications']['Area (mm^2)'])
# except KeyError as e:
#   print('Error: Bad Input Specfile. \'Area (mm^2)\' value is missing under \'specifications\'.')
#   sys.exit(1)
# except ValueError as e:
#   print('Error: Bad Input Specfile. Please use a float value for \'Area (mm^2)\' under \'specifications\'.')
#   sys.exit(1)
#
# try:
#   Efficiency = float(jsonSpec['specifications']['Efficiency (%)'])
# except KeyError as e:
#   print('Error: Bad Input Specfile. \'Efficiency (%)\' value is missing under \'specifications\'.')
#   sys.exit(1)
# except ValueError as e:
#   print('Error: Bad Input Specfile. Please use a float value for \'Efficiency (%)\' under \'specifications\'.')
#   sys.exit(1)

try:
    Frequency = float(jsonSpec["specifications"]["Clock frequency (kHz)"])
except KeyError as e:
    print(
        "Error: Bad Input Specfile. 'Clock frequency (kHz)' value is missing under 'specifications'."
    )
    sys.exit(1)
except ValueError as e:
    print(
        "Error: Bad Input Specfile. Please use a float value for 'Clock frequency (kHz)' under 'specifications'."
    )
    sys.exit(1)

print("\n\nRun Config:")
print('Mode - "' + args.mode + '"')
if args.mode != "verilog":
    print('Aux Lib - "' + platformConfig["aux_lib"] + '"')
    print('Digital Flow Directory - "' + flowDir + '"')
    print('Simulation Tool - "' + simTool + '"')
    print('Simulation Directory - "' + simDir + '"')
    if args.mode == "full":
        print('Netlisting Tool - "' + netlistTool + '"')
        print('Extraction Tool - "' + extTool + '"')
        print('Calibre Rules Directory - "' + calibreRulesDir + '"')
        print('Extraction Directory - "' + extDir + '"')

print("\n\nDCDC Spec:")
print('DCDC Instance Name - "' + designName + '"')
print('Supply Voltage - "' + str(platformConfig["nominal_voltage"]) + '"')
print('Iload(mA) - "' + str(Iload) + '"')
print('Output voltage (V) - "' + str(OutVolt) + '"')
# print('Area (mm^2) - \"' + str(Area) + '\"')
# print('Efficiency (%) - \"' + str(Efficiency) + '\"')
print('Frequency (kHz) - "' + str(Frequency) + '"')


# ------------------------------------------------------------------------------
# Clean the workspace
# ------------------------------------------------------------------------------
print("#---------------------------------------------------------------------")
print("# Cleaning the workspace...")
print("#---------------------------------------------------------------------")
if os.path.isdir(args.output):
    shutil.rmtree(args.output, ignore_errors=True)

if args.mode != "verilog":
    clc.wrkspace_clean(flowDir, extDir, simDir)
    if args.clean:
        print("Workspace clean done. Exiting the flow.")
        sys.exit(0)

    try:
        os.mkdir(flowDir + "/src")
    except OSError:
        print('Unable to create the "src" directory in "flow" folder')
        sys.exit(1)

    try:
        os.mkdir(simDir + "/run")
    except OSError:
        print('Unable to create the "run" directory in "simulation" folder')
        sys.exit(1)

    if args.mode == "full":
        try:
            os.mkdir(extDir + "/layout")
        except OSError:
            print('Unable to create the "layout" directory in "extraction" folder')
            sys.exit(1)

        try:
            os.mkdir(extDir + "/run")
        except OSError:
            print('Unable to create the "run" directory in "extraction" folder')
            sys.exit(1)

        try:
            os.mkdir(extDir + "/sch")
        except OSError:
            print('Unable to create the "sch" directory in "extraction" folder')
            sys.exit(1)
else:
    if args.clean:
        print("Workspace clean done. Exiting the flow.")
        sys.exit(0)

try:
    os.mkdir(args.output)
except OSError:
    print("Unable to create the output directory")
    sys.exit(1)

# ------------------------------------------------------------------------------
# Generate the Verilog
# ------------------------------------------------------------------------------

# Technology parameter ######
if args.platform == "tsmc65lp":
    k_sqrt_rc = 2.0e-6
    deltaV = 0.10
    unit_cap_capacitance = 1.8e-12
    unit_r_resistance = 5.0e2
elif args.platform == "gf12lp":
    k_sqrt_rc = 3.0e-6
    deltaV = 0.08
    unit_cap_capacitance = 2.0e-12
    unit_r_resistance = 2.0e2
#############################

SupplyVolt = platformConfig["nominal_voltage"]

# Determine the number of stages and the configuration
tmp_OutVolt = 0
up1_down0 = 1
dcdc_config = 0
dcdc_num_stage = 4

for i in range(4):
    if up1_down0 == 1:
        tmp_OutVolt = (SupplyVolt + tmp_OutVolt) / 2
        dcdc_config += 1 << (3 - i)
    else:
        tmp_OutVolt = tmp_OutVolt / 2
        dcdc_config -= 1 << (3 - i)
    if OutVolt + deltaV > tmp_OutVolt:
        up1_down0 = 1
    else:
        up1_down0 = 0

for i in range(4):
    if dcdc_config & 1 == 0:
        dcdc_config = dcdc_config >> 1
        dcdc_num_stage -= 1

# Determine the cap and switch size
dcdc_cap_size = int(
    (Iload * 0.001) / (2 * deltaV * Frequency * 1000) / 2 / unit_cap_capacitance
)
if dcdc_cap_size == 0:
    dcdc_cap_size = 1

dcdc_sw_size = int(
    unit_r_resistance
    / (k_sqrt_rc * SupplyVolt * math.sqrt(Frequency * 1000) / (Iload * 0.001))
)
if dcdc_sw_size == 0:
    dcdc_sw_size = 1

# Determine Offset_y
offset_y = 50 * int(dcdc_sw_size / (1 << (dcdc_num_stage - 1)))
if offset_y == 0:
    offset_y = 50

# Determine metals for power lines
if args.platform == "gf12lp":
    pg_m_h = "K3"
    pg_m_v = "K2"
    pg_via_hv = "U2"
    pg_unit_cap = "H2"
else:
    pg_m_h = "M7"
    pg_m_v = "M6"
    pg_via_hv = "VIA6"
    pg_unit_cap = "M9"

# Test Samples
# dcdc_num_stage = 2;
# dcdc_config = 3;
# dcdc_cap_size = 8;
# dcdc_sw_size = 4;

# dcdc_num_stage = 4;
# dcdc_config = 9;
# dcdc_cap_size = 48;
# dcdc_sw_size = 12;

# dcdc_num_stage = 4;
# dcdc_config = 9;
# dcdc_cap_size = 8;
# dcdc_sw_size = 4;

print("\n\n<DCDC Configuration>")
print("dcdc_num_stage: " + str(dcdc_num_stage))
print("dcdc_config: " + bin(dcdc_config))
print("dcdc_cap_size: " + str(dcdc_cap_size))
print("dcdc_sw_size: " + str(dcdc_sw_size) + "\n\n")

# Top Verilog Modification
with open(verilogDir + "/DCDC_TOP.template.v", "r") as file:
    filedata = file.read()
filedata = re.sub(r"module \S+", r"module " + designName, filedata)
filedata = re.sub(
    r"parameter DCDC_NUM_STAGE = \d+;",
    r"parameter DCDC_NUM_STAGE = " + str(dcdc_num_stage) + ";",
    filedata,
)
filedata = re.sub(
    r"parameter DCDC_CONFIG = \d+;",
    r"parameter DCDC_CONFIG = " + str(dcdc_config) + ";",
    filedata,
)
filedata = re.sub(
    r"parameter DCDC_CAP_SIZE = \d+;",
    r"parameter DCDC_CAP_SIZE = " + str(dcdc_cap_size) + ";",
    filedata,
)
filedata = re.sub(
    r"parameter DCDC_SW_SIZE = \d+;",
    r"parameter DCDC_SW_SIZE = " + str(dcdc_sw_size) + ";",
    filedata,
)

if args.mode == "verilog":
    with open(args.output + "/" + designName + ".v", "w") as file:
        file.write(filedata)
else:
    with open(flowDir + "/src/" + designName + ".v", "w") as file:
        file.write(filedata)
    shutil.copy(verilogDir + "/DCDC_CONV2to1.v", flowDir + "/src/" + "/DCDC_CONV2to1.v")
    shutil.copy(
        verilogDir + "/DCDC_HUNIT_CONV2to1.v",
        flowDir + "/src/" + "/DCDC_HUNIT_CONV2to1.v",
    )

    # SDC file Modification
    if args.platform == "gf12lp":
        period = 1.0e12 / (Frequency * 1000)
    else:
        period = 1.0e9 / (Frequency * 1000)
    clk_tran = period / 20
    with open(flowDir + "/scripts/dc/constraints.tcl", "r") as file:
        filedata = file.read()
    filedata = re.sub(
        r"create_clock .*",
        r'create_clock [get_ports clk] -name "CLK" -period ' + str(round(period, 2)),
        filedata,
    )
    with open(flowDir + "/scripts/dc/constraints.tcl", "w") as file:
        file.write(filedata)

    # innovus/setup.tcl Modification
    with open(flowDir + "/scripts/innovus/setup.tcl", "r") as file:
        filedata = file.read()
    filedata = re.sub(r"set v_supply .*", r"set v_supply " + str(SupplyVolt), filedata)
    filedata = re.sub(
        r"set num_stage .*", r"set num_stage " + str(dcdc_num_stage), filedata
    )
    filedata = re.sub(r"set config .*", r"set config " + str(dcdc_config), filedata)
    filedata = re.sub(
        r"set cap_size .*", r"set cap_size " + str(dcdc_cap_size), filedata
    )
    filedata = re.sub(r"set sw_size .*", r"set sw_size " + str(dcdc_sw_size), filedata)

    filedata = re.sub(r"set offset_y .*", r"set offset_y " + str(offset_y), filedata)
    filedata = re.sub(r"set pg_m_h .*", r'set pg_m_h "' + str(pg_m_h) + '"', filedata)
    filedata = re.sub(r"set pg_m_v .*", r'set pg_m_v "' + str(pg_m_v) + '"', filedata)
    filedata = re.sub(
        r"set pg_via_hv .*", r'set pg_via_hv "' + str(pg_via_hv) + '"', filedata
    )
    filedata = re.sub(
        r"set pg_unit_cap .*", r'set pg_unit_cap "' + str(pg_unit_cap) + '"', filedata
    )
    with open(flowDir + "/scripts/innovus/setup.tcl", "w") as file:
        file.write(filedata)

# ------------------------------------------------------------------------------
# Back-End
# ------------------------------------------------------------------------------

if args.mode != "verilog":
    # ---------------------------------------------------------------------------
    # Configure Synth and APR scripts
    # ---------------------------------------------------------------------------
    print("#------------------------------------------------------------------")
    print("# Configuring Synth and APR scripts...")
    print("#------------------------------------------------------------------")

    cfg.dcdc_gen_dg_flow_cfg(
        args.platform, platformConfig["aux_lib"], designName, flowDir
    )

    # ---------------------------------------------------------------------------
    # Run Synthesis and APR
    # ---------------------------------------------------------------------------
    print("#------------------------------------------------------------------")
    print("# Running Synth and APR scripts...")
    print("#------------------------------------------------------------------")

    rdf.run_synth_n_apr(args.platform, designName, flowDir)

    print("# DC-DC - Synthesis and APR finished")

# ------------------------------------------------------------------------------
# Write the Outputs
# ------------------------------------------------------------------------------
print("Writing the outputs")

if args.mode != "verilog":
    if os.path.isdir(args.output):
        for file in os.listdir(args.output):
            os.remove(args.output + "/" + file)

    p = sp.Popen(
        [
            "cp",
            flowDir + "/export/" + designName + ".gds.gz",
            args.output + "/" + designName + ".gds.gz",
        ]
    )
    p.wait()
    p = sp.Popen(
        [
            "cp",
            flowDir + "/export/" + designName + ".lef",
            args.output + "/" + designName + ".lef",
        ]
    )
    p.wait()
    p = sp.Popen(
        [
            "cp",
            flowDir + "/export/" + designName + "_typ.lib",
            args.output + "/" + designName + ".lib",
        ]
    )
    p.wait()
    p = sp.Popen(
        [
            "cp",
            flowDir + "/export/" + designName + "_typ.db",
            args.output + "/" + designName + ".db",
        ]
    )
    p.wait()
    p = sp.Popen(
        [
            "cp",
            flowDir + "/export/" + designName + ".lvs.v",
            args.output + "/" + designName + ".v",
        ]
    )
    p.wait()
    for file in glob.glob(flowDir + "/results/calibre/lvs/_" + designName + "*.sp"):
        shutil.copy(file, args.output + "/" + designName + ".spi")

# jsonSpec['results'] = {'platform': args.platform}
#
# with open(args.output + '/' + designName + '.json', 'w') as resultSpecfile:
#   json.dump(jsonSpec, resultSpecfile, indent=True)

print("Generator completed! \n")
