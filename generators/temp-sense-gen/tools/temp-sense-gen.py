import sys
import getopt
import math
import subprocess as sp
import fileinput
import re
import shutil
import numpy as np
import argparse
import json
import glob

import operator
import TEMP_netlist
import readparamgen
import os
import time
from readparamgen import check_search_done, designName, args, jsonSpec


genDir = os.path.join(os.path.dirname(os.path.relpath(__file__)),"../")
srcDir = genDir + "src/"
flowDir = genDir + "flow/"
designDir = genDir + "designs/src/tempsense/"
simDir = genDir + "simulations/"

#------------------------------------------------------------------------------
# Clean the workspace
#------------------------------------------------------------------------------
print('#----------------------------------------------------------------------')
print('# Cleaning the workspace...')
print('#----------------------------------------------------------------------')
if (args.clean):
  p = sp.Popen(['make','clean_all'], cwd=genDir)
  p.wait()


temp, power, error, ninv, nhead, hist = check_search_done()

print ('Error : ' , error)
print('Inv : ' , ninv)
print('Header : ' , nhead)
print('History : ' , hist)
print("INV:{0}\nHEADER:{1}\n".format(ninv,nhead))

if args.ninv:
  print("target number of inverters: " + args.ninv)
  ninv = int(args.ninv)

if args.nhead:
  print("target number of headers: " + args.nhead)
  nhead = int(args.nhead)


print('#----------------------------------------------------------------------')
print('# Verilog Generation')
print('#----------------------------------------------------------------------')


if args.platform == 'sky130hd':
  aux1 = 'sky130_fd_sc_hd__nand2_1'
  aux2 = 'sky130_fd_sc_hd__inv_1'
  aux3 = 'sky130_fd_sc_hd__buf_1'
  aux4 = 'sky130_fd_sc_hd__buf_1'
  aux5 = 'HEADER'
  aux6 = 'SLC'
elif args.platform == 'sky130hs':
  aux1 = 'sky130_fd_sc_hs__nand2_1'
  aux2 = 'sky130_fd_sc_hs__inv_1'
  aux3 = 'sky130_fd_sc_hs__buf_1'
  aux4 = 'sky130_fd_sc_hs__buf_1'
  aux5 = 'HEADER_hs'
  aux6 = 'SLC_hs'

ninv=ninv+1
TEMP_netlist.gen_temp_netlist(ninv,nhead,aux1,aux2,aux3,aux4,aux5, srcDir)

with open(srcDir + 'TEMP_ANALOG_hv.nl.v', 'r') as rf:
    filedata = rf.read()
header_list = re.findall('HEADER\s+(\w+)\(', filedata)
with open(genDir + 'blocks/sky130hd/tempsenseInst_custom_net.txt', 'w') as wf:
    wf.write('r_VIN\n')
    for header_cell in header_list:
        wf.write('temp_analog_1.' + header_cell + ' VIN\n')

with open(srcDir + 'TEMP_ANALOG_lv.nl.v', 'r') as rf:
    filedata = rf.read()
lv_list = re.findall('\nsky130_fd_sc\w*\s+(\w+)\s+\(', filedata)
with open(genDir + 'blocks/sky130hd/tempsenseInst_domain_insts.txt', 'w') as wf:
    for lv_cell in lv_list:
        wf.write('temp_analog_0.' + lv_cell + '\n')

with open(srcDir + 'tempsenseInst.v', 'r') as rf:
    filedata = rf.read()
    filedata = re.sub('module\s*(\w+)\s*\n', 'module ' + designName + '\n', filedata)
with open(srcDir + 'tempsenseInst.v', 'w') as wf:
    wf.write(filedata)

with open(flowDir + 'design/sky130hd/tempsense/config.mk', 'r') as rf:
    filedata = rf.read()
    filedata = re.sub('export DESIGN_NAME\s*=\s*(\w+)', 'export DESIGN_NAME = ' + designName, filedata)
with open(flowDir + 'design/sky130hd/tempsense/config.mk', 'w') as wf:
    wf.write(filedata)

shutil.copyfile(srcDir + 'TEMP_ANALOG_lv.nl.v', flowDir + 'design/src/tempsense/TEMP_ANALOG_lv.nl.v')
shutil.copyfile(srcDir + 'TEMP_ANALOG_hv.nl.v', flowDir + 'design/src/tempsense/TEMP_ANALOG_hv.nl.v')
shutil.copyfile(srcDir + 'TEMP_AUTO_def.v', flowDir + 'design/src/tempsense/TEMP_AUTO_def.v')
shutil.copyfile(srcDir + 'tempsenseInst.v', flowDir + 'design/src/tempsense/' + designName + '.v')
shutil.copyfile(srcDir + 'counter.v', flowDir + 'design/src/tempsense/counter' + '.v')

print('#----------------------------------------------------------------------')
print('# Verilog Generated')
print('#----------------------------------------------------------------------')
print()
if args.mode == 'verilog':
  print("Exiting tool....")
  exit()

print('#----------------------------------------------------------------------')
print('# Run Synthesis and APR')
print('#----------------------------------------------------------------------')

p = sp.Popen(['make','finish'], cwd=flowDir)
p.wait()


print('#----------------------------------------------------------------------')
print('# Place and Route finished')
print('#----------------------------------------------------------------------')

time.sleep(2)

p = sp.Popen(['make','magic_drc'], cwd=flowDir)
p.wait()

print('#----------------------------------------------------------------------')
print('# DRC finished')
print('#----------------------------------------------------------------------')

time.sleep(2)

p = sp.Popen(['make','netgen_lvs'], cwd=flowDir)
p.wait()


print('#----------------------------------------------------------------------')
print('# LVS finished')
print('#----------------------------------------------------------------------')

if os.path.isdir(args.outputDir):
    shutil.rmtree(genDir + args.outputDir)
os.mkdir(genDir + args.outputDir)
shutil.copyfile(flowDir + 'results/' + args.platform + '/tempsense/6_final.gds', genDir + args.outputDir + '/' + designName + '.gds')
shutil.copyfile(flowDir + 'results/' + args.platform + '/tempsense/6_final.def', genDir + args.outputDir + '/' + designName + '.def')
shutil.copyfile(flowDir + 'results/' + args.platform + '/tempsense/6_final.v', genDir + args.outputDir + '/' + designName + '.v')
shutil.copyfile(flowDir + 'results/' + args.platform + '/tempsense/6_1_fill.sdc', genDir + args.outputDir + '/' + designName + '.sdc')
shutil.copyfile(flowDir + designName + '.spice', genDir + args.outputDir + '/' + designName + '.spice')
shutil.copyfile(flowDir + designName + '_pex.spice', genDir + args.outputDir + '/' + designName + '_pex.spice')
shutil.copyfile(flowDir + 'reports/' + args.platform + '/tempsense/6_final_drc.rpt', genDir + args.outputDir + '/6_final_drc.rpt')
shutil.copyfile(flowDir + 'reports/' + args.platform + '/tempsense/6_final_lvs.rpt', genDir + args.outputDir + '/6_final_lvs.rpt')


time.sleep(2)

print('#----------------------------------------------------------------------')
print('# Macro Generated')
print('#----------------------------------------------------------------------')
print()
if args.mode == 'macro':
  print("Exiting tool....")
  #sys.exit(1)
  exit()

print("Loading platform_config file...")
print()
try:
  with open(genDir + '../../common/platform_config.json') as file:
    jsonConfig = json.load(file)
except ValueError as e:
  print("Error occurred opening or loading json file.")
  print >> sys.stderr, 'Exception: %s' % str(e)
  sys.exit(1)

platform_config = jsonConfig["platforms"][args.platform]
nominal_voltage = platform_config["nominal_voltage"]
model_file = platform_config["model_file"] 
model_corner = platform_config["model_corner"]

stage_var = int(ninv) - 1
header_var = int(nhead)

runDir = simDir + "inv{:d}_header{:d}/".format(stage_var, header_var)
if os.path.isdir(runDir):
  shutil.rmtree(runDir)
os.mkdir(runDir)

shutil.copyfile(flowDir + designName + '.spice', runDir + designName + '.spice')
shutil.copyfile(flowDir + designName + '_pex.spice', runDir + designName + '_pex.spice')
shutil.copyfile(genDir + "tools/result.py", runDir + "result.py")
shutil.copyfile(genDir + "tools/result_error.py", runDir + "result_error.py")


temp_start = -20
temp_stop = 100
temp_step = 20

temp_points = int((temp_stop - temp_start) / temp_step)+1

temp_list=[]
for i in range(0, temp_points+1):
   temp_list.append(temp_start + i*temp_step)


with open(genDir + "tools/tempsenseInst_sim.sp", "r") as rf:
  filedata = rf.read()
  filedata = re.sub("@model_file", model_file, filedata)
  filedata = re.sub("@model_corner", model_corner, filedata)
  filedata = re.sub("@voltage", str(nominal_voltage), filedata)
  filedata = re.sub("@netlist", os.path.abspath(runDir + designName + '.spice'), filedata)

for temp in temp_list:
  w_file = open(simDir + "inv%d_header%d/%s_%d.sp" % (stage_var, header_var, designName, temp), "w")
  wfdata = re.sub("@temp", str(temp), filedata)
  w_file.write(wfdata)
  w_file.close()

with open(runDir + "run_sim", "w") as wf:
  for temp in temp_list:
    wf.write("ngspice -b %s_%d.sp &\n" % (designName, temp))

print("Exiting tool....")
exit()
