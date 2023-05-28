from mako.template import Template
from os import path, makedirs, listdir

def __get_output_filepath(filename: str, out_dir: str) -> str:
	return path.join(out_dir, filename.replace(".template", ""))

def __generate_file(input_path: str, output_path: str, parameters: dict) -> None:
	template = Template(filename=input_path)

	out_file = open(output_path, "w")
	out_file.write(template.render(**parameters))

def __generate_subdirectory(src_dir: str, out_dir: str, parameters: dict) -> None:
	# generate the output directory if it doesn't exist
	if not path.exists(out_dir):
		makedirs(out_dir)

	for filename in listdir(src_dir):
		file_path = path.join(src_dir, filename)

		if path.isdir(file_path):
			# if the path is a subdirectory, recursively call the function
			__generate_subdirectory(file_path, path.join(out_dir, filename), parameters)
		else:
			# if the path is a fine, generate the output
			__generate_file(
				file_path,
				__get_output_filepath(filename, out_dir),
				parameters
			)

def generate_verilog(
	parameters: dict,
	src_dir: str = "src",
	out_dir: str = path.join("flow", "design", "src")
) -> None:
	__generate_subdirectory(src_dir, out_dir, parameters)