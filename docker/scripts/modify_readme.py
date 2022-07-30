#!/bin/python3
home = "/home/runner/work/OpenFASOC/OpenFASOC"
readme = home + "/README.rst"

# Open the README file, indentify the respective tool lines and replace the versions accordingly
fversions = open("versions.txt", "r")
tools = []
for i in fversions:
    tools.append([i.split(" ")[0].strip(), i.split(" ")[2].strip()])


fin = open(readme, "rt")
data = fin.readlines()
data_mod = ""
j = 0
for i in data:
    for j in range(len(tools)):
        if str(tools[j][0]) + ">" in i:
            print(str(tools[j][0]))
            i = i.split("version:")[0] + "version:%s" % tools[j][1] + ")\n"

    data_mod = data_mod + i


# open the README file in write mode
fin = open(readme, "wt")
fin.write(data_mod)
fin.close()
