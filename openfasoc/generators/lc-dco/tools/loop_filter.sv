// Loop Filter Top level

module loop_filter(freq_incr_decr, freq_gain_adj, phase_adj, phase_updn, dco_outval);
    parameter FreqGainWidth = 5;
    parameter PhaseGainWidth = 5;
    parameter DCOWidth = 1;
    parameter FilterWidth = 8;
    //
    input freq_incr_decr;
    input [FreqGainWidth-1:0] freq_gain_adj;
    input [PhaseGainWidth-1:0] phase_gain_adj;
    input phase_updn;
    input filter_clock;
    output [DCOWidth-1:0] dco_outval;

    // Registers
    reg [FilterWidth-1:0]filter_reg;
    // Loop Filter

    always @ (posedge filter_clock or negedge reset) begin
        if (reset) begin
            filter_reg <= 0;
        end
        else begin
            if (freq_incr_decr) begin
                filter_reg <= filter_reg + freq_gain_adj;
            end else begin
                filter_reg <= filter_reg - freq_gain_adj;
            end
        end
    end

endmodule : loop_filter
