module TEMP_ANALOG_lv (EN, OUT, OUTB);
 input  EN;
// inout in_vin;
 output OUT, OUTB;
 wire  n;
@@ wire n@nn;
wire nx1, nx2, nx3, nb1, nb2;
@@ @na a_nand_0 ( .A(EN), .B(n@n0), .Y(n1));
@@ @nb a_inv_@ni ( .A(n@n1), .Y(n@n2));
@@ @ng a_inv_m1 ( .A(n@n3), .Y(nx1));
@@ @nk a_inv_m2 ( .A(n@n4), .Y(nx2));
@@ @nm a_inv_m3 ( .A(nx2), .Y(nx3));
@@ @np a_buf_3 ( .A(nx3), .nbout(nb2));
@@ @nc a_buf_0 ( .A(nx1), .nbout(nb1));
@@ @nd a_buf_1 ( .A(nb1), .nbout(OUT));
@@ @ne a_buf_2 ( .A(nb2), .nbout(OUTB));

endmodule
