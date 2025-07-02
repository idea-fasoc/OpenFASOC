from fvf import flipped_voltage_follower, fvf_netlist, sky130_add_fvf_labels
from evaluator_wrapper import run_evaluation
from glayout.pdk.sky130_mapped import sky130_mapped_pdk

fvf = sky130_add_fvf_labels(flipped_voltage_follower(sky130_mapped_pdk, width=(2,1), sd_rmult=3))
fvf.name = "fvf"
fvf.show()
fvf_gds = fvf.write_gds("fvf.gds")
result = run_evaluation("fvf.gds",fvf.name,fvf)
print(result)
