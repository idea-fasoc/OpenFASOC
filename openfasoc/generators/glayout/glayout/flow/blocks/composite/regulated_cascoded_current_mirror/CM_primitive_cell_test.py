import sys
from os import path, rename, environ
environ['OPENBLAS_NUM_THREADS'] = '1'
from pathlib import Path
# path to glayout
sys.path.append(path.join(str(Path(__file__).resolve().parents[2])))


from glayout.flow.primitives.guardring import tapring
from glayout.flow.primitives.fet import pmos
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.routing.straight_route import straight_route
from glayout.flow.routing.c_route import c_route
from glayout.flow.routing.L_route import L_route
from gdsfactory import Component
from glayout.flow.spice.netlist import Netlist
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
from glayout.flow.pdk.gf180_mapped import gf180_mapped_pdk as gf180
from glayout.flow.placement.two_transistor_interdigitized import two_nfet_interdigitized, two_pfet_interdigitized
from gdsfactory.components import text_freetype, rectangle
from typing import Optional, Union 
from glayout.flow.pdk.util.comp_utils import evaluate_bbox, prec_center, prec_array, movey, align_comp_to_port, prec_ref_center
from glayout.flow.routing.smart_route import smart_route


global PDK_ROOT
if 'PDK_ROOT' in environ:
	PDK_ROOT = str(Path(environ['PDK_ROOT']).resolve())
else:
	PDK_ROOT = "/usr/bin/miniconda3/share/pdk/"
 
from glayout.flow.blocks.elementary.current_mirror.current_mirror import current_mirror, current_mirror_netlist

comp = CurrentMirror(sky130, (3, 3, 2), type='nfet', rmult=1)
comp = sky130_add_current_mirror_labels(comp, transistor_type='nfet', pdk=sky130)
comp.name = "CM"
comp.write_gds("CM.gds")

# for absc in comp.ports.keys():
#     if len(absc.split("_")) <=5:
#         print(absc)
    
print(comp.info["netlist"].generate_netlist())
comp.show()

# %%
print("\n...Running LVS...")

sky130.lvs_netgen(comp, "CM")        

# %%



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