
**************************Description*************************************
*                                                                        *
* This is the testbench file, including the circuit, model, and stimuli. *
* For those who use ngspice, just type ngspice comparator_control.sp     *
* There are several parameters in this scripts can be changed. Onw thing *
* is pending now, which is the way to change parameters which is used in *
* the control part in the beginning instead of in the control part.      *
*                                                                        *
**************************************************************************


**************************parameter************************************

.param clk_period = 1440p            ; clock cycle 

**************************Other Parameter********************************

.param pulse = 'clk_period / 2'      ; pusle width
.param risetime = 'clk_period /10'   ; rise time
.param falltime = 'clk_period /10'   ; falltime 
.param delay = 'clk_period / 4'      ; delay
*.csparam pausetime = {delay}
*.csparam pulse = {pulse}

**************************Comparator.spice***************************

**.subckt comparator CLK AVSS IN- IN+ AV33 CMP+ CMP- CLKB
*.iopin CLK
*.iopin AVSS
*.iopin IN-
*.iopin IN+
*.iopin AV33
*.iopin CMP+
*.iopin CMP-
*.iopin CLKB

************************Include Model and Circuit Netlist*************

.include ../src/comparator.spice  ; circuit netlist
.include ../model/model.spice     ; model path



.option wnflag=1
**************************STIMULI************************************

vip in+ 0 dc 1.6
vin in- 0 dc 1.5
v33 av33 0 dc 3.3
vgnd avss 0 dc 0
vclk clk 0 dc 0 pulse(0 3.3 delay risetime falltime pulse clk_period)
vclkb clkb 0 dc 0 pulse(3.3 0 delay risetime falltime pulse clk_period)

*inoise cmp- avss dc 0 trnoise(1m 1u 1.0 0.1m)

****************************control part************************************

.control


set filetype=ascii
set path = "../output/comparator.out"   ; output file path(for furthor analysis)

wrdata $path 1
set appendwrite



**************************offset simulation (monte carlo)*************************

*********parameter***********
set points = 100            ; monte carlo points
set offsetmin = -20m        ; offset min
set offsetmax = 20m         ; offset max
set stoptime = 1.08n        ; save the value at this point to the output file
set risetime = 720p

set wr_singlescale
*set wr_vecnames
*set notrnoise
option numdgt=5

save v(in+)
save v(in-)
save v(cmp+)

let run = 1
while run le $points
	set run = $&run
	setseed $run

	let v_start = $offsetmin
	let v_stop = $offsetmax
	let v_act = v_start
	let v_delta = 1m
	let v_act = v_start

	while v_act le v_stop
		echo $&v_act
		alter vip 1.5+v_act
		alter vin 1.5-v_act
		stop when time=$stoptime
		tran $risetime 20u $stoptime
		wrdata $path v(in+) v(in-) v(cmp+)
		set appendwrite
		echo move to the next vid
		let v_act = v_act + v_delta
	end

	*wrdata comparator.out all.v(cmp+) all.vip
	let run = run + 1
	reset
end


**************************Functionality**********************************
*save all
save v(in+) 
save v(in-)
save v(clk)
save v(clkb)
save v(di-)
save v(di+)
save v(cmp+)
save v(cmp-)

tran $risetime 10n


plot v(in+) v(in-)
plot v(clk) v(clkb)
plot v(di-) v(di+)
plot v(cmp+) v(cmp-)
*write comparator.raw

.endc

.GLOBAL GND
.end


