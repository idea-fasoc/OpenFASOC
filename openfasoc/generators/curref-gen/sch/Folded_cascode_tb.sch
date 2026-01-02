v {xschem version=3.4.6RC file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 320 -200 320 -180 {
lab=GND}
N 320 -300 320 -260 {
lab=VSS}
N 400 -200 400 -180 {
lab=GND}
N 320 -180 320 -160 {
lab=GND}
N 400 -300 400 -260 {
lab=VDD}
N -210 -390 -210 -280 {
lab=#net1}
N -210 -280 -150 -280 {
lab=#net1}
N -340 -390 -340 -350 {
lab=#net2}
N -340 -290 -340 -260 {
lab=GND}
N -340 -470 -340 -450 {
lab=#net3}
N -340 -390 -300 -390 {
lab=#net2}
N 10 -450 50 -450 {
lab=Vout}
N 50 -450 50 -280 {
lab=Vout}
N -90 -280 50 -280 {
lab=Vout}
N -210 -420 -210 -390 {
lab=#net1}
N -340 -480 -340 -470 {
lab=#net3}
N -340 -480 -180 -480 {
lab=#net3}
N -240 -390 -210 -390 {
lab=#net1}
N 400 -180 400 -160 {
lab=GND}
N 480 -200 480 -180 {
lab=GND}
N 480 -300 480 -260 {
lab=VrefBG}
N 480 -180 480 -160 {
lab=GND}
N -210 -430 -210 -420 {
lab=#net1}
N -210 -430 -180 -430 {
lab=#net1}
N -0 -450 10 -450 {
lab=Vout}
C {devices/lab_wire.sym} -110 -350 0 0 {name=p2 sig_type=std_logic lab=VDD}
C {devices/lab_wire.sym} 50 -450 0 1 {name=p11 sig_type=std_logic lab=Vout}
C {devices/vsource.sym} 320 -230 0 0 {name=V0 value=0 savecurrent=false}
C {devices/gnd.sym} 320 -160 0 0 {name=l3 lab=GND}
C {devices/vsource.sym} 400 -230 0 0 {name=V2 value=\{vdd\} savecurrent=false}
C {devices/lab_wire.sym} 320 -300 0 0 {name=p1 sig_type=std_logic lab=VSS}
C {devices/lab_wire.sym} 400 -300 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/corner.sym} -630 -460 0 0 {name=CORNER only_toplevel=false corner=tt}
C {ind.sym} -120 -280 1 0 {name=L1
m=1
value=100Meg
footprint=1206
device=inductor}
C {vsource.sym} -340 -320 0 0 {name=V1 value=0.9 savecurrent=false}
C {devices/gnd.sym} -340 -260 0 0 {name=l2 lab=GND}
C {vsource.sym} -340 -420 0 0 {name=V3 value="AC 1" savecurrent=false}
C {capa.sym} -270 -390 3 0 {name=C1
m=1
value=100Meg
footprint=1206
device="ceramic capacitor"}
C {devices/lab_wire.sym} -110 -330 0 0 {name=p3 sig_type=std_logic lab=VSS}
C {devices/lab_wire.sym} -110 -370 0 0 {name=p4 sig_type=std_logic lab=VrefBG}
C {devices/gnd.sym} 400 -160 0 0 {name=l4 lab=GND}
C {devices/vsource.sym} 480 -230 0 0 {name=V4 value=\{VrefBG\} savecurrent=false}
C {devices/lab_wire.sym} 480 -300 0 0 {name=p6 sig_type=std_logic lab=VrefBG}
C {devices/gnd.sym} 480 -160 0 0 {name=l5 lab=GND}
C {simulator_commands.sym} -760 -460 0 0 {name="COMMANDS1"
simulator="ngspice"
only_toplevel="false" 
value="
.param vdd=1.8
.param VrefBG=1.2

.save

.control

    op
    show

    write Folded_cascode_tb.raw
    set appendwrite

    * run ac simulation
    ac dec 20 1 100e6

    * measure parameters
    let vout_mag = db(abs(v(Vout)))

    meas ac A0 find vout_mag at=1k

    write Folded_cascode_tb.raw
.endc
"}
C {/foss/designs/Folded_cascode/Folded_cascode.sym} -90 -450 0 0 {name=x1}
