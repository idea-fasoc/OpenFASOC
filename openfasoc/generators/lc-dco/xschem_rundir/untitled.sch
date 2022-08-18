v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 55 -40 95 -40 { lab=outp}
N 155 -80 155 -40 { lab=#net1}
N 215 -80 215 -40 { lab=#net2}
N 215 -40 225 -40 { lab=#net2}
N 185 -140 185 -120 { lab=sw[0]}
N 185 -140 375 -140 { lab=sw[0]}
N 330 -40 340 -40 { lab=outn}
N 225 -40 270 -40 { lab=#net2}
N 265 -110 265 -40 { lab=#net2}
N 95 -110 95 -45 { lab=outp}
N 95 -45 95 -40 { lab=outp}
N 135 -140 185 -140 { lab=sw[0]}
N 95 -170 185 -170 { lab=GND}
N 185 -170 265 -170 { lab=GND}
C {sky130_fd_pr/cap_mim_m3_1.sym} 125 -40 3 0 {name=C1 model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {devices/opin.sym} 340 -40 0 0 {name=p2 lab=outn
}
C {devices/opin.sym} 55 -40 0 1 {name=p3 lab=outp}
C {sky130_fd_pr/cap_mim_m3_1.sym} 300 -40 3 0 {name=C2 model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 185 -100 3 1 {name=M6
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
C {devices/lab_wire.sym} 365 -140 0 1 {name=l7 sig_type=std_logic lab=sw[0]}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 115 -140 0 1 {name=M1
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
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 245 -140 0 0 {name=M2
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
C {devices/gnd.sym} 185 -170 0 0 {name=l1 lab=GND}
