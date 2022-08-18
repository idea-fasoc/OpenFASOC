* 2:1 stage: PMOS SWITCH
.subckt DCDC_XSW_PMOS VPB clk clkb vIN vOUT0 vOUT1
x0 int_sw0 int_sw1 vIN VPB sky130_fd_pr__pfet_01v8 w=420000u l=150000u
x1 int_sw1 int_sw0 vIN VPB sky130_fd_pr__pfet_01v8 w=420000u l=150000u
x2 vOUT0 int_sw0 vIN VPB sky130_fd_pr__pfet_01v8 w=1260000u l=150000u
x3 vOUT1 int_sw1 vIN VPB sky130_fd_pr__pfet_01v8 w=1260000u l=150000u
x4 clkb int_sw0 clkb clkb sky130_fd_pr__pfet_01v8 w=2100000u l=2100000u
x5 clk int_sw1 clk clk sky130_fd_pr__pfet_01v8 w=2100000u l=2100000u
.ends DCDC_XSW_PMOS

* 2:1 stage: NMOS SWITCH
.subckt DCDC_XSW_NMOS VNB clk clkb vIN vOUT0 vOUT1
x0 int_sw0 int_sw1 vIN VNB sky130_fd_pr__nfet_01v8 w=420000u l=150000u
x1 int_sw1 int_sw0 vIN VNB sky130_fd_pr__nfet_01v8 w=420000u l=150000u
x2 vOUT0 int_sw0 vIN VNB sky130_fd_pr__nfet_01v8 w=840000u l=150000u
x3 vOUT1 int_sw1 vIN VNB sky130_fd_pr__nfet_01v8 w=840000u l=150000u
x4 clkb int_sw0 clkb clkb sky130_fd_pr__pfet_01v8 w=2100000u l=2100000u
x5 clk int_sw1 clk clk sky130_fd_pr__pfet_01v8 w=2100000u l=2100000u
.ends DCDC_XSW_NMOS

*2:1 converter: DCDC_HUNIT_CONV2to1
.subckt DCDC_HUNIT_CONV2to1 VGND VPWR clk0 clk0b clk1 clk1b y0 y1 vhigh vlow
x0 VPWR clk1b clk0b vhigh y0 y1 DCDC_XSW_PMOS
x1 VGND clk0 clk1 vlow y0 y1 DCDC_XSW_NMOS
.ends DCDC_HUNIT_CONV2to1

*2:1 converter: DCDC_CONV2TO1
.subckt DCDC_CONV2TO1 VGND VPWR clk0 clk0b clk1 clk1b y0_top y1_top y0_bot y1_bot vhigh vmid vlow
x0 VGND VPWR clk0 clk0b clk1 clk1b y0_top y1_top vhigh vmid DCDC_HUNIT_CONV2to1
x1 VGND VPWR clk0 clk0b clk1 clk1b y0_bot y1_bot vmid vlow DCDC_HUNIT_CONV2to1
.ends DCDC_CONV2TO1
