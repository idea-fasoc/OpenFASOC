* opamp_perf_eval.sp
** OpenFASOC Team, Ryan Wans 2023

** IMPORTANT:   Temperature setting is added automatically in the reading
**              of this file on line 6 as {@@TEMP}. DO NOT OVERRIDE.
.temp {@@TEMP}

** Define global parameters for altering
.param bdp = 5u
.param bcs = 5u
.param bo = 5u

** Define netlist
Vsupply VDD GND 1.8
.save i(vsupply)
V2 vin net1 AC 0.5
.save i(v2)
V3 vip net1 AC -0.5
.save i(v3)

* bias currents
Ibiasdp biasdpn GND {bdp}
*.save i(vbias2)
Ibiascs biascsn GND {bcs}
*.save i(vbias1)
Ibiaso biason GND {bo}

Vindc net1 GND 1
.save i(vindc)


** Import SKY130 libs (this should be replaced with a path relative to some env variable)
* the ones with double * will not be used. The one with only 1 * will be used

** Ryan
** .lib /home/rw/work/open_pdks/sky130/sky130A/libs.tech/ngspice/sky130.lib.spice tt
**@@stp .include /home/rw/work/open_pdks/sky130/sky130A/libs.ref/sky130_fd_sc_hvl/spice/sky130_fd_sc_hvl.spice

** GCP machine
.lib /usr/bin/miniconda3/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice tt
*@@stp .include /usr/bin/miniconda3/share/pdk/sky130A/libs.ref/sky130_fd_sc_hvl/spice/sky130_fd_sc_hvl.spice


** Import cryo libs (these are stored in the sky130A folder)
*@@cryo .include ./sky130A/cryo_models/nshort.spice
*@@cryo .include ./sky130A/cryo_models/nshortlvth.spice
*@@cryo .include ./sky130A/cryo_models/pmos.spice

** Import opamp subcircuit
.include opamp_pex.spice
XDUT vo VDD vip vin biascsn biason biasdpn GND opamp
* parameter sweep
** Run initial analysis
.save all
.options savecurrents
.ac dec 100 1k 10G
.control
** Set initial values
set filetype = ascii
let maxUGB = -1
let maxBics = -1
let maxBidp = -1
let savedPhaseMargin = -1
let savedDCGain = -1
** Tune these
let biasCurrentMin = 5u
let biasCurrentMax = 100u
let biasCurrentStep = 10u
let biasCurrent_cs = biasCurrentMin
let biasCurrent_dp = biasCurrentMin
let biasCurrent_o = biasCurrentMin
* print loop number so user gets an idea of progress / time remaining
let absolute_counter = 0
** Sweep bias voltages
while biasCurrent_cs le biasCurrentMax
    ** Alter parameters and reset top-level ckt
    alterparam bcs = $&biasCurrent_cs
    reset
    while biasCurrent_dp le biasCurrentMax
        alterparam bdp = $&biasCurrent_dp
        reset
        while biasCurrent_o le biasCurrentMax
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
                let maxBics = biasCurrent_cs
                let maxBidp = biasCurrent_dp
                let savedPhaseMargin = pm % 360
                let savedDCGain = dcg
            end
            * print loop number
            echo "loop number: $&absolute_counter"
            let absolute_counter = absolute_counter + 1
            * increment output bias current
            let biasCurrent_o = biasCurrent_o + biasCurrentStep
        end
        ** Reset biasCurrent_o for next value of biasCurrent_dp
        let biasCurrent_o = biasCurrentMin
        let biasCurrent_dp = biasCurrent_dp + biasCurrentStep
    end
    ** Reset biasCurrent_dp for next value of biasCurrent_cs
    let biasCurrent_dp = biasCurrentMin
    let biasCurrent_cs = biasCurrent_cs + biasCurrentStep
end
** Export global maxima
wrdata result_ac.txt maxUGB maxBics maxBidp savedPhaseMargin savedDCGain

** Export power usage of opamp w/ best gain
alterparam bcs = $&maxBics
alterparam bdp = $&maxBidp
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
