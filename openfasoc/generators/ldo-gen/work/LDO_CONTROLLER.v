module LDO_CONTROLLER(
   clk, reset, mode, ctrl_in,
   std_pt_in_cnt, ctrl_word, ctrl_word_cnt);

   parameter integer ARRSZ = 23;

   input                        clk, reset, ctrl_in, mode;
   input      [8:0]             std_pt_in_cnt;
   output reg [8:0]             ctrl_word_cnt;
   output reg [ARRSZ-1:0]       ctrl_word;

   wire [ARRSZ-1:0] ctrl_rst = 23'h7fffff;

   always @(posedge clk) begin
      if (reset) begin
         ctrl_word              <= ctrl_rst;
         ctrl_word_cnt          <= 9'h0;
      end
      else if (mode) begin
         if (ctrl_in) begin
            ctrl_word           <= {1'b1, ctrl_word[ARRSZ-1:1]};
            if (~ctrl_word[0])
               ctrl_word_cnt    <= ctrl_word_cnt - 1;
         end
         else begin
            ctrl_word           <= {ctrl_word[ARRSZ-2:0], 1'b0};
            if (ctrl_word[ARRSZ-1])
               ctrl_word_cnt    <= ctrl_word_cnt + 1;
         end
      end
      else begin
         ctrl_word              <= ctrl_rst << std_pt_in_cnt;
         ctrl_word_cnt          <= std_pt_in_cnt;
      end
   end

endmodule
