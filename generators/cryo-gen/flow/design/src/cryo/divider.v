module divider
(
	input CLK_in,
	output CLK_out
);
	reg Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10;

	assign CLK_out=Q10;
	always @ (posedge CLK_in )
	begin
		Q1<=~Q1;
	end
	always @ (posedge Q1 )
	begin
		Q2<=~Q2;
	end
	always @ (posedge Q2 )
	begin
		Q3<=~Q3;
	end
	always @ (posedge Q3 )
	begin
		Q4<=~Q4;
	end
	always @ (posedge Q4 )
	begin
		Q5<=~Q5;
	end
	always @ (posedge Q5 )
	begin
		Q6<=~Q6;
	end
	always @ (posedge Q6 )
	begin
		Q7<=~Q7;
	end
	always @ (posedge Q7 )
	begin
		Q8<=~Q8;
	end
	always @ (posedge Q8 )
	begin
		Q9<=~Q9;
	end
	always @ (posedge Q9 )
	begin
		Q10<=~Q10;
	end
endmodule
