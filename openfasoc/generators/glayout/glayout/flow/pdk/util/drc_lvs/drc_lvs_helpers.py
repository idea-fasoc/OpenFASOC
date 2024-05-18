import shutil
import os
import sys
import pathlib
import subprocess as sp

def clean_copied_files(util_dir: str):
    """cleans the copied files from the pdk directory to revert to original state

    Args:
        util_dir (str): path to the util directory in the pdk folder
    """
    if os.path.exists(f'{util_dir}/../../sky130_mapped/sky130A.magicrc'):
        os.remove(f'{util_dir}/../../sky130_mapped/sky130A.magicrc')
    if os.path.exists(f'{util_dir}/../../sky130_mapped/sky130A_setup.tcl'):
        os.remove(f'{util_dir}/../../sky130_mapped/sky130A_setup.tcl')
    if os.path.exists(f'{util_dir}/../../gf180_mapped/gf180mcuC.magicrc'):
        os.remove(f'{util_dir}/../../gf180_mapped/gf180mcuC.magicrc')
    if os.path.exists(f'{util_dir}/../../gf180_mapped/gf180mcuC_setup.tcl'):
        os.remove(f'{util_dir}/../../gf180_mapped/gf180mcuC_setup.tcl')
        
# pdk is sky130 or gf180
def copy_pdk_files(pdk: str):
    # get stdout of os.system('whereis conda')
    utildir = pathlib.Path(__file__).resolve().parent
    CONDA_PREFIX = os.popen('whereis conda').read().split(' ')[1].strip()
    MINICONDA_PREFIX = CONDA_PREFIX.removesuffix('/bin/conda')
    print(f'MINICONDA_PREFIX: {MINICONDA_PREFIX}')
    if pdk == 'sky130':
        PDK_ROOT = f'{MINICONDA_PREFIX}/share/pdk/{pdk}A'
        magicrc_file = f'{PDK_ROOT}/libs.tech/magic/{pdk}' + 'A.magicrc'
        lvs_setup_file = f'{PDK_ROOT}/libs.tech/netgen/{pdk}' + 'A_setup.tcl'
        dest_magicrc = f'{utildir}/../../{pdk}_mapped/{pdk}' + 'A.magicrc'
        dest_lvs_setup = f'{utildir}/../../{pdk}_mapped/{pdk}' + 'A_setup.tcl'
    elif pdk == 'gf180':
        PDK_ROOT = f'{MINICONDA_PREFIX}/share/pdk/{pdk}' + 'mcuC'
        magicrc_file = f'{PDK_ROOT}/libs.tech/magic/{pdk}' + 'mcuC.magicrc'
        lvs_setup_file = f'{PDK_ROOT}/libs.tech/netgen/{pdk}' + 'mcuC_setup.tcl'
        dest_magicrc = f'{utildir}/../../{pdk}_mapped/{pdk}' + 'mcuC.magicrc'
        dest_lvs_setup = f'{utildir}/../../{pdk}_mapped/{pdk}' + 'mcuC_setup.tcl'
    
    if os.path.exists(magicrc_file) and not os.path.exists(dest_magicrc):
        print(f'copying file to required pdk dir: {magicrc_file}')
        shutil.copy(magicrc_file, f'{utildir}/../../{pdk}_mapped/')
    else: 
        print(f'Either file not found: {magicrc_file}, or already copied to: {dest_magicrc}')
    if os.path.exists(lvs_setup_file) and not os.path.exists(dest_lvs_setup):
        print(f'copying file to required pdk dir: {lvs_setup_file}')
        shutil.copy(lvs_setup_file, f'{utildir}/../../{pdk}_mapped/')
    else:
        print(f'Either file not found: {lvs_setup_file}, or already copied to: {dest_lvs_setup}')
    
def run_glayout_drc(gds_file_path: str, DESIGN_NAME: str, PDK_ROOT: str, RESULTS_DIR: str, magicrc_file: str, REPORTS_DIR: str, magic_commands_tcl_file: str):
    os.environ['PDK_ROOT'] = PDK_ROOT
    os.environ['REPORTS_DIR'] = REPORTS_DIR
    os.environ['RESULTS_DIR'] = RESULTS_DIR 
    os.environ['DESIGN_NAME'] = DESIGN_NAME
    print(f'PDK_ROOT: {PDK_ROOT}, REPORTS_DIR: {REPORTS_DIR}, RESULTS_DIR: {RESULTS_DIR}, DESIGN_NAME: {DESIGN_NAME}')
    # os.rename(gds_file_path, f'{RESULTS_DIR}/{DESIGN_NAME}.gds')
    
    if os.path.exists(f'{REPORTS_DIR}/{DESIGN_NAME}.rpt') and os.path.exists(magicrc_file) and os.path.exists(magic_commands_tcl_file):
        print(f'All files exist: {REPORTS_DIR}/{DESIGN_NAME}.rpt, {RESULTS_DIR}/{DESIGN_NAME}.gds, {magicrc_file}, {magic_commands_tcl_file}')
    cmd = f'bash -c "magic -rcfile {magicrc_file} -noconsole -dnull {magic_commands_tcl_file} < /dev/null"'
    subp = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    subp.wait()
    # print output
    print(subp.stdout.read().decode('utf-8'))
    
    subproc_code = subp.returncode
    drc_report_code = 0
    
    # with open(f'{REPORTS_DIR}/{DESIGN_NAME}.rpt', 'r') as f:
    #     # print number of lines
    #     num_lines = len(f.readlines())
    #     if num_lines > 3:
    #         drc_report_code = 1
    #         f.seek(0)
    #         print(f.read())
                    
    
    # os.rename(f'{RESULTS_DIR}/{DESIGN_NAME}.gds', gds_file_path)
    
    return [subproc_code, drc_report_code]
    