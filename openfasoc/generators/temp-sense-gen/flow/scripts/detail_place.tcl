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

set_placement_padding -left 0 -right 0 -masters sky130_fd_sc_hd__decap_4

set_placement_padding -global \
    -left $::env(CELL_PAD_IN_SITES_DETAIL_PLACEMENT) \
    -right $::env(CELL_PAD_IN_SITES_DETAIL_PLACEMENT)

set db [ord::get_db]
set tech [$db getTech]
set libs [$db getLibs]
set block [[$db getChip] getBlock]

customPlace_east $block "HEADER" 10

set has_domain 0
foreach region [$block getRegions] {
  set domain $region
  set domain_name [$region getName]
  set has_domain 1
}
# delete rows from the smaller voltage domain
set domain_rows []
if {$has_domain == 1} {
  foreach row [$block getRows] {
    set result [regexp $domain_name [$row getName] match]
    if {$result == 1} {
      lappend domain_rows [list [$row getName] \
                                [$row getSite] \
                                [$row getBBox] \
                                [$row getOrient] \
                          ]
      odb::dbRow_destroy $row
    }
  }
}

set row [lindex [$block getRows] 0]
set row_site [$row getSite]
set site_width [$row_site getWidth]
set row_height [$row_site getHeight]

# run detailed placement
detailed_placement

#recreate the small voltage domain
foreach row $domain_rows {
  odb::dbRow_create $block [lindex $row 0] \
                           [lindex $row 1] \
                           [[lindex $row 2] xMin] \
                           [[lindex $row 2] yMin] \
                           [lindex $row 3] \
                           "HORIZONTAL" \
                           [expr ([[lindex $row 2] xMax] - [[lindex $row 2] xMin]) / [[lindex $row 1] getWidth]] \
                           [[lindex $row 1] getWidth]
}


if {$has_domain == 1} {
  set placed_insts []
  set region_insts [$region getRegionInsts]
  foreach inst [$block getInsts] {
    if {[lsearch -exact $region_insts $inst] >= 0} {
    } else {
      if {[$inst getPlacementStatus] == "FIRM"} {
      } else {
        lappend placed_insts $inst
        $inst setPlacementStatus "FIRM"
      }
    }
  }

  set core_rows []
  foreach row [$block getRows] {
    set result [regexp $domain_name [$row getName] match]
    if {$result == 1} {
    } else {
      lappend core_rows [list [$row getName] \
                              [$row getSite] \
                              [$row getBBox] \
                              [$row getOrient] \
                        ]
      odb::dbRow_destroy $row
    }
  }
#rerun detailed place
  detailed_placement

  foreach row $core_rows {
    odb::dbRow_create $block [lindex $row 0] \
                             [lindex $row 1] \
                             [[lindex $row 2] xMin] \
                             [[lindex $row 2] yMin] \
                             [lindex $row 3] \
                             "HORIZONTAL" \
                             [expr ([[lindex $row 2] xMax] - [[lindex $row 2] xMin]) / [[lindex $row 1] getWidth]] \
                             [[lindex $row 1] getWidth]

  }

  foreach inst $placed_insts {
    $inst setPlacementStatus "PLACED"
  }
}

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
