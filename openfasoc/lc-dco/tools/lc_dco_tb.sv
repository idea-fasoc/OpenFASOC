// Testbench for lc_dco.v
`timescale 1ns/1ps

module lc_dco_tb;

	parameter SW_Width=8;

	reg [SW_Width-1:0] sw_val;
	wire outp_sig, outn_sig;
	wire open;

	initial begin
		$dumpfile("test.vcd");
		$dumpvars(4,lc_dco_tb);
		$dumpon;
		$display("DCO at 0");
    		sw_val <= 8'd0;
    		#100;
		$display("DCO at 1");
    		sw_val <= 8'd1;
    		#100;
		$display("DCO at 15");
    		sw_val <= 8'd15;
    		#100;
    		sw_val <= 8'd31;
		$display("DCO at 31");
    		#100;
		$display("DCO at 63");
    		sw_val <= 8'd63;
    		#100;
		$display("DCO at 127");
    		sw_val <= 8'd127;
    		#100;
		$dumpoff;
		$finish;
	end

        lc_dco lc_dco_inst(
                .sw(sw_val),
                .outp(outp_sig),
                .outn(outn_sig),
                .Ibias()
        );


endmodule : lc_dco_tb
