v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N -100 -0 -30 -0 { lab=#net1}
N 30 0 120 0 { lab=#net2}
N -60 30 -60 40 { lab=sw}
N -60 40 -0 40 { lab=sw}
N 0 40 80 40 { lab=sw}
N 80 30 80 40 { lab=sw}
N -100 60 -100 100 { lab=GND}
N -100 100 120 100 { lab=GND}
N 120 60 120 100 { lab=GND}
N -0 40 0 70 { lab=sw}
N 0 70 50 70 { lab=sw}
N -140 -0 -100 -0 { lab=#net1}
N 120 0 150 0 { lab=#net2}
N -260 0 -210 -0 { lab=outp}
N -150 0 -140 0 { lab=#net1}
N -0 100 -0 130 { lab=GND}
N 150 0 210 -0 { lab=#net2}
N -130 30 -100 30 { lab=GND}
N -130 30 -130 60 { lab=GND}
N -130 60 -100 60 { lab=GND}
N 120 30 140 30 { lab=GND}
N 140 30 140 60 { lab=GND}
N 120 60 140 60 { lab=GND}
N -0 -90 0 -0 { lab=GND}
N 270 0 300 0 { lab=outn}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 0 20 3 0 {name=M1
L=Lsw
W=Wsw
nf=nsw
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'"
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'"
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X}
C {sky130_fd_pr/nfet_01v8_lvt.sym} -80 30 2 0 {name="M2"
L=Wpd
W=Wpd
nf=npd
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'"
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'"
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 100 30 0 0 {name=M3
L=Lpd
W=Wpd
nf=npd
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'"
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'"
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {devices/opin.sym} 300 0 0 0 {name=p2 lab=outn
}
C {devices/opin.sym} -255 0 0 1 {name=p3 lab=outp}
C {devices/ipin.sym} 50 70 2 0 {name=p1 lab=sw}
C {sky130_fd_pr/cap_mim_m3_1.sym} 240 0 1 0 {name=C1 model=cap_mim_m3_1 W=1 L=1 MF=Mc spiceprefix=X}
C {sky130_fd_pr/cap_mim_m3_1.sym} -180 0 1 0 {name=C2 model=cap_mim_m3_1 W=1 L=1 MF=Mc spiceprefix=X}
C {devices/iopin.sym} 0 130 2 0 {name=p4 lab=GND}
C {devices/lab_wire.sym} 0 -90 0 0 {name=l1 sig_type=std_logic lab=GND}
