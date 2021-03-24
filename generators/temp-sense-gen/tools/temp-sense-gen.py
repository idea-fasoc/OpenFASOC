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

shutil.copyfile(srcDir + 'TEMP_ANALOG_lv.nl.v', flowDir + 'design/src/tempsense/TEMP_ANALOG_lv.nl.v')
shutil.copyfile(srcDir + 'TEMP_ANALOG_hv.nl.v', flowDir + 'design/src/tempsense/TEMP_ANALOG_hv.nl.v')
shutil.copyfile(srcDir + 'TEMP_AUTO_def.v', flowDir + 'design/src/tempsense/TEMP_AUTO_def.v')
shutil.copyfile(srcDir + 'tempsenseInst.v', flowDir + 'design/src/tempsense/tempsenseInst.v')
shutil.copyfile(srcDir + 'counter.v', flowDir + 'design/src/tempsense/counter' + '.v')

print('#----------------------------------------------------------------------')
print('# Verilog Generated')
print('#----------------------------------------------------------------------')
print()
if args.mode == 'verilog':
  print("Exiting tool....")
  #sys.exit(1)
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
shutil.copytree(flowDir + 'results/' + args.platform + '/tempsense', genDir + args.outputDir)
shutil.copyfile(flowDir + 'reports/' + args.platform + '/tempsense/6_final_drc.rpt', genDir + args.outputDir + '/6_final_drc.rpt')
shutil.copyfile(flowDir + 'reports/' + args.platform + '/tempsense/6_final_lvs.rpt', genDir + args.outputDir + '/6_final_lvs.rpt')


time.sleep(2)

sys.exit(0)

