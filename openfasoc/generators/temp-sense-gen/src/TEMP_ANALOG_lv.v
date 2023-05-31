module TEMP_ANALOG_lv (EN, OUT, OUTB);
 input  EN;
// inout in_vin;
 output OUT, OUTB;
 wire  n;

% for i in range(ninv + 1):
wire n${i + 1};
% endfor

wire nx1, nx2, nx3, nb1, nb2;

${cell('nand2')} a_nand_0 ( .A(EN), .B(n${ninv + 1}), .Y(n1));

% for i in range(ninv):
${cell('inv')} a_inv_${i} ( .A(n${i + 1}), .Y(n${i + 2}));
% endfor

${cell('inv')} a_inv_m1 ( .A(n${ninv + 1}), .Y(nx1));
${cell('inv')} a_inv_m2 ( .A(n${ninv + 1}), .Y(nx2));
${cell('inv')} a_inv_m3 ( .A(nx2), .Y(nx3));
${cell('buf')} a_buf_3 ( .A(nx3), .X(nb2));
${cell('buf')} a_buf_0 ( .A(nx1), .X(nb1));
${cell('buf')} a_buf_1 ( .A(nb1), .X(OUT));
${cell('buf')} a_buf_2 ( .A(nb2), .X(OUTB));

endmodule
