# Get tap and endcap cells
set block [ord::get_db_block]
set all_insts [$block getInsts]
set region [$block findRegion "TEMP_ANALOG"]
set boundary [$region getBoundaries]
set caps_analog {}
set caps_core {}
foreach inst $all_insts {
  if {[[$inst getMaster] getName] eq "sky130_fd_sc_hd__tapvpwrvgnd_1" || \
      [[$inst getMaster] getName] eq "sky130_fd_sc_hd__decap_4"} {
    set box [$inst getBBox]

    # Select cells from TEMP_ANALOG region
    if { [$box xMin] >= [$boundary xMin] && [$box xMax] <= [$boundary xMax] \
      && [$box yMin] >= [$boundary yMin] && [$box yMax] <= [$boundary yMax]} {
        lappend caps_analog $inst
      } else {
        lappend caps_core $inst
      }
  }
}

# Add global connections
add_global_connection -net VDD -inst_pattern {.*} -pin_pattern {VPWR|VPB} -power ;# default: VDD as power
add_global_connection -net VDD -inst_pattern {temp_analog_1.*} -pin_pattern {VPWR|VPB} -power
add_global_connection -net VIN -inst_pattern {temp_analog_0.*} -pin_pattern {VPWR|VPB} -power
add_global_connection -net VSS -inst_pattern {.*} -pin_pattern {VGND|VNB} -ground

# Manually add connections for tap and encap cells
foreach inst $caps_analog {
  add_global_connection -net VIN -inst_pattern [$inst getName] -pin_pattern {VPWR|VPB} -power
}
foreach inst $caps_core {
  add_global_connection -net VDD -inst_pattern [$inst getName] -pin_pattern {VPWR|VPB} -power
}

global_connect

# Set voltage domains
# TEMP_ANALOG region created with the create_voltage_domain command
set_voltage_domain -name CORE -power VDD -ground VSS
set_voltage_domain -region TEMP_ANALOG -power VIN -ground VSS

# Standard cell grids
# VDD / GND
define_pdn_grid -name stdcell -pins met5 -starts_with POWER -voltage_domains CORE

add_pdn_stripe -grid stdcell -layer met1 -width 0.49 -pitch 6.66 -offset 0 -extend_to_core_ring -followpins
add_pdn_ring -grid stdcell -layer {met4 met5} -widths {5.0 5.0} -spacings {2.0 2.0} -core_offsets {2.0 2.0}
add_pdn_stripe -grid stdcell -layer met4 -width 1.2 -pitch 56.0 -offset 2 -extend_to_core_ring

# Straps to connect the two domains together
add_pdn_stripe -grid stdcell -layer met5 -width 1.6 -offset 80.0 -pitch 56.0 -extend_to_core_ring -starts_with GROUND
add_pdn_stripe -grid stdcell -layer met5 -width 1.6 -pitch 15.0 -extend_to_core_ring -starts_with GROUND -number_of_straps 4 -nets VSS

add_pdn_connect -grid stdcell -layers {met4 met5}
add_pdn_connect -grid stdcell -layers {met1 met4}

# VIN / GND
define_pdn_grid -name stdcell_analog -pins met3 -starts_with POWER -voltage_domains TEMP_ANALOG

add_pdn_stripe -grid stdcell_analog -layer met1 -width 0.49 -pitch 6.66 -offset 0 -extend_to_core_ring -followpins
add_pdn_ring -grid stdcell_analog -layer {met4 met3} -widths {5.0 5.0} -spacings {2.0 2.0} -core_offsets {2.0 2.0}
add_pdn_stripe -grid stdcell_analog -layer met4 -width 1.2 -pitch 56.0 -offset 2 -extend_to_core_ring

add_pdn_connect -grid stdcell_analog -layers {met4 met3}
add_pdn_connect -grid stdcell_analog -layers {met1 met4}
add_pdn_connect -grid stdcell_analog -layers {met4 met5}
