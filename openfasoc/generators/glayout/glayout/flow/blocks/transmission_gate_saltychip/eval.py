import subprocess
#from glayout.flow.pdk.gf180_mapped import gf180
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
import reconfig_inv as reconfig_inv
import transmission_gate as tg
import comp_dc

TARGET_PDK = sky130
PWD_OUTPUT = subprocess.run(['pwd'], capture_output=True, text=True)
GDS_DIR = PWD_OUTPUT.stdout.strip() + "/gds"

pmos_width  = 6.0*2
pmos_length = 0.15
nmos_width  = 6.0*2
nmos_length = 0.15

def basic_tg_eval():
	tg_dut = tg.reconfig_tg(
		pdk=TARGET_PDK,
		component_name="tg",
		pmos_width=pmos_width,
		pmos_length=pmos_length,
		nmos_width=nmos_width,
		nmos_length=nmos_length,
		add_pin=True
	)

	tg_dut.show()
	tg_dut.write_gds(f"{GDS_DIR}/{tg_dut.name}.gds")
	'''
	magic_drc_result = sky130.drc_magic(
		layout=tg_dut,
		design_name=tg_dut.name#,
		#output_file=f"{absolute_path}/{tg.name}.rpt"
	)
	print(f"Magic DRC result ({tg_dut.name}): \n", magic_drc_result)
	print("--------------------------------------")
	'''

def gate_ctrl_inv_eval():
	gate_ctrl_inv = reconfig_inv.reconfig_inv(
		pdk=TARGET_PDK,
		component_name="gate_ctrl_inv",
		pmos_width=pmos_width,
		pmos_length=pmos_length,
		nmos_width=nmos_width,
		nmos_length=nmos_length,
		add_pin=True
	)
	gate_ctrl_inv.show()
	gate_ctrl_inv.write_gds(f"{GDS_DIR}/{gate_ctrl_inv.name}.gds")
	magic_drc_result = sky130.drc_magic(
		layout=gate_ctrl_inv,
		design_name=gate_ctrl_inv.name#,
		#output_file=f"{absolute_path}/{gate_ctrl_inv.name}.rpt"
	)
	print(f"Magic DRC result ({gate_ctrl_inv.name}): \n", magic_drc_result)
	print("--------------------------------------")

def tg_with_ctrl_eval():
	tg_dut = tg.tg_with_ctrl(
		pdk=TARGET_PDK,
		component_name="tg_with_ctrl",
		pmos_width=pmos_width,
		pmos_length=pmos_length,
		nmos_width=nmos_width,
		nmos_length=nmos_length
	)
	tg_dut.show()
	tg_dut.write_gds(f"{GDS_DIR}/{tg_dut.name}.gds")
	magic_drc_result = sky130.drc_magic(
		layout=tg_dut,
		design_name=tg_dut.name#,
		#output_file=f"{absolute_path}/{tg_dut.name}.rpt"
	)
	print(f"Magic DRC result ({tg_dut.name}): \n", magic_drc_result)
	print("--------------------------------------")

def main():
	basic_tg_eval()
	#gate_ctrl_inv_eval()
	#tg_with_ctrl_eval()

if __name__ == "__main__":
	comp_dc.initialise()
	main()