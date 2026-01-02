v {xschem version=3.4.6RC file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 210 -60 210 -40 {
lab=GND}
N 210 -150 210 -120 {
lab=VrefBG}
N 140 -60 140 -40 {
lab=GND}
N 140 -150 140 -120 {
lab=VSS}
N 70 -60 70 -40 {
lab=GND}
N 70 -150 70 -120 {
lab=VDD}
N 650 -100 670 -100 {
lab=VDD}
N 650 -80 670 -80 {
lab=VSS}
N 650 -60 670 -60 {
lab=VrefBG}
N 600 -160 620 -160 {
lab=#net1}
N 600 -220 620 -220 {
lab=#net2}
N 810 -190 940 -190 {
lab=#net3}
N 940 -340 940 -190 {
lab=#net3}
N 550 -340 550 -220 {
lab=#net2}
N 550 -220 600 -220 {
lab=#net2}
N 760 -340 940 -340 {
lab=#net3}
N 550 -340 700 -340 {
lab=#net2}
N 490 -340 550 -340 {
lab=#net2}
C {devices/vsource.sym} 210 -90 0 0 {name=VrefBG value="1.2" savecurrent=false}
C {devices/gnd.sym} 210 -40 0 0 {name=l6 lab=GND}
C {lab_pin.sym} 210 -150 0 1 {name=p7 sig_type=std_logic lab=VrefBG}
C {devices/vsource.sym} 140 -90 0 0 {name=VSS value="0" savecurrent=false}
C {devices/gnd.sym} 140 -40 0 0 {name=l7 lab=GND}
C {lab_pin.sym} 140 -150 0 1 {name=p9 sig_type=std_logic lab=VSS}
C {devices/vsource.sym} 70 -90 0 0 {name=VDD value="1.8" savecurrent=false}
C {devices/gnd.sym} 70 -40 0 0 {name=l8 lab=GND}
C {lab_pin.sym} 70 -150 0 1 {name=p14 sig_type=std_logic lab=VDD}
C {/foss/designs/Folded_cascode/Folded_cascode_test.sym} 690 -190 0 0 {name=x1}
C {lab_pin.sym} 650 -100 2 1 {name=p3 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 650 -80 2 1 {name=p1 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 650 -60 2 1 {name=p2 sig_type=std_logic lab=VrefBG}
C {simulator_commands.sym} 30 -290 0 0 {name=COMMANDS
simulator=ngspice
only_toplevel=false 
value="
.save
+ @m.xm1.msky130_fd_pr__nfet_01v8[gm]
+ v(@m.xm1.msky130_fd_pr__nfet_01v8[vth])
+ @m.xm1.msky130_fd_pr__nfet_01v8[gds]
+ @m.xm1.msky130_fd_pr__nfet_01v8[id]

+ @m.xm6.msky130_fd_pr__nfet_01v8[gm]
+ v(@m.xm6.msky130_fd_pr__nfet_01v8[vth])
+ @m.xm6.msky130_fd_pr__nfet_01v8[gds]
+ @m.xm6.msky130_fd_pr__nfet_01v8[id]

+ @m.xm7.msky130_fd_pr__nfet_01v8[gm]
+ v(@m.xm7.msky130_fd_pr__nfet_01v8[vth])
+ @m.xm7.msky130_fd_pr__nfet_01v8[gds]
+ @m.xm7.msky130_fd_pr__nfet_01v8[id]

+ @m.xm8.msky130_fd_pr__nfet_01v8[gm]
+ v(@m.xm8.msky130_fd_pr__nfet_01v8[vth])
+ @m.xm8.msky130_fd_pr__nfet_01v8[gds]
+ @m.xm8.msky130_fd_pr__nfet_01v8[id]

+ @m.xm9.msky130_fd_pr__nfet_01v8[gm]
+ v(@m.xm9.msky130_fd_pr__nfet_01v8[vth])
+ @m.xm9.msky130_fd_pr__nfet_01v8[gds]
+ @m.xm9.msky130_fd_pr__nfet_01v8[id]

+ @m.xm10.msky130_fd_pr__nfet_01v8[gm]
+ v(@m.xm10.msky130_fd_pr__nfet_01v8[vth])
+ @m.xm10.msky130_fd_pr__nfet_01v8[gds]
+ @m.xm10.msky130_fd_pr__nfet_01v8[id]

+ @m.xm11.msky130_fd_pr__nfet_01v8[gm]
+ v(@m.xm11.msky130_fd_pr__nfet_01v8[vth])
+ @m.xm11.msky130_fd_pr__nfet_01v8[gds]
+ @m.xm11.msky130_fd_pr__nfet_01v8[id]

+ @m.xm12.msky130_fd_pr__nfet_01v8[gm]
+ v(@m.xm12.msky130_fd_pr__nfet_01v8[vth])
+ @m.xm12.msky130_fd_pr__nfet_01v8[gds]
+ @m.xm12.msky130_fd_pr__nfet_01v8[id]

+ @m.xm13.msky130_fd_pr__nfet_01v8[gm]
+ v(@m.xm13.msky130_fd_pr__nfet_01v8[vth])
+ @m.xm13.msky130_fd_pr__nfet_01v8[gds]
+ @m.xm13.msky130_fd_pr__nfet_01v8[id]

+ @m.xm17.msky130_fd_pr__nfet_01v8[gm]
+ v(@m.xm17.msky130_fd_pr__nfet_01v8[vth])
+ @m.xm17.msky130_fd_pr__nfet_01v8[gds]
+ @m.xm17.msky130_fd_pr__nfet_01v8[id]

+ @m.xm2.msky130_fd_pr__pfet_01v8[gm]
+ v(@m.xm2.msky130_fd_pr__pfet_01v8[vth])
+ @m.xm2.msky130_fd_pr__pfet_01v8[gds]
+ @m.xm2.msky130_fd_pr__pfet_01v8[id]

+ @m.xm3.msky130_fd_pr__pfet_01v8[gm]
+ v(@m.xm3.msky130_fd_pr__pfet_01v8[vth])
+ @m.xm3.msky130_fd_pr__pfet_01v8[gds]
+ @m.xm3.msky130_fd_pr__pfet_01v8[id]

+ @m.xm4.msky130_fd_pr__pfet_01v8[gm]
+ v(@m.xm4.msky130_fd_pr__pfet_01v8[vth])
+ @m.xm4.msky130_fd_pr__pfet_01v8[gds]
+ @m.xm4.msky130_fd_pr__pfet_01v8[id]

+ @m.xm5.msky130_fd_pr__pfet_01v8[gm]
+ v(@m.xm5.msky130_fd_pr__pfet_01v8[vth])
+ @m.xm5.msky130_fd_pr__pfet_01v8[gds]
+ @m.xm5.msky130_fd_pr__pfet_01v8[id]

+ @m.xm14.msky130_fd_pr__pfet_01v8[gm]
+ v(@m.xm14.msky130_fd_pr__pfet_01v8[vth])
+ @m.xm14.msky130_fd_pr__pfet_01v8[gds]
+ @m.xm14.msky130_fd_pr__pfet_01v8[id]

+ @m.xm15.msky130_fd_pr__pfet_01v8[gm]
+ v(@m.xm15.msky130_fd_pr__pfet_01v8[vth])
+ @m.xm15.msky130_fd_pr__pfet_01v8[gds]
+ @m.xm15.msky130_fd_pr__pfet_01v8[id]

+ @m.xm16.msky130_fd_pr__pfet_01v8[gm]
+ v(@m.xm16.msky130_fd_pr__pfet_01v8[vth])
+ @m.xm16.msky130_fd_pr__pfet_01v8[gds]
+ @m.xm16.msky130_fd_pr__pfet_01v8[id]


.control
  save all
  op
  show
  write Folded_cascode.raw
.endc
"}
C {ind.sym} 730 -340 1 0 {name=L1
m=1
value=1G
footprint=1206
device=inductor}
C {ipin.sym} 100 -430 0 0 {name=p4 lab=Vin}
C {capa.sym} 460 -340 1 0 {name=C1
m=1
value=1p
footprint=1206
device="ceramic capacitor"}
