utl::set_metrics_stage "globalplace__{}"
source $::env(SCRIPTS_DIR)/load.tcl
load_design 2_floorplan_ro.odb 2_floorplan.sdc "Starting global placement"

set_dont_use $::env(DONT_USE_CELLS)

# set fastroute layer reduction
if {[info exist env(FASTROUTE_TCL)]} {
  source $env(FASTROUTE_TCL)
} else {
  set_global_routing_layer_adjustment $env(MIN_ROUTING_LAYER)-$env(MAX_ROUTING_LAYER) 0.5
  set_routing_layers -signal $env(MIN_ROUTING_LAYER)-$env(MAX_ROUTING_LAYER)
  set_macro_extension 2
}
# check the lower boundary of the PLACE_DENSITY and add PLACE_DENSITY_LB_ADDON if it exists
if {[info exist ::env(PLACE_DENSITY_LB_ADDON)]} {
  set place_density_lb [gpl::get_global_placement_uniform_density \
  -pad_left $::env(CELL_PAD_IN_SITES_GLOBAL_PLACEMENT) \
  -pad_right $::env(CELL_PAD_IN_SITES_GLOBAL_PLACEMENT)]
  set place_density [expr $place_density_lb + ((1.0 - $place_density_lb) * $::env(PLACE_DENSITY_LB_ADDON)) + 0.01]
  if {$place_density > 1.0} {
    utl::error FLW 24 "Place density exceeds 1.0 (current PLACE_DENSITY_LB_ADDON = $::env(PLACE_DENSITY_LB_ADDON)). Please check if the value of PLACE_DENSITY_LB_ADDON is between 0 and 0.99."
  }
} else {
  set place_density $::env(PLACE_DENSITY)
}

# TEMPORARY FIX!!!! (sorry) ASSUME ROUTABILITY DRIVEN
set global_placement_args ""
append global_placement_args " -routability_driven"

if { 0 != [llength [array get ::env GLOBAL_PLACEMENT_ARGS]] } {
global_placement -density $place_density \
    -pad_left $::env(CELL_PAD_IN_SITES_GLOBAL_PLACEMENT) \
    -pad_right $::env(CELL_PAD_IN_SITES_GLOBAL_PLACEMENT) \
    {*}$global_placement_args \
    $::env(GLOBAL_PLACEMENT_ARGS)
} else {
global_placement -density $place_density \
    -pad_left $::env(CELL_PAD_IN_SITES_GLOBAL_PLACEMENT) \
    -pad_right $::env(CELL_PAD_IN_SITES_GLOBAL_PLACEMENT) \
    {*}$global_placement_args
}

# force divider to be placed on the right side
set db [::ord::get_db]
set block [[$db getChip] getBlock]
set tech [$db getTech]

set core [$block getCoreArea]
set core_xl [$core xMin]
set core_yl [$core yMin]
set core_xh [$core xMax]
set core_yh [$core yMax]

set div_cen_x [expr double(($core_xl + $core_xh) * 3 / 4 / 1000)]
set div_cen_y [expr double(($core_yl + $core_yh) / 2 / 1000)]

set div_cen [concat $div_cen_x $div_cen_y]

set allInsts [$block getInsts]

foreach inst $allInsts {
	set master [$inst getMaster]
	set name [$inst getName]
	if {[string match "_*_" $name]} {
		place_cell -inst $name \
		       	   -origin $div_cen \
		       	   -orient R0
	}
}
		      
		       			  
estimate_parasitics -placement

source $::env(SCRIPTS_DIR)/report_metrics.tcl
report_metrics "global place" false

if {![info exists save_checkpoint] || $save_checkpoint} {
  write_db $::env(RESULTS_DIR)/3_1_place_gp.odb
}
