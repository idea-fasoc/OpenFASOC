import os
import sys
import re
import subprocess as sp
from gdsfactory.component import Component

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '.github', 'scripts'))

from glayout.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.pdk.gf180_mapped import gf180_mapped_pdk as gf180
from glayout.components.diff_pair import diff_pair
from glayout.primitives.fet import  nmos, pmos
from glayout.components.opamp import opamp

from run_glayout_drc import place_component

# ###########################################################################################################
# ###########################################################################################################
def get_gds_netlist(component_name, func, pdk, gds_path):
    component = place_component(component_name, func, pdk)
    component.write_gds(gds_path)
    netlist = component.info['netlist'].generate_netlist()
    return netlist, component


def compname_in_net(mynet: str) -> str:
    pattern_diff = re.compile(r'\bDIFF_PAIR\b')
    pattern_nmos = re.compile(r'\bNMOS\b')
    pattern_pmos = re.compile(r'\bPMOS\b')
    pattern_opamp = re.compile(r'\bopamp\b')
    patterns = [pattern_diff, pattern_nmos, pattern_pmos, pattern_opamp]
    replacements = ['diff_test', 'nmos_test', 'pmos_test', 'opamp_test']

    for i, pattern in enumerate(patterns):
        if pattern.search(mynet):
            replacement = replacements[i]
            mynet = re.sub(pattern, replacement, mynet)  
    return mynet
        
def edit_lvs_script(lvs_script: str, comp: Component, revert_flag: bool):
    with open(lvs_script, 'r', encoding='utf-8') as rf:
        data = rf.read()
    print(f'Editing lvs script: {lvs_script}')
    pattern = re.compile(r'\{\!\[string compare \$2 "(.*?)"\]\}')
    matches = pattern.findall(data)

    to_replace = matches[0]
    if not revert_flag:
        to_replace_with = comp.name
    else: 
        to_replace_with = 'ldoInst'

    data = re.sub(to_replace, to_replace_with, data)
    print(f'Edited lvs script: {data}')
    with open(lvs_script, 'w', encoding='utf-8') as wf:
        wf.write(data)
        

def edit_makefile(comp: Component, makefile_path: str):
    pattern = re.compile(r'export DESIGN_NAME = (.*)_test')
    my_var = comp.name

    with open(makefile_path, 'r') as rf:
        data = rf.read()

    new_content = re.sub(pattern, f'export DESIGN_NAME = {my_var}', data)

    with open(makefile_path, 'w') as wf:
        wf.write(new_content)
######################################################################################################################################################################################################################   
######################################################################################################################################################################################################################


gds_path = './results/sky130hd/glayout/6_final.gds'
cdl_path = './results/sky130hd/glayout/6_final.cdl'
makefile_script = './Makefile'

## PMOS
mynet, comp = get_gds_netlist('pmos_test', pmos, sky130, gds_path)

net_file = cdl_path
mynet = compname_in_net(mynet)
with open(net_file, 'w') as wf:
    wf.write(mynet)
    
edit_makefile(comp, makefile_script)

subproc_cmd = ['make', 'netgen_lvs']
sub = sp.Popen(subproc_cmd, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
stdout, stderr = sub.communicate()

print(stdout)

if sub.returncode != 0:
    print(f'LVS failed for pmos_test with error:\n {stderr}')
else:
    print(f'LVS run successful for pmos_test')

## NMOS
mynet, comp = get_gds_netlist('nmos_test', nmos, sky130, gds_path)

net_file = cdl_path
mynet = compname_in_net(mynet)
with open(net_file, 'w') as wf:
    wf.write(mynet)
    
edit_makefile(comp, makefile_script)

subproc_cmd = ['make', 'netgen_lvs']
sub = sp.Popen(subproc_cmd, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
stdout, stderr = sub.communicate()

print(stdout)

if sub.returncode != 0:
    print(f'LVS failed for nmos_test with error:\n {stderr}')
else:
    print(f'LVS run successful for nmos_test')
    
## DIFF_PAIR
mynet, comp = get_gds_netlist('diff_test', diff_pair, sky130, gds_path)

net_file = cdl_path
mynet = compname_in_net(mynet)
with open(net_file, 'w') as wf:
    wf.write(mynet)
    
edit_makefile(comp, makefile_script)

subproc_cmd = ['make', 'netgen_lvs']
sub = sp.Popen(subproc_cmd, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
stdout, stderr = sub.communicate()

print(stdout)

if sub.returncode != 0:
    print(f'LVS failed for diff_test with error:\n {stderr}')
else:
    print(f'LVS run successful for diff_test')
    
## OPAMP
mynet, comp = get_gds_netlist('opamp_test', opamp, sky130, gds_path)

net_file = cdl_path
mynet = compname_in_net(mynet)
with open(net_file, 'w') as wf:
    wf.write(mynet)
    
edit_makefile(comp, makefile_script)

subproc_cmd = ['make', 'netgen_lvs']
sub = sp.Popen(subproc_cmd, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
stdout, stderr = sub.communicate()

print(stdout)

if sub.returncode != 0:
    print(f'LVS failed for opamp_test with error:\n {stderr}')
else:
    print(f'LVS run successful for opamp_test')