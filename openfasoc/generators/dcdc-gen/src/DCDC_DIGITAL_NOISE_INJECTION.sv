// Design: DCDC_DIGITAL_NOISE_INJECTION
// Description: Use clock-controlled sequence generator for noise injection (pseudo-random number)
// Author：Jianwei Jia
// Updated by:
// Last update: 04/18/22

`timescale 1ns/1ps

// Digital noise injection block
module DCDC_DIGITAL_NOISE_INJECTION(
    input logic CLK, rst_n, control, input logic[8:0] seed, output logic[3:0] Q
);
logic Q_internal;
LFSR2 NON_CLK_NOISE_LFSR2(.CLK(CLK), .rst_n(rst_n), .control(control), .seed(seed[4:0]), .Q_internal(Q_internal));
LFSR1 NON_CLK_NOISE_LFSR1(.CLK(CLK), .rst_n(rst_n), .seed(seed[8:5]), .Q_internal(Q_internal), .Q(Q));
endmodule

`timescale 1ns/1ps
//the second LFSR - 6bit LFSR
module NON_CLK_NOISE_LFSR2(
    input logic CLK, rst_n, control, input logic[4:0] seed, output logic Q_internal
);
logic[5:0] Q;
logic OUT, XOR1_OUT;
//asynchronous reset->1 negedge D flip-flop
always_ff @(posedge CLK or negedge rst_n) begin
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
    input logic CLK, rst_n, Q_internal, input logic[3:0] seed, output logic[3:0] Q
);
logic Q4;
logic D;
//asynchronous reset->1 negedge D flip-flop
always_ff @(posedge CLK or negedge rst_n) begin
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
