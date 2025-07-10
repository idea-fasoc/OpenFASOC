import sys
from os import path, rename, environ , listdir, remove, chmod
# environ['OPENBLAS_NUM_THREADS'] = '1'
from pathlib import Path
# # path to glayout
# sys.path.append(path.join(str(Path(__file__).resolve().parents[2])))

from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.flow.pdk.gf180_mapped import gf180_mapped_pdk as gf180

from glayout.flow.primitives.guardring import tapring
from glayout.flow.routing.smart_route import smart_route
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from glayout.flow.primitives.via_gen import via_stack
from glayout.flow.primitives.via_gen import via_stack


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
 
from CM_primitive import current_mirror_base, generate_current_mirror_netlist

def generate_self_biased_current_mirror_netlist(
    names: str = "SelfBiasedCurrentMirror",
    regulator: Component = None,
    base: Component = None,
    show_netlist : Optional[bool] = False,
    ) -> Netlist:
    """Generate a netlist for a current mirror."""
    
    topnet = Netlist(
        circuit_name=names,
        nodes=['IREF', 'ICOPY', 'VSS'],
    )
    
    base_ref = topnet.connect_netlist(
        base.info['netlist'],
        [('VSS', 'VSS') ]
    )

    regulator_ref = topnet.connect_netlist(
        regulator.info['netlist'],
        [('IREF', 'IREF'), ('ICOPY', 'ICOPY'), ('VSS', 'VSS')]
    )
    
    topnet.connect_subnets(
        base_ref,
        regulator_ref,
        [('IREF', 'INTA'), (('ICOPY', 'INTB')),('VSS', 'VSS')]
    )
    
    if show_netlist:
        generated_netlist_for_lvs = topnet.generate_netlist()
        print(f"Generated netlist :\n", generated_netlist_for_lvs)

        file_path_local_storage = "./gen_netlist.txt"
        try:
            with open(file_path_local_storage, 'w') as file:
                file.write(generated_netlist_for_lvs)
        except:
            print(f"Verify the file availability and type: ", generated_netlist_for_lvs, type(generated_netlist_for_lvs))
    return topnet

# @validate_arguments
def self_biased_cascode_current_mirror(
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
        show_netlist: Optional[bool] = False,
        **kwargs
    ) -> Component:
    """An instantiable self biased casoded current mirror that returns a Component object."""
    
    pdk.activate()
    maxmet_sep = pdk.util_max_metal_seperation()
    psize=(0.35,0.35)
    
    # Create the current mirror component
    SBCurrentMirror = Component(name="SBCurrentMirror")
    Length = Length if Length is not None else pdk.get_grule('poly')['min_width']
    
    # Create the interdigitized fets
    if type.lower() =="pfet" or type.lower() =="pmos":
        currm= two_pfet_interdigitized(pdk,numcols=num_cols,width=Width,length=Length,fingers=fingers, dummy=with_dummy,with_substrate_tap=with_substrate_tap,with_tie=with_tie)
        well, sdglayer = "nwell", "p+s/d"
    elif type.lower() =="nfet" or type.lower() =="nmos":
        currm= two_nfet_interdigitized(pdk,numcols=num_cols,width=Width,length=Length,fingers=fingers,dummy=with_dummy,                                with_substrate_tap=with_substrate_tap,with_tie=with_tie)
        well, sdglayer = "pwell", "n+s/d"
    else:
        raise ValueError("type must be either nfet or pfet")
        
    # Add the interdigitized fets to the current mirror top component
    top_currm_ref = prec_ref_center(currm)
    mid_currm_ref = prec_ref_center(currm)
    bottom_currm_ref = prec_ref_center(currm)
    
    
    SBCurrentMirror.add(top_currm_ref)
    SBCurrentMirror.add_ports(top_currm_ref.get_ports_list(),prefix="top_currm_")

    #Routing
    viam2m3 = via_stack(pdk, "met2", "met3", centered=True)
    topA_drain_via  = SBCurrentMirror << viam2m3
    topA_drain_via.move(SBCurrentMirror.ports[f"top_currm_A_{num_cols-1:d}_drain_E"].center).movex(1.2*(num_cols))
    topA_source_via  = SBCurrentMirror << viam2m3
    topA_source_via.move(SBCurrentMirror.ports[f"top_currm_A_0_source_W"].center).movex(-2.0)
    topA_gate_via  = SBCurrentMirror << viam2m3
    topA_gate_via.move(SBCurrentMirror.ports[f"top_currm_A_{num_cols-1:d}_gate_E"].center).movex(-0.5*Length+maxmet_sep+0.5*(num_cols))
    
    topB_drain_via  = SBCurrentMirror << viam2m3
    topB_drain_via.move(SBCurrentMirror.ports[f"top_currm_B_{num_cols-1:d}_drain_E"].center).movex(+0.5*num_cols)
    topB_source_via  = SBCurrentMirror << viam2m3
    topB_source_via.move(topA_source_via.center).movex(-2).movey(+1+maxmet_sep-Length)
    
    topB_gate_via  = SBCurrentMirror << viam2m3
    topB_gate_via.move(SBCurrentMirror.ports[f"top_currm_B_0_gate_W"].center).movex(-1.0)
    ##################### TOP
    SBCurrentMirror << straight_route(pdk,top_currm_ref.ports["A_0_drain_E"], topA_drain_via.ports["bottom_met_W"])
    SBCurrentMirror << straight_route(pdk,top_currm_ref.ports["B_0_drain_E"], topB_drain_via.ports["bottom_met_W"])
    ##################### 
    SBCurrentMirror << straight_route(pdk,top_currm_ref.ports["A_0_source_E"], topA_source_via.ports["bottom_met_W"])
    #SBCurrentMirror << straight_route(pdk,top_currm_ref.ports["B_0_source_E"], topB_source_via.ports["bottom_met_W"])
    topbulk=SBCurrentMirror << straight_route(pdk,SBCurrentMirror.ports[f"top_currm_B_0_source_W"],SBCurrentMirror.ports["top_currm_welltie_W_top_met_E"])
    SBCurrentMirror << straight_route(pdk,topbulk.ports["route_W"], topB_source_via["bottom_met_E"])    
    #####################
    SBCurrentMirror << straight_route(pdk,top_currm_ref.ports["A_0_gate_W"], topA_gate_via.ports["bottom_met_W"])
    SBCurrentMirror << straight_route(pdk,top_currm_ref.ports["B_0_gate_W"], topB_gate_via.ports["bottom_met_W"])
    #####################
    ASBG_shortT =  SBCurrentMirror << c_route(pdk, topA_source_via.ports["top_met_W"], topB_gate_via.ports["top_met_W"], extension=0.2*max(Width,Width), width1=psize[0], width2=psize[0], cwidth=0.32, e1glayer="met3", e2glayer="met3", cglayer="met3")
    AGBD_shortT =  SBCurrentMirror << c_route(pdk, topA_gate_via.ports["top_met_E"], topB_drain_via.ports["top_met_E"], extension=0.1*max(Width,Width), width1=psize[0], width2=psize[0], cwidth=0.32, e1glayer="met3", e2glayer="met3", cglayer="met3")
    #######################################################################################################################
    ## Adding the MID Current Mirror
    mid_currm_ref.move(top_currm_ref.center).movey(-evaluate_bbox(top_currm_ref)[1])
    SBCurrentMirror.add(mid_currm_ref)
    SBCurrentMirror.add_ports(mid_currm_ref.get_ports_list(), prefix="mid_cm_")
    #####################
    midA_drain_via  = SBCurrentMirror << viam2m3
    midA_drain_via.move(SBCurrentMirror.ports[f"mid_cm_A_0_drain_E"].center).movex(-2.0)
    SBCurrentMirror << straight_route(pdk,SBCurrentMirror.ports[f"mid_cm_A_{num_cols-1:d}_drain_E"], midA_drain_via["bottom_met_W"])
    SBCurrentMirror << L_route(pdk,midA_drain_via.ports["top_met_W"], ASBG_shortT.ports["con_S"])
    #, extension=1.5*max(Width,Width), width1=psize[0], width2=psize[0], cwidth=0.32, e1glayer="met3", e2glayer="met3", cglayer="met3")
    
    midA_gate_via  = SBCurrentMirror << viam2m3
    midA_gate_via.move(SBCurrentMirror.ports[f"mid_cm_A_{num_cols-1:d}_gate_E"].center).movex(1.2*(num_cols))
    SBCurrentMirror << straight_route(pdk,SBCurrentMirror.ports[f"mid_cm_A_{num_cols-1:d}_gate_E"], midA_gate_via["bottom_met_W"])
    gate_drain=SBCurrentMirror << c_route(pdk,midA_gate_via.ports["top_met_E"],topA_drain_via["top_met_E"],extension=0.1*max(Width,Width), width1=psize[0], width2=psize[0], cwidth=0.32, e1glayer="met3", e2glayer="met3", cglayer="met3")
    
    #####################
    midA_source_via  = SBCurrentMirror << viam2m3
    midA_source_via.move(SBCurrentMirror.ports[f"mid_cm_A_0_source_W"].center).movex(-4.0)
    midbulk1=SBCurrentMirror << straight_route(pdk,SBCurrentMirror.ports[f"mid_cm_A_0_source_W"],SBCurrentMirror.ports["mid_cm_welltie_W_top_met_E"])
    SBCurrentMirror << straight_route(pdk,midbulk1.ports["route_W"], midA_source_via["bottom_met_E"])
    SBCurrentMirror << straight_route(pdk,midA_source_via.ports["top_met_N"], topB_source_via["top_met_S"])
    
    #midB_source_via  = SBCurrentMirror << viam2m3
    #midB_source_via.move(SBCurrentMirror.ports[f"mid_cm_B_0_source_W"].center).movex(-5.0)
    midbulk2=SBCurrentMirror << straight_route(pdk,SBCurrentMirror.ports[f"mid_cm_B_0_source_W"],SBCurrentMirror.ports["mid_cm_welltie_W_top_met_E"])
    #SBCurrentMirror << straight_route(pdk,midbulk2.ports["route_S"], midbulk1.ports["route_N"])
 
    #####################
    midB_drain_via  = SBCurrentMirror << viam2m3
    midB_drain_via.move(SBCurrentMirror.ports[f"mid_cm_B_0_drain_E"].center).movex(-0.5*num_cols + maxmet_sep)
    SBCurrentMirror << straight_route(pdk,SBCurrentMirror.ports[f"mid_cm_B_0_drain_E"], midB_drain_via["bottom_met_W"])
    
    # #######################################################################################################################
    bottom_currm_ref.move(top_currm_ref.center).movey(-2*evaluate_bbox(top_currm_ref)[1])
    SBCurrentMirror.add(bottom_currm_ref)
    
    SBCurrentMirror.add_ports(bottom_currm_ref.get_ports_list(),prefix="bottom_currm_")
    
    
    #Routing
    bottomA_drain_via  = SBCurrentMirror << viam2m3
    bottomA_drain_via.move(SBCurrentMirror.ports[f"bottom_currm_A_{num_cols-1:d}_drain_E"].center).movex(1.2*(num_cols))
    bottomA_source_via  = SBCurrentMirror << viam2m3
    bottomA_source_via.move(SBCurrentMirror.ports[f"bottom_currm_A_0_source_W"].center).movex(-2.0)
    bottomA_gate_via  = SBCurrentMirror << viam2m3
    bottomA_gate_via.move(SBCurrentMirror.ports[f"bottom_currm_A_{num_cols-1:d}_gate_E"].center).movex(-0.5*Length+maxmet_sep+0.5*(num_cols))
    
    bottomB_drain_via  = SBCurrentMirror << viam2m3
    bottomB_drain_via.move(SBCurrentMirror.ports[f"bottom_currm_B_{num_cols-1:d}_drain_E"].center).movex(+0.5*num_cols)
    bottomB_source_via  = SBCurrentMirror << viam2m3
    bottomB_source_via.move(bottomA_source_via.center).movex(-2).movey(+1+maxmet_sep-Length)
    
    bottomB_gate_via  = SBCurrentMirror << viam2m3
    bottomB_gate_via.move(SBCurrentMirror.ports[f"bottom_currm_B_0_gate_W"].center).movex(-1.0)
    ##################### BOTTOM
    SBCurrentMirror << straight_route(pdk,bottom_currm_ref.ports["A_0_drain_E"], bottomA_drain_via.ports["bottom_met_W"])
    SBCurrentMirror << straight_route(pdk,bottom_currm_ref.ports["B_0_drain_E"], bottomB_drain_via.ports["bottom_met_W"])
    ##################### 
    SBCurrentMirror << straight_route(pdk,bottom_currm_ref.ports["A_0_source_E"], bottomA_source_via.ports["bottom_met_W"])
    #SBCurrentMirror << straight_route(pdk,top_currm_ref.ports["B_0_source_E"], topB_source_via.ports["bottom_met_W"])
    bottombulk=SBCurrentMirror << straight_route(pdk,SBCurrentMirror.ports[f"bottom_currm_B_0_source_W"],SBCurrentMirror.ports["bottom_currm_welltie_W_top_met_E"])
    SBCurrentMirror << straight_route(pdk,bottombulk.ports["route_W"], bottomB_source_via["bottom_met_E"]) 
    SBCurrentMirror << straight_route(pdk,midA_source_via.ports["top_met_S"], bottomB_source_via["top_met_N"])   
    
    #####################
    SBCurrentMirror << straight_route(pdk,bottom_currm_ref.ports["A_0_gate_W"], bottomA_gate_via.ports["bottom_met_W"])
    SBCurrentMirror << straight_route(pdk,bottom_currm_ref.ports["B_0_gate_W"], bottomB_gate_via.ports["bottom_met_W"])
    # #####################
    ASBG_shortB =  SBCurrentMirror << c_route(pdk, bottomA_source_via.ports["top_met_W"], bottomB_gate_via.ports["top_met_W"], extension=0.2*max(Width,Width), width1=psize[0], width2=psize[0], cwidth=0.32, e1glayer="met3", e2glayer="met3", cglayer="met3")
    AGBD_shortB =  SBCurrentMirror << c_route(pdk, bottomA_gate_via.ports["top_met_E"], bottomB_drain_via.ports["top_met_E"], extension=0.1*max(Width,Width), width1=psize[0], width2=psize[0], cwidth=0.32, e1glayer="met3", e2glayer="met3", cglayer="met3")
    
    SBCurrentMirror << L_route(pdk,midB_drain_via.ports["top_met_S"], bottomA_source_via.ports["top_met_E"])  
    #######################################################################################################################
    #######################################################################################################################
	# # Connecting dummies to the welltie
    # if with_dummy:
    #     try:
    #         CurrentMirror << straight_route(pdk, CurrentMirror.ports["A_0_dummy_L_gsdcon_top_met_W"],CurrentMirror.ports["welltie_W_top_met_W"],glayer2="met1")
    #     except KeyError:
    #         pass
    #     try:
    #         end_col = num_cols - 1
    #         port1 = f'B_{end_col}_dummy_R_gdscon_top_met_E'
    #         CurrentMirror << straight_route(pdk, CurrentMirror.ports[port1], CurrentMirror.ports["welltie_E_top_met_E"], glayer2="met1")
    #     except KeyError:
    #         pass
    
    # # add well
    # CurrentMirror.add_padding(default=pdk.get_grule(well, "active_tap")["min_enclosure"],layers=[pdk.get_glayer(well)])
    # CurrentMirror = add_ports_perimeter(CurrentMirror, layer = pdk.get_glayer(well), prefix="well_")
    #if well == "nwell": 
    #    CurrentMirror.add_padding(layers=(pdk.get_glayer("nwell"),),default= 1 )
    
    ###########################################################
    Irefpin = SBCurrentMirror << rectangle(size=psize,layer=pdk.get_glayer("met3"),centered=True)
    Irefpin.move(topA_drain_via.center).movey(0.2*evaluate_bbox(top_currm_ref)[0])
    SBCurrentMirror << L_route(pdk, gate_drain.ports["con_N"],Irefpin.ports["e3"])
    
    Icopypin = SBCurrentMirror << rectangle(size=psize,layer=pdk.get_glayer("met3"),centered=True)
    Icopypin.move(topA_drain_via.center).movex(+0.5*num_cols).movey(0.2*evaluate_bbox(top_currm_ref)[0])
    SBCurrentMirror << L_route(pdk, bottomA_drain_via["top_met_E"],Icopypin.ports["e4"])
    
    Ibiaspin = SBCurrentMirror << rectangle(size=psize,layer=pdk.get_glayer("met3"),centered=True)
    Ibiaspin.move(AGBD_shortB.center).movey(-evaluate_bbox(top_currm_ref)[1])
    SBCurrentMirror << L_route(pdk, AGBD_shortB["con_S"],Ibiaspin.ports["e1"])
    SBCurrentMirror << c_route(pdk, topB_drain_via["top_met_W"],Ibiaspin.ports["e1"],extension=max(Width,Width), width1=psize[0], width2=psize[0], cwidth=0.32, e1glayer="met3", e2glayer="met3", cglayer="met3")
    
    
    bulkpin = SBCurrentMirror << rectangle(size=psize,layer=pdk.get_glayer("met3"),centered=True)
    bulkpin.move(topB_source_via.center).movey(0.3*evaluate_bbox(top_currm_ref)[1])
    SBCurrentMirror << straight_route(pdk,topB_source_via["top_met_N"], bulkpin.ports["e4"] )
    
    SBCurrentMirror.add_ports(Irefpin.get_ports_list(), prefix="refport_")
    SBCurrentMirror.add_ports(Icopypin.get_ports_list(), prefix="copyport_")
    SBCurrentMirror.add_ports(Ibiaspin.get_ports_list(), prefix="biasport_")
    SBCurrentMirror.add_ports(bulkpin.get_ports_list(), prefix="bulkport_")
    
    ##############################
    # # Adding the Top Current Mirror Netlist
    # topcurrm.info["netlist"] = generate_current_mirror_netlist(
    #                                 pdk=pdk,
    #                                 instance_name="TopCurrentMirror",
    #                                 CM_size= (Width, Length, num_cols,fingers),  # (width, length, multipliers, fingers)
    #                                 transistor_type=type,
    #                                 drain_net_ref="IREF",  # Input drain connected to VREF 
    #                                 drain_net_copy="ICOPY", # Output drain connected to VCOPY
    #                                 gate_net="IREF",      # Gate connected to VREF 
    #                                 source_net_ref="INTA" ,
    #                                 source_net_copy="INTB" ,
    #                                 proposed_ground= "VSS" if type=="nfet" else "VDD", #Proposed ground should also change
    #                                 subckt_only=True,
    #                                 show_netlist=False,
    #                                 )
    
    # SBCurrentMirror.info["netlist"] = generate_self_biased_current_mirror_netlist(
    #                                 names=SBCurrentMirror.name,
    #                                 regulator=topcurrm,
    #                                 base=BCM,
    #                                 show_netlist=False,
    #                                 )

    return rename_ports_by_orientation(component_snap_to_grid(SBCurrentMirror))

def add_self_biased_cascode_cm_labels(
    CMS: Component, 
    transistor_type: str = "nfet",
    pdk: MappedPDK =sky130
    ) -> Component:  
    """Add labels to the current mirror layout for LVS, handling both nfet and pfet."""

    #Would be adjusted for pdk agonastic later
    met2_pin = (69, 16)
    met2_label = (69, 5)
    met3_pin = (70, 16)
    met3_label = (70, 5)
    
    CMS.unlock()
    move_info = []
    psize=(0.35,0.35)
    
    
    # VREF label (for both gate and drain of transistor A, and dummy drains)
    Iref_label = rectangle(layer=met2_pin, size=psize, centered=True).copy()
    Iref_label.add_label(text="IREF", layer=met2_label)
    move_info.append((Iref_label, CMS.ports["refport_N"], None)) # Drain of A
    #move_info.append((Iref_label, CMS.ports["gateshortports_con_N"], None))  # Gate of A & B
    
    # VCOPY label (for drain of transistor B)
    Icopy_label = rectangle(layer=met2_pin, size=psize, centered=True).copy()
    Icopy_label.add_label(text="ICOPY", layer=met2_label)
    move_info.append((Icopy_label, CMS.ports["copyport_N"], None))  # Drain of B
    
     # VCOPY label (for drain of transistor B)
    Ibias_label = rectangle(layer=met2_pin, size=psize, centered=True).copy()
    Ibias_label.add_label(text="IBIAS", layer=met2_label)
    move_info.append((Ibias_label, CMS.ports["biasport_N"], None))  # Drain of B


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
    vb_label = rectangle(layer=bulk_pin_layer, size=psize, centered=True).copy() 
    vb_label.add_label(text=bulk_net_name , layer=bulk_label_layer)
    move_info.append((vb_label, CMS.ports["bulkport_N"], None)) 
    
    # Add labels to the component
    for label, port, alignment in move_info:
        if port:
            alignment = ('c', 'b') if alignment is None else alignment
            aligned_label = align_comp_to_port(label, port, alignment=alignment)
            CMS.add(aligned_label)

    return CMS.flatten()




## To Test their primitives
# from current_mirror import current_mirror, current_mirror_netlist

if __name__ == "__main__":
	# Main function to generate the current mirror layout
    # mappedpdk, Width, Length, num_cols, fingers, transistor type
    comp = self_biased_cascode_current_mirror(sky130, num_cols=2, Width=3, device='nfet',show_netlist=False)
    #comp.pprint_ports()
    comp = add_self_biased_cascode_cm_labels(comp, transistor_type='nfet', pdk=sky130)
 

    

	# # # Write the current mirror layout to a GDS file
    #comp.name = "CM"
	# # delete_files_in_directory("GDS/")
	# # tmpdirname = Path("GDS/").resolve()
	# # delete_files_in_directory("GDS/")
	# # tmp_gds_path = Path(comp.write_gds(gdsdir=tmpdirname)).resolve()
    #comp.write_gds("./CM.gds")
    comp.show()
	# # # Generate the netlist for the current mirror
	# # print("\n...Generating Netlist...")
    #print(comp.info["netlist"].generate_netlist())
	# # # DRC Checks
	# # #delete_files_in_directory("DRC/")
    print("\n...Running DRC...")
    drc_result = sky130.drc_magic(comp, "CM")
    # # #drc_result = sky130.drc_magic(comp, "CM",output_file="DRC/")
    # print(drc_result['result_str'])
	# # LVS Checks
	# #delete_files_in_directory("LVS/")
    #print("\n...Running LVS...")
    #netgen_lvs_result = sky130.lvs_netgen(comp, "CM")  
	#netgen_lvs_result = sky130.lvs_netgen(comp, "CM",output_file_path="LVS/")        
    #print(netgen_lvs_result['result_str'])

  