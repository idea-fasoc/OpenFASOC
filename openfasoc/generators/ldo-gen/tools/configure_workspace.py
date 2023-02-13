# Utility functions to setup neccessary vars used in LDO-gen
import subprocess as sp
import argparse
import json
import math
import os
import re
import shutil
import sys
import time

DEFAULT_JSON_SPEC = "spec.json"


def check_JSON(JSON_to_check):
    """Checks opening a JSON and that the JSON is valid format.
    Return a dictionary object with the JSON data."""
    if not os.path.isfile(JSON_to_check):
        print(str(JSON_to_check) + " is not a valid json file, exiting the flow.")
        sys.exit(1)
    try:
        with open(JSON_to_check, "r") as file:
            jsonModel = json.load(file)
    except ValueError as e:
        print("Error: json file has an invalid format. %s" % str(e))
        sys.exit(1)
    return jsonModel


def get_directories():
    """Returns a hash table containing all neccessary dirs used in ldo-gen"""
    genDir = os.path.join(os.path.dirname(os.path.relpath(__file__)), "../")
    directories = dict()
    directories["genDir"] = genDir + "/"
    directories["flowDir"] = os.path.abspath(genDir + "flow/") + "/"
    directories["simDir"] = os.path.abspath(genDir + "simulations/") + "/"
    directories["verilogDir"] = os.path.abspath(genDir + "src/") + "/"
    directories["blocksDir"] = os.path.abspath(genDir + "blocks/sky130hvl/") + "/"
    directories["commonDir"] = os.path.abspath(genDir + "../../common/") + "/"
    directories["supportedInputs"] = os.path.abspath(
        genDir + "tools/supported_inputs.json"
    )
    directories["objDir"] = (
        os.path.abspath(genDir + "flow/objects/sky130hvl/ldo/base/") + "/"
    )
    return directories


def check_args(args, clean_work_dir):
    """Provides command line valid input checking. returns spec file when appropriate - exits on fail"""
    JSON_spec = dict()
    if args.specfile is not None:
        JSON_spec = check_JSON(args.specfile)
    else:
        if not (args.name) or not (args.imax) or not (args.vref):
            if not check_JSON(DEFAULT_JSON_SPEC):
                print(
                    "Error: no spec file and no default spec file and one or more command line spec args are not properly set."
                )
                print(
                    'The generator looks for a default spec file called "'
                    + str(DEFAULT_JSON_SPEC)
                    + '" in the ldo-gen directory'
                )
                sys.exit(1)
    if args.platform != "sky130hvl":
        print("Error: Only supports sky130 tech as of now")
        sys.exit(1)
    # create output dir
    if clean_work_dir:
        shutil.rmtree(args.outputDir, ignore_errors=True)
        try:
            os.mkdir(args.outputDir)
        except OSError:
            print("Unable to create the output directory")
            sys.exit(1)
    return JSON_spec


def process_supported_inputs(args, directories):
    """Returns a hash table containing all neccessary information on generator supported specs."""
    supportedInputs = directories["supportedInputs"]
    jsonSupportedInputs = check_JSON(directories["supportedInputs"])
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


def fill_in_the_blank_specs(user_specs):
    """Checks if missing specs then uses specification.json in ldo-gen directory to fill in missing specs."""
    if (
        not "designName" in user_specs
        or not "vin" in user_specs
        or not "imax" in user_specs
    ):
        print("One or more required specs are missing")
        print("Attempting to fill in missing entries using backup specfile")
        jsonSpec = check_JSON(DEFAULT_JSON_SPEC)
        if not "designName" in user_specs:
            user_specs["designName"] = str(jsonSpec["module_name"])
        if not "vin" in user_specs:
            user_specs["vin"] = float(jsonSpec["specifications"]["vin"])
        if not "imax" in user_specs:
            user_specs["imax"] = float(jsonSpec["specifications"]["imax"])
    return user_specs


def get_spec(args, jsonSpec, valid_spec_ranges):
    """Returns a hash table containing user specs."""
    user_specs = dict()
    # enter design spec and parameters into hash table
    if jsonSpec:
        try:
            user_specs["designName"] = jsonSpec["module_name"]
            user_specs["vin"] = float(jsonSpec["specifications"]["vin"])
            user_specs["imax"] = float(jsonSpec["specifications"]["imax"])
        except KeyError as e:
            user_specs = fill_in_the_blank_specs(user_specs)
    else:
        if args.name:
            user_specs["designName"] = str(args.name)
        if args.vref:
            user_specs["vin"] = float(args.vref)
        if args.imax:
            user_specs["imax"] = float(args.imax)
        user_specs = fill_in_the_blank_specs(user_specs)

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


def dump_JSON_specs(user_specs):
    """Dumps user specs to a JSON file and returns the file path."""
    JSON_dumpfile_data = dict()
    JSON_dumpfile_data["module_name"] = str(user_specs["designName"])
    JSON_dumpfile_data["generator"] = "ldo-gen"
    JSON_dumpfile_data["specifications"] = dict()
    JSON_dumpfile_data["specifications"]["vin"] = float(user_specs["vin"])
    JSON_dumpfile_data["specifications"]["imax"] = float(user_specs["imax"])
    JSON_dumpfile_name = time.strftime("%b_%d_%H_%M_%S", time.localtime()) + "dump.json"
    with open(JSON_dumpfile_name, "w") as JSON_dumpfile_handle:
        json.dump(JSON_dumpfile_data, JSON_dumpfile_handle, indent=4)
        JSON_dumpfile_path = os.path.abspath(JSON_dumpfile_name)
    return JSON_dumpfile_path


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


def copy_outputs(directories, relativeOutputDir, platform, designName):
    """Copies all final files to the work directory."""
    outputDir = directories["genDir"] + relativeOutputDir
    shutil.copyfile(
        directories["flowDir"] + "results/" + platform + "/ldo/base/6_final.gds",
        outputDir + "/" + designName + ".gds",
    )
    shutil.copyfile(
        directories["flowDir"] + "results/" + platform + "/ldo/base/6_final.def",
        outputDir + "/" + designName + ".def",
    )
    shutil.copyfile(
        directories["flowDir"] + "results/" + platform + "/ldo/base/6_final.v",
        outputDir + "/" + designName + ".v",
    )
    shutil.copyfile(
        directories["flowDir"] + "results/" + platform + "/ldo/base/6_1_fill.sdc",
        outputDir + "/" + designName + ".sdc",
    )
    shutil.copyfile(
        directories["objDir"] + "netgen_lvs/spice/" + designName + ".spice",
        outputDir + "/" + designName + ".spice",
    )
    shutil.copyfile(
        directories["objDir"] + "netgen_lvs/spice/" + designName + "_pex.spice",
        outputDir + "/" + designName + "_pex.spice",
    )
    shutil.copyfile(
        directories["flowDir"] + "reports/" + platform + "/ldo/base/6_final_drc.rpt",
        outputDir + "/6_final_drc.rpt",
    )
    shutil.copyfile(
        directories["flowDir"] + "reports/" + platform + "/ldo/base/6_final_lvs.rpt",
        outputDir + "/6_final_lvs.rpt",
    )
