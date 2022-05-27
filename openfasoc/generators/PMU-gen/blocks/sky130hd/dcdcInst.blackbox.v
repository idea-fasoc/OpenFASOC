// dcdcInst: AUX CELL DCDC_COMP
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module DCDC_COMP(
  input VIN,
  input VIP,
  input CLK,
  output VOP,
  output VON
);
parameter dont_touch = "on";
endmodule



// DCDC_MUX
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module DCDC_MUX(
  input SEL_H,
  //input SEL_INV_H,
  input SEL_L,
  //input SEL_INV_L,
  input VIN,
  output VOUT_H,
  output VOUT_L
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
	input [5:0] sel_vh, sel_vl,
  input w_clk0, w_clk0b, w_clk1, w_clk1b
);
parameter dont_touch = "on";
endmodule

// DCDC_DAC
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module DCDC_DAC(
  input D0, D1, D2, D3, D4, D5,
  input RST,
  input REF,
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
  input [8:0] seed,
  output clk0, clk0b, clk1, clk1b
);
parameter dont_touch = "on";
endmodule
