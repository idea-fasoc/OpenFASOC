.subckt DCDC_DAC VPWR VGND VPWR RST D0 D1 D2 D3 D4 D5 VOUT
x0  V0  D0 VGND VGND  sky130_fd_pr__nfet_01v8 w=420000u l=150000u m=2
x1  V0  D0 VPWR VPWR  sky130_fd_pr__pfet_01v8 w=420000u l=150000u m=4
*C0  V0  VOUT 4f
x20 VOUT V0 sky130_fd_pr__cap_mim_m3_1 w=2 l=2
x2  V1  D1 VGND VGND  sky130_fd_pr__nfet_01v8 w=420000u l=150000u m=2
x3  V1  D1 VPWR VPWR  sky130_fd_pr__pfet_01v8 w=420000u l=150000u m=4
*C1  V1  VOUT 8f
x21 VOUT V1 sky130_fd_pr__cap_mim_m3_1 w=4 l=2
x4  V2  D2 VGND VGND  sky130_fd_pr__nfet_01v8 w=420000u l=150000u m=2
x5  V2  D2 VPWR VPWR  sky130_fd_pr__pfet_01v8 w=420000u l=150000u m=4
*C2  V2  VOUT 16f
x22 VOUT V2 sky130_fd_pr__cap_mim_m3_1 w=4 l=4
x6  V3  D3 VGND VGND  sky130_fd_pr__nfet_01v8 w=420000u l=150000u m=2
x7  V3  D3 VPWR VPWR  sky130_fd_pr__pfet_01v8 w=420000u l=150000u m=4
*C3  V3  VOUT 32f
x23 VOUT V3 sky130_fd_pr__cap_mim_m3_1 w=8 l=4
x8  V4  D4 VGND VGND  sky130_fd_pr__nfet_01v8 w=420000u l=150000u m=2
x9  V4  D4 VPWR VPWR  sky130_fd_pr__pfet_01v8 w=420000u l=150000u m=4
*C4  V4  VOUT 64f
x24 VOUT V4 sky130_fd_pr__cap_mim_m3_1 w=8 l=8
x10 V5  D5 VGND VGND  sky130_fd_pr__nfet_01v8 w=420000u l=150000u m=2
x11 V5  D5 VPWR VPWR  sky130_fd_pr__pfet_01v8 w=420000u l=150000u m=4
*C5  V5  VOUT 128f
x25 VOUT V5 sky130_fd_pr__cap_mim_m3_1 w=8 l=16
*C6  VGND VOUT 4f
x26 VOUT VGND sky130_fd_pr__cap_mim_m3_1 w=2 l=2
x12 VOUT RST VGND VGND sky130_fd_pr__nfet_01v8 w=420000u l=150000u m=2
.ends DCDC_DAC
