** sch_path: /home/lmadhu/openmpw/pdk_1/Project_gf180_tp/xschem/Amplifiers/OTA_2stage.sch
**.subckt OTA_2stage vout vin1 vin2 vdd vss vp
*.opin vout
*.ipin vin1
*.ipin vin2
*.iopin vdd
*.iopin vss
*.ipin vp



**** begin user architecture code

.lib /gf180mcuA/libs.tech/ngspice/sm141064.ngspice typical

.include /gf180mcuA/libs.tech/ngspice/design.ngspice
.param  sw_stat_mismatch = 0

.save @m.xm9.m0[id]
.save @m.xm10.m0[id]
.save @m.xm7.m0[id]
.save @m.xm6.m0[id]
.save @m.xm5.m0[id]
.save @m.xm4.m0[id]
.save @m.xm3.m0[id]
.save @m.xm2.m0[id]
.save @m.xm1.m0[id]

.save @m.xm10.m0[vth]
.save @m.xm10.m0[gm]
.save @m.xm10.m0[gds]


.save @m.xm7.m0[vth]
.save @m.xm7.m0[gm]
.save @m.xm7.m0[gds]
.save @m.xm6.m0[vth]
.save @m.xm6.m0[gm]
.save @m.xm6.m0[gds]
.save @m.xm5.m0[vth]
.save @m.xm5.m0[gm]
.save @m.xm5.m0[gds]
.save @m.xm4.m0[vth]
.save @m.xm4.m0[gm]
.save @m.xm4.m0[gds]
.save @m.xm3.m0[vth]
.save @m.xm3.m0[gm]
.save @m.xm3.m0[gds]
.save @m.xm2.m0[vth]
.save @m.xm2.m0[gm]
.save @m.xm2.m0[gds]
.save @m.xm1.m0[vth]
.save @m.xm1.m0[gm]
.save @m.xm1.m0[gds]
.save all
.control
run
let a = 0
let step = 0.05
let final = 2
let test = a
let test1 = a
let cnt = 0
let ind = ((final-a)/step)
let n = vector(ind)
let power = vector(ind)

set color0 = white
set color1 = black
set hcopydevtype = svg
setcs svg_stropts = ( black Arial Arial )

set gain = ' '
set phasedeg = ' '
set tranout = ' '
set nolegend

while test le final
alter @v5[dc] = test
print @v5[dc]
let test = test + step
ac dec 10 1 300MEG
let phase = {57.29*vp(vout)}-180
set gain = ( $gain db({$curplot}.vout) )
set phasedeg = ( $phasedeg ({$curplot}.phase) )
end

plot $gain xlabel Frequency(Hz) ylabel Gain(db) title Gain(dB)
plot $phasedeg xlabel Frequency(Hz) ylabel Phase(deg) title Phase(deg)

hardcopy Gain.svg $gain label Frequency(Hz) ylabel Gain(db) title 'OTA_2stage Gain'
hardcopy Phase.svg $phasedeg xlabel Frequency(Hz) ylabel Phase(deg) title 'OTA_2stage Phase'

let test = a
while test le final
alter @v5[dc] = test
print @v5[dc]
let test = test + step
tran 1ns 100ns 0
set tranout = ( $tranout ({$curplot}.vout) )
end


plot $tranout xlabel Time(ns) ylabel Output(V) title Output_Signal

hardcopy Transient.svg $tranout xlabel Time(ns) ylabel Output title 'OTA_2stage Transient Plot'


while test1 le final
alter @v5[dc] = test1
print @v5[dc]
save all
let ic = @m.xm5.m0[id] + @m.xm6.m0[id] + @m.xm9.m0[id]
let power[cnt] = 3.3*ic
let test1 = test1 + step
noise v(vout) v3 dec 100 20K 2MEG 1
let n[cnt] = inoise_total
let cnt = cnt + 1
end

plot n vs power xlabel Power(mW) ylabel Integrated_Noise(uV) title Integrated_Noise

hardcopy Noise.svg n vs power xlabel Power(mW) ylabel Integrated_Noise(uV) title 'OTA_2stage Integrated_Noise'
.endc

**** end user architecture code
**.ends
.GLOBAL GND
.end
