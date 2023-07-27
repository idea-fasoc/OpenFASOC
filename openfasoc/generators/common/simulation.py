from os import path, makedirs
from common.verilog_generation import _generate_file
import time
import subprocess
import threading

def run_simulations(
	parameters: dict,
	simulation_dir: str = "simulations",
	template_path: str = path.join("templates", "template.sp"),
	run_dir: str = "runs",
	sim_tool: str = "ngspice",
	num_concurrent_sims: int = 4,
	netlist_path: str = "netlist.sp"
) -> None:
	runs_dir_path = path.join(simulation_dir, run_dir)
	template = path.join(simulation_dir, template_path)

	if not path.exists(runs_dir_path):
		makedirs(runs_dir_path)

	config_number = _generate_configs(
		parameters=parameters,
		sim_tool=sim_tool,
		platform=platform,
		template=template,
		netlist_path=netlist_path,
		runs_dir_path=runs_dir_path
	)

	print(f"Number of configurations: {config_number}")
	print(f"Number of concurrent simulations: {num_concurrent_sims}")

	_run_simulations(
		config_number=config_number,
		num_concurrent_sims=num_concurrent_sims,
		sim_tool=sim_tool,
		runs_dir_path=runs_dir_path
	)

def _run_simulations(
	config_number: int,
	num_concurrent_sims: int,
	sim_tool: str,
	runs_dir_path: str
):
	simulation_state = {
		'ongoing_sims': 0,
		'completed_sims': 0
	}

	def thread_on_exit(state=simulation_state):
		state['ongoing_sims'] -= 1
		state['completed_sims'] += 1

	start_time = int(time.time())
	run_number = 1
	while simulation_state['completed_sims'] < config_number:
		if simulation_state['ongoing_sims'] < num_concurrent_sims and run_number <= config_number:
			_run_config(
				sim_tool=sim_tool,
				run_dir=path.join(runs_dir_path, str(run_number)),
				run_number=run_number,
				on_exit=thread_on_exit
			).start()

			simulation_state['ongoing_sims'] += 1
			run_number += 1

		_print_progress(config_number, simulation_state['completed_sims'], start_time)
		time.sleep(1)

	_print_progress(config_number, simulation_state['completed_sims'], start_time, end='\n')

def _print_progress(total_runs: int, run_number: int, start_time: int, end: str = '\r'):
	print(f"Completed {run_number} out of {total_runs} simulations. Elapsed time: {_format_elapsed_time(start_time)}", end=end)

def _format_elapsed_time(start_time: int):
	elapsed_seconds = int(time.time()) - start_time

	if elapsed_seconds > 60 * 60:
		hours, minutes = divmod(elapsed_seconds, 60 * 60)
		minutes, seconds = divmod(minutes, 60)
		return f"{hours}h {minutes}m {seconds}s"

	elif elapsed_seconds > 60:
		minutes, seconds = divmod(elapsed_seconds, 60)
		return f"{minutes}m {seconds}s"

	else:
		return f"{elapsed_seconds}s"

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
		parameters_iterator[parameter[0]] = {
			'values': parameter[1]['values'],
			'i': 0
		}

	num_params = len(parameters_iterator.keys())
	config_number = 0
	configs_generated = num_params == 0
	while not configs_generated:
		config_number += 1
		_generate_configs(
			run_parameters=_generate_config(parameters_iterator, config_number, sim_tool, template, netlist_path),
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

def _generate_config(
	parameters_iterator: dict,
	config_number: int,
	sim_tool: str,
	template: str,
	netlist_path: str
) -> dict:
	run_parameters = {
		'run_number': config_number,
		'sim_tool': sim_tool,
		'template': template,
		'netlist_path': path.abspath(netlist_path),
		'root_dir': path.abspath('.')
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
	run_number: int,
	on_exit
):
	return threading.Thread(
		target=_threaded_run,
		args=(sim_tool, run_dir, run_number, on_exit),
		daemon=True
	)

def _threaded_run(
	sim_tool: str,
	run_dir: str,
	run_number: int,
	on_exit
):
	match sim_tool:
		case "ngspice":
			subprocess.Popen(
				[
					"ngspice",
					"-b",
					f"-o sim_{run_number}.log",
					f"sim_{run_number}.sp"
				],
				cwd=run_dir,
				stdout=subprocess.DEVNULL,
			).wait()

	on_exit()