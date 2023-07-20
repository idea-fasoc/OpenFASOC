#!/bin/bash
#export PDK_ROOT=/usr/local/share/pdk/
export PDK_ROOT=/usr/bin/miniconda3/share/pdk/

# generate lvs netlist using magic
magic -rcfile ./sky130A/sky130A.magicrc -noconsole -dnull << EOF
gds read $1
load $2
flatten $2_flat
load $2_flat
gds write $2_flat.gds
EOF

magic -rcfile ./sky130A/sky130A.magicrc -noconsole -dnull << EOF
gds read $2_flat.gds
load $2_flat
flatten $2
load $2
gds write $2.gds
EOF


magic -rcfile ./sky130A/sky130A.magicrc -noconsole -dnull << EOF
gds read $2.gds
load $2
extract all
ext2spice lvs
ext2spice merge aggressive
ext2spice cthresh 0
ext2spice rthresh 0
ext2spice -o $2_pex.spice
exit
EOF

magic -rcfile ./sky130A/sky130A.magicrc -noconsole -dnull << EOF
gds read $2.gds
load $2
extract all
ext2spice merge aggressive
ext2spice -o $2_pex.spice
exit
EOF

rm -f $2_flat.gds
rm -f $2.ext
