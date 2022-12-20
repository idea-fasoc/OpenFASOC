import argparse
import re

parser = argparse.ArgumentParser(description="parse simulators' output file")
parser.add_argument("--tool", "-t", required=True, help="simulator type")
parser.add_argument(
    "--inputFile", "-i", required=True, help="simulator's output for processing"
)
args = parser.parse_args()

file_name = args.inputFile
tool_name = args.tool

with open(file_name, "r") as rf:
    log_file_text = rf.read()

    temp_patten = "TEMP\s*=\s*([0-9\-\.]+)"
    temp_value_re = re.search(temp_patten, log_file_text)
    temp_value = "failed"
    if temp_value_re:
        temp_value = temp_value_re.group(1)

    period_pattern = "PERIOD\s*=\s*([0-9\.e-]+)"
    period_pattern_re = re.search(period_pattern, log_file_text)
    period_value = "failed"
    if period_pattern_re:
        period_value = period_pattern_re.group(1)

    power_pattern = "POWER\s*=\s*([0-9\.e-]+)"
    power_pattern_re = re.search(power_pattern, log_file_text)
    power_value = "failed"
    if power_pattern_re:
        power_value = power_pattern_re.group(1)

    print(
        "%s	%s %s" % (temp_value, period_value, power_value),
        file=open("sim_output", "a"),
    )
