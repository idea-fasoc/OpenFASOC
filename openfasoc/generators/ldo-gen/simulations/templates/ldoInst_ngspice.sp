* VREG and load current Transient

* include from .../sky130A/libs.tech/ngspice/sky130.lib.spice
.lib '@model_file' @model_corner
* include the LDO spice netlist
.include 'ldo_sim.spice'


xi1 clk cmp_out ctrl_out[0] ctrl_out[1] ctrl_out[2] ctrl_out[3]
+ ctrl_out[4] ctrl_out[5] ctrl_out[6] ctrl_out[7] ctrl_out[8] mode_sel[0] mode_sel[1]
+ reset std_ctrl_in std_pt_in_cnt[0] std_pt_in_cnt[1] std_pt_in_cnt[2] std_pt_in_cnt[3]
+ std_pt_in_cnt[4] std_pt_in_cnt[5] std_pt_in_cnt[6] std_pt_in_cnt[7] std_pt_in_cnt[8]
+ trim1 trim10 trim2 trim3 trim4 trim5 trim6 trim7 trim8 trim9 VDD VSS VREF VREG ldoInst


*Controls
V0 VSS 0 dc 0
V1 VDD VSS pwl 0 0 2n 0 2.0001n 3.3
V2 VREF VSS pwl 0 0 2n 0 2.0001n @VALUE_REF_VOLTAGE  ;to be commented if using Analog Vref block

vtrim1 trim1 0 DC=0
vtrim2 trim2 0 DC=0
vtrim3 trim3 0 DC=0
vtrim4 trim4 0 DC=0
vtrim5 trim5 0 DC=0
vtrim6 trim6 0 DC=0
vtrim7 trim7 0 DC=0
vtrim8 trim8 0 DC=0
vtrim9 trim9 0 DC=0
vtrim10 trim10 DC=0

*With ideal VRef block
V3 clk  VSS pulse 0 3.3 0 1n 1n 5u 10u  ; change here if want to change clock frequency

V4 reset 0 pwl 0 3.3 10n 3.3 10.1n 0

V5 mode_sel[0] VSS 3.3
V6 mode_sel[1] VSS 3.3
vctrl std_ctrl_in 0 dc 0
vstd0 std_pt_in_cnt[0] 0 dc 0
vstd1 std_pt_in_cnt[1] 0 dc 0
vstd2 std_pt_in_cnt[2] 0 dc 0
vstd3 std_pt_in_cnt[3] 0 dc 0
vstd4 std_pt_in_cnt[4] 0 dc 0
vstd5 std_pt_in_cnt[5] 0 dc 0
vstd6 std_pt_in_cnt[6] 0 dc 0
vstd7 std_pt_in_cnt[7] 0 dc 0
vstd8 std_pt_in_cnt[8] 0 dc 0

R1 VREG VSS 3.6k
*Resistance 3600 --> 0.5 mA for 1.8 V reference voltage. R to be adjusted according to Iload and output voltage.

*R0 VREG 0 R='TIME > 500u ? 720 : 3600' ;If want to do a transient simulation where I load is changing in the middle of a transient simulation. Example: Here it is changing from 720 ohm (2.5mA) to 3600 ohm (0.5 mA) at t = 1000us

C1 VREG VSS 0.2n

*.options savecurrents
.options rshunt=1e12
.ic v(VREG) = 0 v(clk) =0 v(reset)=3.3
*Analysis
.temp 25
.tran 50n 1000u uic

.probe V(VREG)
.control
run
meas TRAN id find I(R1) AT=300u
* setting vec names prints names of columns
* set wr_vecnames

* wrdata VREG_I.csv VREG
*set hcopydev
*set hcopydevtype=svg
*set hcopypscolor=1
*hardcopy vregPlot.ps v(VREG) v(VREF)
*hardcopy cmp_out_clk_plot.ps cmp_out clk

write output.raw v(VREG) v(VREF) cmp_out clk (("ctrl_out[0]"+2*"ctrl_out[1]"+4*"ctrl_out[2]"+8*"ctrl_out[3]"+16*"ctrl_out[4]"+32*"ctrl_out[5]"+ 64*"ctrl_out[6]"+128*"ctrl_out[7]"+ 256*"ctrl_out[8]")/3.3) ;Last variable is for the counter indicating number of switches that are turning ON (ctrl_word_cnt)

.endc
.end
