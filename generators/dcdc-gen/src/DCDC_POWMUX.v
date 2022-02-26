// Design: DCDC_POWMUX
// Description: Instantiates two 2:1 Power Muxes into 4:2 Power Mux
// Author：Tuohang Zeng
// Updated by:
// Last update: 02/09/22

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
	
	// power mux t-gate
	DCDC_MUX_TGATE pmux_hi_rail [m-1:0] (.VIN(1'b1), .SEL_INV(sel_vh_inv), .SEL(sel_vh), .VOUT(vhigh));
	DCDC_MUX_TGATE pmux_hi [m-1:0] (.VIN(vin), .SEL_INV(sel_vh), .SEL(sel_vh_inv), .VOUT(vhigh));
	
	DCDC_MUX_TGATE pmux_lo [m-1:0] (.VIN(vin), .SEL_INV(sel_vl_inv), .SEL(sel_vl), .VOUT(vlow));
	DCDC_MUX_TGATE pmux_lo_rail [m-1:0] (.VIN(1'b0), .SEL_INV(sel_vl), .SEL(sel_vl_inv), .VOUT(vlow));
	
	// inverters
	sky130_fd_sc_hd__inv_1 inv0 [1:0] (.A({sel_vh, sel_vl}), .Y({sel_vh_inv, sel_vl_inv}));	

endmodule 