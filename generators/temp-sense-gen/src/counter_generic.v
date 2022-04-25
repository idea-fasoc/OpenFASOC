module counter#
(
	parameter NBIT = 24
)
//(CLK_SENS, CLK_REF, RESET_COUNTERn, SEL_CONV_TIME, DOUT, DONE);
(
	input RESET_COUNTERn,
	input CLK_REF, CLK_SENS,
	input [3:0] SEL_CONV_TIME,

	output DONE,
	output reg [NBIT-1:0] DOUT
);
	reg [NBIT-1:0] div_s;
	reg [NBIT-1:0] div_r;

	reg doneb;
	wire done_pre, done_ref, done_sens;
	wire clk_ref_in, clk_sens_in;
	reg WAKE;
	reg WAKE_pre;


	assign clk_sens_in = done_sens && CLK_SENS;
	assign clk_ref_in = done_ref && CLK_REF;
	assign done_pre = ~doneb;
	assign done_sens = WAKE_pre &&  doneb;
	assign done_ref = WAKE && doneb;
//	BUFH_X4M_A9TR	Buf_DONE(.A(done_pre), .Y(DONE));
//	BUF_X0P4N_A10P5PP84TR_C14	Buf_DONE(.A(done_pre), .Y(DONE));
@@ @np Buf_DONE(.A(done_pre), .nbout(DONE));
	//assign RESET_CLK_REF = ~q1;

	always @ (*) begin
		case (done_pre)
			1'd0:	DOUT = 0;
			1'd1:	DOUT = div_s;
		endcase
	end
	always @ (*) begin
		case (SEL_CONV_TIME)
			4'd0:	doneb = ~div_r[5];
			4'd1:	doneb = ~div_r[6];
			4'd2:	doneb = ~div_r[7];
			4'd3:	doneb = ~div_r[8];
			4'd4:	doneb = ~div_r[9];
			4'd5:	doneb = ~div_r[10];
			4'd6:	doneb = ~div_r[11];
			4'd7:	doneb = ~div_r[12];
			4'd8:	doneb = ~div_r[13];
			4'd9:	doneb = ~div_r[14];
			4'd10:	doneb = ~div_r[15];
			4'd11:	doneb = ~div_r[16];
			4'd12:	doneb = ~div_r[17];
			4'd13:	doneb = ~div_r[18];
			4'd14:	doneb = ~div_r[19];
			4'd15:	doneb = ~div_r[20];
		endcase
	end

	always @ (negedge RESET_COUNTERn or posedge CLK_REF) begin
		if (~RESET_COUNTERn) begin	WAKE <= 1'd0;
						WAKE_pre <= 1'd0;
		end
		else if (WAKE_pre == 0)		WAKE_pre <= 1'd1;
		else 				WAKE <= WAKE_pre;
	end
	// CLK_Sens DIV count
	always @ (negedge RESET_COUNTERn or posedge clk_sens_in) begin
		if (~RESET_COUNTERn)	div_s[0] <= 1'd0;
		else 			div_s[0] <= ~div_s[0];
	end

	genvar j;
	generate
		for (j=1; j< NBIT; j=j+1) begin
			always @ (negedge RESET_COUNTERn or negedge div_s[j-1]) begin
				if (~RESET_COUNTERn)		div_s[j] <=  1'd0;
				else 				div_s[j] <= ~div_s[j];
			end
		end
	endgenerate

	// CLK_REF DIV count
	always @ (negedge RESET_COUNTERn or posedge clk_ref_in) begin
		if (~RESET_COUNTERn)
						div_r[0] <= 1'd0;
		else			div_r[0] <=  ~div_r[0];
	end

	generate
		for (j=1; j<(NBIT-3); j=j+1) begin
			always @ (negedge RESET_COUNTERn or negedge div_r[j-1]) begin
				if (~RESET_COUNTERn)
							div_r[j] <=  1'd0;
				else 		div_r[j] <=  ~div_r[j];
			end
		end
	endgenerate

endmodule
