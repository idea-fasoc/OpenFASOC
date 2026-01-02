v {xschem version=3.4.6RC file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Reference 1uA} 860 -60 0 0 0.4 0.4 {}
T {Reference 10uA} 1060 -60 0 0 0.4 0.4 {}
N 580 -230 580 -190 {
lab=#net1}
N 580 -370 580 -230 {
lab=#net1}
N 450 -400 540 -400 {
lab=Vrefp}
N 190 -380 270 -380 {
lab=VrefBG}
N 580 -130 580 -80 {
lab=VSS}
N 580 -520 580 -430 {
lab=VDD}
N 760 -520 760 -430 {
lab=VDD}
N 580 -430 580 -400 {
lab=VDD}
N 760 -430 760 -400 {
lab=VDD}
N 660 -400 720 -400 {
lab=Vrefp}
N 490 -460 490 -400 {
lab=Vrefp}
N 660 -460 660 -400 {
lab=Vrefp}
N 760 -370 760 -190 {
lab=Vrefn}
N 680 -160 720 -160 {
lab=Vrefn}
N 680 -240 680 -160 {
lab=Vrefn}
N 680 -240 760 -240 {
lab=Vrefn}
N 760 -130 760 -80 {
lab=VSS}
N 760 -160 760 -130 {
lab=VSS}
N 940 -130 940 -80 {
lab=VSS}
N 940 -160 940 -130 {
lab=VSS}
N 840 -160 900 -160 {
lab=Vrefn}
N 840 -220 840 -160 {
lab=Vrefn}
N 940 -430 940 -400 {
lab=VDD}
N 840 -400 900 -400 {
lab=Vrefp}
N 840 -460 840 -400 {
lab=Vrefp}
N 940 -520 940 -430 {
lab=VDD}
N 940 -260 940 -190 {
lab=Iref1n}
N 940 -370 940 -300 {
lab=Iref1p}
N 1140 -130 1140 -80 {
lab=VSS}
N 1140 -160 1140 -130 {
lab=VSS}
N 1040 -160 1100 -160 {
lab=Vrefn}
N 1040 -220 1040 -160 {
lab=Vrefn}
N 1140 -430 1140 -400 {
lab=VDD}
N 1040 -400 1100 -400 {
lab=Vrefp}
N 1040 -460 1040 -400 {
lab=Vrefp}
N 1140 -520 1140 -430 {
lab=VDD}
N 1140 -260 1140 -190 {
lab=Iref10n}
N 1140 -370 1140 -300 {
lab=Iref10p}
N -640 -110 -640 -90 {
lab=GND}
N -640 -210 -640 -170 {
lab=VSS}
N -560 -110 -560 -90 {
lab=GND}
N -640 -90 -640 -70 {
lab=GND}
N -560 -210 -560 -170 {
lab=VDD}
N -560 -90 -560 -70 {
lab=GND}
N -480 -110 -480 -90 {
lab=GND}
N -480 -210 -480 -170 {
lab=VrefBG}
N -480 -90 -480 -70 {
lab=GND}
N -400 -110 -400 -90 {
lab=GND}
N -400 -210 -400 -170 {
lab=V+}
N -400 -90 -400 -70 {
lab=GND}
N -320 -110 -320 -90 {
lab=GND}
N -320 -210 -320 -170 {
lab=V-}
N -320 -90 -320 -70 {
lab=GND}
N 190 -430 270 -430 {
lab=#net1}
N 70 -430 190 -430 {
lab=#net1}
N 70 -430 70 -220 {
lab=#net1}
N 70 -220 580 -220 {
lab=#net1}
N 1440 -230 1440 -190 {
lab=Iref1p}
N 1440 -130 1440 -80 {
lab=VSS}
N 1560 -230 1560 -190 {
lab=Iref10p}
N 1560 -130 1560 -80 {
lab=VSS}
N 1440 -510 1440 -470 {
lab=VDD}
N 1440 -410 1440 -360 {
lab=Iref1n}
N 1560 -510 1560 -470 {
lab=VDD}
N 1560 -410 1560 -360 {
lab=Iref10n}
C {/foss/designs/Folded_cascode/Folded_cascode.sym} 360 -400 0 0 {name=x1}
C {ipin.sym} -110 -150 0 0 {name=p22 lab=VrefBG}
C {iopin.sym} -130 -120 0 0 {name=p23 lab=VDD}
C {iopin.sym} -130 -90 0 0 {name=p24 lab=VSS}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 560 -400 0 0 {name=M1
L=10
W=2.25
nf=1 mult=2
model=pfet_01v8_lvt
spiceprefix=X
}
C {lab_pin.sym} 340 -320 2 1 {name=p3 sig_type=std_logic lab=VrefBG}
C {lab_pin.sym} 340 -300 2 1 {name=p1 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 340 -280 2 1 {name=p2 sig_type=std_logic lab=VSS}
C {res.sym} 580 -160 0 0 {name=R1
value=600k
footprint=1206
device=resistor
m=1}
C {lab_pin.sym} 190 -380 2 1 {name=p4 sig_type=std_logic lab=VrefBG}
C {lab_pin.sym} 580 -80 2 1 {name=p5 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 580 -520 2 1 {name=p6 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 740 -400 0 0 {name=M2
L=10
W=2.25
nf=1 mult=1
model=pfet_01v8_lvt
spiceprefix=X
}
C {lab_pin.sym} 760 -520 2 1 {name=p7 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 490 -460 0 1 {name=p8 sig_type=std_logic lab=Vrefp}
C {lab_pin.sym} 660 -460 0 1 {name=p9 sig_type=std_logic lab=Vrefp}
C {sky130_fd_pr/nfet_01v8.sym} 740 -160 0 0 {name=M5
W=0.5
L=10
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {lab_pin.sym} 760 -80 2 1 {name=p10 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/nfet_01v8.sym} 920 -160 0 0 {name=M6
W=0.5
L=10
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {lab_pin.sym} 940 -80 2 1 {name=p11 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 840 -220 0 1 {name=p12 sig_type=std_logic lab=Vrefn}
C {lab_pin.sym} 680 -220 0 0 {name=p13 sig_type=std_logic lab=Vrefn}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 920 -400 0 0 {name=M3
L=10
W=2.25
nf=1 mult=1
model=pfet_01v8_lvt
spiceprefix=X
}
C {lab_pin.sym} 840 -460 0 1 {name=p14 sig_type=std_logic lab=Vrefp}
C {lab_pin.sym} 940 -520 2 1 {name=p16 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/nfet_01v8.sym} 1120 -160 0 0 {name=M7
W=0.5
L=10
nf=1 
mult=10
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {lab_pin.sym} 1140 -80 2 1 {name=p17 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1040 -220 0 1 {name=p18 sig_type=std_logic lab=Vrefn}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 1120 -400 0 0 {name=M4
L=10
W=2.25
nf=1 mult=10
model=pfet_01v8_lvt
spiceprefix=X
}
C {lab_pin.sym} 1040 -460 0 1 {name=p19 sig_type=std_logic lab=Vrefp}
C {lab_pin.sym} 1140 -520 2 1 {name=p20 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/corner.sym} -610 -470 0 0 {name=CORNER only_toplevel=true corner=tt}
C {simulator_commands.sym} -460 -470 0 0 {name="COMMANDS"
simulator="ngspice"
only_toplevel="false" 
value="
.param VDD=1.8
.param VrefBG=1.2
.save

*nfet

+ @m.xm5.msky130_fd_pr__nfet_01v8[gm]
+ v(@m.xm5.msky130_fd_pr__nfet_01v8[vth])
+ @m.xm5.msky130_fd_pr__nfet_01v8[gds]
+ @m.xm5.msky130_fd_pr__nfet_01v8[id]

+ @m.xm6.msky130_fd_pr__nfet_01v8[gm]
+ v(@m.xm6.msky130_fd_pr__nfet_01v8[vth])
+ @m.xm6.msky130_fd_pr__nfet_01v8[gds]
+ @m.xm6.msky130_fd_pr__nfet_01v8[id]

+ @m.xm7.msky130_fd_pr__nfet_01v8[gm]
+ v(@m.xm7.msky130_fd_pr__nfet_01v8[vth])
+ @m.xm7.msky130_fd_pr__nfet_01v8[gds]
+ @m.xm7.msky130_fd_pr__nfet_01v8[id]

*pfet

+ @m.xm1.msky130_fd_pr__pfet_01v8_lvt[gm]
+ v(@m.xm1.msky130_fd_pr__pfet_01v8_lvt[vth])
+ @m.xm1.msky130_fd_pr__pfet_01v8_lvt[gds]
+ @m.xm1.msky130_fd_pr__pfet_01v8_lvt[id]

+ @m.xm2.msky130_fd_pr__pfet_01v8_lvt[gm]
+ v(@m.xm2.msky130_fd_pr__pfet_01v8_lvt[vth])
+ @m.xm2.msky130_fd_pr__pfet_01v8_lvt[gds]
+ @m.xm2.msky130_fd_pr__pfet_01v8_lvt[id]

+ @m.xm3.msky130_fd_pr__pfet_01v8_lvt[gm]
+ v(@m.xm3.msky130_fd_pr__pfet_01v8_lvt[vth])
+ @m.xm3.msky130_fd_pr__pfet_01v8_lvt[gds]
+ @m.xm3.msky130_fd_pr__pfet_01v8_lvt[id]

+ @m.xm4.msky130_fd_pr__pfet_01v8_lvt[gm]
+ v(@m.xm4.msky130_fd_pr__pfet_01v8_lvt[vth])
+ @m.xm4.msky130_fd_pr__pfet_01v8_lvt[gds]
+ @m.xm4.msky130_fd_pr__pfet_01v8_lvt[id]

.control
  save all
  op
  show
  write Current_reference_generator.raw
.endc
"}
C {devices/vsource.sym} -640 -140 0 0 {name=V0 value=0 savecurrent=false}
C {devices/gnd.sym} -640 -70 0 0 {name=l5 lab=GND}
C {devices/vsource.sym} -560 -140 0 0 {name=V2 value=\{VDD\} savecurrent=false}
C {devices/lab_wire.sym} -640 -210 0 0 {name=p25 sig_type=std_logic lab=VSS}
C {devices/lab_wire.sym} -560 -210 0 0 {name=p26 sig_type=std_logic lab=VDD}
C {devices/gnd.sym} -560 -70 0 0 {name=l6 lab=GND}
C {devices/vsource.sym} -480 -140 0 0 {name=V4 value=\{VrefBG\} savecurrent=false}
C {devices/lab_wire.sym} -480 -210 0 0 {name=p27 sig_type=std_logic lab=VrefBG}
C {devices/gnd.sym} -480 -70 0 0 {name=l7 lab=GND}
C {devices/vsource.sym} -400 -140 0 0 {name=V1 value=1.2 savecurrent=false}
C {devices/lab_wire.sym} -400 -210 0 0 {name=p28 sig_type=std_logic lab=V+}
C {devices/gnd.sym} -400 -70 0 0 {name=l8 lab=GND}
C {devices/vsource.sym} -320 -140 0 0 {name=V3 value=1.2 savecurrent=false}
C {devices/lab_wire.sym} -320 -210 0 0 {name=p29 sig_type=std_logic lab=V-}
C {devices/gnd.sym} -320 -70 0 0 {name=l9 lab=GND}
C {res.sym} 1440 -160 0 0 {name=R2
value=450k
footprint=1206
device=resistor
m=1}
C {lab_pin.sym} 1440 -80 2 1 {name=p15 sig_type=std_logic lab=VSS}
C {res.sym} 1560 -160 0 0 {name=R3
value=45k
footprint=1206
device=resistor
m=1}
C {lab_pin.sym} 1560 -80 2 1 {name=p21 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 940 -300 2 1 {name=p30 sig_type=std_logic lab=Iref1p}
C {lab_pin.sym} 1440 -230 2 1 {name=p31 sig_type=std_logic lab=Iref1p}
C {lab_pin.sym} 1560 -230 2 1 {name=p32 sig_type=std_logic lab=Iref10p}
C {lab_pin.sym} 1140 -300 2 1 {name=p33 sig_type=std_logic lab=Iref10p}
C {res.sym} 1440 -440 0 0 {name=R4
value=450k
footprint=1206
device=resistor
m=1}
C {res.sym} 1560 -440 0 0 {name=R5
value=45k
footprint=1206
device=resistor
m=1}
C {lab_pin.sym} 1440 -510 2 1 {name=p36 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1560 -510 2 1 {name=p37 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1140 -260 2 1 {name=p38 sig_type=std_logic lab=Iref10n}
C {lab_pin.sym} 940 -260 2 1 {name=p39 sig_type=std_logic lab=Iref1n}
C {lab_pin.sym} 1440 -360 2 1 {name=p34 sig_type=std_logic lab=Iref1n}
C {lab_pin.sym} 1560 -360 2 1 {name=p35 sig_type=std_logic lab=Iref10n}
