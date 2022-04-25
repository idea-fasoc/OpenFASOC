// Top level for Spread spectrum PLL
// 1. Base PLL without the spread spectrum modulation first
// 2. Freq Lock loop WIP

module pll_ss();
    input ref_clk;
    output pll_outclk;

// Digital Freq Acquisition Loop
freq_loop fllinst(
    .reset(),
    .ref_clk(ref_clk),
    .dco_divclk(),
    .ref_freq_cnt(),
    .dco_freq_cnt(),
    .fll_locked(),
    .divcnt_diff(),
    .floop_lock_range(),
    .freq_update(),
    .freq_incr_decr()
);
    // DCO Analog Model
lc_dco lc_dco_inst(
    .sw(),
    .outp(),
    .outn(),
    .Ibias()
);
endmodule : pll_ss
