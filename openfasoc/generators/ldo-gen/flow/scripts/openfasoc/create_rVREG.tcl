# Create r_VREG net
#
# This net will allow routing from the standard cells to the VREG power ring,
# because connections to the regular VREG net aren't routed since it's
# a power net.

set block [ord::get_db_block]
set tech [ord::get_db_tech]

# Create the net in the database
set r_pin "r_VREG"
set r_net [odb::dbNet_create $block $r_pin]
set r_bterm [odb::dbBTerm_create $r_net $r_pin]
set r_bpin [odb::dbBPin_create $r_bterm]
$r_bpin setPlacementStatus "FIRM"

# Set to r_VREG the same physical box as that of VREG (it's grid)
set net [$block findNet "VREG"]
set bterm [$net getBTerms]
set bpin [$bterm getBPins]

foreach box [$bpin getBoxes] {
    set layer [$box getTechLayer] ;# get metal layer
    odb::dbBox_create $r_bpin $layer [$box xMin] [$box yMin] \
        [$box xMax] [$box yMax] ;# create physical box for net
}
