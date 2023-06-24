from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.geometry import boolean
from gdsfactory.typings import LayerSpec
from gdsfactory.components.rectangle import rectangle


@cell
def rectangular_ring(
    enclosed_size=(4.0, 2.0),
    width: float = 0.5,
    layer: LayerSpec = "WG",
    centered: bool = False,
) -> Component:
    """Returns a Rectangular Ring

    Args:
            enclosed_size = (width,hieght) of the enclosed area.
            width = width of the ring.
            layer = Specific layer to put polygon geometry on.
            centered: True sets center to (0,0), False sets south-west to (0,0).
    """
    c = Component()
    c_temp = Component("temp create ring")
    rect_in = c_temp << rectangle(size=enclosed_size, centered=centered, layer=layer)
    rect_out = c_temp << rectangle(
        size=[dim + 2 * width for dim in enclosed_size], centered=centered, layer=layer
    )
    if not centered:
        rect_in.move((width, width))
    c << boolean(A=rect_out, B=rect_in, operation="A-B", layer=layer)
    return c


if __name__ == "__main__":
    c = rectangular_ring(centered=True)
    c.show()
