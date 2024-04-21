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

from run_glayout_drc import place_component, setup_pdk_dir

# ###########################################################################################################
# ###########################################################################################################
def get_gds_netlist(component_name, func, pdk, gds_path):
    """used to return the netlist and component object for the 
    desired component's placement

    Args:
        component_name (str): the global descriptor for the instantiated component
        func (callable[[Component], any]): the function to be called to generate the component
        pdk (MappedPDK): the pdk object for which the component is to be generated
        gds_path (str): the path to the generated gds file

    Returns:
        Component: the instance of the component
        str: the netlist string
    """
    component = place_component(component_name, func, pdk)
    component.write_gds(gds_path)
    netlist = component.info['netlist'].generate_netlist()
    return netlist, component


def compname_in_net(mynet: str) -> str:
    """used to edit netlist to change the component name to 
    the test component name for global definition

    Args:
        mynet (str): the netlist string input

    Returns:
        str: the modified netlist string
    """
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

def edit_makefile(comp: Component, makefile_path: str):
    """used to edit the makefile to change the DESIGN_NAME variable
    according to the component name

    Args:
        comp (Component): the component object for which the makefile is to be edited
        makefile_path (str): the string path to the makefile
    """
    pattern = re.compile(r'export DESIGN_NAME = (.*)_test')
    my_var = comp.name

    with open(makefile_path, 'r') as rf:
        data = rf.read()

    new_content = re.sub(pattern, f'export DESIGN_NAME = {my_var}', data)

    with open(makefile_path, 'w') as wf:
        wf.write(new_content)
    
def evaluate_report(report_fle: str) -> bool:
    """used to evaluate the lvs report file

    Args:
        report_fle (str): the path to the lvs report file (6_final_lvs.rpt)

    Returns:
        bool: The flag indicating if the lvs run was successful
    """
    with open(report_fle, 'r') as file:
        report_content = file.read()

    string1 = 'Cell pin lists are equivalent.'
    string2 = 'Netlists match with'
    
    if string1 in report_content and string2 in report_content:
        return True
    return False
######################################################################################################################################################################################################################   
######################################################################################################################################################################################################################
os.system('mkdir -p ./reports/sky130hd/glayout')

gds_path = './results/sky130hd/glayout/6_final.gds'
cdl_path = './results/sky130hd/glayout/6_final.cdl'
report_path = './reports/sky130hd/glayout/6_final_lvs.rpt'
makefile_script = './Makefile'

setup_pdk_dir('sky130')
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

report_return_code = evaluate_report(report_path)

if report_return_code:
    print(f'LVS run successful for pmos_test')
else:
    print(f'LVS failed for pmos_test!')
    sys.exit(1)

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

report_return_code = evaluate_report(report_path)

if report_return_code:
    print(f'LVS run successful for nmos_test')
else:
    print(f'LVS failed for nmos_test!')
    sys.exit(1)
    
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

report_return_code = evaluate_report(report_path)

if report_return_code:
    print(f'LVS run successful for diff_test')
else:
    print(f'LVS failed for diff_test!')
    sys.exit(1)
    
## OPAMP
##### not using currently because not LVS clean
# mynet, comp = get_gds_netlist('opamp_test', opamp, sky130, gds_path)

# net_file = cdl_path
# mynet = compname_in_net(mynet)
# with open(net_file, 'w') as wf:
#     wf.write(mynet)
    
# edit_makefile(comp, makefile_script)

# subproc_cmd = ['make', 'netgen_lvs']
# sub = sp.Popen(subproc_cmd, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
# stdout, stderr = sub.communicate()

# print(stdout)

# if sub.returncode != 0:
#     print(f'LVS failed for opamp_test with error:\n {stderr}')
# else:
#     print(f'LVS run successful for opamp_test')