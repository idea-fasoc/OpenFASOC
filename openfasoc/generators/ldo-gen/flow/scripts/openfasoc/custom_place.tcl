# This will place the comparator latch (cmp1) correctly which will not cause LVS issues further in the flow. This is used before detail_placement.
set block [ord::get_db_block]
set inst [$block findInst cmp1]
set instName [$inst getName]

place_cell -inst_name $instName -orient MY -origin [list 170 40.700] -status PLACED
