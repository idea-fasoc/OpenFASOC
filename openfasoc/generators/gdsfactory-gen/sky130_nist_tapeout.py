import sys
# path to pygen
sys.path.append('./pygen')

from gdsfactory.read.import_gds import import_gds
from gdsfactory.components import text_freetype, rectangle
from pygen.pdk.util.custom_comp_utils import prec_array, add_ports_perimeter, movey, print_ports, align_comp_to_port
from gdsfactory.component import Component
from pygen.pdk.mappedpdk import MappedPDK
from pygen.opamp import opamp
from pygen.L_route import L_route
from pygen.straight_route import straight_route
from pygen.via_gen import via_array
from pygen.pdk.util.standard_main import pdk, parser
from gdsfactory.cell import cell, clear_cache
import numpy as np
from subprocess import Popen
from pathlib import Path
from typing import Union
from tempfile import TemporaryDirectory
from shutil import copyfile, copytree
from multiprocessing import Pool


def sky130_opamp_add_pads(opamp_in: Component) -> Component:
	"""adds the MPW-5 pads and nano pads to opamp.
	Also adds text labels and pin layers so that extraction is nice
	"""
	opamp_wpads = opamp_in.copy()
	opamp_wpads = movey(opamp_wpads, destination=0)
	# create pad array and add to opamp
	pad = import_gds("sky130_mpw5_pad.gds")
	pad.name = "mpw5pad"
	pad = add_ports_perimeter(pad, pdk.get_glayer("met4"),prefix="pad_")
	pad_array = prec_array(pad, rows=2, columns=(4+1), spacing=(40,120))
	pad_array_ref = pad_array.ref_center()
	opamp_wpads.add(pad_array_ref)
	# add via_array to vdd pin
	vddarray = via_array(pdk, "met4","met5",size=(opamp_wpads.ports["vdd_pin_N"].width,opamp_wpads.ports["vdd_pin_E"].width))
	via_array_ref = opamp_wpads << vddarray
	align_comp_to_port(via_array_ref,opamp_wpads.ports["vdd_pin_N"],alignment=('c','b'))
	# route to the pads
	opamp_wpads << L_route(pdk, opamp_wpads.ports["minus_pin_W"],pad_array_ref.ports["row1_col1_pad_S"],hwidth=3)
	opamp_wpads << L_route(pdk, opamp_wpads.ports["plus_pin_W"],pad_array_ref.ports["row0_col1_pad_N"],hwidth=3)
	opamp_wpads << L_route(pdk, opamp_wpads.ports["vbias2_pin_E"],pad_array_ref.ports["row0_col2_pad_N"],hwidth=3)
	opamp_wpads << L_route(pdk, opamp_wpads.ports["vbias1_pin_E"],pad_array_ref.ports["row0_col3_pad_N"],hwidth=3)
	opamp_wpads << L_route(pdk, opamp_wpads.ports["gnd_route_con_E"],pad_array_ref.ports["row1_col4_pad_S"],hwidth=3,vglayer="met5")
	opamp_wpads << L_route(pdk, opamp_wpads.ports["vdd_pin_N"],pad_array_ref.ports["row1_col2_pad_E"],vwidth=4,vglayer="met5")
	opamp_wpads << L_route(pdk, opamp_wpads.ports["output_pin_E"],pad_array_ref.ports["row0_col4_pad_N"],hwidth=3,vglayer="met5")
	# add pin layer and text labels for LVS
	text_pin_labels = list()
	met5pin = rectangle(size=(5,5),layer=(72,16), centered=True)
	for name in ["plus","vbias2","vbias1","output","minus","vdd","NC","gnd"]:
		pin_w_label = met5pin.copy()
		pin_w_label.add_label(text=name,layer=(72,5),magnification=4)
		text_pin_labels.append(pin_w_label)
	for row in range(2):
		for col_u in range(4):
			col = col_u + 1# left most are for nano pads
			if row==1 and col==2+1:
				continue
			port_name = "row"+str(row)+"_col"+str(col)+"_pad_S"
			pad_array_port = pad_array_ref.ports[port_name]
			pin_ref = opamp_wpads << text_pin_labels[4*row + col_u]
			align_comp_to_port(pin_ref,pad_array_port,alignment=('c','t'))
	# import nano pad and add to opamp
	nanopad = import_gds("sky130_nano_pad.gds")
	nanopad.name = "nanopad"
	nanopad = add_ports_perimeter(nanopad, pdk.get_glayer("met4"),prefix="nanopad_")
	nanopad_array = prec_array(nanopad, rows=2, columns=2, spacing=(10,10))
	nanopad_array_ref = nanopad_array.ref_center()
	opamp_wpads.add(nanopad_array_ref)
	nanopad_array_ref.movex(opamp_wpads.xmin+nanopad_array.xmax)
	# route nano pad connections
	opamp_wpads << straight_route(pdk, nanopad_array_ref.ports["row1_col0_nanopad_N"],pad_array_ref.ports["row1_col0_pad_S"],width=3)
	opamp_wpads << straight_route(pdk, nanopad_array_ref.ports["row0_col0_nanopad_S"],pad_array_ref.ports["row0_col0_pad_N"],width=3)
	opamp_wpads << straight_route(pdk, nanopad_array_ref.ports["row0_col1_nanopad_E"],pad_array_ref.ports["row0_col1_pad_N"],width=3)
	opamp_wpads << straight_route(pdk, nanopad_array_ref.ports["row1_col1_nanopad_E"],pad_array_ref.ports["row1_col1_pad_S"],width=3)
	#vddnanopad = opamp_wpads << nanopad
	#opamp_wpads << nanopad
	return opamp_wpads.flatten()


def sky130_add_opamp_labels(opamp_in: Component) -> Component:
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
	move_info.append((gndlabel,opamp_in.ports["gnd_pin_N"]))
	#vbias1
	vbias1label = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
	vbias1label.add_label(text="vbias1",layer=met2_label)
	move_info.append((vbias1label,opamp_in.ports["vbias1_pin_N"]))
	# vbias2
	vbias2label = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
	vbias2label.add_label(text="vbias2",layer=met2_label)
	move_info.append((vbias2label,opamp_in.ports["vbias2_pin_N"]))
	#minus
	minuslabel = rectangle(layer=met3_pin,size=(1,1),centered=True).copy()
	minuslabel.add_label(text="minus",layer=met3_label)
	move_info.append((minuslabel,opamp_in.ports["minus_pin_N"]))
	#-plus
	pluslabel = rectangle(layer=met3_pin,size=(1,1),centered=True).copy()
	pluslabel.add_label(text="plus",layer=met3_label)
	move_info.append((pluslabel,opamp_in.ports["plus_pin_N"]))
	#vdd
	vddlabel = rectangle(layer=met3_pin,size=(1,1),centered=True).copy()
	vddlabel.add_label(text="vdd",layer=met3_label)
	move_info.append((vddlabel,opamp_in.ports["vdd_pin_N"]))
	# output
	outputlabel = rectangle(layer=met4_pin,size=(1,1),centered=True).copy()
	outputlabel.add_label(text="output",layer=met4_label)
	move_info.append((outputlabel,opamp_in.ports["output_pin_N"]))
	# move everything to position
	for comp, prt in move_info:
		compref = align_comp_to_port(comp, prt, alignment=('c','b'))
		opamp_in.add(compref)
	return opamp_in.flatten()


def opamp_parameters_serializer(
	diffpair_params: tuple[float, float, int] = (6, 1, 4),
	diffpair_bias: tuple[float, float, int] = (6, 2, 4),
	houtput_bias: tuple[float, float, int, int] = (6, 2, 8, 3),
	pamp_hparams: tuple[float, float, int, int] = (7, 1, 10, 3),
	mim_cap_size=(12, 12),
	mim_cap_rows=3
) -> np.array:
	"""converts opamp params into the uniform numpy float format"""
	return np.array(
		[diffpair_params[0],diffpair_params[1],diffpair_params[2],
		diffpair_bias[0],diffpair_bias[1],diffpair_bias[2],
		houtput_bias[0],houtput_bias[1],houtput_bias[2],houtput_bias[3],
		pamp_hparams[0],pamp_hparams[1],pamp_hparams[2],pamp_hparams[3],
		mim_cap_size[0],mim_cap_size[1],
		mim_cap_rows],
		dtype=np.float64
	)

def opamp_parameters_de_serializer(serialized_params: np.array) -> dict:
	"""converts uniform numpy float format to opamp kwargs"""
	if not len(serialized_params) == 17:
		raise ValueError("serialized_params should be a length 15 array")
	params_dict = dict()
	params_dict["diffpair_params"] = tuple(serialized_params[0:3])
	params_dict["diffpair_bias"] = tuple(serialized_params[3:6])
	params_dict["houtput_bias"] = tuple(serialized_params[6:10])
	params_dict["pamp_hparams"] = tuple(serialized_params[10:14])
	params_dict["mim_cap_size"] = tuple(serialized_params[14:16])
	params_dict["mim_cap_rows"] = int(serialized_params[16])
	return params_dict


def get_small_parameter_list(test_mode = False) -> np.array:
	"""creates small parameter list intended for brute force"""
	# all diffpairs to try
	diffpairs = list()
	if test_mode:
		diffpairs.append((6,1,4))
		diffpairs.append((5,1,4))
	else:
		for width in [3,6,9]:
			for length in [0.3,1, 2]:
				for fingers in [2,6]:
					diffpairs.append((width,length,fingers))
	# all bias2 (output amp bias) transistors
	bias2s = list()
	if test_mode:
		bias2s.append((6,1,4,3))
	else:
		for width in [3,6,9]:
			for length in [1]:
				for fingers in [2,6]:
					bias2s.append((width,length,fingers,3))
	# all output pmos transistors
	pamp_hparams = list()
	if test_mode:
		pamp_hparams.append((7,1,8,3))
	else:
		for width in [4,7,10]:
			for length in [0.3,1,2]:
				for fingers in [6,14]:
					pamp_hparams.append((width,length,fingers,3))
	# rows of the cap array to try
	cap_arrays = [2,3]
	# ******************************************
	# create and return the small parameters list
	short_list_len = len(diffpairs) * len(bias2s) * len(pamp_hparams) * len(cap_arrays)
	short_list = np.empty(shape=(short_list_len,len(opamp_parameters_serializer())),dtype=np.float64)
	index = 0
	for diffpair_v in diffpairs:
		for bias2_v in bias2s:
			for pamp_o_v in pamp_hparams:
				for cap_array_v in cap_arrays:
					tup_to_add = opamp_parameters_serializer(
						diffpair_params=diffpair_v, 
						houtput_bias=bias2_v, 
						mim_cap_rows=cap_array_v, 
						pamp_hparams=pamp_o_v
					)
					short_list[index] = tup_to_add
					index = index + 1
	return short_list


def get_big_parameter_list() -> np.array:
	"""creates a large parameters list intended for the neural network"""
	raise NotImplementedError("TODO")
	return




def get_result(filepath: Union[str,Path]):
	fileabspath = Path(filepath).resolve()
	with open(fileabspath, "r") as ResultReport:
		RawResult = ResultReport.readline()
		Columns = RawResult.split(" ")
	if len(columns)<11:
		return {"UGB":-123.45,"biasVoltage1":-123.45,"biasVoltage2":-123.45}
	return {
		"UGB": Columns[3],
		"biasVoltage1": Columns[7],
		"biasVoltage2": Columns[11]
	}

def standardize_netlist_subckt_def(netlist: Union[str,Path]):
	netlist = Path(netlist).resolve()
	if not netlist.is_file():
		raise ValueError("netlist must be file")
	hints = [".subckt","output","plus","minus","vbias1","vbias2"]
	subckt_lines = list()
	with open(netlist, "r") as spice_net:
		subckt_lines = spice_net.readlines()
		for i,line in enumerate(subckt_lines):
			if all([hint in line for hint in hints]):
				subckt_lines[i] = ".subckt opamp minus plus vbias1 vbias2 output vdd gnd\n"
			if "floating" in line.lower():
				subckt_lines[i] = "\n"
	with open(netlist, "w") as spice_net:
		spice_net.writelines(subckt_lines)

def __run_single_brtfrc(parameters_ele):
	# generate layout
	global pdk
	sky130pdk = pdk
	params = opamp_parameters_de_serializer(parameters_ele)
	opamp_v = sky130_add_opamp_labels(opamp(sky130pdk, **params))
	opamp_v.name = "opamp"
	# use temp dir
	with TemporaryDirectory() as tmpdirname:
		tmp_gds_path = Path(opamp_v.write_gds(gdsdir=tmpdirname)).resolve()
		copyfile("extract.bash",str(tmpdirname)+"/extract.bash")
		copyfile("opamp_perf_eval.sp",str(tmpdirname)+"/opamp_perf_eval.sp")
		copytree("sky130A",str(tmpdirname)+"/sky130A")
		# extract layout
		Popen(["bash","extract.bash", tmp_gds_path, opamp_v.name],cwd=tmpdirname).wait()
		standardize_netlist_subckt_def(str(tmpdirname)+"/opamp_pex.spice")
		# run sim and store result
		Popen(["ngspice","-b","opamp_perf_eval.sp"],cwd=tmpdirname).wait()
		return get_result(str(tmpdirname)+"/output.txt")["UGB"]

def brute_force_full_layout_and_PEXsim(sky130pdk: MappedPDK, parameter_list: np.array) -> np.array:
	"""runs the brute force testing of parameters by
	1-constructing the opamp layout specfied by parameters
	2-extracting the netlist for the opamp
	3-running simulations on the opamp
	returns the ugb of the opamps
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
	with Pool(120) as cores:
		results = np.array(cores.map(__run_single_brtfrc, parameter_list),np.float64)
	# undo pdk modification
	sky130pdk.default_decorator = add_npc_decorator
	return results


def get_training_data(test_mode=True,):
	params = get_small_parameter_list(test_mode)
	results = brute_force_full_layout_and_PEXsim(pdk, params)
	np.save("training_params.npy",params)
	np.save("training_results.npy",results)


#parser.add_argument("--test_mode", "-t", action="store_true", help="runs a short 2 ele test")
#args = parser.parse_args()
#get_training_data(test_mode=args.test_mode)

opamp_out = sky130_opamp_add_pads(opamp(pdk))
#sky130_add_opamp_labels(opamp_in).show()
opamp_out.show()


#parameters = np.array()
#result = array()
#for i, comp in enumerate(opamps):
#	comp.write_gds(str(i)+".gds")


# generate opamps
