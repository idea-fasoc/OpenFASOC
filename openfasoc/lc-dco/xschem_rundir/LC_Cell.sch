v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 240 -90 240 -80 { lab=#net1}
N 80 -150 140 -150 { lab=outp}
N 140 -150 175 -120 { lab=outp}
N 175 -120 200 -120 { lab=outp}
N 120 -120 160 -150 { lab=outn}
N 160 -150 240 -150 { lab=outn}
N 90 -415 130 -415 { lab=outp}
N 50 -190 80 -190 { lab=outp}
N 240 -190 290 -190 { lab=outn}
N 160 -455 160 -425 { lab=VDD}
N 445 -90 445 -80 { lab=Ibias}
N 395 -82.5 395 -50 { lab=Ibias}
N 395 -90 395 -82.5 { lab=Ibias}
N 395 -90 445 -90 { lab=Ibias}
N 445 -120 445 -90 { lab=Ibias}
N 445 -120 477.5 -120 { lab=Ibias}
N 20 -415 20 -265 { lab=outp}
N 20 -415 90 -415 { lab=outp}
N 80 -190 80 -150 { lab=outp}
N 240 -190 240 -150 { lab=outn}
N 20 -265 20 -260 { lab=outp}
N 320 -415 320 -255 { lab=outn}
N 190 -415 320 -415 { lab=outn}
N 383 -50 395 -50 { lab=Ibias}
N 383 -50 383 -47 { lab=Ibias}
N 280 -50 280 -47 { lab=Ibias}
N 475 -240 486 -240 { lab=swcap[7:0]}
N 395 -50 405 -50 { lab=Ibias}
N 20 -260 20 -255 { lab=outp}
N 80 -90 80 -80 { lab=#net2}
N 280 -47 383 -47 { lab=Ibias}
N 120 -47 280 -47 { lab=Ibias}
N 120 -50 120 -47 { lab=Ibias}
N 80 -20 95 -20 { lab=#net3}
N 320 -235 475 -240 {}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 100 -120 0 1 {name=M1
L=0.15
W=4.8
nf=20
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
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 220 -120 0 0 {name=M2
L=0.15
W=4.8
nf=20
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
C {devices/ipin.sym} 477.5 -120 0 1 {name=p1 lab=Ibias
}
C {devices/gnd.sym} 95 -19.5 0 0 {name=l1 lab=GND}
C {sky130_fd_pr/ind_generic.sym} 160 -415 1 0 {name=L1
**N=1
**L=1
** Other Params
spiceprefix=X
model=ind_05_220
}
C {devices/opin.sym} 290 -190 0 0 {name=p2 lab=outn
}
C {devices/opin.sym} 50 -190 0 1 {name=p3 lab=outp}
C {devices/vdd.sym} 160 -455 0 0 {name=l2 lab=VDD}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 260 -50 0 1 {name=M4
L=0.15
W=2.4
nf=10
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
C {devices/gnd.sym} 240 -20 0 0 {name=l3 lab=GND}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 425 -50 0 0 {name=M5
L=0.15
W=1.2
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
C {devices/gnd.sym} 445 -20 0 1 {name=l4 lab=GND}
C {mimcap_sw_2C1M.sym} 170 -255 0 0 {name=x1}
C {devices/lab_pin.sym} 320 -326 0 1 {name=l6 sig_type=std_logic lab=outn
}
C {devices/lab_pin.sym} 20 -320 0 0 {name=l7 sig_type=std_logic lab=outp}
C {devices/ipin.sym} 483 -240 0 1 {name=p4 lab=swcap[7:0]
}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 100 -50 0 1 {name=M3
L=0.15
W=2.4
nf=10
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
