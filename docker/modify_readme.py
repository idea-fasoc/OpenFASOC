#!/bin/python3

#open the README and tools.json file in read mode
fversions = open("versions.txt",'r')
fin = open("README.md", "rt")
data = fin.readlines()
data_mod=""
j=0

for i in fversions:

for i in data:
    if j <= len(tools)-1:
        if str(tools[j][0]) in i :
            i=i.split("version:")[0]+"version:%s"%tools[j][1]+")\n"
            j=j+1

    data_mod=data_mod+i


#open the README file in write mode
fin = open("README.md", "wt")
fin.write(data_mod)
fin.close()

