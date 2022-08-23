# change to ext/ directory because the extract command generates .ext files
# in the current directory
cd $OBJECTS_DIR/netgen_lvs/ext/

# generate lvs netlist using magic
magic -rcfile $COMMON_VERIF_DIR/sky130A/sky130A.magicrc -noconsole -dnull << EOF
gds read $1
load $2
# gds flatglob $2
# flatten $2_flat
# load $2_flat
# gds write ./FLATTEN_GDS/$2_flat.gds
# EOF
# magic -rcfile ./sky130A/sky130A.magicrc -noconsole -dnull << EOF
# gds read ./FLATTEN_GDS/$2_flat.gds
# load $2_flat
# flatten $2
# load $2
# gds write ./FLATTEN_GDS/$2.gds
# EOF
# magic -rcfile ./sky130A/sky130A.magicrc -noconsole -dnull << EOF
# gds read ./FLATTEN_GDS/$2.gds
# load $2
extract all
ext2spice lvs
# ext2spice merge aggressive
ext2spice -o ../spice/$2_lvsmag.spice
extract all
ext2spice lvs
ext2spice rthresh 0
ext2spice cthresh 0
ext2spice -o ../spice/$2_pex.spice
load $2
extract all
ext2spice cthresh 0
ext2spice -o ../spice/$2_sim.spice
exit
EOF

# Adapt the extracted spice file to account for errors in Magic
# Importantly, this script is specific in what it looks for,
# so is unlikely to break LVS if Magic improves in the future
# note that --toplevel is optional (specify if you have a top level subckt)
python $COMMON_VERIF_DIR/process_extracted.py --lvsmag $OBJECTS_DIR/netgen_lvs/spice/$2_lvsmag.spice --toplevel $2

# run lvs check using netgen
# netgen lvs $2_lvsmag.spice $2.spice $COMMON_VERIF_DIR/sky130A/sky130A_setup.tcl $3 -full
# Run netgen in batch mode
netgen -batch lvs "$OBJECTS_DIR/netgen_lvs/spice/$2_lvsmag.spice $2" "$OBJECTS_DIR/netgen_lvs/spice/$2.spice $2" $COMMON_VERIF_DIR/sky130A/sky130A_setup.tcl $3
