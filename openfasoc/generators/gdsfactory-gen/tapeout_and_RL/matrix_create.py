import numpy as np
import sys
# path to pygen
sys.path.append('../')
from sky130_nist_tapeout import sky130_opamp_add_pads, opamp_parameters_de_serializer, opamp_results_de_serializer
from pygen.opamp import opamp
from pygen.pdk.sky130_mapped import sky130_mapped_pdk as pdk
from pathlib import Path
from pygen.pdk.util.opamp_array_create import write_opamp_matrix
from multiprocessing import Pool
from gdsfactory.cell import clear_cache
from pygen.pdk.util.snap_to_grid import component_snap_to_grid
from pygen.routing.L_route import L_route
from pygen.pdk.util.port_utils import add_ports_perimeter

results= np.load("results.npy")
params = np.load("params.npy")

#low_noise = params[[58,18,42]]
#low_pwr_high_FOM = params[[0,4,2,1]]
#high_BW = params[[10,27,31]]
#high_DCg = params[[59,9,33]]


def create_opamps(save_dir_name: str, indices: list):
	pdk.cell_decorator_settings.cache=False
	comps = list()
	for index in indices:
		# create opamp
		comp = sky130_opamp_add_pads(opamp(pdk, **opamp_parameters_de_serializer(params[index])), flatten=False)
		comp = component_snap_to_grid(comp)
		comp.name = "opamp_" + str(index)
		# append to list
		comps.append(comp)
		clear_cache()
		with open(save_dir_name+".txt","a") as resfile:
			strtowrite = "\n-------------------------\nopamp_"+str(index)
			strtowrite += "\nparams = " + str(opamp_parameters_de_serializer(params[index]))
			strtowrite += "\n\nresults = " + str(opamp_results_de_serializer(results[index]))
			strtowrite += "\n\n\n"
			resfile.write(strtowrite)
	write_opamp_matrix(comps, write_name = save_dir_name + ".gds", xspace=600)


listnames = ["low_noise","low_pwr_high_FOM","high_BW","high_DCg"]
listindices = [[58,18,42],[0,4,2,1],[10,27,31],[59,9,33]]

for name, indices in zip(listnames,listindices):
	create_opamps(name, indices)
	clear_cache()

