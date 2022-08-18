proc create_custom_connections {file_name} {
  set block [ord::get_db_block]
  set units [$block getDefUnits]

  set ch [open $file_name]

  set line [gets $ch]
  set net [$block findNet [lindex $line 0]]

  while {![eof $ch]} {
    set line [gets $ch]
    if {[llength $line] == 0} {break}

    set inst [$block findInst [lindex $line 0]]
    set iterm [$inst findITerm [lindex $line 1]]

    if {[ catch {odb::dbITerm_connect $iterm $net} ]} {
      puts "Cannot create custom connection on: "
      puts "instance name: [$inst getName]"
      puts "MTerm name: [[$iterm getMTerm] getName]"
    }

  }

  close $ch

}
