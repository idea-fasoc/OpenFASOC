from gdsfactory.read.import_gds import import_gds
from gdsfactory.components import text_freetype, rectangle
from glayout.flow.pdk.util.comp_utils import prec_array, movey, align_comp_to_port, prec_ref_center
from glayout.flow.pdk.util.port_utils import add_ports_perimeter, print_ports
from gdsfactory.component import Component
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.blocks.composite.opamp.opamp import opamp
from glayout.flow.routing.L_route import L_route
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.primitives.via_gen import via_array
from gdsfactory.cell import cell, clear_cache
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as pdk
from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid
from glayout.flow.pdk.util.component_array_create import write_component_matrix
from evaluator_wrapper import run_evaluation
def sky130_add_opamp_2_labels(opamp_in: Component) -> Component:
	"""adds opamp labels for extraction, without adding pads
	this function does not need to be used with sky130_add_opamp_pads
	"""
	opamp_in.unlock()
	# define layers
	met2_pin = (69,16)
	met2_label = (69,5)
	met3_pin = (70,16)
	met3_label = (70,5)
	met4_pin = (71,16)
	met4_label = (71,5)
	# list that will contain all port/comp info
	move_info = list()
	# create labels and append to info list
	# gnd
	gndlabel = rectangle(layer=met3_pin,size=(1,1),centered=True).copy()
	gndlabel.add_label(text="GND",layer=met3_label)
	move_info.append((gndlabel,opamp_in.ports["pin_gnd_N"],None))
	#diffpairibias
	ibias1label = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
	ibias1label.add_label(text="DIFFPAIR_BIAS",layer=met2_label)
	move_info.append((ibias1label,opamp_in.ports["pin_diffpairibias_N"],None))
	# commonsourceibias
	ibias2label = rectangle(layer=met4_pin,size=(1,1),centered=True).copy()
	ibias2label.add_label(text="CS_BIAS",layer=met4_label)
	move_info.append((ibias2label,opamp_in.ports["pin_commonsourceibias_N"],None))
	#minus
	minuslabel = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
	minuslabel.add_label(text="VP",layer=met2_label)
	move_info.append((minuslabel,opamp_in.ports["pin_minus_N"],None))
	#-plus
	pluslabel = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
	pluslabel.add_label(text="VN",layer=met2_label)
	move_info.append((pluslabel,opamp_in.ports["pin_plus_N"],None))
	#vdd
	vddlabel = rectangle(layer=met3_pin,size=(1,1),centered=True).copy()
	vddlabel.add_label(text="VDD",layer=met3_label)
	move_info.append((vddlabel,opamp_in.ports["pin_vdd_N"],None))
	# output (2nd stage)
	outputlabel = rectangle(layer=met4_pin,size=(0.2,0.2),centered=True).copy()
	outputlabel.add_label(text="VOUT",layer=met4_label)
	move_info.append((outputlabel,opamp_in.ports["commonsource_output_E"],('l','c')))
	# move everything to position
	for comp, prt, alignment in move_info:
		alignment = ('c','b') if alignment is None else alignment
		compref = align_comp_to_port(comp, prt, alignment=alignment)
		opamp_in.add(compref)
	return opamp_in.flatten()

def sky130_add_opamp_3_labels(opamp_in: Component) -> Component:
	"""adds opamp labels for extraction, without adding pads
	this function does not need to be used with sky130_add_opamp_pads
	"""
	opamp_in.unlock()
	# define layers
	met2_pin = (69,16)
	met2_label = (69,5)
	met3_pin = (70,16)
	met3_label = (70,5)
	met4_pin = (71,16)
	met4_label = (71,5)
	# list that will contain all port/comp info
	move_info = list()
	# create labels and append to info list
	# gnd
	gndlabel = rectangle(layer=met3_pin,size=(1,1),centered=True).copy()
	gndlabel.add_label(text="gnd",layer=met3_label)
	move_info.append((gndlabel,opamp_in.ports["pin_gnd_N"],None))
	#diffpairibias
	ibias1label = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
	ibias1label.add_label(text="diffpairibias",layer=met2_label)
	move_info.append((ibias1label,opamp_in.ports["pin_diffpairibias_N"],None))
	#outputibias
	ibias3label = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
	ibias3label.add_label(text="outputibias",layer=met2_label)
	move_info.append((ibias3label,opamp_in.ports["pin_outputibias_N"],None))
	# commonsourceibias
	ibias2label = rectangle(layer=met4_pin,size=(1,1),centered=True).copy()
	ibias2label.add_label(text="commonsourceibias",layer=met4_label)
	move_info.append((ibias2label,opamp_in.ports["pin_commonsourceibias_N"],None))
	#minus
	minuslabel = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
	minuslabel.add_label(text="minus",layer=met2_label)
	move_info.append((minuslabel,opamp_in.ports["pin_minus_N"],None))
	#-plus
	pluslabel = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
	pluslabel.add_label(text="plus",layer=met2_label)
	move_info.append((pluslabel,opamp_in.ports["pin_plus_N"],None))
	#vdd
	vddlabel = rectangle(layer=met3_pin,size=(1,1),centered=True).copy()
	vddlabel.add_label(text="vdd",layer=met3_label)
	move_info.append((vddlabel,opamp_in.ports["pin_vdd_N"],None))
	# output (3rd stage)
	outputlabel = rectangle(layer=met2_pin,size=(1,1),centered=True).copy()
	outputlabel.add_label(text="output",layer=met2_label)
	move_info.append((outputlabel,opamp_in.ports["pin_output_route_N"],None))
	# output (2nd stage)
	outputlabel = rectangle(layer=met4_pin,size=(0.2,0.2),centered=True).copy()
	outputlabel.add_label(text="CSoutput",layer=met4_label)
	move_info.append((outputlabel,opamp_in.ports["commonsource_output_E"],('l','c')))
	# move everything to position
	for comp, prt, alignment in move_info:
		alignment = ('c','b') if alignment is None else alignment
		compref = align_comp_to_port(comp, prt, alignment=alignment)
		opamp_in.add(compref)
	return opamp_in.flatten()

if __name__=="__main__":
    opamp_comp = sky130_add_opamp_2_labels(opamp(pdk, add_output_stage=False))
    #opamp_comp.show()
    opamp_comp.name = "opamp"
    #magic_drc_result = pdk.drc_magic(opamp_comp, opamp_comp.name)
    #netgen_lvs_result = pdk.lvs_netgen(opamp_comp, opamp_comp.name)
    opamp_gds = opamp_comp.write_gds("opamp.gds")
    res = run_evaluation("opamp.gds", opamp_comp.name, opamp_comp)
