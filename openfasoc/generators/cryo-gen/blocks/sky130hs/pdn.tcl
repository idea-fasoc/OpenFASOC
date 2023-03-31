####################################
## global connections
#####################################
add_global_connection  -net {VDD} -inst_pattern {.*} -pin_pattern {^VDD$} -power
add_global_connection  -net {VDD} -inst_pattern {.*} -pin_pattern {^VDDPE$}
add_global_connection  -net {VDD} -inst_pattern {.*} -pin_pattern {^VDDCE$}
add_global_connection  -net {VDD} -inst_pattern {.*} -pin_pattern {VPWR}
add_global_connection  -net {VDD} -inst_pattern {.*} -pin_pattern {VPB}
add_global_connection  -net {VSS} -inst_pattern {.*} -pin_pattern {^VSS$} -ground
add_global_connection  -net {VSS} -inst_pattern {.*} -pin_pattern {^VSSE$}
add_global_connection  -net {VSS} -inst_pattern {.*} -pin_pattern {VGND}
add_global_connection  -net {VSS} -inst_pattern {.*} -pin_pattern {VNB}
global_connect
#####################################
## voltage domains
#####################################
set_voltage_domain -name {CORE} -power {VDD} -ground {VSS}
#####################################
## standard cell grid
#####################################
define_pdn_grid -name {grid} -voltage_domains {CORE} -starts_with POWER -pins met5
add_pdn_stripe -grid {grid} -layer {met1} -width {0.48} -pitch {6.66} -offset {0} -extend_to_core_ring -followpins
add_pdn_ring -grid {grid} -layers {met4 met5} -widths {4.2 4.2} -spacings {1.6 1.6} -core_offsets {4.1 4.1}
add_pdn_stripe -grid {grid} -layer {met4} -width {1.600} -pitch {27.140} -offset {13.570} -extend_to_core_ring
add_pdn_stripe -grid {grid} -layer {met5} -width {1.600} -pitch {27.200} -offset {13.600} -extend_to_core_ring -net {VSS}
#add_pdn_stripe -grid {grid} -layer {met5} -width {1.600} -pitch {27.200} -offset {11.440} -extend_to_core_ring
add_pdn_connect -grid {grid} -layers {met1 met4}
add_pdn_connect -grid {grid} -layers {met4 met5}
