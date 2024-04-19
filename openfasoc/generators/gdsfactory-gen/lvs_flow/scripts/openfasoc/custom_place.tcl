# Template procedure which will place cells in the large voltage domain off east
# with name "cell_name" semi-stacked starting from row "row_num" (0 indexed)
# No error checking is used, so you must ensure the target row and block object are correct
#
# The "isfixed" argument indicates whether the instances should be placed as FIRM
# (won't move in detailed_placement) or as PLACED (moves slightly in detailed_placement
# to avoid DRC errors).
#
# Example of usage (after global_placement but before detailed_placement):
#
# source $::env(SCRIPTS_DIR)/openfasoc/custom_place.tcl
# set block [ord::get_db_block]
# customPlace_east $block "HEADER" 10 no

proc customPlace_east {block_object cell_name row_num isfixed} {
	set target_row [lindex [$block_object getRows] $row_num]
	set y_initial_row [expr {[lindex [$target_row getOrigin] 1] / 1000.0}]
	set row_ydim [expr {[[$target_row getSite] getHeight] / 1000.0}]
	set status [expr {$isfixed ? "FIRM" : "PLACED"}]

	foreach inst [$block_object getInsts] {
		if {[[$inst getMaster] getName] == $cell_name} {
			set row_orient [$target_row getOrient]
			if {$row_orient eq "R0"} {
				# if row orientation is R0 (VDD above row, GND below)
				place_cell -cell $cell_name -inst_name [$inst getName] -origin [list 82.8 $y_initial_row] -orient R0 -status $status
			} elseif {$row_orient eq "MX"} {
				# if row orientation is MX (VDD below row, GND above)
				place_cell -cell $cell_name -inst_name [$inst getName] -origin [list 82.8 [expr $y_initial_row + $row_ydim]] -orient MX -status $status
			}

			incr row_num
			set target_row [lindex [$block_object getRows] $row_num]
			set y_initial_row [expr {[lindex [$target_row getOrigin] 1] / 1000.0}]
		}
	}
}
