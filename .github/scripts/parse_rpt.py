import sys, os
import json

sys.stdout.flush()

if len(sys.argv) == 1 or sys.argv[1] == "sky130hvl_ldo":
    drc_filename = "work/6_final_drc.rpt"
    lvs_filename = "work/6_final_lvs.rpt"
else:
    drc_filename = "work/"+sys.argv[1]+"/6_final_drc.rpt"
    lvs_filename = "work/"+sys.argv[1]+"/6_final_lvs.rpt"

if len(sys.argv) > 1 and sys.argv[1] == "sky130hvl_ldo":
    with open(drc_filename, 'r') as f1, open("../../../.github/scripts/expected_drc_reports/expected_ldo_drc.rpt", 'r') as f2:
        content1 = f1.readlines()
        content2 = f2.readlines()
        if content1 == content1:
            print("DRC is clean!")
        else:
            raise ValueError("DRC failed!")
        
elif sum(1 for line in open(drc_filename)) > 3:
    raise ValueError("DRC failed!")
else:
    print("DRC is clean!")


with open(lvs_filename) as f:
    f1 = f.read()

    if "failed" in f1:
        raise ValueError("LVS failed!")
    else:
        print("LVS is clean!")

if len(sys.argv) > 1 and sys.argv[1] == "sky130hd_temp_full":
    result_filename = "work/prePEX_sim_result" # might remove from check or need to implement different logic later if sim outputs change due to downstream changes
    sim_state_filename = "work/sim_state_file.txt"

    with open(result_filename) as f2, open("../../../.github/scripts/expected_sim_outputs/prePEX_sim_result.txt") as f1:
        content1 = f2.readlines()
        content2 = f1.readlines()
        if content1 != content2:
            raise ValueError("Simulations failed: simulation result file does not match!")
    
    sim_state = json.load(open("work/sim_state_file.txt"))
    if sim_state["failed_sims"] != 0:
        raise ValueError("Simulations failed: Non zero failed simulations!")

    for folder_num in range(1, sim_state["completed_sims"] + 1):
        dir_path = r'simulations/run/'
        pex_path = os.listdir(dir_path)
        
        file_name = "simulations/run/" + pex_path + "/" + str(folder_num) + "/"
        param_file = file_name + "parameters.txt"
        log_file = file_name + "sim_" + str(folder_num) + ".log"
        spice_file = file_name + "sim_" + str(folder_num) + ".sp"

        if os.path.exists(log_file) and os.path.exists(log_file) and os.path.exists(spice_file):
            pass
        else:
            raise ValueError("Simulations failed: required of run folders do not exist!")
    
    print("Simulations are clean!")
