import sys
from os import path

# TODO: Find a better way to import modules from parent directory
sys.path.append(path.join(path.dirname(__file__), '..', '..'))
from common.simulation import run_simulations

def run_dcdc_simulations(
	platform: str,
	sim_tool: str,
	open_pdks_root: str,
	json_config: dict
):
	run_simulations(
		parameters={
			**generate_dcdc_sim_params(),
			'model_file': path.join(open_pdks_root, 'libs.tech', sim_tool, 'sky130.lib.spice'),
			'model_corner': json_config['platforms'][platform]['model_corner']
		},
		platform=platform,
		sim_tool=sim_tool,
		template_path=path.join('templates', 'dcdc-testbench.sp'),
		netlist_path=path.join("simulations", "dcdc_synth_extracted_power_pins.sp"),
		num_concurrent_sims=2
	)

def generate_dcdc_sim_params():
	parameters = {}

	# Each of sel_vh[i] and sel_vl[i] can either be HIGH ('vvdd') or LOW (0)
	# Since there are 2^12 possibilities, only all high and all low possibilities (total 4) are simulated
	for i in range(6):
		parameters[f"sel_vh"] = [["'vvdd'"] * 6, ["0"] * 6]
		parameters[f"sel_vl"] = [["'vvdd'"] * 6, ["0"] * 6]

	return parameters