import sys
from datetime import datetime
import subprocess
#from glayout.flow.pdk.gf180_mapped import gf180
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
#from glayout.flow.blocks.elementary.transmission_gate import transmission_gate as tg
import transmission_gate as tg
import cdac_sw as cdac_sw
import mim_cdac as mim_cdac

TARGET_PDK = sky130
PWD_OUTPUT = subprocess.run(['pwd'], capture_output=True, text=True)
GDS_DIR = PWD_OUTPUT.stdout.strip() + "/gds"
DRC_RPT_DIR = PWD_OUTPUT.stdout.strip() + "/regression/drc"
LVS_RPT_DIR = PWD_OUTPUT.stdout.strip() + "/regression/lvs"

pmos_width  = 3*4
pmos_length = 0.15
nmos_width  = 3*4
nmos_length = 0.15
fet_min_width = 3

def basic_tg_eval():
	tg_dut = tg.tg_cell(
		pdk=TARGET_PDK,
		component_name="tg",
		with_substrate_tap={"top_level":False, "pmos":False, "nmos":False},
		tap_cell={"pmos":True, "nmos":True},
		fet_min_width=fet_min_width,
		pmos_width=pmos_width,
		pmos_length=pmos_length,
		nmos_width=nmos_width,
		nmos_length=nmos_length,
		is_top_level=True
	)
	tg_dut.show()
	print(tg_dut.info["netlist"].generate_netlist())
	tg_dut.write_gds(f"{GDS_DIR}/{tg_dut.name}.gds")

	now = datetime.now() # Get the current date and time
	regression_id = now.strftime('%Y%m%d%H%M%S') # Format the date and time without spaces

	magic_drc_result = sky130.drc_magic(
		layout=tg_dut,
		design_name=tg_dut.name,
		output_file=f"{DRC_RPT_DIR}/{tg_dut.name}_{regression_id}_drc.rpt"
	)
	print(f"Magic DRC result ({tg_dut.name}): \n", magic_drc_result)
	print("--------------------------------------\n\n")
	netgen_lvs_result = sky130.lvs_netgen(
		layout=tg_dut,
		design_name=tg_dut.name,
		output_file_path=f"{LVS_RPT_DIR}/{tg_dut.name}_{regression_id}_lvs.rpt",
		copy_intermediate_files=True
	)

def basic_inv_eval():
	inv_dut = cdac_sw.inv_cell(
		pdk=TARGET_PDK,
		component_name="inv",
		with_substrate_tap={"top_level":False, "pmos":False, "nmos":False},
		tap_cell={"pmos":True, "nmos":True},
		fet_min_width=fet_min_width,
		pmos_width=pmos_width,
		pmos_length=pmos_length,
		nmos_width=nmos_width,
		nmos_length=nmos_length,
		is_top_level=True
	)
	inv_dut.show()
	print(inv_dut.info["netlist"].generate_netlist())
	inv_dut.write_gds(f"{GDS_DIR}/{inv_dut.name}.gds")

	now = datetime.now() # Get the current date and time
	regression_id = now.strftime('%Y%m%d%H%M%S') # Format the date and time without spaces

	magic_drc_result = sky130.drc_magic(
		layout=inv_dut,
		design_name=inv_dut.name,
		output_file=f"{DRC_RPT_DIR}/{inv_dut.name}_{regression_id}_drc.rpt"
	)
	print(f"Magic DRC result ({inv_dut.name}): \n", magic_drc_result)
	print("--------------------------------------\n\n")
	netgen_lvs_result = sky130.lvs_netgen(
		layout=inv_dut,
		design_name=inv_dut.name,
		output_file_path=f"{LVS_RPT_DIR}/{inv_dut.name}_{regression_id}_lvs.rpt",
		copy_intermediate_files=True
	)

def cdac_sw_1b_eval():
	cdac_sw_dut = cdac_sw.cdac_sw(
		pdk=TARGET_PDK,
		component_name="cdac_sw_1b",
		with_substrate_tap={"top_level":False, "pmos":False, "nmos":False},
		tap_cell={"pmos":True, "nmos":True},
		fet_min_width=fet_min_width,
		pmos_width=pmos_width,
		pmos_length=pmos_length,
		nmos_width=nmos_width,
		nmos_length=nmos_length,
		is_top_level=True
	)
	cdac_sw_dut.show()
	print(cdac_sw_dut.info["netlist"].generate_netlist())
	cdac_sw_dut.write_gds(f"{GDS_DIR}/{cdac_sw_dut.name}.gds")

	now = datetime.now() # Get the current date and time
	regression_id = now.strftime('%Y%m%d%H%M%S') # Format the date and time without spaces

	magic_drc_result = sky130.drc_magic(
		layout=cdac_sw_dut,
		design_name=cdac_sw_dut.name,
		output_file=f"{DRC_RPT_DIR}/{cdac_sw_dut.name}_{regression_id}_drc.rpt"
	)
	print(f"Magic DRC result ({cdac_sw_dut.name}): \n", magic_drc_result)
	print("--------------------------------------\n\n")
	netgen_lvs_result = sky130.lvs_netgen(
		layout=cdac_sw_dut,
		design_name=cdac_sw_dut.name,
		output_file_path=f"{LVS_RPT_DIR}/{cdac_sw_dut.name}_{regression_id}_lvs.rpt",
		copy_intermediate_files=True
	)

def mim_cdac_6b_eval():
	mim_cdac_dut = mim_cdac.mim_cdac(
		pdk=TARGET_PDK,
		component_name="mim_cdac_6b",
		with_substrate_tap={"top_level":False, "pmos":False, "nmos":False},
		tap_cell={"pmos":True, "nmos":True},
		fet_min_width=fet_min_width,
		pmos_width=pmos_width,
		pmos_length=pmos_length,
		nmos_width=nmos_width,
		nmos_length=nmos_length,
		is_top_level=True
	)
	mim_cdac_dut.show()
	print(mim_cdac_dut.info["netlist"].generate_netlist())
	mim_cdac_dut.write_gds(f"{GDS_DIR}/{mim_cdac_dut.name}.gds")

	now = datetime.now() # Get the current date and time
	regression_id = now.strftime('%Y%m%d%H%M%S') # Format the date and time without spaces

	magic_drc_result = sky130.drc_magic(
		layout=mim_cdac_dut,
		design_name=mim_cdac_dut.name,
		output_file=f"{DRC_RPT_DIR}/{mim_cdac_dut.name}_{regression_id}_drc.rpt"
	)
	print(f"Magic DRC result ({mim_cdac_dut.name}): \n", magic_drc_result)
	print("--------------------------------------")
	netgen_lvs_result = sky130.lvs_netgen(
		layout=mim_cdac_dut,
		design_name=mim_cdac_dut.name,
		output_file_path=f"{LVS_RPT_DIR}/{mim_cdac_dut.name}_{regression_id}_lvs.rpt",
		copy_intermediate_files=True
	)

def main():
	#basic_tg_eval()
	#basic_inv_eval()
	cdac_sw_1b_eval()
	#mim_cdac_6b_eval()

if __name__ == "__main__":
	main()