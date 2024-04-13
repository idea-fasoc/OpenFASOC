# import sys, os
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'openfasoc', 'generators', 'gdsfactory-gen'))
# from glayout.primitives.fet import nmos
# from glayout.components.diff_pair import diff_pair
# from glayout.components.opamp import opamp
# from glayout.pdk.sky130_mapped import sky130_mapped_pdk as sky130


# diff_pair = diff_pair(pdk=sky130)
# diff_pair.name = "diff_test"
# print((diff_pair.info['netlist'].generate_netlist()))

# opamp = opamp(pdk=sky130)
# opamp.name = "opamp_test"
# print((opamp.info['netlist'].generate_netlist()))