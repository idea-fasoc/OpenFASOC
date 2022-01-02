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

from simulation import generate_runs



#------------------------------------------------------------------------------
# Parse the command line arguments
#------------------------------------------------------------------------------
print("#----------------------------------------------------------------------")
print("# Parsing command line arguments...")
print("#----------------------------------------------------------------------")
print( sys.argv)

genDir = os.path.join(os.path.dirname(os.path.relpath(__file__)),"../")

parser = argparse.ArgumentParser(description='Cryo design generator')
parser.add_argument('--specfile', required=True,
                    help='File containing the specification for the generator')
parser.add_argument('--outputDir', required=True,
                    help='Output directory for generator results')
parser.add_argument('--platform', required=True,
                    help='PDK/process kit for cadre flow (.e.g tsmc16)')
parser.add_argument('--mode', required=True,
                    help='Specify the outputs to be generated: verilog, macro, full (includes PEX extraction)')
parser.add_argument('--ninv', required=False,
                    help='Number of target inverters')
parser.add_argument('--nhead', required=False,
                    help='Number of target headers')
parser.add_argument('--clean', action='store_true',
                    help='Clean the workspace.')
args = parser.parse_args()



if not os.path.isfile(args.specfile):
   print('Error: specfile does not exist')
   print('File Path: ' + args.specfile)
   sys.exit(1)


if args.platform != 'sky130hd' and args.platform != 'sky130hs' and args.platform != 'sky130hvl' and args.platform != 'sky130osu12Ths' and args.platform != 'sky130osu18Ths':
  print("Error: only sky130hd, sky130hs, sky130hvl, sky130osu12Ths, and sky130osu18Ths platforms are supported as of now")
  sys.exit(1)

# Load json spec file
print("Loading specfile...")
try:
  with open(args.specfile) as file:
    jsonSpec = json.load(file)
except ValueError as e:
  print("Error occurred opening or loading json file.")
  print >> sys.stderr, 'Exception: %s' % str(e)
  sys.exit(1)

if jsonSpec['generator'] != 'cryo-gen':
  print("Error: Generator specification must be \"cryo-gen\".")
  sys.exit(1)


try:
   designName = jsonSpec['module_name']
except KeyError as e:
   print('Error: Bad Input Specfile. \'module_name\' variable is missing.')
   sys.exit(1)


#      generate_runs(genDir, jsonSpec['module_name'], headerList, invList, tempList, jsonConfig, args.platform, modeling=True)
      
      
# Get the design spec & parameters from spec file
designName = jsonSpec['module_name']


def main():
    #check model
    if Model == "":
        print("Model file is missing")
        exit()
    else:
        #Check if temparature range field is not empty
        if Tempmin == "" or Tempmax == "":
            print("Please provide a temperature range")
            exit()
        else:
            if Optimization == "power":
                #THIS IS THE MAIN FUNCTION for power optimization
                print("*********Performing Power Optimization*********")
                time.sleep(5)
                return calculate_min_error_new(df, delta_1st_pass, number_rows)
            elif Optimization == "error":
                print("*********Performing Error Optimization*********")
                time.sleep(5)
                #THIS IS THE MAIN FUNCTION for error optimization
                return calculate_min_power_new(df, delta_1st_pass, number_rows)



