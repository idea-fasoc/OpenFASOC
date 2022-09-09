// sch_path: /home/chandru/Tools/OpenFASOC/generators/lc-dco/xschem_rundir/diff_cross_mirror_verilog.sch
module diff_cross_mirror (
  output wire outn,
  output wire outp,
  input wire Ibias
);

wire net1  ;
wire net2  ;
wire net3  ;
wire GND  ;

nfet3_01v8_lvt
M1 (
 .D( outp ),
 .G( outn ),
 .S( net2 )
);


nfet3_01v8_lvt
M2 (
 .D( outn ),
 .G( outp ),
 .S( net1 )
);


nfet3_01v8_lvt
M4 (
 .D( net1 ),
 .G( Ibias ),
 .S( GND )
);


nfet3_01v8_lvt
M5 (
 .D( Ibias ),
 .G( Ibias ),
 .S( GND )
);


nfet3_01v8_lvt
M3 (
 .D( net2 ),
 .G( Ibias ),
 .S( net3 )
);

endmodule
