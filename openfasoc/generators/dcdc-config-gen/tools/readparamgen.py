import numpy as np
from numpy.polynomial import Polynomial
import csv
import json
import os
import time
import heapq
from collections import defaultdict
import glob
import operator

import sys
import getopt
import math
import subprocess as sp
import fileinput
import re
import shutil
import argparse

# ------------------------------------------------------------------------------
# Parse the command line arguments
# ------------------------------------------------------------------------------
print("#----------------------------------------------------------------------")
print("# Parsing command line arguments...")
print("#----------------------------------------------------------------------")
print(sys.argv)

genDir = os.path.join(os.path.dirname(os.path.relpath(__file__)), "../")

parser = argparse.ArgumentParser(
    description="Programmable Switched-Cap DC-DC generator"
)
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
parser.add_argument(
    "--mode",
    default="verilog",
    help="Specify the outputs to be generated: verilog, macro, full (includes PEX extraction)",
)
parser.add_argument("--clean", action="store_true", help="Clean the workspace.")
args = parser.parse_args()


if not os.path.isfile(args.specfile):
    print("Error: specfile does not exist")
    print("File Path: " + args.specfile)
    sys.exit(1)

supportedPlatforms = {"sky130hd", "sky130hs"}
unsupportedPlatforms = {
    "sky130hvl",
    "sky130osu12Ths",
    "sky130osu12Tms",
    "sky130osu12Tls",
    "sky130osu15Ths",
    "sky130osu15Tms",
    "sky130osu15Tls",
    "sky130osu18Ths",
    "sky130osu18Tms",
    "sky130osu18Tls",
}

if args.platform not in supportedPlatforms:
    print("Error: only", supportedPlatforms, "platforms are supported as of now")
    sys.exit(1)

# Load json spec file
print("Loading specfile...")
try:
    with open(args.specfile) as file:
        jsonSpec = json.load(file)
except ValueError as e:
    print("Error occurred opening or loading json file.")
    print >> sys.stderr, "Exception: %s" % str(e)
    sys.exit(1)

if jsonSpec["generator"] != "dcdc-gen":
    print('Error: Generator specification must be "dcdc-gen".')
    sys.exit(1)

try:
    designName = jsonSpec["module_name"]
except KeyError as e:
    print("Error: Bad Input Specfile. 'module_name' variable is missing.")
    sys.exit(1)
