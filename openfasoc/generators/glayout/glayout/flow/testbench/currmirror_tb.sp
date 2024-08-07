* currmirr_perf_eval.sp
** OpenFASOC Team, Chetanya Goyal 2024, As a part of GSoC
.temp 25

.param bref = 5u
.param rbias = 10k
.param cbias = 1p
* input voltages
Vsup VDD GND 1.8

* measure current through ref_drain and mirr_drain
V1 ref_drain GND DC 0
V2 mirr_drain GND DC 0

* source bias
Iref VDD ref_drain {bref}

* bias resistors 
R1 ref_drain VDD {rbias}

.lib /usr/bin/miniconda3/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice tt
.include @@PEX_PATH
XDUT mirr_drain ref_drain GND @@MODULE_NAME
* .ac dec 10 10 10G
.control

echo "Starting simulation"
set filetype = ascii
let maxBiasRef = -1
let minCurrDiff = 987654321
let maxBiasR = -1 

* init biases
let linear_step_until      = 0u
let linear_step_default    = 1.1u
let bias_ref_Min           = 0.5u
let bias_ref_Max           = 50u
let bias_ref_logStep       = 1.1
let bias_rbias_Min         = 1k
let bias_rbias_Max         = 1Meg
let bias_rbias_logStep     = 1.1

let bias_ref    = bias_ref_Min
let bias_rbias  = bias_rbias_Min

let index = 0

while bias_ref le bias_ref_Max
    while bias_rbias le bias_rbias_Max
        
        * this way because matching is necessary
        * place 
        alter R1 = $&bias_rbias
        alter iref = $&bias_ref

        echo "~~~~ Run #$&index ~~~~"
        echo "Bias Current: $&bias_ref"
        echo "Bias Resistor: $&bias_rbias"

        op          
        save mirr_drain ref_drain
        let mirr_curr = bias_ref
        let ref_curr = (1.8 - v(ref_drain))/bias_rbias 
        let currdiff = (( abs( abs(mirr_curr) - abs(ref_curr) ) ) / abs(mirr_curr)) * 100

        echo "mirr_curr = $&mirr_curr"
        echo "ref_curr = $&ref_curr"
        echo "currdiff = $&currdiff %"

        * update max values
        if ( currdiff le minCurrDiff )
            let minCurrDiff = currdiff
            let maxBiasRef = bias_ref
            let maxBiasR = bias_rbias
        end
        let index = index + 1
        let bias_rbias = bias_rbias * bias_rbias_logStep
    end
    let bias_rbias = bias_rbias_Min
    if ( linear_step_until ge bias_ref )
        let bias_ref = bias_ref + linear_step_default 
    else   
        let bias_ref = bias_ref * bias_ref_logStep
    end
end
    
echo "Simulation complete"
echo "Best Bias Current: $&maxBiasRef"
echo "Min Curr Diff: $&minCurrDiff %"
echo "Best Bias Resistance: $&maxBiasR"

wrdata result_ac.txt maxBiasRef minCurrDiff maxBiasR
alterparam bref = $&maxBiasRef
alterparam rbias = $&maxBiasR
reset 

op 
let ptotal_exact = i(Vsup) * 1.8
wrdata result_power.txt ptotal_exact
echo "Best power usage: $&ptotal_exact"


.endc
.GLOBAL VDD
.GLOBAL GND
.end
