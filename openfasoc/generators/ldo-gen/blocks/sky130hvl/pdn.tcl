####################################
# global connections
####################################
add_global_connection -defer_connection -net {VDD} -pin_pattern {^VDD$} -power
add_global_connection -defer_connection -net {VDD} -pin_pattern {^VDDPE$}
add_global_connection -defer_connection -net {VDD} -pin_pattern {VPWR}
add_global_connection -defer_connection -net {VDD} -pin_pattern {vpwr}
add_global_connection -defer_connection -net {VDD} -pin_pattern {VPB}
add_global_connection -defer_connection -net {VDD} -pin_pattern {vpb}
add_global_connection -defer_connection -net {VSS} -pin_pattern {^VSS$} -ground
add_global_connection -defer_connection -net {VSS} -pin_pattern {^VSSE$}
add_global_connection -defer_connection -net {VSS} -pin_pattern {VGND}
add_global_connection -defer_connection -net {VSS} -pin_pattern {vgnd}
add_global_connection -defer_connection -net {VSS} -pin_pattern {VNB}
add_global_connection -defer_connection -net {VSS} -pin_pattern {vnb}
add_global_connection -defer_connection -net {VREG} -pin_pattern {vref} -power
add_global_connection -defer_connection -net {VREG} -pin_pattern {vreg} -power
add_global_connection -defer_connection -net {VREG} -pin_pattern {VREG} -power
add_global_connection -defer_connection -net {VREG} -pin_pattern {pin0} -power
add_global_connection -defer_connection -net {VREF} -pin_pattern {VREF} -power

global_connect
####################################
# voltage domains
####################################
set_voltage_domain -name {CORE} -power {VDD} -ground {VSS} 
set_voltage_domain -region {LDO_VREG} -power {VDD} -ground {VSS} -secondary_power {VREG}
####################################
# standard cell grid
####################################
define_pdn_grid -name {grid} -voltage_domains {CORE LDO_VREG} -pins {met5}
 
add_pdn_stripe -grid {grid} -layer {met1} -width {0.48} -pitch {5.44} -offset {0} -followpins -extend_to_core_ring
add_pdn_stripe -grid {grid} -layer {met4} -width {0.96} -pitch {56} -offset {2} -extend_to_core_ring
add_pdn_stripe -grid {grid} -layer {met5} -width {1.600} -pitch {40} -offset {2} 
            
add_pdn_ring -grid {grid} -layer {met4 met5} -widths 5.0 -spacings  2.0 -core_offset 2.0              
             
add_pdn_connect -grid {grid} -layers {met1 met4}
add_pdn_connect -grid {grid} -layers {met4 met5}
####################################
# macro grids
####################################
####################################
# grid for: CORE_macro_grid_1
####################################
define_pdn_grid -name {CORE_macro_grid_1} -voltage_domains {LDO_VREG} -macro -orient {R0 R180 MX MY} -halo {2.0 2.0 2.0 2.0} -default -obstructions {met1 met2 met3 met4}
                              
add_pdn_connect -grid {CORE_macro_grid_1} -layers {met4 met5} 
