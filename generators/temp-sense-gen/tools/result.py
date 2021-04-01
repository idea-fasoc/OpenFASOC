import re
import sys
import argparse

parser = argparse.ArgumentParser(
    description = "parse simulators' output file")
parser.add_argument("--tool", "-t", required=True,
                    help="simulator type")
parser.add_argument("--inputFile", "-i", required=True,
                    help="simulator's output for processing")
args = parser.parse_args()

file_name = args.inputFile
tool_name = args.tool

if tool_name == "finesim":
  r_mt0 = open(file_name)
  mt0_lines=r_mt0.readlines()
  
  data_start_line = 4
  result = list()
  result = mt0_lines[data_start_line-1].split()
  
  print("%s	%s"%(result[2], result[0]), file=open("sim_output", "a"))
elif tool_name == "ngspice":
  log_file = open(file_name)
  log_file_text = log_file.read()

  temp_patten = "TEMP = ([0-9\-\.]+)"
  temp_value_re = re.search(temp_patten, log_file_text)
  temp_value = 'failed'
  if temp_value_re:
    temp_value = temp_value_re.group(1)

  period_pattern = "period\s+=\s+([0-9\.e-]+)"
  period_pattern_re = re.search(period_pattern, log_file_text)
  period_value = 'failed'
  if period_pattern_re:
    period_value = period_pattern_re.group(1)

  print("%s	%s"%(temp_value, period_value), file=open("sim_output", "a"))

