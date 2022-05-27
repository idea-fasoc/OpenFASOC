// NON_CLK_GEN
module NON_CLK_GEN(
  input clk,
  input clk_in,
  input rst_n,
  input control,
  input [8:0] seed,
  output clk0, clk0b, clk1, clk1b
);
wire [3:0] Q;
DCDC_NOV_CLKGEN #(.N_delay(7)) u_DCDC_NOV_CLKGEN (
    .clk_in(clk_in),
    .s (Q[1:0]), // two bits to select the dead time
    .clk0(clk0),
    .clk0b(clk0b),
    .clk1(clk1),
    .clk1b(clk1b)
);

//DCDE_DIGITAL_NOISE_INJECTION
DCDC_DIGITAL_NOISE_INJECTION u_DCDC_DIGITAL_NOISE_INJECTION(
  .CLK(clk),
  .rst_n(rst_n),
  .control(control),
  .seed(seed),
  .Q(Q)
);
endmodule

//noise injection
module DCDC_DIGITAL_NOISE_INJECTION(
    input CLK, rst_n, control, input [8:0] seed, output [3:0] Q
);
wire Q_internal;
NON_CLK_NOISE_LFSR2 LFSR2(.CLK(CLK), .rst_n(rst_n), .control(control), .seed(seed[4:0]), .Q_internal(Q_internal));
NON_CLK_NOISE_LFSR1 LFSR1(.CLK(CLK), .rst_n(rst_n), .seed(seed[8:5]), .Q_internal(Q_internal), .Q(Q));
endmodule

//the second LFSR - 6bit LFSR
module NON_CLK_NOISE_LFSR2(
    input CLK, rst_n, control, input [4:0] seed, output Q_internal
);
wire[5:0] Q;
wire OUT, XOR1_OUT;
//asynchronous reset->1 negedge D flip-flop
always@(posedge CLK or negedge rst_n) begin
    if(!rst_n) begin
    Q[0]<=seed[0];
    Q[1]<=seed[1];
    Q[2]<=seed[2];
    Q[3]<=seed[3];
    Q[4]<=seed[4];
    Q[5]<=1'b1; // ensure the LFSR won't go into '000000'
    end
    else begin
    Q[0]<=Q[1];
    Q[1]<=Q[2];
    Q[2]<=Q[3];
    Q[3]<=Q[4];
    Q[4]<=Q[5];
    Q[5]<=Q_internal;
    end
end
//The XOR
xor xor1 (XOR1_OUT, Q[0], Q[5]);
xor xor2 (Q_internal, control, XOR1_OUT);
endmodule

// the first LFSR - 5bit LFSR
module NON_CLK_NOISE_LFSR1(
    input CLK, rst_n, Q_internal, input[3:0] seed, output[3:0] Q
);
wire Q4;
wire D;
//asynchronous reset->1 negedge D flip-flop
always@(posedge CLK or negedge rst_n) begin
    if(!rst_n) begin
    Q[0]<=seed[0];
    Q[1]<=seed[1];
    Q[2]<=seed[2];
    Q[3]<=seed[3];
    Q4<=1'b1; // ensure the LFSR won't go into '00000'
    end
    else begin
    Q[0]<=Q[1];
    Q[1]<=Q[2];
    Q[2]<=Q[3];
    Q[3]<=Q4;
    Q4<=D;
    end
end
//The XOR
xor xor1 (D, Q_internal, Q[0]);
endmodule

//define non_overlap clock generator
module DCDC_NOV_CLKGEN #(parameter N_delay) (
    input [1:0] s, input clk_in, output clk0, clk0b, clk1, clk1b
);
    wire [N_delay:0] clk_in1;
    wire nandout1, nandout2;
    wire norout1, norout2;

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
	sky130_fd_sc_hd__nand2_1 nand1(.Y(nandout1), .A(clk_in1[0]), .B(clk_in9));
	sky130_fd_sc_hd__clkinv_1 not1(.Y(nandout2), .A(nandout1));
	sky130_fd_sc_hd__clkinv_1 not2(.Y(clk0b), .A(nandout2));
	DCDC_BUFFER buf1(clk0, nandout2);

	//output clk1, clk1b
	sky130_fd_sc_hd__nor2_1 nor1(.Y(norout1), .A(clk_in1[0]), .B(clk_in9));
	sky130_fd_sc_hd__clkinv_1 not3(.Y(norout2), .A(norout1));
	sky130_fd_sc_hd__clkinv_1 not4(.Y(clk1), .A(norout2));
    DCDC_BUFFER buf2(clk1b, norout2);
endmodule

//MUX 4:1
module MUX4 (output y, input a,b,c,d, input [1:0] s);
always@(*) begin
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

module DCDC_BUFFER(
    output logic out, input logic in
);
logic out1;

	sky130_fd_sc_hd__clkinv_1 u_DCDC_INVERTER1(
		.A(in),
		.Y(out1)
	);

	sky130_fd_sc_hd__clkinv_1 u_DCDC_INVERTER2(
		.A(out1),
		.Y(out)
	);
endmodule
