
.TEMP temp_var
.OPTION sim_la
.OPTION autostop
.OPTION
+    artist=2
+    ingold=2
+    parhier=LOCAL
+    psf=2
+    gmin=1E-25
+    gmindc=1E-25
+    reltol=1E-6
+    dvdt=2
+    lvltim=3
+    runlvl=6
+    post=0
+    nomod
+    method=gear
*+    accurate
*+    probe
*+    kcltest
*+    measdgt=8
*+    numdgt=12

.lib '@model_file' @model_corner
.include '@netlist'

.param temp_var = @temp
.param vvdd = @voltage
.param sim_end = 80000u/exp(0.04*temp_var)
.csparam sim_end_const = 'sim_end'
.csparam temp_const = 'temp_var'
*.param sim_end = 20u

xi1  VSS VDD DOUT[12] DOUT[13] lc_out DOUT[15] DOUT[2] VIN en
+ DOUT[14] DOUT[11] out outb DOUT[23] DOUT[9] DOUT[16] DOUT[22] DOUT[1] DOUT[0]
+ CLK_REF DOUT[10] DOUT[18] DOUT[3] DOUT[21] DOUT[19] DOUT[8] DOUT[4] DOUT[17]
+ DOUT[20] DONE DOUT[6] DOUT[7] DOUT[5] SEL_CONV_TIME[1] RESET_COUNTERn
+ SEL_CONV_TIME[3] SEL_CONV_TIME[0] SEL_CONV_TIME[2] designName


vCLK_REF                  CLK_REF                  0                  pulse		0 'vvdd' 12u 1n 1n '4/32768' '8/32768'
vRESET_COUNTERn           RESET_COUNTERn           0                  pwl		0 0 5u 0 '5u+1n' 'vvdd'
vSEL_CONV_TIME<3>         SEL_CONV_TIME[3]         0                  dc                0
vSEL_CONV_TIME<2>         SEL_CONV_TIME[2]         0                  dc                0
vSEL_CONV_TIME<1>         SEL_CONV_TIME[1]         0                  dc                0
vSEL_CONV_TIME<0>         SEL_CONV_TIME[0]         0                  dc                0
ven                       en                       0                  pwl       0 0 10u 0 '10u+1n' 'vvdd'
vVDD                      VDD                      0                  pwl		0 0 1u 0 2u 'vvdd'
vVSS                      VSS                      0                  dc                0

c0 lc_out 0 1f

.TRAN 1n 'sim_end'

*.meas	tran d0 find v(xasync_counter_0/div_s<0>) when v(done)=0.6 rise=last
*.meas	tran d1 find v(xasync_counter_0/div_s<1>) when v(done)=0.6 rise=last
*.meas	tran d2 find v(xasync_counter_0/div_s<2>) when v(done)=0.6 rise=last
*.meas	tran d3 find v(xasync_counter_0/div_s<3>) when v(done)=0.6 rise=last
*.meas	tran d4 find v(xasync_counter_0/div_s<4>) when v(done)=0.6 rise=last
*.meas	tran d5 find v(xasync_counter_0/div_s<5>) when v(done)=0.6 rise=last
*.meas	tran d6 find v(xasync_counter_0/div_s<6>) when v(done)=0.6 rise=last
*.meas	tran d7 find v(xasync_counter_0/div_s<7>) when v(done)=0.6 rise=last
*.meas	tran d8 find v(xasync_counter_0/div_s<8>) when v(done)=0.6 rise=last
*.meas	tran d9 find v(xasync_counter_0/div_s<9>) when v(done)=0.6 rise=last
*.meas	tran d10 find v(xasync_counter_0/div_s<10>) when v(done)=0.6 rise=last
*.meas	tran d11 find v(xasync_counter_0/div_s<11>) when v(done)=0.6 rise=last
*.meas	tran d12 find v(xasync_counter_0/div_s<12>) when v(done)=0.6 rise=last
*.meas	tran d13 find v(xasync_counter_0/div_s<13>) when v(done)=0.6 rise=last
*.meas	tran d14 find v(xasync_counter_0/div_s<14>) when v(done)=0.6 rise=last
*.meas	tran d15 find v(xasync_counter_0/div_s<15>) when v(done)=0.6 rise=last
*.meas	tran d16 find v(xasync_counter_0/div_s<16>) when v(done)=0.6 rise=last
*.meas	tran d17 find v(xasync_counter_0/div_s<17>) when v(done)=0.6 rise=last
*.meas	tran d18 find v(xasync_counter_0/div_s<18>) when v(done)=0.6 rise=last
*.meas	tran d19 find v(xasync_counter_0/div_s<19>) when v(done)=0.6 rise=last
*.meas	tran d20 find v(xasync_counter_0/div_s<20>) when v(done)=0.6 rise=last
*.meas	tran d21 find v(xasync_counter_0/div_s<21>) when v(done)=0.6 rise=last
*.meas	tran d22 find v(xasync_counter_0/div_s<22>) when v(done)=0.6 rise=last
*.meas	tran d23 find v(xasync_counter_0/div_s<23>) when v(done)=0.6 rise=last

*.PROBE v(out)
.control
run

meas    tran period TRIG v(lc_out) td=10p val=1.0 rise=2
+           TARG v(lc_out) td=10p val=1.0 rise=3

let frequency = 1/period

let power_avg = -i(vVDD)*v(VDD)
let start_time = 10u
let end_time = sim_end_const
meas tran power AVG power_avg FROM=start_time TO=end_time
meas tran vin AVG v(VIN) from=start_time to=end_time

set wr_singlescale
set wr_vecnames
set noprintscale true

let data = j(vector(5))
let data[0] = period
let data[1] = frequency
let data[2] = power
let data[3] = vin
let data[4] = temp_const

print line data > tempsenseInst_@temp.mt0

quit
.endc

.END
