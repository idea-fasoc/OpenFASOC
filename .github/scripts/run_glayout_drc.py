import os, sys, re, gdstk, shutil, warnings
from pathlib import Path
import subprocess as sp
from gdsfactory.component import Component

def place_component(comp_name: str, func: "callable[[Component], any]", pdk, *args):
    """This function places the component on the layout and runs DRC on it
    in the most modular manner possible to accomodate for possible changes
    later

    Args:
        comp_name (str): the name of the component
        func (callable[[Component], any]): the function to be called to generate the component
        pdk (str): the PDK to be used (sky130, etc.)

    Returns:
        int: returns nothing if an error occurs, else returns the component
    """
    try:
        inst = Component()
        inst = func(pdk, *args)
        inst.name = comp_name
        return inst
    except Exception as e:
        print(f"Error in placing {comp_name} : {e}\n exiting....")
        sys.exit(1)

def eval_component(comp_to_run: Component, pdk, clean: int):
    """runs DRC on the generated component passed to it and 
    describes the errors if any. Also cleans the generated gds file

    Args:
        comp_to_run (Component): the generated component to run DRC on
        clean (int): a flag to clean the generated gds file
    """
    gds_path = f'./{comp_to_run.name}.gds'
    comp_to_run.write_gds(gds_path)
    error_list = run_glayout_drc(comp_to_run.name, gds_path)
    check_errors(error_list, comp_to_run.name, pdk)
    
    # clean
    if clean:
        os.remove(gds_path)
    return error_list


def run_glayout_drc(design_name: str, gds_file: str) -> list:
    """sets up the magicDRC script found in the drc-lvs-check directory and 
    runs it on the passed gds file. It then checks the output file for errors

    Args:
        design_name (str): the name of the component for which DRC is to be run
        gds_file (str): the path to the gds file to be checked

    Returns:
        list: a list containing the return code of the subprocess and the DRC report 
        code respectively
    """
    os.environ['DESIGN_NAME'] = design_name
    os.rename(gds_file, '../../../res/results/6_final.gds')
    sky130_path = Path(str(os.getenv('COMMON_VERIF_DIR')).replace("\\", "")) / "sky130A"
    pdk_root = '/usr/bin/miniconda3/share/pdk'
    
    if not sky130_path.exists():
        print(f"Sky130A directory not found at {sky130_path}")
        os.mkdir(sky130_path)
    
    # source_file = os.path.join(pdk_root, 'libs.tech/magic/sky130A.magicrc')
    # shutil.copy2(source_file, sky130_path)
    # source_file = os.path.join(pdk_root, 'libs.tech/netgen/sky130A_setup.tcl')
    # shutil.copy2(source_file, sky130_path)
    
    cmd = 'bash -c "../../common/drc-lvs-check/run_drc.sh"'
    subproc = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    subproc.wait()
    
    subproc_code = subproc.returncode
    drc_report_code = 0
    
    with open('../../../res/reports/6_final_drc.rpt', 'r') as f:
        # print number of lines
        num_lines = len(f.readlines())
        if num_lines > 3:
            drc_report_code = 1
            f.seek(0)
            print(f.read())
                    
    
    os.rename('../../../res/results/6_final.gds', gds_file)
    
    return [subproc_code, drc_report_code]


def check_errors(list_of_errors: list, comp: str, pdk):
    """helper function to print the errors if any

    Args:
        list_of_errors (list): the list of errors returned by run_glayout_drc
        comp (str): the name of the component
    """
    if list_of_errors[0] == 1:
        print(f"Error in running default {comp} for {pdk.name}")
        sys.exit(1)
    elif list_of_errors[1] == 1:
        warnings.warn(f"DRC returned non-zero errors for {comp} for {pdk.name}")
    else:
        print(f"DRC passed successfully for {comp} for {pdk.name}")
        
def run_drc_wrapper(pdk, components: list):
    """wrapper function to run DRC on a list of components

    Args:
        pdk (MappedPDK): sky130 or gf180, the process-design-kit being used
        components (list): a list of components to run DRC on, contains the name of the 
            component, the function to generate it and the arguments to be passed to the function
    """
    error_codes = []
    for component_info in components:
        component_name, component_function, *args = component_info
        
        inst = place_component(component_name, component_function, pdk, *args)
        error_codes.append(eval_component(inst, pdk, 1))
        