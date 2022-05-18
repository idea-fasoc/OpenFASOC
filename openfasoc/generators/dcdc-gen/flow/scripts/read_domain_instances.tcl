proc read_domain_instances {voltage_domain_name instances_list} {
  set block [ord::get_db_block]
  set units [$block getDefUnits]

  set ch [open $instances_list]

  set domain_region [$block findRegion $voltage_domain_name]

  while {![eof $ch]} {
    set line [gets $ch]
    if {[llength $line] == 0} {continue}

    set inst_name [lindex $line 0]
    $domain_region addInst [$block findInst $inst_name]
  }

  close $ch
}
