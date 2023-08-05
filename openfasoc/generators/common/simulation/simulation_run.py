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
	"""Runs (simulates) the generated configurations.

    Runs `num_configs` number of simulations, with configurations in the `runs_dir_path` directory.

    Arguments:
    - `num_configs` (int): Number of configurations generated in the `runs_dir_path` directory.
    - `num_concurrent_sims` (int): The maximum number of concurrent simulations.
    - `sim_tool` (str): Path to the directory in which the simulation runs will be generated.
    - `runs_dir_path` (str): Path to the directory in which the simulation runs will be generated.
	"""

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
	"""Runs (simulates) a particular configuration.

	Runs the `run_number`th configuration in the `run_dir` directory.

	Arguments:
	- `sim_tool` (str): Command for the simulation tool. (Currently only supports `ngspice`)
	- `run_dir` (str): Path to the directory in which the run configuration exists.
	- `run_number` (int): The number/index of the run configuration.
	- `on_exit` (function): An optional function to run when the simulation completes.
	"""

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
	"""Runs a particular simulation using `sim_tool` in a `threading.Thread`.

	Arguments:
	- `sim_tool` (str): Command for the simulation tool. (Currently only supports `ngspice`)
	- `run_dir` (str): Path to the directory in which the run configuration exists.
	- `run_number` (int): The number/index of the run configuration.
	- `on_exit` (function): An optional function to run when the simulation completes.
	"""

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