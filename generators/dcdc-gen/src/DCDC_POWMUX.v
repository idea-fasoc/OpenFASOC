// Design: DCDC_POWMUX
// Description: Instantiates two 2:1 Power Muxes into 4:2 Power Mux
// Author：Tuohang Zeng
// Updated by:
// Last update: 03/10/2022

module DCDC_POWMUX (
	inout vin,
	input sel_vh,
	input sel_vl,
	output vhigh,
	output vlow
);
	// device multiplier
	parameter m = 1;
	
	wire sel_vh_inv, sel_vl_inv;
	
	// power mux
	DCDC_MUX dcdc0 [m-1:0] (.SEL_H(sel_vh), .SEL_INV_H(sel_vh_inv), .SEL_L(sel_vl), .SEL_INV_L(sel_vl_inv), .VIN(vin), .VOUT_H(vhigh), .VOUT_L(vlow));
	
	// inverters
	sky130_fd_sc_hd__inv_4 inv0 [1:0] (.A({sel_vh, sel_vl}), .Y({sel_vh_inv, sel_vl_inv}));	

endmodule 