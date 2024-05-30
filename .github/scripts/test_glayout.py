from glayout.flow.components.opamp import opamp 
from glayout.flow.components.diff_pair  import diff_pair
from glayout.flow.primitives.fet import nmos, pmos
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk 
from glayout.flow.components.current_mirror import current_mirror
import shutil
import tempfile as Temp
from pathlib import Path as Path
from typing import Union
import argparse
import warnings
import sys, os 

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



parser = argparse.ArgumentParser()
parser.add_argument('--component', type=str, help='Component name to simulate')
args = parser.parse_args()

# simulate the component
if args.component == 'opamp':
    comp = (opamp(sky130_mapped_pdk, add_output_stage=True))
    comp.name = 'opamp_test'
    simulate_component(comp, sky130_mapped_pdk)
    
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