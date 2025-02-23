import sys
from os import path, rename, environ , listdir, remove, chmod
# environ['OPENBLAS_NUM_THREADS'] = '1'
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

from glayout.flow.pdk.util.snap_to_grid import component_snap_to_grid
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, prec_center, prec_array, movey, align_comp_to_port, prec_ref_center
from glayout.flow.pdk.util.port_utils import rename_ports_by_orientation, rename_ports_by_list, add_ports_perimeter, print_ports, set_port_orientation, rename_component_ports

from gdsfactory.components import text_freetype, rectangle
from gdsfactory import Component
from gdsfactory.routing.route_quad import route_quad
from glayout.flow.spice.netlist import Netlist
from typing import Optional, Union 


global PDK_ROOT
if 'PDK_ROOT' in environ:
	PDK_ROOT = str(Path(environ['PDK_ROOT']).resolve())
else:
	PDK_ROOT = "/usr/bin/miniconda3/share/pdk/"
 
def generate_current_mirror_netlist(
    pdk: MappedPDK,
    instance_name: str,
    CM_size: tuple[float, float, int, int],  # (width, length, multipliers, fingers)
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
    fingers =  CM_size[3] # Number of fingers of the interdigitized fets


    model_name = pdk.models[transistor_type.lower()]

    circuit_name = instance_name
    nodes = [drain_net_A, drain_net_B, proposed_ground]

    source_netlist = f".subckt {circuit_name} {' '.join(nodes)}\n"

    #source_netlist += f"V{proposed_ground}1 ({proposed_ground} {bulk_net}) 0\n" #Proposed ground connection


    # Generating only two transistors (one on each side):
    source_netlist += f"XA {drain_net_A} {gate_net} {source_net} {bulk_net} {model_name} l={length} w={width} m={mtop} nf={fingers}\n"
    source_netlist += f"XB {drain_net_B} {gate_net} {source_net} {bulk_net} {model_name} l={length} w={width} m={mtop} nf={fingers}\n"
    if dummy:
        source_netlist += f"XDUMMY {bulk_net} {bulk_net} {bulk_net} {bulk_net} {model_name} l={length} w={width} m={mtop}\n"
    source_netlist += ".ends " + circuit_name


    instance_format = "X{name} {nodes} {circuit_name} l={length} w={width} m={mult} nf={fingers}"

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

# @validate_arguments
def cascode_current_mirror(
        pdk: MappedPDK,
        Width: float = 1,
        Length: Optional[float] = None,
        num_cols: int = 2,
        fingers: int = 1,
        type: Optional[str] = 'nfet',
        with_substrate_tap: Optional[bool] = False,
        with_tie: Optional[bool] = True,
        with_dummy: Optional[bool] = True,
        tie_layers: tuple[str,str]=("met2","met1"),
        **kwargs
    ) -> Component:
    
    """An instantiable current mirror that returns a Component object. 
    The current mirror could be a two transistor interdigitized structure with a shorted source and gate.
    It can be instantiated with either nmos or pmos devices. It can also be instantiated with a dummy device, a substrate tap, and a tie layer, and is centered at the origin.
    Transistor A acts as the reference and Transistor B acts as the mirror fet
    This current mirror is used to generate a exact copy of the reference current.
    [TODO] Needs to be checked for both pfet and nfet configurations.
    [TODO] It will be updated with multi-leg or stackked length parametrization in future.
    [TODO] There will also be a Regulated Cascoded block added to it. 

	Args:
		pdk (MappedPDK): the process design kit to use
        Width (float): width of the interdigitized fets (same for both reference and mirror)
        Length (float): length of the interdigitized fets (same for both reference and mirror) 
        As Default, Set to None to use the minimum length of the technology
		numcols (int): number of columns of the interdigitized fets
        fingers: Number of fingers of interdigitized fets (same for both reference and mirror)
		device (str): nfet or pfet (can only interdigitize one at a time with this option)
		with_dummy (bool): True places dummies on either side of the interdigitized fets
		with_substrate_tap (bool): boolean to decide whether to place a substrate tapring
		with_tie (bool): boolean to decide whether to place a tapring for tielayer
		tie_layers (tuple[str,str], optional): the layers to use for the tie. Defaults to ("met2","met1").
		**kwargs: The keyword arguments are passed to the two_nfet_interdigitized or two_pfet_interdigitized functions and need to be valid arguments that can be accepted by the multiplier 
	Returns:
		Component: a current mirror component object
	"""
    pdk.activate()
    # Create the current mirror component
    CurrentMirror = Component(name="CurrentMirror")
    
    # Create the interdigitized fets
    if type.lower() =="pfet" or type.lower() =="pmos":
        currm= two_pfet_interdigitized(pdk,numcols=num_cols,width=Width,length=Length,fingers=fingers,
                                       dummy=with_dummy,with_substrate_tap=with_substrate_tap,with_tie=with_tie,tie_layers=tie_layers)
    elif type.lower() =="nfet" or type.lower() =="nmos":
        currm= two_nfet_interdigitized(pdk,numcols=num_cols,width=Width,length=Length,fingers=fingers,dummy=with_dummy,
                                       with_substrate_tap=with_substrate_tap,with_tie=with_tie,tie_layers=tie_layers)
    else:
        raise ValueError("type must be either nfet or pfet")
        
    # Add the interdigitized fets to the current mirror top component
    currm_ref = prec_ref_center(currm)
    CurrentMirror.add(currm_ref)
    CurrentMirror.add_ports(currm_ref.get_ports_list(),prefix="currm_")

    maxmet_sep = pdk.util_max_metal_seperation()
    
    # Connecting the source and gate of the fets
    gate_short = CurrentMirror << c_route(pdk,CurrentMirror.ports["currm_A_gate_W"],CurrentMirror.ports["currm_B_gate_W"],extension=3*maxmet_sep)
    
    CurrentMirror << L_route(pdk,CurrentMirror.ports["currm_A_drain_W"],gate_short.ports["con_S"],fullbottom=True)
    
    source_short = CurrentMirror << c_route(pdk,CurrentMirror.ports["currm_A_source_E"],CurrentMirror.ports["currm_B_source_E"],fullbottom=True)
   
    if with_dummy:
        # Connecting dummies to the welltie
        try:
            CurrentMirror << straight_route(pdk, CurrentMirror.ports["A_0_dummy_L_gsdcon_top_met_W"],CurrentMirror.ports["welltie_W_top_met_W"],glayer2="met1")
        except KeyError:
            pass
        try:
            end_col = num_cols - 1
            port1 = f'B_{end_col}_dummy_R_gdscon_top_met_E'
            CurrentMirror << straight_route(pdk, CurrentMirror.ports[port1], CurrentMirror.ports["welltie_E_top_met_E"], glayer2="met1")
        except KeyError:
            pass
    

     # add well (probably unnecessary)
    if type.lower() == "nfet":
        # add a pwell 
        CurrentMirror.add_padding(layers = (pdk.get_glayer("pwell"),), default = pdk.get_grule("pwell", "active_tap")["min_enclosure"], )
        CurrentMirror = add_ports_perimeter(CurrentMirror, layer = pdk.get_glayer("pwell"), prefix="well_")
    elif type.lower() == "pfet":
        # add a nwell 
        CurrentMirror.add_padding(layers = (pdk.get_glayer("nwell"),), default = pdk.get_grule("nwell", "active_tap")["min_enclosure"], )
        CurrentMirror = add_ports_perimeter(CurrentMirror, layer = pdk.get_glayer("nwell"), prefix="well_")
    else:
        raise ValueError("type must be either nfet or pfet")
    
   
    #Connecting the source of the fets to the bulk ???
    src2bulk=CurrentMirror << straight_route(pdk, source_short.ports["con_N"],CurrentMirror.ports["currm_welltie_N_top_met_W"], glayer2="met2")
    
    ##The default naming scheme of ports in GDSFactory
    ##e1=West, e2=North, e3=East, e4=South. The default naming scheme of ports in GDSFactory

    # place vref pin (Needs more work to place it properly)
    vrefpin = CurrentMirror << rectangle(size=(0.5,0.5),layer=pdk.get_glayer("met3"),centered=True)
    vrefpin.movex(evaluate_bbox(vrefpin)[0]+(num_cols*maxmet_sep))
    vrefpin.movey(CurrentMirror.ymax)
    # route vref to drain of A
    CurrentMirror  << smart_route(pdk, CurrentMirror.ports["currm_A_0_drain_W"], vrefpin.ports["e4"])
    ## align_comp_to_port(vrefpin,ss.ports["top_met_E"], alignment=('c', 'b')) ?? How to align it properly
    
    
    # place vcopy pin (Needs more work to place it properly)
    vcopypin = CurrentMirror << rectangle(size=(0.5,0.5),layer=pdk.get_glayer("met3"),centered=True)
    vcopypin.movex(evaluate_bbox(vcopypin)[0]-(num_cols*maxmet_sep))
    vcopypin.movey(CurrentMirror.ymax)
    # route vcopy to drain of B
    CurrentMirror  << smart_route(pdk, CurrentMirror.ports["currm_B_0_drain_W"], vcopypin.ports["e4"])
    ## align_comp_to_port(vrefpin,ss.ports["top_met_E"], alignment=('c', 'b')) ?? How to align it properly
    

    CurrentMirror.add_ports(gate_short.get_ports_list(), prefix="gateshortports_")
    CurrentMirror.add_ports(src2bulk.get_ports_list(), prefix="purposegndports_")


    CurrentMirror.add_ports(vrefpin.get_ports_list(), prefix="refport_")
    CurrentMirror.add_ports(vcopypin.get_ports_list(), prefix="copyport_")


    CurrentMirror.info["netlist"] = generate_current_mirror_netlist(
                                    pdk=pdk,
                                    instance_name=CurrentMirror.name,
                                    CM_size= (Width, Length, num_cols,fingers),  # (width, length, multipliers)
                                    transistor_type=type,
                                    drain_net_A="VREF",  # Input drain connected to VREF 
                                    drain_net_B="VCOPY", # Output drain connected to VCOPY
                                    gate_net="VREF",      # Gate connected to VREF 
                                    source_net="VSS" if type=="nfet" else "VDD",    # Source connected to VSS
                                    proposed_ground= "VSS" if type=="nfet" else "VDD", #Proposed ground should also change
                                    subckt_only=True
                                    )

    generated_netlist_for_lvs = CurrentMirror.info['netlist'].generate_netlist()
    print(f"Type of generated netlist is :", generated_netlist_for_lvs)
    file_path_local_storage = "./gen_netlist.txt"
    try:
        with open(file_path_local_storage, 'w') as file:
            file.write(generated_netlist_for_lvs)
    except:
        print(f"Verify the file availability and type: ", generated_netlist_for_lvs, type(generated_netlist_for_lvs))

    return rename_ports_by_orientation(component_snap_to_grid(CurrentMirror))

def sky130_add_current_mirror_labels(
    CMS: Component, 
    transistor_type: str = "nfet",
    pdk: MappedPDK =sky130) -> Component:  
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
    
    move_info.append((vref_label, CMS.ports["refport_N"], None)) # Drain of A
    move_info.append((vref_label, CMS.ports["gateshortports_con_N"], None))  # Gate of A & B
    
    # VCOPY label (for drain of transistor B)
    vcopy_label = rectangle(layer=met2_pin, size=(0.5, 0.5), centered=True).copy()
    vcopy_label.add_label(text="VCOPY", layer=met2_label)
    move_info.append((vcopy_label, CMS.ports["copyport_N"], None))  # Drain of B
    
    
   # VSS/VDD label (for sources/bulk connection)
    if transistor_type.lower() == "nfet":
        bulk_net_name = "VSS"
        bulk_pin_layer = met2_pin 
        bulk_label_layer = met2_label 
    else:  # pfet
        bulk_net_name = "VDD"
        bulk_pin_layer = met2_pin 
        bulk_label_layer = met2_label 
    
    ##Need to clarify the bulk and source connection??
    # VB label 
    vb_label = rectangle(layer=bulk_pin_layer, size=(0.5, 0.5), centered=True).copy() 
    vb_label.add_label(text=bulk_net_name , layer=bulk_label_layer)

    move_info.append((vb_label, CMS.ports["purposegndports_route_N"], None)) 
    
    # Add labels to the component
    for label, port, alignment in move_info:
        if port:
            alignment = ('c', 'b') if alignment is None else alignment
            aligned_label = align_comp_to_port(label, port, alignment=alignment)
            CMS.add(aligned_label)

    return CMS.flatten()



# Main function to generate the current mirror layout
# mappedpdk, Width, Length, num_cols, fingers, transistor type
comp = cascode_current_mirror(sky130,3,0.5,2,1, type='nfet')
# Add labels to the current mirror layout
comp = sky130_add_current_mirror_labels(comp, transistor_type='nfet', pdk=sky130)



# Write the current mirror layout to a GDS file
comp.name = "CM"
delete_files_in_directory("GDS/")
tmpdirname = Path("GDS/").resolve()
delete_files_in_directory("GDS/")
tmp_gds_path = Path(comp.write_gds(gdsdir=tmpdirname)).resolve()
comp.write_gds("GDS/CM.gds")
comp.show()
# Generate the netlist for the current mirror
print("\n...Generating Netlist...")
print(comp.info["netlist"].generate_netlist())
# DRC Checks
#delete_files_in_directory("DRC/")
print("\n...Running DRC...")
drc_result = sky130.drc_magic(comp, "CM")
#drc_result = sky130.drc_magic(comp, "CM",output_file="DRC/")
print(drc_result['result_str'])
# LVS Checks
#delete_files_in_directory("LVS/")
print("\n...Running LVS...")
netgen_lvs_result = sky130.lvs_netgen(comp, "CM")  
#netgen_lvs_result = sky130.lvs_netgen(comp, "CM",output_file_path="LVS/")        
print(netgen_lvs_result['result_str'])


## Will be used in future for simulation
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
