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

/* // 2:1 stage: PMOS SWITCH
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
endmodule */

/* // 2:1 stage: NMOS SWITCH
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
endmodule */

// 2:1 stage: unit cap
(* keep *)
(* keep_hierarchy *)
(* blackbox *) module DCDC_CAP_UNIT(
  inout TOP,
  inout BOT
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
    inout    VHIGH,
    inout    VLOW,
    inout    VMID,
    inout    Y1_TOP,
    inout    Y0_TOP,
    inout    Y1_BOT,
    inout    Y0_BOT,

    input    CLK0,
    input    CLK0B,
    input    CLK1,
    input    CLK1B
);
parameter dont_touch = "on";
endmodule
