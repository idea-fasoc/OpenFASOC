// sch_path: /home/chandru/Tools/OpenFASOC/generators/lc-dco/xschem_rundir/swcap_verilog_ver.sch
module swcap (
  output wire outn,
  output wire outp,
  inout wire GND,
  input wire sw
);

wire net1  ;
wire net2  ;

nfet_01v8_lvt
M1 (
 .D( net1 ),
 .G( sw ),
 .S( net2 ),
 .B( GND )
);


nfet_01v8_lvt
M2 (
 .D( GND ),
 .G( sw ),
 .S( net1 ),
 .B( GND )
);


nfet_01v8_lvt
M3 (
 .D( net2 ),
 .G( sw ),
 .S( GND ),
 .B( GND )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 )
)
C1 (
 .c0( outn ),
 .c1( net2 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 )
)
C2 (
 .c0( net1 ),
 .c1( outp )
);

endmodule
