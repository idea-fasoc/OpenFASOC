#!/bin/python3

import json,os

#home=os.getenv("GITHUB_WORKSPACE")
home="/home/runner/work/OpenFASOC/OpenFASOC"
tools_json=home+"/.github/tools.json"
readme=home+"/README.rst"
#build the tools.json file with commit numbers
tools = []
with open("commits.txt") as f1:
    for i in f1:
        if i != "\n":
            tools.append([i.split(":")[0],i.split(":")[1].strip()])

with open(tools_json, "w") as outfile:
    outfile.write(json.dumps(tools,indent=4, separators=(", ", " : ")))


#open the README and tools.json file in read mode
fjson = open(tools_json,'r')
tools=json.load(fjson)
fin = open(readme, "rt")
data = fin.readlines()
data_mod=""
j=0
for i in data:
    if j <= len(tools)-1:
        if str(tools[j][0]) in i :
            i=i.split("commit-id")[0]+"commit-id:%s"%tools[j][1]+")\n"
            j=j+1

    data_mod=data_mod+i


#open the README file in write mode
fin = open(readme, "wt")
fin.write(data_mod)
fin.close()

