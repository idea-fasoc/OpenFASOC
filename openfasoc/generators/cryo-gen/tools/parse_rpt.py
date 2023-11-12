import re
import subprocess
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common.check_gen_files import check_gen_files

_generator_is = {
    'sky130hvl_ldo': 0, 
    'sky130hd_temp': 0, 
    'sky130XX_cryo': 1
}

dir_path = r'flow/reports'
lib = os.listdir(dir_path)
cryo_library = str(lib[0])

drc_filename = "flow/reports/" + cryo_library + "/cryo/6_final_drc.rpt"
num_lines = sum(1 for line in open(drc_filename))

if num_lines > 3:
    raise ValueError("DRC failed!")
else:
    print("DRC is clean!")

lvs_filename = "flow/reports/" + cryo_library + "/cryo/6_final_lvs.rpt"
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

if check_gen_files(json_filename, _generator_is, cryo_library):
        print("Flow check is clean!")
else:
  print("Flow check failed!")