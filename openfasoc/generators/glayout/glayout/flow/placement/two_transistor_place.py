from glayout.flow.pdk.mappedpdk import MappedPDK
from pydantic import validate_arguments
from gdsfactory.component import Component
from typing import Callable
from glayout.flow.primitives.fet import nmos, pmos
from glayout.flow.pdk.util.comp_utils import evaluate_bbox

@validate_arguments
def two_transistor_place(pdk: MappedPDK, pattern: str, deviceA: tuple[Callable, dict], deviceB: tuple[Callable, dict]) -> Component:
    """Place two transitors according to the patter provided
    args:
    pdk = MappedPDK to use
    pattern = placement pattern. This string must contain only white space, the char a, the char b.
    **** any other chars result in error. White space indicates a new row in the place
    **** all rows must have same number of cols
    deviceA/deviceB = tuple(function to call, kwargs for function) kwargs must include pdk
    """
    toplvlcomp = Component("2tranplace")
    # create the transistors
    tranA = deviceA[0](**deviceA[1])
    tranA_dims = evaluate_bbox(tranA)
    tranB = deviceB[0](**deviceB[1])
    tranB_dims = evaluate_bbox(tranB)
    # parse pattern into a matrix
    pattern = pattern.lower().split()
    parsed_pattern = list()
    for i, row in enumerate(pattern):
        parsed_pattern.append(list())
        if i==0:
            num_cols = len(row)
        elif len(row)!=num_cols:
            raise ValueError("all rows should have same number of devices")
        for char in row:
            if char=="a":
                parsed_pattern[i].append(tranA)
            elif char=="b":
                parsed_pattern[i].append(tranB)
            else:
                raise ValueError("pattern should only contain a,b, or whitespace")
    # run place (center, then right, then left, ...)
    extra_sep = 2*pdk.util_max_metal_seperation()
    yspace = extra_sep + max(tranA_dims[1], tranB_dims[1])
    xspace = extra_sep + max(tranA_dims[0], tranB_dims[0])
    for i, row in enumerate(parsed_pattern):
        for j, tran in enumerate(row):
            tranref = toplvlcomp << tran
            ymov = i * yspace
            xmov = j * xspace * (-1**(j%2))
            tranref.movex(xmov).movey(ymov)
            toplvlcomp.add_ports(tranref.get_ports_list(), prefix=f"place{i}_{j}_")
    return toplvlcomp
