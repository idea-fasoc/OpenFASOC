.subckt DCDC_COMP VPWR VGND VIN VIP VOP CLK
X0 VCM CLK VGND VGND  sky130_fd_pr__nfet_01v8 w=840000u l=150000u m=2
X1 VMP VIN VCM VGND  sky130_fd_pr__nfet_01v8 w=420000u l=150000u m=2
X2 VMN VIP VCM VGND  sky130_fd_pr__nfet_01v8 w=420000u l=150000u m=2
X3 VOP VON VMP VGND  sky130_fd_pr__nfet_01v8 w=420000u l=150000u m=2
X4 VON VOP VMN VGND  sky130_fd_pr__nfet_01v8 w=420000u l=150000u m=2
X5 VOP VON VPWR VPWR  sky130_fd_pr__pfet_01v8 w=420000u l=150000u m=2
X6 VON VOP VPWR VPWR  sky130_fd_pr__pfet_01v8 w=420000u l=150000u m=2
X7 VOP CLK VPWR VPWR  sky130_fd_pr__pfet_01v8 w=420000u l=150000u m=2
X8 VON CLK VPWR VPWR  sky130_fd_pr__pfet_01v8 w=420000u l=150000u m=2
X9 VMP CLK VPWR VPWR  sky130_fd_pr__pfet_01v8 w=420000u l=150000u m=2
X10 VMN CLK VPWR VPWR sky130_fd_pr__pfet_01v8 w=420000u l=150000u m=2
.ends DCDC_COMP
