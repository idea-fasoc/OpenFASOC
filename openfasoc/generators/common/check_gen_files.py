import json
import os

def check_gen_files():
    with open('test.json', 'r') as file:
        data = json.load(file)
    
    # print('Found .json config file...')

    module_name = data.get("module_name", "default")

    work_dir = "./work/"

    if (os.path.exists(work_dir) == 0):
        raise ValueError("work directory does not exist!")
    else:
        filename = work_dir + module_name
        for file in (filename + ".gds", filename + ".spice", filename + ".v", filename + ".def", filename + "_pex.spice", filename + ".sdc"):
            if (os.path.exists(file) == 0):
                raise ValueError(file + " does not exist!")

    # print("Found necessary work result files!")

    for file in ("error_within_x.csv", "golden_error_opt.csv", "search_result.csv"):
        if os.path.exists(file) == 0:
            raise ValueError(file + " does not exist!")
    
    #print("Found generated .csv files!")
    return 1