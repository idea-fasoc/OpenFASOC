import re
import glob

wf = open("ModelFile", "w")

wf.write("Temp,Frequency,Power,Error,inv,header\n")
tcfiles = glob.glob("run/*")
for tcfile in tcfiles:
    pg = re.search("inv([0-9]+)_header([0-9]+)", tcfile)
    ninv = pg.group(1)
    nheader = pg.group(2)
    with open(tcfile + "/all_result", "r") as f:
        for line in f.readlines():
            prep_line = line[:-1] + ' ' + ninv + ' ' + nheader
            prep_line = prep_line.replace(' ', ',')
            wf.write(prep_line+"\n")
