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
N 450 -230 510 -230 { lab=CO}
N 130 -290 150 -290 { lab=VDD}
N 270 -290 290 -290 { lab=VDD}
N 200 -180 210 -180 { lab=GND}
N 200 -80 220 -80 { lab=GND}
N 140 -180 160 -180 { lab=A}
N 140 -80 160 -80 { lab=B}
N 450 -240 450 -210 { lab=CO}
N 370 -180 410 -180 { lab=#net1}
N 370 -260 370 -180 { lab=#net1}
N 370 -270 370 -260 { lab=#net1}
N 370 -270 410 -270 { lab=#net1}
N 270 -230 370 -230 { lab=#net1}
N 450 -350 450 -300 { lab=VDD}
N 450 -150 450 -130 { lab=GND}
N 450 -270 470 -270 { lab=VDD}
N 450 -180 470 -180 { lab=GND}
N 690 -410 690 -380 { lab=VDD}
N 640 -350 650 -350 { lab=#net1}
N 690 -350 710 -350 { lab=VDD}
N 830 -460 830 -430 { lab=VDD}
N 780 -400 790 -400 { lab=A}
N 830 -400 850 -400 { lab=VDD}
N 780 -320 790 -320 { lab=B}
N 830 -320 850 -320 { lab=VDD}
N 830 -370 830 -350 { lab=#net3}
N 710 -150 720 -150 { lab=GND}
N 830 -150 850 -150 { lab=GND}
N 760 -50 770 -50 { lab=GND}
N 760 -100 760 -80 { lab=#net4}
N 710 -100 760 -100 { lab=#net4}
N 710 -120 710 -100 { lab=#net4}
N 520 -350 640 -350 { lab=#net1}
N 520 -450 520 -350 { lab=#net1}
N 340 -450 520 -450 { lab=#net1}
N 340 -450 340 -240 { lab=#net1}
N 340 -240 340 -230 { lab=#net1}
N 340 -50 720 -50 { lab=#net1}
N 340 -230 340 -50 { lab=#net1}
N 650 -150 670 -150 { lab=A}
N 770 -150 790 -150 { lab=B}
N 760 -20 760 0 { lab=GND}
N 830 -120 830 -100 { lab=#net4}
N 760 -100 830 -100 { lab=#net4}
N 710 -210 710 -180 { lab=#net5}
N 710 -210 830 -210 { lab=#net5}
N 830 -210 830 -180 { lab=#net5}
N 690 -320 690 -270 { lab=#net5}
N 690 -270 830 -270 { lab=#net5}
N 830 -290 830 -270 { lab=#net5}
N 760 -270 760 -210 { lab=#net5}
N 1030 -230 1090 -230 { lab=S}
N 1030 -240 1030 -210 { lab=S}
N 950 -180 990 -180 { lab=#net5}
N 950 -260 950 -180 { lab=#net5}
N 950 -270 950 -260 { lab=#net5}
N 950 -270 990 -270 { lab=#net5}
N 1030 -350 1030 -300 { lab=VDD}
N 1030 -150 1030 -130 { lab=GND}
N 1030 -270 1050 -270 { lab=VDD}
N 1030 -180 1050 -180 { lab=GND}
N 760 -240 950 -240 { lab=#net5}
C {vdd.sym} 130 -350 0 0 {name=l1 lab=VDD}
C {vdd.sym} 270 -350 0 0 {name=l2 lab=VDD}
C {gnd.sym} 200 -20 0 0 {name=l3 lab=GND}
C {ipin.sym} 70 -290 0 0 {name=p3 lab=A
}
C {ipin.sym} 220 -290 0 0 {name=p4 lab=B
}
C {opin.sym} 510 -230 0 0 {name=p5 lab=CO}
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
C {vdd.sym} 690 -410 0 0 {name=l15 lab=VDD}
C {pmos4.sym} 670 -350 0 0 {name=X6 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {lab_wire.sym} 710 -350 2 0 {name=l16 sig_type=std_logic lab=VDD}
C {vdd.sym} 690 -410 0 0 {name=l17 lab=VDD}
C {vdd.sym} 830 -460 0 0 {name=l18 lab=VDD}
C {pmos4.sym} 810 -400 0 0 {name=X7 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {lab_wire.sym} 850 -400 2 0 {name=l19 sig_type=std_logic lab=VDD}
C {vdd.sym} 830 -460 0 0 {name=l20 lab=VDD}
C {pmos4.sym} 810 -320 0 0 {name=X9 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {lab_wire.sym} 850 -320 2 0 {name=l24 sig_type=std_logic lab=VDD}
C {nmos4.sym} 690 -150 0 0 {name=X10 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {nmos4.sym} 810 -150 0 0 {name=X11 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {lab_wire.sym} 720 -150 2 0 {name=l25 sig_type=std_logic lab=GND}
C {lab_wire.sym} 850 -150 2 0 {name=l26 sig_type=std_logic lab=GND}
C {nmos4.sym} 740 -50 0 0 {name=X12 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {lab_wire.sym} 770 -50 2 0 {name=l27 sig_type=std_logic lab=GND}
C {lab_wire.sym} 650 -150 0 0 {name=l28 sig_type=std_logic lab=A}
C {lab_wire.sym} 770 -150 0 0 {name=l29 sig_type=std_logic lab=B}
C {gnd.sym} 760 0 0 0 {name=l30 lab=GND}
C {lab_wire.sym} 780 -400 0 0 {name=l31 sig_type=std_logic lab=A}
C {lab_wire.sym} 780 -320 0 0 {name=l32 sig_type=std_logic lab=B}
C {pmos4.sym} 1010 -270 0 0 {name=X8 model=pmos_3p3 w=1.7u l=0.3u m=1}
C {nmos4.sym} 1010 -180 0 0 {name=X13 model=nmos_3p3 w=0.85u l=0.3u m=1}
C {vdd.sym} 1030 -350 0 0 {name=l21 lab=VDD}
C {gnd.sym} 1030 -130 0 0 {name=l22 lab=GND}
C {lab_wire.sym} 1050 -270 2 0 {name=l23 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 1050 -180 2 0 {name=l33 sig_type=std_logic lab=GND}
C {opin.sym} 1090 -230 0 0 {name=p1 lab=S}
