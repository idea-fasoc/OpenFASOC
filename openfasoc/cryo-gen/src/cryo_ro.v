
module cryo_ro (EN, OUT);
input  EN;
output OUT;
@@ wire n@nn;
@@ @na a_nand_0 ( .A(EN), .B(n@n0), .Y(n1));
@@ @nb a_inv_@ni ( .A(n@n1), .Y(n@n2));
@@ @ng a_inv_out ( .A(n1), .Y(OUT));
endmodule
