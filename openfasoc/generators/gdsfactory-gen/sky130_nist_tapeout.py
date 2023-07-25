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
	area: float = -987.654321
) -> np.array:
	return np.array([ugb, dcGain, phaseMargin, biasVoltage1, biasVoltage2, area], dtype=np.float64)

def opamp_results_de_serializer(
	results: np.array
) -> dict:
	if not len(serialized_params) == 6:
		raise ValueError("results should be a length 5 array")
	results_dict = dict()
	results_dict["ugb"] = float(serialized_params[0])
	results_dict["dcGain"] = float(serialized_params[1])
	results_dict["phaseMargin"] = float(serialized_params[2])
	results_dict["biasVoltage1"] = float(serialized_params[3])
	results_dict["biasVoltage2"] = float(serialized_params[4])
	results_dict["area"] = float(serialized_params[5])
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



def get_sim_results(filepath: Union[str,Path]):
	fileabspath = Path(filepath).resolve()
	with open(fileabspath, "r") as ResultReport:
		RawResult = ResultReport.readlines()[0]
		Columns = [item for item in RawResult.split() if item]
	na = -987.654321
	if len(Columns)<9 or Columns is None:
		return {"ugb":na,"biasVoltage1":na,"biasVoltage2":na,"phaseMargin":na,"dcGain":na}
	return_dict = {
		"ugb": Columns[1],
		"biasVoltage1": Columns[3],
		"biasVoltage2": Columns[5],
		"phaseMargin": Columns[7],
		"dcGain": Columns[9]
	}
	for key, val in return_dict.items():
		val_flt = na
		try:
			val_flt = float(val)
		except ValueError:
			val_flt = na
		return_dict[key] = val_flt
	return return_dict

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

def __run_single_brtfrc(index, parameters_ele):
	# generate layout
	global pdk
	global save_gds_dir
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
		standardize_netlist_subckt_def(str(tmpdirname)+"/opamp_pex.spice")
		# run sim and store result
		Popen(["ngspice","-b","opamp_perf_eval.sp"],cwd=tmpdirname).wait()
		result_dict = get_sim_results(str(tmpdirname)+"/output.txt")
		result_dict["area"] = area
		results = opamp_results_serializer(**result_dict)
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


parser.add_argument("--test_mode", "-t", action="store_true", help="runs a short 2 ele test")
args = parser.parse_args()
get_training_data(test_mode=args.test_mode)

#opamp_out = sky130_opamp_add_pads(opamp(pdk))
#sky130_add_opamp_labels(opamp_in).show()
#opamp_out.show()


#parameters = np.array()
#result = array()
#for i, comp in enumerate(opamps):
#	comp.write_gds(str(i)+".gds")


# generate opamps


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

def create_pca_biplot_with_clusters(data, results, output_file, max_clusters=10):
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
    plt.scatter(pca_result[:, 0], pca_result[:, 1], c=results, cmap='viridis', edgecolor='k', s=80)
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

def create_heatmap_with_clusters(parameters, results, output_file, max_clusters=10):
    if isinstance(parameters, pd.DataFrame):
        parameters = parameters.to_numpy()
    if isinstance(results, pd.Series):
        results = results.to_numpy()
    # Perform PCA
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(parameters)
    # Cluster the parameters based on the results using hierarchical clustering
    results_dist = pdist(results.reshape(-1, 1))  # Pairwise distance between result values
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
    plt.xlabel('17-Dimensional Parameters')
    plt.ylabel('Clusters')
    plt.title('Heatmap with Clusters')
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

def isolate_single_param_scatter(data: np.array, results: np.array, col_to_isolate: int, output_file: str):
	example_others = data[0, :]
	indices = find_indices_with_same_other_params(data, col_to_isolate, example_others)
	x = data[indices, col_to_isolate]
	y = results[indices]
	plt.scatter(x, y, marker='o', s=50, label="Data Points")
	# Fit a quadratic regression model to the data
	coeffs = np.polyfit(x, y, deg=2)
	# Generate points for the quadratic trend line
	quadratic_function = lambda x, a, b, c: a * x**2 + b * x + c
	trend_line_x = np.linspace(min(x), max(x), 1000)
	trend_line_y = quadratic_function(trend_line_x, *coeffs)
	# Plot the quadratic trend line
	plt.plot(trend_line_x, trend_line_y, color='red', label="Quadratic Trend Line")
	# label and return
	plt.xlabel("param vals")
	plt.ylabel("isolated changes")
	plt.title("Scatter Plot of 2D Array")
	plt.legend()
	plt.grid(True)
	plt.savefig(output_file)
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
	clean_condition = results_dirty > 0
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
	param_stats_isolate = Path("./stats/param_stats/isolate")
	param_stats_isolate.mkdir(parents=True)
	for i, colname in enumerate(colnames_vals):
		isolate_single_param_scatter(params,results,i,str(param_stats_isolate)+"/"+colname+".png")
	# run stats on distribution of training parameters using pair scatter plots
	params_stats_scatter = Path("./stats/param_stats/scatter")
	params_stats_scatter.mkdir(parents=True)
	save_pairwise_scatter_plot(params,str(params_stats_scatter)+"/pairscatter_params.png")
	# run PCA on training parameters
	run_pca_and_save_plot(params,str(params_stats_scatter)+"/PCA_params.png")
	# run statistics on results
	result_stats_dir = Path("./stats/result_stats")
	result_stats_dir.mkdir(parents=True)
	save_distwith_best_fit(results,str(result_stats_dir)+"/result_UGB_dist.png","UGB Distribution","UGB")
	# run stats on results and data combined
	comb_stats_dir = Path("./stats/combined")
	comb_stats_dir.mkdir(parents=True)
	create_pca_biplot_with_clusters(params,results,str(comb_stats_dir)+"/heatmapresults_params.png")
	create_heatmap_with_clusters(params,results,str(comb_stats_dir)+"/heatmap_results_clustered.png")
