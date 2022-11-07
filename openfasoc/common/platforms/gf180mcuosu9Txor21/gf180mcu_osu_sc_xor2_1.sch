v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 200 -230 200 -210 { lab=Y}
N 200 -150 200 -110 { lab=#net1}
N 200 -50 200 -20 { lab=GND}
N 200 -180 210 -180 { lab=GND}
N 200 -80 220 -80 { lab=GND}
N 140 -180 160 -180 { lab=A}
N 140 -80 160 -80 { lab=B}
N 400 -150 400 -110 { lab=#net2}
N 400 -50 400 -20 { lab=GND}
N 400 -180 410 -180 { lab=GND}
N 400 -80 420 -80 { lab=GND}
N 340 -180 360 -180 { lab=AN}
N 340 -80 360 -80 { lab=BN}
N 200 -340 200 -320 { lab=#net3}
N 400 -340 400 -320 { lab=#net4}
N 200 -260 200 -230 { lab=Y}
N 400 -260 400 -230 { lab=Y}
N 200 -420 200 -400 { lab=VDD}
N 400 -420 400 -400 { lab=VDD}
N 200 -370 220 -370 { lab=VDD}
N 200 -290 220 -290 { lab=VDD}
N 400 -290 420 -290 { lab=VDD}
N 400 -370 420 -370 { lab=VDD}
N 140 -290 160 -290 { lab=BN}
N 140 -370 160 -370 { lab=A}
N 600 -360 600 -320 { lab=AN}
N 520 -390 560 -390 { lab=A}
N 520 -390 520 -290 { lab=A}
N 520 -290 560 -290 { lab=A}
N 600 -390 620 -390 { lab=VDD}
N 600 -290 620 -290 { lab=GND}
N 600 -260 600 -240 { lab=GND}
N 600 -440 600 -420 { lab=VDD}
N 510 -340 520 -340 { lab=A}
N 600 -340 640 -340 { lab=AN}
N 820 -360 820 -320 { lab=BN}
N 740 -390 780 -390 { lab=B}
N 740 -390 740 -290 { lab=B}
N 740 -290 780 -290 { lab=B}
N 820 -390 840 -390 { lab=VDD}
N 820 -290 840 -290 { lab=GND}
N 820 -260 820 -240 { lab=GND}
N 820 -440 820 -420 { lab=VDD}
N 730 -340 740 -340 { lab=B}
N 820 -340 860 -340 { lab=BN}
N 330 -370 360 -370 { lab=AN}
N 330 -290 360 -290 { lab=B}
N 400 -260 400 -210 { lab=Y}
N 200 -230 400 -230 { lab=Y}
N 400 -230 440 -230 { lab=Y}
C {gnd.sym} 200 -20 0 0 {name=l3 lab=GND}
C {nmos4.sym} 180 -180 0 0 {name=X2 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {nmos4.sym} 180 -80 0 0 {name=X3 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {lab_wire.sym} 210 -180 2 0 {name=l6 sig_type=std_logic lab=GND}
C {lab_wire.sym} 220 -80 2 0 {name=l7 sig_type=std_logic lab=GND}
C {lab_wire.sym} 140 -180 0 0 {name=l8 sig_type=std_logic lab=A}
C {lab_wire.sym} 340 -80 0 0 {name=l9 sig_type=std_logic lab=BN}
C {gnd.sym} 400 -20 0 0 {name=l1 lab=GND}
C {nmos4.sym} 380 -180 0 0 {name=X1 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {nmos4.sym} 380 -80 0 0 {name=X4 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {lab_wire.sym} 410 -180 2 0 {name=l2 sig_type=std_logic lab=GND}
C {lab_wire.sym} 420 -80 2 0 {name=l4 sig_type=std_logic lab=GND}
C {lab_wire.sym} 340 -180 0 0 {name=l5 sig_type=std_logic lab=AN}
C {lab_wire.sym} 140 -80 0 0 {name=l10 sig_type=std_logic lab=B}
C {pmos4.sym} 180 -370 0 0 {name=M1 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {pmos4.sym} 180 -290 0 0 {name=M2 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {pmos4.sym} 380 -370 0 0 {name=M3 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {pmos4.sym} 380 -290 0 0 {name=M4 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {vdd.sym} 200 -420 0 0 {name=l11 lab=VDD}
C {vdd.sym} 400 -420 0 0 {name=l12 lab=VDD}
C {lab_wire.sym} 220 -370 2 0 {name=l13 sig_type=std_logic lab=VDD
}
C {lab_wire.sym} 220 -290 2 0 {name=l14 sig_type=std_logic lab=VDD
}
C {lab_wire.sym} 420 -290 2 0 {name=l15 sig_type=std_logic lab=VDD
}
C {lab_wire.sym} 420 -370 2 0 {name=l16 sig_type=std_logic lab=VDD
}
C {ipin.sym} 330 -290 0 0 {name=p1 lab=B
}
C {ipin.sym} 140 -370 0 0 {name=p2 lab=A
}
C {nmos4.sym} 580 -290 0 0 {name=X5 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {pmos4.sym} 580 -390 0 0 {name=M5 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {lab_wire.sym} 620 -390 2 0 {name=l17 sig_type=std_logic lab=VDD
}
C {lab_wire.sym} 620 -290 2 0 {name=l18 sig_type=std_logic lab=GND}
C {gnd.sym} 600 -240 0 0 {name=l19 lab=GND}
C {vdd.sym} 600 -440 0 0 {name=l20 lab=VDD}
C {lab_wire.sym} 510 -340 0 0 {name=l21 sig_type=std_logic lab=A
}
C {lab_wire.sym} 640 -340 2 0 {name=l22 sig_type=std_logic lab=AN
}
C {nmos4.sym} 800 -290 0 0 {name=X6 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {pmos4.sym} 800 -390 0 0 {name=M6 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {lab_wire.sym} 840 -390 2 0 {name=l23 sig_type=std_logic lab=VDD
}
C {lab_wire.sym} 840 -290 2 0 {name=l24 sig_type=std_logic lab=GND}
C {gnd.sym} 820 -240 0 0 {name=l25 lab=GND}
C {vdd.sym} 820 -440 0 0 {name=l26 lab=VDD}
C {lab_wire.sym} 730 -340 0 0 {name=l27 sig_type=std_logic lab=B
}
C {lab_wire.sym} 860 -340 2 0 {name=l28 sig_type=std_logic lab=BN
}
C {lab_wire.sym} 330 -370 0 0 {name=l29 sig_type=std_logic lab=AN
}
C {lab_wire.sym} 140 -290 0 0 {name=l30 sig_type=std_logic lab=BN
}
C {opin.sym} 440 -230 0 0 {name=p3 lab=Y}
