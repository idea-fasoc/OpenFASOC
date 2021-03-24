# echo "gds read $1
# load $2
# flatten drc_cell
# load drc_cell" > magic_commands.tcl

# run magic
magic -rcfile util/sky130A.magicrc magic_commands.tcl 
# -noconsole -dnull < /dev/null
