from gdsfactory.read.import_gds import import_gds
from gdsfactory.component import Component
from pathlib import Path
import os
import math
from gdsfactory.pdk import Pdk
from pathlib import Path
from typing import Union, Optional
from pydantic import validate_arguments

def get_files_with_extension(directory, extension):
	file_list = []
	for filename in os.listdir(directory):
		if filename.endswith(extension):
			file_list.append(filename)
	return file_list


@validate_arguments
def write_opamp_matrix(opamps_dir: Union[str,Path,list]="./", xspace: float=400,yspace: float=300, rtr_comp: bool=False, write_name: str="big_gds_here.gds"):
	"""Use the write_opamp_matrix function to create a matrix of many different opamps
	reads the different opamps from all gds files in opamps_dir
	args:
	opamps_dir = a file directory where all gds files are treated as opamps (i.e. to add to the matrix)
	****Note: you can specify this as a list Components, in which case, the list is used to make the matrix
	xspace = xspacing to use (center to center x distance between adajacent elements in the matrix)
	yspace = yspacing to use (center to center y distance between adajacent elements in the matrix)
	rtr_comp = if true will not write the component to gds (default = false)
	write_name = name/path of gds write file
	"""
	pdk_nochache = Pdk(name="nocache")
	pdk_nochache.cell_decorator_settings.cache=False
	pdk_nochache.activate()

	if isinstance(opamps_dir, list):
		opamp_comp_list = opamps_dir
	else:
		search_dir = Path(opamps_dir).resolve()
		opamp_files_list = get_files_with_extension(str(search_dir),".gds")
		opamp_comp_list = list()
		for i,filev in enumerate(opamp_files_list):
			if "big_gds_here" in str(filev) or write_name in str(filev):
				continue
			tempcomp = import_gds(filev)
			tempcomp.name = "opamp"+str(i)
			opamp_comp_list.append(tempcomp)

	col_len = round(math.sqrt(len(opamp_comp_list)))
	col_index = 0
	row_index = 0
	big_comp = Component("big comp")
	for opamp_v in opamp_comp_list:
		if opamp_v is None:
			continue
		opref = big_comp << opamp_v
		opref.movex(col_index * xspace).movey(row_index*yspace)
		col_index += 1
		if not col_index % col_len:
			col_index=0
			row_index += 1
	if rtr_comp:
		return big_comp
	else:
		big_comp.write_gds(write_name)

if __name__=="__main__":
	write_opamp_matrix()
