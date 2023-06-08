import sys

if len(sys.argv) == 1:
    drc_filename = "work/6_final_drc.rpt"
else:
    drc_filename = "work/" + sys.argv[1] + "/6_final_drc.rpt"


if len(sys.argv) == 1:
    lvs_filename = "work/6_final_lvs.rpt"
else:
    lvs_filename = "work/" + sys.argv[1] + "/6_final_lvs.rpt"


num_lines = sum(1 for line in open(drc_filename))

if num_lines > 3:
    raise ValueError("DRC failed!")
else:
    print("DRC is clean!")


with open(lvs_filename) as f:
    f1 = f.read()

    if "failed" in f1:
        raise ValueError("LVS failed!")
    else:
        print("LVS is clean!")
