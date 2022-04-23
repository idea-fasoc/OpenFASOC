// Design: dcdcInst
// Description: Top-level verilog structure
// Author：Wanyue Xu
// Updated by: Tuohang Zeng, Jianwei Jia
// Last update: 02/08/22

module dcdcInst (
    inout VOUT,
    input clk,
	input VREF_in, //new added input
	input [5:0] sel_vh, sel_vl,
	input [1:0] s
);

    wire w_clk0, w_clk0b, w_clk1, w_clk1b;
	wire comp_out, clk_gate_out, FF_out, FF_out_inv;

/*
    DCDC_SIX_STAGES_CONV u_DCDC_SIX_STAGES_CONV(
		.VOUT(VOUT),
		.SEL_VH(sel_vh),
		.SEL_VL(sel_vl),
		.W_CLK0(w_clk0),
		.W_CLK0B(w_clk0b),
		.W_CLK1(w_clk1),
		.W_CLK1B(w_clk1b)
	);
	*/
	DCDC_SIX_STAGES_CONV u_DCDC_SIX_STAGES_CONV(
		.VOUT(VOUT),
		.sel_vh(sel_vh),
		.sel_vl(sel_vl),
		.w_clk0(FF_out),
		.w_clk0b(FF_out),
		.w_clk1(FF_out),
		.w_clk1b(FF_out)
	);

	/*   DCDC_NOV_CLKGEN #(.N_delay(7)) u_DCDC_NOV_CLKGEN (
        .clk_in(FF_out),
		.s (s), // two bits to select the dead time
        .clk0(w_clk0),
        .clk0b(w_clk0b),
        .clk1(w_clk1),
        .clk1b(w_clk1b)
    );
	*/

	// AUX CELL DCDC_COMP
	DCDC_COMP u_DCDC_COMP(
		.VIP(VREF_in),
		.VIN(VOUT),
		.CLK(clk),
		.VOP(comp_out)
	);

	// Clock Gate
	sky130_fd_sc_hs__dlclkp_1 u_DCDC_CLKGATE(
		.CLK(clk),
		.GATE(comp_out),
		.GCLK(clk_gate_out)
	);

	// Sync FF
	sky130_fd_sc_hs__dfxtp_1 u_DCDC_FF(
		.CLK(clk_gate_out), //check which input is clk
		.D(FF_out_inv),
		.Q(FF_out)
	);

	// Sync Inv
	sky130_fd_sc_hs__inv_1 u_DCDC_INVERTER(
		.A(FF_out),
		.Y(FF_out_inv)
	);
endmodule
