// Design: DCDC_NOV_CLKGEN
// Description: Using parameter and sel to adjust the delay time in nov_clk generation
// Author：Jianwei Jia
// Updated by:
// Last update: 02/05/22

//define non_overlap clock generator
module DCDC_NOV_CLKGEN #(parameter N_delay) (
    input logic [1:0] s, input logic clk_in, output logic clk0, clk0b, clk1, clk1b
);
    logic [N_delay:0] clk_in1;
    logic nandout1, nandout2;
    logic norout1, norout2;

    //clk buffer
    DCDC_BUFFER b1(clk_in1[0], clk_in);

    //add delay - deside the interval delay time,N inverter
    genvar i;
    generate
    for (i=0; i<(N_delay); i++) begin
    DCDC_BUFFER b(clk_in1[i+1], clk_in1[i]);
    end
    endgenerate

	wire out1, out2, out3, out4, clk_in9;

    //adjust delay element
    inverterchain_4 inverterchain_4(.in(clk_in1[N_delay]), .out1(out1), .out2(out2), .out3(out3), .out4(out4));
    MUX4 mux4(.y(clk_in9), .a(out1), .b(out2), .c(out3), .d(out4), .s(s));

    //output clk0, clk0b
@@ 	@na nand1(.Y(nandout1), .A(clk_in1[0]), .B(clk_in9));
@@ 	@nb not1(.Y(nandout2), .A(nandout1));
@@ 	@nc not2(.Y(clk0b), .A(nandout2));
	DCDC_BUFFER buf1(clk0, nandout2);

	//output clk1, clk1b
@@ 	@nd nor1(.Y(norout1), .A(clk_in1[0]), .B(clk_in9));
@@ 	@ne not3(.Y(norout2), .A(norout1));
@@ 	@nf not4(.Y(clk1), .A(norout2));
    DCDC_BUFFER buf2(clk1b, norout2);
endmodule

//MUX 4:1
module MUX4 (output logic y, input logic a,b,c,d, input logic [1:0] s);
always_comb begin
if(s[0])
    if(s[1])
        y=d;
    else
        y=c;
else
    if(s[1])
        y=b;
    else
        y=a;
end
endmodule


//4 Delay inverter chain
module inverterchain_4 (input in, output out1, out2, out3, out4);

	wire out2_0, out3_0, out4_0;
	wire out3_1, out4_1;
	wire out4_2;

	DCDC_BUFFER b1(out1, in);
	DCDC_BUFFER b2(out2_0, in), b3(out2, out2_0);
	DCDC_BUFFER b4(out3_0, in), b5(out3_1, out3_0), b6(out3, out3_1);
	DCDC_BUFFER b7(out4_0, in), b8(out4_1, out4_0), b9(out4_2, out4_1), b10(out4, out4_2);
endmodule
