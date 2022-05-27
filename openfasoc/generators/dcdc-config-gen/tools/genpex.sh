magic -rcfile ../../../common/drc-lvs-check/sky130A/sky130A.magicrc -noconsole -dnull
gds read $1
load $2
extract
ext2spice -o ./flow/spice/$2_netlist.spice
exit
EOF
