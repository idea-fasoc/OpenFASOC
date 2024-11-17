import transmission_gate as tg
#from glayout.flow.pdk.gf180_mapped import gf180
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
import reconfig_inv as reconfig_inv

TARGET_PDK = sky130

def main():
	gate_ctrl_inv = reconfig_inv.reconfig_inv(
		pdk=TARGET_PDK,
		component_name="gate_ctrl_inv",
		pmos_width=1,
		pmos_length=0.15,
		nmos_width=1,
		nmos_length=0.15,
		orientation="horizontal"
	)
	gate_ctrl_inv.show()
	gate_ctrl_inv.write_gds("/home/tsengs0/gate_ctrl_inv.gds")

	magic_drc_result = sky130.drc_magic(
		layout=gate_ctrl_inv,
		design_name=gate_ctrl_inv.name#,
		#output_file=f"{absolute_path}/{gate_ctrl_inv.name}.rpt"
	)
	print("Magic DRC result: \n", magic_drc_result)

if __name__ == "__main__":
    main()