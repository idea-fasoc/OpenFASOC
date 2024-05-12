# 4 transistor placed in two rows (each row is an interdigitized pair of transistors)
# the 4 transistors are labeled top or bottom and transistor A or B
# top_A_, bottom_A, top_B_, bottom_B_

from glayout.pdk.mappedpdk import MappedPDK
from glayout.placement.two_transistor_interdigitized import two_nfet_interdigitized, two_pfet_interdigitized
from typing import Literal, Optional
from gdsfactory import Component
from glayout.pdk.util.comp_utils import evaluate_bbox

def generic_4T_interdigitzed(
    pdk: MappedPDK,
    top_row_device: Literal["nfet", "pfet"],
    bottom_row_device: Literal["nfet", "pfet"],
    numcols: int,
    top_kwargs: Optional[dict]=None,
    bottom_kwargs: Optional[dict]=None
):
    if top_kwargs is None:
        top_kwargs = dict()
    if bottom_kwargs is None:
        bottom_kwargs = dict()
    # place
    toplvl = Component()
    if top_row_device=="nfet":
        toprow = toplvl << two_nfet_interdigitized(pdk,numcols,with_substrate_tap=False,**top_kwargs)
    else:
        toprow = toplvl << two_pfet_interdigitized(pdk,numcols,with_substrate_tap=False,**top_kwargs)
    if bottom_row_device=="nfet":
        bottomrow = toplvl << two_nfet_interdigitized(pdk,numcols,with_substrate_tap=False,**bottom_kwargs)
    else:
        bottomrow = toplvl << two_pfet_interdigitized(pdk,numcols,with_substrate_tap=False,**bottom_kwargs)
    # move
    toprow.movey(pdk.snap_to_2xgrid((evaluate_bbox(bottomrow)[1]/2 + evaluate_bbox(toprow)[1]/2 + pdk.util_max_metal_seperation())))
    # routes

    return toplvl