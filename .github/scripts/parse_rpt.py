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
