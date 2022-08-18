(* blackbox *) module LDO_COMPARATOR_LATCH(
  input CLK,
  input VREF,
  output OUT
);
parameter dont_touch = "on";
endmodule

(* keep *)
(* keep_hierarchy *)
(* blackbox *) module PT_UNIT_CELL(
  input CTRL
);
parameter dont_touch = "on";
endmodule

(* keep *)
(* keep_hierarchy *)
(* blackbox *) module PMOS(
  input cmp_out
);
parameter dont_touch = "on";
endmodule

(* keep *)
(* keep_hierarchy *)
(* blackbox *) module capacitor_test_nf(
  input pin0
);
parameter dont_touch = "on";
endmodule

(* blackbox *) module vref_gen_nmos_with_trim(
  input trim1,
  input trim2,
  input trim3,
  input trim4,
  input trim5,
  input trim6,
  input trim7,
  input trim8,
  input trim9,
  input trim10,
  output vref
);
parameter dont_touch = "on";
endmodule
