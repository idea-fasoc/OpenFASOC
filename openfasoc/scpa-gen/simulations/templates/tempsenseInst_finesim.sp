
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
+    DLENCSDF=10
+    post=0
+    nomod
+    method=gear
+    measdgt=10

.lib '@model_file' @model_corner
.include '@netlist'

.param temp_var = @temp
.param vvdd = @voltage
.param sim_end = 800m/exp(0.04*temp_var)

*@modelingxi1 en out VDD VIN VSS TEMP_sensor

*@verificationxi1 CLK_REF DONE DOUT[0] DOUT[10] DOUT[11]
*@verification+ DOUT[12] DOUT[13] DOUT[14] DOUT[15] DOUT[16] DOUT[17] DOUT[18]
*@verification+ DOUT[19] DOUT[1] DOUT[20] DOUT[21] DOUT[22] DOUT[23] DOUT[2]
*@verification+ DOUT[3] DOUT[4] DOUT[5] DOUT[6] DOUT[7] DOUT[8] DOUT[9] RESET_COUNTERn
*@verification+ SEL_CONV_TIME[0] SEL_CONV_TIME[1] SEL_CONV_TIME[2] SEL_CONV_TIME[3]
*@verification+ VDD VIN VSS en lc_out out outb tempsenseInst

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

.TRAN 1e-12 'sim_end'
*@modeling.meas tran period TRIG v(out) td=10p val=0.1 rise=2
*@modeling+		    TARG v(out) td=10p val=0.1 rise=3
*@verification.meas tran period TRIG v(lc_out) td=10p val=1.0 rise=2
*@verification+		    TARG v(lc_out) td=10p val=1.0 rise=3
.meas frequency param = '1/period'

*@partial.meas tran power AVG '-i(vVDD)*v(VDD)' from=10u to='sim_end'

*@full.meas	tran d0 find v(DOUT[0]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d1 find v(DOUT[1]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d2 find v(DOUT[2]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d3 find v(DOUT[3]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d4 find v(DOUT[4]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d5 find v(DOUT[5]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d6 find v(DOUT[6]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d7 find v(DOUT[7]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d8 find v(DOUT[8]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d9 find v(DOUT[9]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d10 find v(DOUT[10]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d11 find v(DOUT[11]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d12 find v(DOUT[12]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d13 find v(DOUT[13]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d14 find v(DOUT[14]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d15 find v(DOUT[15]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d16 find v(DOUT[16]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d17 find v(DOUT[17]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d18 find v(DOUT[18]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d19 find v(DOUT[19]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d20 find v(DOUT[20]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d21 find v(DOUT[21]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d22 find v(DOUT[22]) when v(DONE)='0.9*vvdd' rise=last
*@full.meas	tran d23 find v(DOUT[23]) when v(DONE)='0.9*vvdd' rise=last


.END
