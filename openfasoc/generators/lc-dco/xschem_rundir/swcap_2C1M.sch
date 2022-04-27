v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 60 -20 90 -20 { lab=outp}
N 90 -20 100 -20 { lab=outp}
N 160 -60 160 -20 { lab=#net1}
N 220 -60 220 -20 { lab=#net2}
N 220 -20 230 -20 { lab=#net2}
N 190 -120 190 -100 { lab=sw_on}
N 190 -120 380 -120 { lab=sw_on}
N 290 -20 300 -20 { lab=outn}
C {sky130_fd_pr/cap_mim_m3_1.sym} 130 -20 3 0 {name=C1 model=cap_mim_m3_1 W=Wc L=Lc MF=1 spiceprefix=X}
C {devices/opin.sym} 300 -20 0 0 {name=p2 lab=outn
}
C {devices/opin.sym} 60 -20 0 1 {name=p3 lab=outp}
C {sky130_fd_pr/cap_mim_m3_1.sym} 260 -20 3 0 {name=C2 model=cap_mim_m3_1 W=Wc L=Lc MF=1 spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 190 -80 3 1 {name=M6
L=0.15
W=Wsw
nf=1
mult=Lsw
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
C {devices/ipin.sym} 377.5 -120 0 1 {name=p4 lab=sw_on}
