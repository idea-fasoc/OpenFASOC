////////////////////////////////////////////////////////////////
//Design unit: buffer
//
//File name: DCDC_BUFFER.sv
//
//Description: two inverter to construct one buffer
//
//Limitaions: Should be changed into different inv to control the delay time if needed
//
//
//Replacement fit: nb
//
//System: IEEE 1800-2017
//
//Author: Jianwei Jia
//
//Revison: Version 1.0 02/05/2022 
/////////////////////////////////////////////////////////////////

module DCDC_BUFFER(
    output logic out, input logic in
)
logic out1;

always_comb
begin
	sky130_fd_sc_hd__clkinv_1 u_DCDC_INVERTER1( 
		.A(in), 
		.Y(out1)
	);

	sky130_fd_sc_hd__clkinv_1 u_DCDC_INVERTER2( 
		.A(out1), 
		.Y(out)
	);
end

endmodule