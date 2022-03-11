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

// power mux: DCDC_MUX
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module DCDC_MUX(
  input SEL_H,
  input SEL_INV_H,
  input SEL_L,
  input SEL_INV_L,
  input VIN,
  output VOUT_H,
  output VOUT_L
);
parameter dont_touch = "on";
endmodule

// power mux: DCDC_MUX
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module DCDC_CONV2TO1 (
    inout    vhigh,
    inout    vlow,
    inout    vmid,
    inout    y1_top,
    inout    y0_top,
    inout    y1_bot,
    inout    y0_bot,

    input    clk0,
    input    clk0b,
    input    clk1,
    input    clk1b
);
parameter dont_touch = "on";
endmodule