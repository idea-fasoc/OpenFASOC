(* blackbox *) module SLC(
  output VOUT,
  input IN,
  input INB
);
endmodule
(* keep_hierarchy *)
(* blackbox *) module HEADER(
  inout VIN
);
parameter dont_touch = "on";
endmodule
