module ldo(
   input        clk,
   input        reset,

   input  [1:0] mode_sel,         // 2'b00 (Comparator & PT Array Test Mode)
                                  // 2'b01 (Controller Test Mode)
                                  // 2'b1X (LDO Run Mode)

   input        std_ctrl_in,      // Standalone Controller Test Input
   input  [8:0] std_pt_in_cnt,    // Standalone PT Array Test Input

   output       cmp_out,          // Comparator Output
   output [8:0] ctrl_out,         // Controller Output Count

   input        VREF              // Reference Voltage
);

   parameter integer ARRSZ = 23;

   reg             ctrl_in, mode;
   reg [ARRSZ-1:0] pt_ctrl_word;

   LDO_COMPARATOR cmp1 (.CLK(clk),
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

   always @(*) begin
      mode = mode_sel[0] || mode_sel[1];

      if (mode_sel[1])
         ctrl_in        = cmp_out;
      else
         ctrl_in        = std_ctrl_in;
   end

endmodule
