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
	input [1:0] s,
	input non_clk_rst_n, //give a low-level voltage to reset seeds at the beginnnig
	input non_clk_control, //inject random noise all the time
	input [8:0] non_clk_seed //inject seeds of random noise at reset time
);

    wire w_clk0, w_clk0b, w_clk1, w_clk1b;
	wire comp_out, clk_gate_out, FF_out, FF_out_inv;
	wire [3:0] non_clk_dcde_noise_injection

	DCDC_SIX_STAGES_CONV u_DCDC_SIX_STAGES_CONV(
		.VOUT(VOUT),
		.sel_vh(sel_vh),
		.sel_vl(sel_vl),
		.w_clk0(w_clk0),
		.w_clk0b(w_clk0b),
		.w_clk1(w_clk1),
		.w_clk1b(w_clk1b)
	);

    DCDC_NOV_CLKGEN #(.N_delay(7)) u_DCDC_NOV_CLKGEN (
        .clk_in(FF_out),
		.s (non_clk_dcde_noise_injection[1:0]), // two bits to select the dead time
        .clk0(w_clk0),
        .clk0b(w_clk0b),
        .clk1(w_clk1),
        .clk1b(w_clk1b)
    );

	//DCDE_DIGITAL_NOISE_INJECTION
	DCDC_DIGITAL_NOISE_INJECTION u_DCDC_DIGITAL_NOISE_INJECTION(
		.CLK(clk),
		.rst_n(non_clk_rst_n),
		.control(non_clk_control),
		.seed(non_clk_seed),
		.Q(non_clk_dcde_noise_injection)
	);

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
