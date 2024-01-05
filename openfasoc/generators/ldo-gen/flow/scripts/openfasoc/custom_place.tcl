# This will place all the PT_UNIT_CELL in uniform fashion as well as the comparator latch (cmp1) correctly.This is used before detail_placement.
proc place_pt_unit {instances_list place_limit} {
  set block [ord::get_db_block]
  set units [$block getDefUnits]
  set inst [$block findInst cmp1]
  set instName [$inst getName]
  place_cell -inst_name $instName -orient MY -origin [list 66.72 40.000] -status PLACED
  set place_limit [expr $place_limit-5]
  set x_R1 [expr 0 + 48.480]
  set y_R1 [expr 0 + 48.840]
  set x_R2 [expr 0 + 62.880]
  set y_R2 [expr 0 + 44.770]
  set x_R3 [expr 0 + 62.880]
  set y_R3 [expr 0 + 40.700]
  set ch [open $instances_list]
  while {![eof $ch]} {
    set line [gets $ch]
    if {[llength $line] == 0} {continue}
    set instname [lindex $line 1]
    set pt [ $block findInst $instname]
    set orient [$pt getOrient]

    if {$orient == "R0" && $x_R1<$place_limit} {
      place_cell -inst_name [lindex $line 0] -orient R0 -origin [list $x_R1 $y_R1] -status PLACED
      set x_R1 [expr $x_R1 + 2.40]
    } elseif { $orient == "R0" && $x_R2<$place_limit} {
     place_cell -inst_name [lindex $line 0] -orient R0 -origin [list $x_R2 $y_R2] -status PLACED
     set x_R2 [expr $x_R2 + 2.40]
     } else {
       place_cell -inst_name [lindex $line 0] -orient R0 -origin [list $x_R3 $y_R3] -status PLACED
       set x_R3 [expr $x_R3 + 2.40]
      }
  }
  close $ch
  }
