module tempsenseInst_error
(
	input CLK_REF,
	input RESET_COUNTERn,
	input [3:0] SEL_CONV_TIME,
	input en,

        output [23:0] DOUT,
	output DONE,
	output out, outb,
	output lc_out
	);

	wire VIN;
	TEMP_ANALOG_lv temp_analog_0(
		.EN(en),
		.OUT(out),
		.OUTB(outb)
	);

	TEMP_ANALOG_hv temp_analog_1(
	       	.CLK_REF(CLK_REF),
        	.RESET_COUNTERn(RESET_COUNTERn),
        	.SEL_CONV_TIME(SEL_CONV_TIME),
		.out(out),
		.outb(outb),
		.DOUT(DOUT),
		.DONE(DONE),
		.lc_out(lc_out),
		.VIN(VIN)
	);

endmodule
