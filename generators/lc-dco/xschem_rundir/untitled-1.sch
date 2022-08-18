v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 55 -270 95 -270 { lab=outp}
N 235 -310 235 -270 { lab=#net1}
N 295 -310 295 -270 { lab=#net2}
N 295 -270 305 -270 { lab=#net2}
N 246 -330 246 -310 { lab=#net3}
N 285 -180 475 -180 { lab=sw}
N 490 -270 500 -270 { lab=outn}
N 305 -270 350 -270 { lab=#net2}
N 235 -180 285 -180 { lab=sw}
N 350 -270 385 -270 { lab=#net2}
N 445 -270 490 -270 { lab=outn}
N 175 -270 235 -270 { lab=#net1}
N 155 -270 175 -270 { lab=#net1}
N 195 -270 195 -209 { lab=#net1}
N 365 -270 365 -210 { lab=#net2}
N 195 -149 366 -149 { lab=#net4}
N 279 -149 279 -105 { lab=#net4}
N 266 -270 266 -181 { lab=sw}
N 266 -181 266 -180 { lab=sw}
C {devices/opin.sym} 500 -270 0 0 {name=p2 lab=outn
}
C {devices/opin.sym} 55 -270 0 1 {name=p3 lab=outp}
C {sky130_fd_pr/cap_mim_m3_1.sym} 415 -270 3 0 {name=C2[7:0] model=cap_mim_m3_1 W=1 L=1 MF=Mc spiceprefix=X}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 266 -290 1 1 {name=M6
L=Lsw
W=Wsw
nf=nsw
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
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 215 -180 0 1 {name=M1
L=Lpd
W=Wpd
nf=npd
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
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 345 -180 0 0 {name=M2
L=Lpd
W=Wpd
nf=npd
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
C {sky130_fd_pr/cap_mim_m3_1.sym} 125 -270 3 0 {name=C1[7:0] model=cap_mim_m3_1 W=1 L=1 MF=MC spiceprefix=X}
C {devices/iopin.sym} 270 -104 0 0 {name=p1 lab=GND
}
C {devices/ipin.sym} 475 -180 2 0 {name=p4 lab=sw}
