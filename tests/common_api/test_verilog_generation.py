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
TEST_SUBDIR_FILENAME = 'TEMP_ANALOG_hv.v'

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

def test_directory_structure(tmp_path):
	PARAMETERS={
		"cell_prefix": "sky130_fd_sc_hd__",
		"cell_suffix": "_1",
		"header_cell": "HEADER",
		"slc_cell": "SLC",
		"ninv": 6,
		"nhead": 3
	}

	expected_file_1 = os.path.join(TEST_VERILOG_DIR, 'expected-sky130hd-6inv', TEST_FILENAME)
	expected_file_2 = os.path.join(TEST_VERILOG_DIR, 'expected-sky130hd-6inv', 'subdirectory', TEST_SUBDIR_FILENAME)

	output_path_1 = os.path.join(tmp_path, TEST_FILENAME)
	output_subdir = os.path.join(tmp_path, 'subdirectory')
	output_path_2 = os.path.join(output_subdir, TEST_SUBDIR_FILENAME)

	verilog_generation.generate_verilog(PARAMETERS, SRC_VERILOG_DIR, tmp_path)

	# Check if all the expected files and directories exist
	assert os.path.exists(output_path_1), "Generated Verilog file does not exist."
	assert os.path.exists(output_subdir), "Subdirectory does not exist in generated Verilog."
	assert os.path.exists(output_path_2), "Files from subdirectory do not exist in generated Verilog."

	# Check if all the expected files are correctly generated
	generated_verilog_1 = open(output_path_1).read()
	generated_verilog_2 = open(output_path_2).read()

	expected_verilog_1 = open(expected_file_1).read()
	expected_verilog_2 = open(expected_file_2).read()

	assert generated_verilog_1 == expected_verilog_1, "Generated Verilog does not match the expected Verilog for first file."
	assert generated_verilog_2 == expected_verilog_2, "Generated Verilog does not match the expected Verilog for the subdirectory file."
