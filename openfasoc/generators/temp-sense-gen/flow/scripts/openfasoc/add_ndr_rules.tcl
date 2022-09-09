set block [ord::get_db_block]

# Add 2W, 2S rule to ring oscillator input
create_ndr -name NDR_2W_2S \
           -spacing { li1 0.12 met1 0.06 met2 0.92 met3 1.36 met4 1.84 met5 6.8 } \
           -width { li1 0.17 met1 0.14 met2 0.28 met3 0.6 met4 0.6 met5 3.2}

set ndr [$block findNonDefaultRule NDR_2W_2S]
$ndr setHardSpacing 1

assign_ndr -ndr NDR_2W_2S -net r_VIN
