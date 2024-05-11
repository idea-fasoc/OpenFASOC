# this file contains functions which dynamically create and import cells
import importlib.util
import inspect
import os
import re

from glayout.pdk.mappedpdk import MappedPDK


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


#def get_glayout


def run_glayout_code_cell(pdk: MappedPDK, glayout_code: str) -> bool:
    """Instantiates a layout form the given glayout cell
    
    Args:
        glayout_code (str): string containg the cell function and all needed imports

    Returns:
        bool: True if the cell was instantiated
    """
    # modify the code to rename the cell function to "testcell"
    pattern = r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)cell\s*\("
    glayout_code = re.sub(pattern,"def testcell(",glayout_code)
    # write the code to a file called "testcell.py"
    with open("testcell.py",mode="w") as testfile:
        testfile.write(glayout_code)
    # import testcell
    spec = importlib.util.spec_from_file_location("testcell", "testcell.py")
    temp_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(temp_module)
    # execute the code with some arguments to create and show the layout
    temp_module.testcell(**get_default_arguments(temp_module.testcell, pdk)).show()
    # delete testcell.py
    if os.path.exists("testcell.py"):
        os.remove("testcell.py")
    # if we got this far the cell is clean, so return True
    return True
