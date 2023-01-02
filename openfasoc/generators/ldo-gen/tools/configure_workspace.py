# Utility functions to setup neccessary vars used in LDO-gen
import subprocess as sp
import argparse
import json
import math
import os
import re
import shutil
import sys


def get_directories():
    """Returns a hash table containing all neccessary dirs used in ldo-gen"""
    genDir = os.path.join(os.path.dirname(os.path.relpath(__file__)), "../")
    directories = dict()
    directories["genDir"] = genDir
    directories["flowDir"] = genDir + "flow/"
    directories["simDir"] = genDir + "simulations/"
    directories["verilogDir"] = genDir + "src/"
    directories["blocksDir"] = genDir + "blocks/sky130hvl/"
    directories["commonDir"] = genDir + "../../common/"
    directories["supportedInputs"] = genDir + "tools/supported_inputs.json"
    directories["objDir"] = genDir + "flow/objects/sky130hvl/ldo/base/"
    return directories


def check_args(args):
    """Provides command line valid input checking. No return - exits on fail"""
    if not os.path.isfile(args.specfile):
        print("Error: specfile does not exist")
        print("File Path: " + args.specfile)
        sys.exit(1)
    if args.platform != "sky130hvl":
        print("Error: Only supports sky130 tech as of now")
        sys.exit(1)
    # create output dir
    if os.path.isdir(args.outputDir):
        shutil.rmtree(args.outputDir, ignore_errors=True)
    try:
        os.mkdir(args.outputDir)
    except OSError:
        print("Unable to create the output directory")
        sys.exit(1)


def process_supported_inputs(args, directories):
    """Returns a hash table containing all neccessary information on generator supported specs."""
    supportedInputs = directories["supportedInputs"]
    spec_ranges = dict()
    # Load json supported inputs file and conduct error checking
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
    # write into dictionary
    try:
        spec_ranges["vin_max"] = float(supportedSpecs["vin"]["max"])
    except KeyError as e:
        print("Error: Bad Supported Inputs file. 'vin[max]' value is missing.")
        sys.exit(1)
    except ValueError as e:
        print("Error: Bad Input Specfile. Please use a float value for 'vin[max]'.")
        sys.exit(1)
    try:
        spec_ranges["vin_min"] = float(supportedSpecs["vin"]["min"])
    except KeyError as e:
        print("Error: Bad Supported Inputs file. 'vin[min]' value is missing.")
        sys.exit(1)
    except ValueError as e:
        print("Error: Bad Input Specfile. Please use a float value for 'vin[min]'.")
        sys.exit(1)
    try:
        spec_ranges["maxLoad_max"] = float(supportedSpecs["maxLoad"]["max"])
    except KeyError as e:
        print("Error: Bad Supported Inputs file. 'maxLoad[max]' value is missing.")
        sys.exit(1)
    except ValueError as e:
        print("Error: Bad Input Specfile. Please use a float value for 'maxLoad[max]'.")
        sys.exit(1)
    try:
        spec_ranges["maxLoad_min"] = float(supportedSpecs["maxLoad"]["min"])
    except KeyError as e:
        print("Error: Bad Supported Inputs file. 'maxLoad[min]' value is missing.")
        sys.exit(1)
    except ValueError as e:
        print("Error: Bad Input Specfile. Please use a float value for 'maxLoad[min]'.")
        sys.exit(1)
    # return filled hash table
    return spec_ranges


def get_spec(specfile, valid_spec_ranges):
    """Returns a hash table containing user specs."""
    user_specs = dict()
    # Load json input spec file
    print("Loading specfile...")
    try:
        with open(specfile) as file:
            jsonSpec = json.load(file)
    except ValueError as e:
        print("Error: Input Spec json file has an invalid format. %s" % str(e))
        sys.exit(1)
    # ensure generator is ldo-gen
    try:
        generator = jsonSpec["generator"]
    except KeyError as e:
        print("Error: Bad Input Specfile. 'generator' variable is missing.")
        sys.exit(1)
    if jsonSpec["generator"] != "ldo-gen":
        print('Error: Generator specification must be "ldo-gen".')
        sys.exit(1)
    # enter design spec and parameters into hash table
    try:
        user_specs["designName"] = jsonSpec["module_name"]
    except KeyError as e:
        print("Error: Bad Input Specfile. 'module_name' variable is missing.")
        sys.exit(1)
    try:
        user_specs["vin"] = float(jsonSpec["specifications"]["vin"])
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
    # ensure vin falls within valid range
    if (
        user_specs["vin"] > valid_spec_ranges["vin_max"]
        or user_specs["vin"] < valid_spec_ranges["vin_min"]
    ):
        print(
            "Error: Only support vin from "
            + str(valid_spec_ranges["vin_min"])
            + " to "
            + str(valid_spec_ranges["vin_max"])
            + " with increments of 0.1V now"
        )
        sys.exit(1)
    try:
        user_specs["imax"] = float(jsonSpec["specifications"]["imax"])
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
    if (
        user_specs["imax"] > valid_spec_ranges["maxLoad_max"]
        or user_specs["imax"] < valid_spec_ranges["maxLoad_min"]
    ):
        print(
            "Error: Only support imax in the range ["
            + str(valid_spec_ranges["maxLoad_min"])
            + ", "
            + str(valid_spec_ranges["maxLoad_max"])
            + "] now"
        )
        sys.exit(1)
    # return populated hash table
    return user_specs


def get_config(genmode, genDir):
    """Load JSON config with error checking."""
    print("Loading platform_config file...")
    try:
        with open(genDir + "../../common/platform_config.json") as file:
            jsonConfig = json.load(file)
    except ValueError as e:
        print("Error: platform_config.json file has an invalid format. %s" % str(e))
        sys.exit(1)
    # check that simTool is supported
    if genmode != "verilog":
        if jsonConfig["simTool"] != "ngspice":
            print("Error: Only support simulator 'ngspice' as of now")
            sys.exit(1)
    return jsonConfig


def get_setup_pdk(jsonConfig, commonDir):
    """Returns the pdk_path and copies DRC/LVS files from pdk to common dir."""
    # TODO: check GCP/GHA pdk paths
    pdk = None
    if os.getenv("PDK_ROOT") is not None:
        pdk = os.path.join(os.environ["PDK_ROOT"], "sky130A")
        try:
            sp.Popen(
                [
                    "sed -i 's/set PDKPATH \".*/set PDKPATH $env(PDK_ROOT)\/sky130A/' $PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc"
                ],
                shell=True,
            ).wait()
        except:
            pass
    else:
        pdk = jsonConfig["open_pdks"]
    # error checking for libs.ref / libs.tech in pdk dir
    if not os.path.isdir(os.path.join(pdk, "libs.ref")):
        print("Cannot find libs.ref folder from open_pdks in " + pdk)
        sys.exit(1)
    elif not os.path.isdir(os.path.join(pdk, "libs.tech")):
        print("Cannot find libs.tech folder from open_pdks in " + pdk)
        sys.exit(1)
    # copy LVS/DRC setup files to common dir
    sky130A_path = commonDir + "drc-lvs-check/sky130A/"
    if not os.path.isdir(sky130A_path):
        os.mkdir(sky130A_path)
    shutil.copy2(os.path.join(pdk, "libs.tech/magic/sky130A.magicrc"), sky130A_path)
    shutil.copy2(os.path.join(pdk, "libs.tech/netgen/sky130A_setup.tcl"), sky130A_path)
    return pdk


def check_JSON(JSON_to_check):
    """Checks opening a JSON and that the JSON is valid format."""
    if not os.path.isfile(JSON_to_check):
        print(str(JSON_to_check) + "is not a valid file, exit the flow.")
        sys.exit(1)
    try:
        with open(JSON_to_check, "r") as file:
            jsonModel = json.load(file)
    except ValueError as e:
        print("Error: ldoModel.json file has an invalid format. %s" % str(e))
        sys.exit(1)
    return jsonModel
