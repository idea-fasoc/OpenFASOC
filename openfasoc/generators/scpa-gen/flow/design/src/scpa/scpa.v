module scpa(
   input    cap_sel,
   output   cap_out
);

//   parameter integer ARRSZ = 32;
//   logic [ARRSZ-1:0] cap_bot_in;

//   logic dum_inter;

//   always_ff @ (posedge dum_clk) begin
//      dum_inter <= ~dum_in;
//      dum_out <= dum_inter + dum_in;
//   end

//  genvar i;
//  generate
//     for (i = 0; i < ARRSZ; i = i + 1) begin
//         CLK_DRIVER clk_drv (.rf(clk), .sel(cap_sel[i]), .vout(cap_bot_in[i]));
         mimcaptut mimcaptut_inst_0 (.top(cap_out), .bot(cap_sel));
//   assign cap_out = ~cap_sel;
//     end
//  endgenerate


endmodule
