# Utilities included in this python file can be used to 
# 1- verify the test_cases
# 2- augment test_cases to synthetically increase the number of data points


import os
import traceback
from pathlib import Path
from typing import Union

from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk
import glayout.syntaxer.dynamic_load


def instantiate_convo(pdk: MappedPDK, convo_file: Union[str, Path]) -> bool:
    """Instantiates a layout for the given conversation file
    
    Args:
        convo_file (str or Path): path to Glayout .convo file

    Returns:
        bool: True if the cell was instantiated
    """
    try:
        # convert NLP to code and pass to show_glayout_code_cell
        session_code = glayout.syntaxer.dynamic_load.run_session(load_conversation=convo_file, restore_and_exit=True)
        comp = glayout.syntaxer.dynamic_load.run_glayout_code_cell(pdk, session_code)
        comp.show()
        # pdk.magic_drc(comp)
        # pdk.lvs_netgen(comp)
        return True
    except Exception as e:
        print(f"Error running session with {convo_file}: {e}")
        print(traceback.format_exc())
    return False


def run_all_tests(test_cases_dir: Union[str, Path] = "./syntax_data/convos"):
    """Run all test cases found in the 'test_cases' directory."""
    # Directory containing test cases
    test_cases_dir = str(Path(test_cases_dir).resolve())
    # Get all files in the directory that end with ".convo"
    convo_files = [f for f in os.listdir(test_cases_dir) if f.endswith(".convo")]
    # run and verify all convos
    for convo_file in convo_files:
        convo_file_path = os.path.join(test_cases_dir, convo_file)
        print(f"Running session with {convo_file_path}")
        instantiate_convo(pdk=sky130_mapped_pdk, convo_file=convo_file_path)


if __name__ == "__main__":
    run_all_tests()

