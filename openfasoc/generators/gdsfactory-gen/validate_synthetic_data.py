# Utilities included in this python file can be used to 
# 1- verify the test_cases
# 2- augment test_cases to synthetically increase the number of data points

import os
from pathlib import Path
from typing import Union
from run import run_session


def verify_glayout_cell(code: str) -> bool:
    """runs the glayout cell provided with default args

    Args:
        code (str): Glayout python code (cell function only)

    Returns:
        bool: True if the cell is a valid testcase
    """
    # TODO: finish implementing
    return True

def run_with_convo(convo_file: Union[str, Path]) -> bool:
    """Run the run_session function with the given conversation file.
    
    Args:
        convo_file (str or Path): path to Glayout .convo file

    Returns:
        bool: True if the cell is a valid testcase
    """
    try:
        session_code = run_session(load_conversation=convo_file, restore_and_exit=True)
        return verify_glayout_cell(session_code)
        print(f"Session code for {convo_file}:\n{session_code}")
    except Exception as e:
        print(f"Error running session with {convo_file}: {e}")
    return False

def run_all_tests(test_cases_dir: Union[str, Path] = "test_cases"):
    """Run all test cases found in the 'test_cases' directory."""
    # Directory containing test cases
    test_cases_dir = str(Path(test_cases_dir).resolve())
    # Get all files in the directory that end with ".convo"
    convo_files = [f for f in os.listdir(test_cases_dir) if f.endswith(".convo")]
    # run and verify all convos
    for convo_file in convo_files:
        convo_file_path = os.path.join(test_cases_dir, convo_file)
        print(f"Running session with {convo_file_path}...")
        run_with_convo(convo_file_path)

if __name__ == "__main__":
    run_all_tests()

