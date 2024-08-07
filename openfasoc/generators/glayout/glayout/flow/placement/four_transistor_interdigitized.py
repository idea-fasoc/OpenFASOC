# 4 transistor placed in two rows (each row is an interdigitized pair of transistors)
# the 4 transistors are labeled top or bottom and transistor A or B
# top_A_, bottom_A, top_B_, bottom_B_

from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.placement.two_transistor_interdigitized import two_nfet_interdigitized, two_pfet_interdigitized
from typing import Literal, Optional
from gdsfactory import Component
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, movey
from glayout.flow.primitives.guardring import tapring

def generic_4T_interdigitzed(
    pdk: MappedPDK,
    top_row_device: Literal["nfet", "pfet"],
    bottom_row_device: Literal["nfet", "pfet"],
    numcols: int,
    length: float=None,
    with_substrate_tap: bool = True,
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
        toprow = toplvl << two_nfet_interdigitized(pdk,numcols,with_substrate_tap=False,length=length,**top_kwargs)
    else:
        toprow = toplvl << two_pfet_interdigitized(pdk,numcols,with_substrate_tap=False,length=length,**top_kwargs)
    if bottom_row_device=="nfet":
        bottomrow = toplvl << two_nfet_interdigitized(pdk,numcols,with_substrate_tap=False,length=length,**bottom_kwargs)
    else:
        bottomrow = toplvl << two_pfet_interdigitized(pdk,numcols,with_substrate_tap=False,length=length,**bottom_kwargs)
    # move
    toprow.movey(pdk.snap_to_2xgrid((evaluate_bbox(bottomrow)[1]/2 + evaluate_bbox(toprow)[1]/2 + pdk.util_max_metal_seperation())))
    # add substrate tap
    if with_substrate_tap:
        substrate_tap = tapring(pdk, enclosed_rectangle=pdk.snap_to_2xgrid(evaluate_bbox(toplvl.flatten(),padding=pdk.util_max_metal_seperation())))
        substrate_tap_ref = toplvl << movey(substrate_tap,destination=pdk.snap_to_2xgrid(toplvl.flatten().center[1],snap4=True))
    # add ports
    toplvl.add_ports(substrate_tap_ref.get_ports_list(),prefix="substratetap_")
    toplvl.add_ports(toprow.get_ports_list(),prefix="top_")
    toplvl.add_ports(bottomrow.get_ports_list(),prefix="bottom_")
    # flag for smart route
    toplvl.info["route_genid"] = "four_transistor_interdigitized"
    return toplvl
