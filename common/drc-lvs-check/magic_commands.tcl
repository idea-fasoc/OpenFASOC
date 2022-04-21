# gds read ./results/sky130hd/tempsense/6_final.gds
# load tempsenseInst
# flatten drc_cell
# load drc_cell


# if { [info exists ::env(TECH)] } {
#   tech load $::env(TECH)
# }

gds read $::env(RESULTS_DIR)/6_final.gds
proc custom_drc_save_report {{cellname ""} {outfile ""}} {

    if {$outfile == ""} {set outfile "drc.out"}

    set fout [open $outfile w]
    set oscale [cif scale out]

    if {$cellname == ""} {
        select top cell
        set cellname [cellname list self]
        set origname ""
    } else {
        set origname [cellname list self]
        puts stdout "\[INFO\]: Loading $cellname\n"
        flush stdout

        load $cellname
        select top cell
    }

    drc check
    set count [drc list count]

    puts $fout "$cellname count: $count"
    puts $fout "----------------------------------------"
    set drcresult [drc listall why]
    foreach {errtype coordlist} $drcresult {
        puts $fout $errtype
        puts $fout "----------------------------------------"
        foreach coord $coordlist {
            set bllx [expr {$oscale * [lindex $coord 0]}]
            set blly [expr {$oscale * [lindex $coord 1]}]
            set burx [expr {$oscale * [lindex $coord 2]}]
            set bury [expr {$oscale * [lindex $coord 3]}]
            set coords [format " %.3fum %.3fum %.3fum %.3fum" $bllx $blly $burx $bury]
            puts $fout "$coords"
        }
    puts $fout "----------------------------------------"
    }
    puts $fout ""

    if {$origname != ""} {
        load $origname
    }

    close $fout
    puts "\[INFO\]: DONE with $outfile\n"
}

custom_drc_save_report $::env(DESIGN_NAME) $::env(REPORTS_DIR)/6_final_drc.rpt
