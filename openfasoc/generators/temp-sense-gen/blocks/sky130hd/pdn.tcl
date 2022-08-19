# Script not working yet: misses a connection between the VSS of both voltage domains,
# doesn't assign VIN (or VDD) to the endcap cells and doesn't create vias for the met4 straps

# Add global connections
add_global_connection -net VDD -inst_pattern {temp_analog_1.*} -pin_pattern VPWR -power
add_global_connection -net VDD -inst_pattern {temp_analog_1.*} -pin_pattern VPB
add_global_connection -net VIN -inst_pattern {temp_analog_0.*} -pin_pattern VPWR -power
add_global_connection -net VIN -inst_pattern {temp_analog_0.*} -pin_pattern VPB
add_global_connection -net VSS -inst_pattern {.*} -pin_pattern VGND -ground
add_global_connection -net VSS -inst_pattern {.*} -pin_pattern VNB

# Set voltage domains
# TEMP_ANALOG region created with the create_voltage_domain command
set_voltage_domain -name CORE -power VDD -ground VSS
set_voltage_domain -region TEMP_ANALOG -power VIN -ground VSS

# Standard cell grids
define_pdn_grid -name stdcell -pins met5 -starts_with POWER -voltage_domains {CORE TEMP_ANALOG}

add_pdn_stripe -grid stdcell -layer met1 -width 0.49 -pitch 6.66 -offset 0 -extend_to_core_ring -followpins
add_pdn_ring -grid stdcell -layer {met4 met5} -widths {5.0 5.0} -spacings {2.0 2.0} -core_offsets {2.0 2.0}
add_pdn_stripe -grid stdcell -layer met4 -width 0.96 -pitch 56.0 -offset 2 -extend_to_core_ring

add_pdn_connect -grid stdcell -layers {met4 met5}
add_pdn_connect -grid stdcell -layers {met1 met4}
