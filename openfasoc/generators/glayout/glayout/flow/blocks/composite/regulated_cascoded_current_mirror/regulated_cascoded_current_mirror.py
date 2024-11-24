import sys
from os import path, rename, environ, listdir, remove
environ['OPENBLAS_NUM_THREADS'] = '1'
from pathlib import Path
# path to glayout
sys.path.append(path.join(str(Path(__file__).resolve().parents[2])))


from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.flow.pdk.gf180_mapped import gf180_mapped_pdk as gf180

from glayout.flow.primitives.guardring import tapring
from glayout.flow.routing.smart_route import smart_route
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route

from glayout.flow.placement.two_transistor_interdigitized import two_nfet_interdigitized, two_pfet_interdigitized

from glayout.flow.pdk.util.comp_utils import evaluate_bbox, prec_center, prec_array, movey, align_comp_to_port, prec_ref_center
prec_ref_center
from glayout.flow.pdk.util.port_utils import add_ports_perimeter	


from gdsfactory.components import text_freetype, rectangle
from gdsfactory import Component
from gdsfactory.routing.route_quad import route_quad
from glayout.flow.spice.netlist import Netlist
from typing import Optional, Union 

def delete_files_in_directory(directory_path):
   try:
     files = listdir(directory_path)
     for file in files:
       file_path = path.join(directory_path, file)
       if path.isfile(file_path):
         remove(file_path)
     print("All files deleted successfully.")
   except OSError:
     print("Error occurred while deleting files.")


global PDK_ROOT
if 'PDK_ROOT' in environ:
	PDK_ROOT = str(Path(environ['PDK_ROOT']).resolve())
else:
	PDK_ROOT = "/usr/bin/miniconda3/share/pdk/"
 
 
def generate_current_mirror_netlist(
    pdk: MappedPDK,
    instance_name: str,
    CM_size: tuple[float, float, int],  # (width, length, multipliers)
    drain_net_A: str,
    gate_net: str,
    source_net: str,
    drain_net_B: str,
    transistor_type: str = "nfet",
    bulk_net: str = None,
    proposed_ground: str = None,  # Proposed ground net
    dummy: bool = True,
    subckt_only: bool = False,
) -> Netlist:
    """Generate a netlist for a current mirror."""

    if bulk_net is None:
        bulk_net = "VDD" if transistor_type.lower() == "pfet" else "VSS"

    width = CM_size[0]
    length = CM_size[1]
    multipliers = CM_size[2]  
    mtop = multipliers if subckt_only else 1
    #mtop = multipliers * 2 if dummy else multipliers # Double the multiplier to account for the dummies


    model_name = pdk.models[transistor_type.lower()]

    circuit_name = instance_name
    nodes = [drain_net_A, drain_net_B, proposed_ground]

    source_netlist = f".subckt {circuit_name} {' '.join(nodes)}\n"

    #source_netlist += f"V{proposed_ground}1 ({proposed_ground} {bulk_net}) 0\n" #Proposed ground connection


    # Generating only two transistors (one on each side):
    source_netlist += f"XA {drain_net_A} {gate_net} {source_net} {bulk_net} {model_name} l={length} w={width} m={mtop}\n"
    source_netlist += f"XB {drain_net_B} {gate_net} {source_net} {bulk_net} {model_name} l={length} w={width} m={mtop}\n"
    source_netlist += f"XDUMMY {bulk_net} {bulk_net} {bulk_net} {bulk_net} {model_name} l={length} w={width} m={mtop}\n"
    source_netlist += ".ends " + circuit_name


    instance_format = "X{name} {nodes} {circuit_name} l={length} w={width} m={mult}"

    return Netlist(
        circuit_name=circuit_name,
        nodes=nodes,
        source_netlist=source_netlist,
        instance_format=instance_format,
        parameters={
            "model": model_name,
            "width": width,
            "length": length,
            'mult': multipliers,
        },
    )

def CurrentMirror(
    pdk: MappedPDK,
    CM_size: tuple[float, float, int], # (width, length, multipliers)
    type: Optional[str] = 'nfet',
    rmult: Optional[int] =1,
    with_substrate_tap: Optional[bool] = False,
    with_tie: Optional[bool] = True,
    with_dummy: Optional[bool] = True,
    tie_layers: tuple[str,str]=("met2","met1"),
    ) -> Component:
    """Create a current mirror """   
    
    CurrentMirror = Component(name="CurrentMirror")
    
    if type.lower() =="pfet" or type.lower() =="pmos":
        currm= two_pfet_interdigitized(pdk,numcols=CM_size[2],width=CM_size[0],length=CM_size[1],dummy=with_dummy,
                                       rmult=rmult,with_substrate_tap=with_substrate_tap,with_tie=with_tie,tie_layers=tie_layers)
    elif type.lower() =="nfet" or type.lower() =="nmos":
        currm= two_nfet_interdigitized(pdk,numcols=CM_size[2],width=CM_size[0],length=CM_size[1],dummy=with_dummy,
                                       rmult=rmult,with_substrate_tap=with_substrate_tap,with_tie=with_tie,tie_layers=tie_layers)
    else:
        raise ValueError("type must be either nfet or pfet")
        
    currm_ref = prec_ref_center(currm)
    CurrentMirror.add(currm_ref)
    CurrentMirror.add_ports(currm_ref.get_ports_list(),prefix="currm_")
    
    
    maxmet_sep = pdk.util_max_metal_seperation()
    
    gate_short = CurrentMirror << c_route(pdk,CurrentMirror.ports["currm_A_gate_W"],CurrentMirror.ports["currm_B_gate_W"],extension=3*maxmet_sep, viaoffset=False)
    
    CurrentMirror << L_route(pdk,CurrentMirror.ports["currm_A_drain_W"],gate_short.ports["con_S"],viaoffset=False, fullbottom=False)
    
    source_short = CurrentMirror << c_route(pdk,CurrentMirror.ports["currm_A_source_E"],CurrentMirror.ports["currm_B_source_E"], viaoffset=False)
    

     # add a pwell 
    CurrentMirror.add_padding(layers = (pdk.get_glayer("pwell"),), default = pdk.get_grule("pwell", "active_tap")["min_enclosure"], )
    CurrentMirror = add_ports_perimeter(CurrentMirror, layer = pdk.get_glayer("pwell"), prefix="well_")


    CurrentMirror.add_ports(srcshort.get_ports_list(), prefix="purposegndports")

    CurrentMirror.info["netlist"] = generate_current_mirror_netlist(
                                    pdk=pdk,
                                    instance_name=CurrentMirror.name,
                                    CM_size=CM_size,  # (width, length, multipliers)
                                    transistor_type=type,
                                    drain_net_A="VREF",  # Input drain connected to VREF (as seen in the layout)
                                    gate_net="VREF",      # Gate connected to VREF (as seen in the layout)
                                    source_net="VSS" if type=="nfet" else "VDD",    # Source connected to VSS
                                    drain_net_B="VCOPY", # Output drain connected to VCOPY
                                    dummy=True,          # Include dummy transistors (present in the layout)
                                    subckt_only=True,    # Generate only the subcircuit (no instances)
                                    proposed_ground= "VSS" if type=="nfet" else "VDD", #Proposed ground should also change

                                    )

    return CurrentMirror 

def sky130_add_current_mirror_labels(
    CMS: Component, 
    transistor_type: str = "nfet",
    pdk: MappedPDK =sky130) -> Component:  # Re-introduce transistor_type
    """Add labels to the current mirror layout for LVS, handling both nfet and pfet."""

    met2_pin = (69, 16)
    met2_label = (69, 5)
    met3_pin = (70, 16)
    met3_label = (70, 5)
    
    

    CMS.unlock()
    move_info = []

    # VREF label (for both gate and drain of transistor A, and dummy drains)
    vref_label = rectangle(layer=met2_pin, size=(0.5, 0.5), centered=True).copy()
    vref_label.add_label(text="VREF", layer=met2_label)
    
    move_info.append((vref_label, CMS.ports["currm_A_gate_E"], None))  # Gate of A
    move_info.append((vref_label, CMS.ports["currm_A_drain_E"], None)) # Drain of A


    # VCOPY label (for drain of transistor B)
    vcopy_label = rectangle(layer=met2_pin, size=(0.5, 0.5), centered=True).copy()
    vcopy_label.add_label(text="VCOPY", layer=met2_label)
    
    move_info.append((vcopy_label, CMS.ports["currm_B_drain_E"], None))  # Drain of B



   # VSS/VDD label (for sources/bulk connection)
    if transistor_type.lower() == "nfet":
        bulk_net_name = "VSS"
        bulk_pin_layer = met2_pin #met2 for nfet bulk
        bulk_label_layer = met2_label #met2 for nfet bulk
    else:  # pfet
        bulk_net_name = "VDD"
        bulk_pin_layer = met2_pin #met3 for pfet bulk
        bulk_label_layer = met2_label #met3 for pfet bulk
    
    bulk_label = rectangle(layer=bulk_pin_layer, size=(0.5, 0.5), centered=True).copy() #Layer changes based on type
    bulk_label.add_label(text=bulk_net_name, layer=bulk_label_layer)
    
    move_info.append((bulk_label, CMS.ports["currm_A_source_E"], None))  # Source of A
    move_info.append((bulk_label, CMS.ports["currm_B_source_E"], None))  # Source of B
    
    # VB label (connected to the dummy transistors' drains if present)
    if type == "nfet":
        vb_label = rectangle(layer=met2_pin, size=(0.5, 0.5), centered=True).copy() #met2 for nfet
        vb_label.add_label(text=bulk_net_name , layer=met2_label)
        
        move_info.append((vb_label, CMS.ports["purposegndportstop_met_N"], None)) 
        move_info.append((vb_label, CMS.ports["purposegndportstop_met_S"], None))
    else: #type is pfet
        vb_label = rectangle(layer=met2_pin, size=(0.5, 0.5), centered=True).copy() #met3 for pfet
        vb_label.add_label(text=bulk_net_name , layer=met2_label)
        
        move_info.append((vb_label, CMS.ports["purposegndportstop_met_N"], None)) 
        move_info.append((vb_label, CMS.ports["purposegndportstop_met_S"], None))



    # Add labels to the component
    for label, port, alignment in move_info:
        if port:
            alignment = ('c', 'c') if alignment is None else alignment
            aligned_label = align_comp_to_port(label, port, alignment=alignment)
            CMS.add(aligned_label)

    return CMS.flatten()


comp = CurrentMirror(sky130, (2, 1, 2), type='nfet', with_substrate_tap=False, with_tie=True)
comp = sky130_add_current_mirror_labels(comp, transistor_type='nfet', pdk=sky130)
comp.name = "CM"
comp.write_gds("GDS/CM.gds")
comp.show()
# for absc in comp.ports.keys():
#     if len(absc.split("_")) <=5:
#         print(absc)

print("\n...Generating Netlist...")
print(comp.info["netlist"].generate_netlist())
# %%
# print("\n...Running DRC...")
# drc_result = sky130.drc_magic(comp, "CM",output_file="DRC/")
# print(drc_result)
# %%
print("\n...Running LVS...")
netgen_lvs_result = sky130.lvs_netgen(comp, "CM",output_file_path="LVS")        
print(netgen_lvs_result)


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