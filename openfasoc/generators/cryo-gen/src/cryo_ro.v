
module cryo_ro (EN, OUT);
input  EN;
output OUT;

% for i in range(ninv + 1):
wire n${i + 1};
% endfor

${cell('nand2')} a_nand_0 ( .A(EN), .B(n${ninv + 1}), .Y(n1));

% for i in range(ninv):
${cell('inv')} a_inv_${i} ( .A(n${i + 1}), .Y(n${i + 2}));
% endfor

${cell('inv')} a_inv_out ( .A(n1), .Y(OUT));
endmodule
