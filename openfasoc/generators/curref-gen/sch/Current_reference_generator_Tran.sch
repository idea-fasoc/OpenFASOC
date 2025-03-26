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
lab=Vout}
N 580 -370 580 -230 {
lab=Vout}
N 450 -400 540 -400 {
lab=Vrefp}
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
N -250 -100 -250 -80 {
lab=GND}
N -250 -200 -250 -160 {
lab=VSS}
N -170 -100 -170 -80 {
lab=GND}
N -250 -80 -250 -60 {
lab=GND}
N -170 -200 -170 -160 {
lab=VDD}
N -170 -80 -170 -60 {
lab=GND}
N -90 -100 -90 -80 {
lab=GND}
N -90 -200 -90 -160 {
lab=VrefBG}
N -90 -80 -90 -60 {
lab=GND}
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
N 190 -380 270 -380 {
lab=Vin}
N 60 -430 270 -430 {
lab=Vout}
N 340 -220 580 -220 {
lab=Vout}
N 380 -340 400 -340 {
lab=#net1}
N 400 -330 500 -330 {
lab=#net1}
N 400 -340 400 -330 {
lab=#net1}
N 400 -360 500 -360 {
lab=#net1}
N 400 -360 400 -340 {
lab=#net1}
N 400 -300 500 -300 {
lab=#net1}
N 400 -330 400 -300 {
lab=#net1}
N 540 -330 580 -330 {
lab=Vout}
N 190 -380 190 -360 {
lab=Vin}
N 190 -200 190 -180 {
lab=GND}
N 60 -430 60 -80 {
lab=Vout}
N 60 -80 340 -80 {
lab=Vout}
N 340 -220 340 -80 {
lab=Vout}
N 190 -300 190 -260 {
lab=#net2}
N 1130 -160 1140 -160 {
lab=VSS}
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
C {devices/vsource.sym} -250 -130 0 0 {name=V0 value=0 savecurrent=false}
C {devices/gnd.sym} -250 -60 0 0 {name=l5 lab=GND}
C {devices/vsource.sym} -170 -130 0 0 {name=V2 value=1.8 savecurrent=false}
C {devices/lab_wire.sym} -250 -200 0 0 {name=p25 sig_type=std_logic lab=VSS}
C {devices/lab_wire.sym} -170 -200 0 0 {name=p26 sig_type=std_logic lab=VDD}
C {devices/gnd.sym} -170 -60 0 0 {name=l6 lab=GND}
C {devices/vsource.sym} -90 -130 0 0 {name=V4 value=1.2 savecurrent=false}
C {devices/lab_wire.sym} -90 -200 0 0 {name=p27 sig_type=std_logic lab=VrefBG}
C {devices/gnd.sym} -90 -60 0 0 {name=l7 lab=GND}
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
C {vsource.sym} 190 -230 0 0 {name=V6 value=1.2 savecurrent=false}
C {devices/gnd.sym} 190 -180 0 0 {name=l2 lab=GND}
C {lab_pin.sym} 580 -270 0 1 {name=p4 sig_type=std_logic lab=Vout}
C {/foss/designs/Folded_cascode/Folded_cascode.sym} 360 -400 0 0 {name=x1}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 520 -330 2 0 {name=M8
L=10
W=10
nf=1 mult=8
model=pfet_01v8_lvt
spiceprefix=X
}
C {simulator_commands.sym} -340 -360 0 0 {name=COMMANDS3
simulator="ngspice"
only_toplevel="false" 
value="
.param VDD=1.8
.param VrefBG=1.2

.save

.control

    op
    show

    write Current_reference_generator_Tran.raw
    set appendwrite

    * run tran simulation
    tran 1n 20u
    
    plot v(Vout) v(Vin)
    plot i(Iref1n)

    write Current_reference_generator_Tran.raw
.endc
"}
C {sky130_fd_pr/corner.sym} -170 -360 0 0 {name=CORNER only_toplevel=true corner=tt}
C {lab_pin.sym} 190 -380 2 1 {name=p22 sig_type=std_logic lab=Vin}
C {devices/vsource.sym} 190 -330 0 0 {name=V1 value="pwl 0 0 10u 0 1.001u 0.02"}
C {noconn.sym} 380 -360 2 0 {name=l1}
