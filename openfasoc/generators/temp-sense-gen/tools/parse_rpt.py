import os, sys 

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common.check_gen_files import check_gen_files

_generator_is = {
    'sky130hvl_ldo': 0, 
    'sky130hd_temp': 1, 
    'sky130XX_cryo': 0
}

drc_filename = "work/6_final_drc.rpt"
num_lines = sum(1 for line in open(drc_filename))

if num_lines > 3:
    raise ValueError("DRC failed!")
else:
    print("DRC is clean!")


lvs_filename = "work/6_final_lvs.rpt"

with open(lvs_filename) as f:
    f1 = f.read()

    if "failed" in f1:
        raise ValueError("LVS failed!")
    else:
        print("LVS is clean!")

json_filename = "test.json"

if check_gen_files(json_filename, _generator_is, " "):
        print("Flow check is clean!")
else:
    print("Flow check failed!")
