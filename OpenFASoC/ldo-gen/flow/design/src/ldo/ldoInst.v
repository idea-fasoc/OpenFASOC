module ldoInst(
   input        clk,
   input        reset,
   input	trim1,trim2,trim3,trim4,trim5,trim6,trim7,trim8,trim9,trim10,

   input  [1:0] mode_sel,         // 2'b00 (Comparator & PT Array Test Mode)
                                  // 2'b01 (Controller Test Mode)
                                  // 2'b1X (LDO Run Mode)

   input        std_ctrl_in,      // Standalone Controller Test Input
   input  [8:0] std_pt_in_cnt,    // Standalone PT Array Test Input

   output       cmp_out,          // Comparator Output
   output [8:0] ctrl_out         // Controller Output Count

   //input        VREF              // Reference Voltage
);

   parameter integer ARRSZ = 23;

   reg             ctrl_in, mode;
   reg [ARRSZ-1:0] pt_ctrl_word;

   wire 	   VREF;

   LDO_COMPARATOR_LATCH cmp1 (.CLK(clk),
                        .VREF(VREF),
                        .OUT(cmp_out));

   LDO_CONTROLLER #(.ARRSZ(ARRSZ))
             ctrl1 (.clk(clk),
                    .reset(reset),
                    .mode(mode),
                    .ctrl_in(ctrl_in),
                    .std_pt_in_cnt(std_pt_in_cnt),
                    .ctrl_word(pt_ctrl_word),
                    .ctrl_word_cnt(ctrl_out));

   PT_UNIT_CELL pt_array_unit [ARRSZ-1:0] (.CTRL(pt_ctrl_word));

   vref_gen_nmos_with_trim vref_gen (.trim1(trim1),
                          .trim2(trim2),
                          .trim3(trim3),
                          .trim4(trim4),
                          .trim5(trim5),
                          .trim6(trim6),
                          .trim7(trim7),
                          .trim8(trim8),
                          .trim9(trim9),
                          .trim10(trim10),
                          .vref(VREF)
                           );

   PMOS pmos_1 (.cmp_out(cmp_out));
   PMOS pmos_2 (.cmp_out(cmp_out));

   capacitor_test_nf cap_1 (.pin0(VREF));
   capacitor_test_nf cap_2 (.pin0(VREF));
   capacitor_test_nf cap_3 (.pin0(VREF));
   capacitor_test_nf cap_4 (.pin0(VREF));
   capacitor_test_nf cap_5 (.pin0(VREF));

   always @(*) begin
      mode = mode_sel[0] || mode_sel[1];

      if (mode_sel[1])
         ctrl_in        = cmp_out;
      else
         ctrl_in        = std_ctrl_in;
   end

endmodule
