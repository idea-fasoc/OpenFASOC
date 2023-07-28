from os import path, makedirs
from common.verilog_generation import _generate_file

def _generate_configs(
	parameters: dict,
	sim_tool: str,
	platform: str,
	template: str,
	netlist_path: str,
	runs_dir_path: str
) -> int:
	parameters_iterator = {}

	for parameter in parameters.items():
		parameter_values = []

		if type(parameter[1]) is dict:
			parameter_values = parameter[1]['values']
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
	run_dir_path = path.join(runs_dir_path, str(config_number))

	if not path.exists(run_dir_path):
		makedirs(run_dir_path)

	open(path.join(run_dir_path, 'parameters.txt'), "w").write(str(run_parameters))

	_generate_file(
		input_path=template,
		output_path=path.join(run_dir_path, f"sim_{config_number}.sp"),
		parameters=run_parameters
	)