import sys
# path to pygen
sys.path.append('./pygen')

from gdsfactory.read.import_gds import import_gds
from gdsfactory.components import text_freetype, rectangle
from pygen.pdk.util.comp_utils import prec_array, movey, align_comp_to_port
from pygen.pdk.util.port_utils import add_ports_perimeter, print_ports
from gdsfactory.component import Component
from pygen.pdk.mappedpdk import MappedPDK
from pygen.opamp import opamp
from pygen.L_route import L_route
from pygen.straight_route import straight_route
from pygen.via_gen import via_array
from gdsfactory.cell import cell, clear_cache
import numpy as np
from subprocess import Popen
from pathlib import Path
from typing import Union, Optional
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
from pygen.pdk.sky130_mapped import sky130_mapped_pdk as pdk


# ====Build Opamp====


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



# ====Run Training====



def opamp_parameters_serializer(
	diffpair_params: tuple[float, float, int] = (6, 1, 4),
	diffpair_bias: tuple[float, float, int] = (6, 2, 4),
	houtput_bias: tuple[float, float, int, int] = (6, 2, 8, 3),
	pamp_hparams: tuple[float, float, int, int] = (7, 1, 10, 3),
	mim_cap_size: tuple[int,int]=(12, 12),
	mim_cap_rows: int=3,
	rmult: int=2
) -> np.array:
	"""converts opamp params into the uniform numpy float format"""
	return np.array(
		[diffpair_params[0],diffpair_params[1],diffpair_params[2],
		diffpair_bias[0],diffpair_bias[1],diffpair_bias[2],
		houtput_bias[0],houtput_bias[1],houtput_bias[2],houtput_bias[3],
		pamp_hparams[0],pamp_hparams[1],pamp_hparams[2],pamp_hparams[3],
		mim_cap_size[0],mim_cap_size[1],
		mim_cap_rows,
		rmult],
		dtype=np.float64
	)

def opamp_parameters_de_serializer(serialized_params: Optional[np.array]=None) -> dict:
	"""converts uniform numpy float format to opamp kwargs"""
	if serialized_params is None:
		serialized_params = 18*[-987.654321]
		serialized_params[16] = int(-987.654321)
		serialized_params[17] = int(-987.654321)
	if not len(serialized_params) == 18:
		raise ValueError("serialized_params should be a length 18 array")
	params_dict = dict()
	params_dict["diffpair_params"] = tuple(serialized_params[0:3])
	params_dict["diffpair_bias"] = tuple(serialized_params[3:6])
	params_dict["houtput_bias"] = tuple(serialized_params[6:10])
	params_dict["pamp_hparams"] = tuple(serialized_params[10:14])
	params_dict["mim_cap_size"] = tuple(serialized_params[14:16])
	params_dict["mim_cap_rows"] = int(serialized_params[16])
	params_dict["rmult"] = int(serialized_params[17])
	return params_dict

def opamp_results_serializer(
	ugb: float = -987.654321,
	dcGain: float = -987.654321,
	phaseMargin: float = -987.654321,
	biasVoltage1: float = -987.654321,
	biasVoltage2: float = -987.654321,
	area: float = -987.654321,
	power: float = -987.654321,
	noise: float = -987.654321
) -> np.array:
	return np.array([ugb, dcGain, phaseMargin, biasVoltage1, biasVoltage2, area, power, noise], dtype=np.float64)

def opamp_results_de_serializer(
	results: Optional[np.array]=None
) -> dict:
	if results is None:
		results = 8*[-987.654321]
	if not len(results) == 8:
		raise ValueError("results should be a length 5 array")
	results_dict = dict()
	results_dict["ugb"] = float(results[0])
	results_dict["dcGain"] = float(results[1])
	results_dict["phaseMargin"] = float(results[2])
	results_dict["biasVoltage1"] = float(results[3])
	results_dict["biasVoltage2"] = float(results[4])
	results_dict["area"] = float(results[5])
	results_dict["power"] = float(results[6])
	results_dict["noise"] = float(results[7])
	return results_dict

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
	# routing mults to try
	rmults = [1,2]
	# ******************************************
	# create and return the small parameters list
	short_list_len = len(diffpairs) * len(bias2s) * len(pamp_hparams) * len(cap_arrays) * len(rmults)
	short_list = np.empty(shape=(short_list_len,len(opamp_parameters_serializer())),dtype=np.float64)
	index = 0
	for diffpair_v in diffpairs:
		for bias2_v in bias2s:
			for pamp_o_v in pamp_hparams:
				for cap_array_v in cap_arrays:
					for rmult in rmults:
						tup_to_add = opamp_parameters_serializer(
							diffpair_params=diffpair_v, 
							houtput_bias=bias2_v, 
							mim_cap_rows=cap_array_v, 
							pamp_hparams=pamp_o_v,
							rmult=rmult,
						)
						short_list[index] = tup_to_add
						index = index + 1
	return short_list



def get_sim_results(acpath: Union[str,Path], dcpath: Union[str,Path], noisepath: Union[str,Path]):
	acabspath = Path(acpath).resolve()
	dcabspath = Path(dcpath).resolve()
	noiseabspath = Path(noisepath).resolve()
	with open(acabspath, "r") as ACReport:
		RawAC = ACReport.readlines()[0]
		ACColumns = [item for item in RawAC.split() if item]
	with open(dcabspath, "r") as DCReport:
		RawDC = DCReport.readlines()[0]
		DCColumns = [item for item in RawDC.split() if item]
	with open(noiseabspath, "r") as NoiseReport:
		RawNoise = NoiseReport.readlines()[0]
		NoiseColumns = [item for item in RawNoise.split() if item]
	na = -987.654321
	if ACColumns is None or len(ACColumns)<9:
		return {"ugb":na,"biasVoltage1":na,"biasVoltage2":na,"phaseMargin":na,"dcGain":na,"power":na,"noise":na}
	if DCColumns is None or len(DCColumns)<2:
		return {"ugb":na,"biasVoltage1":na,"biasVoltage2":na,"phaseMargin":na,"dcGain":na,"power":na,"noise":na}
	if NoiseColumns is None or len(NoiseColumns)<2:
		return {"ugb":na,"biasVoltage1":na,"biasVoltage2":na,"phaseMargin":na,"dcGain":na,"power":na,"noise":na}
	return_dict = {
		"ugb": ACColumns[1],
		"biasVoltage1": ACColumns[3],
		"biasVoltage2": ACColumns[5],
		"phaseMargin": ACColumns[7],
		"dcGain": ACColumns[9],
		"power": DCColumns[1],
		"noise": NoiseColumns[1]
	}
	for key, val in return_dict.items():
		val_flt = na
		try:
			val_flt = float(val)
		except ValueError:
			val_flt = na
		return_dict[key] = val_flt
	return return_dict

def standardize_netlist_subckt_def(netlist: Union[str,Path], sim_temperature: Optional[float] = float(27)):
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

def __run_single_brtfrc(index, parameters_ele, output_dir: Optional[Union[str,Path]] = None):
	# generate layout
	global pdk
	global save_gds_dir
	global SIM_TEMP
	destination_gds_copy = save_gds_dir / (str(index)+".gds")
	sky130pdk = pdk
	params = opamp_parameters_de_serializer(parameters_ele)
	opamp_v = sky130_add_opamp_labels(opamp(sky130pdk, **params))
	opamp_v.name = "opamp"
	area = float(opamp_v.area())
	# use temp dir
	with TemporaryDirectory() as tmpdirname:
		tmp_gds_path = Path(opamp_v.write_gds(gdsdir=tmpdirname)).resolve()
		if tmp_gds_path.is_file():
			destination_gds_copy.write_bytes(tmp_gds_path.read_bytes())
		copyfile("extract.bash",str(tmpdirname)+"/extract.bash")
		copyfile("opamp_perf_eval.sp",str(tmpdirname)+"/opamp_perf_eval.sp")
		copytree("sky130A",str(tmpdirname)+"/sky130A")
		# extract layout
		Popen(["bash","extract.bash", tmp_gds_path, opamp_v.name],cwd=tmpdirname).wait()
		print("Running simulation at temperature: " + str(SIM_TEMP) + "C")
		spice_lines = list()
		with open(str(tmpdirname)+"/opamp_perf_eval.sp", "r") as spice_file:
			spice_lines = spice_file.readlines()
			print("BEFORE REPL: " + spice_lines[5])
			spice_lines[5] = spice_lines[5].replace('{@@TEMP}', str(int(SIM_TEMP)))
			print("AFTER REPL: " + spice_lines[5])
		with open(str(tmpdirname)+"/opamp_perf_eval.sp", "w") as spice_file:
			spice_file.writelines(spice_lines)
		standardize_netlist_subckt_def(str(tmpdirname)+"/opamp_pex.spice", SIM_TEMP)
		# run sim and store result
		Popen(["ngspice","-b","opamp_perf_eval.sp"],cwd=tmpdirname).wait()
		result_dict = get_sim_results(str(tmpdirname)+"/result_ac.txt", str(tmpdirname)+"/result_power.txt", str(tmpdirname)+"/result_noise.txt")
		result_dict["area"] = area
		results = opamp_results_serializer(**result_dict)
		if output_dir: 
			output_dir = Path(output_dir).resolve()
			if not output_dir.is_dir():
				raise ValueError("Output directory must be a directory")
			copytree(str(tmpdirname), str(output_dir)+"/test_output", dirs_exist_ok=True)
		return results

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
	global save_gds_dir
	save_gds_dir = Path('./save_gds_by_index').resolve()
	save_gds_dir.mkdir(parents=True)
	with Pool(120) as cores:
		results = np.array(cores.starmap(__run_single_brtfrc, enumerate(parameter_list)),np.float64)
	# undo pdk modification
	sky130pdk.default_decorator = add_npc_decorator
	return results


def get_training_data(test_mode=True,):
	params = get_small_parameter_list(test_mode)
	results = brute_force_full_layout_and_PEXsim(pdk, params)
	np.save("training_params.npy",params)
	np.save("training_results.npy",results)


#util function for pure simulation
def single_build_and_simulation(parameters: np.array, output_dir: Optional[Union[str,Path]] = None) -> np.array:
	"""Builds, extract, and simulates a single opamp
	saves opamp gds in current directory with name 12345678987654321.gds
	"""
	global pdk
	global save_gds_dir
	pdk = pdk
	save_gds_dir = Path('./').resolve()
	index = 12345678987654321
	return __run_single_brtfrc(index, parameters, output_dir)


#======stats=======



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





if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="sky130 nist tapeout sample, RL generation, and statistics utility.")
	subparsers = parser.add_subparsers(title="mode", required=True, dest="mode")

	# Subparser for extract_stats mode
	extract_stats_parser = subparsers.add_parser("extract_stats", help="Run the extract_stats function.")
	extract_stats_parser.add_argument("-p", "--params", default="training_params.npy", help="File path for params (default: training_params.npy)")
	extract_stats_parser.add_argument("-r", "--results", default="training_results.npy", help="File path for results (default: training_results.npy)")

	# Subparser for get_training_data mode
	get_training_data_parser = subparsers.add_parser("get_training_data", help="Run the get_training_data function.")
	get_training_data_parser.add_argument("-t", "--test-mode", action="store_true", help="Set test_mode to True (default: False)")

	# Subparser for gen_opamp mode
	gen_opamp_parser = subparsers.add_parser("gen_opamp", help="Run the gen_opamp function.")
	gen_opamp_parser.add_argument("--diffpair_params", nargs=3, type=float, default=[6, 1, 4], help="diffpair_params (default: 6 1 4)")
	gen_opamp_parser.add_argument("--diffpair_bias", nargs=3, type=float, default=[6, 2, 4], help="diffpair_bias (default: 6 2 4)")
	gen_opamp_parser.add_argument("--houtput_bias", nargs=4, type=float, default=[6, 2, 8, 3], help="houtput_bias (default: 6 2 8 3)")
	gen_opamp_parser.add_argument("--pamp_hparams", nargs=4, type=float, default=[7, 1, 10, 3], help="pamp_hparams (default: 7 1 10 3)")
	gen_opamp_parser.add_argument("--mim_cap_size", nargs=2, type=int, default=[12, 12], help="mim_cap_size (default: 12 12)")
	gen_opamp_parser.add_argument("--mim_cap_rows", type=int, default=3, help="mim_cap_rows (default: 3)")
	gen_opamp_parser.add_argument("--rmult", type=int, default=2, help="rmult (default: 2)")
	gen_opamp_parser.add_argument("--add_pads",action="store_true" , help="add pads (gen_opamp mode only)")
	gen_opamp_parser.add_argument("--output_gds", help="Filename for outputing opamp (gen_opamp mode only)")
	gen_opamp_parser.add_argument("--temp", type=float, default=float(27), help="Simulation temperature")

	# Testing
	test = subparsers.add_parser("test", help="Test mode")
	test.add_argument("--output_dir", type=Path, default="./", help="Directory for output GDS file")
	test.add_argument("--temp", type=float, default=float(27), help="Simulation temperature")
	
	args = parser.parse_args()

	# Simulation Temperature
	global SIM_TEMP
	SIM_TEMP = args.temp

	if args.mode=="extract_stats":
		# Call the extract_stats function with the specified file paths or defaults
		extract_stats(params=args.params, results=args.results)

	elif args.mode=="get_training_data":
		# Call the get_training_data function with test_mode flag
		get_training_data(test_mode=args.test_mode)

	elif args.mode=="gen_opamp":
		from pygen.pdk.sky130_mapped.sky130_mapped import sky130_mapped_pdk as pdk
		# Call the opamp function with the parsed arguments
		diffpair_params = tuple(args.diffpair_params)
		diffpair_bias = tuple(args.diffpair_bias)
		houtput_bias = tuple(args.houtput_bias)
		pamp_hparams = tuple(args.pamp_hparams)
		mim_cap_size = tuple(args.mim_cap_size)
		mim_cap_rows = args.mim_cap_rows
		rmult = args.rmult
		opamp_comp = opamp(pdk=pdk,
				diffpair_params=diffpair_params,
				diffpair_bias=diffpair_bias,
				houtput_bias=houtput_bias,
				pamp_hparams=pamp_hparams,
				mim_cap_size=mim_cap_size,
				mim_cap_rows=mim_cap_rows,
				rmult=rmult,
			)
		if args.add_pads:
			opamp_comp_labels = sky130_add_opamp_labels(opamp_comp)
			opamp_comp_final = sky130_opamp_add_pads(opamp_comp_labels)
		else:
			opamp_comp_final = opamp_comp
		opamp_comp_final.show()
		if args.output_gds:
			opamp_comp_final.write_gds(args.output_gds)

	elif args.mode == "test":
		params = {
			"diffpair_params": (6, 1, 4),
			"diffpair_bias": (6, 2, 4),
			"houtput_bias": (6, 2, 8, 3),
			"pamp_hparams": (7, 1, 10, 3),
			"mim_cap_size": (12, 12),
			"mim_cap_rows": 3,
			"rmult": 2
		}
		single_build_and_simulation(opamp_parameters_serializer(**params), args.output_dir)
