import transmission_gate as tg
#from glayout.flow.pdk.gf180_mapped import gf180
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
import cell_config as config

def main():
    tg_inst = tg.tg_with_inv(pdk=sky130, pmos_width=1, pmos_length=0.15, nmos_width=1, nmos_length=0.15)
    tg_inst = config.add_port_lvs(
        pdk=sky130,
        comp=tg_inst,
        port_list=[
	    	{
                "new_port": "Vctrl", 
	    		"new_port_label": "Vctrl",
	    		"pin_width": tg_inst.ports["inv_nmos_multiplier_0_gate_S"].width, 
	    		"pin_height": tg_inst.ports["inv_nmos_multiplier_0_gate_S"].width, 
	    		"ref_port": "inv_nmos_multiplier_0_gate_S"
            },
	    	{
                "new_port": "Vin", 
	    		"new_port_label": "Vin",
	    		"pin_width": 0.3,#tg_inst.ports["tg_nmos_multiplier_0_source_S"].width, 
	    		"pin_height": 0.3,#tg_inst.ports["tg_nmos_multiplier_0_source_S"].width, 
	    		"ref_port": "tg_pmos_multiplier_0_source_W"
            },
	    	{
                "new_port": "Vout", 
	    		"new_port_label": "Vout",
	    		"pin_width": 0.3,#tg_inst.ports["tg_nmos_multiplier_0_drain_S"].width, 
	    		"pin_height": 0.3,#tg_inst.ports["tg_nmos_multiplier_0_drain_S"].width, 
	    		"ref_port": "tg_nmos_multiplier_0_drain_N"
            }
	    ],
		port_feature = {"port_type":"wire", "layer":"met2"} # met2 is actually mapped to met1 in sky130 proceess
	)
    #tg_inst.flatten()
    tg_inst.show()
	#tg_inst.write_gds("gds/tg_with_inv.gds")

if __name__ == "__main__":
    main()