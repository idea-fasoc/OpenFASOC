v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 210 -380 210 -350 { lab=VDD}
N 210 -290 210 -260 { lab=#net1}
N 120 -70 120 -30 { lab=GND}
N 290 -60 290 -30 { lab=GND}
N 160 -230 170 -230 { lab=B}
N 210 -320 230 -320 { lab=VDD}
N 210 -230 230 -230 { lab=VDD}
N 120 -100 130 -100 { lab=GND}
N 290 -90 310 -90 { lab=GND}
N 60 -100 80 -100 { lab=A}
N 230 -90 250 -90 { lab=B}
N 120 -160 120 -130 { lab=Y}
N 210 -200 210 -160 { lab=Y}
N 120 -160 210 -160 { lab=Y}
N 290 -160 290 -120 { lab=Y}
N 210 -160 290 -160 { lab=Y}
N 290 -160 320 -160 { lab=Y}
N 160 -320 170 -320 { lab=A}
C {vdd.sym} 210 -380 0 0 {name=l1 lab=VDD}
C {gnd.sym} 120 -30 0 0 {name=l3 lab=GND}
C {ipin.sym} 160 -320 0 0 {name=p3 lab=A
}
C {ipin.sym} 160 -230 0 0 {name=p4 lab=B
}
C {opin.sym} 320 -160 0 0 {name=p5 lab=Y}
C {pmos4.sym} 190 -320 0 0 {name=X1 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {pmos4.sym} 190 -230 0 0 {name=X0 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {nmos4.sym} 100 -100 0 0 {name=X2 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {nmos4.sym} 270 -90 0 0 {name=X3 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {lab_wire.sym} 230 -320 2 0 {name=l4 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 230 -230 2 0 {name=l5 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 130 -100 2 0 {name=l6 sig_type=std_logic lab=GND}
C {lab_wire.sym} 310 -90 2 0 {name=l7 sig_type=std_logic lab=GND}
C {lab_wire.sym} 60 -100 0 0 {name=l8 sig_type=std_logic lab=A}
C {lab_wire.sym} 230 -90 0 0 {name=l9 sig_type=std_logic lab=B}
C {gnd.sym} 290 -30 0 0 {name=l10 lab=GND}
