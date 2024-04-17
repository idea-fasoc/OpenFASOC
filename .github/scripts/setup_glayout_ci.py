import os
import pathlib
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.github', 'scripts'))
from run_glayout_drc import run_drc_wrapper
from gdsfactory.component import Component
import argparse

from glayout.pdk.mappedpdk import MappedPDK
from glayout.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.pdk.gf180_mapped import gf180_mapped_pdk as gf180
import glayout.primitives.fet as fet
import glayout.primitives.guardring as guardring
import glayout.primitives.mimcap as mimcap
import glayout.primitives.via_gen as via
import glayout.placement.two_transistor_place as two_transistor_place
import glayout.components.diff_pair as diff_pair
import glayout.components.opamp as opamp

parser = argparse.ArgumentParser(description='Run DRC on components')
parser.add_argument('--pdk', required=True, type=str, help='PDK to be used (sky130, gf180)')
args = parser.parse_args(sys.argv[1:])
if (args.pdk == 'sky130'):
    pdk = sky130
elif (args.pdk == 'gf180'):
    pdk = gf180
else:
    print('Invalid PDK, continuing with sky130')
    pdk = sky130
    
##### SETUP #####

# get path of conda executable
conda_path = pathlib.Path(sys.executable).parent
CONDA_PATH = str(conda_path)
os.environ["CONDA_PATH"] = CONDA_PATH
COMMON_VERIF_DIR = '../../common/drc-lvs-check'
os.environ["COMMON_VERIF_DIR"] = COMMON_VERIF_DIR

# create results and reports directories
os.makedirs("../../../res/results", exist_ok=True)
os.makedirs("../../../res/reports", exist_ok=True)
results_dir = os.path.abspath("../../../res/results")
reports_dir = os.path.abspath("../../../res/reports")
os.environ["RESULTS_DIR"] = results_dir
os.environ["REPORTS_DIR"] = reports_dir


components = [
    ("nfet_test", fet.nmos),
    ("pfet_test", fet.pmos),
    ("tapring_test", guardring.tapring),
    ("mimcap_test", mimcap.mimcap),
    ("via_stack_test", via.via_stack, 'poly', 'met1'),
    ("via_array_test", via.via_array, 'poly', 'met1', (2.0, 2.5)),
    ("ttp_test", two_transistor_place.two_transistor_place, 'aba bab aba', (fet.nmos, {"pdk": pdk}), (fet.nmos, {"pdk": pdk})),
    ("diff_pair_test", diff_pair.diff_pair),
    ("opamp_test", opamp.opamp)
]

run_drc_wrapper(pdk, components)

sys.exit(0)
