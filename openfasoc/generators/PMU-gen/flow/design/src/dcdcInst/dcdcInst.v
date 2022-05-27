// Design: dcdcInst
// Description: Top-level verilog structure
// Author：Wanyue Xu
// Updated by: Tuohang Zeng, Jianwei Jia
// Last update: 02/08/22

module dcdcInst(
    inout VOUT,
    input clk,
	input DAC_VREF,
	input DAC_RST,
	input [5:0] D,
	input [5:0] config_in,
	input non_clk_rst_n, //give a low-level voltage to reset seeds at the beginnnig
	input non_clk_control, //inject random noise all the time
	input [8:0] non_clk_seed //inject seeds of random noise at reset time
);

    wire w_clk0, w_clk0b, w_clk1, w_clk1b;
	wire comp_out, clk_gate_out, FF_out, FF_out_inv;
    wire [5:0] sel_vh, sel_vl;
	wire VREF_in;

    dcdc_config u_dcdc_config(
        .a(config_in),
        .s({sel_vh,sel_vl})
    );//need change

	six_stage_conv u_DCDC_SIX_STAGES_CONV(
		.VOUT(VOUT),
		.sel_vh(sel_vh),
		.sel_vl(sel_vl),
		.w_clk0(w_clk0),
		.w_clk0b(w_clk0b),
		.w_clk1(w_clk1),
		.w_clk1b(w_clk1b)
	);

	//NON_CLK_GEN
	NON_CLK_GEN u_NON_CLK_GEN(
		.clk(clk),
		.clk_in(FF_out),
		.rst_n(non_clk_rst_n),
		.control(non_clk_control),
		.seed(non_clk_seed),
		.clk0(w_clk0),
		.clk0b(w_clk0b),
		.clk1(w_clk1),
		.clk1b(w_clk1b)
	);

	// AUX CELL DCDC_COMP
	DCDC_COMP u_DCDC_COMP(
		.VIP(VREF_in),
		.VIN(VOUT),
		.CLK(clk),
		.VOP(comp_out)
	);

	// DCDC_DAC
	DCDC_DAC u_DCDC_DAC(
		.D0(D[0]), .D1(D[1]), .D2(D[2]), .D3(D[3]), .D4(D[4]), .D5(D[5]),
		.RST(DAC_RST),
		.REF(DAC_VREF),
		.VOUT(VREF_in)
	);

	// Clock Gate
	sky130_fd_sc_hd__dlclkp_1 u_DCDC_CLKGATE(
		.CLK(clk),
		.GATE(comp_out),
		.GCLK(clk_gate_out)
	);

	// Sync FF
	sky130_fd_sc_hd__dfxtp_1 u_DCDC_FF(
		.CLK(clk_gate_out), //check which input is clk
		.D(FF_out_inv),
		.Q(FF_out)
	);

	// Sync Inv
	sky130_fd_sc_hd__inv_1 u_DCDC_INVERTER(
		.A(FF_out),
		.Y(FF_out_inv)
	);
endmodule
