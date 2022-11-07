// Verilog for library /import/yukari1/lrburle/OSU_180/char/liberate/VERILOG/gf180mcu_9T_TT_3P3_25C.ccs created by Liberate 19.2.2.189 on Thu Oct 27 10:01:39 CDT 2022 for SDF version 2.1

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_addf_1 (CO, S, A, B, CI);
	output CO, S;
	input A, B, CI;

	// Function
	wire A__bar, B__bar, CI__bar;
	wire int_fwire_0, int_fwire_1, int_fwire_2;
	wire int_fwire_3, int_fwire_4, int_fwire_5;
	wire int_fwire_6;

	and (int_fwire_0, B, CI);
	and (int_fwire_1, A, CI);
	and (int_fwire_2, A, B);
	or (CO, int_fwire_2, int_fwire_1, int_fwire_0);
	not (B__bar, B);
	not (A__bar, A);
	and (int_fwire_3, A__bar, B__bar, CI);
	not (CI__bar, CI);
	and (int_fwire_4, A__bar, B, CI__bar);
	and (int_fwire_5, A, B__bar, CI__bar);
	and (int_fwire_6, A, B, CI);
	or (S, int_fwire_6, int_fwire_5, int_fwire_4, int_fwire_3);

	// Timing
	specify
		if ((B & ~CI))
			(A => CO) = 0;
		if ((~B & CI))
			(A => CO) = 0;
		ifnone (A => CO) = 0;
		if ((A & ~CI))
			(B => CO) = 0;
		if ((~A & CI))
			(B => CO) = 0;
		ifnone (B => CO) = 0;
		if ((A & ~B))
			(CI => CO) = 0;
		if ((~A & B))
			(CI => CO) = 0;
		ifnone (CI => CO) = 0;
		if ((B & CI))
			(A => S) = 0;
		if ((~B & ~CI))
			(A => S) = 0;
		ifnone (A => S) = 0;
		if ((B & ~CI))
			(A => S) = 0;
		if ((~B & CI))
			(A => S) = 0;
		if ((A & CI))
			(B => S) = 0;
		if ((~A & ~CI))
			(B => S) = 0;
		ifnone (B => S) = 0;
		if ((A & ~CI))
			(B => S) = 0;
		if ((~A & CI))
			(B => S) = 0;
		if ((A & B))
			(CI => S) = 0;
		if ((~A & ~B))
			(CI => S) = 0;
		ifnone (CI => S) = 0;
		if ((A & ~B))
			(CI => S) = 0;
		if ((~A & B))
			(CI => S) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_addh_1 (CO, S, A, B);
	output CO, S;
	input A, B;

	// Function
	wire A__bar, B__bar, int_fwire_0;
	wire int_fwire_1;

	and (CO, A, B);
	not (A__bar, A);
	and (int_fwire_0, A__bar, B);
	not (B__bar, B);
	and (int_fwire_1, A, B__bar);
	or (S, int_fwire_1, int_fwire_0);

	// Timing
	specify
		(A => CO) = 0;
		(B => CO) = 0;
		if (~B)
			(A => S) = 0;
		if (B)
			(A => S) = 0;
		if (~A)
			(B => S) = 0;
		if (A)
			(B => S) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_and2_1 (Y, A, B);
	output Y;
	input A, B;

	// Function
	and (Y, A, B);

	// Timing
	specify
		(A => Y) = 0;
		(B => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_aoi21_1 (Y, A0, A1, B);
	output Y;
	input A0, A1, B;

	// Function
	wire A0__bar, A1__bar, B__bar;
	wire int_fwire_0, int_fwire_1;

	not (B__bar, B);
	not (A1__bar, A1);
	and (int_fwire_0, A1__bar, B__bar);
	not (A0__bar, A0);
	and (int_fwire_1, A0__bar, B__bar);
	or (Y, int_fwire_1, int_fwire_0);

	// Timing
	specify
		(A0 => Y) = 0;
		(A1 => Y) = 0;
		if ((A0 & ~A1))
			(B => Y) = 0;
		if ((~A0 & A1))
			(B => Y) = 0;
		if ((~A0 & ~A1))
			(B => Y) = 0;
		ifnone (B => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_buf_1 (Y, A);
	output Y;
	input A;

	// Function
	buf (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_buf_16 (Y, A);
	output Y;
	input A;

	// Function
	buf (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_buf_2 (Y, A);
	output Y;
	input A;

	// Function
	buf (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_buf_4 (Y, A);
	output Y;
	input A;

	// Function
	buf (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_buf_8 (Y, A);
	output Y;
	input A;

	// Function
	buf (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_clkbuf_1 (Y, A);
	output Y;
	input A;

	// Function
	buf (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_clkbuf_16 (Y, A);
	output Y;
	input A;

	// Function
	buf (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_clkbuf_2 (Y, A);
	output Y;
	input A;

	// Function
	buf (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_clkbuf_4 (Y, A);
	output Y;
	input A;

	// Function
	buf (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_clkbuf_8 (Y, A);
	output Y;
	input A;

	// Function
	buf (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_clkinv_1 (Y, A);
	output Y;
	input A;

	// Function
	not (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_clkinv_16 (Y, A);
	output Y;
	input A;

	// Function
	not (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_clkinv_2 (Y, A);
	output Y;
	input A;

	// Function
	not (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_clkinv_4 (Y, A);
	output Y;
	input A;

	// Function
	not (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_clkinv_8 (Y, A);
	output Y;
	input A;

	// Function
	not (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_dff_1 (Q, QN, D, CLK);
	output Q, QN;
	input D, CLK;
	reg notifier;
	wire delayed_D, delayed_CLK;

	// Function
	wire int_fwire_IQ, int_fwire_IQN, xcr_0;

	altos_dff_err (xcr_0, delayed_CLK, delayed_D);
	altos_dff (int_fwire_IQ, notifier, delayed_CLK, delayed_D, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing
	specify
		(posedge CLK => (Q+:D)) = 0;
		(posedge CLK => (QN-:D)) = 0;
		$setuphold (posedge CLK, posedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$width (posedge CLK &&& D, 0, 0, notifier);
		$width (negedge CLK &&& D, 0, 0, notifier);
		$width (posedge CLK &&& ~D, 0, 0, notifier);
		$width (negedge CLK &&& ~D, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_dffn_1 (Q, QN, D, CLKN);
	output Q, QN;
	input D, CLKN;
	reg notifier;
	wire delayed_D, delayed_CLKN;

	// Function
	wire int_fwire_IQ, int_fwire_IQN, xcr_0;

	altos_dff_err (xcr_0, delayed_CLKN, delayed_D);
	altos_dff (int_fwire_IQ, notifier, delayed_CLKN, delayed_D, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing
	specify
		(posedge CLKN => (Q+:D)) = 0;
		(posedge CLKN => (QN-:D)) = 0;
		$setuphold (posedge CLKN, posedge D, 0, 0, notifier,,, delayed_CLKN, delayed_D);
		$setuphold (posedge CLKN, negedge D, 0, 0, notifier,,, delayed_CLKN, delayed_D);
		$width (posedge CLKN &&& D, 0, 0, notifier);
		$width (negedge CLKN &&& D, 0, 0, notifier);
		$width (posedge CLKN &&& ~D, 0, 0, notifier);
		$width (negedge CLKN &&& ~D, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_dffsr_1 (Q, QN, D, RN, SN, CLK);
	output Q, QN;
	input D, RN, SN, CLK;
	reg notifier;
	wire delayed_D, delayed_RN, delayed_SN, delayed_CLK;

	// Function
	wire int_fwire_IQ, int_fwire_IQN, int_fwire_r;
	wire int_fwire_s, xcr_0;

	not (int_fwire_s, delayed_SN);
	not (int_fwire_r, delayed_RN);
	altos_dff_sr_err (xcr_0, delayed_CLK, delayed_D, int_fwire_s, int_fwire_r);
	altos_dff_sr_0 (int_fwire_IQ, notifier, delayed_CLK, delayed_D, int_fwire_s, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond0, adacond1, adacond2;
	wire adacond3, adacond4, adacond5;
	wire adacond6, adacond7, adacond8;
	wire CLK__bar, D__bar;


	// Additional timing gates
	and (adacond0, RN, SN);
	and (adacond1, D, SN);
	and (adacond2, CLK, SN);
	not (CLK__bar, CLK);
	and (adacond3, CLK__bar, SN);
	not (D__bar, D);
	and (adacond4, D__bar, RN);
	and (adacond5, CLK, RN);
	and (adacond6, CLK__bar, RN);
	and (adacond7, D, RN, SN);
	and (adacond8, D__bar, RN, SN);

	specify
		if ((CLK & SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CLK & ~SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((~CLK & D & SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((~CLK & D & ~SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((~CLK & ~D & SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((~CLK & ~D & ~SN))
			(negedge RN => (Q+:1'b0)) = 0;
		ifnone (negedge RN => (Q+:1'b0)) = 0;
		if ((CLK & ~SN))
			(posedge RN => (Q+:1'b1)) = 0;
		if ((~CLK & D & ~SN))
			(posedge RN => (Q+:1'b1)) = 0;
		if ((~CLK & ~D & ~SN))
			(posedge RN => (Q+:1'b1)) = 0;
		ifnone (posedge RN => (Q+:1'b1)) = 0;
		if ((CLK & RN))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((~CLK & D & RN))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((~CLK & ~D & RN))
			(negedge SN => (Q+:1'b1)) = 0;
		ifnone (negedge SN => (Q+:1'b1)) = 0;
		(posedge CLK => (Q+:D)) = 0;
		if ((CLK & ~SN))
			(posedge RN => (QN-:1'b1)) = 0;
		if ((~CLK & D & ~SN))
			(posedge RN => (QN-:1'b1)) = 0;
		if ((~CLK & ~D & ~SN))
			(posedge RN => (QN-:1'b1)) = 0;
		ifnone (posedge RN => (QN-:1'b1)) = 0;
		if ((CLK & SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((CLK & ~SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((~CLK & D & SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((~CLK & D & ~SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((~CLK & ~D & SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((~CLK & ~D & ~SN))
			(negedge RN => (QN-:1'b0)) = 0;
		ifnone (negedge RN => (QN-:1'b0)) = 0;
		if ((CLK & RN))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((~CLK & D & RN))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((~CLK & ~D & RN))
			(negedge SN => (QN-:1'b1)) = 0;
		ifnone (negedge SN => (QN-:1'b1)) = 0;
		(posedge CLK => (QN-:D)) = 0;
		$setuphold (posedge CLK &&& adacond0, posedge D &&& adacond0, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK &&& adacond0, negedge D &&& adacond0, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, posedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge SN &&& CLK, posedge RN &&& CLK, 0, 0, notifier,,, delayed_SN, delayed_RN);
		$setuphold (posedge SN &&& ~CLK, posedge RN &&& ~CLK, 0, 0, notifier,,, delayed_SN, delayed_RN);
		$setuphold (posedge SN, posedge RN, 0, 0, notifier,,, delayed_SN, delayed_RN);
		$recovery (posedge RN &&& adacond1, posedge CLK &&& adacond1, 0, notifier);
		$recovery (posedge RN, posedge CLK, 0, notifier);
		$hold (posedge CLK &&& adacond1, posedge RN &&& adacond1, 0, notifier);
		$hold (posedge CLK, posedge RN, 0, notifier);
		$recovery (posedge SN &&& adacond4, posedge CLK &&& adacond4, 0, notifier);
		$recovery (posedge SN, posedge CLK, 0, notifier);
		$hold (posedge CLK &&& adacond4, posedge SN &&& adacond4, 0, notifier);
		$hold (posedge CLK, posedge SN, 0, notifier);
		$width (negedge RN &&& adacond2, 0, 0, notifier);
		$width (negedge RN &&& adacond3, 0, 0, notifier);
		$width (negedge SN &&& adacond5, 0, 0, notifier);
		$width (negedge SN &&& adacond6, 0, 0, notifier);
		$width (posedge CLK &&& adacond7, 0, 0, notifier);
		$width (negedge CLK &&& adacond7, 0, 0, notifier);
		$width (posedge CLK &&& adacond8, 0, 0, notifier);
		$width (negedge CLK &&& adacond8, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_dlat_1 (Q, D, CLK);
	output Q;
	input D, CLK;
	reg notifier;
	wire delayed_D, delayed_CLK;

	// Function
	wire int_fwire_IQ;

	altos_latch (int_fwire_IQ, notifier, delayed_CLK, delayed_D);
	buf (Q, int_fwire_IQ);

	// Timing
	specify
		(D => Q) = 0;
		(posedge CLK => (Q+:D)) = 0;
		$setuphold (negedge CLK, posedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (negedge CLK, negedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$width (posedge CLK &&& D, 0, 0, notifier);
		$width (posedge CLK &&& ~D, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_dlatn_1 (Q, D, CLKN);
	output Q;
	input D, CLKN;
	reg notifier;
	wire delayed_D, delayed_CLKN;

	// Function
	wire int_fwire_IQ;

	altos_latch (int_fwire_IQ, notifier, delayed_CLKN, delayed_D);
	buf (Q, int_fwire_IQ);

	// Timing
	specify
		(D => Q) = 0;
		(posedge CLKN => (Q+:D)) = 0;
		$setuphold (negedge CLKN, posedge D, 0, 0, notifier,,, delayed_CLKN, delayed_D);
		$setuphold (negedge CLKN, negedge D, 0, 0, notifier,,, delayed_CLKN, delayed_D);
		$width (posedge CLKN &&& D, 0, 0, notifier);
		$width (posedge CLKN &&& ~D, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_inv_1 (Y, A);
	output Y;
	input A;

	// Function
	not (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_inv_16 (Y, A);
	output Y;
	input A;

	// Function
	not (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_inv_2 (Y, A);
	output Y;
	input A;

	// Function
	not (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_inv_4 (Y, A);
	output Y;
	input A;

	// Function
	not (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_inv_8 (Y, A);
	output Y;
	input A;

	// Function
	not (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_mux2_1 (Y, A, B, Sel);
	output Y;
	input A, B, Sel;

	// Function
	wire int_fwire_0, int_fwire_1, Sel__bar;

	and (int_fwire_0, B, Sel);
	not (Sel__bar, Sel);
	and (int_fwire_1, A, Sel__bar);
	or (Y, int_fwire_1, int_fwire_0);

	// Timing
	specify
		(A => Y) = 0;
		(B => Y) = 0;
		if ((~A & B))
			(Sel => Y) = 0;
		if ((A & ~B))
			(Sel => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_nand2_1 (Y, A, B);
	output Y;
	input A, B;

	// Function
	wire A__bar, B__bar;

	not (B__bar, B);
	not (A__bar, A);
	or (Y, A__bar, B__bar);

	// Timing
	specify
		(A => Y) = 0;
		(B => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_nor2_1 (Y, A, B);
	output Y;
	input A, B;

	// Function
	wire A__bar, B__bar;

	not (B__bar, B);
	not (A__bar, A);
	and (Y, A__bar, B__bar);

	// Timing
	specify
		(A => Y) = 0;
		(B => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_oai21_1 (Y, A0, A1, B);
	output Y;
	input A0, A1, B;

	// Function
	wire A0__bar, A1__bar, B__bar;
	wire int_fwire_0;

	not (B__bar, B);
	not (A1__bar, A1);
	not (A0__bar, A0);
	and (int_fwire_0, A0__bar, A1__bar);
	or (Y, int_fwire_0, B__bar);

	// Timing
	specify
		(A0 => Y) = 0;
		(A1 => Y) = 0;
		if ((A0 & A1))
			(B => Y) = 0;
		if ((A0 & ~A1))
			(B => Y) = 0;
		if ((~A0 & A1))
			(B => Y) = 0;
		ifnone (B => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_or2_1 (Y, A, B);
	output Y;
	input A, B;

	// Function
	or (Y, A, B);

	// Timing
	specify
		(A => Y) = 0;
		(B => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_tiehi (Y);
	output Y;

	// Function
	buf (Y, 1'b1);

	// Timing
	specify
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_tielo (Y);
	output Y;

	// Function
	buf (Y, 1'b0);

	// Timing
	specify
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_xnor2_1 (Y, A, B);
	output Y;
	input A, B;

	// Function
	wire A__bar, B__bar, int_fwire_0;
	wire int_fwire_1;

	not (B__bar, B);
	not (A__bar, A);
	and (int_fwire_0, A__bar, B__bar);
	and (int_fwire_1, A, B);
	or (Y, int_fwire_1, int_fwire_0);

	// Timing
	specify
		if (B)
			(A => Y) = 0;
		if (~B)
			(A => Y) = 0;
		if (A)
			(B => Y) = 0;
		if (~A)
			(B => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:
`timescale 1ns/10ps
`celldefine
module gf180mcu_osu_sc_9T_xor2_1 (Y, A, B);
	output Y;
	input A, B;

	// Function
	wire A__bar, B__bar, int_fwire_0;
	wire int_fwire_1;

	not (A__bar, A);
	and (int_fwire_0, A__bar, B);
	not (B__bar, B);
	and (int_fwire_1, A, B__bar);
	or (Y, int_fwire_1, int_fwire_0);

	// Timing
	specify
		if (~B)
			(A => Y) = 0;
		if (B)
			(A => Y) = 0;
		if (~A)
			(B => Y) = 0;
		if (A)
			(B => Y) = 0;
	endspecify
endmodule
`endcelldefine


`ifdef _udp_def_altos_latch_
`else
`define _udp_def_altos_latch_
primitive altos_latch (q, v, clk, d);
	output q;
	reg q;
	input v, clk, d;

	table
		* ? ? : ? : x;
		? 1 0 : ? : 0;
		? 1 1 : ? : 1;
		? x 0 : 0 : -;
		? x 1 : 1 : -;
		? 0 ? : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_err_
`else
`define _udp_def_altos_dff_err_
primitive altos_dff_err (q, clk, d);
	output q;
	reg q;
	input clk, d;

	table
		(0x) ? : ? : 0;
		(1x) ? : ? : 1;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_
`else
`define _udp_def_altos_dff_
primitive altos_dff (q, v, clk, d, xcr);
	output q;
	reg q;
	input v, clk, d, xcr;

	table
		*  ?   ? ? : ? : x;
		? (x1) 0 0 : ? : 0;
		? (x1) 1 0 : ? : 1;
		? (x1) 0 1 : 0 : 0;
		? (x1) 1 1 : 1 : 1;
		? (x1) ? x : ? : -;
		? (bx) 0 ? : 0 : -;
		? (bx) 1 ? : 1 : -;
		? (x0) b ? : ? : -;
		? (x0) ? x : ? : -;
		? (01) 0 ? : ? : 0;
		? (01) 1 ? : ? : 1;
		? (10) ? ? : ? : -;
		?  b   * ? : ? : -;
		?  ?   ? * : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_r_err_
`else
`define _udp_def_altos_dff_r_err_
primitive altos_dff_r_err (q, clk, d, r);
	output q;
	reg q;
	input clk, d, r;

	table
		 ?   0 (0x) : ? : -;
		 ?   0 (x0) : ? : -;
		(0x) ?  0   : ? : 0;
		(0x) 0  x   : ? : 0;
		(1x) ?  0   : ? : 1;
		(1x) 0  x   : ? : 1;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_r_
`else
`define _udp_def_altos_dff_r_
primitive altos_dff_r (q, v, clk, d, r, xcr);
	output q;
	reg q;
	input v, clk, d, r, xcr;

	table
		*  ?   ?  ?   ? : ? : x;
		?  ?   ?  1   ? : ? : 0;
		?  b   ? (1?) ? : 0 : -;
		?  x   0 (1?) ? : 0 : -;
		?  ?   ? (10) ? : ? : -;
		?  ?   ? (x0) ? : ? : -;
		?  ?   ? (0x) ? : 0 : -;
		? (x1) 0  ?   0 : ? : 0;
		? (x1) 1  0   0 : ? : 1;
		? (x1) 0  ?   1 : 0 : 0;
		? (x1) 1  0   1 : 1 : 1;
		? (x1) ?  ?   x : ? : -;
		? (bx) 0  ?   ? : 0 : -;
		? (bx) 1  0   ? : 1 : -;
		? (x0) 0  ?   ? : ? : -;
		? (x0) 1  0   ? : ? : -;
		? (x0) ?  0   x : ? : -;
		? (01) 0  ?   ? : ? : 0;
		? (01) 1  0   ? : ? : 1;
		? (10) ?  ?   ? : ? : -;
		?  b   *  ?   ? : ? : -;
		?  ?   ?  ?   * : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_s_err_
`else
`define _udp_def_altos_dff_s_err_
primitive altos_dff_s_err (q, clk, d, s);
	output q;
	reg q;
	input clk, d, s;

	table
		 ?   1 (0x) : ? : -;
		 ?   1 (x0) : ? : -;
		(0x) ?  0   : ? : 0;
		(0x) 1  x   : ? : 0;
		(1x) ?  0   : ? : 1;
		(1x) 1  x   : ? : 1;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_s_
`else
`define _udp_def_altos_dff_s_
primitive altos_dff_s (q, v, clk, d, s, xcr);
	output q;
	reg q;
	input v, clk, d, s, xcr;

	table
		*  ?   ?  ?   ? : ? : x;
		?  ?   ?  1   ? : ? : 1;
		?  b   ? (1?) ? : 1 : -;
		?  x   1 (1?) ? : 1 : -;
		?  ?   ? (10) ? : ? : -;
		?  ?   ? (x0) ? : ? : -;
		?  ?   ? (0x) ? : 1 : -;
		? (x1) 0  0   0 : ? : 0;
		? (x1) 1  ?   0 : ? : 1;
		? (x1) 1  ?   1 : 1 : 1;
		? (x1) 0  0   1 : 0 : 0;
		? (x1) ?  ?   x : ? : -;
		? (bx) 1  ?   ? : 1 : -;
		? (bx) 0  0   ? : 0 : -;
		? (x0) 1  ?   ? : ? : -;
		? (x0) 0  0   ? : ? : -;
		? (x0) ?  0   x : ? : -;
		? (01) 1  ?   ? : ? : 1;
		? (01) 0  0   ? : ? : 0;
		? (10) ?  ?   ? : ? : -;
		?  b   *  ?   ? : ? : -;
		?  ?   ?  ?   * : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_sr_err_
`else
`define _udp_def_altos_dff_sr_err_
primitive altos_dff_sr_err (q, clk, d, s, r);
	output q;
	reg q;
	input clk, d, s, r;

	table
		 ?   1 (0x)  ?   : ? : -;
		 ?   0  ?   (0x) : ? : -;
		 ?   0  ?   (x0) : ? : -;
		(0x) ?  0    0   : ? : 0;
		(0x) 1  x    0   : ? : 0;
		(0x) 0  0    x   : ? : 0;
		(1x) ?  0    0   : ? : 1;
		(1x) 1  x    0   : ? : 1;
		(1x) 0  0    x   : ? : 1;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_sr_0
`else
`define _udp_def_altos_dff_sr_0
primitive altos_dff_sr_0 (q, v, clk, d, s, r, xcr);
	output q;
	reg q;
	input v, clk, d, s, r, xcr;

	table
	//	v,  clk, d, s, r : q' : q;

		*  ?   ?   ?   ?   ? : ? : x;
		?  ?   ?   ?   1   ? : ? : 0;
		?  ?   ?   1   0   ? : ? : 1;
		?  b   ? (1?)  0   ? : 1 : -;
		?  x   1 (1?)  0   ? : 1 : -;
		?  ?   ? (10)  0   ? : ? : -;
		?  ?   ? (x0)  0   ? : ? : -;
		?  ?   ? (0x)  0   ? : 1 : -;
		?  b   ?  0   (1?) ? : 0 : -;
		?  x   0  0   (1?) ? : 0 : -;
		?  ?   ?  0   (10) ? : ? : -;
		?  ?   ?  0   (x0) ? : ? : -;
		?  ?   ?  0   (0x) ? : 0 : -;
		? (x1) 0  0    ?   0 : ? : 0;
		? (x1) 1  ?    0   0 : ? : 1;
		? (x1) 0  0    ?   1 : 0 : 0;
		? (x1) 1  ?    0   1 : 1 : 1;
		? (x1) ?  ?    0   x : ? : -;
		? (x1) ?  0    ?   x : ? : -;
		? (1x) 0  0    ?   ? : 0 : -;
		? (1x) 1  ?    0   ? : 1 : -;
		? (x0) 0  0    ?   ? : ? : -;
		? (x0) 1  ?    0   ? : ? : -;
		? (x0) ?  0    0   x : ? : -;
		? (0x) 0  0    ?   ? : 0 : -;
		? (0x) 1  ?    0   ? : 1 : -;
		? (01) 0  0    ?   ? : ? : 0;
		? (01) 1  ?    0   ? : ? : 1;
		? (10) ?  0    ?   ? : ? : -;
		? (10) ?  ?    0   ? : ? : -;
		?  b   *  0    ?   ? : ? : -;
		?  b   *  ?    0   ? : ? : -;
		?  ?   ?  ?    ?   * : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_sr_1
`else
`define _udp_def_altos_dff_sr_1
primitive altos_dff_sr_1 (q, v, clk, d, s, r, xcr);
	output q;
	reg q;
	input v, clk, d, s, r, xcr;

	table
	//	v,  clk, d, s, r : q' : q;

		*  ?   ?   ?   ?   ? : ? : x;
		?  ?   ?   0   1   ? : ? : 0;
		?  ?   ?   1   ?   ? : ? : 1;
		?  b   ? (1?)  0   ? : 1 : -;
		?  x   1 (1?)  0   ? : 1 : -;
		?  ?   ? (10)  0   ? : ? : -;
		?  ?   ? (x0)  0   ? : ? : -;
		?  ?   ? (0x)  0   ? : 1 : -;
		?  b   ?  0   (1?) ? : 0 : -;
		?  x   0  0   (1?) ? : 0 : -;
		?  ?   ?  0   (10) ? : ? : -;
		?  ?   ?  0   (x0) ? : ? : -;
		?  ?   ?  0   (0x) ? : 0 : -;
		? (x1) 0  0    ?   0 : ? : 0;
		? (x1) 1  ?    0   0 : ? : 1;
		? (x1) 0  0    ?   1 : 0 : 0;
		? (x1) 1  ?    0   1 : 1 : 1;
		? (x1) ?  ?    0   x : ? : -;
		? (x1) ?  0    ?   x : ? : -;
		? (1x) 0  0    ?   ? : 0 : -;
		? (1x) 1  ?    0   ? : 1 : -;
		? (x0) 0  0    ?   ? : ? : -;
		? (x0) 1  ?    0   ? : ? : -;
		? (x0) ?  0    0   x : ? : -;
		? (0x) 0  0    ?   ? : 0 : -;
		? (0x) 1  ?    0   ? : 1 : -;
		? (01) 0  0    ?   ? : ? : 0;
		? (01) 1  ?    0   ? : ? : 1;
		? (10) ?  0    ?   ? : ? : -;
		? (10) ?  ?    0   ? : ? : -;
		?  b   *  0    ?   ? : ? : -;
		?  b   *  ?    0   ? : ? : -;
		?  ?   ?  ?    ?   * : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_latch_r_
`else
`define _udp_def_altos_latch_r_
primitive altos_latch_r (q, v, clk, d, r);
	output q;
	reg q;
	input v, clk, d, r;

	table
		* ? ? ? : ? : x;
		? ? ? 1 : ? : 0;
		? 0 ? 0 : ? : -;
		? 0 ? x : 0 : -;
		? 1 0 0 : ? : 0;
		? 1 0 x : ? : 0;
		? 1 1 0 : ? : 1;
		? x 0 0 : 0 : -;
		? x 0 x : 0 : -;
		? x 1 0 : 1 : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_latch_s_
`else
`define _udp_def_altos_latch_s_
primitive altos_latch_s (q, v, clk, d, s);
	output q;
	reg q;
	input v, clk, d, s;

	table
		* ? ? ? : ? : x;
		? ? ? 1 : ? : 1;
		? 0 ? 0 : ? : -;
		? 0 ? x : 1 : -;
		? 1 1 0 : ? : 1;
		? 1 1 x : ? : 1;
		? 1 0 0 : ? : 0;
		? x 1 0 : 1 : -;
		? x 1 x : 1 : -;
		? x 0 0 : 0 : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_latch_sr_0
`else
`define _udp_def_altos_latch_sr_0
primitive altos_latch_sr_0 (q, v, clk, d, s, r);
	output q;
	reg q;
	input v, clk, d, s, r;

	table
		* ? ? ? ? : ? : x;
		? 1 1 ? 0 : ? : 1;
		? 1 0 0 ? : ? : 0;
		? ? ? 1 0 : ? : 1;
		? ? ? ? 1 : ? : 0;
		? 0 * ? ? : ? : -;
		? 0 ? * 0 : 1 : 1;
		? 0 ? 0 * : 0 : 0;
		? * 1 ? 0 : 1 : 1;
		? * 0 0 ? : 0 : 0;
		? ? 1 * 0 : 1 : 1;
		? ? 0 0 * : 0 : 0;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_latch_sr_1
`else
`define _udp_def_altos_latch_sr_1
primitive altos_latch_sr_1 (q, v, clk, d, s, r);
	output q;
	reg q;
	input v, clk, d, s, r;

	table
		* ? ? ? ? : ? : x;
		? 1 1 ? 0 : ? : 1;
		? 1 0 0 ? : ? : 0;
		? ? ? 1 ? : ? : 1;
		? ? ? 0 1 : ? : 0;
		? 0 * ? ? : ? : -;
		? 0 ? * 0 : 1 : 1;
		? 0 ? 0 * : 0 : 0;
		? * 1 ? 0 : 1 : 1;
		? * 0 0 ? : 0 : 0;
		? ? 1 * 0 : 1 : 1;
		? ? 0 0 * : 0 : 0;
	endtable
endprimitive
`endif
