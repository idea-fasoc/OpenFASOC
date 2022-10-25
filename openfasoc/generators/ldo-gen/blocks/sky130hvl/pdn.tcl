####################################
# global connections
####################################
#add_global_connection -defer_connection -net {VDD} -pin_pattern {^VDD$} -power
#add_global_connection -defer_connection -net {VDD} -pin_pattern {^VDDPE$}
add_global_connection -net {VDD} -pin_pattern {VPWR} -power
add_global_connection -net {VDD} -pin_pattern {vpwr}
add_global_connection -net {VDD} -pin_pattern {VPB}
add_global_connection -net {VDD} -pin_pattern {vpb}
#add_global_connection -defer_connection -net {VSS} -pin_pattern {^VSS$} -ground
#add_global_connection -defer_connection -net {VSS} -pin_pattern {^VSSE$}
add_global_connection -net {VSS} -pin_pattern {VGND} -ground
add_global_connection -net {VSS} -pin_pattern {vgnd}
add_global_connection -net {VSS} -pin_pattern {VNB}
add_global_connection -net {VSS} -pin_pattern {vnb}
#add_global_connection -defer_connection -net {VREF} -pin_pattern {vref} -power
#add_global_connection -net VREG -inst_pattern {.*} -pin_pattern {VREG} -power
#add_global_connection -defer_connection -net {VREF} -pin_pattern {pin0} -power
#add_global_connection -defer_connection -net {VREF} -pin_pattern {VREF} -power
add_global_connection -net VREG -pin_pattern {VREG} -power
global_connect
####################################
# voltage domains
####################################
set_voltage_domain -name {CORE} -power {VDD} -ground {VSS}
set_voltage_domain -region {LDO_VREG} -power {VDD} -ground {VSS} -secondary_power VREG
####################################
# standard cell grid
####################################
define_pdn_grid -name {grid} -pins {met5} -voltage_domains {CORE}

add_pdn_stripe -grid {grid} -layer {met1} -width {0.49} -pitch {5.48} -offset {0} -extend_to_core_ring -followpins
add_pdn_stripe -grid {grid} -layer {met4} -starts_with POWER -width {1.2} -pitch {27.0} -offset {2} -extend_to_core_ring
add_pdn_stripe -grid {grid} -layer {met5} -starts_with POWER -width {1.6} -pitch {29.1} -offset {2} -extend_to_core_ring

add_pdn_ring -grid {grid} -layer {met4 met5} -widths 5.0 -spacings  2.0 -core_offset 2.0

add_pdn_connect -grid {grid} -layers {met1 met4}
add_pdn_connect -grid {grid} -layers {met4 met5}
####################################
define_pdn_grid -name stdcell_analog1  -starts_with POWER -voltage_domains LDO_VREG -pins {met3}

add_pdn_stripe -grid stdcell_analog1 -layer met1 -width {0.49} -pitch {5.48} -offset 0 -extend_to_core_ring -followpins
add_pdn_ring -grid stdcell_analog1 -layer {met4 met3} -widths {5.0 5.0} -spacings {2.0 2.0} -core_offsets {2.0 2.0}
#add_pdn_stripe -grid stdcell_analog1 -layer met4 -width 1.2 -pitch 10.0 -offset 2 -extend_to_core_ring
add_pdn_stripe -grid stdcell_analog1 -layer met3 -width 1.2 -pitch 27.0 -offset 2 -extend_to_core_ring

add_pdn_connect -grid stdcell_analog1 -layers {met4 met3}
add_pdn_connect -grid stdcell_analog1 -layers {met1 met4}
add_pdn_connect -grid stdcell_analog1 -layers {met4 met5}



####################################
####################################
# macro grids
####################################
####################################
# grid for: CORE_macro_grid_1
####################################
define_pdn_grid -name {CORE_macro_grid_1} -voltage_domains {CORE} -macro -orient {R0 R180 MX MY} -halo {2.0 2.0 2.0 2.0} -default -grid_over_boundary -obstructions {li1 met1 met2 met3 met4}

add_pdn_connect -grid {CORE_macro_grid_1} -layers {met4 met5}
add_pdn_connect -grid {CORE_macro_grid_1} -layers {met1 met4}
