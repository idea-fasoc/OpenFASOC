import sys, os
try:
    __import__('glayout')
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))) 
from glayout.flow.components.opamp import opamp 
from glayout.flow.components.diff_pair  import diff_pair
from glayout.flow.primitives.fet import nmos, pmos
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk 
from glayout.flow.components.current_mirror import current_mirror
import json
import numpy as np
import shutil
import tempfile as Temp
from pathlib import Path as Path
from typing import Union
import argparse
import warnings

def validate_drc_result(drc_result: dict, component_name: str):
    """used to validate the DRC results, checks if the DRC results are present, if the DRC was successful and if there are any errors in the DRC report

    Args:
        drc_result (dict): a dictionary containing the DRC results, returned from drc_magic
        component_name (str): the name of the component

    Raises:
        ValueError: if no DRC results are found for the component
        ValueError: if there was an error running DRC for the component
        ValueError: if there are errors in the DRC report for the component

    Returns:
        int: a return code of 0 if DRC has passed for the component
    """
    if drc_result is None: 
        raise ValueError(f'No DRC results found for {component_name}!')
    
    if drc_result['subproc_code'] != 0:
        raise ValueError(f'Error running DRC for {component_name}!')
    
    report_str = 'No errors found in DRC report'
    
    if report_str not in drc_result['result_str'] \
        or 'failed' in drc_result['result_str']:
        raise ValueError(f'Errors found in DRC report for {component_name}!')

    return 0


def validate_lvs_results(lvs_report: Union[Path, str], lvs_result: dict, component_name: str):
    """used to validate the LVS results, checks if the LVS results are present, if the LVS was successful and if there are any errors in the LVS report

    Args:
        lvs_report (Union[Path, str]): path to the LVS report file
        lvs_result (dict): a dictionary containing the LVS results, returned from lvs_netgen
        component_name (str): the name of the component

    Raises:
        ValueError: if no LVS results are found for the component
        ValueError: if there was an error running LVS for the component
        ValueError: if there are errors in the LVS report for the component
        ValueError: if the cell pin lists could not be altered to match
        ValueError: if the device classes are not equivalent
        ValueError: if the cell pin lists are not equivalent

    Returns:
        int: a return code of 0 if LVS has passed for the component
    """
    str1 = f'Cell pin lists for {component_name} and {component_name} altered to match.'
    str2 = f'Device classes {component_name} and {component_name} are equivalent.'
    str3 = f'Cell pin lists are equivalent.'
    str4 = f'Netlists do not match.'
    error_str1 = f'Error: Cell pin lists could not be altered to match.'
    error_str2 = f'Error: Device classes are not equivalent.'
    error_str3 = f'Error: Cell pin lists are not equivalent.'
    error_str4 = f'Error: Netlists do not match.'
    
    if lvs_result is None: 
        raise ValueError(f'No LVS results found for {component_name}!')
    if lvs_result['magic_subproc_code'] != 0:
        raise ValueError(f'Error running LVS for {component_name}, magic subprocess failed!')
    if lvs_result['netgen_subproc_code'] != 0:
        raise ValueError(f'Error running LVS for {component_name}, netgen subprocess failed!')
    # all str1, str2, str3 need to be in lvs_result
    
    with open(lvs_report, 'r') as f:
        report = f.read()
        
        if str1 not in report:
            raise ValueError(error_str1)
        if str2 not in report:
            raise ValueError(error_str2)
        if str3 not in report: 
            raise ValueError(error_str3)
        if str4 in report:
            raise ValueError(error_str4)
    
    return 0


def simulate_component(comp, pdk, componentref = None):
    with Temp.TemporaryDirectory() as tmpdirname:
        tmpdirpath = Path(tmpdirname).resolve()

        # the paths for the temporary files
        gds_file = tmpdirpath / f'{comp.name}.gds'
        cdl_file = tmpdirpath / f'{comp.name}.cdl'
        cdl_file = str(Path(__file__).resolve().parent / f'{comp.name}_test.cdl')
        report_path = tmpdirpath / f'{comp.name}.rpt'
        klayout_report_path = tmpdirpath / 'klayout_report.lyrdb'
        
        # create empty klayout report file
        klayout_report_path.touch()
        
        # write gds and copy to temp directory
        comp.write_gds(str(gds_file))
        shutil.copy(str(gds_file), str(Path(__file__).resolve().parent / f'{comp.name}_test.gds'))
        
        # write netlist and copy to temp directory
        net = comp.info['netlist'].generate_netlist(with_pins=True)
        with open(cdl_file, 'w') as f:
            f.write(net)
        # shutil.copy(str(cdl_file), str(Path(__file__).resolve().parent / f'{comp.name}_test.cdl'))

        result = pdk.drc_magic(gds_file, comp.name)

        drc_result = validate_drc_result(result, comp.name)
        if drc_result: 
            raise ValueError(f'DRC failed for {comp.name}!')
        else: 
            print(f'DRC passed for {comp.name}!')
        
        
        result = pdk.lvs_netgen(gds_file, comp.name, netlist=cdl_file, report_handling=report_path, copy_intermediate_files = True)

        lvs_result = validate_lvs_results(report_path, result, comp.name)

        if lvs_result:
            raise ValueError(f'LVS failed for {comp.name}!')
        else:
            print(f'LVS passed for {comp.name}!')
        
        # not supporting klayout drc for now
        # result = pdk.drc(comp, klayout_report_path)
        # if not result:
        #     warnings.warn(f'Errors found in Klayout DRC report for {comp.name}!')

def check_opamp_results(results, path_to_variances, path_to_means):
    
# read variances.json
    with open(path_to_variances, "r") as f:
        variances = json.load(f)
    # read means.json
    with open(path_to_means, "r") as f:
        means = json.load(f)
        
    warn_ugb = means["unity gain bandwidth"] - np.sqrt(variances["unity gain bandwidth"])
    warn_dc_gain = means["dc gain"] - np.sqrt(variances["dc gain"])
    warn_phase_margin = means["phase margin"] - np.sqrt(variances["phase margin"])
    warn_area = means["area"] + 1e4
    warn_power = means["power"] + np.sqrt(variances["power"])
    warn_two_stage_power = means["two stage power"] + np.sqrt(variances["two stage power"])
    warn_noise = means["noise"] + np.sqrt(variances["noise"])
    warn_3db_bandwidth = means["3db bandwidth"] - np.sqrt(variances["3db bandwidth"])


    for key, val in results.items():
        if key == "unity gain bandwidth":
            if val <= warn_ugb:
                warnings.warn(f"Unity Gain Bandwidth: {val} is less than the minimum value of {warn_ugb}")
            if val <= warn_ugb - 2 * np.sqrt(variances["unity gain bandwidth"]):
                raise ValueError(f"Unity Gain Bandwidth: {val} is less than the minimum value of {warn_ugb - 2 * np.sqrt(variances['unity gain bandwidth'])}")
        
        elif key == "dc gain":
            if val <= warn_dc_gain:
                warnings.warn(f"DC Gain: {val} is less than the minimum value of {warn_dc_gain}")
            if val <= warn_dc_gain - 2 * np.sqrt(variances["dc gain"]):
                raise ValueError(f"DC Gain: {val} is less than the minimum value of {warn_dc_gain - 2 * np.sqrt(variances['dc gain'])}")
        
        elif key == "phase margin":
            if val <= warn_phase_margin:
                warnings.warn(f"Phase Margin: {val} is less than the minimum value of {warn_phase_margin}")
            if val <= warn_phase_margin - 2 * np.sqrt(variances["phase margin"]):
                raise ValueError(f"Phase Margin: {val} is less than the minimum value of {warn_phase_margin - 2 * np.sqrt(variances['phase margin'])}")
        
        elif key == "area":
            if val >= warn_area:
                warnings.warn(f"Area: {val} is greater than the maximum value of {warn_area}")
            if val >= warn_area + 2 * np.sqrt(variances["area"]):
                raise ValueError(f"Area: {val} is greater than the maximum value of {warn_area + 2 * np.sqrt(variances['area'])}")
        
        elif key == "power":
            if val >= warn_power:
                warnings.warn(f"Power: {val} is greater than the maximum value of {warn_power}")
            if val >= warn_power + 2 * np.sqrt(variances["power"]):
                raise ValueError(f"Power: {val} is greater than the maximum value of {warn_power + 2 * np.sqrt(variances['power'])}")
        
        elif key == "two stage power":
            if val >= warn_two_stage_power:
                warnings.warn(f"Two Stage Power: {val} is greater than the maximum value of {warn_two_stage_power}")
            if val >= warn_two_stage_power + 2 * np.sqrt(variances["two stage power"]):
                raise ValueError(f"Two Stage Power: {val} is greater than the maximum value of {warn_two_stage_power + 2 * np.sqrt(variances['two stage power'])}")
        
        elif key == "noise":
            if val >= warn_noise:
                warnings.warn(f"Noise: {val} is greater than the maximum value of {warn_noise}")
            if val >= warn_noise + 2 * np.sqrt(variances["noise"]):
                raise ValueError(f"Noise: {val} is greater than the maximum value of {warn_noise + 2 * np.sqrt(variances['noise'])}")
        
        elif key == "3db bandwidth":
            if val <= warn_3db_bandwidth:
                warnings.warn(f"3dB Bandwidth: {val} is less than the minimum value of {warn_3db_bandwidth}")
            if val <= warn_3db_bandwidth - 2 * np.sqrt(variances["3db bandwidth"]):
                raise ValueError(f"3dB Bandwidth: {val} is less than the minimum value of {warn_3db_bandwidth - 2 * np.sqrt(variances['3db bandwidth'])}")

def opamp_parametric_sim():
    json_paths = Path(__file__).resolve().parents[5] / ".github" / "scripts" / "expected_sim_outputs" / "opamp"
    path_to_variances = json_paths / "variances.json"
    path_to_means = json_paths / "means.json"
    
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
    
    results = single_build_and_simulation(
        opamp_parameters_serializer(
            **params
        ), 
        temp=25, 
        cload=0, 
        noparasitics=False, 
        hardfail=True
    )

    check_opamp_results(results, path_to_variances, path_to_means)
    
parser = argparse.ArgumentParser()
parser.add_argument('--component', type=str, help='Component name to simulate')
args = parser.parse_args()

# simulate the component
if args.component == 'opamp':
    comp = (opamp(sky130_mapped_pdk, add_output_stage=True))
    comp.name = 'opamp_test'
    simulate_component(comp, sky130_mapped_pdk)

elif args.component == 'opamp_parametric':
    from tapeout.tapeout_and_RL.sky130_nist_tapeout import *
    opamp_parametric_sim()
    
elif args.component == 'diff_pair':
    comp = (diff_pair(sky130_mapped_pdk))
    comp.name = 'diff_pair_test'
    simulate_component(comp, sky130_mapped_pdk)
    
elif args.component == 'nmos':
    comp = (nmos(sky130_mapped_pdk))
    comp.name = 'nmos_test'
    simulate_component(comp, sky130_mapped_pdk)
    
elif args.component == 'pmos':
    comp = pmos(sky130_mapped_pdk)
    comp.name = 'pmos_test'
    simulate_component(comp, sky130_mapped_pdk)

elif args.component == 'current_mirror':
    comp = current_mirror(sky130_mapped_pdk, numcols = 3, with_dummy=False)
    comp.name = 'currmirror_test'
    simulate_component(comp, sky130_mapped_pdk)