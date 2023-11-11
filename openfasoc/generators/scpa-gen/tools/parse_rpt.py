drc_filename = "flow/reports/sky130hd/scpa/6_final_drc.rpt"
num_lines = sum(1 for line in open(drc_filename))

if num_lines > 3:
    raise ValueError("DRC failed!")
else:
    print("DRC is clean!")

print("Generator check is clean!")
