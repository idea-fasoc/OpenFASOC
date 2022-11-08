v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 130 -350 130 -320 { lab=VDD}
N 270 -350 270 -320 { lab=VDD}
N 130 -260 130 -230 { lab=#net1}
N 130 -230 270 -230 { lab=#net1}
N 270 -260 270 -230 { lab=#net1}
N 200 -230 200 -210 { lab=#net1}
N 200 -150 200 -110 { lab=#net2}
N 200 -50 200 -20 { lab=GND}
N 70 -290 90 -290 { lab=A}
N 220 -290 230 -290 { lab=B}
N 450 -230 510 -230 { lab=Y}
N 130 -290 150 -290 { lab=VDD}
N 270 -290 290 -290 { lab=VDD}
N 200 -180 210 -180 { lab=GND}
N 200 -80 220 -80 { lab=GND}
N 140 -180 160 -180 { lab=A}
N 140 -80 160 -80 { lab=B}
N 450 -240 450 -210 { lab=Y}
N 370 -180 410 -180 { lab=#net1}
N 370 -260 370 -180 { lab=#net1}
N 370 -270 370 -260 { lab=#net1}
N 370 -270 410 -270 { lab=#net1}
N 270 -230 370 -230 { lab=#net1}
N 450 -350 450 -300 { lab=VDD}
N 450 -150 450 -130 { lab=GND}
N 450 -270 470 -270 { lab=VDD}
N 450 -180 470 -180 {}
C {vdd.sym} 130 -350 0 0 {name=l1 lab=VDD}
C {vdd.sym} 270 -350 0 0 {name=l2 lab=VDD}
C {gnd.sym} 200 -20 0 0 {name=l3 lab=GND}
C {ipin.sym} 70 -290 0 0 {name=p3 lab=A
}
C {ipin.sym} 220 -290 0 0 {name=p4 lab=B
}
C {opin.sym} 510 -230 0 0 {name=p5 lab=Y}
C {pmos4.sym} 110 -290 0 0 {name=X1 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {pmos4.sym} 250 -290 0 0 {name=X0 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {nmos4.sym} 180 -180 0 0 {name=X2 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {nmos4.sym} 180 -80 0 0 {name=X3 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {lab_wire.sym} 150 -290 2 0 {name=l4 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 290 -290 2 0 {name=l5 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 210 -180 2 0 {name=l6 sig_type=std_logic lab=GND}
C {lab_wire.sym} 220 -80 2 0 {name=l7 sig_type=std_logic lab=GND}
C {lab_wire.sym} 140 -180 0 0 {name=l8 sig_type=std_logic lab=A}
C {lab_wire.sym} 140 -80 0 0 {name=l9 sig_type=std_logic lab=B}
C {pmos4.sym} 430 -270 0 0 {name=X4 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {nmos4.sym} 430 -180 0 0 {name=X5 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {vdd.sym} 270 -350 0 0 {name=l10 lab=VDD}
C {vdd.sym} 450 -350 0 0 {name=l11 lab=VDD}
C {gnd.sym} 450 -130 0 0 {name=l12 lab=GND}
C {lab_wire.sym} 470 -270 2 0 {name=l13 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 470 -180 2 0 {name=l14 sig_type=std_logic lab=GND}
