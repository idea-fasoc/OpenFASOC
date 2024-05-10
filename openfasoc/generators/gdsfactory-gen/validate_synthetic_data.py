# Utilities included in this python file can be used to 
# 1- verify the test_cases
# 2- augment test_cases to synthetically increase the number of data points

import os
from pathlib import Path
from typing import Union
from run import run_session
from glayout.pdk.mappedpdk import MappedPDK
from glayout.pdk.sky130_mapped import sky130_mapped_pdk
import re
import inspect
import traceback
import importlib.util
import os

def get_default_arguments(func, pdk: MappedPDK) -> dict:
    """Gets default arguments to a function based on its argument types.

    Args:
        func (callable): The function to which default arguments will be added.
        pdk (MappedPDK): If one of the non default args is of type MappedPDK, then this pdk is used for default value

    Returns:
        dict: A dictionary containing default arguments with values based on the argument types of the input function.
    """
    # get args that dont have a default
    argspec = inspect.getfullargspec(func)
    args_with_defaults = argspec.defaults or []
    num_args_without_defaults = len(argspec.args) - len(args_with_defaults)
    args_without_defaults = argspec.args[:num_args_without_defaults]
    # loop through non default args and try to set some value for them
    kwargs = {}
    for arg, arg_type in zip(args_without_defaults, argspec.annotations.values()):
        # pick some default value
        if arg_type == int:
            default_value = 2
        elif arg_type == float:
            default_value = 2.5
        elif arg_type == bool:
            default_value = True
        elif arg_type == str:
            default_value = "met1"
        elif arg_type == MappedPDK:
            default_value = pdk
        else:# for other types, set default to None
            default_value = None
        # add this argument to the kwargs
        kwargs[arg] = default_value
    return kwargs


def instantiate_convo(pdk: MappedPDK, convo_file: Union[str, Path]) -> bool:
    """Instantiates a layout for the given conversation file
    
    Args:
        convo_file (str or Path): path to Glayout .convo file

    Returns:
        bool: True if the cell was instantiated
    """
    try:
        # convert NLP to code
        session_code = run_session(load_conversation=convo_file, restore_and_exit=True)
        # modify the code to rename the cell function to "testcell"
        pattern = r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)cell\s*\("
        session_code = re.sub(pattern,"def testcell(",session_code)
        # write the code to a file called "testcell.py"
        with open("testcell.py",mode="w") as testfile:
            testfile.write(session_code)
        # import testcell
        spec = importlib.util.spec_from_file_location("testcell", "testcell.py")
        temp_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(temp_module)
        # execute the code with some arguments to create and show the layout
        temp_module.testcell(**get_default_arguments(temp_module.testcell, pdk)).show()
        # delete testcell.py
        if os.path.exists("testcell.py"):
            os.remove("testcell.py")
        # if we got this far testcase is clean, so return True
        return True
    except Exception as e:
        print(f"Error running session with {convo_file}: {e}")
        print(traceback.format_exc())
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
        print(f"Running session with {convo_file_path}")
        instantiate_convo(pdk=sky130_mapped_pdk, convo_file=convo_file_path)


if __name__ == "__main__":
    run_all_tests()

