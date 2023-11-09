import sys
import os
import re
import pytest
from shutil import rmtree

# Add the common API to the path
# TODO: Find a better way to import the modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'openfasoc', 'generators'))

from common.simulation import run_simulations

TEST_SIMULATION_DIR = os.path.join(os.path.dirname(__file__), 'test-simulation')
EXPECTED_CONFIGS_DIR = os.path.join(TEST_SIMULATION_DIR, 'expected')
RUNS_DIR = os.path.join(TEST_SIMULATION_DIR, 'runs')

PARAMS = {
	'temp': {'start': -5, 'end': 5, 'step': 10},
	'netlist_subckt_name': 'TEST_NETLIST',
	'Vhigh': [1, 10],
	'end_time': 1,
	'freq': ['1k', '10k']
}

EXPECTED_NUM_CONFIGS = 8

# From the temperature senssor generator.
def get_value(log_file_text, key):
	"""Finds a value in the simulation log file.

	Finds and returns the value from a statement of the format key = value.
	"""
	pattern = f"{key}\s*=\s*([0-9\.e-]+)"
	pattern_re = re.search(pattern, log_file_text, flags=re.IGNORECASE)
	value = "NOT_FOUND"

	if pattern_re:
		value = pattern_re.group(1)

	return value

def isfloat(num: str):
	"""Checks if a string represents a float."""
	try:
		float(num)
		return True

	except ValueError:
		return False

@pytest.fixture(autouse=False)
def run_before_and_after_tests():
	"""Cleans the runs directory before and after tests."""
	if os.path.exists(RUNS_DIR):
		rmtree(RUNS_DIR)

	yield

	if os.path.exists(RUNS_DIR):
		rmtree(RUNS_DIR)

def test_simulations():
	num_runs = run_simulations(
		parameters=PARAMS,
		platform = "",
		simulation_dir = TEST_SIMULATION_DIR,
		template_path = os.path.join(TEST_SIMULATION_DIR, 'src', 'template.sp'),
		num_concurrent_sims = 8
	)

	# Check if the correct number of configurations are generated
	assert num_runs == EXPECTED_NUM_CONFIGS, "The number of runs does not match the expected number."
	assert len(os.listdir(RUNS_DIR)) == EXPECTED_NUM_CONFIGS, "The number of generated configurations does not match the expected number."


	for i in range(1, EXPECTED_NUM_CONFIGS + 1):
		expected_spice_path = os.path.join(EXPECTED_CONFIGS_DIR, str(i), f"sim_{i}.sp")

		run_dir = os.path.join(RUNS_DIR, str(i))
		generated_spice_path = os.path.join(run_dir, f"sim_{i}.sp")
		generated_log_file_path = os.path.join(run_dir, f"sim_{i}.log")
		parameters_file_path = os.path.join(run_dir, f"parameters.txt")

		# Check if all the correct files are generated
		assert os.path.exists(generated_spice_path), f"SPICE file is not generated for config #{i}"
		assert os.path.exists(generated_log_file_path), f"Simulation log file is not generated for config #{i}"
		assert os.path.exists(parameters_file_path), f"parameters.txt file is not generated for config #{i}"

		# Check if the generated spice matches
		with open(expected_spice_path) as expected_spice:
			with open(generated_spice_path) as generated_spice:
				assert generated_spice.read() == expected_spice.read(), f"Generated SPICE does not match the expected SPICE for config #{i}"

		# Check if the simulations are run correctly
		with open(generated_log_file_path) as log_file:
			log_file_text = log_file.read()
			# 1. Search for vrms and irms values
			vrms_value = get_value(log_file_text, 'vrms')
			irms_value = get_value(log_file_text, 'irms')

			assert vrms_value != "NOT_FOUND", f"`vrms` value not found in the simulation output for config #{i}"
			assert irms_value != "NOT_FOUND", f"`irms` value not found in the simulation output for config #{i}"
