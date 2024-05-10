from glayout.pdk.mappedpdk import MappedPDK
from gdsfactory import Component
from glayout.pdk.util.comp_utils import move
from glayout.pdk.util.port_utils import remove_ports_with_prefix
from glayout.primitives.fet import nmos
from glayout.primitives.fet import pmos
from glayout.primitives.guardring import tapring
from glayout.primitives.mimcap import mimcap
from glayout.primitives.mimcap import mimcap_array
from glayout.primitives.via_gen import via_stack
from glayout.primitives.via_gen import via_array
from glayout.components.diff_pair import diff_pair
from glayout.routing.L_route import L_route
from glayout.routing.c_route import c_route
from glayout.routing.straight_route import straight_route
from glayout.pdk.util.comp_utils import prec_ref_center
from glayout.pdk.util.comp_utils import evaluate_bbox
from glayout.pdk.sky130_mapped import sky130_mapped_pdk
def CascodeCommonGate_cell(
	pdk: MappedPDK,
	width_m1: float, 
	width_m2: float, 
):
	CascodeCommonGate = Component()
	max_metal_sep_ = pdk.util_max_metal_seperation()
	# placing m1 centered at the origin
	m1 = nmos(pdk,**{'width': width_m1},with_substrate_tap=False)
	m1_ref = prec_ref_center(m1)
	CascodeCommonGate.add(m1_ref)
	CascodeCommonGate.add_ports(m1_ref.get_ports_list(),prefix="m1_")
	# placing m2 centered at the origin
	m2 = nmos(pdk,**{'width': width_m2},with_substrate_tap=False)
	m2_ref = prec_ref_center(m2)
	CascodeCommonGate.add(m2_ref)
	CascodeCommonGate.add_ports(m2_ref.get_ports_list(),prefix="m2_")
	# move m2 above m1
	relativemovcorrection_0 = [0, 1*(max_metal_sep_ + evaluate_bbox(m1)[1]/2 + evaluate_bbox(m2)[1]/2)]
	move(m2_ref,destination=[dim+relativemovcorrection_0[idir] for idir,dim in enumerate(m1.center)])
	remove_ports_with_prefix(CascodeCommonGate,"m2_")
	CascodeCommonGate.add_ports(m2_ref.get_ports_list(),prefix="m2_")
	CascodeCommonGate << c_route(pdk,CascodeCommonGate.ports["m1_multiplier_0_source_W"],CascodeCommonGate.ports["m2_multiplier_0_drain_W"],**{})
	return CascodeCommonGate

CascodeCommonGate_cell(sky130_mapped_pdk, 3,3).show()