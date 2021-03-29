module TEMP_ANALOG_hv
(
input CLK_REF,
input RESET_COUNTERn,
input [3:0] SEL_CONV_TIME,
input out, outb,

output [23:0] DOUT,
output DONE,
output lc_out,
inout VIN
);

wire lc_0;
//	reg  iso;
//	assign iso = 0 ;
counter async_counter_0(
	// Input
	.CLK_SENS       (lc_out),
	.CLK_REF        (CLK_REF),
	.RESET_COUNTERn (RESET_COUNTERn),
	.SEL_CONV_TIME  (SEL_CONV_TIME),
	// Output
	.DOUT           (DOUT),
	.DONE  		(DONE)
);

(* keep *)
HEADER a_header_0(.VIN(VIN));
HEADER a_header_1(.VIN(VIN));
HEADER a_header_2(.VIN(VIN));
SLC a_lc_0(.IN(out), .INB(outb), .VOUT(lc_0));
sky130_fd_sc_hd__buf_1 a_buffer_0 (.A(lc_0), .X(lc_out));
	
endmodule

