import re
import argparse

parser = argparse.ArgumentParser(description="Add ndr rules to specified nets")
parser.add_argument("--inputDef", "-i", required=True, help="Input DEF")
parser.add_argument("--nets", "-n", required=True, help="target Nets")
parser.add_argument("--rule", "-r", required=True, help="ndr rule")
parser.add_argument("--outputDef", "-o", required=True, help="Output DEF")

args = parser.parse_args()
nets = args.nets.split()
rule = args.rule

with open(args.inputDef, "r") as rf:
    filedata = rf.read()

for net in nets:
    filedata = re.sub(
        "(-\s" + net + " .*\+ USE SIGNAL );",
        "\g<1>" + "+ NONDEFAULTRULE " + rule + " ;",
        filedata,
    )

with open(args.outputDef, "w") as wf:
    wf.write(filedata)
