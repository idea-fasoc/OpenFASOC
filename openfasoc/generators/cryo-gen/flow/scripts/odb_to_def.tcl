source $::env(SCRIPTS_DIR)/load.tcl
load_design 2_floorplan.odb 2_floorplan.sdc "Starting file transposition"

write_def $::env(RESULTS_DIR)/2_floorplan.def
puts "DEF file written to $::env(RESULTS_DIR)"
