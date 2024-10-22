import numpy as np
import glayout_import
import sys 

from sky130_nist_tapeout import safe_single_build_and_simulation
from sky130_nist_tapeout import opamp_parameters_serializer

import yaml
from pathlib import Path
import numpy as np
from typing import Union

def get_indices_from_ranges(opamp_parameters: Union[dict, np.array]) -> np.array:
	"""The RL framework works by doing design searches within a user defined range for each parameter
	For example, the RL framework may be told to search diffpair widths between 1um and 8um in steps of 1um
	In this case, the RL framework will only ever try to make opamps with diff pair width one of [1,2,3,4,5,6,7,8]
	this is done to limit the search space
	The RL result will then show an index of the result. For example, if the best opamp in a design iteration had a with of 3um,
	the corresponding index for 3um is 2 (3um is at the 2nd index in the array [1,2,3,4,5,6,7,8])
	
	The purpose of this function to convert a list of opamp parameter into a list of indices into these range arrays
	returns a list of indicies
	
	input can either be given in dictionary or np.array format
	here is an example dictionary input:
	{'half_diffpair_params': (-987.654321, -987.654321, -987.654321), 'diffpair_bias': (-987.654321, -987.654321, -987.654321), 'half_common_source_params': (-987.654321, -987.654321, -987.654321, -987.654321), 'half_common_source_bias': (-987.654321, -987.654321, -987.654321, -987.654321), 'output_stage_params': (-987.654321, -987.654321, -987), 'output_stage_bias': (-987, -987.654321, -987.654321), 'half_pload': (-987.654321, -987.654321, -987.654321), 'mim_cap_size': (-987.654321, -987.654321), 'mim_cap_rows': -987, 'rmult': -987}
	
	here is an example np.array indices output:
	np.array([6, 2, 7, 6, 0, 5, 7, 0, 10, 6, 5, 13, 0, 6, 4, 2])
	"""
	# convert to dictionary format first
	if isinstance(opamp_parameters, dict):
		opamp_parameter_dict = opamp_parameters
	else:
		opamp_parameter_dict = opamp_parameters_de_serializer(opamp_parameters)
	# Function to find the closest index in the range
	def closest_index(range_params, number):
		start, end, step = range_params
		values = np.arange(start, end, step)
		idx = (np.abs(values - number)).argmin()
		return idx
	# loop through params and find closest indices
	opamp_parameter_arr = list()
	for key, val in params.items():
		if key == "diffpair_params0":
			opamp_parameter_arr.append(closest_index(val, opamp_parameter_dict["half_diffpair_params"][0]))
		elif key == "diffpair_params1":
			opamp_parameter_arr.append(closest_index(val, opamp_parameter_dict["half_diffpair_params"][1]))
		elif key == "diffpair_params2":
			opamp_parameter_arr.append(closest_index(val, opamp_parameter_dict["half_diffpair_params"][2]))
		elif key == "Diffpair_bias0":
			opamp_parameter_arr.append(closest_index(val, opamp_parameter_dict["diffpair_bias"][0]))
		elif key == "Diffpair_bias1":
			opamp_parameter_arr.append(closest_index(val, opamp_parameter_dict["diffpair_bias"][1]))
		elif key == "Diffpair_bias2":
			opamp_parameter_arr.append(closest_index(val, opamp_parameter_dict["diffpair_bias"][2]))
		elif key == "pamp_hparams0":
			opamp_parameter_arr.append(closest_index(val, opamp_parameter_dict["half_common_source_params"][0]))
		elif key == "pamp_hparams1":
			opamp_parameter_arr.append(closest_index(val, opamp_parameter_dict["half_common_source_params"][1]))
		elif key == "pamp_hparams2":
			opamp_parameter_arr.append(closest_index(val, opamp_parameter_dict["half_common_source_params"][2]))
		elif key == "bias0":
			opamp_parameter_arr.append(closest_index(val, opamp_parameter_dict["half_common_source_bias"][0]))
		elif key == "bias1":
			opamp_parameter_arr.append(closest_index(val, opamp_parameter_dict["half_common_source_bias"][1]))
		elif key == "bias2":
			opamp_parameter_arr.append(closest_index(val, opamp_parameter_dict["half_common_source_bias"][2]))
		elif key == "bias3":
			opamp_parameter_arr.append(closest_index(val, opamp_parameter_dict["half_common_source_bias"][3]))
		elif key == "half_pload1":
			opamp_parameter_arr.append(closest_index(val, opamp_parameter_dict["half_pload"][0]))
		elif key == "half_pload3":
			opamp_parameter_arr.append(closest_index(val, opamp_parameter_dict["half_pload"][2]))
		elif key == "mim_cap_rows":
			opamp_parameter_arr.append(closest_index(val, opamp_parameter_dict["mim_cap_rows"]))
		else:
			raise ValueError("invalid key")
	# this relies on the fact that the params dict should be in order
	return np.array(opamp_parameter_arr)

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
