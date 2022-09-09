// sch_path: /home/chandru/Tools/OpenFASOC/generators/lc-dco/xschem_rundir/swcap.sch
module swcap (
  output wire outn,
  output wire outp,
  inout wire GND,
  input wire sw
);

wire net1  ;
wire net2  ;

nfet_01v8_lvt
#(
.L ( Lsw ) ,
.W ( Wsw ) ,
.nf ( nsw ) ,
.mult ( 1 ) ,
.ad ( "'int((nf+1)/2) ) ,
.pd ( "'2*int((nf+1)/2) ) ,
.as ( "'int((nf+2)/2) ) ,
.ps ( "'2*int((nf+2)/2) ) ,
.nrd ( "'0.29 ) ,
.nrs ( "'0.29 ) ,
.sa ( 0 ) ,
.sb ( 0 ) ,
.sd ( 0 ) ,
.model ( nfet_01v8_lvt ) ,
.spiceprefix ( X )
)
M1 (
 .D( net1 ),
 .G( sw ),
 .S( net2 ),
 .B( GND )
);


nfet_01v8_lvt
#(
.L ( Wpd ) ,
.W ( Wpd ) ,
.nf ( npd ) ,
.mult ( 1 ) ,
.ad ( "'int((nf+1)/2) ) ,
.pd ( "'2*int((nf+1)/2) ) ,
.as ( "'int((nf+2)/2) ) ,
.ps ( "'2*int((nf+2)/2) ) ,
.nrd ( "'0.29 ) ,
.nrs ( "'0.29 ) ,
.sa ( 0 ) ,
.sb ( 0 ) ,
.sd ( 0 ) ,
.model ( nfet_01v8_lvt ) ,
.spiceprefix ( X )
)
M2 (
 .D( GND ),
 .G( sw ),
 .S( net1 ),
 .B( GND )
);


nfet_01v8_lvt
#(
.L ( Lpd ) ,
.W ( Wpd ) ,
.nf ( npd ) ,
.mult ( 1 ) ,
.ad ( "'int((nf+1)/2) ) ,
.pd ( "'2*int((nf+1)/2) ) ,
.as ( "'int((nf+2)/2) ) ,
.ps ( "'2*int((nf+2)/2) ) ,
.nrd ( "'0.29 ) ,
.nrs ( "'0.29 ) ,
.sa ( 0 ) ,
.sb ( 0 ) ,
.sd ( 0 ) ,
.model ( nfet_01v8_lvt ) ,
.spiceprefix ( X )
)
M3 (
 .D( net2 ),
 .G( sw ),
 .S( GND ),
 .B( GND )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( Mc ) ,
.spiceprefix ( X )
)
C1 (
 .c0( outn ),
 .c1( net2 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( Mc ) ,
.spiceprefix ( X )
)
C2 (
 .c0( net1 ),
 .c1( outp )
);

endmodule
