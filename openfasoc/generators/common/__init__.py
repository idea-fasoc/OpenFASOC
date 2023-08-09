"""A common module used in OpenFASOC generators.

This module exports functions used in OpenFASOC generators. The following submodules and functions are exported.

- `common.verilog_generation`
	1. `generate_verilog(parameters: dict, src_dir: str, out_dir: str) -> None`: Used to generate synthesizable Verilog files (for OpenROAD flow) from source Mako-based Verilog templates.
	2. `COMMON_PLATFORMS_PREFIX_MAP` (dict): This is a dictionary of common platforms (currently sky130) and their cell naming prefixes.
- `common.simulation`
	1. `run_simulations()`: Used to run SPICE testbenches with multiple parameters.

See individual function documentation for more information on a particular function.
"""