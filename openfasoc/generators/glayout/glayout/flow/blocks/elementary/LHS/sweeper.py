import os
import sys
import json
import time
import logging
import random
from concurrent.futures import ProcessPoolExecutor, as_completed

# Add the parent directories to the Python path
# current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up to the OpenFASOC generators directory 
# openfasoc_generators = os.path.join(current_dir, '..', '..', '..', '..', '..')
# sys.path.insert(0, openfasoc_generators)

# Use relative imports for local files
import sys
# sys.path.append('/home/arnavshukla/OpenFASOC/openfasoc/generators/glayout')

from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk

# Import evaluator_wrapper from its actual location
# sys.path.append(os.path.join(current_dir, '..', '..', 'evaluator_box'))
from evaluator_wrapper import run_evaluation

from elhs import all_samples

# Add the elementary blocks directory to the path
# elementary_blocks_dir = os.path.join(current_dir, '..')
# sys.path.append(elementary_blocks_dir)

# from fvf import flipped_voltage_follower
from fvf import flipped_voltage_follower
from transmission_gate import transmission_gate
from current_mirror import current_mirror
from diff_pair import diff_pair
from opamp import sky130_add_opamp_labels
from lvcm import add_lvcm_labels, low_voltage_cmirror

# Import the opamp function from the main glayout package
from glayout.flow.blocks.composite.opamp.opamp import opamp

print("Available PCells and sample counts:")
for pcell, samples in all_samples.items():
    print(f"  {pcell}: {len(samples)} samples")


# Ensure output directory
OUTPUT_DIR = "sweep_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="sweep.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# Map PCell keys to factory functions
PCELL_FUNCS = {
    'fvf': flipped_voltage_follower,
    'txgate': transmission_gate,
    'current_mirror': current_mirror,
    'diff_pair': diff_pair,
    'opamp': lambda pdk, **kwargs: sky130_add_opamp_labels(opamp(pdk, **kwargs)),
    'lvcm': lambda pdk, **kwargs: add_lvcm_labels(low_voltage_cmirror(pdk, **kwargs), pdk),
}

def run_task(pcell, idx, params, retry=1):
    """
    Worker function: instantiates, writes GDS, evaluates, logs, returns result dict.
    Retries up to `retry` times on failure.
    """
    comp_name = f"{pcell}_{idx}"
    for attempt in range(1, retry + 2):
        start = time.time()
        try:
            comp = PCELL_FUNCS[pcell](sky130_mapped_pdk, **params)
            comp.name = comp_name
            gds_path = os.path.join(OUTPUT_DIR, f"{comp_name}.gds")
            comp.write_gds(gds_path)
            report = run_evaluation(gds_path, comp_name, comp)
            duration = time.time() - start
            logging.info(f"SUCCESS {comp_name} (attempt {attempt}) in {duration:.1f}s")
            return {
                "pcell": pcell,
                "index": idx,
                "params": params,
                "report": report
            }
        except Exception as e:
            duration = time.time() - start
            logging.error(f"ERROR {comp_name} (attempt {attempt}) after {duration:.1f}s: {e}")
            if attempt <= retry:
                logging.info(f"Retrying {comp_name} (attempt {attempt + 1})")
                time.sleep(1)  # small delay before retry
            else:
                logging.error(f"FAILED {comp_name} after {retry + 1} attempts")
                # Return minimal failure record or re-raise
                return {
                    "pcell": pcell,
                    "index": idx,
                    "params": params,
                    "report": None,
                    "error": str(e)
                }

def main():
    # Flatten tasks
    tasks = []
    for pcell, samples in all_samples.items():
        for idx, params in enumerate(samples):
            tasks.append((pcell, idx, params))

    # Shuffle for load-balancing
    random.shuffle(tasks)

    results = []
    with ProcessPoolExecutor(max_workers=26) as executor:
        futures = {
            executor.submit(run_task, pcell, idx, params, retry=1): (pcell, idx)
            for pcell, idx, params in tasks
        }
        for fut in as_completed(futures):
            res = fut.result()
            results.append(res)

    # Save all results
    with open(os.path.join(OUTPUT_DIR, "sweep_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print(f"Sweep completed: {len(results)} total records.")

if __name__ == "__main__":
    # Seed for reproducibility of categorical random choices
    random.seed(0)
    main()
