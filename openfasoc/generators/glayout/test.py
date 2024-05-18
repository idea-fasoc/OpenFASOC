from glayout.flow.pdk.util.drc_lvs.drc_lvs_helpers import run_glayout_drc

results = run_glayout_drc(gds_file_path='./my_opamp_test.gds', DESIGN_NAME='opamp_test', PDK_ROOT='/usr/bin/miniconda3/share/pdk/', RESULTS_DIR='./', REPORTS_DIR='./', magicrc_file='./glayout/flow/pdk/sky130_mapped/sky130A.magicrc', magic_commands_tcl_file='./magic_commands.tcl')
print(f'results: {results}') 
