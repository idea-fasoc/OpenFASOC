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
  read_def $::env(RESULTS_DIR)/2_1_floorplan.def
} else {
  puts "Starting IO placement"
}

place_pin -pin_name EBL -layer met3 -location {0 5} -pin_size {0.5 0.3} -force_to_die_boundary

place_pin -pin_name OUT -layer met3 -location {160 5} -pin_size {0.5 0.3} -force_to_die_boundary

#  place_pins -hor_layer $::env(IO_PLACER_H) \
             -ver_layer $::env(IO_PLACER_V) \
             -random

if {![info exists standalone] || $standalone} {
  # write output
  write_def $::env(RESULTS_DIR)/2_2_floorplan_io.def
  exit
}
