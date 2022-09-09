// sch_path: /home/chandru/Tools/OpenFASOC/generators/lc-dco/xschem_rundir/swcap_3M2C_scaled.sch
module swcap_3M2C_scaled (
  output wire outn,
  output wire outp,
  inout wire GND,
  input wire [7:0] sw
);

wire [1:0] net10  ;
wire [2:0] net11  ;
wire [2:0] net12  ;
wire [2:0] net13  ;
wire [2:0] net14  ;
wire [3:0] net15  ;
wire [3:0] net16  ;
wire net1  ;
wire net2  ;
wire net3  ;
wire net4  ;
wire net5  ;
wire net6  ;
wire net7  ;
wire net8  ;
wire [1:0] net9  ;

cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C2_7 (
 .c0( net2 ),
 .c1( outn )
);

cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C2_6 (
 .c0( net2 ),
 .c1( outn )
);

cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C2_5 (
 .c0( net2 ),
 .c1( outn )
);

cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C2_4 (
 .c0( net2 ),
 .c1( outn )
);

cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C2_3 (
 .c0( net2 ),
 .c1( outn )
);

cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C2_2 (
 .c0( net2 ),
 .c1( outn )
);

cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C2_1 (
 .c0( net2 ),
 .c1( outn )
);

cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C2_0 (
 .c0( net2 ),
 .c1( outn )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M6 (
 .D( net1 ),
 .G( sw[0] ),
 .S( net2 )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
 .D( GND ),
 .G( sw[0] ),
 .S( net1 )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
 .G( sw[0] ),
 .S( net2 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C1_7 (
 .c0( outp ),
 .c1( net1 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C1_6 (
 .c0( outp ),
 .c1( net1 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C1_5 (
 .c0( outp ),
 .c1( net1 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C1_4 (
 .c0( outp ),
 .c1( net1 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C1_3 (
 .c0( outp ),
 .c1( net1 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C1_2 (
 .c0( outp ),
 .c1( net1 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C1_1 (
 .c0( outp ),
 .c1( net1 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C1_0 (
 .c0( outp ),
 .c1( net1 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C4_15 (
 .c0( net4 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C4_14 (
 .c0( net4 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C4_13 (
 .c0( net4 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C4_12 (
 .c0( net4 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C4_11 (
 .c0( net4 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C4_10 (
 .c0( net4 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C4_9 (
 .c0( net4 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C4_8 (
 .c0( net4 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C4_7 (
 .c0( net4 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C4_6 (
 .c0( net4 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C4_5 (
 .c0( net4 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C4_4 (
 .c0( net4 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C4_3 (
 .c0( net4 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C4_2 (
 .c0( net4 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C4_1 (
 .c0( net4 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C4_0 (
 .c0( net4 ),
 .c1( outn )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 1 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
 .D( net3 ),
 .G( sw[1] ),
 .S( net4 )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M4 (
 .D( GND ),
 .G( sw[1] ),
 .S( net3 )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M5 (
 .D( GND ),
 .G( sw[1] ),
 .S( net4 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C3_15 (
 .c0( outp ),
 .c1( net3 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C3_14 (
 .c0( outp ),
 .c1( net3 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C3_13 (
 .c0( outp ),
 .c1( net3 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C3_12 (
 .c0( outp ),
 .c1( net3 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C3_11 (
 .c0( outp ),
 .c1( net3 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C3_10 (
 .c0( outp ),
 .c1( net3 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C3_9 (
 .c0( outp ),
 .c1( net3 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C3_8 (
 .c0( outp ),
 .c1( net3 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C3_7 (
 .c0( outp ),
 .c1( net3 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C3_6 (
 .c0( outp ),
 .c1( net3 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C3_5 (
 .c0( outp ),
 .c1( net3 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C3_4 (
 .c0( outp ),
 .c1( net3 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C3_3 (
 .c0( outp ),
 .c1( net3 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C3_2 (
 .c0( outp ),
 .c1( net3 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C3_1 (
 .c0( outp ),
 .c1( net3 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C3_0 (
 .c0( outp ),
 .c1( net3 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_31 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_30 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_29 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_28 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_27 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_26 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_25 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_24 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_23 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_22 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_21 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_20 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_19 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_18 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_17 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_16 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_15 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_14 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_13 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_12 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_11 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_10 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_9 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_8 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_7 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_6 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_5 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_4 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_3 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_2 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_1 (
 .c0( net6 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C6_0 (
 .c0( net6 ),
 .c1( outn )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 6 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M7 (
 .D( net5 ),
 .G( sw[2] ),
 .S( net6 )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M8 (
 .D( GND ),
 .G( sw[2] ),
 .S( net5 )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M9 (
 .D( GND ),
 .G( sw[2] ),
 .S( net6 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_31 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_30 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_29 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_28 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_27 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_26 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_25 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_24 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_23 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_22 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_21 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_20 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_19 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_18 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_17 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_16 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_15 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_14 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_13 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_12 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_11 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_10 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_9 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_8 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_7 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_6 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_5 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_4 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_3 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_2 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_1 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C5_0 (
 .c0( outp ),
 .c1( net5 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_63 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_62 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_61 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_60 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_59 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_58 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_57 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_56 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_55 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_54 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_53 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_52 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_51 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_50 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_49 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_48 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_47 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_46 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_45 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_44 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_43 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_42 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_41 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_40 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_39 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_38 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_37 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_36 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_35 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_34 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_33 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_32 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_31 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_30 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_29 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_28 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_27 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_26 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_25 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_24 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_23 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_22 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_21 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_20 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_19 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_18 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_17 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_16 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_15 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_14 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_13 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_12 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_11 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_10 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_9 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_8 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_7 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_6 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_5 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_4 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_3 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_2 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_1 (
 .c0( net8 ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C8_0 (
 .c0( net8 ),
 .c1( outn )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 6 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M10 (
 .D( net7 ),
 .G( sw[3] ),
 .S( net8 )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M11 (
 .D( GND ),
 .G( sw[3] ),
 .S( net7 )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M12 (
 .D( GND ),
 .G( sw[3] ),
 .S( net8 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_63 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_62 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_61 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_60 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_59 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_58 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_57 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_56 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_55 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_54 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_53 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_52 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_51 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_50 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_49 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_48 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_47 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_46 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_45 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_44 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_43 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_42 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_41 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_40 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_39 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_38 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_37 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_36 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_35 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_34 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_33 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_32 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_31 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_30 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_29 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_28 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_27 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_26 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_25 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_24 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_23 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_22 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_21 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_20 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_19 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_18 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_17 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_16 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_15 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_14 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_13 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_12 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_11 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_10 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_9 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_8 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_7 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_6 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_5 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_4 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_3 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_2 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_1 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C7_0 (
 .c0( outp ),
 .c1( net7 )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_127 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_126 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_125 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_124 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_123 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_122 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_121 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_120 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_119 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_118 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_117 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_116 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_115 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_114 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_113 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_112 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_111 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_110 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_109 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_108 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_107 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_106 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_105 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_104 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_103 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_102 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_101 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_100 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_99 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_98 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_97 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_96 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_95 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_94 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_93 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_92 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_91 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_90 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_89 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_88 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_87 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_86 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_85 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_84 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_83 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_82 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_81 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_80 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_79 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_78 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_77 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_76 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_75 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_74 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_73 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_72 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_71 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_70 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_69 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_68 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_67 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_66 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_65 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_64 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_63 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_62 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_61 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_60 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_59 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_58 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_57 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_56 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_55 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_54 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_53 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_52 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_51 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_50 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_49 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_48 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_47 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_46 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_45 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_44 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_43 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_42 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_41 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_40 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_39 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_38 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_37 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_36 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_35 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_34 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_33 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_32 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_31 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_30 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_29 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_28 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_27 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_26 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_25 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_24 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_23 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_22 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_21 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_20 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_19 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_18 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_17 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_16 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_15 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_14 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_13 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_12 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_11 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_10 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_9 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_8 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_7 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_6 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_5 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_4 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_3 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_2 (
 .c0( net10[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_1 (
 .c0( net10[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C10_0 (
 .c0( net10[0] ),
 .c1( outn )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 8 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M13_1 (
 .D( net9[1] ),
 .G( sw[4] ),
 .S( net10[1] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 8 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M13_0 (
 .D( net9[0] ),
 .G( sw[4] ),
 .S( net10[0] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M14_2 (
 .D( GND ),
 .G( sw[4] ),
 .S( net9[1] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M14_1 (
 .D( GND ),
 .G( sw[4] ),
 .S( net9[0] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M14_0 (
 .D( GND ),
 .G( sw[4] ),
 .S( net9[1] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M15_2 (
 .D( GND ),
 .G( sw[4] ),
 .S( net10[1] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M15_1 (
 .D( GND ),
 .G( sw[4] ),
 .S( net10[0] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M15_0 (
 .D( GND ),
 .G( sw[4] ),
 .S( net10[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_127 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_126 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_125 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_124 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_123 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_122 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_121 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_120 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_119 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_118 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_117 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_116 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_115 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_114 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_113 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_112 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_111 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_110 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_109 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_108 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_107 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_106 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_105 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_104 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_103 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_102 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_101 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_100 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_99 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_98 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_97 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_96 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_95 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_94 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_93 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_92 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_91 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_90 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_89 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_88 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_87 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_86 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_85 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_84 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_83 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_82 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_81 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_80 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_79 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_78 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_77 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_76 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_75 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_74 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_73 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_72 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_71 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_70 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_69 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_68 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_67 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_66 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_65 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_64 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_63 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_62 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_61 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_60 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_59 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_58 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_57 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_56 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_55 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_54 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_53 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_52 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_51 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_50 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_49 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_48 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_47 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_46 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_45 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_44 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_43 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_42 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_41 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_40 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_39 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_38 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_37 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_36 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_35 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_34 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_33 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_32 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_31 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_30 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_29 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_28 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_27 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_26 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_25 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_24 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_23 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_22 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_21 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_20 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_19 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_18 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_17 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_16 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_15 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_14 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_13 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_12 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_11 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_10 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_9 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_8 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_7 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_6 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_5 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_4 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_3 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_2 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_1 (
 .c0( outp ),
 .c1( net9[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C9_0 (
 .c0( outp ),
 .c1( net9[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_255 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_254 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_253 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_252 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_251 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_250 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_249 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_248 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_247 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_246 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_245 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_244 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_243 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_242 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_241 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_240 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_239 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_238 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_237 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_236 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_235 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_234 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_233 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_232 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_231 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_230 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_229 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_228 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_227 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_226 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_225 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_224 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_223 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_222 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_221 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_220 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_219 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_218 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_217 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_216 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_215 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_214 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_213 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_212 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_211 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_210 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_209 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_208 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_207 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_206 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_205 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_204 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_203 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_202 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_201 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_200 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_199 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_198 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_197 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_196 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_195 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_194 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_193 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_192 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_191 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_190 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_189 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_188 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_187 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_186 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_185 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_184 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_183 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_182 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_181 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_180 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_179 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_178 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_177 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_176 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_175 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_174 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_173 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_172 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_171 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_170 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_169 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_168 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_167 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_166 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_165 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_164 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_163 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_162 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_161 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_160 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_159 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_158 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_157 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_156 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_155 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_154 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_153 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_152 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_151 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_150 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_149 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_148 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_147 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_146 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_145 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_144 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_143 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_142 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_141 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_140 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_139 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_138 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_137 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_136 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_135 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_134 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_133 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_132 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_131 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_130 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_129 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_128 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_127 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_126 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_125 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_124 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_123 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_122 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_121 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_120 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_119 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_118 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_117 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_116 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_115 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_114 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_113 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_112 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_111 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_110 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_109 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_108 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_107 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_106 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_105 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_104 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_103 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_102 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_101 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_100 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_99 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_98 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_97 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_96 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_95 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_94 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_93 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_92 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_91 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_90 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_89 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_88 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_87 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_86 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_85 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_84 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_83 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_82 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_81 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_80 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_79 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_78 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_77 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_76 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_75 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_74 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_73 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_72 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_71 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_70 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_69 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_68 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_67 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_66 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_65 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_64 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_63 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_62 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_61 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_60 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_59 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_58 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_57 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_56 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_55 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_54 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_53 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_52 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_51 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_50 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_49 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_48 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_47 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_46 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_45 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_44 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_43 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_42 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_41 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_40 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_39 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_38 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_37 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_36 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_35 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_34 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_33 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_32 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_31 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_30 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_29 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_28 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_27 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_26 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_25 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_24 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_23 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_22 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_21 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_20 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_19 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_18 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_17 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_16 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_15 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_14 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_13 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_12 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_11 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_10 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_9 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_8 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_7 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_6 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_5 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_4 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_3 (
 .c0( net12[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_2 (
 .c0( net12[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_1 (
 .c0( net12[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C12_0 (
 .c0( net12[2] ),
 .c1( outn )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 11 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M16_2 (
 .D( net11[2] ),
 .G( sw[5] ),
 .S( net12[2] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 11 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M16_1 (
 .D( net11[1] ),
 .G( sw[5] ),
 .S( net12[1] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 11 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M16_0 (
 .D( net11[0] ),
 .G( sw[5] ),
 .S( net12[0] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M17_2 (
 .D( GND ),
 .G( sw[5] ),
 .S( net11[2] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M17_1 (
 .D( GND ),
 .G( sw[5] ),
 .S( net11[1] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M17_0 (
 .D( GND ),
 .G( sw[5] ),
 .S( net11[0] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M18_2 (
 .D( GND ),
 .G( sw[5] ),
 .S( net12[2] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M18_1 (
 .D( GND ),
 .G( sw[5] ),
 .S( net12[1] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M18_0 (
 .D( GND ),
 .G( sw[5] ),
 .S( net12[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_255 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_254 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_253 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_252 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_251 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_250 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_249 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_248 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_247 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_246 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_245 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_244 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_243 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_242 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_241 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_240 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_239 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_238 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_237 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_236 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_235 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_234 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_233 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_232 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_231 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_230 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_229 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_228 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_227 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_226 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_225 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_224 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_223 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_222 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_221 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_220 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_219 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_218 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_217 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_216 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_215 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_214 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_213 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_212 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_211 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_210 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_209 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_208 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_207 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_206 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_205 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_204 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_203 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_202 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_201 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_200 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_199 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_198 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_197 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_196 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_195 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_194 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_193 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_192 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_191 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_190 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_189 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_188 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_187 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_186 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_185 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_184 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_183 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_182 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_181 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_180 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_179 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_178 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_177 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_176 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_175 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_174 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_173 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_172 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_171 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_170 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_169 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_168 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_167 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_166 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_165 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_164 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_163 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_162 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_161 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_160 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_159 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_158 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_157 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_156 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_155 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_154 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_153 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_152 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_151 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_150 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_149 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_148 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_147 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_146 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_145 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_144 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_143 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_142 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_141 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_140 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_139 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_138 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_137 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_136 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_135 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_134 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_133 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_132 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_131 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_130 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_129 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_128 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_127 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_126 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_125 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_124 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_123 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_122 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_121 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_120 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_119 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_118 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_117 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_116 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_115 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_114 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_113 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_112 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_111 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_110 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_109 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_108 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_107 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_106 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_105 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_104 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_103 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_102 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_101 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_100 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_99 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_98 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_97 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_96 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_95 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_94 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_93 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_92 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_91 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_90 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_89 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_88 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_87 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_86 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_85 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_84 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_83 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_82 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_81 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_80 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_79 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_78 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_77 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_76 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_75 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_74 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_73 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_72 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_71 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_70 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_69 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_68 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_67 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_66 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_65 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_64 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_63 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_62 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_61 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_60 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_59 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_58 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_57 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_56 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_55 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_54 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_53 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_52 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_51 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_50 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_49 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_48 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_47 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_46 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_45 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_44 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_43 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_42 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_41 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_40 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_39 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_38 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_37 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_36 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_35 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_34 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_33 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_32 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_31 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_30 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_29 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_28 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_27 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_26 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_25 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_24 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_23 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_22 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_21 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_20 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_19 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_18 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_17 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_16 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_15 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_14 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_13 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_12 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_11 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_10 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_9 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_8 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_7 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_6 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_5 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_4 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_3 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_2 (
 .c0( outp ),
 .c1( net11[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_1 (
 .c0( outp ),
 .c1( net11[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C11_0 (
 .c0( outp ),
 .c1( net11[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_511 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_510 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_509 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_508 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_507 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_506 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_505 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_504 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_503 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_502 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_501 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_500 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_499 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_498 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_497 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_496 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_495 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_494 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_493 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_492 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_491 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_490 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_489 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_488 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_487 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_486 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_485 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_484 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_483 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_482 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_481 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_480 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_479 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_478 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_477 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_476 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_475 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_474 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_473 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_472 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_471 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_470 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_469 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_468 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_467 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_466 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_465 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_464 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_463 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_462 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_461 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_460 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_459 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_458 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_457 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_456 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_455 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_454 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_453 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_452 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_451 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_450 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_449 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_448 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_447 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_446 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_445 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_444 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_443 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_442 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_441 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_440 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_439 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_438 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_437 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_436 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_435 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_434 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_433 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_432 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_431 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_430 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_429 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_428 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_427 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_426 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_425 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_424 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_423 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_422 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_421 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_420 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_419 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_418 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_417 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_416 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_415 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_414 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_413 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_412 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_411 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_410 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_409 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_408 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_407 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_406 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_405 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_404 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_403 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_402 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_401 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_400 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_399 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_398 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_397 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_396 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_395 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_394 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_393 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_392 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_391 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_390 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_389 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_388 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_387 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_386 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_385 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_384 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_383 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_382 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_381 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_380 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_379 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_378 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_377 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_376 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_375 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_374 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_373 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_372 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_371 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_370 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_369 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_368 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_367 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_366 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_365 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_364 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_363 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_362 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_361 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_360 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_359 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_358 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_357 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_356 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_355 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_354 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_353 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_352 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_351 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_350 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_349 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_348 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_347 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_346 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_345 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_344 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_343 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_342 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_341 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_340 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_339 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_338 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_337 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_336 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_335 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_334 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_333 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_332 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_331 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_330 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_329 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_328 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_327 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_326 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_325 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_324 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_323 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_322 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_321 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_320 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_319 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_318 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_317 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_316 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_315 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_314 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_313 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_312 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_311 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_310 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_309 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_308 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_307 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_306 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_305 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_304 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_303 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_302 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_301 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_300 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_299 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_298 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_297 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_296 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_295 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_294 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_293 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_292 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_291 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_290 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_289 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_288 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_287 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_286 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_285 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_284 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_283 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_282 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_281 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_280 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_279 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_278 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_277 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_276 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_275 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_274 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_273 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_272 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_271 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_270 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_269 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_268 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_267 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_266 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_265 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_264 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_263 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_262 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_261 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_260 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_259 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_258 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_257 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_256 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_255 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_254 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_253 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_252 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_251 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_250 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_249 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_248 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_247 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_246 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_245 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_244 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_243 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_242 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_241 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_240 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_239 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_238 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_237 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_236 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_235 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_234 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_233 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_232 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_231 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_230 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_229 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_228 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_227 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_226 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_225 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_224 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_223 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_222 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_221 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_220 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_219 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_218 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_217 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_216 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_215 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_214 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_213 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_212 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_211 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_210 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_209 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_208 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_207 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_206 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_205 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_204 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_203 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_202 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_201 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_200 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_199 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_198 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_197 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_196 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_195 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_194 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_193 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_192 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_191 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_190 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_189 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_188 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_187 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_186 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_185 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_184 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_183 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_182 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_181 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_180 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_179 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_178 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_177 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_176 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_175 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_174 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_173 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_172 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_171 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_170 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_169 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_168 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_167 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_166 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_165 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_164 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_163 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_162 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_161 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_160 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_159 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_158 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_157 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_156 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_155 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_154 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_153 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_152 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_151 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_150 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_149 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_148 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_147 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_146 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_145 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_144 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_143 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_142 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_141 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_140 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_139 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_138 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_137 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_136 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_135 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_134 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_133 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_132 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_131 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_130 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_129 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_128 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_127 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_126 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_125 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_124 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_123 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_122 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_121 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_120 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_119 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_118 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_117 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_116 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_115 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_114 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_113 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_112 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_111 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_110 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_109 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_108 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_107 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_106 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_105 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_104 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_103 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_102 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_101 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_100 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_99 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_98 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_97 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_96 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_95 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_94 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_93 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_92 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_91 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_90 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_89 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_88 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_87 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_86 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_85 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_84 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_83 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_82 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_81 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_80 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_79 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_78 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_77 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_76 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_75 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_74 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_73 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_72 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_71 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_70 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_69 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_68 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_67 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_66 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_65 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_64 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_63 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_62 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_61 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_60 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_59 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_58 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_57 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_56 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_55 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_54 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_53 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_52 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_51 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_50 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_49 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_48 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_47 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_46 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_45 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_44 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_43 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_42 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_41 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_40 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_39 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_38 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_37 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_36 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_35 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_34 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_33 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_32 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_31 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_30 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_29 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_28 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_27 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_26 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_25 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_24 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_23 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_22 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_21 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_20 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_19 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_18 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_17 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_16 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_15 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_14 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_13 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_12 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_11 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_10 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_9 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_8 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_7 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_6 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_5 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_4 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_3 (
 .c0( net14[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_2 (
 .c0( net14[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_1 (
 .c0( net14[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C14_0 (
 .c0( net14[1] ),
 .c1( outn )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 11 ) ,
.mult ( 2 ) ,
.body ( GND ) ,
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
M19_2 (
 .D( net13[2] ),
 .G( sw[6] ),
 .S( net14[2] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 11 ) ,
.mult ( 2 ) ,
.body ( GND ) ,
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
M19_1 (
 .D( net13[1] ),
 .G( sw[6] ),
 .S( net14[1] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 11 ) ,
.mult ( 2 ) ,
.body ( GND ) ,
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
M19_0 (
 .D( net13[0] ),
 .G( sw[6] ),
 .S( net14[0] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M20_2 (
 .D( GND ),
 .G( sw[6] ),
 .S( net13[2] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M20_1 (
 .D( GND ),
 .G( sw[6] ),
 .S( net13[1] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M20_0 (
 .D( GND ),
 .G( sw[6] ),
 .S( net13[0] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M21_2 (
 .D( GND ),
 .G( sw[6] ),
 .S( net14[2] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M21_1 (
 .D( GND ),
 .G( sw[6] ),
 .S( net14[1] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 1 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M21_0 (
 .D( GND ),
 .G( sw[6] ),
 .S( net14[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_511 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_510 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_509 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_508 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_507 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_506 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_505 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_504 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_503 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_502 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_501 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_500 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_499 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_498 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_497 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_496 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_495 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_494 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_493 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_492 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_491 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_490 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_489 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_488 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_487 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_486 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_485 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_484 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_483 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_482 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_481 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_480 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_479 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_478 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_477 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_476 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_475 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_474 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_473 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_472 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_471 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_470 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_469 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_468 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_467 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_466 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_465 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_464 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_463 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_462 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_461 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_460 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_459 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_458 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_457 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_456 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_455 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_454 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_453 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_452 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_451 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_450 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_449 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_448 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_447 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_446 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_445 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_444 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_443 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_442 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_441 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_440 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_439 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_438 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_437 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_436 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_435 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_434 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_433 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_432 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_431 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_430 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_429 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_428 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_427 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_426 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_425 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_424 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_423 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_422 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_421 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_420 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_419 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_418 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_417 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_416 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_415 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_414 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_413 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_412 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_411 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_410 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_409 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_408 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_407 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_406 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_405 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_404 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_403 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_402 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_401 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_400 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_399 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_398 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_397 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_396 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_395 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_394 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_393 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_392 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_391 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_390 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_389 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_388 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_387 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_386 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_385 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_384 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_383 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_382 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_381 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_380 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_379 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_378 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_377 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_376 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_375 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_374 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_373 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_372 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_371 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_370 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_369 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_368 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_367 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_366 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_365 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_364 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_363 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_362 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_361 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_360 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_359 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_358 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_357 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_356 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_355 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_354 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_353 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_352 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_351 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_350 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_349 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_348 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_347 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_346 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_345 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_344 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_343 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_342 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_341 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_340 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_339 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_338 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_337 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_336 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_335 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_334 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_333 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_332 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_331 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_330 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_329 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_328 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_327 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_326 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_325 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_324 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_323 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_322 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_321 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_320 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_319 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_318 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_317 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_316 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_315 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_314 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_313 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_312 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_311 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_310 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_309 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_308 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_307 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_306 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_305 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_304 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_303 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_302 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_301 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_300 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_299 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_298 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_297 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_296 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_295 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_294 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_293 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_292 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_291 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_290 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_289 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_288 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_287 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_286 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_285 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_284 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_283 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_282 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_281 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_280 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_279 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_278 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_277 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_276 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_275 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_274 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_273 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_272 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_271 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_270 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_269 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_268 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_267 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_266 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_265 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_264 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_263 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_262 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_261 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_260 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_259 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_258 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_257 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_256 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_255 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_254 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_253 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_252 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_251 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_250 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_249 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_248 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_247 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_246 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_245 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_244 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_243 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_242 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_241 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_240 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_239 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_238 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_237 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_236 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_235 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_234 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_233 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_232 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_231 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_230 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_229 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_228 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_227 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_226 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_225 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_224 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_223 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_222 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_221 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_220 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_219 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_218 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_217 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_216 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_215 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_214 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_213 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_212 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_211 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_210 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_209 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_208 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_207 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_206 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_205 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_204 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_203 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_202 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_201 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_200 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_199 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_198 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_197 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_196 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_195 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_194 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_193 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_192 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_191 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_190 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_189 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_188 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_187 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_186 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_185 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_184 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_183 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_182 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_181 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_180 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_179 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_178 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_177 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_176 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_175 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_174 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_173 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_172 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_171 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_170 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_169 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_168 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_167 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_166 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_165 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_164 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_163 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_162 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_161 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_160 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_159 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_158 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_157 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_156 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_155 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_154 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_153 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_152 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_151 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_150 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_149 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_148 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_147 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_146 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_145 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_144 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_143 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_142 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_141 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_140 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_139 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_138 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_137 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_136 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_135 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_134 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_133 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_132 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_131 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_130 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_129 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_128 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_127 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_126 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_125 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_124 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_123 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_122 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_121 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_120 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_119 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_118 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_117 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_116 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_115 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_114 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_113 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_112 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_111 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_110 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_109 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_108 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_107 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_106 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_105 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_104 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_103 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_102 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_101 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_100 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_99 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_98 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_97 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_96 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_95 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_94 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_93 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_92 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_91 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_90 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_89 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_88 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_87 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_86 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_85 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_84 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_83 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_82 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_81 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_80 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_79 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_78 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_77 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_76 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_75 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_74 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_73 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_72 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_71 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_70 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_69 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_68 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_67 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_66 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_65 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_64 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_63 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_62 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_61 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_60 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_59 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_58 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_57 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_56 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_55 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_54 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_53 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_52 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_51 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_50 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_49 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_48 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_47 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_46 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_45 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_44 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_43 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_42 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_41 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_40 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_39 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_38 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_37 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_36 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_35 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_34 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_33 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_32 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_31 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_30 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_29 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_28 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_27 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_26 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_25 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_24 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_23 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_22 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_21 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_20 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_19 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_18 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_17 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_16 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_15 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_14 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_13 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_12 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_11 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_10 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_9 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_8 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_7 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_6 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_5 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_4 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_3 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_2 (
 .c0( outp ),
 .c1( net13[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_1 (
 .c0( outp ),
 .c1( net13[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C13_0 (
 .c0( outp ),
 .c1( net13[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1023 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1022 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1021 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1020 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1019 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1018 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1017 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1016 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1015 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1014 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1013 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1012 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1011 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1010 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1009 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1008 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1007 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1006 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1005 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1004 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1003 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1002 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1001 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1000 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_999 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_998 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_997 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_996 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_995 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_994 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_993 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_992 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_991 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_990 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_989 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_988 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_987 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_986 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_985 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_984 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_983 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_982 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_981 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_980 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_979 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_978 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_977 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_976 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_975 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_974 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_973 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_972 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_971 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_970 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_969 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_968 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_967 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_966 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_965 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_964 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_963 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_962 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_961 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_960 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_959 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_958 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_957 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_956 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_955 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_954 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_953 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_952 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_951 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_950 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_949 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_948 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_947 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_946 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_945 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_944 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_943 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_942 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_941 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_940 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_939 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_938 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_937 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_936 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_935 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_934 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_933 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_932 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_931 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_930 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_929 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_928 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_927 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_926 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_925 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_924 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_923 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_922 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_921 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_920 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_919 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_918 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_917 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_916 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_915 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_914 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_913 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_912 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_911 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_910 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_909 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_908 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_907 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_906 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_905 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_904 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_903 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_902 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_901 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_900 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_899 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_898 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_897 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_896 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_895 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_894 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_893 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_892 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_891 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_890 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_889 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_888 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_887 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_886 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_885 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_884 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_883 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_882 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_881 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_880 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_879 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_878 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_877 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_876 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_875 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_874 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_873 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_872 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_871 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_870 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_869 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_868 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_867 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_866 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_865 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_864 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_863 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_862 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_861 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_860 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_859 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_858 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_857 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_856 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_855 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_854 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_853 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_852 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_851 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_850 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_849 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_848 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_847 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_846 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_845 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_844 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_843 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_842 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_841 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_840 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_839 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_838 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_837 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_836 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_835 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_834 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_833 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_832 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_831 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_830 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_829 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_828 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_827 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_826 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_825 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_824 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_823 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_822 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_821 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_820 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_819 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_818 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_817 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_816 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_815 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_814 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_813 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_812 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_811 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_810 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_809 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_808 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_807 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_806 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_805 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_804 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_803 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_802 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_801 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_800 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_799 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_798 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_797 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_796 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_795 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_794 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_793 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_792 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_791 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_790 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_789 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_788 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_787 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_786 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_785 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_784 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_783 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_782 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_781 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_780 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_779 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_778 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_777 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_776 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_775 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_774 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_773 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_772 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_771 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_770 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_769 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_768 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_767 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_766 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_765 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_764 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_763 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_762 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_761 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_760 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_759 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_758 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_757 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_756 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_755 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_754 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_753 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_752 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_751 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_750 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_749 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_748 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_747 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_746 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_745 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_744 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_743 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_742 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_741 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_740 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_739 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_738 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_737 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_736 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_735 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_734 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_733 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_732 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_731 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_730 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_729 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_728 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_727 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_726 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_725 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_724 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_723 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_722 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_721 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_720 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_719 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_718 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_717 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_716 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_715 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_714 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_713 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_712 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_711 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_710 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_709 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_708 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_707 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_706 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_705 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_704 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_703 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_702 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_701 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_700 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_699 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_698 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_697 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_696 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_695 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_694 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_693 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_692 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_691 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_690 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_689 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_688 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_687 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_686 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_685 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_684 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_683 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_682 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_681 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_680 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_679 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_678 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_677 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_676 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_675 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_674 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_673 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_672 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_671 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_670 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_669 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_668 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_667 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_666 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_665 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_664 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_663 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_662 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_661 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_660 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_659 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_658 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_657 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_656 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_655 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_654 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_653 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_652 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_651 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_650 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_649 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_648 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_647 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_646 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_645 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_644 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_643 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_642 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_641 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_640 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_639 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_638 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_637 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_636 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_635 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_634 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_633 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_632 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_631 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_630 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_629 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_628 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_627 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_626 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_625 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_624 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_623 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_622 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_621 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_620 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_619 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_618 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_617 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_616 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_615 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_614 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_613 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_612 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_611 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_610 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_609 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_608 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_607 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_606 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_605 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_604 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_603 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_602 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_601 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_600 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_599 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_598 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_597 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_596 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_595 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_594 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_593 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_592 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_591 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_590 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_589 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_588 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_587 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_586 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_585 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_584 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_583 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_582 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_581 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_580 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_579 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_578 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_577 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_576 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_575 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_574 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_573 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_572 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_571 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_570 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_569 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_568 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_567 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_566 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_565 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_564 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_563 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_562 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_561 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_560 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_559 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_558 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_557 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_556 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_555 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_554 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_553 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_552 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_551 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_550 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_549 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_548 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_547 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_546 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_545 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_544 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_543 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_542 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_541 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_540 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_539 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_538 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_537 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_536 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_535 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_534 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_533 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_532 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_531 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_530 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_529 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_528 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_527 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_526 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_525 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_524 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_523 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_522 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_521 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_520 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_519 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_518 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_517 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_516 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_515 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_514 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_513 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_512 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_511 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_510 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_509 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_508 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_507 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_506 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_505 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_504 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_503 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_502 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_501 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_500 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_499 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_498 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_497 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_496 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_495 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_494 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_493 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_492 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_491 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_490 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_489 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_488 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_487 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_486 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_485 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_484 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_483 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_482 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_481 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_480 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_479 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_478 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_477 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_476 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_475 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_474 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_473 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_472 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_471 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_470 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_469 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_468 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_467 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_466 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_465 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_464 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_463 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_462 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_461 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_460 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_459 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_458 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_457 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_456 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_455 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_454 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_453 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_452 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_451 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_450 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_449 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_448 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_447 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_446 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_445 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_444 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_443 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_442 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_441 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_440 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_439 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_438 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_437 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_436 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_435 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_434 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_433 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_432 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_431 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_430 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_429 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_428 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_427 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_426 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_425 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_424 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_423 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_422 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_421 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_420 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_419 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_418 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_417 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_416 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_415 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_414 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_413 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_412 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_411 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_410 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_409 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_408 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_407 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_406 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_405 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_404 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_403 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_402 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_401 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_400 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_399 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_398 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_397 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_396 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_395 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_394 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_393 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_392 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_391 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_390 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_389 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_388 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_387 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_386 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_385 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_384 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_383 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_382 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_381 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_380 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_379 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_378 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_377 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_376 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_375 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_374 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_373 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_372 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_371 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_370 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_369 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_368 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_367 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_366 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_365 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_364 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_363 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_362 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_361 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_360 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_359 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_358 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_357 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_356 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_355 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_354 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_353 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_352 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_351 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_350 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_349 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_348 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_347 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_346 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_345 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_344 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_343 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_342 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_341 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_340 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_339 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_338 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_337 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_336 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_335 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_334 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_333 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_332 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_331 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_330 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_329 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_328 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_327 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_326 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_325 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_324 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_323 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_322 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_321 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_320 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_319 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_318 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_317 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_316 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_315 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_314 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_313 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_312 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_311 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_310 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_309 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_308 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_307 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_306 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_305 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_304 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_303 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_302 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_301 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_300 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_299 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_298 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_297 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_296 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_295 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_294 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_293 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_292 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_291 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_290 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_289 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_288 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_287 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_286 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_285 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_284 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_283 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_282 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_281 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_280 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_279 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_278 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_277 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_276 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_275 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_274 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_273 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_272 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_271 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_270 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_269 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_268 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_267 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_266 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_265 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_264 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_263 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_262 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_261 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_260 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_259 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_258 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_257 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_256 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_255 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_254 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_253 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_252 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_251 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_250 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_249 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_248 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_247 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_246 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_245 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_244 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_243 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_242 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_241 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_240 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_239 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_238 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_237 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_236 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_235 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_234 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_233 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_232 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_231 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_230 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_229 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_228 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_227 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_226 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_225 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_224 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_223 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_222 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_221 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_220 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_219 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_218 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_217 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_216 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_215 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_214 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_213 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_212 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_211 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_210 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_209 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_208 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_207 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_206 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_205 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_204 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_203 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_202 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_201 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_200 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_199 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_198 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_197 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_196 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_195 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_194 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_193 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_192 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_191 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_190 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_189 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_188 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_187 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_186 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_185 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_184 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_183 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_182 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_181 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_180 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_179 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_178 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_177 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_176 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_175 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_174 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_173 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_172 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_171 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_170 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_169 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_168 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_167 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_166 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_165 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_164 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_163 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_162 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_161 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_160 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_159 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_158 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_157 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_156 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_155 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_154 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_153 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_152 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_151 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_150 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_149 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_148 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_147 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_146 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_145 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_144 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_143 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_142 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_141 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_140 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_139 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_138 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_137 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_136 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_135 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_134 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_133 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_132 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_131 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_130 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_129 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_128 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_127 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_126 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_125 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_124 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_123 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_122 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_121 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_120 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_119 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_118 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_117 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_116 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_115 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_114 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_113 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_112 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_111 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_110 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_109 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_108 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_107 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_106 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_105 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_104 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_103 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_102 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_101 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_100 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_99 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_98 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_97 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_96 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_95 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_94 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_93 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_92 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_91 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_90 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_89 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_88 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_87 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_86 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_85 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_84 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_83 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_82 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_81 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_80 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_79 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_78 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_77 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_76 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_75 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_74 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_73 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_72 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_71 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_70 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_69 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_68 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_67 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_66 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_65 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_64 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_63 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_62 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_61 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_60 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_59 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_58 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_57 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_56 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_55 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_54 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_53 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_52 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_51 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_50 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_49 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_48 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_47 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_46 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_45 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_44 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_43 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_42 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_41 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_40 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_39 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_38 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_37 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_36 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_35 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_34 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_33 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_32 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_31 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_30 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_29 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_28 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_27 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_26 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_25 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_24 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_23 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_22 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_21 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_20 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_19 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_18 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_17 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_16 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_15 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_14 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_13 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_12 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_11 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_10 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_9 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_8 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_7 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_6 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_5 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_4 (
 .c0( net16[0] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_3 (
 .c0( net16[3] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_2 (
 .c0( net16[2] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_1 (
 .c0( net16[1] ),
 .c1( outn )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C16_0 (
 .c0( net16[0] ),
 .c1( outn )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 11 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M22_3 (
 .D( net15[3] ),
 .G( sw[7] ),
 .S( net16[3] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 11 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M22_2 (
 .D( net15[2] ),
 .G( sw[7] ),
 .S( net16[2] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 11 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M22_1 (
 .D( net15[1] ),
 .G( sw[7] ),
 .S( net16[1] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 11 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M22_0 (
 .D( net15[0] ),
 .G( sw[7] ),
 .S( net16[0] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M23_3 (
 .D( GND ),
 .G( sw[7] ),
 .S( net15[3] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M23_2 (
 .D( GND ),
 .G( sw[7] ),
 .S( net15[2] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M23_1 (
 .D( GND ),
 .G( sw[7] ),
 .S( net15[1] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M23_0 (
 .D( GND ),
 .G( sw[7] ),
 .S( net15[0] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M24_3 (
 .D( GND ),
 .G( sw[7] ),
 .S( net16[3] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M24_2 (
 .D( GND ),
 .G( sw[7] ),
 .S( net16[2] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M24_1 (
 .D( GND ),
 .G( sw[7] ),
 .S( net16[1] )
);


nfet3_01v8_lvt
#(
.L ( 0.15 ) ,
.W ( 4.8 ) ,
.nf ( 2 ) ,
.mult ( 1 ) ,
.body ( GND ) ,
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
M24_0 (
 .D( GND ),
 .G( sw[7] ),
 .S( net16[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1023 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1022 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1021 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1020 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1019 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1018 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1017 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1016 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1015 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1014 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1013 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1012 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1011 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1010 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1009 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1008 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1007 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1006 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1005 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1004 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1003 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1002 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1001 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1000 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_999 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_998 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_997 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_996 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_995 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_994 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_993 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_992 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_991 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_990 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_989 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_988 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_987 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_986 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_985 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_984 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_983 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_982 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_981 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_980 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_979 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_978 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_977 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_976 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_975 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_974 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_973 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_972 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_971 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_970 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_969 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_968 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_967 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_966 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_965 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_964 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_963 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_962 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_961 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_960 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_959 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_958 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_957 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_956 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_955 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_954 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_953 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_952 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_951 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_950 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_949 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_948 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_947 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_946 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_945 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_944 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_943 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_942 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_941 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_940 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_939 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_938 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_937 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_936 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_935 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_934 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_933 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_932 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_931 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_930 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_929 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_928 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_927 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_926 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_925 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_924 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_923 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_922 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_921 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_920 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_919 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_918 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_917 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_916 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_915 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_914 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_913 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_912 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_911 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_910 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_909 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_908 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_907 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_906 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_905 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_904 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_903 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_902 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_901 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_900 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_899 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_898 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_897 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_896 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_895 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_894 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_893 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_892 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_891 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_890 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_889 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_888 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_887 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_886 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_885 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_884 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_883 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_882 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_881 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_880 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_879 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_878 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_877 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_876 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_875 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_874 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_873 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_872 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_871 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_870 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_869 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_868 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_867 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_866 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_865 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_864 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_863 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_862 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_861 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_860 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_859 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_858 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_857 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_856 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_855 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_854 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_853 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_852 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_851 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_850 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_849 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_848 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_847 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_846 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_845 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_844 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_843 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_842 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_841 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_840 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_839 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_838 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_837 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_836 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_835 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_834 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_833 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_832 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_831 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_830 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_829 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_828 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_827 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_826 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_825 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_824 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_823 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_822 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_821 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_820 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_819 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_818 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_817 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_816 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_815 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_814 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_813 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_812 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_811 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_810 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_809 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_808 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_807 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_806 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_805 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_804 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_803 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_802 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_801 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_800 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_799 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_798 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_797 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_796 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_795 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_794 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_793 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_792 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_791 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_790 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_789 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_788 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_787 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_786 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_785 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_784 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_783 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_782 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_781 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_780 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_779 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_778 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_777 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_776 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_775 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_774 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_773 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_772 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_771 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_770 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_769 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_768 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_767 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_766 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_765 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_764 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_763 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_762 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_761 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_760 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_759 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_758 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_757 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_756 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_755 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_754 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_753 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_752 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_751 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_750 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_749 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_748 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_747 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_746 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_745 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_744 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_743 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_742 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_741 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_740 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_739 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_738 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_737 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_736 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_735 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_734 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_733 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_732 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_731 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_730 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_729 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_728 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_727 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_726 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_725 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_724 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_723 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_722 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_721 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_720 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_719 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_718 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_717 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_716 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_715 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_714 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_713 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_712 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_711 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_710 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_709 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_708 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_707 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_706 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_705 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_704 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_703 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_702 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_701 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_700 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_699 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_698 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_697 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_696 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_695 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_694 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_693 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_692 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_691 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_690 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_689 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_688 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_687 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_686 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_685 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_684 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_683 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_682 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_681 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_680 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_679 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_678 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_677 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_676 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_675 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_674 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_673 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_672 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_671 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_670 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_669 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_668 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_667 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_666 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_665 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_664 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_663 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_662 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_661 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_660 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_659 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_658 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_657 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_656 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_655 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_654 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_653 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_652 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_651 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_650 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_649 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_648 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_647 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_646 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_645 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_644 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_643 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_642 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_641 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_640 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_639 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_638 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_637 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_636 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_635 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_634 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_633 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_632 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_631 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_630 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_629 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_628 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_627 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_626 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_625 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_624 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_623 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_622 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_621 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_620 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_619 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_618 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_617 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_616 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_615 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_614 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_613 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_612 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_611 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_610 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_609 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_608 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_607 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_606 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_605 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_604 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_603 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_602 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_601 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_600 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_599 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_598 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_597 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_596 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_595 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_594 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_593 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_592 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_591 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_590 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_589 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_588 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_587 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_586 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_585 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_584 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_583 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_582 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_581 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_580 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_579 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_578 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_577 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_576 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_575 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_574 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_573 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_572 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_571 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_570 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_569 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_568 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_567 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_566 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_565 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_564 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_563 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_562 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_561 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_560 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_559 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_558 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_557 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_556 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_555 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_554 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_553 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_552 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_551 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_550 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_549 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_548 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_547 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_546 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_545 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_544 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_543 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_542 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_541 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_540 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_539 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_538 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_537 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_536 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_535 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_534 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_533 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_532 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_531 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_530 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_529 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_528 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_527 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_526 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_525 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_524 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_523 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_522 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_521 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_520 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_519 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_518 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_517 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_516 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_515 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_514 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_513 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_512 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_511 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_510 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_509 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_508 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_507 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_506 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_505 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_504 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_503 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_502 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_501 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_500 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_499 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_498 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_497 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_496 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_495 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_494 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_493 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_492 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_491 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_490 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_489 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_488 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_487 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_486 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_485 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_484 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_483 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_482 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_481 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_480 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_479 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_478 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_477 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_476 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_475 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_474 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_473 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_472 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_471 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_470 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_469 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_468 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_467 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_466 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_465 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_464 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_463 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_462 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_461 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_460 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_459 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_458 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_457 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_456 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_455 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_454 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_453 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_452 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_451 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_450 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_449 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_448 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_447 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_446 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_445 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_444 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_443 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_442 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_441 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_440 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_439 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_438 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_437 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_436 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_435 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_434 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_433 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_432 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_431 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_430 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_429 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_428 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_427 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_426 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_425 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_424 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_423 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_422 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_421 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_420 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_419 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_418 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_417 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_416 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_415 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_414 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_413 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_412 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_411 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_410 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_409 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_408 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_407 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_406 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_405 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_404 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_403 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_402 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_401 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_400 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_399 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_398 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_397 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_396 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_395 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_394 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_393 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_392 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_391 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_390 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_389 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_388 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_387 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_386 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_385 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_384 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_383 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_382 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_381 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_380 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_379 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_378 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_377 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_376 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_375 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_374 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_373 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_372 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_371 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_370 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_369 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_368 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_367 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_366 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_365 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_364 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_363 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_362 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_361 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_360 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_359 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_358 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_357 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_356 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_355 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_354 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_353 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_352 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_351 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_350 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_349 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_348 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_347 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_346 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_345 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_344 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_343 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_342 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_341 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_340 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_339 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_338 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_337 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_336 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_335 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_334 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_333 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_332 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_331 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_330 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_329 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_328 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_327 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_326 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_325 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_324 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_323 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_322 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_321 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_320 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_319 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_318 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_317 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_316 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_315 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_314 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_313 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_312 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_311 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_310 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_309 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_308 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_307 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_306 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_305 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_304 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_303 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_302 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_301 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_300 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_299 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_298 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_297 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_296 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_295 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_294 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_293 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_292 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_291 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_290 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_289 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_288 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_287 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_286 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_285 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_284 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_283 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_282 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_281 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_280 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_279 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_278 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_277 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_276 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_275 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_274 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_273 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_272 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_271 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_270 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_269 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_268 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_267 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_266 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_265 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_264 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_263 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_262 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_261 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_260 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_259 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_258 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_257 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_256 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_255 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_254 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_253 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_252 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_251 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_250 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_249 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_248 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_247 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_246 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_245 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_244 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_243 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_242 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_241 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_240 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_239 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_238 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_237 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_236 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_235 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_234 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_233 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_232 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_231 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_230 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_229 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_228 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_227 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_226 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_225 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_224 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_223 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_222 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_221 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_220 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_219 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_218 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_217 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_216 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_215 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_214 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_213 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_212 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_211 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_210 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_209 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_208 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_207 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_206 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_205 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_204 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_203 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_202 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_201 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_200 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_199 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_198 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_197 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_196 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_195 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_194 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_193 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_192 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_191 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_190 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_189 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_188 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_187 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_186 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_185 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_184 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_183 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_182 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_181 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_180 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_179 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_178 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_177 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_176 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_175 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_174 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_173 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_172 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_171 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_170 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_169 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_168 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_167 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_166 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_165 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_164 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_163 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_162 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_161 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_160 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_159 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_158 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_157 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_156 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_155 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_154 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_153 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_152 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_151 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_150 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_149 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_148 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_147 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_146 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_145 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_144 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_143 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_142 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_141 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_140 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_139 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_138 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_137 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_136 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_135 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_134 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_133 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_132 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_131 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_130 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_129 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_128 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_127 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_126 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_125 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_124 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_123 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_122 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_121 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_120 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_119 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_118 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_117 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_116 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_115 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_114 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_113 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_112 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_111 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_110 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_109 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_108 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_107 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_106 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_105 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_104 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_103 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_102 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_101 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_100 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_99 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_98 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_97 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_96 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_95 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_94 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_93 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_92 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_91 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_90 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_89 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_88 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_87 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_86 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_85 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_84 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_83 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_82 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_81 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_80 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_79 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_78 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_77 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_76 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_75 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_74 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_73 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_72 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_71 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_70 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_69 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_68 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_67 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_66 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_65 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_64 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_63 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_62 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_61 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_60 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_59 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_58 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_57 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_56 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_55 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_54 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_53 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_52 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_51 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_50 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_49 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_48 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_47 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_46 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_45 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_44 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_43 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_42 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_41 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_40 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_39 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_38 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_37 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_36 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_35 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_34 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_33 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_32 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_31 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_30 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_29 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_28 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_27 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_26 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_25 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_24 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_23 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_22 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_21 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_20 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_19 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_18 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_17 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_16 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_15 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_14 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_13 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_12 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_11 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_10 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_9 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_8 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_7 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_6 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_5 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_4 (
 .c0( outp ),
 .c1( net15[0] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_3 (
 .c0( outp ),
 .c1( net15[3] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_2 (
 .c0( outp ),
 .c1( net15[2] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_1 (
 .c0( outp ),
 .c1( net15[1] )
);


cap_mim_m3_1
#(
.model ( cap_mim_m3_1 ) ,
.W ( 1 ) ,
.L ( 1 ) ,
.MF ( 1 ) ,
.spiceprefix ( X )
)
C15_0 (
 .c0( outp ),
 .c1( net15[0] )
);

endmodule
