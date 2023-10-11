import re
import subprocess
import sys

drc_filename = "flow/reports/sky130hd/cyro/6_final_drc.rpt"
num_lines = sum(1 for line in open(drc_filename))

if num_lines > 3:
    raise ValueError("DRC failed!")
else:
    print("DRC is clean!")

lvs_filename = "flow/reports/sky130hd/cyro/6_final_lvs.rpt"
lvs_line = subprocess.check_output(["tail", "-1", lvs_filename]).decode(
    sys.stdout.encoding
)

regex = r"failed"
match = re.search(regex, lvs_line)

if match != None:
    raise ValueError("LVS failed!")
else:
    print("LVS is clean!")

with open('test.json', 'r') as file:
    data = json.load(file)

    module_name = data.get("module_name", "default")

    work_dir = "./work/"

    if (os.path.exists(work_dir) == 0):
        raise ValueError("work directory does not exist!")
    else:
        filename = work_dir + module_name
        for file in (filename + ".gds", filename + ".spice", filename + ".v", filename + ".def", filename + "_pex.spice", filename + ".sdc"):
            if (os.path.exists(file) == 0):
                raise ValueError(file + " does not exist!")
            
    for file in ("error_within_x.csv", "golden_error_opt.csv", "search_result.csv"):
        if os.path.exists(file) == 0:
            raise ValueError(file + " does not exist!")
