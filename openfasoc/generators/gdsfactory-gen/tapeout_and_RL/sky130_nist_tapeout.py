import sys
# path to glayout
sys.path.append('../')

from gdsfactory.read.import_gds import import_gds
from gdsfactory.components import text_freetype, rectangle
from glayout.pdk.util.comp_utils import prec_array, movey, align_comp_to_port, prec_ref_center
from glayout.pdk.util.port_utils import add_ports_perimeter, print_ports
from gdsfactory.component import Component
from glayout.pdk.mappedpdk import MappedPDK
from glayout.opamp import opamp
from glayout.routing.L_route import L_route
from glayout.routing.straight_route import straight_route
from glayout.routing.c_route import c_route
from glayout.via_gen import via_array
from gdsfactory.cell import cell, clear_cache
import numpy as np
from subprocess import Popen
from pathlib import Path
from typing import Union, Optional, Literal, Iterable
from tempfile import TemporaryDirectory
from shutil import copyfile, copytree
from multiprocessing import Pool
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import curve_fit
from scipy.spatial.distance import pdist, squareform
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
import argparse
from glayout.pdk.sky130_mapped import sky130_mapped_pdk as pdk
from itertools import count, repeat
from glayout.pdk.util.snap_to_grid import component_snap_to_grid
from glayout.pdk.util.opamp_array_create import write_opamp_matrix


global _GET_PARAM_SET_LENGTH_
global _TAKE_OUTPUT_AT_SECOND_STAGE_
global PDK_ROOT
global __NO_LVT_GLOBAL_
__NO_LVT_GLOBAL_ = False
_GET_PARAM_SET_LENGTH_ = False
_TAKE_OUTPUT_AT_SECOND_STAGE_ = False
PDK_ROOT = "/usr/bin/miniconda3/share/pdk/"

# ====Build Opamp====


def sky130_opamp_add_pads(opamp_in: Component, flatten=False) -> Component:
	"""adds the MPW-5 pads and nano pads to opamp.
	Also adds text labels and pin layers so that extraction is nice
	this function does not need to be used with sky130_add_opamp_labels
	"""
	opamp_wpads = opamp_in.copy()
	opamp_wpads = movey(opamp_wpads, destination=0)
	# create pad array and add to opamp
	pad = import_gds("pads/pad_60um_flat.gds")
	pad.name = "NISTpad"
	pad = add_ports_perimeter(pad, pdk.get_glayer("met4"),prefix="pad_")
	pad_array = prec_array(pad, rows=2, columns=(4+1), spacing=(40,120))
	pad_array_ref = prec_ref_center(pad_array)
	opamp_wpads.add(pad_array_ref)
	# add via_array to vdd pin
	vddarray = via_array(pdk, "met4","met5",size=(opamp_wpads.ports["pin_vdd_N"].width,opamp_wpads.ports["pin_vdd_E"].width))
	via_array_ref = opamp_wpads << vddarray
	align_comp_to_port(via_array_ref,opamp_wpads.ports["pin_vdd_N"],alignment=('c','b'))
	# route to the pads
	leftroutelayer="met4"
	opamp_wpads << L_route(pdk, opamp_wpads.ports["pin_plus_W"],pad_array_ref.ports["row1_col1_pad_S"], hwidth=3, vglayer=leftroutelayer)
	opamp_wpads << L_route(pdk, opamp_wpads.ports["pin_minus_W"],pad_array_ref.ports["row0_col1_pad_N"],hwidth=3, vglayer=leftroutelayer)
	opamp_wpads << straight_route(pdk, pad_array_ref.ports["row1_col2_pad_S"],opamp_wpads.ports["pin_vdd_S"], width=4,glayer1="met5")
	opamp_wpads << straight_route(pdk, opamp_wpads.ports["pin_diffpairibias_S"],pad_array_ref.ports["row0_col2_pad_N"])
	opamp_wpads << L_route(pdk, opamp_wpads.ports["pin_gnd_E"],pad_array_ref.ports["row0_col3_pad_N"], vglayer="met4",hwidth=3)
	opamp_wpads << L_route(pdk, opamp_wpads.ports["pin_commonsourceibias_E"],pad_array_ref.ports["row0_col4_pad_N"],hwidth=3)
	opamp_wpads << L_route(pdk, opamp_wpads.ports["pin_outputibias_E"],pad_array_ref.ports["row1_col4_pad_S"], hwidth=3)
	opamp_wpads << c_route(pdk, opamp_wpads.ports["pin_output_route_E"],pad_array_ref.ports["row1_col3_pad_E"], extension=1, cglayer="met3", cwidth=4)
	# add pin layer and text labels for LVS
	text_pin_labels = list()
	met5pin = rectangle(size=(5,5),layer=(72,16), centered=True)
	for name in ["minus","diffpairibias","gnd","commonsourceibias","plus","vdd","output","outputibias"]:
		pin_w_label = met5pin.copy()
		pin_w_label.add_label(text=name,layer=(72,5),magnification=4)
		text_pin_labels.append(pin_w_label)
	for row in range(2):
		for col_u in range(4):
			col = col_u + 1# left most are for nano pads
			port_name = "row"+str(row)+"_col"+str(col)+"_pad_S"
			pad_array_port = pad_array_ref.ports[port_name]
			pin_ref = opamp_wpads << text_pin_labels[4*row + col_u]
			align_comp_to_port(pin_ref,pad_array_port,alignment=('c','t'))
	# import nano pad and add to opamp
	nanopad = import_gds("pads/sky130_nano_pad.gds")
	nanopad.name = "nanopad"
	nanopad = add_ports_perimeter(nanopad, pdk.get_glayer(leftroutelayer),prefix="nanopad_")
	nanopad_array = prec_array(nanopad, rows=2, columns=2, spacing=(10,10))
	nanopad_array_ref = nanopad_array.ref_center()
	opamp_wpads.add(nanopad_array_ref)
	nanopad_array_ref.movex(opamp_wpads.xmin+nanopad_array.xmax)
	# route nano pad connections
	opamp_wpads << straight_route(pdk, nanopad_array_ref.ports["row1_col0_nanopad_N"],pad_array_ref.ports["row1_col0_pad_S"],width=3,glayer2=leftroutelayer)
	opamp_wpads << straight_route(pdk, nanopad_array_ref.ports["row0_col0_nanopad_S"],pad_array_ref.ports["row0_col0_pad_N"],width=3,glayer2=leftroutelayer)
	opamp_wpads << straight_route(pdk, nanopad_array_ref.ports["row0_col1_nanopad_E"],pad_array_ref.ports["row0_col1_pad_N"],width=3,glayer2=leftroutelayer)
	opamp_wpads << straight_route(pdk, nanopad_array_ref.ports["row1_col1_nanopad_E"],pad_array_ref.ports["row1_col1_pad_S"],width=3,glayer2=leftroutelayer)
	# add the extra pad for the CS output
	cspadref = opamp_wpads << pad
	cspadref.movex(300).movey(90)
	opamp_wpads << L_route(pdk, cspadref.ports["pad_S"], opamp_wpads.ports["commonsource_output_E"],hwidth=3, hglayer="met5",vglayer="met5")
	#opamp_wpads << nanopad
	if flatten:
		return opamp_wpads.flatten()
	else:
		return opamp_wpads


def sky130_add_opamp_labels(opamp_in: Component) -> Component:
	"""adds opamp labels for extraction, without adding pads
	this function does not need to be used with sky130_add_opamp_pads
	"""
	opamp_in.unlock()
	# define layers
	met2_pin = (69,16)
	met2_label = (69,5)
	met3_pin = (70,16)
	met3_label = (70,5)
	met4_pin = (71,16)
	met4_label = (71,5)
	# list that will contain all port/comp info
	move_info = list()
	# create labels and append to info list
	# gnd
	gndlabel = rectangle(layer=met3_pin,size=(1,1),centered=True).copy()
	gndlabel.add_label(text="gnd",layer=met3_label)
	move_info.append((gndlabel,opamp_in.ports["pin_gnd_N"],None))
	#diffpairibias
	ibias1label = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
	ibias1label.add_label(text="diffpairibias",layer=met2_label)
	move_info.append((ibias1label,opamp_in.ports["pin_diffpairibias_N"],None))
	#outputibias
	ibias3label = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
	ibias3label.add_label(text="outputibias",layer=met2_label)
	move_info.append((ibias3label,opamp_in.ports["pin_outputibias_N"],None))
	# commonsourceibias
	ibias2label = rectangle(layer=met4_pin,size=(1,1),centered=True).copy()
	ibias2label.add_label(text="commonsourceibias",layer=met4_label)
	move_info.append((ibias2label,opamp_in.ports["pin_commonsourceibias_N"],None))
	#minus
	minuslabel = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
	minuslabel.add_label(text="minus",layer=met2_label)
	move_info.append((minuslabel,opamp_in.ports["pin_minus_N"],None))
	#-plus
	pluslabel = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
	pluslabel.add_label(text="plus",layer=met2_label)
	move_info.append((pluslabel,opamp_in.ports["pin_plus_N"],None))
	#vdd
	vddlabel = rectangle(layer=met3_pin,size=(1,1),centered=True).copy()
	vddlabel.add_label(text="vdd",layer=met3_label)
	move_info.append((vddlabel,opamp_in.ports["pin_vdd_N"],None))
	# output (3rd stage)
	outputlabel = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
	outputlabel.add_label(text="output",layer=met2_label)
	move_info.append((outputlabel,opamp_in.ports["pin_output_route_N"],None))
	# output (2nd stage)
	outputlabel = rectangle(layer=met4_pin,size=(0.2,0.2),centered=True).copy()
	outputlabel.add_label(text="CSoutput",layer=met4_label)
	move_info.append((outputlabel,opamp_in.ports["commonsource_output_E"],('l','c')))
	# move everything to position
	for comp, prt, alignment in move_info:
		alignment = ('c','b') if alignment is None else alignment
		compref = align_comp_to_port(comp, prt, alignment=alignment)
		opamp_in.add(compref)
	return opamp_in.flatten()


def sky130_add_lvt_layer(opamp_in: Component) -> Component:
	global __NO_LVT_GLOBAL_
	if __NO_LVT_GLOBAL_:
		return opamp_in
	opamp_in.unlock()
	# define layers
	lvt_layer = (125,44)
	# define geometry over pmos components and add lvt
	SW_S_edge = opamp_in.ports["commonsource_Pamp_L_multiplier_0_plusdoped_S"]
	SW_W_edge = opamp_in.ports["commonsource_Pamp_L_multiplier_0_dummy_L_plusdoped_W"]
	NE_N_edge = opamp_in.ports["commonsource_Pamp_R_multiplier_2_plusdoped_N"]
	NE_E_edge = opamp_in.ports["commonsource_Pamp_R_multiplier_2_dummy_R_plusdoped_E"]
	SW_S_center = SW_S_edge.center
	SW_W_center = SW_W_edge.center
	NE_N_center = NE_N_edge.center
	NE_E_center = NE_E_edge.center
	SW_corner = [SW_W_center[0], SW_S_center[1]]
	NE_corner = [NE_E_center[0], NE_N_center[1]]
	middle_top_y = opamp_in.ports["pcomps_ptopAB_L_plusdoped_N"].center[1]
	middle_bottom_y = opamp_in.ports["pcomps_pbottomAB_R_plusdoped_S"].center[1]
	max_y = max(middle_top_y, NE_corner[1])
	min_y = min(middle_bottom_y, SW_corner[1])
	abs_center = (SW_corner[0] + (NE_corner[0] - SW_corner[0])/2, min_y + (max_y - min_y)/2)
	# draw lvt rectangle
	LVT_rectangle = rectangle(layer=lvt_layer, size=(abs(NE_corner[0] - SW_corner[0]), abs(max_y - min_y)+0.36), centered=True)
	LVT_rectangle_ref = opamp_in << LVT_rectangle
	# align lvt rectangle to the plusdoped_N region
	LVT_rectangle_ref.move(origin=(0, 0), destination=abs_center)
	# define geometry over output amplfier and add lvt
	outputW = opamp_in.ports["outputstage_amp_multiplier_0_dummy_L_plusdoped_W"]
	outputE = opamp_in.ports["outputstage_amp_multiplier_0_dummy_R_plusdoped_E"]
	width = abs(outputE.center[0]-outputW.center[0])
	hieght = outputW.width+0.36
	center = (outputW.center[0] + width/2, outputW.center[1])
	lvtref = opamp_in << rectangle(size=(width,hieght),layer=lvt_layer,centered=True)
	lvtref.move(destination=center)
	return opamp_in



# ====Run Training====



def opamp_parameters_serializer(
	half_diffpair_params: tuple[float, float, int] = (6, 1, 4),
    diffpair_bias: tuple[float, float, int] = (6, 2, 4),
    half_common_source_params: tuple[float, float, int, int] = (7, 1, 10, 3),
    half_common_source_bias: tuple[float, float, int, int] = (6, 2, 8, 2),
    output_stage_params: tuple[float, float, int] = (5, 1, 16),
    output_stage_bias: tuple[float, float, int] = (6, 2, 4),
	half_pload: tuple[float,float,int] = (6,1,6),
    mim_cap_size=(12, 12),
    mim_cap_rows=3,
    rmult: int = 2
) -> np.array:
	"""converts opamp params into the uniform numpy float format"""
	return np.array(
		[half_diffpair_params[0],half_diffpair_params[1],half_diffpair_params[2],
		diffpair_bias[0],diffpair_bias[1],diffpair_bias[2],
		half_common_source_params[0],half_common_source_params[1],half_common_source_params[2],half_common_source_params[3],
		half_common_source_bias[0],half_common_source_bias[1],half_common_source_bias[2],half_common_source_bias[3],
		output_stage_params[0],output_stage_params[1],output_stage_params[2],
		output_stage_bias[0],output_stage_bias[1],output_stage_bias[2],
		half_pload[0],half_pload[1],half_pload[2],
		mim_cap_size[0],mim_cap_size[1],
		mim_cap_rows,
		rmult],
		dtype=np.float64
	)

def opamp_parameters_de_serializer(serialized_params: Optional[np.array]=None) -> dict:
	"""converts uniform numpy float format to opamp kwargs"""
	if serialized_params is None:
		serialized_params = 27*[-987.654321]
		serialized_params[16] = int(-987.654321)
		serialized_params[17] = int(-987.654321)
	if not len(serialized_params) == 27:
		raise ValueError("serialized_params should be a length 27 array")
	params_dict = dict()
	params_dict["half_diffpair_params"] = tuple(serialized_params[0:3])
	params_dict["diffpair_bias"] = tuple(serialized_params[3:6])
	params_dict["half_common_source_params"] = tuple(serialized_params[6:10])
	params_dict["half_common_source_bias"] = tuple(serialized_params[10:14])
	params_dict["output_stage_params"] = tuple(serialized_params[14:17])
	params_dict["output_stage_bias"] = tuple(serialized_params[17:20])
	params_dict["mim_cap_size"] = tuple(serialized_params[20:23])
	params_dict["mim_cap_size"] = tuple(serialized_params[23:25])
	params_dict["mim_cap_rows"] = int(serialized_params[25])
	params_dict["rmult"] = int(serialized_params[26])
	return params_dict

def opamp_results_serializer(
	ugb: float = -987.654321,
	dcGain: float = -987.654321,
	phaseMargin: float = -987.654321,
	Ibias_diffpair: float = -987.654321,
	Ibias_commonsource: float = -987.654321,
	Ibias_output: float = -987.654321,
	area: float = -987.654321,
	power: float = -987.654321,
	noise: float = -987.654321,
	bw_3db: float = -987.654321,
	power_twostage: float = -987.654321
) -> np.array:
	return np.array([ugb, dcGain, phaseMargin, Ibias_diffpair, Ibias_commonsource, Ibias_output, area, power, noise, bw_3db, power_twostage], dtype=np.float64)

def opamp_results_de_serializer(
	results: Optional[np.array]=None
) -> dict:
	results_length_const = 11
	if results is None:
		results = results_length_const*[-987.654321]
	if not len(results) == results_length_const:
		raise ValueError("results should be a length "+str(results_length_const)+" array")
	results_dict = dict()
	results_dict["ugb"] = float(results[0])
	results_dict["dcGain"] = float(results[1])
	results_dict["phaseMargin"] = float(results[2])
	results_dict["Ibias_diffpair"] = float(results[3])
	results_dict["Ibias_commonsource"] = float(results[4])
	results_dict["Ibias_output"] = float(results[5])
	results_dict["area"] = float(results[6])
	results_dict["power"] = float(results[7])
	results_dict["noise"] = float(results[8])
	results_dict["bw_3db"] = float(results[9])
	results_dict["power_twostage"] = float(results[10])
	return results_dict

def get_small_parameter_list(test_mode = False) -> np.array:
	"""creates small parameter list intended for brute force"""
	# all diffpairs to try
	diffpairs = list()
	if test_mode:
		diffpairs.append((6,1,4))
		diffpairs.append((5,1,4))
	else:
		for width in [7]:
			for length in [0.5,0.7, 0.9]:
				for fingers in [8,10,12]:
					diffpairs.append((width,length,fingers))
	# all bias2 (output amp bias) transistors
	bias2s = list()
	if test_mode:
		bias2s.append((6,1,4,3))
	else:
		for width in [7]:
			for length in [1]:
				for fingers in [12,16,20]:
					for mults in [2,3]:
						bias2s.append((width,length,fingers,mults))
	# all pmos first stage load transistors
	half_pload = list()
	if test_mode:
		half_pload.append((6,1,6))
	else:
		for width in [9]:
			for length in [0.5]:
				for fingers in [6,8,10,12]:
					half_pload.append((width,length,fingers))
	# all output pmos transistors
	pamp_hparams = list()
	if test_mode:
		pamp_hparams.append((7,1,8,3))
	else:
		for width in [8]:
			for length in [0.5]:
				for fingers in [8,12,16,20]:
					pamp_hparams.append((width,length,fingers,3))
	# diffpair bias cmirror
	diffpair_cmirrors = list()
	if test_mode:
		pass
	else:
		for width in [7]:
			for length in [1]:
				for fingers in [8,10]:
					diffpair_cmirrors.append((width,length,fingers))
	# rows of the cap array to try
	cap_arrays = [3]
	# routing mults to try
	rmults = [2]
	# ******************************************
	# create and return the small parameters list
	short_list_len = len(diffpairs) * len(bias2s) * len(pamp_hparams) * len(cap_arrays) * len(rmults) * len(diffpair_cmirrors) * len(half_pload)
	short_list_len += 2 if test_mode else 0
	short_list = np.empty(shape=(short_list_len,len(opamp_parameters_serializer())),dtype=np.float64)
	index = 0
	for diffpair_v in diffpairs:
		for bias2_v in bias2s:
			for pamp_o_v in pamp_hparams:
				for cap_array_v in cap_arrays:
					for rmult in rmults:
						for diffpair_cmirror_v in diffpair_cmirrors:
							for halfpld in half_pload:
								tup_to_add = opamp_parameters_serializer(
									half_pload=halfpld,
									half_diffpair_params=diffpair_v, 
									half_common_source_bias=bias2_v, 
									mim_cap_rows=cap_array_v, 
									half_common_source_params=pamp_o_v,
									rmult=rmult,
									diffpair_bias=diffpair_cmirror_v,
								)
								short_list[index] = tup_to_add
								index = index + 1
	# if test_mode create a failed attempt (to test error handling)
	if test_mode:
		short_list[index] = opamp_parameters_serializer(mim_cap_rows=-1)
		short_list[index+1] = opamp_parameters_serializer(mim_cap_rows=0)
	global _GET_PARAM_SET_LENGTH_
	if _GET_PARAM_SET_LENGTH_:
		print("created parameter set of length: "+str(len(short_list)))
		import sys
		sys.exit()
	return short_list

def get_sim_results(acpath: Union[str,Path], dcpath: Union[str,Path], noisepath: Union[str,Path]):
	acabspath = Path(acpath).resolve()
	dcabspath = Path(dcpath).resolve()
	noiseabspath = Path(noisepath).resolve()
	ACColumns = None
	DCColumns = None
	NoiseColumns = None
	try:
		with open(acabspath, "r") as ACReport:
			RawAC = ACReport.readlines()[0]
			ACColumns = [item for item in RawAC.split() if item]
	except Exception:
		pass
	try:
		with open(dcabspath, "r") as DCReport:
			RawDC = DCReport.readlines()[0]
			DCColumns = [item for item in RawDC.split() if item]
	except Exception:
		pass
	try:
		with open(noiseabspath, "r") as NoiseReport:
			RawNoise = NoiseReport.readlines()[0]
			NoiseColumns = [item for item in RawNoise.split() if item]
	except Exception:
		pass
	na = -987.654321
	noACresults = (ACColumns is None) or len(ACColumns)<13
	noDCresults = (DCColumns is None) or len(DCColumns)<4
	nonoiseresults = (NoiseColumns is None) or len(NoiseColumns)<2
	return_dict = {
		"ugb": na if noACresults else ACColumns[1],
		"Ibias_diffpair": na if noACresults else ACColumns[3],
		"Ibias_commonsource": na if noACresults else ACColumns[5],
		"Ibias_output": na if noACresults else ACColumns[7],
		"phaseMargin": na if noACresults else ACColumns[9],
		"dcGain": na if noACresults else ACColumns[11],
		"bw_3db": na if noACresults else ACColumns[13],
		"power": na if noDCresults else DCColumns[1],
		"noise": na if nonoiseresults else NoiseColumns[1],
		"power_twostage": na if noDCresults else DCColumns[3],
	}
	for key, val in return_dict.items():
		val_flt = na
		try:
			val_flt = float(val)
		except ValueError:
			val_flt = na
		return_dict[key] = val_flt
	return return_dict

def process_netlist_subckt(netlist: Union[str,Path], sim_model: Literal["normal model", "cryo model"], cload: float=0.0, noparasitics: bool=False):
	global _TAKE_OUTPUT_AT_SECOND_STAGE_
	netlist = Path(netlist).resolve()
	if not netlist.is_file():
		raise ValueError("netlist is not a valid file")
	hints = [".subckt","output","plus","minus","vdd","gnd","commonsourceibias","outputibias"]
	subckt_lines = list()
	with open(netlist, "r") as spice_net:
		subckt_lines = spice_net.readlines()
		for i,line in enumerate(subckt_lines):
			line = line.strip().lower()
			if (i+1)<len(subckt_lines) and len(line) and len(subckt_lines[i+1]) and (subckt_lines[i+1][0]=="+" or line[-1]=="+"):
				subckt_lines[i+1] = subckt_lines[i+1].replace("+","").strip()
				subckt_lines[i] = line.rstrip("+") + " " + subckt_lines[i+1] + "\n"
				subckt_lines[i+1] = ""
				line = subckt_lines[i]
			if "cryo" in sim_model and len(line)>1:
				subckt_lines[i] = subckt_lines[i].replace("sky130_fd_pr__nfet_01v8_lvt","nshortlvth")
				subckt_lines[i] = subckt_lines[i].replace("sky130_fd_pr__pfet_01v8_lvt","pshort")
				subckt_lines[i] = subckt_lines[i].replace("sky130_fd_pr__nfet_01v8","nshort")
				if ("nshort" in subckt_lines[i]) or ("pshort" in subckt_lines[i]) or ("nshortlvth" in subckt_lines[i]):
					subckt_lines[i] = "M" + subckt_lines[i][1:]
			if all([hint in line for hint in hints]):
				if _TAKE_OUTPUT_AT_SECOND_STAGE_:
					headerstr = ".subckt opamp CSoutput vdd plus minus commonsourceibias outputibias diffpairibias gnd output"
				else:
					headerstr = ".subckt opamp output vdd plus minus commonsourceibias outputibias diffpairibias gnd CSoutput"
				subckt_lines[i] = headerstr+"\nCload output gnd " + str(cload) +"p\n"
			if ("floating" in line) or (noparasitics and len(line) and line[0]=="C"):
				subckt_lines[i] = "* "+ subckt_lines[i]
	with open(netlist, "w") as spice_net:
		spice_net.writelines(subckt_lines)

def process_spice_testbench(testbench: Union[str,Path], temperature_info: tuple[int,str]=(25,"normal model")):
	global PDK_ROOT
	PDK_ROOT = Path(PDK_ROOT).resolve()
	testbench = Path(testbench).resolve()
	if not testbench.is_file():
		raise ValueError("testbench must be file")
	if not PDK_ROOT.is_dir():
		raise ValueError("PDK_ROOT is not a valid directory")
	PDK_ROOT = str(PDK_ROOT)
	with open(testbench, "r") as spice_file:
		spicetb = spice_file.read()
		spicetb = spicetb.replace('{@@TEMP}', str(int(temperature_info[0])))
		spicetb = spicetb.replace("@@PDK_ROOT", PDK_ROOT)
		if temperature_info[1] == "cryo model":
			spicetb = spicetb.replace("*@@cryo ","")
		else:
			spicetb = spicetb.replace("*@@stp ","")
	with open(testbench, "w") as spice_file:
		spice_file.write(spicetb)

def __run_single_brtfrc(index, parameters_ele, save_gds_dir, temperature_info: tuple[int,str]=(25,"normal model"), cload: float=0.0, noparasitics: bool=False, output_dir: Optional[Union[int,str,Path]] = None):
	# pass pdk as global var to avoid pickling issues
	global pdk
	global PDK_ROOT
	# generate layout
	destination_gds_copy = save_gds_dir / (str(index)+".gds")
	sky130pdk = pdk
	params = opamp_parameters_de_serializer(parameters_ele)
	try:
		opamp_v = sky130_add_opamp_labels(sky130_add_lvt_layer(opamp(sky130pdk, **params)))
		opamp_v.name = "opamp"
		area = float(opamp_v.area())
		# use temp dir
		with TemporaryDirectory() as tmpdirname:
			results=None
			tmp_gds_path = Path(opamp_v.write_gds(gdsdir=tmpdirname)).resolve()
			if tmp_gds_path.is_file():
				destination_gds_copy.write_bytes(tmp_gds_path.read_bytes())
			extractbash_template=str()
			#import pdb; pdb.set_trace()
			with open("extract.bash.template","r") as extraction_script:
				extractbash_template = extraction_script.read()
				extractbash_template = extractbash_template.replace("@@PDK_ROOT",PDK_ROOT)
			with open(str(tmpdirname)+"/extract.bash","w") as extraction_script:
				extraction_script.write(extractbash_template)
			#copyfile("extract.bash",str(tmpdirname)+"/extract.bash")
			copyfile("opamp_perf_eval.sp",str(tmpdirname)+"/opamp_perf_eval.sp")
			copytree("sky130A",str(tmpdirname)+"/sky130A")
			# extract layout
			Popen(["bash","extract.bash", tmp_gds_path, opamp_v.name],cwd=tmpdirname).wait()
			print("Running simulation at temperature: " + str(temperature_info[0]) + "C")
			process_spice_testbench(str(tmpdirname)+"/opamp_perf_eval.sp",temperature_info=temperature_info)
			process_netlist_subckt(str(tmpdirname)+"/opamp_pex.spice", temperature_info[1], cload=cload, noparasitics=noparasitics)
			# run sim and store result
			Popen(["ngspice","-b","opamp_perf_eval.sp"],cwd=tmpdirname).wait()
			ac_file = str(tmpdirname)+"/result_ac.txt"
			power_file = str(tmpdirname)+"/result_power.txt"
			noise_file = str(tmpdirname)+"/result_noise.txt"
			result_dict = get_sim_results(ac_file, power_file, noise_file)
			result_dict["area"] = area
			results = opamp_results_serializer(**result_dict)
			if output_dir is not None:
				if isinstance(output_dir, int):
					output_dir = save_gds_dir / ("dir_"+str(output_dir))
					output_dir = Path(output_dir).resolve()
				else:
					output_dir = Path(output_dir).resolve()
				output_dir.mkdir(parents=True, exist_ok=True)
				if not output_dir.is_dir():
					raise ValueError("Output directory must be a directory")
				copytree(str(tmpdirname), str(output_dir)+"/test_output", dirs_exist_ok=True)
	except Exception as e_LorA:
		results = opamp_results_serializer()
		with open('get_training_data_ERRORS.log', 'a') as errlog:
			errlog.write("\nopamp run "+str(index)+" with the following params failed: \n"+str(params))
	return results


def brute_force_full_layout_and_PEXsim(sky130pdk: MappedPDK, parameter_list: np.array, temperature_info: tuple[int,str]=(25,"normal model"), cload: float=0.0, noparasitics: bool=False, saverawsims: bool=False) -> np.array:
	"""runs the brute force testing of parameters by
	1-constructing the opamp layout specfied by parameters
	2-extracting the netlist for the opamp
	3-running simulations on the opamp
	returns the results from opamp simulations as nparray
	"""
	if sky130pdk.name != "sky130":
		raise ValueError("this is for sky130 only")
	# disable adding NPC layer
	add_npc_decorator = sky130pdk.default_decorator
	sky130pdk.default_decorator = None
	sky130pdk.activate()
	# initialize empty results array
	results = None
	# run layout, extraction, sim
	save_gds_dir = Path('./save_gds_by_index').resolve()
	save_gds_dir.mkdir(parents=True)
	# pass pdk as global var to avoid pickling issues
	global pdk
	pdk = sky130pdk
	with Pool(120) as cores:
		if saverawsims:
			results = np.array(cores.starmap(__run_single_brtfrc, zip(count(0), parameter_list, repeat(save_gds_dir), repeat(temperature_info), repeat(cload), repeat(noparasitics), count(0))),np.float64)
		else:
			results = np.array(cores.starmap(__run_single_brtfrc, zip(count(0), parameter_list, repeat(save_gds_dir), repeat(temperature_info), repeat(cload), repeat(noparasitics))),np.float64)
	# undo pdk modification
	sky130pdk.default_decorator = add_npc_decorator
	return results

# data gathering main function
def get_training_data(test_mode: bool=True, temperature_info: tuple[int,str]=(25,"normal model"), cload: float=0.0, noparasitics: bool=False, parameter_array: Optional[np.array]=None, saverawsims=False) -> None:
	if temperature_info[1] != "normal model" and temperature_info[1] != "cryo model":
		raise ValueError("model must be one of \"normal model\" or \"cryo model\"")
	if parameter_array is None:
		params = get_small_parameter_list(test_mode)
	else:
		params = parameter_array
	results = brute_force_full_layout_and_PEXsim(pdk, params, temperature_info, cload=cload, noparasitics=noparasitics,saverawsims=saverawsims)
	np.save("training_params.npy",params)
	np.save("training_results.npy",results)



#util function for pure simulation. sky130 is imported automatically
def single_build_and_simulation(parameters: np.array, temp: int=25, output_dir: Optional[Union[str,Path]] = None, cload: float=0.0, noparasitics: bool=False) -> dict:
	"""Builds, extract, and simulates a single opamp
	saves opamp gds in current directory with name 12345678987654321.gds
	returns -987.654321 for all values IF phase margin < 45
	"""
	from glayout.pdk.sky130_mapped import sky130_mapped_pdk
	# process temperature info
	temperature_info = [temp, None]
	if temperature_info[0] > -20:
		temperature_info[1] = "normal model"
	elif temperature_info[0]!=-269:
		raise ValueError("simulation temperature should be exactly -269C for cryo sim. Below -20C there are no good models for simulation")
	else:
		temperature_info[1] = "cryo model"
	temperature_info = tuple(temperature_info)
	# run single build
	save_gds_dir = Path('./').resolve()
	index = 12345678987654321
	# pass pdk as global var to avoid pickling issues
	global pdk
	pdk = sky130_mapped_pdk
	results = __run_single_brtfrc(index, parameters, temperature_info=temperature_info, save_gds_dir=save_gds_dir, output_dir=output_dir, cload=cload, noparasitics=noparasitics)
	results = opamp_results_de_serializer(results)
	if results["phaseMargin"] < 45:
		for key in results:
			results[key] = -987.654321
	return results




# ================ stats ==================





def save_distwith_best_fit(data, output_file, title="Distribution With Trend", xlabel="Data", ylabel="Distribution"):
	"""Create a histogram with a line of best fit for the input data and save it as a PNG file.
	args:
		data (numpy.array): 1D array containing the simulation metrics.
		output_file (str): File path to save the generated PNG.
		bins (int or str): Number of bins for the histogram or 'auto' for automatic binning (default is 'auto').
		fit_distribution (str): Distribution to fit to the data. Supported options: 'norm' (normal distribution) or 'exponential'.
	"""
	# Create the histogram
	plt.figure()
	n, bins, patches = plt.hist(data, bins="auto", density=True, alpha=0.7)
	# Fit a normal distribution to the data
	mu, sigma = norm.fit(data)
	best_fit_line = norm.pdf(bins, mu, sigma)
	distribution_label = 'Normal Distribution'
	# Add the line of best fit to the plot
	plt.plot(bins, best_fit_line, 'r-', label=distribution_label)
	# Add labels and legend
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.legend()
	# Save the plot as a PNG file
	plt.savefig(output_file)
	plt.clf()

def save_pairwise_scatter_plot(data, output_file):
	"""Create a Pairwise Scatter Plot for the input data and save it as a PNG file.
	args:
		data (numpy.array or pandas.DataFrame):
		output_file (str/path): File path to save the generated PNG.
	"""
	# If the data is a NumPy array, convert it to a pandas DataFrame
	if isinstance(data, np.ndarray):
		data = pd.DataFrame(data)
	# Create the Pairwise Scatter Plot
	sns.pairplot(data)
	# Save the plot as a PNG file
	plt.savefig(output_file)
	plt.close()
	plt.clf()

def run_pca_and_save_plot(data, output_file):
	"""Run PCA on the input data and save the PCA plot as a PNG file.
	args:
		data (numpy.array or pandas.DataFrame): The 17-dimensional input data for PCA.
		output_file (str): File path to save the generated PNG.
	"""
	# If the data is a pandas DataFrame, convert it to a NumPy array
	if isinstance(data, pd.DataFrame):
		data = data.to_numpy()
	# Perform PCA
	pca = PCA(n_components=2)  # Reduce to 2 dimensions for visualization
	pca_result = pca.fit_transform(data)
	# Create the biplot
	plt.figure(figsize=(10, 8))
	plt.scatter(pca_result[:, 0], pca_result[:, 1], alpha=0.7)
	# Plot feature loadings as arrows
	feature_vectors = pca.components_.T
	for i, (x, y) in enumerate(feature_vectors):
		plt.arrow(0, 0, x, y, color='r', alpha=0.5)
		plt.text(x, y, f'Feature {i+1}', color='g', ha='center', va='center')
	# Add labels and title
	plt.xlabel('Principal Component 1')
	plt.ylabel('Principal Component 2')
	plt.title('PCA Biplot')
	# Save the plot as a PNG file
	plt.savefig(output_file)
	plt.close()
	plt.clf()

def find_optimal_clusters(data, max_clusters=10):
    if isinstance(data, pd.DataFrame):
        data = data.to_numpy()
    results = []
    for num_clusters in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=num_clusters)
        kmeans.fit(data)
        inertia = kmeans.inertia_
        results.append((num_clusters, inertia))
    return results

def elbow_point(x, y):
    deltas = np.diff(y)
    elbow_index = np.argmax(deltas < np.mean(deltas))
    return x[elbow_index]

def create_pca_biplot_with_clusters(data, results, output_file, max_clusters=10, results_index: int=0):
    if isinstance(data, pd.DataFrame):
        data = data.to_numpy()
    if isinstance(results, pd.Series):
        results = results.to_numpy()
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(data)
    cluster_results = find_optimal_clusters(data, max_clusters)
    num_clusters_values, inertias = zip(*cluster_results)
    optimal_num_clusters = elbow_point(num_clusters_values, inertias)
    kmeans = KMeans(n_clusters=int(optimal_num_clusters))
    cluster_assignments = kmeans.fit_predict(data)
    plt.figure(figsize=(10, 8))
    for i in range(int(optimal_num_clusters)):
        cluster_indices = np.where(cluster_assignments == i)[0]
        plt.scatter(pca_result[cluster_indices, 0], pca_result[cluster_indices, 1], alpha=0.7, label=f'Cluster {i+1}')
    # Color the data points based on their result values
    plt.scatter(pca_result[:, 0], pca_result[:, 1], c=results[:,results_index], cmap='viridis', edgecolor='k', s=80)
    feature_vectors = pca.components_.T
    for i, (x, y) in enumerate(feature_vectors):
        plt.arrow(0, 0, x, y, color='r', alpha=0.5)
        plt.text(x, y, f'Feature {i+1}', color='g', ha='center', va='center')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('PCA Biplot with Clusters')
    plt.legend()
    plt.colorbar(label='Results')
    plt.savefig(output_file)
    plt.close()
    plt.clf()

def create_heatmap_with_clusters(parameters, results, output_file, max_clusters=10,results_index: int=0):
    if isinstance(parameters, pd.DataFrame):
        parameters = parameters.to_numpy()
    if isinstance(results, pd.Series):
        results = results.to_numpy()
    # Perform PCA
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(parameters)
    # Cluster the parameters based on the results using hierarchical clustering
    results_dist = pdist(results[:,results_index].reshape(-1, 1))  # Pairwise distance between result values
    results_linkage = squareform(results_dist)  # Convert to a condensed distance matrix
    clustering = AgglomerativeClustering(n_clusters=max_clusters, affinity='precomputed', linkage='complete')
    cluster_assignments = clustering.fit_predict(results_linkage)
    # Create a dictionary to map clusters to their corresponding parameters
    cluster_param_dict = {}
    for cluster_id, param_values in zip(cluster_assignments, parameters):
        if cluster_id not in cluster_param_dict:
            cluster_param_dict[cluster_id] = []
        cluster_param_dict[cluster_id].append(param_values)
    # Calculate the mean parameter values for each cluster
    cluster_means = [np.mean(cluster_param_dict[cluster_id], axis=0) for cluster_id in range(max_clusters)]
    # Create the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(cluster_means, cmap='YlGnBu', annot=True, fmt='.2f', xticklabels=False,
                yticklabels=False, cbar_kws={'label': 'Mean Parameter Value'})
    plt.xlabel('Parameter Clusters')
    plt.ylabel('Parameter Clusters')
    plt.title('Heatmap Clusters')
    plt.savefig(output_file)
    plt.close()
    plt.clf()

def find_indices_with_same_other_params(data, parameter_index, other_params_values):
    mask = np.ones(len(data), dtype=bool)
    num_params = data.shape[1]
    for param_idx in range(num_params):
        if param_idx == parameter_index:
            continue
        mask = mask & (data[:, param_idx] == other_params_values[param_idx])
    return np.where(mask)[0]

def single_param_scatter(data: np.array, results: np.array, col_to_isolate: int, output_file: str, isolate: bool=True,results_index: int=0, trend:bool=True):
	output_file = Path(output_file).resolve()
	example_others = data[0, :]
	if isolate:
		indices = find_indices_with_same_other_params(data, col_to_isolate, example_others)
		x = data[indices, col_to_isolate]
		y = results[:,results_index][indices]
	else:
		x = data[:, col_to_isolate]
		y = results[:,results_index]
	plt.scatter(x, y, marker='o', s=50, label="Data Points")
	# Fit a quadratic regression model to the data
	coeffs = np.polyfit(x, y, deg=2)
	# Generate points for the quadratic trend line
	if trend:
		quadratic_function = lambda x, a, b, c: a * x**2 + b * x + c
		trend_line_x = np.linspace(min(x), max(x), 1000)
		trend_line_y = quadratic_function(trend_line_x, *coeffs)
		# Plot the quadratic trend line
		plt.plot(trend_line_x, trend_line_y, color='red')#, label="Quadratic Trend Line")
	# label and return
	plt.xlabel(output_file.stem)
	plt.ylabel("Normalized Performance Score")
	plt.title("Performance vs Parameter="+output_file.stem)
	plt.legend()
	plt.grid(True)
	plt.savefig(output_file)
	plt.clf()

def simple2pt_param_scatter(x: np.array, y: np.array, output_file: str, x_label: str,y_label:str, trend:bool=True):
	output_file = Path(output_file).resolve()
	plt.scatter(x, y, marker='o', s=50, label="Data Points")
	# Fit a quadratic regression model to the data
	coeffs = np.polyfit(x, y, deg=2)
	# Generate points for the quadratic trend line
	if trend:
		quadratic_function = lambda x, a, b, c: a * x**2 + b * x + c
		trend_line_x = np.linspace(min(x), max(x), 1000)
		trend_line_y = quadratic_function(trend_line_x, *coeffs)
		# Plot the quadratic trend line
		plt.plot(trend_line_x, trend_line_y, color='red')#, label="Quadratic Trend Line")
	# label and return
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.title(output_file.stem)
	plt.legend()
	plt.grid(True)
	plt.savefig(output_file)
	plt.clf()

def find_optimal_num_clusters(data, max_clusters=10):
    wcss = []
    for num_clusters in range(1, max_clusters+1):
        kmeans = KMeans(n_clusters=num_clusters)
        kmeans.fit(data)
        wcss.append(kmeans.inertia_)  # Inertia is the WCSS value

    # Find the optimal number of clusters using the elbow method
    optimal_num_clusters = np.argmin(np.diff(wcss)) + 1

    return optimal_num_clusters

def simple2pt_param_scatter_wautocluster(x, y, output_file, x_label='X Axis', y_label='Y Axis', max_clusters=10):
    output_file = Path(output_file).resolve()
    # Create a scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, c='blue', label='Data Points', edgecolors='black')
    # Combine data into a 2D array for clustering
    data = np.column_stack((x, y))
    # Find the optimal number of clusters using the elbow method
    optimal_num_clusters = find_optimal_num_clusters(data, max_clusters)
    # Perform K-means clustering with the determined number of clusters
    kmeans = KMeans(n_clusters=optimal_num_clusters)
    kmeans.fit(data)
    cluster_centers = kmeans.cluster_centers_
    cluster_labels = kmeans.labels_
    # Color code the clusters
    unique_labels = np.unique(cluster_labels)
    colors = plt.cm.tab10.colors
    for i, label in enumerate(unique_labels):
        cluster_data = data[cluster_labels == label]
        cluster_center = cluster_centers[label]
        plt.scatter(cluster_data[:, 0], cluster_data[:, 1], c=colors[i], label=f'Cluster {label}', edgecolors='black')
        plt.scatter(cluster_center[0], cluster_center[1], marker='x', s=100, c=colors[i], edgecolors='black')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(output_file.stem)
    plt.legend()
    plt.grid(True)
    # Save the plot as PNG if output_file is provided
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.clf()


def simple2pt_param_scatter_wcluster(x, y, output_file, x_label='X Axis', y_label='Y Axis', num_clusters=3):
    output_file = Path(output_file).resolve()
    # Create a scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, c='blue', label='Data Points', edgecolors='black')
    # Combine data into a 2D array for clustering
    data = np.column_stack((x, y))
    # Perform K-means clustering with the specified number of clusters
    kmeans = KMeans(n_clusters=num_clusters)
    cluster_labels = kmeans.fit_predict(data)
    # Color code the clusters and label each point
    unique_labels = np.unique(cluster_labels)
    colors = plt.cm.tab10.colors
    for i, label in enumerate(unique_labels):
        cluster_data = data[cluster_labels == label]
        plt.scatter(cluster_data[:, 0], cluster_data[:, 1], c=colors[i], label=f'Cluster {label}', edgecolors='black')
        for point in cluster_data:
            plt.text(point[0], point[1], f'{label}', fontsize=10, ha='center', va='center', color='black')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(output_file.stem)
    #plt.legend()
    plt.grid(True)
    # Save the plot as PNG if output_file is provided
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.clf()


def extract_stats(
	params: Union[np.array,str,Path],
	results: Union[np.array,str,Path],
) -> None:
	# reading files, error checks
	strtopath = lambda strin : Path(strin).resolve() if isinstance(strin,str) else strin
	pathtoarr = lambda datain : np.load(datain.resolve()) if isinstance(datain,Path) else datain
	params_dirty = pathtoarr(strtopath(params))
	results_dirty = pathtoarr(strtopath(results))
	# clean condition eliminates all failed runs AND negative phase margins
	clean_condition = np.where(np.all(results_dirty > 0,axis=1)==True)
	params = params_dirty[clean_condition]
	results = results_dirty[clean_condition]
	if len(params)!=len(results):
		raise ValueError("expect both results and params to be same length")
	# construct dictionary key=colnames: vals=1D np arrays
	col_struct = opamp_parameters_de_serializer()
	colnames_vals = dict()
	for key, val in col_struct.items():
		if type(val)==tuple:
			if len(val)==3:
				colnames = ["width","length","fingers"]
			elif len(val)==4:
				colnames = ["width","length","fingers","multipliers"]
			elif len(val)==2:
				colnames = ["width","length"]
			for colname in colnames:
				colnames_vals[key+"_"+colname] = "place_holder"
		elif type(val)==int:
			colnames_vals[key] = "place_holder"
	for i, colname in enumerate(colnames_vals):
		colnames_vals[colname] = params[:, i]
	
	# run statistics on distribution of training parameters individually
	params_stats_hists = Path("./stats/param_stats/hists1D")
	params_stats_hists.mkdir(parents=True)
	for colname, val in colnames_vals.items():
		save_distwith_best_fit(val,str(params_stats_hists)+"/"+colname+".png",'Parameter Distribution',colname,'Normalized trials')
	# run stats on distribution of training parameters using pair scatter plots
	params_stats_scatter = Path("./stats/param_stats/scatter")
	params_stats_scatter.mkdir(parents=True)
	save_pairwise_scatter_plot(params,str(params_stats_scatter)+"/pairscatter_params.png")
	# run PCA on training parameters
	run_pca_and_save_plot(params,str(params_stats_scatter)+"/PCA_params.png")
	
	# run statistics on results
	result_stats_dir = Path("./stats/result_stats/hist1d")
	result_stats_dir.mkdir(parents=True)
	for i,name in enumerate(opamp_results_de_serializer()):
		save_distwith_best_fit(results[:,i],str(result_stats_dir)+"/result_"+name+"_dist.png",name+" Distribution",name)
	# plot results against each other
	result_stats_verses = Path("./stats/result_stats/compare")
	result_stats_verses.mkdir(parents=True)
	result_combs=list(opamp_results_de_serializer().keys())
	result_unqiue_combs=np.array(np.meshgrid(result_combs, result_combs)).T.reshape(-1, 2)
	for name1, name2 in result_unqiue_combs:
		if name1==name2:
			continue
		index1 = result_combs.index(name1)
		index2 = result_combs.index(name2)
		output_name = str(result_stats_verses)+"/"+name1+"_vs_"+name2+".png"
		simple2pt_param_scatter_wcluster(results[:,index1],results[:,index2],output_name,name1,name2)

	# run stats on results and data combined
	comb_stats_dir = Path("./stats/combined")
	comb_stats_dir.mkdir(parents=True)
	create_pca_biplot_with_clusters(params,results,str(comb_stats_dir)+"/heatmapresults_params.png")
	create_heatmap_with_clusters(params,results,str(comb_stats_dir)+"/heatmap_results_clustered.png")
	for i, name in enumerate(opamp_results_de_serializer()):
		param_stats_isolate = Path("./stats/combined/isolate_params") / name
		param_stats_isolate.mkdir(parents=True)
		param_stats_NOisolate = Path("./stats/combined/NONisolated_params") / name
		param_stats_NOisolate.mkdir(parents=True)
		for j, colname in enumerate(colnames_vals):
			single_param_scatter(params,results,j,str(param_stats_isolate)+"/"+colname+".png",results_index=i)
			single_param_scatter(params,results,j,str(param_stats_NOisolate)+"/"+colname+".png",isolate=False,results_index=i)





# ================ create opamp matrix ==================



def create_opamp_matrix(save_dir_name: str, params: np.array, results: Optional[np.array] = None, indices: Optional[list]=None):
	"""create opamps with pads from the np array of opamp parameters 
	args:
	save_dir_name = name of directory to save gds array and text description into
	params = 2d list-like container (list, np.array, tuple, etc.) where each row is in the same form as opamp_parameters_serializer
	results = (Optional) 2d list-like container (list, np.array, tuple, etc.) where each row is in the same form as opamp_results_serializer
	****NOTE: if results is not specfied, the stats.txt will not list the sim results for each opamp
	indices = (Optional) an iterable of integers where each integer represent an index into the params and results lists
	"""
	# arg setup
	current_setting = pdk.cell_decorator_settings.cache
	pdk.cell_decorator_settings.cache = False
	comps = list()
	if indices is None:
		indices = range(len(params))
	# dir setup
	save_dir = Path(save_dir_name).resolve()
	save_dir.mkdir(parents=True,exist_ok=True)
	# run opamps
	for index in indices:
		# create opamp
		comp = sky130_opamp_add_pads(sky130_add_lvt_layer(opamp(pdk, **opamp_parameters_de_serializer(params[index]))), flatten=False)
		comp = component_snap_to_grid(comp)
		comp.name = "opamp_" + str(index)
		# append to list
		comps.append(comp)
		clear_cache()
		with open(str(save_dir)+"/stats.txt","a") as resfile:
			strtowrite = "\n-------------------------\nopamp_"+str(index)
			strtowrite += "\nparams = " + str(opamp_parameters_de_serializer(params[index]))
			if results is not None:
				strtowrite += "\n\nresults = " + str(opamp_results_de_serializer(results[index]))
			strtowrite += "\n\n\n"
			resfile.write(strtowrite)
	write_opamp_matrix(comps, write_name = str(save_dir) + "/opamp_matrix.gds", xspace=600)
	pdk.cell_decorator_settings.cache = current_setting





if __name__ == "__main__":
	import time
	start_watch = time.time()

	parser = argparse.ArgumentParser(description="sky130 nist tapeout sample, RL generation, and statistics utility.")
	
	subparsers = parser.add_subparsers(title="mode", required=True, dest="mode")

	# Subparser for extract_stats mode
	extract_stats_parser = subparsers.add_parser("extract_stats", help="Run the extract_stats function.")
	extract_stats_parser.add_argument("-p", "--params", default="training_params.npy", help="File path for params (default: training_params.npy)")
	extract_stats_parser.add_argument("-r", "--results", default="training_results.npy", help="File path for results (default: training_results.npy)")

	# Subparser for get_training_data mode
	get_training_data_parser = subparsers.add_parser("get_training_data", help="Run the get_training_data function.")
	get_training_data_parser.add_argument("-t", "--test-mode", action="store_true", help="Set test_mode to True (default: False)")
	get_training_data_parser.add_argument("--temp", type=int, default=int(25), help="Simulation temperature")
	get_training_data_parser.add_argument("--cload", type=float, default=float(0), help="run simulation with load capacitance units=pico Farads")
	get_training_data_parser.add_argument("--noparasitics",action="store_true",help="specify that parasitics should be removed when simulating")
	get_training_data_parser.add_argument("--nparray",default=None,help="overrides the test parameters and takes the ones you provide (file path to .npy file).\n\tMUST HAVE LEN > 1")
	get_training_data_parser.add_argument("--saverawsims",action="store_true",help="specify that the raw simulation directories should be saved (default saved under save_gds_by_index/...)")
	get_training_data_parser.add_argument("--get_tset_len",action="store_true",help="print the length of the default parameter set and quit")
	get_training_data_parser.add_argument("--output_second_stage",action="store_true",help="measure relevant sim metrics at the output of the second stage rather than output of third stage")

	# Subparser for gen_opamp mode
	gen_opamp_parser = subparsers.add_parser("gen_opamp", help="Run the gen_opamp function. optional parameters for transistors are width,length,fingers,mults")
	gen_opamp_parser.add_argument("--half_diffpair_params", nargs=3, type=float, default=[6, 1, 4], help="half_diffpair_params (default: 6 1 4)")
	gen_opamp_parser.add_argument("--diffpair_bias", nargs=3, type=float, default=[6, 2, 4], help="diffpair_bias (default: 6 2 4)")
	gen_opamp_parser.add_argument("--half_common_source_params", nargs=4, type=float, default=[7, 1, 10, 3], help="half_common_source_params (default: 7 1 10 3)")
	gen_opamp_parser.add_argument("--half_common_source_bias", nargs=4, type=float, default=[6, 2, 8, 2], help="half_common_source_bias (default: 6 2 8 3)")
	gen_opamp_parser.add_argument("--output_stage_params", nargs=3, type=float, default=[5, 1, 16], help="pamp_hparams (default: 5 1 16)")
	gen_opamp_parser.add_argument("--output_stage_bias", nargs=3, type=float, default=[6,2,4], help="pamp_hparams (default: 6 2 4)")
	gen_opamp_parser.add_argument("--mim_cap_size", nargs=2, type=int, default=[12, 12], help="mim_cap_size (default: 12 12)")
	gen_opamp_parser.add_argument("--mim_cap_rows", type=int, default=3, help="mim_cap_rows (default: 3)")
	gen_opamp_parser.add_argument("--rmult", type=int, default=2, help="rmult (default: 2)")
	gen_opamp_parser.add_argument("--add_pads",action="store_true" , help="add pads (gen_opamp mode only)")
	gen_opamp_parser.add_argument("--output_gds", help="Filename for outputing opamp (gen_opamp mode only)")

	# subparser for gen_opamps mode
	gen_opamps_parser = subparsers.add_parser("gen_opamps", help="generates the opamps returned in the small parameters list but only saves GDS and does not add pads. always outputs to ./outputrawopamps")
	gen_opamps_parser.add_argument("--pdk", help="specify sky130 or gf180 pdk")

	# subparse for testing mode (create opamp and run sims)
	test = subparsers.add_parser("test", help="Test mode")
	test.add_argument("--output_dir", type=Path, default="./", help="Directory for output GDS file")
	test.add_argument("--temp", type=int, default=int(25), help="Simulation temperature")
	test.add_argument("--cload", type=float, default=float(0), help="run simulation with load capacitance units=pico Farads")
	test.add_argument("--noparasitics",action="store_true",help="specify that parasitics should be removed when simulating")
	test.add_argument("--output_second_stage",action="store_true",help="measure relevant sim metrics at the output of the second stage rather than output of third stage")
	
	# Subparser for create_opamp_matrix mode
	create_opamp_matrix_parser = subparsers.add_parser("create_opamp_matrix", help="create a matrix of opamps")
	create_opamp_matrix_parser.add_argument("-p", "--params", default="params.npy", help="File path for params (default: params.npy)")
	create_opamp_matrix_parser.add_argument("-r", "--results", help="Optional File path for results")
	create_opamp_matrix_parser.add_argument("--indices", type=int, nargs="+", help="list of int indices to pick from the opamp param.npy and add to the matrix (default: the entire params list)")
	create_opamp_matrix_parser.add_argument("--output_dir", type=Path, default="./opampmatrix", help="Directory for output files (default: ./opampmatrix)")

	for prsr in [get_training_data_parser,gen_opamp_parser,test,create_opamp_matrix_parser]:
		prsr.add_argument("--no_lvt",action="store_true",help="do not place any low threshold voltage transistors.")
		prsr.add_argument("--PDK_ROOT",type=Path,default="/usr/bin/miniconda3/share/pdk/",help="path to the sky130 PDK library")
	
	args = parser.parse_args()

	if args.mode in ["get_training_data","test","gen_opamps","create_opamp_matrix"]:
		__NO_LVT_GLOBAL_ = args.no_lvt
		PDK_ROOT = Path(args.PDK_ROOT).resolve()
		if not(PDK_ROOT.is_dir()):
			raise ValueError("PDK_ROOT is not a valid directory\n")
		PDK_ROOT = str(PDK_ROOT)
	
	# Simulation Temperature information
	if vars(args).get("temp") is not None:
		temperature_info = [args.temp, None]
		if temperature_info[0] > -20:
			temperature_info[1] = "normal model"
		elif temperature_info[0]!=-269:
			raise ValueError("simulation temperature should be exactly -269C for cryo sim. Below -20C there are no good models for simulation")
		else:
			temperature_info[1] = "cryo model"
		temperature_info = tuple(temperature_info)

	if args.mode=="extract_stats":
		# Call the extract_stats function with the specified file paths or defaults
		extract_stats(params=args.params, results=args.results)

	elif args.mode=="get_training_data":
		if args.get_tset_len:
			_GET_PARAM_SET_LENGTH_ = True
		if args.output_second_stage:
			_TAKE_OUTPUT_AT_SECOND_STAGE_ = True
		# Call the get_training_data function with test_mode flag
		parameter_array = None
		if args.nparray is not None:
			parameter_array = Path(args.nparray).resolve()
			assert(parameter_array.is_file())
			parameter_array = np.load(parameter_array)
		get_training_data(test_mode=args.test_mode, temperature_info=temperature_info, cload=args.cload, noparasitics=args.noparasitics, parameter_array=parameter_array, saverawsims=args.saverawsims)

	elif args.mode=="gen_opamp":
		# Call the opamp function with the parsed arguments
		opamp_comp = opamp(pdk=pdk,
				half_diffpair_params=tuple(args.half_diffpair_params),
				diffpair_bias=tuple(args.diffpair_bias),
				half_common_source_bias=tuple(args.half_common_source_bias),
				half_common_source_params=tuple(args.half_common_source_params),
				output_stage_params = tuple(args.output_stage_params),
				output_stage_bias = tuple(args.output_stage_bias),
				mim_cap_size=tuple(args.mim_cap_size),
				mim_cap_rows=args.mim_cap_rows,
				rmult=args.rmult,
			)
		opamp_comp = sky130_add_lvt_layer(opamp_comp)
		if args.add_pads:
			opamp_comp_labels = sky130_add_opamp_labels(opamp_comp)
			opamp_comp_final = sky130_opamp_add_pads(opamp_comp_labels)
		else:
			opamp_comp_final = opamp_comp
		opamp_comp_final.show()
		if args.output_gds:
			opamp_comp_final.write_gds(args.output_gds)

	elif args.mode == "test":
		if args.output_second_stage:
			_TAKE_OUTPUT_AT_SECOND_STAGE_ = True
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
		results = single_build_and_simulation(opamp_parameters_serializer(**params), temperature_info[0], args.output_dir, cload=args.cload, noparasitics=args.noparasitics)
		print(results)

	elif args.mode =="create_opamp_matrix":
		params = Path(args.params).resolve()
		params = np.load(str(params))
		results = Path(args.results).resolve() if args.results else None
		results = np.load(str(results)) if results else None
		if args.indices is not None:
			indices = args.indices if isinstance(args.indices, Iterable) else [args.indices]
		else:
			indices = None
		create_opamp_matrix(args.output_dir,params,results,indices)
		
	
	elif args.mode == "gen_opamps":
		global usepdk
		if args.pdk[0].lower()=="g":
			from glayout.pdk.gf180_mapped import gf180_mapped_pdk
			usepdk = gf180_mapped_pdk
		else:
			usepdk = pdk
		output_path = Path("./outputrawopamps").resolve()
		output_path.mkdir()
		def create_func(argnparray, indx: int):
			global usepdk
			comp = opamp(usepdk,**opamp_parameters_de_serializer(argnparray))
			comp.write_gds("./outputrawopamps/amp"+str(indx)+".gds")
		
		argnparray = get_small_parameter_list()
		with Pool(120) as cores:
			cores.starmap(create_func, zip(argnparray,count(0)))
	
	end_watch = time.time()
	print("\ntotal runtime was "+str((end_watch-start_watch)/3600) + " hours\n")
