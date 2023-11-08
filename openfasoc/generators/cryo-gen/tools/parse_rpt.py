import re
import subprocess
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common.check_gen_files import check_gen_files

dir_path = r'flow/reports'
lib = os.listdir(dir_path)

drc_filename = "flow/reports/" + str(lib[0]) + "/cryo/6_final_drc.rpt"
num_lines = sum(1 for line in open(drc_filename))

if num_lines > 3:
    raise ValueError("DRC failed!")
else:
    print("DRC is clean!")

lvs_filename = "flow/reports/" + str(lib[0]) + "/cryo/6_final_lvs.rpt"
lvs_line = subprocess.check_output(["tail", "-1", lvs_filename]).decode(
    sys.stdout.encoding
)

regex = r"failed"
match = re.search(regex, lvs_line)

if match != None:
    raise ValueError("LVS failed!")
else:
    print("LVS is clean!")

json_filename = "test.json"

if check_gen_files(json_filename, (len(sys.argv) == 1)):
        print("Flow check is clean!")
else:
    print("Flow check failed!")