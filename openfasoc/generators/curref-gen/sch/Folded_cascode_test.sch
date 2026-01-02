v {xschem version=3.4.6RC file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {FOLDED CASCODE OTA} 1020 -60 0 0 0.4 0.4 {}
T {BIAS CIRCUIT} 300 -60 0 0 0.4 0.4 {}
N 1210 -620 1210 -510 {
lab=#net1}
N 1390 -620 1390 -510 {
lab=#net2}
N 1210 -340 1210 -300 {
lab=#net3}
N 1390 -340 1390 -300 {
lab=#net4}
N 1390 -450 1390 -400 {
lab=Vout}
N 1210 -450 1210 -400 {
lab=#net5}
N 1250 -480 1350 -480 {
lab=VB1}
N 1250 -650 1350 -650 {
lab=#net5}
N 1210 -430 1280 -430 {
lab=#net5}
N 1280 -650 1280 -430 {
lab=#net5}
N 1250 -370 1350 -370 {
lab=VB2}
N 1250 -220 1350 -220 {
lab=VP}
N 1210 -730 1210 -680 {
lab=VDD}
N 1210 -730 1390 -730 {
lab=VDD}
N 1390 -730 1390 -680 {
lab=VDD}
N 830 -600 830 -380 {
lab=#net1}
N 830 -600 1210 -600 {
lab=#net1}
N 980 -570 980 -380 {
lab=#net2}
N 980 -570 1390 -570 {
lab=#net2}
N 760 -350 790 -350 {
lab=V+}
N 1020 -350 1050 -350 {
lab=V-}
N 1210 -170 1390 -170 {
lab=VSS}
N 830 -320 830 -270 {
lab=#net6}
N 830 -270 980 -270 {
lab=#net6}
N 980 -320 980 -270 {
lab=#net6}
N 910 -270 910 -250 {
lab=#net6}
N 840 -220 870 -220 {
lab=VP}
N 1390 -430 1480 -430 {
lab=Vout}
N 1300 -520 1300 -480 {
lab=VB1}
N 1210 -300 1210 -250 {
lab=#net3}
N 1390 -300 1390 -250 {
lab=#net4}
N 1210 -190 1210 -170 {
lab=VSS}
N 1390 -190 1390 -170 {
lab=VSS}
N 1210 -680 1210 -650 {
lab=VDD}
N 1390 -680 1390 -650 {
lab=VDD}
N 1390 -220 1390 -190 {
lab=VSS}
N 1210 -220 1210 -190 {
lab=VSS}
N 910 -220 910 -190 {
lab=VSS}
N 980 -350 980 -320 {
lab=#net6}
N 830 -350 830 -320 {
lab=#net6}
N 570 -520 570 -300 {
lab=VB2}
N 410 -550 530 -550 {
lab=VB1}
N 370 -520 370 -250 {
lab=VB1}
N 570 -730 570 -580 {
lab=VDD}
N 170 -730 570 -730 {
lab=VDD}
N 170 -730 170 -510 {
lab=VDD}
N 370 -730 370 -550 {
lab=VDD}
N 570 -580 570 -550 {
lab=VDD}
N 170 -510 170 -480 {
lab=VDD}
N 170 -170 570 -170 {
lab=VSS}
N 170 -220 170 -190 {
lab=VSS}
N 170 -450 170 -250 {
lab=VP}
N 210 -220 330 -220 {
lab=VP}
N 270 -320 270 -220 {
lab=VP}
N 170 -320 270 -320 {
lab=VP}
N 470 -270 530 -270 {
lab=VB2}
N 470 -360 470 -270 {
lab=VB2}
N 470 -360 570 -360 {
lab=VB2}
N 370 -440 470 -440 {
lab=VB1}
N 470 -550 470 -440 {
lab=VB1}
N 1200 -370 1210 -370 {
lab=VSS}
N 1200 -370 1200 -170 {
lab=VSS}
N 1390 -370 1400 -370 {
lab=VSS}
N 1400 -370 1400 -170 {
lab=VSS}
N 1390 -170 1400 -170 {
lab=VSS}
N 1200 -480 1210 -480 {
lab=VDD}
N 1200 -730 1200 -480 {
lab=VDD}
N 1200 -730 1210 -730 {
lab=VDD}
N 1390 -730 1400 -730 {
lab=VDD}
N 1400 -730 1400 -480 {
lab=VDD}
N 1390 -480 1400 -480 {
lab=VDD}
N 1300 -790 1300 -730 {
lab=VDD}
N 370 -790 370 -730 {
lab=VDD}
N 210 -480 230 -480 {
lab=VrefBG}
N 1300 -410 1300 -370 {
lab=VB2}
N 1300 -260 1300 -220 {
lab=VP}
N 370 -170 370 -110 {
lab=VSS}
N 910 -170 1200 -170 {
lab=VSS}
N 910 -190 910 -170 {
lab=VSS}
N 570 -240 570 -170 {
lab=VSS}
N 370 -190 370 -170 {
lab=VSS}
N 170 -190 170 -170 {
lab=VSS}
N 570 -270 570 -240 {
lab=VSS}
N 370 -220 370 -190 {
lab=VSS}
N 1300 -170 1300 -110 {
lab=VSS}
N 1200 -170 1210 -170 {
lab=VSS}
C {sky130_fd_pr/pfet_01v8.sym} 1370 -650 0 0 {name=M2
W=5.5
L=0.15
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
q}
C {sky130_fd_pr/pfet_01v8.sym} 1230 -650 0 1 {name=M3
W=5.5
L=0.15
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 1370 -480 0 0 {name=M4
W=14.5
L=0.15
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 1230 -480 0 1 {name=M5
W=14.5
L=0.15
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 1000 -350 0 1 {name=M6
W=15
L=1
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 1370 -370 0 0 {name=M7
W=2
L=3
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
q}
C {sky130_fd_pr/nfet_01v8.sym} 1230 -370 0 1 {name=M8
W=2
L=3
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 1370 -220 0 0 {name=M9
W=0.42
L=8
nf=1
mult=5
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 1230 -220 0 1 {name=M10
W=0.42
L=8
nf=1 
mult=5
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 890 -220 0 0 {name=M11
W=0.42
L=8.5
nf=1 
mult=10
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {lab_pin.sym} 1300 -410 0 1 {name=p8 sig_type=std_logic lab=VB2
}
C {lab_pin.sym} 1300 -520 2 0 {name=p4 sig_type=std_logic lab=VB1}
C {lab_pin.sym} 1300 -260 2 0 {name=p11 sig_type=std_logic lab=VP}
C {lab_pin.sym} 840 -220 0 0 {name=p12 sig_type=std_logic lab=VP}
C {sky130_fd_pr/corner.sym} 1590 -800 0 0 {name=CORNER only_toplevel=true corner=tt}
C {sky130_fd_pr/nfet_01v8.sym} 810 -350 0 0 {name=M1
W=15
L=1
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 190 -220 0 1 {name=M12
W=0.42
L=8.5
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 350 -220 0 0 {name=M13
W=0.42
L=8.5
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 190 -480 0 1 {name=M14
W=6.1
L=0.15
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 390 -550 0 1 {name=M15
W=1
L=1
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 550 -550 0 0 {name=M16
W=1
L=1
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
q}
C {sky130_fd_pr/nfet_01v8.sym} 550 -270 0 0 {name=M17
W=0.42
L=17
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {lab_pin.sym} 370 -790 2 0 {name=p16 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 570 -360 2 0 {name=p18 sig_type=std_logic lab=VB2}
C {lab_pin.sym} 270 -280 0 1 {name=p19 sig_type=std_logic lab=VP}
C {lab_pin.sym} 470 -520 2 0 {name=p3 sig_type=std_logic lab=VB1}
C {lab_pin.sym} 370 -110 2 0 {name=p20 sig_type=std_logic lab=VSS}
C {opin.sym} 1480 -430 0 0 {name=p21 lab=Vout}
C {iopin.sym} 1300 -110 0 0 {name=p2 lab=VSS}
C {ipin.sym} 760 -350 0 0 {name=p22 lab=V+}
C {iopin.sym} 1300 -790 0 0 {name=p24 lab=VDD}
C {ipin.sym} 1050 -350 0 1 {name=p25 lab=V-}
C {ipin.sym} 230 -480 0 1 {name=p26 lab=VrefBG}
