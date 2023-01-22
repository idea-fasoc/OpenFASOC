source $::env(SCRIPTS_DIR)/load.tcl
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

  # Read def
  read_def $::env(RESULTS_DIR)/2_floorplan_ro.def
} else {
  puts "No DEF File?"
}

write_db $::env(RESULTS_DIR)/2_floorplan_ro.odb
puts "ODB file written to $::env(RESULTS_DIR)"