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

set_placement_padding -left 1 -right 1 -masters sky130_fd_sc_hd__decap_4
set_placement_padding -left 1 -right 1 -masters sky130_fd_sc_hd__inv_1
set_placement_padding -left 1 -right 1 -masters sky130_fd_sc_hd__nand2_1
set_placement_padding -left 0 -right 0 -masters sky130_fd_sc_hd__tapvpwrvgnd_1

set_placement_padding -left 1 -right 1 -masters sky130_fd_sc_hs__decap_4
set_placement_padding -left 0 -right 0 -masters sky130_fd_sc_hs__inv_1
set_placement_padding -left 0 -right 0 -masters sky130_fd_sc_hs__nand2_1
set_placement_padding -left 0 -right 0 -masters sky130_fd_sc_hs__tap_1

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



#set db [ord::get_db]
#set tech [$db getTech]
#set libs [$db getLibs]
#set block [$db getChip]

  #
  # Core area
  #
#  set core [$block getCoreArea]
#  set xl [$core xMin]
#  set yl [$core yMin]
#  set xh [$core xMax]
#  set yh [$core yMax]
#  set core_rect [odb::newSetFromRect $xl $yl $xh $yh]

  # Create a block for the Cryo RO
#  set ro_dim_x 40
#  set ro_dim_y 40
#  set ro_xl [expr $xl]
#  set ro_yl [expr $yl]
#  set ro_xh [expr $xl + $ro_dim_x]
#  set ro_yh [expr $yl + $ro_dim_y]
#  set ro_rect [odb::newSetFromRect $ro_xl $ro_yl $ro_xh $ro_yh]

  #
  # Output the blockages
  #
#  set rects [odb::getRectangles $ro_rect]
#  foreach rect $rects {
#      set b [odb::dbBlockage_create $block \
#                 [$rect xMin] [$rect yMin] [$rect xMax] [$rect yMax]]
#  }

#puts "RO Placement Blockage Set"

# find the bounds of the max_displacement
set db [::ord::get_db]
set block [[$db getChip] getBlock]
set tech [$db getTech]

set core [$block getCoreArea]
set core_xl [$core xMin]
set core_yl [$core yMin]
set core_xh [$core xMax]
set core_yh [$core yMax]

set max_disp_x [expr int(($core_xh - (($core_xl + $core_xh) * 3 / 4)) / 1000)]
set max_disp_y [expr int(($core_yh - ($core_yl + $core_yh) / 2) / 1000)]

set max_disp [concat $max_disp_x $max_disp_y]

puts $max_disp

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
