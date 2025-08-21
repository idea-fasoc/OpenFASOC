#!/bin/bash

# Usage: ./run_pex.sh layout.gds layout_cell_name

GDS_FILE=$1
LAYOUT_CELL=$2

# Use the PDK_ROOT environment variable to find the correct magicrc file
MAGICRC_PATH="$PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc"

magic -rcfile "$MAGICRC_PATH" -noconsole -dnull << EOF
gds read $GDS_FILE
flatten $LAYOUT_CELL
load $LAYOUT_CELL
select top cell
extract do local
extract all
ext2sim labels on
ext2sim
extresist tolerance 10
extresist
ext2spice lvs
ext2spice cthresh 0
ext2spice extresist on
ext2spice -o ${LAYOUT_CELL}_pex.spice
exit
EOF