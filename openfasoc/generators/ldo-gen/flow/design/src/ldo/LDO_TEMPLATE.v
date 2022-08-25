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

   parameter integer ARRSZ = 50;

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
    //[ARRSZ-1:0] 
   PT_UNIT_CELL pt_array_unit1 (.CTRL(pt_ctrl_word[0]));
   PT_UNIT_CELL pt_array_unit2 (.CTRL(pt_ctrl_word[1]));
   PT_UNIT_CELL pt_array_unit3 (.CTRL(pt_ctrl_word[2]));
   PT_UNIT_CELL pt_array_unit4 (.CTRL(pt_ctrl_word[3]));
   PT_UNIT_CELL pt_array_unit5 (.CTRL(pt_ctrl_word[4]));
   PT_UNIT_CELL pt_array_unit6 (.CTRL(pt_ctrl_word[5]));
   PT_UNIT_CELL pt_array_unit7 (.CTRL(pt_ctrl_word[6]));
   PT_UNIT_CELL pt_array_unit8 (.CTRL(pt_ctrl_word[7]));
   PT_UNIT_CELL pt_array_unit9 (.CTRL(pt_ctrl_word[8]));
   PT_UNIT_CELL pt_array_unit10 (.CTRL(pt_ctrl_word[9]));
   PT_UNIT_CELL pt_array_unit11 (.CTRL(pt_ctrl_word[10]));
   PT_UNIT_CELL pt_array_unit12 (.CTRL(pt_ctrl_word[11]));
   PT_UNIT_CELL pt_array_unit13 (.CTRL(pt_ctrl_word[12]));
   PT_UNIT_CELL pt_array_unit14 (.CTRL(pt_ctrl_word[13]));
   PT_UNIT_CELL pt_array_unit15 (.CTRL(pt_ctrl_word[14]));
   PT_UNIT_CELL pt_array_unit16 (.CTRL(pt_ctrl_word[15]));
   PT_UNIT_CELL pt_array_unit17 (.CTRL(pt_ctrl_word[16]));
   PT_UNIT_CELL pt_array_unit18 (.CTRL(pt_ctrl_word[17]));
   PT_UNIT_CELL pt_array_unit19 (.CTRL(pt_ctrl_word[18]));
   PT_UNIT_CELL pt_array_unit20 (.CTRL(pt_ctrl_word[19]));
   PT_UNIT_CELL pt_array_unit21 (.CTRL(pt_ctrl_word[20]));
   PT_UNIT_CELL pt_array_unit22 (.CTRL(pt_ctrl_word[21]));
   PT_UNIT_CELL pt_array_unit23 (.CTRL(pt_ctrl_word[22]));
   PT_UNIT_CELL pt_array_unit24 (.CTRL(pt_ctrl_word[23]));
   PT_UNIT_CELL pt_array_unit25 (.CTRL(pt_ctrl_word[24]));
   PT_UNIT_CELL pt_array_unit26 (.CTRL(pt_ctrl_word[25]));
   PT_UNIT_CELL pt_array_unit27 (.CTRL(pt_ctrl_word[26]));
   PT_UNIT_CELL pt_array_unit28 (.CTRL(pt_ctrl_word[27]));
   PT_UNIT_CELL pt_array_unit29 (.CTRL(pt_ctrl_word[28]));
   PT_UNIT_CELL pt_array_unit30 (.CTRL(pt_ctrl_word[29]));
   PT_UNIT_CELL pt_array_unit31 (.CTRL(pt_ctrl_word[30]));
   PT_UNIT_CELL pt_array_unit32 (.CTRL(pt_ctrl_word[31]));
   PT_UNIT_CELL pt_array_unit33 (.CTRL(pt_ctrl_word[32]));
   PT_UNIT_CELL pt_array_unit34 (.CTRL(pt_ctrl_word[33]));
   PT_UNIT_CELL pt_array_unit35 (.CTRL(pt_ctrl_word[34]));
   PT_UNIT_CELL pt_array_unit36 (.CTRL(pt_ctrl_word[35]));
   PT_UNIT_CELL pt_array_unit37 (.CTRL(pt_ctrl_word[36]));
   PT_UNIT_CELL pt_array_unit38 (.CTRL(pt_ctrl_word[37]));
   PT_UNIT_CELL pt_array_unit39 (.CTRL(pt_ctrl_word[38]));
   PT_UNIT_CELL pt_array_unit40 (.CTRL(pt_ctrl_word[39]));
   PT_UNIT_CELL pt_array_unit41 (.CTRL(pt_ctrl_word[40]));
   PT_UNIT_CELL pt_array_unit42 (.CTRL(pt_ctrl_word[41]));
   PT_UNIT_CELL pt_array_unit43 (.CTRL(pt_ctrl_word[42]));
   PT_UNIT_CELL pt_array_unit44 (.CTRL(pt_ctrl_word[43]));
   PT_UNIT_CELL pt_array_unit45 (.CTRL(pt_ctrl_word[44]));
   PT_UNIT_CELL pt_array_unit46 (.CTRL(pt_ctrl_word[45]));
   PT_UNIT_CELL pt_array_unit47 (.CTRL(pt_ctrl_word[46]));
   PT_UNIT_CELL pt_array_unit48 (.CTRL(pt_ctrl_word[47]));
   PT_UNIT_CELL pt_array_unit49 (.CTRL(pt_ctrl_word[48]));
   PT_UNIT_CELL pt_array_unit50 (.CTRL(pt_ctrl_word[49]));
   
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
