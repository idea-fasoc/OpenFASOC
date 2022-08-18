// Frequency locked loop



module freq_loop(reset, ref_clk, dco_divclk,ref_freq_cnt,dco_freq_cnt, fll_locked,
floop_lock_range,freq_update, freq_incr_decr,freq_diff);
    // Parameters
    parameter RefClkCnt = 10;
    parameter DivClkCnt = 10;
    parameter DivDiffCnt = 5;
    localparam CntRatio = RefClkCnt/DivClkCnt;
    input ref_clk, dco_divclk, reset;
    input ref_freq_cnt;
    input dco_freq_cnt;
    output fll_locked;
    input floop_lock_range; // +/-floop_lock_range
    output freq_update;
    output freq_incr_decr;
    output wire [DivClkCnt:0] freq_diff;
    // Registers
    reg [RefClkCnt-1:0] ref_cnt_reg;
    reg [DivClkCnt-1:0] div_cnt_reg;
    reg req, ack;
    reg [1:0] req_sync, ack_sync;
    reg [DivClkCnt-1:0] divclk_pipeline_reg, divclk_pipeline_reg_next;
    reg
    // Enumerated states
    //enum [Requested, Ackowledged, Idle] {currstate, nextstate} ;
    // Wires
    wire [DivDiffCnt-1:0] divcnt_diff;

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
    always @(posedge dco_divclk or negedge reset) begin
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

    // Output Section
    // Freq change
    assign freq_diff = ($signed(divclk_pipeline_reg_next) - $signed(divclk_pipeline_reg));
    if (freq_diff < 0) begin
        assign freq_incr_decr = 1;
        end
    else begin
        assign freq_incr_decr = 0;
    end
    //Absolute Freq Difference

    // Locked Status
    // If the freq_diff is within the  freq_lock_range

endmodule : freq_loop

