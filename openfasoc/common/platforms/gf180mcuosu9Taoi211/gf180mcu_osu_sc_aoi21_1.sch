v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 120 -480 120 -450 { lab=VDD}
N 260 -480 260 -450 { lab=VDD}
N 120 -390 120 -360 { lab=#net1}
N 120 -360 260 -360 { lab=#net1}
N 260 -390 260 -360 { lab=#net1}
N 190 -190 190 -150 { lab=#net2}
N 190 -90 190 -60 { lab=GND}
N 60 -420 80 -420 { lab=A0}
N 210 -420 220 -420 { lab=A1}
N 190 -270 250 -270 { lab=Y}
N 120 -420 140 -420 { lab=VDD}
N 260 -420 280 -420 { lab=VDD}
N 190 -220 200 -220 { lab=GND}
N 190 -120 210 -120 { lab=GND}
N 130 -220 150 -220 { lab=A0}
N 130 -120 150 -120 { lab=A1}
N 300 -130 300 -70 { lab=GND}
N 190 -70 300 -70 { lab=GND}
N 140 -320 150 -320 { lab=B}
N 190 -320 210 -320 { lab=VDD}
N 190 -360 190 -350 { lab=#net1}
N 190 -290 190 -250 { lab=Y}
N 240 -160 260 -160 { lab=B}
N 300 -160 320 -160 { lab=GND}
N 300 -250 300 -190 { lab=Y}
N 190 -250 300 -250 { lab=Y}
C {vdd.sym} 120 -480 0 0 {name=l1 lab=VDD}
C {vdd.sym} 260 -480 0 0 {name=l2 lab=VDD}
C {gnd.sym} 190 -60 0 0 {name=l3 lab=GND}
C {ipin.sym} 60 -420 0 0 {name=p3 lab=A0
}
C {ipin.sym} 210 -420 0 0 {name=p4 lab=A1
}
C {opin.sym} 250 -270 0 0 {name=p5 lab=Y}
C {pmos4.sym} 100 -420 0 0 {name=X1 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {pmos4.sym} 240 -420 0 0 {name=X0 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {nmos4.sym} 170 -220 0 0 {name=X2 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {nmos4.sym} 170 -120 0 0 {name=X3 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {lab_wire.sym} 140 -420 2 0 {name=l4 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 280 -420 2 0 {name=l5 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 200 -220 2 0 {name=l6 sig_type=std_logic lab=GND}
C {lab_wire.sym} 210 -120 2 0 {name=l7 sig_type=std_logic lab=GND}
C {lab_wire.sym} 130 -220 0 0 {name=l8 sig_type=std_logic lab=A0}
C {lab_wire.sym} 130 -120 0 0 {name=l9 sig_type=std_logic lab=A1}
C {nmos4.sym} 280 -160 0 0 {name=X4 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {ipin.sym} 140 -320 0 0 {name=p1 lab=B
}
C {pmos4.sym} 170 -320 0 0 {name=X5 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {lab_wire.sym} 210 -320 2 0 {name=l10 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 240 -160 0 0 {name=l11 sig_type=std_logic lab=B
}
C {lab_wire.sym} 320 -160 2 0 {name=l12 sig_type=std_logic lab=GND}
