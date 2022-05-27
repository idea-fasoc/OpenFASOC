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

#place_pin -pin_name a["0"] -layer met3 -location {5 39} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name a["1"] -layer met3 -location {10 39} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name a["2"] -layer met3 -location {15 39} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name a["3"] -layer met3 -location {20 39} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name a["4"] -layer met3 -location {25 39} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name a["5"] -layer met3 -location {30 39} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name s["0"] -layer met3 -location {5 0} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name s["1"] -layer met3 -location {8 0} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name s["2"] -layer met3 -location {11 0} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name s["3"] -layer met3 -location {14 0} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name s["4"] -layer met3 -location {17 0} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name s["5"] -layer met3 -location {20 0} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name s["6"] -layer met3 -location {23 0} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name s["7"] -layer met3 -location {26 0} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name s["8"] -layer met3 -location {29 0} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name s["9"] -layer met3 -location {32 0} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name s["10"] -layer met3 -location {35 0} -pin_size {0.5 0.3} -force_to_die_boundary
#place_pin -pin_name s["11"] -layer met3 -location {38 0} -pin_size {0.5 0.3} -force_to_die_boundary
place_pins -hor_layer $::env(IO_PLACER_H) \
             -ver_layer $::env(IO_PLACER_V) \
             -random

if {![info exists standalone] || $standalone} {
  # write output
  write_def $::env(RESULTS_DIR)/2_2_floorplan_io.def
  exit
}
