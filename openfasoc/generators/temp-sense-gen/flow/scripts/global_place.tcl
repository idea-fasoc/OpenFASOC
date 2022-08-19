utl::set_metrics_stage "globalplace__{}"
source $::env(SCRIPTS_DIR)/load.tcl
load_design 3_2_place_iop.odb 2_floorplan.sdc "Starting global placement"

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

set global_placement_args ""
if {$::env(GPL_ROUTABILITY_DRIVEN)} {
    append global_placement_args " -routability_driven"
}
if {$::env(GPL_TIMING_DRIVEN)} {
    append global_placement_args " -timing_driven"
}


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

estimate_parasitics -placement

# openfasoc: fix for pdngen problem (issue #81)
# using pdn.cfg, the tracks are placed correctly, but temp_analog_0 instances
# have their VPWR pins associated to VDD (and not VIN) in the database
# (the output layout is right still, this just caused problems for LVS)
set block [ord::get_db_block]
set group [$block findGroup TEMP_ANALOG]
set net_vin [$block findNet VIN]
foreach inst [$group getInsts] {
  set pin_vpwr [$inst findITerm VPWR]
  set pin_vpb [$inst findITerm VPB]
  $pin_vpwr connect $net_vin
  $pin_vpb connect $net_vin
}

source $::env(SCRIPTS_DIR)/report_metrics.tcl
report_metrics "global place" false

if {![info exists save_checkpoint] || $save_checkpoint} {
  write_db $::env(RESULTS_DIR)/3_3_place_gp.odb
}
