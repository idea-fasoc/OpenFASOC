// Top level for Spread spectrum PLL
// 1. Base PLL without the spread spectrum modulation first
// 2. Freq Lock loop WIP

module pll_ss(ref_clk, pll_outclk, reset);
    input wire ref_clk;
    output wire pll_outclk;
    input wire reset;

    // Wire Definitions
    wire divclk;
// Digital Freq Acquisition Loop
freq_loop fllinst(
    .reset(reset),
    .ref_clk(ref_clk),
    .dco_divclk(divclk),
    .ref_freq_cnt(),
    .dco_freq_cnt(),
    .fll_locked(),
    .freq_diff(),
    .floop_lock_range(),
    .freq_incr_decr(),
    .freq_update(),
    .freq_incr_decr()
);
    // DCO Analog Model
lc_dco lc_dco_inst(
    .sw(),
    .outp(),
    .outn(),
    .divclk(divclk),
    .Ibias()
);
endmodule : pll_ss

