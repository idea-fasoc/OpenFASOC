import json
import os

def check_gen_files(json_filename, _generator_is, cryo_library) -> int:
    with open(json_filename) as file:
        data = json.load(file)
    
    # print('Found .json config file...')

    module_name = data.get("module_name", "default")

    if _generator_is['sky130XX_cryo']:
        work_dir = "./work/" + cryo_library + "/"
    else:
        work_dir = "./work/"

    if (os.path.exists(work_dir) == 0):
        raise ValueError("work directory does not exist!")
    else:
        filename = work_dir + module_name
        extension_file_path = "./tools/check_gen_extensions"

        if os.path.exists(extension_file_path):
            with open(extension_file_path) as f:
                
                for extension in f:
                    file = "".join([filename, extension.strip()])
                    if (os.path.exists(file) == 0):
                        raise ValueError(file + " does not exist!")
        else: 
            print("checking flow results with possibly stale list of extensions...")
            extensions = [".sdc", ".gds", ".def", ".spice", ".v", "_pex.spice"]
            for extension in extensions:
                    file = "".join([filename, extension])
                    
                    if (os.path.exists(file) == 0):
                        raise ValueError(file + " does not exist!")
    # print("Found necessary work result files!")
    if _generator_is['sky130hd_temp']:
        for file in ("error_within_x.csv", "golden_error_opt.csv", "search_result.csv"):
            if os.path.exists(file) == 0:
                raise ValueError(file + " does not exist!")
    
    #print("Found generated .csv files!")
    return 1
