// sch_path: /home/chandru/Tools/OpenFASOC/generators/lc-dco/xschem_rundir/Ind_top_ver.sch
module Ind_top (
  inout wire outn,
  inout wire outp,
  inout wire VDD
);

wire net2  ;

ind_generic
#(
.model ( ind_05_220 )
)
L1 (
 .b( outp ),
 .b( outn ),
 .ct( VDD )
);

endmodule
