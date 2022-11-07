v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 190 -310 190 -280 { lab=VDD}
N 190 -220 190 -190 { lab=#net1}
N 190 -190 190 -150 { lab=#net1}
N 190 -90 190 -60 { lab=GND}
N 130 -250 150 -250 { lab=A}
N 110 -250 110 -120 { lab=A}
N 90 -190 110 -190 { lab=A}
N 110 -250 130 -250 { lab=A}
N 110 -120 150 -120 { lab=A}
N 190 -250 220 -250 { lab=VDD}
N 190 -120 220 -120 { lab=GND}
N 370 -220 370 -190 { lab=Y}
N 370 -190 370 -150 { lab=Y}
N 370 -90 370 -60 { lab=GND}
N 310 -250 330 -250 { lab=#net1}
N 370 -180 440 -180 { lab=Y}
N 290 -250 290 -120 { lab=#net1}
N 270 -190 290 -190 { lab=#net1}
N 290 -250 310 -250 { lab=#net1}
N 290 -120 330 -120 { lab=#net1}
N 370 -250 400 -250 { lab=VDD}
N 370 -120 400 -120 { lab=GND}
N 190 -190 270 -190 { lab=#net1}
N 370 -310 370 -280 { lab=VDD}
C {vdd.sym} 190 -310 0 0 {name=l1 lab=VDD}
C {gnd.sym} 190 -60 0 0 {name=l3 lab=GND}
C {ipin.sym} 90 -190 0 0 {name=p3 lab=A
}
C {opin.sym} 440 -180 0 0 {name=p5 lab=Y}
C {pmos4.sym} 170 -250 0 0 {name=X0 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {nmos4.sym} 170 -120 0 0 {name=X1 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {lab_wire.sym} 220 -250 2 0 {name=l2 sig_type=std_logic lab=VDD
}
C {lab_wire.sym} 220 -120 2 0 {name=l4 sig_type=std_logic lab=GND
}
C {pmos4.sym} 350 -250 0 0 {name=X2 model=pmos_3p3 w=1.7u l=0.3u m=2}
C {nmos4.sym} 350 -120 0 0 {name=X3 model=nmos_3p3 w=0.85u l=0.3u m=2}
C {lab_wire.sym} 400 -250 2 0 {name=l5 sig_type=std_logic lab=VDD
}
C {lab_wire.sym} 400 -120 2 0 {name=l6 sig_type=std_logic lab=GND
}
C {vdd.sym} 370 -310 0 0 {name=l7 lab=VDD}
C {gnd.sym} 370 -60 0 0 {name=l8 lab=GND}
