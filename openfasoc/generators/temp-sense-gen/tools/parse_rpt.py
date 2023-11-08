import os, sys 

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common.check_gen_files import check_gen_files

drc_filename = "flow/reports/sky130hd/tempsense/6_final_drc.rpt"
num_lines = sum(1 for line in open(drc_filename))

if num_lines > 3:
    raise ValueError("DRC failed!")
else:
    print("DRC is clean!")


lvs_filename = "flow/reports/sky130hd/tempsense/6_final_lvs.rpt"

with open(lvs_filename) as f:
    f1 = f.read()

    if "failed" in f1:
        raise ValueError("LVS failed!")
    else:
        print("LVS is clean!")

json_filename = "test.json"

if os.path.exists(json_filename):
    if check_gen_files():
        print("Flow check is clean!")
    else:
        print("Flow check failed!")
else:
    raise ValueError(".json config file not found!")
