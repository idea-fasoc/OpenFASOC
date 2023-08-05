from os import path
from common.simulation.utils import _print_progress
import time
import threading
import subprocess

def _run_simulations(
	num_configs: int,
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
	while simulation_state['completed_sims'] < num_configs:
		if simulation_state['ongoing_sims'] < num_concurrent_sims and run_number <= num_configs:
			_run_config(
				sim_tool=sim_tool,
				run_dir=path.join(runs_dir_path, str(run_number)),
				run_number=run_number,
				on_exit=thread_on_exit
			).start()

			simulation_state['ongoing_sims'] += 1
			run_number += 1

		_print_progress(num_configs, simulation_state['completed_sims'], start_time)
		time.sleep(1)

	_print_progress(num_configs, simulation_state['completed_sims'], start_time, end='\n')

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