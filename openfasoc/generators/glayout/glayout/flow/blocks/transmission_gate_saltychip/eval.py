import transmission_gate as tg
#from glayout.flow.pdk.gf180_mapped import gf180
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
import cell_config as config

TARGET_PDK = sky130

def main():
    tg_inst = tg.tg_with_inv(pdk=TARGET_PDK, pmos_width=1, pmos_length=0.15, nmos_width=1, nmos_length=0.15)
    tg_inst = config.add_port_lvs(
        pdk=sky130,
        comp=tg_inst,
        port_list=[
	    	{
                "new_port": "Vctrl", 
	    		"new_port_label": "Vctrl",
				"new_port_via": True,
				"new_port_via_layers": ("met1", "met2"),
				"new_port_move": (0, -TARGET_PDK.get_grule("mcon")["min_separation"]),
	    		"ref_port": "inv_nmos_multiplier_0_gate_E",
				"ref_port_align": ("c", "b"),
				"connect_pos": "W" # To connce the ref_port to the "west" side of the new port
            }#,
	    	#{
            #    "new_port": "Vin", 
	    	#	"new_port_label": "Vin", 
	    	#	"ref_port": "tg_pmos_multiplier_0_source_W"
            #},
	    	#{
            #    "new_port": "Vout", 
	    	#	"new_port_label": "Vout",
	    	#	"ref_port": "tg_nmos_multiplier_0_drain_W",
			#	"connect_pos": "E" # To connect the ref_port to the "east" side of the new port
            #}
	    ],
		port_feature = {"port_type":"pin", "layer":"met1"} # met1 is actually mapped to li1 in sky130 proceess
	)
    #tg_inst.flatten()
    tg_inst.show()
	#tg_inst.write_gds("gds/tg_with_inv.gds")

if __name__ == "__main__":
    main()