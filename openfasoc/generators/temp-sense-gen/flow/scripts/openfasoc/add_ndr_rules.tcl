set block [ord::get_db_block]

# Add 2W, 2S rule to ring oscillator input
create_ndr -name NDR_5W_5S \
           -spacing { *5 } \
           -width { *5 }

set ndr [$block findNonDefaultRule NDR_5W_5S]
$ndr setHardSpacing 1

assign_ndr -ndr NDR_5W_5S -net r_VIN
