import sys
sys.path.append('../../elementary/current_mirror/')
sys.path.append('../../composite/')

from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.flow.pdk.gf180_mapped import gf180_mapped_pdk as gf180

from gdsfactory.cell import cell, clear_cache
from gdsfactory.component import Component, copy
from gdsfactory.component_reference import ComponentReference
from gdsfactory.components.rectangle import rectangle
from glayout.flow.pdk.mappedpdk import MappedPDK
from typing import Optional, Union

from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid
from pydantic import validate_arguments
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, prec_ref_center, movex, movey, to_decimal, to_float, move, align_comp_to_port, get_padding_points_cc
from glayout.flow.pdk.util.port_utils import rename_ports_by_orientation, rename_ports_by_list, add_ports_perimeter, print_ports, set_port_orientation, rename_component_ports


from current_mirror import current_mirror, current_mirror_netlist


def sky130_add_current_mirror_labels(CMS: Component, transistor_type: str = "nfet",pdk: MappedPDK =sky130) -> Component:  # Re-introduce transistor_type
	"""Add labels to the current mirror layout for LVS, handling both nfet and pfet."""

	met2_pin = (69, 16)
	met2_label = (69, 5)
	met3_pin = (70, 16)
	met3_label = (70, 5)



	CMS.unlock()
	move_info = []

	# VREF label (for both gate and drain of transistor A, and dummy drains)
	vref_label = rectangle(layer=met3_pin, size=(1, 1), centered=True).copy()
	vref_label.add_label(text="VREF", layer=met3_label)
	move_info.append((vref_label, CMS.ports["fet_A_gate_E"], None))  # Gate of A
	move_info.append((vref_label, CMS.ports["fet_A_drain_E"], None)) # Drain of A


	# VCOPY label (for drain of transistor B)
	vcopy_label = rectangle(layer=met3_pin, size=(1, 1), centered=True).copy()
	vcopy_label.add_label(text="VCOPY", layer=met3_label)
	move_info.append((vcopy_label, CMS.ports["fet_B_drain_E"], None))  # Drain of B



	# VSS/VDD label (for sources/bulk connection)
	if transistor_type.lower() == "nfet":
		bulk_net_name = "VSS"
		bulk_pin_layer = met2_pin #met2 for nfet bulk
		bulk_label_layer = met2_label #met2 for nfet bulk
	else:  # pfet
		bulk_net_name = "VDD"
		bulk_pin_layer = met3_pin #met3 for pfet bulk
		bulk_label_layer = met3_label #met3 for pfet bulk

	bulk_label = rectangle(layer=bulk_pin_layer, size=(1, 1), centered=True).copy() #Layer changes based on type
	bulk_label.add_label(text=bulk_net_name, layer=bulk_label_layer)
	move_info.append((bulk_label, CMS.ports["fet_A_source_E"], None))  # Source of A
	move_info.append((bulk_label, CMS.ports["fet_B_source_E"], None))  # Source of B

	# VB label (connected to the dummy transistors' drains if present)
	vb_label = rectangle(layer=met3_pin, size=(1, 1), centered=True).copy() #met3 for pfet
	vb_label.add_label(text="VB" , layer=met3_label)
	move_info.append((vb_label, CMS.ports["purposegndportscon_N"], None)) 
	move_info.append((vb_label, CMS.ports["purposegndportscon_S"], None))

	# Add labels to the component
	for label, port, alignment in move_info:
		if port:
			alignment = ('c', 'b') if alignment is None else alignment
			aligned_label = align_comp_to_port(label, port, alignment=alignment)
			CMS.add(aligned_label)

	return CMS.flatten()


comp = current_mirror(sky130, numcols=2, device='nfet')
comp.name = "CM"
comp.write_gds("CM.gds")

# for absc in comp.ports.keys():
#     if len(absc.split("_")) <=4:
#         print(absc)
#         print(comp.ports[absc])
print(comp.info["netlist"].generate_netlist())
comp.show()

# comp = sky130_add_current_mirror_labels(comp, transistor_type='nfet', pdk=sky130)

# print("\n...Running LVS...")

# sky130.lvs_netgen(comp, "CM")        




# extractbash_template=str()
# #import pdb; pdb.set_trace()
# with open(str(_TAPEOUT_AND_RL_DIR_PATH_)+"/extract.bash.template","r") as extraction_script:
#     extractbash_template = extraction_script.read()
#     extractbash_template = extractbash_template.replace("@@PDK_ROOT",PDK_ROOT).replace("@@@PAROPT","noparasitics" if noparasitics else "na")
# with open(str(tmpdirname)+"/extract.bash","w") as extraction_script:
#     extraction_script.write(extractbash_template)
# #copyfile("extract.bash",str(tmpdirname)+"/extract.bash")
# copyfile(str(_TAPEOUT_AND_RL_DIR_PATH_)+"/opamp_perf_eval.sp",str(tmpdirname)+"/opamp_perf_eval.sp")
# copytree(str(_TAPEOUT_AND_RL_DIR_PATH_)+"/sky130A",str(tmpdirname)+"/sky130A")
# # extract layout
# Popen(["bash","extract.bash", tmp_gds_path, opamp_v.name],cwd=tmpdirname).wait()
# print("Running simulation at temperature: " + str(temperature_info[0]) + "C")
# process_spice_testbench(str(tmpdirname)+"/opamp_perf_eval.sp",temperature_info=temperature_info)
# process_netlist_subckt(str(tmpdirname)+"/opamp"+str(index)+"_pex.spice", temperature_info[1], cload=cload, noparasitics=noparasitics)
# rename(str(tmpdirname)+"/opamp"+str(index)+"_pex.spice", str(tmpdirname)+"/opamp_pex.spice")
# # run sim and store result
# #import pdb;pdb.set_trace()
# Popen(["ngspice","-b","opamp_perf_eval.sp"],cwd=tmpdirname).wait()
# ac_file = str(tmpdirname)+"/result_ac.txt"
# power_file = str(tmpdirname)+"/result_power.txt"
# noise_file = str(tmpdirname)+"/result_noise.txt"
# result_dict = get_sim_results(ac_file, power_file, noise_file)
# result_dict["area"] = area
