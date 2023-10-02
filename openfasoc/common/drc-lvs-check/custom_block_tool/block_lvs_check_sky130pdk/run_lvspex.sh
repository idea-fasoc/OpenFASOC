# generate lvs netlist using magic
magic -rcfile ./sky130A/sky130A.magicrc -noconsole -dnull << EOF
gds read $1
load $2
flatten $2_flat
load $2_flat
gds write ./FLATTEN_GDS/$2_flat.gds
EOF

magic -rcfile ./sky130A/sky130A.magicrc -noconsole -dnull << EOF
gds read ./FLATTEN_GDS/$2_flat.gds
load $2_flat
flatten $2
load $2
gds write ./FLATTEN_GDS/$2.gds
EOF

magic -rcfile ./sky130A/sky130A.magicrc -noconsole -dnull << EOF
gds read ./FLATTEN_GDS/$2.gds
load $2
extract all
ext2spice lvs
#ext2spice merge aggressive
ext2spice -o ./EXTRACT_CDL/$2_lvsmag.spice
extract all
ext2spice lvs

ext2spice cthresh 0
ext2spice -o ./EXTRACT_PEX/$2_pex.spice

load $2
extract all
ext2spice cthresh 0
ext2spice -o ./EXTRACT_SIM/$2_sim.spice
exit
EOF

# run lvs check using netgen in batch mode - for subckt check
netgen -batch lvs "./EXTRACT_CDL/$2_lvsmag.spice $2" "./ORIGINAL_CDL/$2.spice $2" ./sky130A/sky130A_setup.tcl $3

# run lvs - for top-level check
#netgen -batch lvs ./EXTRACT_CDL/$2_lvsmag.spice ./ORIGINAL_CDL/$2.spice ./sky130A/sky130A_setup.tcl $3
