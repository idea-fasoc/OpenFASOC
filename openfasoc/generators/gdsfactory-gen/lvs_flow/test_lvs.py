import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from glayout.primitives.fet import nmos
from glayout.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.components.diff_pair import diff_pair
from glayout.components.opamp import opamp
from glayout.primitives.fet import  nmos, pmos
import subprocess as sp
import re

# mynet = mynet.replace('opamp', 'opamp_test')
# mynet = mynet.replace('PMOS', 'pmos_test')
# mynet = mynet.replace('NMOS', 'nmos_test')
lvs_script = './../../../common/drc-lvs-check/run_lvspex.sh'
gds_path = './results/sky130hd/glayout/6_final.gds'
cdl_path = './results/sky130hd/glayout/6_final.cdl'
makefile_script = './Makefile'


mymos = diff_pair(sky130)
mymos.name = 'diff_test'
mymos.write_gds(gds_path)
mynet = mymos.info['netlist'].generate_netlist()
print(mynet)

pattern_diff = re.compile(r'\bDIFF_PAIR\b')
pattern_nmos = re.compile(r'\bNMOS\b')
pattern_pmos = re.compile(r'\bPMOS\b')
patterns = [pattern_diff, pattern_nmos, pattern_pmos]
replacements = ['diff_test', 'nmos_test', 'pmos_test']

for i, pattern in enumerate(patterns):
    if pattern.search(mynet):
        replacement = replacements[i]
        mynet = re.sub(pattern, replacement, mynet)
        
        
with open(lvs_script, 'r') as rf:
    data = rf.read()
    
pattern = re.compile(r'\{\!\[string compare \$2 "(.*?)"\]\}')
matches = pattern.findall(data)
save = matches[0]

to_replace = matches[0]
to_replace_with = mymos.name

data = re.sub(to_replace, to_replace_with, data)

with open(lvs_script, 'w') as wf:
    wf.write(data)

net_file = cdl_path

with open(net_file, 'w') as wf:
    wf.write(mynet)
    
pattern = re.compile(r'export DESIGN_NAME = (.*)_test')
my_var = mymos.name

with open(makefile_script, 'r') as rf:
    data = rf.read()

new_content = re.sub(pattern, f'export DESIGN_NAME = {my_var}', data)

with open(makefile_script, 'w') as wf:
    wf.write(new_content)
    
subproc_cmd = ['make', 'netgen_lvs']
sub = sp.Popen(subproc_cmd, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
stdout, stderr = sub.communicate()

print(stdout)

if sub.returncode != 0:
    print('Error:', stderr)

    

# data = data.replace('nmos_test', mymos.name)
# with open(lvs_script, 'w') as wf:
#     wf.write(data)




# mymos = nmos(sky130)
# mymos.name = 'nmos_test'
# mymos.write_gds('../temp-sense-gen/flow/results/sky130hd/tempsense/6_final.gds')
# mynet = mymos.info['netlist'].generate_netlist()
# print(mynet)
# mynet = mynet.replace('NMOS', 'nmos_test')

# string_to_replace = 'export DESIGN_NAME = diff_test'
# string_to_replace_with = 'export DESIGN_NAME = ' + mymos.name
# data = data.replace(string_to_replace, string_to_replace_with)



# mydiff = opamp(sky130)
# mydiff.name = 'opamp_test'
# mydiff.write_gds('../temp-sense-gen/flow/results/sky130hd/tempsense/6_final.gds')

# mynet = mydiff.info['netlist'].generate_netlist()
# mynet = mynet.replace('DIFF_PAIR', 'diff_test')