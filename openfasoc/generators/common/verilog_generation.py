from mako.template import Template
from os import path, makedirs, listdir

# TODO: Find a better way to import common used defs in the future.
__COMMON_MAKO_DEFS = '''
<%def name="cell(name)">${cell_prefix}${name}${cell_suffix}</%def>
'''

def _mako_defs_preprocessor(input: str) -> str:
	"""A Mako preprocessor that appens commonly used defs to the template.

	Mako templates have a preprocessor argument. See https://docs.makotemplates.org/en/latest/usage.html#mako.template.Template.params.preprocessor.
	This preprocessor adds defs commonly used in Verilog files to the template.
	TODO: Find a better way to import common used defs in the future.
	"""
	return __COMMON_MAKO_DEFS + input

def _generate_file(input_path: str, output_path: str, parameters: dict) -> None:
	"""Generates a single output Verilog file from its Mako template.

	Arguments:
	- `input_path` (str): Path to the input file (Mako template) with the extension.
	- `output_path` (str): Path to the output file location with the extension.
	- `parameters` (dict): Dictionary of all the parameters used in the Mako template.
	"""

	# TODO: Find a better way to import common used defs in the future.
	template = Template(filename=input_path, preprocessor=_mako_defs_preprocessor)

	out_file = open(output_path, "w")
	out_file.write(template.render(**parameters))

def _generate_subdirectory(src_dir: str, out_dir: str, parameters: dict) -> None:
	"""Generates the output Verilog files of a single subdirectory of Mako templates.

	Reads Mako templates from a subdirectory (`src_dir`), generates the output files in the output directory (`out_dir`), and maintains the directory structure. i.e., templates from a subdirectory of the `src_dir` will be generated in a subdirectory in `out_dir` with the same name.

	This function recursively calls itself for subdirectories.

	Arguments:
	- `src_dir` (str): Path to the source directory with Mako templates.
	- `out_dir` (str): Path to the output directory.
	- `parameters` (dict): Dictionary of all the parameters used in the Mako template.
	"""
	# generate the output directory if it doesn't exist
	if not path.exists(out_dir):
		makedirs(out_dir)

	for filename in listdir(src_dir):
		input_filepath = path.join(src_dir, filename)
		output_filepath = path.join(out_dir, filename)

		if path.isdir(input_filepath):
			# if the path is a subdirectory, recursively call the function
			_generate_subdirectory(
				input_filepath,
				output_filepath,
				parameters
			)
		else:
			# if the path is a fine, generate the output
			_generate_file(
				input_filepath,
				output_filepath,
				parameters
			)

def generate_verilog(
	parameters: dict,
	src_dir: str = "src",
	out_dir: str = path.join("flow", "design", "src")
) -> None:
	"""Generates output Verilog files from source Mako templates.

	Reads source Verilog files from `src_dir` and generates output Verilog files for synthesis in the OpenROAD flow.
	The source files are Mako templates. See https://makotemplates.org for syntax and documentation.

	This function maintains the source directory (`src_dir`) structure in the output directory (`out_dir`). i.e., source files from a subdirectory of the `src_dir` will be generated in a subdirectory in `out_dir` with the same name.

	Arguments:
	- `parameters` (dict): Dictionary of all the parameters used in the Mako templates. See https://makotemplates.org for documentation.
	- `src_dir` (str): Path to the directory with the source Verilog templates.
	- `out_dir` (str): Path to the directory in which the output will be generated.
	"""
	_generate_subdirectory(src_dir, out_dir, parameters)

# A dictionary of commonly used platforms and the prefix used in their cell naming
# Currently includes only sky130 platform prefixes
COMMON_PLATFORMS_PREFIX_MAP = {
	"sky130hd": "sky130_fd_sc_hd__",
	"sky130hs": "sky130_fd_sc_hs__",
	"sky130hvl": "sky130_fd_sc_hvl__",
	"sky130osu12Ths": "sky130_osu_sc_12T_hs__",
	"sky130osu12Tms": "sky130_osu_sc_12T_ms__",
	"sky130osu12Tls": "sky130_osu_sc_12T_ls__",
	"sky130osu15Ths": "sky130_osu_sc_15T_hs__",
	"sky130osu15Tms": "sky130_osu_sc_15T_ms__",
	"sky130osu15Tls": "sky130_osu_sc_15T_ls__",
	"sky130osu18Ths": "sky130_osu_sc_18T_hs__",
	"sky130osu18Tms": "sky130_osu_sc_18T_ms__",
	"sky130osu18Tls": "sky130_osu_sc_18T_ls__"
}