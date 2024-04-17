import os
import sys
import subprocess

# Directory paths from the Makefile segment

os.environ["WORK_HOME"] = "./"
os.environ["FLOW_HOME"] = "./"
os.environ["COMMON_HOME"] = os.path.join(os.getenv("WORK_HOME"), "../../../common")
DESIGN_NAME = sys.argv[1]
PLATFORM = sys.argv[2]
os.environ["PLATFORM"] = "sky130hd"
os.environ["DESIGN_NAME"] = DESIGN_NAME
os.environ["FLOW_VARIANT"] = "tempsense"
RESULTS_DIR = os.path.join(os.getenv("WORK_HOME"), "results", PLATFORM, os.getenv("FLOW_VARIANT"))
OBJECTS_DIR = os.path.join(os.getenv("WORK_HOME"), "objects", PLATFORM, os.getenv("FLOW_VARIANT"))
PLATFORM_DIR = os.path.join(os.getenv("COMMON_HOME"), "platforms", PLATFORM)
UTILS_DIR = os.path.join(os.getenv("FLOW_HOME"), "util")
COMMON_VERIF_DIR = os.path.join(os.getenv("COMMON_HOME"), "drc-lvs-check")
# COMMON_HOME = "{WORK_HOME}/../../../common"
# PLATFORM_DIR = "{COMMON_HOME}/{PLATFORM}"
# RESULTS_DIR = "{WORK_HOME}/results/{PLATFORM}/{DESIGN_NICKNAME}/{FLOW_VARIANT}"
# OBJECTS_DIR = "{WORK_HOME}/objects/{PLATFORM}/{DESIGN_NICKNAME}/{FLOW_VARIANT}"
# PLATFORM_DIR = "{PLATFORM_DIR}"
# UTILS_DIR = "{FLOW_HOME}/util"
# COMMON_VERIF_DIR = "{COMMON_HOME}/drc-lvs-check"

# Take DESIGN_NAME and PLATFORM from command-line arguments
if len(sys.argv) < 3:
    print("Usage: python script.py DESIGN_NAME PLATFORM")
    sys.exit(1)



# Define the netgen_lvs target
def netgen_lvs():
    # Check if necessary commands are available
    # if not os.path.exists("netgen"):
    #     raise FileNotFoundError("Netgen not found in PATH")
    # if not os.path.exists("magic"):
    #     raise FileNotFoundError("Magic not found in PATH")

    # Create necessary directories
    os.makedirs(os.path.join(OBJECTS_DIR, "netgen_lvs", "spice"), exist_ok=True)
    os.makedirs(os.path.join(OBJECTS_DIR, "netgen_lvs", "ext"), exist_ok=True)

    # Parse CDL file and generate spice file
    cdl_file = os.path.join(RESULTS_DIR, "6_final.cdl")
    spice_template = os.path.join(PLATFORM_DIR, "cdl", "sky130_fd_sc_hd.spice")
    spice_output = os.path.join(OBJECTS_DIR, "netgen_lvs", "spice", f"{DESIGN_NAME}.spice")
    subprocess.run(["python3", os.path.join(UTILS_DIR, "openfasoc", "cdl_parser.py"), "-i", cdl_file, "-s", spice_template, "-o", spice_output], check=True)

    # Run LVS with Netgen
    gds_file = os.path.join(RESULTS_DIR, "6_final.gds")
    subprocess.run([os.path.join(COMMON_VERIF_DIR, "run_lvspex.sh"), gds_file, DESIGN_NAME, os.path.join(RESULTS_DIR, "6_final_lvs.rpt")], check=True)

# Execute the netgen_lvs target
netgen_lvs()
