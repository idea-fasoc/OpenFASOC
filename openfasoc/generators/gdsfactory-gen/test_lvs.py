from glayout.primitives.fet import nmos
from glayout.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.components.diff_pair import diff_pair
import re

mydiff = diff_pair(sky130)
mydiff.name = 'diff_test'
mydiff.write_gds('../temp-sense-gen/flow/results/sky130hd/tempsense/6_final.gds')

mynet = mydiff.info['netlist'].generate_netlist()
print(type(mynet))
mynet = mynet.replace('DIFF_PAIR', 'diff_test')

# mynet = re.sub(mynet, 'DIFF_PAIR', 'diff_test')
net_file = '../temp-sense-gen/flow/results/sky130hd/tempsense/6_final.cdl'
with open(net_file, 'w') as wf:
    wf.write(mynet)
