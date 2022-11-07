v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 180 -740 180 -710 { lab=VDD}
N 180 -650 180 -620 { lab=SelN}
N 180 -620 180 -580 { lab=SelN}
N 180 -520 180 -490 { lab=GND}
N 120 -680 140 -680 { lab=Sel}
N 100 -680 100 -550 { lab=Sel}
N 80 -620 100 -620 { lab=Sel}
N 100 -680 120 -680 { lab=Sel}
N 100 -550 140 -550 { lab=Sel}
N 180 -680 210 -680 { lab=VDD}
N 180 -550 210 -550 { lab=GND}
N 210 -140 210 -60 { lab=Y}
N 150 -140 150 -60 { lab=B}
N 110 -330 150 -330 { lab=A}
N 210 -370 210 -290 { lab=Y}
N 150 -370 150 -290 { lab=A}
N 180 -250 180 -180 { lab=SelN}
N 110 -100 150 -100 { lab=B}
N 210 -330 290 -330 { lab=Y}
N 210 -100 290 -100 { lab=Y}
N 290 -330 290 -100 { lab=Y}
N 290 -220 320 -220 { lab=Y}
C {vdd.sym} 180 -740 0 0 {name=l1 lab=VDD}
C {gnd.sym} 180 -490 0 0 {name=l3 lab=GND}
C {ipin.sym} 80 -620 0 0 {name=p3 lab=Sel
}
C {pmos4.sym} 160 -680 0 0 {name=X0 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {nmos4.sym} 160 -550 0 0 {name=X1 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {lab_wire.sym} 210 -680 2 0 {name=l2 sig_type=std_logic lab=VDD
}
C {lab_wire.sym} 210 -550 2 0 {name=l4 sig_type=std_logic lab=GND
}
C {pmos4.sym} 180 -160 1 0 {name=X2 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {lab_wire.sym} 180 -140 3 0 {name=l5 sig_type=std_logic lab=VDD
}
C {nmos4.sym} 180 -40 3 0 {name=X3 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {pmos4.sym} 180 -390 1 0 {name=X4 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {lab_wire.sym} 180 -370 3 0 {name=l6 sig_type=std_logic lab=VDD
}
C {nmos4.sym} 180 -270 3 0 {name=X5 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {lab_wire.sym} 180 -290 1 0 {name=l7 sig_type=std_logic lab=GND
}
C {lab_wire.sym} 180 -60 1 0 {name=l8 sig_type=std_logic lab=GND
}
C {lab_wire.sym} 180 -620 2 0 {name=l9 sig_type=std_logic lab=SelN
}
C {lab_wire.sym} 180 -220 2 0 {name=l10 sig_type=std_logic lab=SelN
}
C {lab_wire.sym} 180 -20 2 0 {name=l11 sig_type=std_logic lab=Sel
}
C {lab_wire.sym} 180 -410 0 0 {name=l12 sig_type=std_logic lab=Sel
}
C {ipin.sym} 110 -330 0 0 {name=p1 lab=A
}
C {ipin.sym} 110 -100 0 0 {name=p2 lab=B

}
C {opin.sym} 320 -220 0 0 {name=p4 lab=Y
}
