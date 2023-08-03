* Based on PMU_top_level_test.sp
<% from os import path %>
.lib '${model_file}' ${model_corner}

.include '${path.join(root_dir, 'blocks', platform, 'spice', 'auxcell.cdl')}'
.include '${netlist_path}'

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

.param vvdd = 1.8

.global VPWR VGND

Xdcdc_conv VPWR VGND VOUT VREF_in clk s[0] s[1]
+ sel_vh[0] sel_vh[1] sel_vh[2] sel_vh[3] sel_vh[4] sel_vh[5] sel_vl[0] sel_vl[1]
+ sel_vl[2] sel_vl[3] sel_vl[4] sel_vl[5] DCDC_CONV

* clk(5MHz - 0.2us)
vclk  clk VGND pulse 0 'vvdd'  0p 100p 100p 100n 200n

vs0 s[0] 0 dc 'vvdd'
vs1 s[1] 0 dc 'vvdd'

* set the dc-dc converter configuration
vselvh0 sel_vh[0] 0 dc ${sel_vh[0]}
vselvh1 sel_vh[1] 0 dc ${sel_vh[1]}
vselvh2 sel_vh[2] 0 dc ${sel_vh[2]}
vselvh3 sel_vh[3] 0 dc ${sel_vh[3]}
vselvh4 sel_vh[4] 0 dc ${sel_vh[4]}
vselvh5 sel_vh[5] 0 dc ${sel_vh[5]}

vselvl0 sel_vl[0] 0 dc ${sel_vl[0]}
vselvl1 sel_vl[1] 0 dc ${sel_vl[1]}
vselvl2 sel_vl[2] 0 dc ${sel_vl[2]}
vselvl3 sel_vl[3] 0 dc ${sel_vl[3]}
vselvl4 sel_vl[4] 0 dc ${sel_vl[4]}
vselvl5 sel_vl[5] 0 dc ${sel_vl[5]}

vREF VREF_in 0 dc 3.6

* VPWR VGND
vgnd VGND 0 dc 0
vpwr VPWR 0 dc 'vvdd'

* load
c1 0 VOUT 200f

* set the simulation parameters (5us)
.TRAN 50n 5000n
.measure TRAN vavg AVG v(VOUT) from=2000n to=5000n

.control
set num_threads=4
run
plot v(VOUT)
.endc

.END