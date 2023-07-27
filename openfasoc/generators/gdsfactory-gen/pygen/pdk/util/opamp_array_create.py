from gdsfactory.read.import_gds import import_gds
from gdsfactory.component import Component
from pathlib import Path
import os
import math
from gdsfactory.pdk import Pdk
from pathlib import Path


def get_files_with_extension(directory, extension):
	file_list = []
	for filename in os.listdir(directory):
		if filename.endswith(extension):
			file_list.append(filename)
	return file_list


def write_opamp_matrix(opamps_dir: Union[str,Path]="./"):
	"""Use the write_opamp_matrix function to create a matrix of many different opamps
	reads the different opamps from all gds files in opamps_dir
	"""
	pdk_nochache = Pdk(name="nocache")
	pdk_nochache.cell_decorator_settings.cache=False
	pdk_nochache.activate()

	search_dir = Path(opamps_dir).resolve()
	opamp_files_list = get_files_with_extension(str(search_dir),".gds")
	opamp_comp_list = list()

	for i,filev in enumerate(opamp_files_list):
		tempcomp = import_gds(filev)
		tempcomp.name = "opamp"+str(i)
		opamp_comp_list.append()

	col_len = round(math.sqrt(len(opamp_comp_list)))
	col_index = 0
	row_index = 0
	big_comp = Component("big comp")
	for opamp_v in opamp_comp_list:
		if opamp_v is None:
			continue
		opref = big_comp << opamp_v
		opref.movex(col_index * 200).movey(row_index*200)
		col_index += 1
		if not col_index % col_len:
			col_index=0
			row_index += 1

	big_comp.write_gds("big_gds_here.gds")

if __name__=="__main__":
	write_opamp_matrix()
