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

	//wire sel_vh_inv, sel_vl_inv;

	// power mux
	genvar i;
	generate
        for(i=0; i<m; i=i+1) begin: gen_powmux

		DCDC_MUX powmux (.SEL_H(sel_vh), .SEL_L(sel_vl), .VIN(vin), .VOUT_H(vhigh), .VOUT_L(vlow));
		end
	endgenerate

	// inverters
//@@ 	@na inv1 [m-1:0] (.A({m{sel_vh}}), .Y({m{sel_vh_inv}}));
//@@ 	@nb inv0 [m-1:0] (.A({m{sel_vl}}), .Y({m{sel_vl_inv}}));

endmodule
