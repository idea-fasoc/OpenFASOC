* opamp_perf_eval.sp
** OpenFASOC Team, Ryan Wans 2023

** IMPORTANT:   Temperature setting is added automatically in the reading
**              of this file on line 6 as {@@TEMP}. DO NOT OVERRIDE.
.temp {@@TEMP}

** Define global parameters for altering
.param b1 = 0.8
.param b2 = 0.75

** Define netlist
Vsupply VDD GND 1.8
.save i(vsupply)
V2 vin net1 AC 0.5
.save i(v2)
V3 vip net1 AC -0.5
.save i(v3)
Vbias2 bias2 GND {b2}
.save i(vbias2)
Vbias1 bias1 GND {b1}
.save i(vbias1)
Vindc net1 GND 1
.save i(vindc)

** Import SKY130 libs (this should be replaced with a path relative to some env variable)

** Ali
** .lib /usr/local/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice tt
** .include /usr/local/share/pdk/sky130A/libs.ref/sky130_fd_sc_hvl/spice/sky130_fd_sc_hvl.spice

** Ryan
* .lib /home/rw/work/open_pdks/sky130/sky130A/libs.tech/ngspice/sky130.lib.spice tt
* .include /home/rw/work/open_pdks/sky130/sky130A/libs.ref/sky130_fd_sc_hvl/spice/sky130_fd_sc_hvl.spice

** Actual
.lib /usr/bin/miniconda3/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice tt
.include /usr/bin/miniconda3/share/pdk/sky130A/libs.ref/sky130_fd_sc_hvl/spice/sky130_fd_sc_hvl.spice

** Import opamp subcircuit
.include opamp_pex.spice
XDUT vin vip bias1 bias2 vo VDD GND opamp
* parameter sweep
** Run initial analysis
.save all
.options savecurrents
.ac dec 100 1k 10G
.control
** Set initial values
set filetype = ascii
let maxUGB = -1
let maxBv1 = -1
let maxBv2 = -1
let savedPhaseMargin = -1
let savedDCGain = -1
** Tune these
let biasVoltageMin = 0.4
let biasVoltageMax = 1.6
let biasVoltageStep = 0.1
let biasVoltage1 = biasVoltageMin
let biasVoltage2 = biasVoltageMin
** Sweep bias voltages
while biasVoltage1 le biasVoltageMax
    ** Alter parameters and reset top-level ckt
    alterparam b1 = $&biasVoltage1
    reset
    while biasVoltage2 le biasVoltageMax
        alterparam b2 = $&biasVoltage2
        reset
        ** Run analysis
        run
        ** Find unity-gain bw point
        meas ac ugb_f when vdb(vo)=0
        ** Measure phase margin
        let phase = (180/PI)*vp(vo)
        meas ac pm find phase when vdb(vo)=0
        ** Measure DC(ish) gain
        meas ac dcg find vdb(vo) at=1k
        ** Find local maxima
        if ( ugb_f ge maxUGB )
            let maxUGB = ugb_f
            let maxBv1 = biasVoltage1
            let maxBv2 = biasVoltage2
            let savedPhaseMargin = pm % 360
            let savedDCGain = dcg
        end
        let biasVoltage2 = biasVoltage2 + biasVoltageStep
    end
    ** Reset counter for bv2 loop
    let biasVoltage2 = biasVoltageMin
    let biasVoltage1 = biasVoltage1 + biasVoltageStep
end
** Export global maxima
wrdata result_ac.txt maxUGB maxBv1 maxBv2 savedPhaseMargin savedDCGain

** Export power usage of opamp w/ best gain
alterparam b1 = $&maxBv1
alterparam b2 = $&maxBv2
reset
run
meas ac maxDraw max i(vsupply)
let maxPower = maxDraw * 1.8
wrdata result_power.txt maxPower

** Run noise analysis on opamp w/ best gain
reset
noise V(vo) v2 dec 100 1k 10G
setplot previous
let integ = integ(onoise_spectrum)
let totalNoise = sqrt(integ[length(integ)-1])
wrdata result_noise.txt totalNoise

.endc
.GLOBAL GND
.GLOBAL VDD
.end
