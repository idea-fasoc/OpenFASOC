import sys

sys.stdout.flush()

if len(sys.argv) == 1 or sys.argv[1] == "sky130hvl_ldo":
    drc_filename = "work/6_final_drc.rpt"
    lvs_filename = "work/6_final_lvs.rpt"
else:
    drc_filename = "work/"+sys.argv[1]+"/6_final_drc.rpt"
    lvs_filename = "work/"+sys.argv[1]+"/6_final_lvs.rpt"


if len(sys.argv) > 1 and sys.argv[1] == "sky130hvl_ldo":
    with open(drc_filename, 'r') as f1, open("../../../.github/scripts/expected_drc_reports/expected_ldo_drc.rpt", 'r') as f2:
        content1 = f1.readlines()
        content2 = f2.readlines()
        if content1 == content1:
            print("DRC is clean!")
        else:
            raise ValueError("DRC failed!")
        
elif sum(1 for line in open(drc_filename)) > 3:
    raise ValueError("DRC failed!")
else:
    print("DRC is clean!")


with open(lvs_filename) as f:
    f1 = f.read()

    if "failed" in f1:
        raise ValueError("LVS failed!")
    else:
        print("LVS is clean!")
