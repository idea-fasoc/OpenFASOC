import sys
from os import path, rename, environ
environ['OPENBLAS_NUM_THREADS'] = '1'
# path to glayout
sys.path.append(path.join(path.dirname(__file__), '../../'))

from gdsfactory.read.import_gds import import_gds
from gdsfactory.components import text_freetype, rectangle
from glayout.flow.pdk.util.comp_utils import prec_array, movey, align_comp_to_port, prec_ref_center
from glayout.flow.pdk.util.port_utils import add_ports_perimeter, print_ports
from gdsfactory.component import Component
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.blocks.composite.fvf_based_ota.ota import super_class_AB_OTA
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, prec_ref_center, prec_center, align_comp_to_port
from glayout.flow.pdk.util.port_utils import rename_ports_by_orientation
from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid
from gdsfactory.components import text_freetype, rectangle
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.primitives.via_gen import via_array, via_stack
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
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as pdk
from itertools import count, repeat
from glayout.flow.pdk.util.component_array_create import write_component_matrix
import re
import pickle
import tempfile
import subprocess
import traceback

global _TAPEOUT_AND_RL_DIR_PATH_
global _GET_PARAM_SET_LENGTH_
global PDK_ROOT
global __NO_LVT_GLOBAL_
global __SMALL_PAD_
__SMALL_PAD_ = True
__NO_LVT_GLOBAL_ = False
_GET_PARAM_SET_LENGTH_ = False

if 'PDK_ROOT' in environ:
    PDK_ROOT = str(Path(environ['PDK_ROOT']).resolve())
else:
    PDK_ROOT = "/usr/bin/miniconda3/share/pdk/"

_TAPEOUT_AND_RL_DIR_PATH_ = Path(__file__).resolve().parent
#print(_TAPEOUT_AND_RL_DIR_PATH_)

# ====Build Ota====

def sky130_ota_add_pads(ota_in: Component, flatten=False) -> Component:
    """adds the MPW-5 pads and nano pads to ota.
    Also adds text labels and pin layers so that extraction is nice
    this function does not need to be used with sky130_add_ota_labels
    """
    ota_wpads = ota_in.copy()
    ota_wpads = movey(ota_wpads, destination=0)
    # create pad array and add to ota
    global __SMALL_PAD_
    small_pad=__SMALL_PAD_
    if small_pad:
        pad = import_gds("../../../../../tapeout/tapeout_and_RL/pads/pad_60um_flat.gds")
        pad.name = "NISTpad"
    else:
        pad = import_gds("../../../../../tapeout/tapeout_and_RL/pads/Manhattan120umPad.gds")
        pad.name = "Manhattan120umPad"
    pad = add_ports_perimeter(pad, pdk.get_glayer("met5"),prefix="pad_")
    if small_pad:
        pad_array = prec_array(pad, rows=2, columns=(4), spacing=(80,240))
    else:
        pad_array = prec_array(pad, rows=2, columns=(4), spacing=(160,240))
    pad_array_ref = prec_ref_center(pad_array)
    ota_wpads.add(pad_array_ref)
    # add via_array to vdd pin
    
    # route to the pads
    leftroutelayer="met5"
    ota_wpads << L_route(pdk, ota_wpads.ports["PLUS_top_met_E"],pad_array_ref.ports["row1_col3_pad_S"], hwidth=3, vwidth=3)
    ota_wpads << L_route(pdk, ota_wpads.ports["MINUS_top_met_W"],pad_array_ref.ports["row1_col0_pad_S"], hwidth=3, vwidth=3)
    ota_wpads << L_route(pdk, pad_array_ref.ports["row1_col1_pad_E"],ota_wpads.ports["VCC_top_met_N"], vwidth=4, hwidth=4, vglayer='met3', hglayer='met4')
    ota_wpads << L_route(pdk, ota_wpads.ports["VSS_top_met_E"],pad_array_ref.ports["row0_col3_pad_N"], hwidth=4, vwidth=4)
    ota_wpads << L_route(pdk, ota_wpads.ports["IBIAS2_top_met_E"],pad_array_ref.ports["row0_col2_pad_N"], hwidth=3, vwidth=3)
    ota_wpads << L_route(pdk, ota_wpads.ports["IBIAS1_top_met_W"],pad_array_ref.ports["row0_col1_pad_N"],hwidth=3, vwidth=3)
    ota_wpads << L_route(pdk, ota_wpads.ports["DIFFOUT_top_met_W"],pad_array_ref.ports["row0_col0_pad_N"], hwidth=4, vwidth=4)
    # add pin layer and text labels for LVS
    text_pin_labels = list()
    met5pin = rectangle(size=(5,5),layer=(72,16), centered=True)
    for name in ["vout","nbc_10u","nb_10u","avss","inm","avdd","nc","inp"]:
        pin_w_label = met5pin.copy()
        pin_w_label.add_label(text=name,layer=(72,5),magnification=4)
        text_pin_labels.append(pin_w_label)
    for row in range(2):
        for col_u in range(4):
            col = col_u 
            port_name = "row"+str(row)+"_col"+str(col)+"_pad_S"
            pad_array_port = pad_array_ref.ports[port_name]
            pin_ref = ota_wpads << text_pin_labels[4*row + col_u]
            align_comp_to_port(pin_ref,pad_array_port,alignment=('c','t'))
    
    if flatten:
        return ota_wpads.flatten()
    else:
        return ota_wpads

def sky130_add_ota_labels(ota_in: Component) -> Component:
    
    ota_in.unlock()
    # define layers
    met1_pin = (68,16)
    met1_label = (68,5)
    met2_pin = (69,16)
    met2_label = (69,5)
    met3_pin = (70,16)
    met3_label = (70,5)
    # list that will contain all port/comp info
    move_info = list()
    # create labels and append to info list
    # gnd
    gndlabel = rectangle(layer=met2_pin,size=(0.5,0.5),centered=True).copy()
    gndlabel.add_label(text="AVSS",layer=met2_label)
    move_info.append((gndlabel,ota_in.ports["VSS_top_met_N"],None))
    
    #currentbias
    ibias1label = rectangle(layer=met3_pin,size=(0.5,0.5),centered=True).copy()
    ibias1label.add_label(text="NBC_10U",layer=met3_label)
    move_info.append((ibias1label,ota_in.ports["IBIAS1_top_met_N"],None))
    ibias2label = rectangle(layer=met3_pin,size=(0.5,0.5),centered=True).copy()
    ibias2label.add_label(text="NB_10U",layer=met3_label)
    move_info.append((ibias2label,ota_in.ports["IBIAS2_top_met_N"],None))
    
    #vcc
    vcclabel = rectangle(layer=met2_pin,size=(0.5,0.5),centered=True).copy()
    vcclabel.add_label(text="AVDD",layer=met2_label)
    move_info.append((vcclabel,ota_in.ports["VCC_top_met_N"],None))
    
    # output (3rd stage)
    outputlabel = rectangle(layer=met3_pin,size=(0.5,0.5),centered=True).copy()
    outputlabel.add_label(text="VOUT",layer=met3_label)
    move_info.append((outputlabel,ota_in.ports["DIFFOUT_top_met_N"],None))
    
    # input
    p_inputlabel = rectangle(layer=met3_pin,size=(0.5,0.5),centered=True).copy()
    p_inputlabel.add_label(text="INP",layer=met3_label)
    move_info.append((p_inputlabel,ota_in.ports["PLUS_top_met_N"], None))   
    m_inputlabel = rectangle(layer=met3_pin,size=(0.5,0.5),centered=True).copy()
    m_inputlabel.add_label(text="INM",layer=met3_label)
    move_info.append((m_inputlabel,ota_in.ports["MINUS_top_met_N"], None))
    
    # move everything to position
    for comp, prt, alignment in move_info:
        alignment = ('c','b') if alignment is None else alignment
        compref = align_comp_to_port(comp, prt, alignment=alignment)
        ota_in.add(compref)
    return ota_in.flatten() 



def sky130_add_ota_lvt_layer(ota_in: Component) -> Component:
    global __NO_LVT_GLOBAL_
    if __NO_LVT_GLOBAL_:
        return ota_in
    ota_in.unlock()
    
    lvt_layer=(125,44)
    
    dimensions = (evaluate_bbox(ota_in)[0], (ota_in.ports["VCC_top_met_N"].center[1] - ota_in.ports["res_1_N_tie_S_top_met_S"].center[1]))

    lvt_rectangle = rectangle(layer=lvt_layer, size=(dimensions[0], dimensions[1]))
    lvt_rectangle_ref = prec_ref_center(lvt_rectangle)
    lvt_rectangle_ref.movey(ota_in.ports["res_1_N_tie_S_top_met_S"].center[1] + dimensions[1]/2)
    ota_in.add(lvt_rectangle_ref)

    return ota_in


def ota_parameters_serializer(
        input_pair_params: tuple[float,float]=(4,2),
        fvf_shunt_params: tuple[float,float]=(2.75,1),
        local_current_bias_params: tuple[float,float]=(3.76,3.0),
        diff_pair_load_params: tuple[float,float]=(9,1),
        ratio: int=1,
        current_mirror_params: tuple[float,float]=(2.25,1),
        resistor_params: tuple[float,float,float,float]=(0.5,3,4,4),
        global_current_bias_params: tuple[float,float,float]=(8.3,1.42,2)

) -> np.array:
    """converts ota params into the uniform numpy float format"""
    return np.array(
        [input_pair_params[0],input_pair_params[1],
        fvf_shunt_params[0],fvf_shunt_params[1],
        local_current_bias_params[0],local_current_bias_params[1],
        diff_pair_load_params[0],diff_pair_load_params[1],
        ratio,
        current_mirror_params[0],current_mirror_params[1],
        resistor_params[0],resistor_params[1],resistor_params[2],resistor_params[3],
        global_current_bias_params[0],global_current_bias_params[1],global_current_bias_params[2]],
        dtype=np.float64
    )

def ota_parameters_de_serializer(serialized_params: Optional[np.array]=None) -> dict:
    """converts uniform numpy float format to ota kwargs"""
    if serialized_params is None:
        serialized_params = 18*[-987.654321]
        #serialized_params[16] = int(-987.654321)
        #serialized_params[17] = int(-987.654321)
    if not len(serialized_params) == 18:
        raise ValueError("serialized_params should be a length 18 array")
    params_dict = dict()
    params_dict["input_pair_params"] = tuple(serialized_params[0:2])
    params_dict["fvf_shunt_params"] = tuple(serialized_params[2:4])
    params_dict["local_current_bias_params"] = tuple(serialized_params[4:6])
    params_dict["diff_pair_load_params"] = tuple(serialized_params[6:8])
    params_dict["ratio"] = int(serialized_params[8])
    params_dict["current_mirror_params"] = tuple(serialized_params[9:11])
    params_dict["resistor_params"] = tuple(serialized_params[11:15])
    params_dict["global_current_bias_params"] = tuple(serialized_params[15:])
    return params_dict


def ota_results_serializer(
    ugb: float = -987.654321,
    dcGain: float = -987.654321,
    phaseMargin: float = -987.654321,
    Ibias1: float = -987.654321,
    Ibias2: float = -987.654321,
    area: float = -987.654321,
    power: float = -987.654321,
    noise: float = -987.654321,
    bw_3db: float = -987.654321,
    rise_slew: float = -987.654321,
    fall_slew: float = -987.654321,
) -> np.array:
    return np.array([ugb, dcGain, phaseMargin, Ibias1, Ibias2, area, power, noise, bw_3db, rise_slew, fall_slew], dtype=np.float64)


def ota_results_de_serializer(
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
    results_dict["Ibias1"] = float(results[3])
    results_dict["Ibias2"] = float(results[4])
    results_dict["area"] = float(results[5])
    results_dict["power"] = float(results[6])
    results_dict["noise"] = float(results[7])
    results_dict["bw_3db"] = float(results[8])
    results_dict["rise_slew"] = float(results[9])
    results_dict["fall_slew"] = float(results[10])

    return results_dict


def get_small_parameter_list(test_mode = False) -> np.array:
    """creates small parameter list intended for brute force"""
    # all diffpairs to try
    inputpair = list()
    if test_mode:
        diffpairs.append((4,2))
    else:
        for width in [3,4,5]:
            for length in [1.7,2,2.3]:
                inputpair.append((width,length))
    # all bias2 (output amp bias) transistors
    fvfshunt = list()
    if test_mode:
        fvfshunt.append((2.75,1))
    else:
        for width in [2.5,2.75,3]:
            for length in [0.8,1,1.2]:
                fvfshunt.append((width,length))
    # all pmos first stage load transistors
    local_cm = list()
    if test_mode:
        local_cm.append((3.76,3))
    else:
        for width in [3.5,3.75,4]:
            for length in [2.5,3,3.5]:
                local_cm.append((width,length))
    # all output pmos transistors
    diffp_load = list()
    if test_mode:
        diffp_load.append((9,1))
    else:
        for width in [7,8,9,10]:
            for length in [1]:
                diffp_load.append((width,length))
    
    ratio = list()
    if test_mode:
        ratio.append((1))
    else:
        for amp in [1,2]:
            ratio.append((amp))
    
    op_cm = list()
    if test_mode:
        local_cm.append((2.25,1))
    else:
        for width in [2,2.25,2.5]:
            for length in [1]:
                op_cm.append((width,length))

    res = list()
    if test_mode:
        res.append((0.5,3,4,4))
    else:
        for width1 in [0.5,0.6,0.7]:
            for width2 in [2.8,3,3.2]:
                for length1 in [4]:
                    for length2 in [4]:
                        res.append((width1,width2,length1,length2))

    cbias = list()
    if test_mode:
        cbias.append((8.3,1.42,2))
    else:
        for width1 in [8.3]:
            for width2 in [1.4,1.8,2.2,2.6,3]:
                for length in [2]:
                        cbias.append((width1,width2,length))


    short_list_len = len(inputpair) * len(fvfshunt) * len(local_cm) * len(diffp_load) * len(ratio) * len(op_cm) * len(res) *len(cbias)
    short_list = np.empty(shape=(short_list_len,len(ota_parameters_serializer())),dtype=np.float64)
    index = 0
    
    for inputpair_v in inputpair:
        for fvfshunt_v in fvfshunt:
            for local_cm_v in local_cm:
                for diffp_load_v in diffp_load:
                    for ratio_v in ratio:
                        for op_cm_v in op_cm:
                            for res_v in res:
                                for cbias_v in cbias:
                                    tup_to_add = ota_parameters_serializer(
                                        input_pair_params=inputpair_v,
                                        fvf_shunt_params=fvfshunt_v,
                                        local_current_bias_params=local_cm_v, 
                                        diff_pair_load_params=diffp_load_v,
                                        ratio=ratio_v, 
                                        current_mirror_params=op_cm_v,
                                        resistor_params=res_v,
                                        global_current_bias_params=cbias_v, 
                                            )
                                    short_list[index] = tup_to_add
    
    global _GET_PARAM_SET_LENGTH_
    if _GET_PARAM_SET_LENGTH_:
        print("created parameter set of length: "+str(len(short_list)))
        import sys
        sys.exit()
    return short_list


def get_sim_results(acpath: Union[str,Path], dcpath: Union[str,Path], noisepath: Union[str,Path], slewpath: Union[str,Path]):
    acabspath = Path(acpath).resolve()
    dcabspath = Path(dcpath).resolve()
    noiseabspath = Path(noisepath).resolve()
    slewabspath = Path(slewpath).resolve()
    ACColumns = None
    DCColumns = None
    NoiseColumns = None
    SlewColumns = None
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
    try:
        with open(slewabspath, "r") as SlewReport:
            RawSlew = SlewReport.readlines()[0]
            SlewColumns = [item for item in RawSlew.split() if item]
    except Exception:
        pass

    na = -987.654321
    noACresults = (ACColumns is None) or len(ACColumns)<10
    noDCresults = (DCColumns is None) or len(DCColumns)<2
    nonoiseresults = (NoiseColumns is None) or len(NoiseColumns)<2
    noslewresults = (SlewColumns is None) or len(SlewColumns)<3
    return_dict = {
        "ugb": na if noACresults else ACColumns[1],
        "Ibias1": na if noACresults else ACColumns[3],
        "Ibias2": na if noACresults else ACColumns[5],
        "phaseMargin": na if noACresults else ACColumns[7],
        "dcGain": na if noACresults else ACColumns[9],
        "bw_3db": na if noACresults else ACColumns[11],
        "power": na if noDCresults else DCColumns[1],
        "noise": na if nonoiseresults else NoiseColumns[1],
        "rise_slew": na if noslewresults else SlewColumns[1],
        "fall_slew": na if noslewresults else SlewColumns[3],
    }
    for key, val in return_dict.items():
        val_flt = na
        try:
            val_flt = float(val)
        except ValueError:
            val_flt = na
        return_dict[key] = val_flt
    return return_dict


def process_netlist_subckt(netlist: Union[str,Path], sim_model: Literal["normal model", "cryo model"], cload: float=80.0, noparasitics: bool=False):
    netlist = Path(netlist).resolve()
    if not netlist.is_file():
        raise ValueError("netlist is not a valid file")
    hints = [".subckt","vout","inp","inm","avdd","avss","nb_10u","nbc_10u"]
    subckt_lines = list()
    with open(netlist, "r") as spice_net:
        subckt_lines = spice_net.readlines()
        for i,line in enumerate(subckt_lines):
            #print(f"Processing line {i}: {line.strip()}")
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
                print(f"Line matches hints: {line.strip()}")
                headerstr = ".subckt ota AVSS INM INP VOUT AVDD NBC_10U NB_10U"
                subckt_lines[i] = headerstr+"\nCload VOUT AVSS " + str(cload) +"p\n"
                print(f"Updated line: {subckt_lines[i]}")
            if ("floating" in line) or (noparasitics and len(line) and (line[0]=="c" or line[0]=="r")):
                subckt_lines[i] = "* "+ subckt_lines[i]
            if noparasitics:
                subckt_lines[i] = re.sub(r"ad=(\S*)","",subckt_lines[i])
                subckt_lines[i] = re.sub(r"as=(\S*)","",subckt_lines[i])
                subckt_lines[i] = re.sub(r"ps=(\S*)","",subckt_lines[i])
                subckt_lines[i] = re.sub(r"pd=(\S*)","",subckt_lines[i])
    with open(netlist, "w") as spice_net:
        print(f"Writing updated netlist to: {netlist}")
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

def __run_single_brtfrc(index, parameters_ele, save_gds_dir, temperature_info: tuple[int,str]=(25,"normal model"), cload: float=80.0, noparasitics: bool=False, output_dir: Optional[Union[int,str,Path]] = None, hardfail=False):
    # pass pdk as global var to avoid pickling issues
    global pdk
    global PDK_ROOT
    global _TAPEOUT_AND_RL_DIR_PATH_
    # generate layout
    destination_gds_copy = save_gds_dir / (str(index)+".gds")
    sky130pdk = pdk
    params = ota_parameters_de_serializer(parameters_ele)
    try:
        ota_v = sky130_add_ota_labels(sky130_add_ota_lvt_layer(super_class_AB_OTA(sky130pdk, **params)))
        ota_v.name = "ota"+str(index)
        area = float(ota_v.area())
        # use temp dir
        with TemporaryDirectory() as tmpdirname:
            results=None
            tmp_gds_path = Path(ota_v.write_gds(gdsdir=tmpdirname)).resolve()
            if tmp_gds_path.is_file():
                destination_gds_copy.write_bytes(tmp_gds_path.read_bytes())
            extractbash_template=str()
            #import pdb; pdb.set_trace()
            with open(str(_TAPEOUT_AND_RL_DIR_PATH_)+"/extract.bash.template","r") as extraction_script:
                extractbash_template = extraction_script.read()
                extractbash_template = extractbash_template.replace("@@PDK_ROOT",PDK_ROOT).replace("@@@PAROPT","noparasitics" if noparasitics else "na")
            with open(str(tmpdirname)+"/extract.bash","w") as extraction_script:
                extraction_script.write(extractbash_template)
            #copyfile("extract.bash",str(tmpdirname)+"/extract.bash")
            copyfile(str(_TAPEOUT_AND_RL_DIR_PATH_)+"/ota_perf_eval.sp",str(tmpdirname)+"/ota_perf_eval.sp")
            copytree(str(_TAPEOUT_AND_RL_DIR_PATH_)+"/sky130A",str(tmpdirname)+"/sky130A")
            # extract layouti
            Popen(["bash","extract.bash", tmp_gds_path, ota_v.name],cwd=tmpdirname).wait()
            print("Running simulation at temperature: " + str(temperature_info[0]) + "C")
            process_spice_testbench(str(tmpdirname)+"/ota_perf_eval.sp",temperature_info=temperature_info)
            process_netlist_subckt(str(tmpdirname)+"/ota"+str(index)+"_pex.spice", temperature_info[1], cload=cload, noparasitics=noparasitics)
            rename(str(tmpdirname)+"/ota"+str(index)+"_pex.spice", str(tmpdirname)+"/ota_pex.spice")
            # run sim and store result
            #import pdb;pdb.set_trace()
            Popen(["ngspice","-b","ota_perf_eval.sp"],cwd=tmpdirname).wait()
            ac_file = str(tmpdirname)+"/result_ac.txt"
            power_file = str(tmpdirname)+"/result_power.txt"
            noise_file = str(tmpdirname)+"/result_noise.txt"
            slew_file = str(tmpdirname)+"/result_slew.txt"
            result_dict = get_sim_results(ac_file, power_file, noise_file, slew_file)
            result_dict["area"] = area
            results = ota_results_serializer(**result_dict)
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
        if hardfail:
            raise e_LorA
        results = ota_results_serializer()
        with open('get_training_data_ERRORS.log', 'a') as errlog:
            errlog.write("\nota run "+str(index)+" with the following params failed: \n"+str(params))
    return results


def brute_force_full_layout_and_PEXsim(sky130pdk: MappedPDK, parameter_list: np.array, temperature_info: tuple[int,str]=(25,"normal model"), cload: float=80.0, noparasitics: bool=False, saverawsims: bool=False) -> np.array:
    """runs the brute force testing of parameters by
    1-constructing the ota layout specfied by parameters
    2-extracting the netlist for the ota
    3-running simulations on the ota
    returns the results from ota simulations as nparray
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
    with Pool(128) as cores:
        if saverawsims:
            results = np.array(cores.starmap(safe_single_build_and_simulation, zip(parameter_list, repeat(temperature_info[0]), count(0), repeat(cload), repeat(noparasitics),repeat(False), count(0), repeat(save_gds_dir), repeat(False))),np.float64)
        else:
            results = np.array(cores.starmap(safe_single_build_and_simulation, zip(parameter_list, repeat(temperature_info[0]), repeat(None), repeat(cload), repeat(noparasitics),repeat(False), count(0), repeat(save_gds_dir), repeat(False))),np.float64)
    # undo pdk modification
    sky130pdk.default_decorator = add_npc_decorator
    return results


# data gathering main function
def get_training_data(test_mode: bool=True, temperature_info: tuple[int,str]=(25,"normal model"), cload: float=80.0, noparasitics: bool=False, parameter_array: Optional[np.array]=None, saverawsims=False) -> None:
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
def single_build_and_simulation(parameters: np.array, temp: int=25, output_dir: Optional[Union[str,Path]] = None, cload: float=80.0, noparasitics: bool=False,hardfail=False, index: int = 12345678987654321, save_gds_dir="./", return_dict: bool=True) -> dict:
    """Builds, extract, and simulates a single ota
    saves ota gds in current directory with name 12345678987654321.gds
    returns -987.654321 for all values IF phase margin < 60
    """
    from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
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
    save_gds_dir = Path(save_gds_dir).resolve()
    # pass pdk as global var to avoid pickling issues
    global pdk
    pdk = sky130_mapped_pdk
    results = __run_single_brtfrc(index, parameters, temperature_info=temperature_info, save_gds_dir=save_gds_dir, output_dir=output_dir, cload=cload, noparasitics=noparasitics, hardfail=hardfail)
    if return_dict: # default behavoir will return a dictionary and filter phase margin below 45
        results = ota_results_de_serializer(results)
        if results["phaseMargin"] < 60:
            for key in results:
                results[key] = -987.654321
    return results



# ================ safe single build and sim ==================


class safe_single_build_and_simulation_helperclass:
    def __init__(self, *args, **kwargs):
        self.passed_args = args
        self.passed_kwargs = kwargs
        # create and run using a temp dir to pass information
        with tempfile.TemporaryDirectory() as temp_dir:
            # Define the path for the pickle file
            pickle_file_path = Path(temp_dir).resolve() / 'class_instance.pkl'
            # Serialize the instance to the pickle file
            with open(pickle_file_path, 'wb') as f:
                pickle.dump(self, f)
            # Define and run the subprocess
            python_executable = sys.executable
            command = [python_executable, "sky130_ota_tapeout.py", "safe_single_build_and_sim", "--class_pickle_file", pickle_file_path,"--PDK_ROOT",PDK_ROOT]
            #process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            subprocess.Popen(command,cwd=str(_TAPEOUT_AND_RL_DIR_PATH_)).wait()
            # load the result back from the same pickle file which was passed
            with open(pickle_file_path, 'rb') as pckfile:
                restored_run = pickle.load(pckfile)
            # if restored_run does not have a results attribute, that means execute did not run properly in the other session 
            # single build and sim probably failed
            try:
                self.results = restored_run.results
            except AttributeError:
                raise RuntimeError("\nAn error silently occurred somewhere before this point\n")
                
            
    def execute(self):
        self.results = single_build_and_simulation(*self.passed_args,**self.passed_kwargs)

# same as calling single_build_and_simulation, but runs in a subprocess
def safe_single_build_and_simulation(*args, **kwargs) -> dict:
    def get_parameter_value(param_name: str, *args, **kwargs):
        # Check if the parameter is in kwargs
        if param_name in kwargs:
            return kwargs[param_name]
        # Check if the parameter is in args
        try:
            # Find the index of the param_name in args and return the next item as its value
            index = args.index(param_name)
            return args[index + 1]
        except (ValueError, IndexError):
            # ValueError if param_name is not in args
            # IndexError if param_name is the last item and has no value after it
            return None
    try:
        return safe_single_build_and_simulation_helperclass(*args,**kwargs).results
    except Exception as e_LorA:
        if bool(get_parameter_value("hardfail",*args,**kwargs)):
            raise e_LorA
        results = ota_results_serializer()
        with open('get_training_data_ERRORS.log', 'a') as errlog:
            errlog.write("\nota run "+str(get_parameter_value("index",*args,**kwargs))+" with the following params failed: \n"+str(get_parameter_value("params",*args,**kwargs)))
    return results



if __name__ == "__main__":
    import time
    start_watch = time.time()

    parser = argparse.ArgumentParser(description="sky130 ota tapeout sample, RL generation, and statistics utility.")

    subparsers = parser.add_subparsers(title="mode", required=True, dest="mode")

    
    # Subparser for gen_ota mode
    gen_ota_parser = subparsers.add_parser("gen_ota", help="Run the gen_ota function. optional parameters for transistors are width,length,current multiplication ratio")
    gen_ota_parser.add_argument("--input_pair_params", nargs=2, type=float, default=[4, 2], help="half_diffpair_params (default: 4 2)")
    gen_ota_parser.add_argument("--fvf_shunt_params", nargs=2, type=float, default=[2.75, 1], help="fvf_shunt_params (default: 2.75 1)")
    gen_ota_parser.add_argument("--local_current_bias_params", nargs=2, type=float, default=[3.76, 3], help="local_current_bias_params (default: 3.76 3)")
    gen_ota_parser.add_argument("--diff_pair_load_params", nargs=2, type=float, default=[9, 1], help="diff_pair_load_params (default: 3.76 3)")
    gen_ota_parser.add_argument("--ratio", type=int, default=1, help="ratio (default: 1)")
    gen_ota_parser.add_argument("--current_mirror_params", nargs=2, type=float, default=[2.25,1], help="current_mirror_params (default: 2.25 1)")
    gen_ota_parser.add_argument("--resistor_params", nargs=4, type=float, default=[0.5,3,4,4], help="resistor_params (default: 0.5 3 4 4)")
    gen_ota_parser.add_argument("--global_current_bias_params", nargs=3, type=float, default=[8.3,1.42,2], help="global_currrent_bias_params (default: 8.3 1.42 2)")
    gen_ota_parser.add_argument("--output_gds", help="Filename for outputing ota (gen_ota mode only)")
    gen_ota_parser.add_argument("--add_pads",action="store_true" , help="add pads (gen_ota mode only)")

    # subparser for gen_otas mode
    gen_otas_parser = subparsers.add_parser("gen_otas", help="generates the otas returned in the small parameters list but only saves GDS. Always outputs to ./outputrawotas")
    gen_otas_parser.add_argument("--pdk", help="specify sky130 or gf180 pdk")

    # subparse for testing mode (create ota and run sims)
    test = subparsers.add_parser("test", help="Test mode")
    test.add_argument("--output_dir", type=Path, default="./", help="Directory for output GDS file")
    test.add_argument("--temp", type=int, default=int(25), help="Simulation temperature")
    test.add_argument("--cload", type=float, default=float(80), help="run simulation with load capacitance units=pico Farads")
    test.add_argument("--noparasitics",action="store_true",help="specify that parasitics should be removed when simulating")
    
        
    # Hidden subparser used for safe_single_build_and_simulation
    safe_single_build_and_sim = subparsers.add_parser("safe_single_build_and_sim")
    safe_single_build_and_sim.add_argument("--class_pickle_file",type=Path,help="see safe_single_build_and_simulation")

    for prsr in [gen_ota_parser,test,safe_single_build_and_sim]:
        prsr.add_argument("--no_lvt",action="store_true",help="do not place any low threshold voltage transistors.")
        prsr.add_argument("--PDK_ROOT",type=Path,default="/usr/bin/miniconda3/share/pdk/",help="path to the sky130 PDK library")

    args = parser.parse_args()

    if args.mode in ["gen_otas"]:
        __SMALL_PAD_ = not args.big_pad

    if args.mode in ["test","gen_otas","safe_single_build_and_sim"]:
        __NO_LVT_GLOBAL_ = args.no_lvt
        PDK_ROOT = Path(args.PDK_ROOT).resolve()
        if 'PDK_ROOT' in environ:
            PDK_ROOT = Path(environ['PDK_ROOT']).resolve()
        if not(PDK_ROOT.is_dir()):
            raise ValueError("PDK_ROOT "+str(PDK_ROOT)+" is not a valid directory\n")
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

    if args.mode=="gen_ota":
        # Call the ota function with the parsed arguments
        ota_comp = super_class_AB_OTA(pdk=pdk,
                input_pair_params=tuple(args.input_pair_params),
                fvf_shunt_params=tuple(args.fvf_shunt_params),
                local_current_bias_params=tuple(args.local_current_bias_params),
                diff_pair_load_params=tuple(args.diff_pair_load_params),
                ratio = args.ratio,
                current_mirror_params = tuple(args.current_mirror_params),
                resistor_params = tuple(args.resistor_params),
                global_current_bias_params = tuple(args.global_current_bias_params),
            )
        ota_comp = sky130_add_ota_lvt_layer(ota_comp)
        if args.add_pads:
            ota_comp_labels = sky130_add_ota_labels(ota_comp)
            ota_comp_final = sky130_ota_add_pads(ota_comp_labels)
        else:
            ota_comp_final = ota_comp

        ota_comp_final.show()
        if args.output_gds:
            ota_comp_final.write_gds(args.output_gds)

    elif args.mode == "test":
        params = {
            "input_pair_params": (4, 2),
            "fvf_shunt_params": (2.75, 1),
            "local_current_bias_params": (3.76, 3),
            "diff_pair_load_params": (9, 1),
            "ratio": 1,
            "current_mirror_params": (2.25, 1),
            "resistor_params": (0.5, 3, 4, 4),
            "global_current_bias_params": (8.3, 1.42, 2)
        }
        results = safe_single_build_and_simulation(ota_parameters_serializer(**params), temperature_info[0], args.output_dir, cload=args.cload, noparasitics=args.noparasitics, hardfail=True)
        print(results)
    
    elif args.mode=="safe_single_build_and_sim":
        with open(args.class_pickle_file, 'rb') as pckfile:
            restored_run = pickle.load(pckfile)
        restored_run.execute()
        with open(args.class_pickle_file, 'wb') as pckfile:
            pickle.dump(restored_run, pckfile)

    elif args.mode == "gen_otas":
        global usepdk
        if args.pdk[0].lower()=="g":
            from glayout.flow.pdk.gf180_mapped import gf180_mapped_pdk
            usepdk = gf180_mapped_pdk
        else:
            usepdk = pdk
        output_path = Path("./outputrawotas").resolve()
        output_path.mkdir()
        def create_func(argnparray, indx: int):
            global usepdk
            comp = ota(usepdk,**ota_parameters_de_serializer(argnparray))
            comp.write_gds("./outputrawotas/amp"+str(indx)+".gds")

        argnparray = get_small_parameter_list()
        with Pool(120) as cores:
            cores.starmap(create_func, zip(argnparray,count(0)))

    end_watch = time.time()
    print("\ntotal runtime was "+str((end_watch-start_watch)/3600) + " hours\n")

