// Design: DCDC_POWMUX
// Description: Instantiates two 2:1 Power Muxes into 4:2 Power Mux
// Author：Tuohang Zeng
// Updated by:
// Last update: 02/09/22

module DCDC_POWMUX (
	inout VDD,
	inout VSS,
	input vin,
	input sel_vh,
	input sel_vl,
	output vhigh,
	output vlow
);
	// device multiplier
	parameter m = 1;
	
	// power mux t-gate
	DCDC_MUX_TGATE pmux_hi [m-1:0] (.VIN(vin), .SEL_INV(sel_vh_inv), .SLE(sel_vh), .VDD(VDD), .VSS(VSS), .VOUT(vhigh));
	DCDC_MUX_TGATE pmux_lo [m-1:0] (.VIN(vin), .SEL_INV(sel_vl_inv), .SLE(sel_vl), .VDD(VDD), .VSS(VSS), .VOUT(vlow));
	
	// inverters
@@ 	@na inv0 [1:0] (.A({sel_vh, sel_vl}), .Y({sel_vh_inv, sel_vl_inv}));	

endmodule 