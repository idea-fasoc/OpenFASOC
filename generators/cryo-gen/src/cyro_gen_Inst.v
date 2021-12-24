module Cyro_Gen_Inst_Test
(
	input EBL,
	output Out
	);
	
	wire VIN;
	TEMP_ANALOG_lv ring_oscillator(
		.EN(EBL),
		.OUT(out)
	);

	TEMP_ANALOG_hv divider(
		.CLK_in(out),
		.CLK_out(Out)
	);

endmodule

