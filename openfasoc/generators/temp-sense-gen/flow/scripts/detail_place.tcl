utl::set_metrics_stage "detailedplace__{}"
source $::env(SCRIPTS_DIR)/load.tcl
load_design 3_4_place_resized.odb 2_floorplan.sdc "Starting detailed placement"

source $::env(PLATFORM_DIR)/setRC.tcl

# Note: Ali B Hammoud 8/11/22
# template procedure which will place cells in the large voltage domain off east
# with name "cell_name" semi-stacked starting from row "row_num" (0 indexed)
# No error checking is used, so you must ensure the target row and block object are correct
proc customPlace_east {block_object cell_name row_num} {
	set target_row [lindex [$block_object getRows] $row_num]
	set y_initial [expr {[lindex [$target_row getOrigin] 1] / 1000.0}]
	set row_ydim [expr {[[$target_row getSite] getHeight] / 1000.0}]
	foreach inst [$block_object getInsts] {
		if {[[$inst getMaster] getName] == $cell_name} {
			place_cell -cell $cell_name -inst_name [$inst getName] -origin [list 82.8 $y_initial] -orient R0 -status PLACED
			set y_initial [expr {$y_initial + $row_ydim}]
		}
	}
}

# example of usage
set block [ord::get_db_block]
customPlace_east $block "HEADER" 10

set_placement_padding -global \
    -left $::env(CELL_PAD_IN_SITES_DETAIL_PLACEMENT) \
    -right $::env(CELL_PAD_IN_SITES_DETAIL_PLACEMENT)
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
