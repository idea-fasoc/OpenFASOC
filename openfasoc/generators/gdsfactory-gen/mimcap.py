from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
from PDK.mappedpdk import MappedPDK
from typing import Optional


@cell
def mimcap(
    pdk: MappedPDK, size=(5.0, 5.0), routing: Optional[bool] = False
) -> Component:
    """create a mimcap
    args:
    pdk=pdk to use
    size=tuple(float,float) size of cap
    ****Note: size is the size of the capmet layer
    """
    pdk.has_required_glayers(["capmet", "capbottommet", "captopmet", "capvia"])
    pdk.activate()
    mim_cap = Component()
    mim_cap << rectangle(size=size, layer=pdk.get_glayer("capmet"), centered=True)
    # TODO: implement
    return mim_cap.flatten()
