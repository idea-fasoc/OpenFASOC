# generate lvs netlist using magic
magic -rcfile $MAGIC_SETUPS/sky130A.magicrc -noconsole -dnull << EOF
gds read $1
load $2
flatten -nolabels $2_flat
load $2_flat
extract all
ext2spice lvs
ext2spice -o $2_lvsmag.spice
ext2spice lvs
ext2spice cthresh 0
ext2spice -o $2_pex.spice
exit
EOF

# run lvs check using netgen
netgen lvs $2_lvsmag.spice $2.spice $MAGIC_SETUPS/netgen_sky130A_setup.tcl $3 -full
