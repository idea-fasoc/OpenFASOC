// dcdcInst: AUX CELL DCDC_COMP
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module DCDC_COMP(
  input VIN,
  input VIP,
  input CLK,
  output VOP
);
parameter dont_touch = "on";
endmodule

// dcdc_config
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module dcdc_config(
  input  [5:0] a,
  output [11:0] s
);
parameter dont_touch = "on";
endmodule

// six_stage_conv
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module six_stage_conv (
  output VOUT,
	input [5:0] SEL_H, SEL_L,
  input clk0, clk0b, clk1, clk1b
);
parameter dont_touch = "on";
endmodule

// DCDC_DAC
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module DCDC_DAC(
  input D0, D1, D2, D3, D4, D5,
  input RST,
  output VOUT
);
parameter dont_touch = "on";
endmodule


// NON_CLK_GEN
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module NON_CLK_GEN(
  input clk,
  input clk_in,
  input rst_n,
  input control,
  output clk0, clk0b, clk1, clk1b
);
parameter dont_touch = "on";
endmodule

// NOISE_INJECTION
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module NOISE_INJECTION(
  input [3:0] D,
  input Noise_in,
  output bias_out
);
parameter dont_touch = "on";
endmodule

// DCDC_CLKGATE
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module DCDC_CLKGATE(
		input CLK,
		input GATE,
		output GCLK
);
parameter dont_touch = "on";
endmodule

// DCDC_FF
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module DCDC_FF(
		input CLK,
		input D,
		output Q
);
parameter dont_touch = "on";
endmodule

// DCDC_INVERTER
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module DCDC_INVERTER(
		input A,
		output Y
);
parameter dont_touch = "on";
endmodule
