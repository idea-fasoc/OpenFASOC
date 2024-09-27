import numpy as np
import glayout_import

from sky130_nist_tapeout import safe_single_build_and_simulation
from sky130_nist_tapeout import opamp_parameters_serializer

import yaml
from pathlib import Path
import numpy as np

params = {
                  "diffpair_params0" : [1, 8, 1],       
                  "diffpair_params1" : [0.5, 2.1, 0.1],   
                  "diffpair_params2" : [1, 13, 1],
                  "Diffpair_bias0" : [1, 8, 1],
                  "Diffpair_bias1" : [1, 4.5, 0.5],
                  "Diffpair_bias2" : [3, 13, 1],
                  "pamp_hparams0" : [1, 9, 1], 
                  "pamp_hparams1" : [0.5, 2.1, 0.1], 
                  "pamp_hparams2" : [2, 14, 1],
                  "bias0" : [1, 8, 1], 
                  "bias1" : [0.5, 2.1, 0.1], 
                  "bias2" : [3, 18, 1],
                  "bias3" : [2, 4, 1],
                  "half_pload1": [3, 10, 1],
                  "half_pload3": [4, 9, 1],
                  "mim_cap_rows" : [1, 4, 1],
                  }
paramss = []
params_id = list(params.keys())

params_idx = np.array([6, 2, 7, 6, 0, 5, 7, 0, 10, 6, 5, 13, 0, 6, 4, 2])

for value in params.values():
    param_vec = np.arange(value[0], value[1], value[2])
    paramss.append(param_vec)

paramsss = np.array([paramss[i][params_idx[i]] for i in range(len(params_id))])

inputparam = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 5.0, 1.0, 16.0, 6.0, 2.0, 4.0, 0.0, 0.5, 0.0, 12.0, 12.0, 0.0, 2.0])
inputparam[0:3] = paramsss[0:3]
inputparam[3:6] = paramsss[3:6]
inputparam[6:9] = paramsss[6:9]
inputparam[10:14] = paramsss[9:13]
inputparam[20] = paramsss[13]
inputparam[22] = paramsss[14]
inputparam[25] = paramsss[15]


result = safe_single_build_and_simulation(inputparam, hardfail=True)

print(result)
print(result["ugb"]/(result["Ibias_diffpair"]+result["Ibias_commonsource"]))
