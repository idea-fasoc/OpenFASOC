v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 190 -310 190 -280 { lab=VDD}
N 190 -220 190 -190 { lab=Y}
N 190 -90 190 -60 { lab=GND}
N 130 -250 150 -250 { lab=A}
N 260 -190 320 -190 { lab=Y}
N 190 -190 260 -190 { lab=Y}
N 110 -250 110 -120 { lab=A}
N 110 -250 130 -250 { lab=A}
N 110 -120 150 -120 { lab=A}
N 190 -250 220 -250 { lab=VDD}
N 190 -120 220 -120 { lab=GND}
N 190 -170 190 -150 {}
N 110 -170 190 -170 {}
C {vdd.sym} 190 -310 0 0 {name=l1 lab=VDD}
C {gnd.sym} 190 -60 0 0 {name=l3 lab=GND}
C {opin.sym} 320 -190 0 0 {name=p5 lab=Y}
C {pmos4.sym} 170 -250 0 0 {name=X0 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {nmos4.sym} 170 -120 0 0 {name=X1 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {lab_wire.sym} 220 -250 2 0 {name=l2 sig_type=std_logic lab=VDD
}
C {lab_wire.sym} 220 -120 2 0 {name=l4 sig_type=std_logic lab=GND
}
