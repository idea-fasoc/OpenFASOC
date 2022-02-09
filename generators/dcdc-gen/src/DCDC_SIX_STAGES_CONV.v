module DCDC_SIX_STAGES_CONV(
    inout VDD,
    inout VSS,
    inout AVDD,
    inout GND,
    inout VOUT,
	input [5:0] sel_vh, sel_vl,
    input w_clk0, w_clk0b, w_clk1, w_clk1b
	);
	
    parameter DCDC_NUM_STAGE = 6;
    parameter DCDC_CAP_SIZE = 62;
    parameter DCDC_SW_SIZE = 194;
	parameter DCDC_PWR_MUX_SIZE = 24;
	
    assign VOUT = w_vint[DCDC_NUM_STAGE-1];
	wire [DCDC_NUM_STAGE-1:0] y0_top, y0_bot, y1_top, y1_bot;
	wire vhigh, vlow;
	
	wire [DCDC_NUM_STAGE-1:0] w_vint;
	
	// generate stages with power mux, 2:1 slices, and caps
    genvar i, j;  
    generate
        for(i=0; i<DCDC_NUM_STAGE; i=i+1) begin: gen_stage
            for(j=0; (j==0)||(j<(DCDC_SW_SIZE>>(DCDC_NUM_STAGE-1-i))); j=j+1) begin: gen_pow_mux
				if(!i) begin
				// AUX CELL DCDC_POWMUX
				DCDC_POWMUX u_DCDC_POWMUX (
					.VDD(VDD),
					.VSS(VSS),
					.AVDD(AVDD),
					.GND(GND),
					.vin(GND),
					.sel_vh(sel_vh[i]),
					.sel_vl(sel_vl[i]),
					.vhigh(vhigh),
					.vlow(vlow)
				);		
				end
				else begin
				// AUX CELL DCDC_POWMUX
				DCDC_POWMUX u_DCDC_POWMUX (
					.VDD(VDD),
					.VSS(VSS),
					.AVDD(AVDD),
					.GND(GND),
					.vin(w_vint[i-1]),
					.sel_vh(sel_vh[i]),
					.sel_vl(sel_vl[i]),
					.vhigh(vhigh),
					.vlow(vlow)
				);		
				end
			end
			
			for(j=0; (j==0)||(j<(DCDC_SW_SIZE>>(DCDC_NUM_STAGE-1-i))); j=j+1) begin: gen_conv
				DCDC_CONV2TO1 u_DCDC_CONV2TO1 (
					.VDD(VDD),
					.VSS(VSS),
					.vhigh(vhigh),
					.vlow(vlow),
					.vmid(w_vint[i]),
					.y1_top(y1_top[i]),
					.y0_top(y0_top[i]),
					.y1_bot(y1_bot[i]),
					.y0_bot(y0_bot[i]),
					.clk0(w_clk0),
					.clk0b(w_clk0b),
					.clk1(w_clk1),
					.clk1b(w_clk1b)
				);
            end

            for(j=0; (j==0)||(j<(DCDC_CAP_SIZE>>(DCDC_NUM_STAGE-1-i))); j=j+1) begin: gen_cap
                DCDC_CAP_UNIT u0_DCDC_CAP_UNIT (
                    .top(y0_top[i]),
                    .bot(y0_bot[i])
                );

                DCDC_CAP_UNIT u1_DCDC_CAP_UNIT (
                    .top(y1_top[i]),
                    .bot(y1_bot[i])
                );
            end
        end
    endgenerate
endmodule
