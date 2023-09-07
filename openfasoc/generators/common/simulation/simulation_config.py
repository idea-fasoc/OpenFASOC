"""Sweeps all combinations of given parameters and generates the configurations.

This module is part of the simulation common module. Functions for generating final SPICE files from a template are exported.

Configurations are generated from a template SPICE file that follows the [Mako](https://makotemplates.org) syntax. All possible combinations of the input parameters are swept. The final SPICE files are generated from the template by inserting the parameter combinations. Each file is called a "config" or "configuration."

Exported functions:
- `_generate_configs()`
- `_generate_run_parameters()`
- `_generate_config()`

See individual functions for further documentation.
"""

from os import path, makedirs
from shutil import rmtree
from common.verilog_generation import _generate_file

def _generate_configs(
	parameters: dict,
	sim_tool: str,
	platform: str,
	template: str,
	netlist_path: str,
	runs_dir_path: str
) -> int:
	"""Generates configurations for the simulations.

    Generates a directory for each configuration in the runs directory given by `runs_dir_path`. Each configuration includes a testbench SPICE file (`sim_[run_number].sp`) corresponding to the configuration and a `parameters.txt` file containing the values of each parameter in the particular configuration.

    `parameters` is a dict with keys corresponding to the parameter's name and the values of one of the following types.
    1. A constant value.
    The value of this parameter will be the same for every configuration/run.
    ```
    {'param': 'value'}
    ```

    2. Array of integer/float/string constants.
    Each of the values in the array will be swept.
    ```
    {'param': [1, 2, 3, 8]}
    # OR
    {
        'param': {
            'values': [1, 2, 3, 8]
        }
    }
    ```

    3. Increments.
    All values starting from `start` and ending at `end` will be swept with a step of `step`. The default value for `step` is `1`.
    ```
    {'param': {
        'start': 10,
        'end': 50,
        'step': 10
    }}
    # param will take values 10, 20, 30, 40, 50
    ```

    Arguments:
    - `parameters` (dict): Parameters used to generate the runs.
    - `sim_tool` (str): Command for the simulation tool.
    - `platform` (str): Platform/PDK.
    - `template` (str): Path to the SPICE template file for the testbench. (The template is a SPICE file with [Mako](https://makotemplates.org) templating syntax)
    - `netlist_path` (str): Path to the netlist file used for simulation. (Absolute path to this file will be added as a Mako parameter)
    - `runs_dir_path` (str): Path to the directory in which the simulation runs will be generated.
	"""
	parameters_iterator = {}

	for parameter in parameters.items():
		parameter_values = []

		if type(parameter[1]) is dict:
			if 'values' in parameter[1]:
				parameter_values = parameter[1]['values']

			elif 'start' in parameter[1] and 'end' in parameter[1]:
				value = parameter[1]['start']
				step = parameter[1]['step'] if 'step' in parameter[1] else 1

				while value <= parameter[1]['end']:
					parameter_values.append(value)
					value += step

		elif type(parameter[1]) is list:
			parameter_values = parameter[1]

		else:
			parameter_values = [parameter[1]]

		parameters_iterator[parameter[0]] = {
			'values': parameter_values,
			'i': 0
		}

	num_params = len(parameters_iterator.keys())
	config_number = 0
	configs_generated = num_params == 0
	while not configs_generated:
		config_number += 1
		_generate_config(
			run_parameters=_generate_run_parameters(
				parameters_iterator=parameters_iterator,
				config_number=config_number,
				sim_tool=sim_tool,
				platform=platform,
				template=template,
				netlist_path=netlist_path
			),
			config_number=config_number,
			runs_dir_path=runs_dir_path,
			template=template
		)

		change_next_param = True
		for i, parameter in enumerate(parameters_iterator.items()):
			if change_next_param:
				parameter[1]['i'] += 1

			change_next_param = parameter[1]['i'] == len(parameter[1]['values'])

			if change_next_param:
				parameter[1]['i'] = 0

			if i == num_params - 1 and change_next_param:
				configs_generated = True

	return config_number

def _generate_run_parameters(
	parameters_iterator: dict,
	config_number: int,
	sim_tool: str,
	platform: str,
	template: str,
	netlist_path: str
) -> dict:
	"""Generates and returns parameters for a given run.

    Generates and returns the final parameters for a given run from the parameters iterator and the number of the config.

    Arguments:
    - `parameters_iterator` (dict): A dictionary with keys equal to the parameter name and values of the following format: `{'values': list[str], 'i': int}`. Here `values` is a list of all the possible values the particular parameter can take, and `i` is the value selected for the current config.
    - `config_number` (str): The number/index of the configuration.
    - `sim_tool` (str): Command for the simulation tool.
    - `platform` (str): Platform/PDK.
    - `template` (str): Path to the SPICE template file for the testbench. (The template is a SPICE file with [Mako](https://makotemplates.org) templating syntax)
    - `netlist_path` (str): Path to the netlist file used for simulation. (Absolute path to this file will be added as a Mako parameter)
	"""
	run_parameters = {
		'run_number': config_number,
		'sim_tool': sim_tool,
		'platform': platform,
		'template': template,
		'netlist_path': path.abspath(netlist_path),
		'root_dir': path.abspath('.')
	}

	for parameter in parameters_iterator.items():
		run_parameters[parameter[0]] = parameter[1]['values'][parameter[1]['i']]

	return run_parameters

def _generate_config(
	run_parameters: dict,
	config_number: int,
	runs_dir_path: str,
	template: str
) -> None:
	"""Generates the files required for a particular configuration.

    Generates the files (SPICE testbench file and `parameters.txt`) for a particular configuration/run in the directory for the run.

    Arguments:
    - `run_parameters` (dict): Parameters for the particular run.
    - `config_number` (str): The number/index of the configuration.
    - `runs_dir_path` (str): Path to the directory in which the simulation runs will be generated.
    - `template` (str): Path to the SPICE template file for the testbench. (The template is a SPICE file with [Mako](https://makotemplates.org) templating syntax)
	"""
	run_dir_path = path.join(runs_dir_path, str(config_number))

	if not path.exists(run_dir_path):
		makedirs(run_dir_path)
	else:
		rmtree(run_dir_path)
		makedirs(run_dir_path)

	open(path.join(run_dir_path, 'parameters.txt'), "w").write(str(run_parameters))

	_generate_file(
		input_path=template,
		output_path=path.join(run_dir_path, f"sim_{config_number}.sp"),
		parameters=run_parameters
	)