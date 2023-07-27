from os import path, makedirs
from verilog_generation import _generate_file
import subprocess

def run_simulations(
	parameters: dict,
	simulation_dir: str = "simulations",
	template_path: str = path.join("templates", "template.sp"),
	run_dir: str = "runs",
	sim_tool: str = "ngspice",
	num_concurrent_sims: int = 4
) -> None:
	runs_dir_path = path.join(simulation_dir, run_dir)
	template = path.join(simulation_dir, template_path)

	if not path.exists(runs_dir_path):
		makedirs(runs_dir_path)

	parameters_iterator = {}

	for parameter in parameters.items():
		parameters_iterator[parameter[0]] = {
			'values': parameter[1]['values'],
			'i': 0
		}

	num_params = len(parameters_iterator.keys())
	config_number = 0
	configs_generated = False
	while not configs_generated:
		config_number += 1
		_generate_configs(
			run_parameters=_generate_config(parameters_iterator, config_number, sim_tool, template),
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

	print(f"Number of configurations: {config_number}")
	print(f"Number of concurrent simulations: {num_concurrent_sims}")

	sim_processes: list[subprocess.Popen[bytes]] = []
	_print_progress(config_number, 0)
	for i in range(config_number):

		run_number = i + 1
		run_dir = path.join(runs_dir_path, str(run_number))

		sim_processes.append(_run_config(sim_tool, run_dir, run_number))

		if i % num_concurrent_sims == 0:
			# Wait for the last n simulations to complete
			_finish_processes(sim_processes)

		_print_progress(config_number, 0)

	_finish_processes(sim_processes)
	print(f"Completed {config_number} simulations.")


def _print_progress(total_runs: int, run_number: int):
	print(f"Completed {run_number} out of {total_runs} simulations", end='\r')

def _finish_processes(processess: list[subprocess.Popen[bytes]]):
	while len(processess) > 0:
		processess.pop().wait()

def _generate_config(
	parameters_iterator: dict,
	config_number: int,
	sim_tool: str,
	template: str
) -> dict:
	run_parameters = {
		'run_number': config_number,
		'sim_tool': sim_tool,
		'template': template
	}

	for parameter in parameters_iterator.items():
		run_parameters[parameter[0]] = parameter[1]['values'][parameter[1]['i']]

	return run_parameters

def _generate_configs(
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

def _run_config(
	sim_tool: str,
	run_dir: str,
	run_number: int
):
	match sim_tool:
		case "ngspice":
			return subprocess.Popen(
				[
					"ngspice",
					"-b",
					f"-o sim_{run_number}.log",
					f"sim_{run_number}.sp"
				],
				cwd=run_dir,
				stdout=subprocess.DEVNULL,
			)