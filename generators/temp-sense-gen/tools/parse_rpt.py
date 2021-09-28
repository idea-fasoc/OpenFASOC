import re
import subprocess
import sys

filename = "flow/reports/sky130hd/tempsense/6_final_lvs.rpt"
line = subprocess.check_output(['tail', '-1', filename]).decode(sys.stdout.encoding)

regex = r"failed"
match = re.search(regex, line)

if match != None:
	print("LVS failed!")
	raise ValueError("LVS failed!")
else:
	print("LVS is clean!")
