from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle

# from PDK.mappedpdk import MappedPDK


@cell
def via_stack(pdk, glayer1: str, glayer2: str) -> Component:
    """produces a single via stack between two metal layers
    does not produce via arrays
    args:
    pdk: MappedPDK is the pdk to use
    glayer1: str is the glayer to start on
    glayer2: str is the glayer to end on
    ****NOTE it does not matter what order you pass layers
    ****NOTE will not lay poly or active but will lay metals
    """
    pdk.activate()
    viastack = Component()
    # check that the generic layers specfied can be routed between
    for layer in [glayer1, glayer2]:
        if not pdk.is_routable_glayer(layer):
            raise ValueError("via_stack: specify between two routable layers")
    # correctly order layers (level1 should be lower than level2)
    level1 = int(glayer1[-1]) if "met" in glayer1 else 0
    level2 = int(glayer2[-1]) if "met" in glayer2 else 0
    if level1 > level2:
        level1, level2 = level2, level1
    # if same level return empty component
    if level1 == level2:
        return viastack
    # lay mcon if first layer is active or poly
    if not level1:
        pdk.has_required_glayers(["mcon", "met1"])
        mcondim = pdk.get_grule("mcon")["width"]
        viastack << rectangle(
            size=(mcondim, mcondim), layer=pdk.get_glayer("mcon"), centered=True
        )
        metdim = max(
            2 * pdk.get_grule("met1", "mcon")["min_enclosure"] + mcondim,
            pdk.get_grule("met1")["min_width"],
        )
        viastack << rectangle(
            size=(metdim, metdim), layer=pdk.get_glayer("met1"), centered=True
        )
        # add one to level1 (make it a metal) so we can use the code below
        level1 += 1
        # check if layers are now same
        if level1 == level2:
            return viastack.flatten()
    # construct metal stack if both are metals
    if level1 and level2:
        for level in range(level1, level2):
            gmetlayer = "met" + str(level)
            gnextvia = "via" + str(level)
            pdk.has_required_glayers([gmetlayer, gnextvia])
            metdim = max(
                2 * pdk.get_grule(gmetlayer, gnextvia)["min_enclosure"]
                + pdk.get_grule(gnextvia)["width"],
                pdk.get_grule(gmetlayer)["min_width"],
            )
            viastack << rectangle(
                size=(metdim, metdim), layer=pdk.get_glayer(gmetlayer), centered=True
            )
            viadim = pdk.get_grule(gnextvia)["width"]
            viastack << rectangle(
                size=(viadim, viadim), layer=pdk.get_glayer(gnextvia), centered=True
            )
        gfinalmet = "met" + str(level2)
        gprevvia = "via" + str(level)
        metdim = max(
            2 * pdk.get_grule(gfinalmet, gprevvia)["min_enclosure"]
            + pdk.get_grule(gprevvia)["width"],
            pdk.get_grule(gfinalmet)["min_width"],
        )
        viastack << rectangle(
            size=(metdim, metdim), layer=pdk.get_glayer(gfinalmet), centered=True
        )
    return viastack.flatten()


if __name__ == "__main__":
    from PDK.gf180_mapped import gf180_mapped_pdk

    gf180_mapped_pdk.activate()
    via_stack(gf180_mapped_pdk, "active_diff", "met1").show()
