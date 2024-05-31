import sys, os
from sky130_nist_tapeout import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from glayout.flow.components.opamp import opamp
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130

params = {
    "half_diffpair_params": (6, 1, 4),
    "diffpair_bias": (6, 2, 4),
    "half_common_source_params": (7.2, 1, 10, 3),
    "half_common_source_bias": (8, 2, 12, 3),
    "output_stage_params": (5, 1, 16),
    "output_stage_bias": (6, 2, 4),
    "mim_cap_size": (12, 12),
    "mim_cap_rows": 3,
    "rmult": 2
}
results = single_build_and_simulation(opamp_parameters_serializer(**params), 25, cload=0, noparasitics=False, hardfail=True)

print(results)
with open('result_file.txt', 'w'):
    for result in results:
        print(result, file='result_file.txt')