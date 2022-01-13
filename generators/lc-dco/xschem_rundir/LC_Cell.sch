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
N 80 -330 80 -150 { lab=outp}
N 80 -330 120 -330 { lab=outp}
N 180 -330 230 -330 { lab=outn}
N 240 -330 240 -150 { lab=outn}
N 230 -330 240 -330 { lab=outn}
N 80 -190 120 -190 { lab=outp}
N 180 -190 240 -190 { lab=outn}
N 50 -190 80 -190 { lab=outp}
N 240 -190 290 -190 { lab=outn}
N 150 -370 150 -340 { lab=VDD}
N 280 -50 302.5 -50 { lab=Ibias}
N 120 -47.5 200 -47.5 { lab=Ibias}
N 200 -82.5 200 -47.5 { lab=Ibias}
N 200 -82.5 290 -82.5 { lab=Ibias}
N 290 -82.5 290 -50 { lab=Ibias}
N 445 -90 445 -80 { lab=Ibias}
N 382.5 -50 405 -50 { lab=Ibias}
N 395 -82.5 395 -50 { lab=Ibias}
N 302.5 -50 382.5 -50 { lab=Ibias}
N 395 -90 395 -82.5 { lab=Ibias}
N 395 -90 445 -90 { lab=Ibias}
N 445 -120 445 -90 { lab=Ibias}
N 445 -120 477.5 -120 { lab=Ibias}
N 80 -90 80 -77.5 { lab=#net2}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 100 -120 0 1 {name=M1
L=0.15
W=1
nf=24
mult=1
body=GND
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 220 -120 0 0 {name=M2
L=0.15
W=1
nf=24
mult=1
body=GND
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 100 -47.5 0 1 {name=M3
L=0.15
W=1
nf=48
mult=1
body=GND
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {devices/ipin.sym} 477.5 -120 0 1 {name=p1 lab=Ibias
}
C {devices/gnd.sym} 80 -17.5 0 0 {name=l1 lab=GND}
C {sky130_fd_pr/ind_generic.sym} 150 -330 1 0 {name=L1
**N=1
**L=1
** Other Params
spiceprefix=X
model=ind_05_220
}
C {sky130_fd_pr/cap_mim_m3_1.sym} 150 -190 3 0 {name=C1 model=cap_mim_m3_1 W=1 L=1 MF=1 spiceprefix=X}
C {devices/opin.sym} 290 -190 0 0 {name=p2 lab=outn
}
C {devices/opin.sym} 50 -190 0 1 {name=p3 lab=outp}
C {devices/vdd.sym} 150 -370 0 0 {name=l2 lab=VDD}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 260 -50 0 1 {name=M4
L=0.15
W=1
nf=48
mult=1
body=GND
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {devices/gnd.sym} 240 -20 0 0 {name=l3 lab=GND}
C {sky130_fd_pr/nfet3_01v8_lvt.sym} 425 -50 0 0 {name=M5
L=0.15
W=1
nf=48
mult=1
body=GND
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {devices/gnd.sym} 445 -20 0 1 {name=l4 lab=GND}
C {devices/netlist.sym} 17.5 -537.5 0 0 {name=s1 value=blabla}
C {devices/isource.sym} 445 -150 0 0 {name=I0 value=200u
}
C {devices/vdd.sym} 445 -180 0 0 {name=l5 lab=VDD}
C {devices/code.sym} 330 -537.5 0 0 {name=TT_MODELS
only_toplevel=true
format="tcleval(@value )"
value="** manual skywater pdks install (with patches applied)
* .lib \\\\$::SKYWATER_MODELS\\\\/models/sky130.lib.spice tt

** opencircuitdesign pdks install
.lib \\\\$::SKYWATER_MODELS\\\\/sky130.lib.spice tt

"
spice_ignore=false}
