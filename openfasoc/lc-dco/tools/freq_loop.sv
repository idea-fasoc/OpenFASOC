// Frequency locked loop



module freq_loop(reset, ref_clk, dco_divclk,ref_freq_cnt,dco_freq_cnt, fll_locked,
floop_lock_range,freq_update, freq_incr_decr,divcnt_diff);
    // Parameters
    parameter RefClkCnt = 10;
    parameter DivClkCnt = 10;
    input ref_clk, dco_divclk, reset;
    input ref_freq_cnt;
    input dco_freq_cnt;
    output fll_locked;
    input floop_lock_range; // +/-floop_lock_range
    output freq_update;
    output freq_incr_decr;
    output wire [DivClkCnt:0] divcnt_diff;
    // Registers
    reg [RefClkCnt-1:0] ref_cnt_reg;
    reg [DivClkCnt-1:0] div_cnt_reg;
    reg req, ack;
    reg [1:0] req_sync, ack_sync;
    reg [DivClkCnt-1:0] divclk_pipeline_reg, divclk_pipeline_reg_next;
    // Enumerated states
    //enum [Requested, Ackowledged, Idle] {currstate, nextstate} ;
    // Wires
    //wire [DivClkCnt-1:0] divcnt_diff;


    // Count reference clock cycles
    always @ (posedge ref_clk) begin
        if (reset || ack_sync) begin
            ref_cnt_reg <= {RefClkCnt}*1'b0;
            req <= 1'b0;
        end else if (ref_cnt_reg==ref_freq_cnt) begin
            req <= 1'b1;
            //ref_cnt_reg <= {RefClkCnt}*1'b0;
        end else begin
            if (!ack_sync) begin
                ref_cnt_reg <= ref_cnt_reg + 1'b1;
                req <=1'b0;
            end
        end
    end
    // 2 Bit Sync
    always @ (posedge ref_clk) begin
        if (reset) begin
            ack_sync <= 0;
        end else begin
            ack_sync <= {ack_sync[0],ack};
        end

    end

    // Count dco_div_clk cycles
    // 2 Bit Sync on request to generate acknowledge
    always @(posedge dco_divclk) begin
        if (reset) begin
            req_sync <= 0;
        end else begin
            req_sync <= {req_sync[0], req};
        end
    end

    always @ (posedge dco_divclk) begin
        if (reset) begin
            div_cnt_reg <= {DivClkCnt}*1'b0;
            ack <= 1'b0;
        end else if (div_cnt_reg==dco_freq_cnt) begin
            ack <= 1'b1;
            div_cnt_reg <= {DivClkCnt}*1'b0;
        end else if (req_sync[1]) begin
            divclk_pipeline_reg <= div_cnt_reg;
            divclk_pipeline_reg_next <= divclk_pipeline_reg;
        end else begin
            div_cnt_reg <= div_cnt_reg + 1'b1;
            ack <=1'b0;
        end
    end

    //Output Section
    assign divcnt_diff = (divclk_pipeline_reg_next - divclk_pipeline_reg);


endmodule : freq_loop
