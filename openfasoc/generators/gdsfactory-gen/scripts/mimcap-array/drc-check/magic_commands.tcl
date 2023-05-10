# gds read ./results/sky130hd/tempsense/6_final.gds
# load tempsenseInst
# flatten drc_cell
# load drc_cell


# if { [info exists ::env(TECH)] } {
#   tech load $::env(TECH)
# }

# gds flatglob commands removes the drc errors caused by hierarchy that magic can't process.
# gds faltglob *capacitor_test_nf* is specific to ldo-gen
gds flatglob *$$*
gds flatglob *VIA*
gds flatglob *CDNS*
gds flatglob *capacitor_test_nf*
gds ordering on

gds read ./result_dir/mimcap-array/merged_70_71_cap_array.gds
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

custom_drc_save_report "create_Cstructure" ./result_dir/mimcap-array/merged_70_71_cap_array_drc.rpt
