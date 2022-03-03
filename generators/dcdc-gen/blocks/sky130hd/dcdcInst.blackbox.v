// dcdcInst: AUX CELL DCDC_COMP
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

// 2:1 stage: PMOS SWITCH
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module DCDC_XSW_PMOS(
  input clkb,
  input clk,
  inout vIN,
  inout vOUT0,
  inout vOUT1
);
parameter dont_touch = "on";
endmodule

// 2:1 stage: NMOS SWITCH
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module DCDC_XSW_NMOS(
  input clkb,
  input clk,
  inout vIN,
  inout vOUT0,
  inout vOUT1
);
parameter dont_touch = "on";
endmodule

// 2:1 stage: unit cap
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module DCDC_CAP_UNIT(
  inout top,
  inout bot
);
parameter dont_touch = "on";
endmodule

// power mux: DCDC_MUX_TGATE
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module DCDC_MUX_TGATE(
  input VIN,
  input SEL_INV,
  input SEL,
  inout VOUT
);
parameter dont_touch = "on";
endmodule