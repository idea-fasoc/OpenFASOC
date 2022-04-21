if {![info exists standalone] || $standalone} {
  # Read lef
  read_lef $::env(TECH_LEF)
  read_lef $::env(SC_LEF)
  if {[info exist ::env(ADDITIONAL_LEFS)]} {
    foreach lef $::env(ADDITIONAL_LEFS) {
      read_lef $lef
    }
  }

  # Read liberty files
  foreach libFile $::env(LIB_FILES) {
    read_liberty $libFile
  }

  # Read design files
  read_def $::env(RESULTS_DIR)/3_1_place_gp.def
} else {
  puts "Starting detailed placement"
}

set_placement_padding -global \
    -left $::env(CELL_PAD_IN_SITES_DETAIL_PLACEMENT) \
    -right $::env(CELL_PAD_IN_SITES_DETAIL_PLACEMENT)

  #
  # Output the blockages
  #
#  set rects [odb::getRectangles $ro_rect]
#  foreach rect $rects {
#      set b [odb::dbBlockage_create $block \
#                 [$rect xMin] [$rect yMin] [$rect xMax] [$rect yMax]]
#  }

#detailed_placement -max_displacement $max_disp

detailed_placement

optimize_mirroring
check_placement -verbose

estimate_parasitics -placement
report_design_area
report_tns
report_wns

if {![info exists standalone] || $standalone} {
  # write output
  write_def $::env(RESULTS_DIR)/3_4_place_dp.def
  exit
}
