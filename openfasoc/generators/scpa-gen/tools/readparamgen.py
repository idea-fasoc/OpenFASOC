import argparse
import json
import os
import sys
import time

import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------
# Parse the command line arguments
# ------------------------------------------------------------------------------
print("#----------------------------------------------------------------------")
print("# Parsing command line arguments...")
print("#----------------------------------------------------------------------")
print(sys.argv)

genDir = os.path.join(os.path.dirname(os.path.relpath(__file__)), "../")

parser = argparse.ArgumentParser(
    description="Switched Capacitor Power Amplifier design generator"
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
    required=True,
    help="Specify the outputs to be generated: verilog, macro, full (includes PEX extraction)",
)
parser.add_argument("--ninv", required=False, help="Number of target inverters")
parser.add_argument("--nhead", required=False, help="Number of target headers")
parser.add_argument("--clean", action="store_true", help="Clean the workspace.")
args = parser.parse_args()


if not os.path.isfile(args.specfile):
    print("Error: specfile does not exist")
    print("File Path: " + args.specfile)
    sys.exit(1)


if args.platform != "sky130hd" and args.platform != "sky130hs":
    print("Error: only sky130hd and sky130hs platforms are supported as of now")
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

if jsonSpec["generator"] != "scpa-gen":
    print('Error: Generator specification must be "scpa-gen".')
    sys.exit(1)


try:
    designName = jsonSpec["module_name"]
except KeyError as e:
    print("Error: Bad Input Specfile. 'module_name' variable is missing.")
    sys.exit(1)

# try:
#   Tempmin = jsonSpec['specifications']['temperature']['min']
#   Tempmax = jsonSpec['specifications']['temperature']['max']
# except KeyError as e:
#   print('Error: Bad Input Specfile. \'range o\' value is missing under ' + \
#         '\'specifications\'.')
#   sys.exit(1)
except ValueError as e:
    print(
        "Error: Bad Input Specfile. Please use a float value for 'range ' "
        + "under 'specifications'."
    )
    sys.exit(1)


# mFile1 = genDir + '/models/modelfile.csv'
# mFilePublic1 = genDir + args.platform + '.model_tempsense'

# if not os.path.isfile(mFile1):
#   if args.mode == 'verilog':
#      print('Model file \'' + mFile1 + '\' is not valid. ' + \
#            'Using the model file provided in the repo.')
#      mFile1 = mFilePublic1
#   else:
#      print('generating a local model file')
#
#      try:
#        with open(genDir + '../../common/platform_config.json') as file:
#          jsonConfig = json.load(file)
#      except ValueError as e:
#        print("Error occurred opening or loading json file.")
#        print >> sys.stderr, 'Exception: %s' % str(e)
#        sys.exit(1)
#
#      headerList = range(3, 11, 2)
#      invList = range(4, 12, 2)
#      tempList = range(-20, 120, 20)
#      all_result_start_line = 3
#
#      generate_runs(genDir, jsonSpec['module_name'], headerList, invList, tempList, jsonConfig, args.platform, modeling=True)
#
#      modelfile = open(genDir + "models/modelfile.csv", "w")
#      fieldnames = ["Temp", "Frequency", "Power", "Error", "inv", "header"]
#      writer = csv.DictWriter(modelfile, fieldnames=fieldnames)
#      writer.writeheader()
#
#      all_runs = glob.glob(genDir + "simulations/run/*")
#      for run in all_runs:
#        run_re = re.search("inv([0-9]+)_header([0-9]+)", run)
#        inv = run_re.group(1)
#        header = run_re.group(2)
#
#        with open(run + "/all_result", "r") as rf:
#          filedata = rf.readlines()
#          for valid_line in filedata[all_result_start_line-1:]:
#            valid_data = valid_line.split()
#            writer.writerow({"Temp": valid_data[0], "Frequency": valid_data[1], "Power": valid_data[2], \
#                             "Error": valid_data[3], "inv": inv, "header": header})
#
#      modelfile.close()

# store content in objects
# Temp = obj['temperature']
# Power = jsonSpec['specifications']['power']
# Error = jsonSpec['specifications']['error']
# Optimization = jsonSpec['specifications']['optimization']
# Model = mFile1


# Get the design spec & parameters from spec file
designName = jsonSpec["module_name"]

# Tmin = float(jsonSpec['specifications']['temperature']['min'])
# Tmax = float(jsonSpec['specifications']['temperature']['max'])
# if (Tmax > 100 )  or (Tmin < -20 ):
#   print("Error: Supported temperature sensing must be inside the following range [-20 to 100] Celcius")
#   sys.exit(1)
# if Tmax < Tmin:
#   print("Error: Supported temperature sensing must be inside the following range [-20 to 100] Celcius")
#   sys.exit(1)


# optimization = str(jsonSpec['specifications']['optimization'])
# if optimization != "error" and optimization != "power":
#   print("Error: Please enter a supported optmization strategy [error or power]")
#   sys.exit(1)


###SEARCH starts here
###
# print('-----------split----- :   min power' , split_df(df,7))

# la premiere fonction developee
# calculate min power and extract inv and header
def main():
    # check model
    if Model == "":
        print("Model file is missing")
        exit()
    else:
        # Check if temparature range field is not empty
        if Tempmin == "" or Tempmax == "":
            print("Please provide a temperature range")
            exit()
        else:
            if Optimization == "power":
                # THIS IS THE MAIN FUNCTION for power optimization
                print("*********Performing Power Optimization*********")
                time.sleep(5)
                return calculate_min_error_new(df, delta_1st_pass, number_rows)
            elif Optimization == "error":
                print("*********Performing Error Optimization*********")
                time.sleep(5)
                # THIS IS THE MAIN FUNCTION for error optimization
                return calculate_min_power_new(df, delta_1st_pass, number_rows)
