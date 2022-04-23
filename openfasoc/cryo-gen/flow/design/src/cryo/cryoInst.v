module cryoInst
(
	input EBL,
	output OUT
	);

	wire ro_out;

	cryo_ro cryo_ro_1(
		.EN(EBL),
		.OUT(ro_out)
	);

	divider divider_1(
	       	.CLK_in(ro_out),
		.CLK_out(OUT)
	);

endmodule
