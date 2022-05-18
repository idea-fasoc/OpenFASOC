// Design: DCDC_SIX_STAGES_CONV
// Description: 6 stages of 2:1 Converter Slice and Power Mux generation with parameters
// Author：Wanyue Xu
// Updated by: Tuohang Zeng
// Last update: 02/09/22

module DCDC_SIX_STAGES_CONV(
    output VOUT,
	input [5:0] sel_vh, sel_vl,
    input w_clk0, w_clk0b, w_clk1, w_clk1b
	);

    parameter DCDC_NUM_STAGE = 6;
    parameter DCDC_CAP_SIZE = 18;
    parameter DCDC_SW_SIZE = 8;
	parameter [(DCDC_NUM_STAGE*8)-1:0] DCDC_PWR_MUX_CONF = {8'd1,8'd1,8'd1,8'd1,8'd1,8'd2};

    assign VOUT = w_vint[DCDC_NUM_STAGE-1];

	wire [DCDC_NUM_STAGE-1:0] y0_top, y0_bot, y1_top, y1_bot;
	wire [DCDC_NUM_STAGE-1:0] vhigh, vlow;

	wire [DCDC_NUM_STAGE-1:0] w_vint;

	// generate stages with power mux, 2:1 slices, and caps
    genvar i, j;
    generate
        for(i=0; i<DCDC_NUM_STAGE; i=i+1) begin: gen_stage

			// Power mux generation (Configuration, defined by parameter, is stage dependent)
			if(!i) begin
			// AUX CELL DCDC_POWMUX
			DCDC_POWMUX #(.m(DCDC_PWR_MUX_CONF[(DCDC_NUM_STAGE*8)-i*8-1-:8])) u_DCDC_POWMUX (
				.vin(1'b0),
				.sel_vh(sel_vh[i]),
				.sel_vl(sel_vl[i]),
				.vhigh(vhigh[i]),
				.vlow(vlow[i])
			);
			end
			else begin
			// AUX CELL DCDC_POWMUX
			DCDC_POWMUX #(.m(DCDC_PWR_MUX_CONF[(DCDC_NUM_STAGE*8)-i*8-1-:8])) u_DCDC_POWMUX (
				.vin(w_vint[i-1]),
				.sel_vh(sel_vh[i]),
				.sel_vl(sel_vl[i]),
				.vhigh(vhigh[i]),
				.vlow(vlow[i])
			);
			end

			// 2:1 Conv stages generation
			for(j=0; (j==0)||(j<(DCDC_SW_SIZE>>(DCDC_NUM_STAGE-1-i))); j=j+1) begin: gen_conv
				DCDC_CONV2TO1 u_DCDC_CONV2TO1 (
					.VHIGH(vhigh[i]),
					.VLOW(vlow[i]),
					.VMID(w_vint[i]),
					.Y1_TOP(y1_top[i]),
					.Y0_TOP(y0_top[i]),
					.Y1_BOT(y1_bot[i]),
					.Y0_BOT(y0_bot[i]),
					.CLK0(w_clk0),
					.CLK0B(w_clk0b),
					.CLK1(w_clk1),
					.CLK1B(w_clk1b)
				);
            end

			// Flying cap generation
            for(j=0; (j==0)||(j<(DCDC_CAP_SIZE>>(DCDC_NUM_STAGE-1-i))); j=j+1) begin: gen_cap
                DCDC_CAP_UNIT u0_DCDC_CAP_UNIT (
                    .TOP(y0_top[i]),
                    .BOT(y0_bot[i])
                );

                DCDC_CAP_UNIT u1_DCDC_CAP_UNIT (
                    .TOP(y1_top[i]),
                    .BOT(y1_bot[i])
                );
            end
        end
    endgenerate
endmodule
