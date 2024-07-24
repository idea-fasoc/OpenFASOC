* diffpair_perf_eval.sp
** OpenFASOC Team, Chetanya Goyal 2024, As a part of GSoC
.temp {@@TEMP}
.param bdp = 5u
.param r1p  = 10k
.param r2p  = 10k
.param vbias = 0.8

* input voltages
Vsup VDD GND 1.8
Vbias net1 GND {Vbias}
Vp plus net1 AC 0.5
Vn minus net1 AC -0.5

* source bias
Ibiasdp source GND {bdp}

* bias resistors 
R1 drain_left VDD {r1p}
R2 drain_right VDD {r2p}

.lib @@PDK_ROOT/sky130A/libs.tech/ngspice/sky130.lib.spice tt

.include @@PEX_PATH
XDUT minus drain_right drain_left source plus @@MODULE_NAME

* .ac dec 10 10 10G
.control

echo "Starting simulation"
set filetype = ascii
let maxBiasDP = -1
let maxVinP = -1
let maxBiasR = -1
let minVinN = 1
let maxFOM = -1 
let maxDiffGain = -1
let minCommonModeGain = 987654321
let maxCMRR = -1 
let maxThreeDB = -1
let minNoiseFig = -1

* init biases
let linear_step_until   = 0u
let linear_step_default = 1.1u
let bias_dp_Min         = 0.1u
let bias_dp_Max         = 5u
let bias_dp_logStep     = 1.8
let bias_r2_Min         = 0.85Meg
let bias_r2_Max         = 10G
let bias_r2_logStep     = 1.3
let bias_voltage_min = 0.7
let bias_voltage_max = 1.3
let bias_voltage_step = 0.15

let bias_dp = bias_dp_Min
let bias_r1 = bias_r1_Min
let bias_r2  = bias_r2_Min
let bias_voltage = bias_voltage_min
* let vinp_Min = 0.1
* let vinp_Max = 1.0
* let vinp_logStep = 1.2
* let vinn_Min = -0.1
* let vinn_Max = -1.0
* let vinn_logStep = 1.2
* let vinstep = 0.1
* let vinp = vinp_Min
* let vinn = vinn_Min

let index = 0
while bias_voltage le bias_voltage_max
    while bias_dp le bias_dp_Max
        while bias_r2 le bias_r2_Max
            
            * this way because matching is necessary
            alter R1 = $&bias_r2
            alter ibiasdp = $&bias_dp
            alter R2  = $&bias_r2
            alter Vbias = $&bias_voltage

            echo "~~~~ Run #$&index ~~~~"
            echo "Bias Current DP: $&bias_dp"
            echo "Bias Resistor R1: $&bias_r2"
            echo "Bias Resistor R2: $&bias_r2"
            echo "Bias Voltage: $&bias_voltage"

            save drain_left drain_right
            ac dec 10 10 1G
            let vo = (v(drain_right) - v(drain_left))
            let vadd = (v(drain_right))
            meas ac diff_gain find vdb(vo) at=10
            * meas ac common_mode_gain find vdb(vadd) at=10
            alter Vn ac=0.5
            meas ac common_mode_gain find vdb(vadd) at=10
            alter Vn ac=-0.5
            let threedbgain = diff_gain - 3
            meas ac threedb when vd(vo) = threedbgain

            * update max values
            let FOM = diff_gain / bias_dp
            if ( FOM ge maxFOM )
                let maxFOM = FOM
                let maxDiffGain = diff_gain
                * let maxCommonModeGain = common_mode_gain
                * let maxCMRR = cmrr
                let maxThreeDB = threedb
                let maxBiasDP = bias_dp
                let maxBiasR = bias_r2
            end
            if ( common_mode_gain le minCommonModeGain )
                if ( common_mode_gain ge 0 )
                    let minCommonModeGain = common_mode_gain
                end
            end
            let index = index + 1
            let bias_r2 = bias_r2 * bias_r2_logStep
        end
        let bias_r2 = bias_r2_Min
        if ( linear_step_until ge bias_dp )
            let bias_dp = bias_dp + linear_step_default 
        else   
            let bias_dp = bias_dp * bias_dp_logStep
        end
    end
    let bias_dp = bias_dp_Min
    let bias_voltage = bias_voltage + bias_voltage_step
end 
let maxCMRR = maxDiffGain / minCommonModeGain
echo "Max Bias DP: $&maxBiasDP"
echo "Max Bias Resistance: $&maxBiasR"
echo "Max FOM: $&maxFOM"
echo "Max Diff Gain: $&maxDiffGain"
echo "Min Common Mode Gain: $&minCommonModeGain"
echo "Max CMRR: $&maxCMRR"
echo "Max 3dB: $&maxThreeDB"
echo "Max Bias R: $&maxBiasR"
wrdata result_ac.txt maxBiasDP maxFOM maxDiffGain minCommonModeGain maxCMRR maxThreeDB maxBiasR

alterparam bdp = $&maxBiasDP
alterparam r1p = $&maxBiasR
alterparam r2p = $&maxBiasR
reset 

op 
let ptotal_exact = i(Vsup) * -1.8
wrdata result_power.txt ptotal_exact
echo "Power usage: $&ptotal_exact"

reset 
noise V(drain_left) Vp dec 100 1k 10G
setplot previous
let integ = integ(onoise_spectrum)
let total_noise = sqrt(integ[length(integ)-1])
wrdata result_noise.txt total_noise
echo "Total Noise: $&total_noise"

.endc
.GLOBAL VDD
.GLOBAL GND
.end