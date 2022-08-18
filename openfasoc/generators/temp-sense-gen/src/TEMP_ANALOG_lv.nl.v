module TEMP_ANALOG_lv (EN, OUT, OUTB);
 input  EN;
// inout in_vin;
 output OUT, OUTB;
 wire  n;
wire n1;
wire n2;
wire n3;
wire n4;
wire n5;
wire n6;
wire n7;
wire nx1, nx2, nx3, nb1, nb2;
sky130_fd_sc_hd__nand2_1 a_nand_0 ( .A(EN), .B(n7), .Y(n1));
sky130_fd_sc_hd__inv_1 a_inv_0 ( .A(n1), .Y(n2));
sky130_fd_sc_hd__inv_1 a_inv_1 ( .A(n2), .Y(n3));
sky130_fd_sc_hd__inv_1 a_inv_2 ( .A(n3), .Y(n4));
sky130_fd_sc_hd__inv_1 a_inv_3 ( .A(n4), .Y(n5));
sky130_fd_sc_hd__inv_1 a_inv_4 ( .A(n5), .Y(n6));
sky130_fd_sc_hd__inv_1 a_inv_5 ( .A(n6), .Y(n7));
sky130_fd_sc_hd__inv_1 a_inv_m1 ( .A(n7), .Y(nx1));
sky130_fd_sc_hd__inv_1 a_inv_m2 ( .A(n7), .Y(nx2));
sky130_fd_sc_hd__inv_1 a_inv_m3 ( .A(nx2), .Y(nx3));
sky130_fd_sc_hd__buf_1 a_buf_3 ( .A(nx3), .X(nb2));
sky130_fd_sc_hd__buf_1 a_buf_0 ( .A(nx1), .X(nb1));
sky130_fd_sc_hd__buf_1 a_buf_1 ( .A(nb1), .X(OUT));
sky130_fd_sc_hd__buf_1 a_buf_2 ( .A(nb2), .X(OUTB));

endmodule
