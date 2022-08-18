v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 240 -90 240 -80 { lab=#net1}
N 80 -150 140 -150 { lab=outp}
N 140 -150 175 -120 { lab=outp}
N 175 -120 200 -120 { lab=outp}
N 120 -120 160 -150 { lab=outn}
N 160 -150 240 -150 { lab=outn}
N 50 -190 80 -190 { lab=outp}
N 240 -190 290 -190 { lab=outn}
N 445 -90 445 -80 { lab=Ibias}
N 395 -82.5 395 -50 { lab=Ibias}
N 395 -90 395 -82.5 { lab=Ibias}
N 395 -90 445 -90 { lab=Ibias}
N 445 -120 445 -90 { lab=Ibias}
N 445 -120 477.5 -120 { lab=Ibias}
N 80 -190 80 -150 { lab=outp}
N 240 -190 240 -150 { lab=outn}
N 383 -50 395 -50 { lab=Ibias}
N 383 -50 383 -47 { lab=Ibias}
N 280 -50 280 -47 { lab=Ibias}
N 395 -50 405 -50 { lab=Ibias}
N 80 -90 80 -80 { lab=#net2}
N 280 -47 383 -47 { lab=Ibias}
N 120 -47 280 -47 { lab=Ibias}
N 120 -50 120 -47 { lab=Ibias}
N 80 -20 95 -20 { lab=#net3}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 100 -120 0 1 {name=M1
}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 220 -120 0 0 {name=M2
}
C {devices/ipin.sym} 477.5 -120 0 1 {name=p1 lab=Ibias
}
C {devices/gnd.sym} 95 -19.5 0 0 {name=l1 lab=GND}
C {devices/opin.sym} 290 -190 0 0 {name=p2 lab=outn
}
C {devices/opin.sym} 50 -190 0 1 {name=p3 lab=outp}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 260 -50 0 1 {name=M4
}
C {devices/gnd.sym} 240 -20 0 0 {name=l3 lab=GND}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 425 -50 0 0 {name=M5}
C {devices/gnd.sym} 445 -20 0 1 {name=l4 lab=GND}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 100 -50 0 1 {name=M3
}
