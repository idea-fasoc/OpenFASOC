v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 120 -390 120 -360 { lab=VDD}
N 260 -390 260 -360 { lab=VDD}
N 120 -300 120 -270 { lab=Y}
N 120 -270 260 -270 { lab=Y}
N 260 -300 260 -270 { lab=Y}
N 190 -270 190 -250 { lab=Y}
N 190 -190 190 -150 { lab=#net1}
N 190 -90 190 -60 { lab=GND}
N 60 -330 80 -330 { lab=A}
N 210 -330 220 -330 { lab=B}
N 260 -270 320 -270 { lab=Y}
N 120 -330 140 -330 { lab=VDD}
N 260 -330 280 -330 { lab=VDD}
N 190 -220 200 -220 { lab=GND}
N 190 -120 210 -120 { lab=GND}
N 130 -220 150 -220 { lab=A}
N 130 -120 150 -120 { lab=GND}
C {vdd.sym} 120 -390 0 0 {name=l1 lab=VDD}
C {vdd.sym} 260 -390 0 0 {name=l2 lab=VDD}
C {gnd.sym} 190 -60 0 0 {name=l3 lab=GND}
C {ipin.sym} 60 -330 0 0 {name=p3 lab=A
}
C {ipin.sym} 210 -330 0 0 {name=p4 lab=B
}
C {opin.sym} 320 -270 0 0 {name=p5 lab=Y}
C {pmos4.sym} 100 -330 0 0 {name=X1 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {pmos4.sym} 240 -330 0 0 {name=X0 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {nmos4.sym} 170 -220 0 0 {name=X2 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {nmos4.sym} 170 -120 0 0 {name=X3 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {lab_wire.sym} 140 -330 2 0 {name=l4 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 280 -330 2 0 {name=l5 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 200 -220 2 0 {name=l6 sig_type=std_logic lab=GND}
C {lab_wire.sym} 210 -120 2 0 {name=l7 sig_type=std_logic lab=GND}
C {lab_wire.sym} 130 -220 0 0 {name=l8 sig_type=std_logic lab=A}
C {lab_wire.sym} 130 -120 0 0 {name=l9 sig_type=std_logic lab=B}
