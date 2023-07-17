from opamp import opamp
from gdsfactory.read.import_gds import import_gds
from PDK.util.custom_comp_utils import prec_array, add_ports_perimeter, movey, print_ports, align_comp_to_port
from gdsfactory.component import Component
from gdsfactory.cell import cell
from PDK.mappedpdk import MappedPDK
from opamp import opamp
from L_route import L_route
from via_gen import via_array


@cell
def sky130_opamp_add_pads(sky130pdk: MappedPDK, opamp_in: Component) -> Component:
	"""adds the MPW-5 pads to opamp.
	Also adds text labels and pin layers so that extraction is nice
	"""
	# error checking and setup
	if sky130pdk.name != "sky130":
		raise ValueError("This function is only for sky130 pdk")
	opamp_wpads = opamp_in.copy()
	opamp_wpads = movey(opamp_wpads, destination=0)
	# create pad array and add to opamp
	pad = import_gds("sky130_mpw5_pad.gds")
	pad.name = "mpw5pad"
	pad = add_ports_perimeter(pad, pdk.get_glayer("met4"),prefix="pad_")
	pad_array = prec_array(pad, rows=2, columns=4, spacing=(40,120))
	pad_array_ref = pad_array.ref_center()
	opamp_wpads.add(pad_array_ref)
	# add via_array to vdd pin
	vddarray = via_array(pdk, "met4","met5",size=(opamp_wpads.ports["vdd_pin_N"].width,opamp_wpads.ports["vdd_pin_E"].width))
	via_array_ref = opamp_wpads << vddarray
	align_comp_to_port(via_array_ref,opamp_wpads.ports["vdd_pin_N"],alignment=('c','b'))
	# route to the pads
	opamp_wpads << L_route(pdk, opamp_wpads.ports["minus_pin_W"],pad_array_ref.ports["row1_col0_pad_S"],hwidth=3)
	opamp_wpads << L_route(pdk, opamp_wpads.ports["plus_pin_W"],pad_array_ref.ports["row0_col0_pad_N"],hwidth=3)
	opamp_wpads << L_route(pdk, opamp_wpads.ports["vbias2_pin_E"],pad_array_ref.ports["row0_col1_pad_N"],hwidth=3)
	opamp_wpads << L_route(pdk, opamp_wpads.ports["vbias1_pin_E"],pad_array_ref.ports["row0_col2_pad_N"],hwidth=3)
	opamp_wpads << L_route(pdk, opamp_wpads.ports["gnd_pin_top_met_E"],pad_array_ref.ports["row1_col3_pad_S"],hwidth=3,vglayer="met5")
	opamp_wpads << L_route(pdk, opamp_wpads.ports["vdd_pin_N"],pad_array_ref.ports["row1_col1_pad_E"],vwidth=4,vglayer="met5")
	opamp_wpads << L_route(pdk, opamp_wpads.ports["output_pin_E"],pad_array_ref.ports["row0_col3_pad_N"],hwidth=3,vglayer="met5")
	return opamp_wpads

if __name__ == "__main__":
	from PDK.util.standard_main import pdk
	
	opamp_in = opamp(pdk)
	opamp_out = sky130_opamp_add_pads(pdk, opamp_in)
	opamp_out.show()
