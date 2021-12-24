module cryoInst
(
	input EBL,
	output Out
	);
	
	wire ro_out;
 
	cryo_ro cryo_ro_1(
		.EN(en),
		.OUT(ro_out)
	);

	divider divider_1(
	       	.CLK_in(ro_out),
		.CLK_out(Out)		
	);

endmodule

