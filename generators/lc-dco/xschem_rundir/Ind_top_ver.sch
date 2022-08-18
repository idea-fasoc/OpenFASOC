v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N -40 0 -0 -0 { lab=outp}
N 60 -0 100 -0 { lab=outn}
N 30 -61 30 -15 { lab=#net1}
C {sky130_fd_pr/ind_generic.sym} 30 0 1 0 {name=L1
model=ind_05_220
}
C {devices/iopin.sym} 100 0 0 0 {name=p1 lab=outn}
C {devices/iopin.sym} -30 0 2 0 {name=p2 lab=outp}
C {devices/iopin.sym} 40 -60 0 0 {name=p3 lab=VDD}
