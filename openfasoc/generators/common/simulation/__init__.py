"""A common simulation used in OpenFASOC generators.

Sweeps all combinations of given parameters and runs parallel SPICE simulations with different configurations based on the parameters.

Exported functions:
- `run_simulations()`
"""

from os import path, makedirs
from common.simulation.simulation_config import _generate_configs
from common.simulation.simulation_run import _run_simulations

def run_simulations(
	parameters: dict,
	platform: str,
	simulation_dir: str = "simulations",
	template_path: str = path.join("templates", "template.sp"),
	runs_dir: str = "runs",
	sim_tool: str = "ngspice",
	num_concurrent_sims: int = 4,
	netlist_path: str = "netlist.sp"
) -> dict:
	"""Runs SPICE simulations.

    Generates configurations of all combinations of the given `parameters` and simulates each case. The testbench SPICE file, configuration parameters, and the output for each run are generated in the `simulation_dir/runs_dir` directory.

    The testbench SPICE file given by `template_path` follows the [Mako](https://makotemplates.org) templating syntax. Use the `${parameter}` syntax for inserting parameters in the file. The following parameters are automatically inserted during each run.
    - `run_number` (int): The number/index of the run/configuration.
    - `sim_tool` (str): Command for the simulation tool used.
    - `platform` (str): The platform/PDK.
    - `template` (str): Path to the SPICE testbench template.
    - `netlist_path` (str): Absolute path to the SPICE netlist of the design to be simulated.

    Each configuration is run/simulated in a directory in the `runs_dir`. Each run directory contains the final SPICE testbench with the parameters inserted, a `parameters.txt` file containing the values of each parameter, and the output log file.

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
    - `platform` (str): Platform/PDK.
    - `simulation_dir` (str = "simulations"): Path to the directory where the simulation source files are placed and the outputs will be generated.
    - `template_path` (str = "templates/template.sp"): Path to the SPICE template file for the testbench. (The template is a SPICE file with [Mako](https://makotemplates.org) templating syntax)
    - `runs_dir` (str = "runs"): Path to a directory inside the `simulation_dir` directory where the outputs for the simulations will be generated.
    - `sim_tool` (str = "ngspice"): Command for the simulation tool.
    - `num_concurrent_sims` (int = 4): The maximum number of concurrent simulations.
    - `netlist_path` (str = "netlist.sp"): Path to the SPICE netlist of the design to be simulated.

    Returns : A dictionary containing the number of ongoing (ideally 0), completed and failed simulations.
	"""

	runs_dir_path = path.join(simulation_dir, runs_dir)
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

	sim_state = _run_simulations(
		num_configs=config_number,
		num_concurrent_sims=num_concurrent_sims,
		sim_tool=sim_tool,
		runs_dir_path=runs_dir_path
	)

	return sim_state
