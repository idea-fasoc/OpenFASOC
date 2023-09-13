* opamp_perf_eval.sp
** OpenFASOC Team, Ryan Wans 2023
.param mc_mm_switch=0

** IMPORTANT:   Temperature setting is added automatically in the reading
**              of this file on line 6 as 25. DO NOT OVERRIDE.
.temp {@@TEMP}

.save all
** Define global parameters for altering
.param bdp = 5u
.param bcs = 5u
.param bo  = 5u

** Define netlist
Vsupply VDD GND 1.8
Vindc net1 GND 0.9
V2 vin net1 AC 0.5
V3 vip net1 AC -0.5
.save i(vindc)
.save i(vsupply)
.save i(v2)
.save i(v3)

* bias currents
Ibiasdp VDD biasdpn  {bdp}
Ibiascs VDD biascsn  {bcs}
Ibiaso  VDD biason   {bo}

** Import SKY130 libs (this should be replaced with a path relative to some env variable)
* the ones with double * will not be used. The one with only 1 * will be used

** example not used
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
XDUT vo VDD vip vin biascsn biason biasdpn GND csoutputnetNC opamp
* parameter sweep
** Run initial analysis
.save all
.options savecurrents
.ac dec 100 1k 10G
.control
** Set initial values
set filetype = ascii
let maxFOM = -1
let maxUGB = -1
let maxBics = -1
let maxBidp = -1
let maxBio = -1
let savedPhaseMargin = -1
let savedDCGain = -1
let savedthreedbBW = -1

* dp and cs bias log step
let linear_step_until = 60u
let linear_step_default = 7u
let bias_dp_Min  = 10u
let bias_dp_Max  = 400u
let bias_dp_logStep = 1.1
let bias_cs_Min  = 10u
let bias_cs_Max  = 300u
let bias_cs_logStep = 1.1

* output bias linear step
let bias_o_Min   = 93.5u
let bias_o_Max   = 94u
let bias_o_Step  = 2u

let bias_dp = bias_dp_Min
let bias_cs = bias_cs_Min
let bias_o  = bias_o_Min

let absolute_counter = 0

** Sweep bias voltages
while bias_cs le bias_cs_Max
    while bias_dp le bias_dp_Max
        while bias_o le bias_o_Max
            reset
            alter ibiascs = $&bias_cs
            alter ibiasdp = $&bias_dp
            alter ibiaso  = $&bias_o
            echo  "-- Run # $&absolute_counter -- "
            echo "CS:   $&bias_cs"
            echo "Diff: $&bias_dp"
            echo "Out:  $&bias_o"
        
            run
            ** Find unity-gain bw point
            meas ac ugb_f when vdb(vo)=0
            ** Measure phase margin
            let phase = (180/PI)*vp(vo)
            meas ac pm find phase when vdb(vo)=0
            ** Measure DC(ish) gain
            meas ac dcg find vdb(vo) at=1k
            ** Measure 3db BW
            let threedbabsgain = dcg - 3
            meas ac threedb when vdb(vo)=threedbabsgain FALL=1
            ** if FOM is better than previous max save results
            let FOM = ugb_f / (bias_cs + bias_dp)
            if ( FOM ge maxFOM )
                let maxFOM = FOM
                let maxUGB = ugb_f
                let maxBics = bias_cs
                let maxBidp = bias_dp
                let maxBio = bias_o
                let savedPhaseMargin = pm % 360
                let savedDCGain = dcg
                let savedthreedbBW = threedb
            end

            let absolute_counter = absolute_counter + 1
            let bias_o = bias_o + bias_o_Step
        end
        ** Reset biasCurrent_o for next value of biasCurrent_dp
        let bias_o = bias_o_Min
        if ( linear_step_until ge bias_dp )
            let bias_dp = bias_dp + linear_step_default
        else
            let bias_dp = bias_dp * bias_dp_logStep
        end
    end
    ** Reset biasCurrent_dp for next value of biasCurrent_cs
    let bias_dp = bias_dp_Min
    if ( linear_step_until ge bias_cs )
        let bias_cs = bias_cs + linear_step_default
    else
        let bias_cs = bias_cs * bias_cs_logStep
    end
end
** Export global maxima
wrdata result_ac.txt maxUGB maxBidp maxBics maxBio savedPhaseMargin savedDCGain savedthreedbBW

** Export power usage of correctly biased opamp
alterparam bcs = $&maxBics
alterparam bdp = $&maxBidp
alterparam bo = $&maxBio
reset

op
let estimated_output_1to1_ref = @Ibiaso[current]*1.8
let ptotal_exact = -i(vsupply)*1.8
let estimated_two_stagepwr = ptotal_exact - estimated_output_1to1_ref
wrdata result_power.txt ptotal_exact estimated_two_stagepwr

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
