####################################
# global connections
####################################
#add_global_connection -defer_connection -net {VDD} -pin_pattern {^VDD$} -power
#add_global_connection -defer_connection -net {VDD} -pin_pattern {^VDDPE$}
add_global_connection -net {VDD} -pin_pattern {VPWR} -power
add_global_connection -net {VDD} -pin_pattern {vpwr} -power
add_global_connection -net {VDD} -pin_pattern {VPB} -power
add_global_connection -net {VDD} -pin_pattern {vpb} -power
#add_global_connection -defer_connection -net {VSS} -pin_pattern {^VSS$} -ground
#add_global_connection -defer_connection -net {VSS} -pin_pattern {^VSSE$}
add_global_connection -net {VSS} -pin_pattern {VGND} -ground
add_global_connection -net {VSS} -pin_pattern {vgnd} -ground
add_global_connection -net {VSS} -pin_pattern {VNB} -ground
add_global_connection -net {VSS} -pin_pattern {vnb} -ground
add_global_connection -net VREG -pin_pattern {VREG} -power

global_connect
####################################
# voltage domains
####################################
set_voltage_domain -name {CORE} -power {VDD} -ground {VSS}
set_voltage_domain -region {LDO_VREG} -power {VDD} -ground {VSS} -secondary_power VREG
####################################
# CORE - VDD,VSS
####################################
define_pdn_grid -name {grid} -pins {met5} -voltage_domains {CORE}

add_pdn_stripe -grid {grid} -layer {met1} -width {0.65} -pitch {5.48} -offset {0} -followpins -extend_to_core_ring
add_pdn_stripe -grid {grid} -layer {met4} -starts_with POWER -width {1.8} -pitch {56} -offset {15} -extend_to_core_ring
add_pdn_stripe -grid {grid} -layer {met5} -starts_with POWER -width {2.0} -pitch {85} -offset {10} -extend_to_core_ring

add_pdn_ring -grid {grid} -layer {met4 met5} -widths 5.0 -spacings  2.0 -core_offset 2.0

add_pdn_connect -grid {grid} -layers {met1 met4}
add_pdn_connect -grid {grid} -layers {met4 met5}
####################################
# LDO_VREG - VDD,VSS,VREG
####################################
define_pdn_grid -name stdcell_analog1 -voltage_domains LDO_VREG -pins {met4}

add_pdn_stripe -grid stdcell_analog1 -layer {met1} -starts_with GROUND -width {0.65} -pitch {5.48} -offset {10} -followpins
add_pdn_ring -grid stdcell_analog1 -layer {met4 met3} -widths {5.0 5.0} -spacings {2.0 2.0} -core_offsets {2.0 2.0}
add_pdn_stripe -grid stdcell_analog1 -layer met4 -width 1.8 -pitch 250.0 -offset 2 -extend_to_core_ring -nets VDD -number_of_straps 2
add_pdn_stripe -grid stdcell_analog1 -layer met4 -width 1.8 -pitch 225.0 -offset 14 -extend_to_core_ring -nets VSS -number_of_straps 2
add_pdn_stripe -grid stdcell_analog1 -layer met4 -width 1.8 -pitch 20.0 -offset 24  -extend_to_core_ring -nets VREG -number_of_straps 11

add_pdn_connect -grid {stdcell_analog1} -layers {met4 met3}
add_pdn_connect -grid {stdcell_analog1} -layers {met1 met4}
add_pdn_connect -grid {stdcell_analog1} -layers {met4 met5}

####################################
# macro grids
####################################
####################################
# grid for: CORE_macro_grid_1
####################################
define_pdn_grid -name {CORE_macro_grid_1} -voltage_domains {CORE} -macro -orient {R0 R180 MX MY} -halo {1.0} -instances vref_gen

add_pdn_stripe -grid {CORE_macro_grid_1} -layer met4 -width 1.2 -pitch 90.0 -offset 2 -extend_to_core_ring -nets VDD -number_of_straps 2
add_pdn_stripe -grid {CORE_macro_grid_1} -layer met4 -width 1.2 -pitch 20.00 -offset 2 -extend_to_core_ring -nets VSS

add_pdn_connect -grid {CORE_macro_grid_1} -layers {met4 met5}
add_pdn_connect -grid {CORE_macro_grid_1} -layers {met1 met4}


####################################
# grid for: CORE_macro_grid_2
####################################

define_pdn_grid -name {CORE_macro_grid_2} -voltage_domains {CORE} -macro -orient {R0 R180 MX MY} -halo {1.0} -default

add_pdn_connect -grid {CORE_macro_grid_2} -layers {met4 met5}
add_pdn_connect -grid {CORE_macro_grid_2} -layers {met1 met4}
