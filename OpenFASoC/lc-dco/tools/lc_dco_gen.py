#!/bin/python3.8
import argparse
import glob
import json
import os
import shutil
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ------------------------------------------------------------------------------
# Get the folder/file paths
# ------------------------------------------------------------------------------
genDir = os.path.join(os.path.dirname(os.path.relpath(__file__)), "../")
flowDir = genDir + "flow/"
simDir = genDir + "simulations/"
verilogDir = genDir + "src/"
supportedInputs = genDir + "tools/supported_inputs.json"

# ------------------------------------------------------------------------------
# Parse the command line arguments
# ------------------------------------------------------------------------------
print("#---------------------------------------------------------------------")
print("# Parsing command line arguments...")
print("#---------------------------------------------------------------------")
print(sys.argv)

parser = argparse.ArgumentParser(
    description="Digital Controlled LC-DCO design generator"
)
parser.add_argument(
    "--specfile",
    required=False,
    help="File containing the specification for the generator",
)
parser.add_argument(
    "--outputDir", required=False, help="Output directory for generator results"
)
parser.add_argument(
    "--platform", required=False, help="PDK/process kit for cadre flow (.e.g sky130)"
)
parser.add_argument(
    "--mode",
    default="verilog",
    choices=["verilog", "macro", "full"],
    help="LC-DCO Gen operation mode. Default mode: 'verilog'.",
)
parser.add_argument("--clean", action="store_true", help="Clean the workspace.")
parser.add_argument("--plot", action="store_true", help="Read and Plot the results.")

args = parser.parse_args()
# TODO
# Add arguments related to frequency and resolution
# Automatic calculation of mos and LC sizing based on these parameters
# Can we add ALIGN based generator for aux cells creation
if args.specfile:
    if not os.path.isfile(args.specfile):
        print("Error: specfile does not exist")
        print("File Path: " + args.specfile)
        sys.exit(1)

if args.platform and args.platform != "sky130":
    print("Error: Only supports sky130 tech as of now")
    sys.exit(1)

# Load json supported inputs file
if args.specfile:
    print("Loading supportedInputsFile...")
    try:
        with open(supportedInputs) as file:
            jsonSupportedInputs = json.load(file)
    except ValueError as e:
        print("Error: Supported Inputs json file has an invalid format. %s" % str(e))
        sys.exit(1)

    try:
        supportedSpecs = jsonSupportedInputs["platforms"][args.platform]
    except KeyError as e:
        print(
            "Error: '" + args.platform + "' tech is missing from supported platforms."
        )
        sys.exit(1)

    try:
        vin_max = float(supportedSpecs["vin"]["max"])
    except KeyError as e:
        print("Error: Bad Supported Inputs file. 'vin[max]' value is missing.")
        sys.exit(1)
    except ValueError as e:
        print("Error: Bad Input Specfile. Please use a float value for 'vin[max]'.")
        sys.exit(1)

    try:
        vin_min = float(supportedSpecs["vin"]["min"])
    except KeyError as e:
        print("Error: Bad Supported Inputs file. 'vin[min]' value is missing.")
        sys.exit(1)
    except ValueError as e:
        print("Error: Bad Input Specfile. Please use a float value for 'vin[min]'.")
        sys.exit(1)

    try:
        maxLoad_max = float(supportedSpecs["maxLoad"]["max"])
    except KeyError as e:
        print("Error: Bad Supported Inputs file. 'maxLoad[max]' value is missing.")
        sys.exit(1)
    except ValueError as e:
        print("Error: Bad Input Specfile. Please use a float value for 'maxLoad[max]'.")
        sys.exit(1)

    try:
        maxLoad_min = float(supportedSpecs["maxLoad"]["min"])
    except KeyError as e:
        print("Error: Bad Supported Inputs file. 'maxLoad[min]' value is missing.")
        sys.exit(1)
    except ValueError as e:
        print("Error: Bad Input Specfile. Please use a float value for 'maxLoad[min]'.")
        sys.exit(1)

    # Load json input spec file
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
    if jsonSpec["generator"] != "ldo-gen":
        print('Error: Generator specification must be "ldo-gen".')
        sys.exit(1)

    # Load json config file
    print("Loading platform_config file...")
    try:
        with open(genDir + "../../common/platform_config.json") as file:
            jsonConfig = json.load(file)
    except ValueError as e:
        print("Error: platform_config.json file has an invalid format. %s" % str(e))
        sys.exit(1)

    # Define the config & design variables
    mFile = ""
    mFilePublic = ""
    simTool = ""
    extTool = ""
    netlistTool = ""
    calibreRulesDir = ""
    designName = ""
    imax = ""
    vin = ""
    # Get the config variable from platfom config file
    if args.mode != "verilog":
        simTool = jsonConfig["simTool"]
        if simTool != "ngspice":
            print("Error: Only support simulator 'ngspice' as of now")
            sys.exit(1)

    mFile = genDir + "models/model.json"

    # Get the design spec & parameters from spec file
    try:
        designName = jsonSpec["module_name"]
    except KeyError as e:
        print("Error: Bad Input Specfile. 'module_name' variable is missing.")
        sys.exit(1)

    try:
        vin = float(jsonSpec["specifications"]["vin"])
    except KeyError as e:
        print(
            "Error: Bad Input Specfile. 'vin' value is missing under "
            + "'specifications'."
        )
        sys.exit(1)
    except ValueError as e:
        print(
            "Error: Bad Input Specfile. Please use a float value for 'vin' "
            + "under 'specifications'."
        )
        sys.exit(1)
    if vin > vin_max or vin < vin_min:
        print(
            "Error: Only support vin from "
            + str(vin_min)
            + " to "
            + str(vin_max)
            + " with increments of 0.1V now"
        )
        sys.exit(1)

    try:
        imax = float(jsonSpec["specifications"]["imax"])
    except KeyError as e:
        print(
            "Error: Bad Input Specfile. 'imax' value is missing under "
            + "'specifications'."
        )
        sys.exit(1)
    except ValueError as e:
        print(
            "Error: Bad Input Specfile. Please use a float value for 'imax' "
            + "under 'specifications'."
        )
    if imax > maxLoad_max or imax < maxLoad_min:
        print(
            "Error: Only support imax in the range ["
            + str(maxLoad_min)
            + ", "
            + str(maxLoad_max)
            + "] now"
        )
        sys.exit(1)

    aux_lib = genDir + "blocks/" + args.platform
    print("Run Config:")
    print('Mode - "' + args.mode + '"')
    print('Model File - "' + mFile + '"')
    if args.mode != "verilog":
        print('Aux Lib - "' + aux_lib + '"')
        print('Digital Flow Directory - "' + flowDir + '"')
        print('Simulation Tool - "' + simTool + '"')
        print('Simulation Directory - "' + simDir + '"')
    print('LDO Instance Name - "' + designName + '"')

    # Define the output variables
    designArea = 0
    iMaxOut = imax

# ------------------------------------------------------------------------------
# Clean the workspace
# ------------------------------------------------------------------------------
if args.clean:
    print("#---------------------------------------------------------------------")
    print("# Cleaning the workspace...")
    print("#---------------------------------------------------------------------")
    if os.path.isdir(args.outputDir):
        shutil.rmtree(args.outputDir, ignore_errors=True)

    if args.mode != "verilog":
        # clc.wrkspace_clean(flowDir, extDir, simDir)
        if args.clean:
            print("Workspace clean done. Exiting the flow.")
            sys.exit(0)
        try:
            os.mkdir(flowDir + "/src")
        except OSError:
            print('Unable to create the "src" directory in "flow" folder')
            sys.exit(1)

    else:
        if args.clean:
            print("Workspace clean done. Exiting the flow.")
            sys.exit(0)

    try:
        os.mkdir(args.outputDir)
    except OSError:
        print("Unable to create the output directory")
        sys.exit(1)

# ------------------------------------------------------------------------------
# Get the Power Transistor array size
# ------------------------------------------------------------------------------
# print('#---------------------------------------------------------------------')
# print('# Getting the Power Transistor array Size')
# print('#---------------------------------------------------------------------')
# if not os.path.isfile(mFile):
#    print("no valid model file, exit the flow")
#    sys.exit(1)
#    # if args.mode == 'verilog':
#    #    print('Model file \'' + mFile + '\' is not valid. ' + \
#    #          'Using the model file provided in the repo.')
#    #    mFile = mFilePublic
#    # else:
#    #    p = sp.Popen(['python',genDir+'./tools/ldo_model.py','--platform', \
#    #                 args.platform])
#    #    p.wait()
#
# try:
#    f = open(mFile, 'r')
# except ValueError as e:
#    print('Model file creation failed')
#    sys.exit(1)
# f.close()
#
# try:
#    with open(mFile, 'r') as file:
#        jsonModel = json.load(file)
# except ValueError as e:
#    print('Error: ldoModel.json file has an invalid format. %s' % str(e))
#    sys.exit(1)
#
# N = 0
# imax_t = 1.3*imax
# coefLength = len(jsonModel['Iload,max'][str(vin)])
# for i in range(coefLength):
#    z = jsonModel['Iload,max'][str(vin)][i]
#    N = N + (float(z)*pow(imax_t, (coefLength-i-1)))
# N = int(math.ceil(N))
# arrSize = N
# print('# LDO - Power Transistor array Size = ' + str(arrSize))
#
## Get the estimate of the area
# coefLength = len(jsonModel['area'])
# for i in range(coefLength):
#    z = jsonModel['area'][i]
#    designArea = designArea + (float(z)*pow(arrSize, (coefLength-i-1)))
# print('# LDO - Design Area Estimate = ' + str(designArea))

# ------------------------------------------------------------------------------
# Simulate and get result
# ------------------------------------------------------------------------------
# TODO create the right simulation file to mine data
if args.plot:
    flist = glob.glob(f"{simDir}/Ngspice/LC_run_sw_tia*meas*")
    result_df = pd.DataFrame()
    for fl in flist:
        print(fl)
        df1 = pd.read_csv(fl)
        result_df = result_df.append(df1)
# print(result_df[' code'])
result_df.set_index(" code", inplace=True)
for i in range(1, 256):
    if i in result_df.index:
        pass
    else:
        result_df.loc[i] = np.nan
result_interp = result_df.sort_index()
result_interp = result_interp.interpolate(method="linear").reset_index()
result_interp["Freq_dco"] = 1 / result_interp["tpertiaR_P"]
result_interp.plot.scatter(" code", "Freq_dco")
pd.set_option("display.max_rows", None)
fh = open("dco_code.csv", mode="w+")
print(result_interp[[" code", "Freq_dco"]].to_string(index=False), file=fh)
plt.show()
# -----------------------------------------------------------------------------
# Generate the Behavioral Verilog
# ------------------------------------------------------------------------------
# with open(verilogDir + '/LDO_TEMPLATE.v', 'r') as file:
#    filedata = file.read()
# filedata = re.sub(r'parameter integer ARRSZ = \d+;', \
#                  r'parameter integer ARRSZ = ' + str(arrSize) + ';', filedata)
# filedata = re.sub(r'module \S+', r'module ' + designName + '(', filedata)
# if args.mode == 'verilog':
#    with open(args.outputDir + '/' + designName + '.v', 'w') as file:
#        file.write(filedata)
# else:
#    with open(flowDir + '/src/' + designName + '.v', 'w') as file:
#        file.write(filedata)
#
## Get ctrl word initialization in hex
# ctrlWordHexCntF = int(math.floor(arrSize/4.0))
# ctrlWordHexCntR = int(arrSize % 4.0)
# ctrlWordHex = ['h']
# ctrlWordHex.append(str(hex(pow(2,ctrlWordHexCntR)-1)[2:]))
# for i in range(ctrlWordHexCntF):
#    ctrlWordHex.append('f')
# ctrlWdRst = str(arrSize) + '\'' + ''.join(ctrlWordHex)
#
# with open(verilogDir + '/LDO_CONTROLLER_TEMPLATE.v', 'r') as file:
#    filedata = file.read()
# filedata = re.sub(r'parameter integer ARRSZ = \d+;', \
#                  r'parameter integer ARRSZ = ' + str(arrSize) + ';', filedata)
# filedata = re.sub(r'wire \[ARRSZ-1:0\] ctrl_rst = \S+', r'wire ' + \
#                  '[ARRSZ-1:0] ctrl_rst = ' + ctrlWdRst + ';', filedata)
# if args.mode == 'verilog':
#    with open(args.outputDir + '/LDO_CONTROLLER.v', 'w') as file:
#        file.write(filedata)
# else:
#    with open(flowDir + '/src/LDO_CONTROLLER.v', 'w') as file:
#        file.write(filedata)
#
# print('# LDO - Behavioural Verilog Generated')
