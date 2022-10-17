# Create r_VIN net
#
# This net will allow routing from the HEADER cells to the VIN power ring,
# because connections to the regular VIN net aren't routed since it's
# a power net with a stdcell grid attached.

set block [ord::get_db_block]

# Create the net in the database
set r_pin "r_VIN"
set r_net [odb::dbNet_create $block $r_pin]
set r_bterm [odb::dbBTerm_create $r_net $r_pin]
set r_bpin [odb::dbBPin_create $r_bterm]
$r_bpin setPlacementStatus "FIRM"

# Set to r_VIN the same physical box as that of VIN (it's grid)
set net [$block findNet "VIN"]
set bterm [$net getBTerms]
set bpin [$bterm getBPins]

foreach box [$bpin getBoxes] {
    set layer [$box getTechLayer] ;# get metal layer
    odb::dbBox_create $r_bpin $layer [$box xMin] [$box yMin] \
        [$box xMax] [$box yMax] ;# create physical box for net
}
