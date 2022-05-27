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
  read_def $::env(RESULTS_DIR)/2_floorplan.def
  read_sdc $::env(RESULTS_DIR)/2_floorplan.sdc
  if [file exists $::env(PLATFORM_DIR)/derate.tcl] {
    source $::env(PLATFORM_DIR)/derate.tcl
  }
} else {
  puts "Starting global placement"
}


# Set res and cap
source $::env(PLATFORM_DIR)/setRC.tcl
set_dont_use $::env(DONT_USE_CELLS)

# set fastroute layer reduction
# if {[info exist env(FASTROUTE_TCL)]} {
#   source $env(FASTROUTE_TCL)
# } else {
#     set_global_routing_layer_adjustment $env(MIN_ROUTING_LAYER)-$env(MAX_ROUTING_LAYER) 0.5
#       set_routing_layers -signal $env(MIN_ROUTING_LAYER)-$env(MAX_ROUTING_LAYER)
#         set_macro_extension 2
# }

if { 0 != [llength [array get ::env GLOBAL_PLACEMENT_ARGS]] } {
global_placement -routability_driven -density $::env(PLACE_DENSITY) \
    -pad_left $::env(CELL_PAD_IN_SITES_GLOBAL_PLACEMENT) \
    -pad_right $::env(CELL_PAD_IN_SITES_GLOBAL_PLACEMENT) \
    $::env(GLOBAL_PLACEMENT_ARGS)
} else {
global_placement -routability_driven -density $::env(PLACE_DENSITY) \
    -pad_left $::env(CELL_PAD_IN_SITES_GLOBAL_PLACEMENT) \
    -pad_right $::env(CELL_PAD_IN_SITES_GLOBAL_PLACEMENT)
}

# set db [ord::get_db]
# set tech [$db getTech]
# set libs [$db getLibs]
# set block [[$db getChip] getBlock]

# set region [$block findRegion "u_DCDC_SIX_STAGES_CONV"]
# set rect [lindex [$region getBoundaries] 0]

# set domain_xMin [$rect xMin]
# set domain_yMin [$rect yMin]
# set domain_xMax [$rect xMax]
# set domain_yMax [$rect yMax]

# foreach inst [$block getInsts] {
#   if {[[$inst getMaster] getName] == "HEADER"} {
#     $inst setOrigin $domain_xMax $domain_yMax
#   }
# }

# set allInsts [$block getInsts]

#-------------------------------------------------------------------------
# Force all divider cells into the center of the right half
# set db [::ord::get_db]
# set block [[$db getChip] getBlock]
# set tech [$db getTech]

#  set core [$block getCoreArea]
#  set core_xl [$core xMin]
#  set core_yl [$core yMin]
#  set core_xh [$core xMax]
#  set core_yh [$core yMax]

#  set div_cen_x [expr double(($core_xl + $core_xh) * 3 / 4 / 1000)]
#  set div_cen_y [expr double(($core_yl + $core_yh) / 2 / 1000)]

#  set div_cen [concat $div_cen_x $div_cen_y]

# set allInsts [$block getInsts]
# foreach inst $allInsts {
#   set master [$inst getMaster]
#   set name [$inst getName]
#   if {[string match "SIX" $name]} {
#     # puts $name
# 	place_cell -inst $name \
# 	-origin $div_cen \
# 	-orient R0
#   }
# }
# --------------------------
estimate_parasitics -placement
report_wns
report_tns
report_worst_slack
report_design_area

if {![info exists standalone] || $standalone} {
  write_def $::env(RESULTS_DIR)/3_1_place_gp.def
  exit
}
