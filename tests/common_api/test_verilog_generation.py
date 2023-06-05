import os
import sys
from shutil import rmtree

# Add the common API to the path
# TODO: Find a better way to import the modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'openfasoc', 'generators', 'common'))

import verilog_generation

TEST_VERILOG_DIR = os.path.join(os.path.dirname(__file__), 'test-verilog')
SRC_VERILOG_DIR = os.path.join(TEST_VERILOG_DIR, 'src')
TEST_FILENAME = 'TEMP_ANALOG_lv.v'

def test_different_params(tmp_path):
	PARAMETERS_1={
		"cell_prefix": "sky130_fd_sc_hd__",
		"cell_suffix": "_1",
		"ninv": 6
	}

	PARAMETERS_2={
		"cell_prefix": "sky130_fd_sc_hd__",
		"cell_suffix": "_1",
		"ninv": 8
	}

	input_path = os.path.join(SRC_VERILOG_DIR, TEST_FILENAME)

	output_path_1 = os.path.join(tmp_path, TEST_FILENAME + '.1')
	output_path_2 = os.path.join(tmp_path, TEST_FILENAME + '.2')

	expected_file_1 = os.path.join(TEST_VERILOG_DIR, 'expected-sky130hd-6inv', TEST_FILENAME)
	expected_file_2 = os.path.join(TEST_VERILOG_DIR, 'expected-sky130hd-8inv', TEST_FILENAME)

	verilog_generation._generate_file(input_path, output_path_1, PARAMETERS_1)
	verilog_generation._generate_file(input_path, output_path_2, PARAMETERS_2)

	generated_verilog_1 = open(output_path_1).read()
	generated_verilog_2 = open(output_path_2).read()


	expected_verilog_1 = open(expected_file_1).read()
	expected_verilog_2 = open(expected_file_2).read()

	assert generated_verilog_1 == expected_verilog_1, "Generated Verilog does not match the expected Verilog (6 inverters)."
	assert generated_verilog_2 == expected_verilog_2, "Generated Verilog does not match the expected Verilog (8 inverters)."