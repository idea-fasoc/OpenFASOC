* opamp_perf_eval.sp
** OpenFASOC Team 2023

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
** .lib /usr/local/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice tt
** .include /usr/local/share/pdk/sky130A/libs.ref/sky130_fd_sc_hvl/spice/sky130_fd_sc_hvl.spice

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
set appendwrite = 1
let maxUGB = -1
let maxBv1 = -1
let maxBv2 = -1
let savedPhaseMargin = -1
let savedDCGain = -1
** Tune these
let biasVoltageMin = 0.4
let biasVoltageMax = 1.6
let biasVoltageStep = 0.05
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
            let savedPhaseMargin = pm
            let savedDCGain = dcg
        end
        let biasVoltage2 = biasVoltage2 + biasVoltageStep
    end
    ** Reset counter for bv2 loop
    let biasVoltage2 = biasVoltageMin
    let biasVoltage1 = biasVoltage1 + biasVoltageStep
end
** Export global maxima
wrdata output.txt maxUGB maxBv1 maxBv2 savedPhaseMargin savedDCGain
run
display
.endc
.GLOBAL GND
.GLOBAL VDD
.end
