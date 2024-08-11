import numpy as np
import glayout_import

from sky130_nist_tapeout import safe_single_build_and_simulation
from sky130_nist_tapeout import opamp_parameters_serializer
#from tapeout_and_RL.sky130_nist_tapeout import single_build_and_simulation
#from tapeout_and_RL.sky130_nist_tapeout import opamp_parameters_serializer
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

#params_idx = np.array([1, 5, 3, 5, 2, 1, 6, 0, 6, 5, 5, 1, 1, 3, 2, 0])

#[ 6.   1.   4.   6.   2.   4.   7.2  1.  10.   3.   8.   2.  12.   3.
#  5.   1.  16.   6.   2.   4.   6.   1.   6.  12.  12.   3.   2. ]

#[4.  1.  8.  6.  3.  3.  4.  0.5 4.  6.  2.  4.  2.  6.  8.  3. ]

#[ 4.   1.   8.   6.   3.   3.   4.   0.5  4.   3.   6.   2.   4.   2.
#  5.   1.  16.   6.   2.   4.   6.   1.   8.  12.  12.   3.   2. ]

#[4.  1.  8.  6.  3.  3.  4.  0.5 4.  6.  2.  4.  2.  6.  8.  3. ]

#[ 7. ,  0.7, 12. ,  7. ,  1. , 10. ,  8. ,  0.5, 12. ,  3. ,  7. ,
#        1. , 12. ,  2. ,  5. ,  1. , 16. ,  6. ,  2. ,  4. ,  9. ,  0.5,
#        6. , 12. , 12. ,  3. ,  2. ]

# [ 7. ,  0.7,  8. ,  7. ,  1. ,  8. ,  8. ,  0.5, 12. ,  3. ,  7. ,
#         1. , 16. ,  2. ,  5. ,  1. , 16. ,  6. ,  2. ,  4. ,  9. ,  0.5,
#         8. , 12. , 12. ,  3. ,  2. ])

#params_idx = np.array([6, 2, 11, 6, 0, 7, 7, 0, 10, 6, 5, 9, 0, 6, 2, 2])

params_idx = np.array([6, 2, 7, 6, 0, 5, 7, 0, 10, 6, 5, 13, 0, 6, 4, 2])

# params_idx = np.array([5, 5, 3, 5, 2, 1, 6, 1, 8, 7, 15, 9, 1, 3, 2, 2])

for value in params.values():
    param_vec = np.arange(value[0], value[1], value[2])
    paramss.append(param_vec)

paramsss = np.array([paramss[i][params_idx[i]] for i in range(len(params_id))])
#param_val = np.array[OrderedDict(list(zip(self.params_id,params)))]

#run param vals and simulate
#cur_specs = OrderedDict(sorted(self.sim_env.create_design_and_simulate(param_val[0])[1].items(), key=lambda k:k[0]))
#2.69966400e+07

#inputparam = np.array([ 9.  , 2.,  6. ,  6.,   2. ,  4.  , 6.,   1. ,  2.  , 3. ,  7.  , 1  ,6.  , 3. ,12.  ,12.  , 3. ,  2. ])
#[ 4.   1.   8.   6.   3.   3.   4.   0.5  4.   3.   6.   2.   4.   2.
#  5.   1.  16.   6.   2.   4.   6.   1.   8.  12.  12.   3.   2. ]

#[4.  1.  8.  6.  3.  3.  4.  0.5 4.  6.  2.  4.  2.  6.  8.  3. ]

inputparam = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 5.0, 1.0, 16.0, 6.0, 2.0, 4.0, 0.0, 0.5, 0.0, 12.0, 12.0, 0.0, 2.0])
inputparam[0:3] = paramsss[0:3]
inputparam[3:6] = paramsss[3:6]
inputparam[6:9] = paramsss[6:9]
inputparam[10:14] = paramsss[9:13]
inputparam[20] = paramsss[13]
inputparam[22] = paramsss[14]
inputparam[25] = paramsss[15]

# params = {
#     "half_diffpair_params": (6, 1, 4),
#     "diffpair_bias": (6, 2, 4),
#     "half_common_source_params": (7.2, 1, 10, 3),
#     "half_common_source_bias": (8, 2, 12, 3),
#     "output_stage_params": (5, 1, 16),
#     "output_stage_bias": (6, 2, 4),
#     "mim_cap_size": (12, 12),
#     "mim_cap_rows": 3,
#     "rmult": 2
# }
# numpy_params = opamp_parameters_serializer(**params)
#numpy_params[0:3] = paramsss[0:3]
#numpy_params[3:6] = paramsss[3:6]
#numpy_params[6:9] = paramsss[6:9]
#numpy_params[10:14] = paramsss[9:13]
#numpy_params[20] = paramsss[13]
# numpy_params[22] = paramsss[14]
# numpy_params[25] = paramsss[15]

# print(numpy_params)
print(inputparam)

#{'ugb': 2233790.0, 'dcGain': 65.19988, 'phaseMargin': 104.0, 'Ibias_diffpair': 1e-06, 'Ibias_commonsource': 2.0736e-06, 'Ibias_output': 9.35e-05, 'area': 47939.75594998075, 'power': 0.000353842085, 'noise': 5.22616086, 'bw_3db': 831.1834, 'power_twostage': 1.72420852e-05}
#726766657990.63

# supposed to be 10MHz
#numpy_params = np.array([ 7. ,  0.7, 12. ,  7. ,  1. , 10. ,  8. ,  0.5, 12. ,  3. ,  7. ,
#        1. , 12. ,  2. ,  5. ,  1. , 16. ,  6. ,  2. ,  4. ,  9. ,  0.5,
#        6. , 12. , 12. ,  3. ,  2. ])
#{'ugb': 21067680.0, 'dcGain': 52.27519, 'phaseMargin': 96.0, 'Ibias_diffpair': 7.43008371e-06, 'Ibias_commonsource': 2.21861111e-05, 'Ibias_output': 9.35e-05, 'area': 42865.81769998964, 'power': 0.00049207212, 'noise': 4.18722441, 'bw_3db': 27197.53, 'power_twostage': 0.00015547212}
#711356747048.626

# supposed to be 25459060
numpy_params = np.array([ 7. ,  0.7,  8. ,  7. ,  1. ,  8. ,  8. ,  0.5, 12. ,  3. ,  7. ,
        1. , 16. ,  2. ,  5. ,  1. , 16. ,  6. ,  2. ,  4. ,  9. ,  0.5,
        8. , 12. , 12. ,  3. ,  2. ])
result = safe_single_build_and_simulation(inputparam, hardfail=True)
# {'ugb': 13847390.0, 'dcGain': 50.5001, 'phaseMargin': 101.0, 'Ibias_diffpair': 6.19173642e-06, 'Ibias_commonsource': 1.54070216e-05, 'Ibias_output': 9.35e-05, 'area': 43918.335699987125, 'power': 0.000449201424, 'noise': 3.90373916, 'bw_3db': 25231.79, 'power_twostage': 0.000112601424}
# 641119734161.4553
print(result)
print(result["ugb"]/(result["Ibias_diffpair"]+result["Ibias_commonsource"]))