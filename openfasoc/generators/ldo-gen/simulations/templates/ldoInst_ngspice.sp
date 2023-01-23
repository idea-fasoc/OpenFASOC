* VREG and load current Transient

* include from .../sky130A/libs.tech/ngspice/sky130.lib.spice
.lib '@model_file' @model_corner
* include the LDO spice netlist
.include 'ldo_sim.spice'


xi1 @proper_pin_ordering ldoInst

*Controls
V0 VSS 0 DC=0
V1 VDD 0 DC=3.3
* to be commented if using Analog Vref block
V2 VREF 0 DC=@VALUE_REF_VOLTAGE

vtrim1 trim1 0 DC=0
vtrim2 trim2 0 DC=0
vtrim3 trim3 0 DC=0
vtrim4 trim4 0 DC=0
vtrim5 trim5 0 DC=0
vtrim6 trim6 0 DC=0
vtrim7 trim7 0 DC=0
vtrim8 trim8 0 DC=0
vtrim9 trim9 0 DC=0
vtrim10 trim10 0 DC=0

*With ideal VRef block
*change here if want to change clock frequency
V3 clk VSS pulse 0 3.3 0 1n 1n @duty_cycle @clk_period

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

R1 VREG VSS @Res_Value
*Resistance 3600 --> 0.5 mA for 1.8 V reference voltage. R to be adjusted according to Iload and output voltage.

*R0 VREG 0 R='TIME > 500u ? 720 : 3600' ;If want to do a transient simulation where I load is changing in the middle of a transient simulation. Example: Here it is changing from 720 ohm (2.5mA) to 3600 ohm (0.5 mA) at t = 1000us

C1 VREG VSS @Cap_Value

*.options savecurrents
.option wnflag=1
.options rshunt=1e11
.ic v(VREG) = 0 v(clk)=0 v(reset)=3.3
*Analysis
.temp 25
.tran @sim_step @sim_time

.probe V(VREG) v(VREF) v(cmp_out) v(clk) i(R1)
.control
run

*set hcopydevtype = svg
*set svg_intopts = ( 2560 1440 30 0 1 2 0 )
*setcs svg_stropts = ( white Arial Arial )
*set color1 = black
*set color2 = red
*hardcopy vregPlot.svg v(VREG) title 'LDO VREG startup transients with 1.8V VREF'
*hardcopy currentPlot.svg I(R1) title 'LDO load current startup transients with 1.8V VREF'
*hardcopy cmp_out_clk_plot.ps cmp_out clk

set filetype=binary
write @output_raw v(VREG) v(VREF) v(cmp_out) v(clk) v("ctrl_out[0]") v("ctrl_out[1]") v("ctrl_out[2]") v("ctrl_out[3]") v("ctrl_out[4]") v("ctrl_out[5]") v("ctrl_out[6]") v("ctrl_out[7]") v("ctrl_out[8]")

.endc

.GLOBAL VDD
.GLOBAL VSS

.end
