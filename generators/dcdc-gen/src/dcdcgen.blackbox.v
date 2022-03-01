(* blackbox *) module DCDC_SIX_STAGES_CONV(
  input VDD,
  input VSS,
  input AVDD,
  input GND,
  input sel_vh,
  input sel_vl,
  input w_clk0,
  input w_clk0b,
  input w_clk1,
  input w_clk1b,
  output VOUT
);
parameter dont_touch = "on";
endmodule

// AUX CELL DCDC_NOV_CLKGEN
(* blackbox *) module DCDC_NOV_CLKGEN(
  input clk0,
  input s,
  input clk0
  input clk0b
  input clk1
  input clk1b
);
parameter dont_touch = "on";
endmodule

// AUX CELL DCDC_COMP
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module DCDC_COMP(
  input pos_in,
  input neg_in,
  input clk,
  output out
);
parameter dont_touch = "on";
endmodule

// Clock Gate
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module sky130_fd_sc_hd__dlclkp_1(
  input CLK,
  input GATE,
  output GCLK
);
parameter dont_touch = "on";
endmodule

// Sync FF
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module sky130_fd_sc_hd__dfxtp_1(
  input CLK,
  input D,
  output Q
);
parameter dont_touch = "on";
endmodule

// Sync Inv
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module sky130_fd_sc_hd__inv_1(
  input A,
  output A
);
parameter dont_touch = "on";
endmodule



