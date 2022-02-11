// Design: DCDC_BUFFER
// Description: Buffers used in non-overlapping clock generation
// Author：Jianwei Jia
// Updated by: 
// Last update: 02/05/22

module DCDC_BUFFER(
    output logic out, input logic in
)
logic out1;

always_comb
begin
@@ 	@nb u_DCDC_INVERTER1( 
		.A(in), 
		.Y(out1)
	);

@@ 	@nc u_DCDC_INVERTER2( 
		.A(out1), 
		.Y(out)
	);
end

endmodule