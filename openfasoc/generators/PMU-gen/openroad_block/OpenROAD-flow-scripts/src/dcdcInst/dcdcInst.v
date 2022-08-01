// Design: dcdcInst
// Description: Top-level verilog structure
// Author：Wanyue Xu
// Updated by: Tuohang Zeng, Jianwei Jia
// Last update: 02/08/22

module dcdcInst(
    input clk,
	input clk_noise, //Pseudo-TRNG clk
	input non_clk_rst_n, //give a low-level voltage to reset seeds at the beginnnig
	input non_clk_control, //inject random noise all the time
	input [3:0] noise_D, //inject noise to the Vref
	input Noise_in,
	input DAC_RST, // reset the DAC
	input [5:0] D,
	input [5:0] config_in,
	input VREF_in,
	output VREF_out,
	output VOUT
);

    wire w_clk0, w_clk0b, w_clk1, w_clk1b;
	wire comp_out, clk_gate_out, FF_out, FF_out_inv;
    wire [5:0] sel_vh, sel_vl;

	//dcdc_config
    dcdc_config u_dcdc_config(
        .a(config_in),
        .s({sel_vh[5],sel_vl[5],sel_vh[4],sel_vl[4],sel_vh[3],sel_vl[3],sel_vh[2],sel_vl[2],sel_vh[1],sel_vl[1],sel_vh[0],sel_vl[0]})
    );

	six_stage_conv u_DCDC_SIX_STAGES_CONV(
		.VOUT(VOUT),
		.SEL_H(sel_vh),
		.SEL_L(sel_vl),
		.clk0(w_clk0),
		.clk0b(w_clk0b),
		.clk1(w_clk1),
		.clk1b(w_clk1b)
	);

	//NON_CLK_GEN
	NON_CLK_GEN u_NON_CLK_GEN(
		.clk(clk_noise),
		.clk_in(FF_out),
		.rst_n(non_clk_rst_n),
		.control(non_clk_control),
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
		.VOUT(VREF_out)
	);
	//NOISE_INJECTION
	NOISE_INJECTION u_NOISE_INJECTION(
		.D(noise_D),
		.Noise_in(Noise_in),
		.bias_out(VREF_in) //add noise to the Vref
	);

	// Clock Gate
	DCDC_CLKGATE u_DCDC_CLKGATE(
		.CLK(clk),
		.GATE(comp_out),
		.GCLK(clk_gate_out)
	);

	// Sync FF
	DCDC_FF u_DCDC_FF(
		.CLK(clk_gate_out), //check which input is clk
		.D(FF_out_inv),
		.Q(FF_out)
	);

	// Sync Inv
	DCDC_INVERTER u_DCDC_INVERTER(
		.A(FF_out),
		.Y(FF_out_inv)
	);
endmodule
