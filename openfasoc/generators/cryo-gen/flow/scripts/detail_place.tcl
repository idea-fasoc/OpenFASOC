utl::set_metrics_stage "detailedplace__{}"
source $::env(SCRIPTS_DIR)/load.tcl
load_design 3_1_place_gp.odb 2_floorplan.sdc "Starting detailed placement"

source $::env(PLATFORM_DIR)/setRC.tcl

set_placement_padding -global \
    -left $::env(CELL_PAD_IN_SITES_DETAIL_PLACEMENT) \
    -right $::env(CELL_PAD_IN_SITES_DETAIL_PLACEMENT)

# place header cells in the right, starting from row 1 upward (not randomly)
source $::env(SCRIPTS_DIR)/openfasoc/custom_place.tcl
customPlace_east [ord::get_db_block] "HEADER" 1 no

set_placement_padding -left 1 -right 1 -masters sky130_fd_sc_hd__decap_4
set_placement_padding -left 1 -right 1 -masters sky130_fd_sc_hd__inv_1
set_placement_padding -left 1 -right 1 -masters sky130_fd_sc_hd__nand2_1
set_placement_padding -left 0 -right 0 -masters sky130_fd_sc_hd__tapvpwrvgnd_1

set_placement_padding -left 1 -right 1 -masters sky130_fd_sc_hs__decap_4
set_placement_padding -left 0 -right 0 -masters sky130_fd_sc_hs__inv_1
set_placement_padding -left 0 -right 0 -masters sky130_fd_sc_hs__nand2_1
set_placement_padding -left 0 -right 0 -masters sky130_fd_sc_hs__tapvpwrvgnd_1

set_placement_padding -left 0 -right 0 -masters sky130_fd_sc_hvl__inv_1
set_placement_padding -left 1 -right 1 -masters sky130_fd_sc_hvl__decap_4
set_placement_padding -left 0 -right 0 -masters sky130_fd_sc_hvl__nand2_1

set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_12T_hs__inv_1
set_placement_padding -left 1 -right 1 -masters sky130_osu_sc_12T_hs__decap_1
set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_12T_hs__nand2_1

set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_12T_ms__inv_1
set_placement_padding -left 1 -right 1 -masters sky130_osu_sc_12T_ms__decap_1
set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_12T_ms__nand2_1

set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_12T_ls__inv_1
set_placement_padding -left 1 -right 1 -masters sky130_osu_sc_12T_ls__decap_1
set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_12T_ls__nand2_1

set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_15T_hs__inv_1
set_placement_padding -left 1 -right 1 -masters sky130_osu_sc_15T_hs__decap_1
set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_15T_hs__nand2_1

set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_15T_ms__inv_1
set_placement_padding -left 1 -right 1 -masters sky130_osu_sc_15T_ms__decap_1
set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_15T_ms__nand2_1

set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_15T_ls__inv_1
set_placement_padding -left 1 -right 1 -masters sky130_osu_sc_15T_ls__decap_1
set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_15T_ls__nand2_1

set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_18T_hs__inv_1
set_placement_padding -left 1 -right 1 -masters sky130_osu_sc_18T_hs__decap_1
set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_18T_hs__nand2_1

set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_18T_ms__inv_1
set_placement_padding -left 1 -right 1 -masters sky130_osu_sc_18T_ms__decap_1
set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_18T_ms__nand2_1

set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_18T_ls__inv_1
set_placement_padding -left 1 -right 1 -masters sky130_osu_sc_18T_ls__decap_1
set_placement_padding -left 0 -right 0 -masters sky130_osu_sc_18T_ls__nand2_1

detailed_placement

if {[info exists ::env(ENABLE_DPO)] && $::env(ENABLE_DPO)} {
  if {[info exist ::env(DPO_MAX_DISPLACEMENT)]} {
    improve_placement -max_displacement $::env(DPO_MAX_DISPLACEMENT)
  } else {
    improve_placement
  }
}
optimize_mirroring

utl::info FLW 12 "Placement violations [check_placement -verbose]."

estimate_parasitics -placement

source $::env(SCRIPTS_DIR)/report_metrics.tcl
report_metrics "detailed place"

if {![info exists save_checkpoint] || $save_checkpoint} {
  write_db $::env(RESULTS_DIR)/3_5_place_dp.odb
}
