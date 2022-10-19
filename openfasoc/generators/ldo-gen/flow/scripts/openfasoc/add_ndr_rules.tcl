set db [ord::get_db]
set block [ord::get_db_block]

# Add 2W, 2S rule to ring oscillator input
create_ndr -name NDR_3W_3S \
           -spacing { li1 0.51 met1 0.42 met2 0.42 met3 0.9 met4 0.9 met5 4.8 } \
           -width   { li1 0.51 met1 0.42 met2 0.42 met3 0.9 met4 0.9 met5 4.8 }

set ndr [$block findNonDefaultRule NDR_3W_3S]
$ndr setHardSpacing 1


assign_ndr -ndr NDR_3W_3S -net VREF
assign_ndr -ndr NDR_3W_3S -net r_VREG
