"""A common module used in OpenFASOC generators.

This module exports functions used in OpenFASOC generators. The following submodules and functions are exported.

- `common.verilog_generation`
	1. `generate_verilog(parameters: dict, src_dir: str, out_dir: str) -> None`: Used to generate synthesizable Verilog files (for OpenROAD flow) from source Mako-based Verilog templates.

See individual function documentation for more information on a particular function.
"""