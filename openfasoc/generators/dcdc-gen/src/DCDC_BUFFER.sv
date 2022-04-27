// Design: DCDC_BUFFER
// Description: Buffers used in non-overlapping clock generation
// Author：Jianwei Jia
// Updated by: Tuohang Zeng
// Last update: 02/13/22

module DCDC_BUFFER(
    output logic out, input logic in
);
logic out1;

	sky130_fd_sc_hs__clkinv_1 u_DCDC_INVERTER1(
		.A(in),
		.Y(out1)
	);

	sky130_fd_sc_hs__clkinv_1 u_DCDC_INVERTER2(
		.A(out1),
		.Y(out)
	);
endmodule
