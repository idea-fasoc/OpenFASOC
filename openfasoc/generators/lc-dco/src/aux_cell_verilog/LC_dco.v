// LC DCO top PAR verilog


module lc_dco(sw, outp, outn,Ibias);
    output wire outp, outn;
    inout Ibias;
    input [7:0] sw;

	Ind_top ind1(
	  .outn(outn),
	  .outp(outp)
	`ifdef PG
	  .VDD() // If we need this instead of global net connection
	`endif
	);

// Add xN of these to emulate various swcap cells for e.g 8, though we need differently sized cells if we are binary weighted
	genvar i;
	localparam swwidth = 8 ;
	generate for (i=0; i < swwidth; i=i+1) begin
		swcap swcap_inst1 (
		  .outn(outn),
		  .outp(outp),
		`ifdef PG
		  GND(),
		`endif
		  .sw(sw[i])
		);
	end
	endgenerate
// Cross Coupled Pair
	diff_cross_mirror diff_mirror_inst (
	  .outn(outn),
	  .outp(outp),
	  .Ibias(Ibias)
	);


endmodule
