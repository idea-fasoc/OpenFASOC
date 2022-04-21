import argparse
import math
import os
import sys

parser = argparse.ArgumentParser(description="calculate error values")
parser.add_argument(
    "--mode",
    "-m",
    required=True,
    help="simulation mode, full: skip power, partial: extract power",
)
args = parser.parse_args()


simDir = os.path.dirname(os.path.relpath(__file__))
sim_output_file = open(simDir + "sim_output", "r")

data0 = []
temp = []
power_list = []
sim_output_lines = sim_output_file.readlines()
for line in sim_output_lines:
    data = line.split()
    temp.append(data[0])
    data0.append(data[1])
    if args.mode == "partial":
        power_list.append(data[2])

frequency_list = []
data1 = list()
for i, val in enumerate(data0):
    if val == "failed":
        val_cal = "failed"
        frequency = "failed"
    else:
        frequency = 1 / float(val)
        print("temp: %s, \tfrequency: %f" % (temp[i], frequency))
        val_cal = math.log(1 / float(val)) * ((-20 + i * 20) + 273.15) * 0.01
    frequency_list.append(frequency)
    data1.append(val_cal)

data2 = []
slope_f = 80 / (data1[len(data1) - 2] - data1[1])
for k in data1:
    if k == "failed":
        val = "failed"
    else:
        val = k * slope_f
    data2.append(val)

data3 = []
offset = data2[1]
for val in data2:
    if val == "failed":
        val = "failed"
    else:
        val = val - offset
    data3.append(val)

data4 = []
for i, val in enumerate(data3):
    if val == "failed":
        val = "failed"
    else:
        val = (-20 + i * 20) - val
    data4.append(val)


print(os.getcwd(), file=open("all_result", "a"))
if args.mode == "partial":
    print("Temp Frequency Power Error", file=open("all_result", "a"))
elif args.mode == "full":
    print("Temp Frequency Error", file=open("all_result", "a"))
else:
    print("simulation mode - " + args.mode + " is not supported")
    sys.exit(1)
for idx, line in enumerate(sim_output_lines):
    result_list = line.split()
    if args.mode == "partial":
        print(
            "%s %s %s %s"
            % (result_list[0], frequency_list[idx], power_list[idx], data4[idx]),
            file=open("all_result", "a"),
        )
    elif args.mode == "full":
        print(
            "%s %s %s" % (result_list[0], frequency_list[idx], data4[idx]),
            file=open("all_result", "a"),
        )
