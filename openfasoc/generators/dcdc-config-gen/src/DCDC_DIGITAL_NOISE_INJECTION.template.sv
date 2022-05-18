// Design: DCDC_DIGITAL_NOISE_INJECTION
// Description: Use clock-controlled sequence generator for noise injection (pseudo-random number)
// Author：Jianwei Jia
// Updated by:
// Last update: 04/18/22

`timescale 1ns/1ps

// Digital noise injection block
module DCDC_DNI(
    input logic CLK, rst_n, output logic[3:0] Q
);
logic LFSR1_OUT, CLK_LFSR2;
//the first LFSR
DCDC_LFSR1 DCDC_LFSR1(.CLK(CLK), .rst_n(rst_n), .OUT(LFSR1_OUT));
and and1(CLK_LFSR2, LFSR1_OUT, CLK);
//the second LFSR
DCDC_LFSR2 DCDC_LFSR2(.CLK(CLK_LFSR2), .rst_n(rst_n), .Q(Q));
endmodule

//the first LFSR
module DCDC_LFSR1(
    input logic CLK, rst_n, output logic OUT
);
logic[3:0] Q;
logic D;
//asynchronous reset->1 negedge D flip-flop
always_ff @(posedge CLK or negedge rst_n) begin
    if(!rst_n) begin
    Q[0]<=1'b1;
    Q[1]<=1'b1;
    Q[2]<=1'b1;
    Q[3]<=1'b1;
    end
    else begin
    Q[0]<=Q[3];
    Q[1]<=D;
    Q[2]<=Q[1];
    Q[3]<=Q[2];
    end
end
//The XOR
xor xor1 (D, Q[0], Q[3]);
not not1 (OUT, Q[2]);
endmodule

// the second LFSR
module DCDC_LFSR2(
    input logic CLK, rst_n, output logic[3:0] Q
);
logic D;
//asynchronous reset->1 negedge D flip-flop
always_ff @(posedge CLK or negedge rst_n) begin
    if(!rst_n) begin
    Q[0]<=1'b1;
    Q[1]<=1'b1;
    Q[2]<=1'b1;
    Q[3]<=1'b1;
    end
    else begin
    Q[0]<=Q[3];
    Q[1]<=D;
    Q[2]<=Q[1];
    Q[3]<=Q[2];
    end
end
//The XOR
xor xor1 (D, Q[0], Q[3]);
endmodule
