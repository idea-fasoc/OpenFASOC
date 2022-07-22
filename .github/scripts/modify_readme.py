#!/bin/python3

import json

#build the tools.json file with commit numbers
tools = []
with open("commits.txt") as f1:
    for i in f1:
        if i != "\n":
            tools.append([i.split(":")[0],i.split(":")[1].strip()])

tools_json=

with open("tools.json", "w") as outfile:
    outfile.write(json.dumps(tools,indent=4, separators=(", ", " : ")))


#open the README and tools.json file in read mode
fjson = open("tools.json",'r')
tools=json.load(fjson)
fin = open("README.md", "rt")
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
fin = open("README.md", "wt")
fin.write(data_mod)
fin.close()

