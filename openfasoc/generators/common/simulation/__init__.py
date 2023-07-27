from os import path, makedirs
from common.simulation.simulation_config import _generate_configs
from common.simulation.simulation_run import _run_simulations

def run_simulations(
	parameters: dict,
	platform: str,
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
