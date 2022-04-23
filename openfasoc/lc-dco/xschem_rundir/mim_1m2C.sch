v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 60 -40 100 -40 { lab=outp}
N 160 -80 160 -40 { lab=#net1}
N 220 -80 220 -40 { lab=#net2}
N 220 -40 230 -40 { lab=#net2}
N 190 -140 190 -120 { lab=sw[0]}
N 190 -140 380 -140 { lab=sw[0]}
N 290 -40 300 -40 { lab=outn}
N 160 -200 160 -160 { lab=#net3}
N 220 -200 220 -160 { lab=#net4}
N 220 -160 230 -160 { lab=#net4}
N 190 -260 190 -240 { lab=sw[1]}
N 190 -260 390 -260 { lab=sw[1]}
N 160 -350 160 -310 { lab=#net5}
N 220 -350 220 -310 { lab=#net6}
N 220 -310 230 -310 { lab=#net6}
N 190 -410 190 -390 { lab=sw[2]}
N 190 -410 390 -410 { lab=sw[2]}
N 160 -480 160 -440 { lab=#net7}
N 220 -480 220 -440 { lab=#net8}
N 220 -440 230 -440 { lab=#net8}
N 190 -540 190 -520 { lab=sw[3]}
N 190 -540 390 -540 { lab=sw[3]}
N 290 -600 290 -40 { lab=outn}
N 100 -600 100 -40 { lab=outp}
N 160 -640 160 -600 { lab=#net9}
N 220 -640 220 -600 { lab=#net10}
N 220 -600 230 -600 { lab=#net10}
N 190 -700 190 -680 { lab=sw[4]}
N 190 -700 380 -700 { lab=sw[4]}
N 160 -760 160 -720 { lab=#net11}
N 220 -760 220 -720 { lab=#net12}
N 220 -720 230 -720 { lab=#net12}
N 190 -820 190 -800 { lab=sw[5]}
N 190 -820 390 -820 { lab=sw[5]}
N 160 -910 160 -870 { lab=#net13}
N 220 -910 220 -870 { lab=#net14}
N 220 -870 230 -870 { lab=#net14}
N 190 -970 190 -950 { lab=sw[6]}
N 190 -970 390 -970 { lab=sw[6]}
N 160 -1040 160 -1000 { lab=#net15}
N 220 -1040 220 -1000 { lab=#net16}
N 220 -1000 230 -1000 { lab=#net16}
N 190 -1100 190 -1080 { lab=sw[7]}
N 190 -1100 390 -1100 { lab=sw[7]}
N 100 -1170 100 -600 { lab=outp}
N 290 -1180 290 -600 { lab=outn}
C {sky130_fd_pr/cap_mim_m3_1.sym} 130 -40 3 0 {name=C1 model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {devices/opin.sym} 300 -40 0 0 {name=p2 lab=outn
}
C {devices/opin.sym} 60 -40 0 1 {name=p3 lab=outp}
C {sky130_fd_pr/cap_mim_m3_1.sym} 260 -40 3 0 {name=C2 model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 190 -100 3 1 {name=M6
L=0.15
W=1
nf=2
mult=1
body=GND
ad="'int((nf+1)/2) * W/nf * 0.29'"
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'"
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/cap_mim_m3_1.sym} 130 -160 3 0 {name=C3[1:0] model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {sky130_fd_pr/cap_mim_m3_1.sym} 260 -160 3 0 {name=C4[1:0] model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 190 -220 3 1 {name=M7
L=0.15
W=1
nf=4
mult=1
body=GND
ad="'int((nf+1)/2) * W/nf * 0.29'"
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'"
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {devices/lab_wire.sym} 360 -260 0 0 {name=l6 sig_type=std_logic lab=sw[1]}
C {devices/lab_wire.sym} 350 -140 0 0 {name=l7 sig_type=std_logic lab=sw[0]}
C {sky130_fd_pr/cap_mim_m3_1.sym} 130 -310 3 0 {name=C5[3:0] model=cap_mim_m3_1 W=1 L=1 MF=4 spiceprefix=X}
C {sky130_fd_pr/cap_mim_m3_1.sym} 260 -310 3 0 {name=C6[3:0] model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 190 -370 3 1 {name=M1
L=0.15
W=1
nf=4
mult=1
body=GND
ad="'int((nf+1)/2) * W/nf * 0.29'"
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'"
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {devices/lab_wire.sym} 360 -410 0 0 {name=l1 sig_type=std_logic lab=sw[2]}
C {sky130_fd_pr/cap_mim_m3_1.sym} 130 -440 3 0 {name=C7[7:0] model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {sky130_fd_pr/cap_mim_m3_1.sym} 260 -440 3 0 {name=C8[7:0] model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 190 -500 3 1 {name=M2
L=0.15
W=1
nf=7
mult=1
body=GND
ad="'int((nf+1)/2) * W/nf * 0.29'"
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'"
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {devices/lab_wire.sym} 360 -540 0 0 {name=l2 sig_type=std_logic lab=sw[3]}
C {sky130_fd_pr/cap_mim_m3_1.sym} 130 -600 3 0 {name=C9[15:0] model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {sky130_fd_pr/cap_mim_m3_1.sym} 260 -600 3 0 {name=C10[15:0] model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 190 -660 3 1 {name=M3
L=0.15
W=1
nf=11
mult=1
body=GND
ad="'int((nf+1)/2) * W/nf * 0.29'"
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'"
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/cap_mim_m3_1.sym} 130 -720 3 0 {name=C11[31:0] model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {sky130_fd_pr/cap_mim_m3_1.sym} 260 -720 3 0 {name=C12[31:0] model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 190 -780 3 1 {name=M4
L=0.15
W=1
nf=16
mult=1
body=GND
ad="'int((nf+1)/2) * W/nf * 0.29'"
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'"
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {devices/lab_wire.sym} 360 -820 0 0 {name=l3 sig_type=std_logic lab=sw[5]}
C {devices/lab_wire.sym} 350 -700 0 0 {name=l4 sig_type=std_logic lab=sw[4]}
C {sky130_fd_pr/cap_mim_m3_1.sym} 130 -870 3 0 {name=C13[63:0] model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {sky130_fd_pr/cap_mim_m3_1.sym} 260 -870 3 0 {name=C14[63:0] model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 190 -930 3 1 {name=M5
L=0.15
W=1
nf=11
mult=1
body=GND
ad="'int((nf+1)/2) * W/nf * 0.29'"
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'"
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {devices/lab_wire.sym} 360 -970 0 0 {name=l5 sig_type=std_logic lab=sw[6]}
C {sky130_fd_pr/cap_mim_m3_1.sym} 130 -1000 3 0 {name=C15[127:0] model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {sky130_fd_pr/cap_mim_m3_1.sym} 260 -1000 3 0 {name=C16[127:0] model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 190 -1060 3 1 {name=M8
L=0.15
W=1
nf=15
mult=1
body=GND
ad="'int((nf+1)/2) * W/nf * 0.29'"
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'"
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {devices/lab_wire.sym} 360 -1100 0 0 {name=l8 sig_type=std_logic lab=sw[7]}
C {devices/ipin.sym} 487.5 -540 0 1 {name=p4 lab=sw[7:0]}
