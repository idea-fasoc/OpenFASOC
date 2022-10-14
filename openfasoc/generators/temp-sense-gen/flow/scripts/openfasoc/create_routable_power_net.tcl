# Create routable net from power net
#
# This procedure creates a net that will allow routing from instances that
# should connect to a power net other than the grid they're placed in.
#
# For example, in the temp-sense-gen this net allows routing from the HEADER
# cells to the VIN power ring, because connections to the regular VIN net
# aren't routed since it's a power net with a stdcell grid attached.
#
# Arguments:
# - source_net_name: name of the original power net
# - num_connection_points: number of connection points routed in the ring (optional)

proc create_routable_power_net {source_net_name {num_connection_points 1}} {
    set block [ord::get_db_block]
    set tech [ord::get_db_tech]

    # Get objects from source net
    set net [$block findNet $source_net_name]
    set bterm [$net getBTerms]
    set bpin [$bterm getBPins]

    # Create routable net in the database
    set r_pin "r_$source_net_name"
    set r_net [odb::dbNet_create $block $r_pin]

    if {$num_connection_points == 1} {
        # Create block terminal for routable net
        set r_bterm [odb::dbBTerm_create $r_net $r_pin]
        set r_bpin [odb::dbBPin_create $r_bterm]
        $r_bpin setPlacementStatus "FIRM"

        # Set to r_VIN the same physical box as that of VIN (its ring)
        foreach box [$bpin getBoxes] {
            set layer [$box getTechLayer] ;# get metal layer
            odb::dbBox_create $r_bpin $layer [$box xMin] [$box yMin] \
                [$box xMax] [$box yMax] ;# create physical box for net
        }
    } elseif {$num_connection_points > 1} {
        # Create num_connection_points block terminals
        for {set n 0} {$n < $num_connection_points} {incr n} {
            set r_bterm($n) [odb::dbBTerm_create $r_net "$r_pin\($n\)"]
            set r_bpin($n) [odb::dbBPin_create $r_bterm($n)]
            $r_bpin($n) setPlacementStatus "FIRM"

            # Split the source net's physical box into num_connection_points parts
            # and assign each part to a block terminal
            foreach box [$bpin getBoxes] {
                set layer [$box getTechLayer] ;# get metal layer

                # Get direction to divide physical box (horizontally or vertically)
                set first_box [lindex [$bpin getBoxes] 0]
                set direction [$first_box getDir]

                if {$direction == 1} {
                    # Divide net box horizontally
                    # Careful: the resulting coordinates must stick to the manufacturing grid
                    # hence the r2grid procedure (defined below)
                    set dx [r2grid [expr {([$box xMax] - [$box xMin])/$num_connection_points}] $tech]
                    set xMin($n) [expr {[$box xMin] + $n*$dx}]
                    set xMax($n) [expr {$xMin($n) + $dx}]

                    odb::dbBox_create $r_bpin($n) $layer $xMin($n) [$box yMin] \
                        $xMax($n) [$box yMax] ;# create physical box for net

                } elseif {$direction == 0} {
                    # Divide net box vertically
                    # Careful: the resulting coordinates must stick to the manufacturing grid
                    # hence the r2grid procedure (defined below)
                    set dy [r2grid [expr {([$box yMax] - [$box yMin])/$num_connection_points}] $tech]
                    set yMin($n) [expr {[$box yMin] + $n*$dy}]
                    set yMax($n) [expr {$yMin($n) + $dy}]

                    odb::dbBox_create $r_bpin($n) $layer [$box xMin] $yMin($n) \
                        [$box xMax] $yMax($n) ;# create physical box for net

                } else {
                    puts "WARNING: Could not determine power net pins orientation. \
                        Failed to create routable power net."
                }
            }
        }
    }


}

proc r2grid {number db_tech} {
    # This will round "number" to a value that respects the manufacturing grid
    # For example, if the manufacturing grid is 5 microns and number = 20333,
    # the procedure will output 20335.
    set grid [$db_tech getManufacturingGrid]
    return [expr {round($number / double($grid)) * $grid}]
}
