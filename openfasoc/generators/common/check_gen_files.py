"""
This module is used to check for the presence of the required non-report files that each generator creates. It gets
the module_name (str) from the .json file present in the generator top-level folder.

Args:
    json_filename (str): String containing the name of the .json filename for each generator
    generator_is (dict): Dictionary containing key-value pairs that signify which generator's flow results are being checked
    cryo_library (str): String containing which cryo-gen library (sky130hs, sky130hd, sky130hvl) is being checked for
Uses: 
    work_dir (str): String containing the directory in which to check files
    data (str): String containing data from the .json file
    module_name (str): String containing the name of module that the check is being done for (eg. tempsenseInst_error)
    extension_file_path (str): Contains the extensions of the files which each generator produces for the flows
Returns: 
    1: if all checks are successful
Raises:
    ValueError: If any of the various checks go wrong (.csv file checks for temp-sense, flow generated files for all generators)
"""

import json
import os

def check_gen_files(json_filename, generator_is, cryo_library) -> int:
    with open(json_filename) as file:
        data = json.load(file)
    
    # print('Found .json config file...')

    module_name = data.get("module_name", "default")

    if generator_is['sky130XX_cryo']:
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
                    extension = extension.strip()
                    if (generator_is['sky130XX_cryo']) and (extension == ".spice" or extension == "_pex.spice" or extension.strip() == "_sim.spice"):
                        file = "./flow/" + module_name + extension.strip() 
                    else:
                        file = "".join([filename, extension])
                    if (os.path.exists(file) == 0):
                        raise ValueError(file + " does not exist!")
        else: 
            print("checking flow results with possibly stale list of extensions...")
            extensions = [".sdc", ".gds", ".def", ".spice", ".v", "_pex.spice"]
            for extension in extensions:
                    extension = extension.strip()
                    if (generator_is['sky130XX_cryo']) and (extension == ".spice" or extension == "_pex.spice"):
                        file = "./flow/" + module_name + extension 
                    else:
                        file = "".join([filename, extension])
                    
                    if (os.path.exists(file) == 0):
                        raise ValueError(file + " does not exist!")
    # print("Found necessary work result files!")
    if generator_is['sky130hd_temp']:
        for file in ("error_within_x.csv", "golden_error_opt.csv", "search_result.csv"):
            if os.path.exists(file) == 0:
                raise ValueError(file + " does not exist!")
    
    #print("Found generated .csv files!")
    return 1
