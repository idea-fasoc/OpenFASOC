# Create r_VREG net
#
# This net will allow routing from the standard cells to the VREG power ring,
# because connections to the regular VREG net aren't routed since it's
# a power net.

set block [ord::get_db_block]

# Create the net in the database
set r_pin "r_VREG"
puts vreg_set
set r_net [odb::dbNet_create $block $r_pin]
puts vreg_created
set r_bterm [odb::dbBTerm_create $r_net $r_pin]
puts vregterm_created
set r_bpin [odb::dbBPin_create $r_bterm]
puts vregpin_created
$r_bpin setPlacementStatus "FIRM"

# Set to r_VREG the same physical box as that of VREG (it's grid)
set net [$block findNet "VREG"]
puts found_vreg
set bterm [$net getBTerms]
puts got_bterms
set bpin [$bterm getBPins]
puts got_pins

foreach box [$bpin getBoxes] {
    set layer [$box getTechLayer] ;# get metal layer
    odb::dbBox_create $r_bpin $layer [$box xMin] [$box yMin] \
        [$box xMax] [$box yMax] ;# create physical box for net
}

