# sky130 NIST Tapeout Macros
This directory contains the `sky130_nist_tapeout.py` file which is a python program containing all functions and utils neccessary to produce the circuits, simulation info, and statistics used in the sky130 NIST tapeout.  
`sky130_nist_tapeout.py` has a command line interface. use the `-h` option to see all args for this program. help output is replicated below

## general help
```
usage: sky130_nist_tapeout.py [-h] {extract_stats,get_training_data,gen_opamp,test} ...

sky130 nist tapeout sample, RL generation, and statistics utility.

options:
  -h, --help            show this help message and exit

mode:
  {extract_stats,get_training_data,gen_opamp,test}
    extract_stats       Run the extract_stats function.
    get_training_data   Run the get_training_data function.
    gen_opamp           Run the gen_opamp function. optional parameters for transistors
                        are width,length,fingers,mults
    test                Test mode
```

## extract_stats mode
```
usage: sky130_nist_tapeout.py extract_stats [-h] [-p PARAMS] [-r RESULTS]

options:
  -h, --help            show this help message and exit
  -p PARAMS, --params PARAMS
                        File path for params (default: training_params.npy)
  -r RESULTS, --results RESULTS
                        File path for results (default: training_results.npy)
```

## gen_opamp mode
```
usage: sky130_nist_tapeout.py gen_opamp [-h]
                                        [--diffpair_params DIFFPAIR_PARAMS DIFFPAIR_PARAMS DIFFPAIR_PARAMS]
                                        [--diffpair_bias DIFFPAIR_BIAS DIFFPAIR_BIAS DIFFPAIR_BIAS]
                                        [--half_common_source_params HALF_COMMON_SOURCE_PARAMS HALF_COMMON_SOURCE_PARAMS HALF_COMMON_SOURCE_PARAMS HALF_COMMON_SOURCE_PARAMS]
                                        [--half_common_source_bias HALF_COMMON_SOURCE_BIAS HALF_COMMON_SOURCE_BIAS HALF_COMMON_SOURCE_BIAS HALF_COMMON_SOURCE_BIAS]
                                        [--output_stage_params OUTPUT_STAGE_PARAMS OUTPUT_STAGE_PARAMS OUTPUT_STAGE_PARAMS]
                                        [--output_stage_bias OUTPUT_STAGE_BIAS OUTPUT_STAGE_BIAS OUTPUT_STAGE_BIAS]
                                        [--mim_cap_size MIM_CAP_SIZE MIM_CAP_SIZE]
                                        [--mim_cap_rows MIM_CAP_ROWS] [--rmult RMULT]
                                        [--add_pads] [--output_gds OUTPUT_GDS]

options:
  -h, --help            show this help message and exit
  --diffpair_params DIFFPAIR_PARAMS DIFFPAIR_PARAMS DIFFPAIR_PARAMS
                        diffpair_params (default: 6 1 4)
  --diffpair_bias DIFFPAIR_BIAS DIFFPAIR_BIAS DIFFPAIR_BIAS
                        diffpair_bias (default: 6 2 4)
  --half_common_source_params HALF_COMMON_SOURCE_PARAMS HALF_COMMON_SOURCE_PARAMS HALF_COMMON_SOURCE_PARAMS HALF_COMMON_SOURCE_PARAMS
                        half_common_source_params (default: 7 1 10 3)
  --half_common_source_bias HALF_COMMON_SOURCE_BIAS HALF_COMMON_SOURCE_BIAS HALF_COMMON_SOURCE_BIAS HALF_COMMON_SOURCE_BIAS
                        half_common_source_bias (default: 6 2 8 3)
  --output_stage_params OUTPUT_STAGE_PARAMS OUTPUT_STAGE_PARAMS OUTPUT_STAGE_PARAMS
                        pamp_hparams (default: 5 1 16)
  --output_stage_bias OUTPUT_STAGE_BIAS OUTPUT_STAGE_BIAS OUTPUT_STAGE_BIAS
                        pamp_hparams (default: 6 2 4)
  --mim_cap_size MIM_CAP_SIZE MIM_CAP_SIZE
                        mim_cap_size (default: 12 12)
  --mim_cap_rows MIM_CAP_ROWS
                        mim_cap_rows (default: 3)
  --rmult RMULT         rmult (default: 2)
  --add_pads            add pads (gen_opamp mode only)
  --output_gds OUTPUT_GDS
                        Filename for outputing opamp (gen_opamp mode only)
```

## get_training_data mode
```
usage: sky130_nist_tapeout.py get_training_data [-h] [-t] [--temp TEMP] [--cload CLOAD]
                                                [--noparasitics] [--nparray NPARRAY]
                                                [--saverawsims]

options:
  -h, --help         show this help message and exit
  -t, --test-mode    Set test_mode to True (default: False)
  --temp TEMP        Simulation temperature
  --cload CLOAD      run simulation with load capacitance units=pico Farads
  --noparasitics     specify that parasitics should be removed when simulating
  --nparray NPARRAY  overrides the test parameters and takes the ones you provide (file
                     path to .npy file)
  --saverawsims      specify that the raw simulation directories should be saved
                     (default saved under save_gds_by_index/...)
```

## test mode
```
usage: sky130_nist_tapeout.py test [-h] [--output_dir OUTPUT_DIR] [--temp TEMP]
                                   [--cload CLOAD] [--noparasitics]

options:
  -h, --help            show this help message and exit
  --output_dir OUTPUT_DIR
                        Directory for output GDS file
  --temp TEMP           Simulation temperature
  --cload CLOAD         run simulation with load capacitance units=pico Farads
  --noparasitics        specify that parasitics should be removed when simulating
```