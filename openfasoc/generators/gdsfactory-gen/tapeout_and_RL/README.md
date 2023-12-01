# Installation and Getting Started
These generators require python version >= 3.10  
## Installing Layout Tools
All layout dependencies can be installed with pip (the official python package manager). From here you can generate layouts with [Glayout](https://github.com/idea-fasoc/OpenFASOC/blob/main/openfasoc/generators/gdsfactory-gen/glayout/README.md#glayout).  

```
python3 -m pip install -r requirements.txt
python3 -m pip install gdsfactory==7.7.0
```
**After installing python packages, you can test with:**  
`python3 sky130_nist_tapeout.py gen_opamp --output_gds test1.gds`  
This will create an opamp called "test1.gds"

## Installing Simulation Tools
A full install of these tools has only been verified on Linux platforms
- [Skywater 130nm Open PDK](https://github.com/RTimothyEdwards/open_pdks)
- [Magic](http://opencircuitdesign.com/magic/install.html)
- [ngspice](https://ngspice.sourceforge.io/download.html) 
- **Optional**: [Klayout](https://www.klayout.de/build.html)

**After a full install, you can test with:**  
`python3 sky130_nist_tapeout.py test --output_dir test`  
This will create an opamp, extract, and simulate, then dump all outputs to a new "test" directory

# sky130 NIST Tapeout Macros
The `sky130_nist_tapeout.py` file is a python program using the Glayout API to produce the OPAMPS included in the sky130 NIST nanofabrication tapeout. This file also produces simulation info, statistics, and other useful macro functions for the tapeout.  
`sky130_nist_tapeout.py` has a command line interface. use the `-h` option to see all args for this program. help output is replicated below.

## general help
```
usage: sky130_nist_tapeout.py [-h]
                              {extract_stats,get_training_data,gen_opamp,gen_opamps,test,create_opamp_matrix}
                              ...

sky130 nist tapeout sample, RL generation, and statistics utility.

options:
  -h, --help            show this help message and exit

mode:
  {extract_stats,get_training_data,gen_opamp,gen_opamps,test,create_opamp_matrix}
    extract_stats       Run the extract_stats function.
    get_training_data   Run the get_training_data function.
    gen_opamp           Run the gen_opamp function. optional parameters for transistors
                        are width,length,fingers,mults
    gen_opamps          generates the opamps returned in the small parameters list but
                        only saves GDS and does not add pads. always outputs to
                        ./outputrawopamps
    test                Test mode
    create_opamp_matrix
                        create a matrix of opamps
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
                                        [--half_diffpair_params HALF_DIFFPAIR_PARAMS HALF_DIFFPAIR_PARAMS HALF_DIFFPAIR_PARAMS]
                                        [--diffpair_bias DIFFPAIR_BIAS DIFFPAIR_BIAS DIFFPAIR_BIAS]
                                        [--half_common_source_params HALF_COMMON_SOURCE_PARAMS HALF_COMMON_SOURCE_PARAMS HALF_COMMON_SOURCE_PARAMS HALF_COMMON_SOURCE_PARAMS]
                                        [--half_common_source_bias HALF_COMMON_SOURCE_BIAS HALF_COMMON_SOURCE_BIAS HALF_COMMON_SOURCE_BIAS HALF_COMMON_SOURCE_BIAS]
                                        [--output_stage_params OUTPUT_STAGE_PARAMS OUTPUT_STAGE_PARAMS OUTPUT_STAGE_PARAMS]
                                        [--output_stage_bias OUTPUT_STAGE_BIAS OUTPUT_STAGE_BIAS OUTPUT_STAGE_BIAS]
                                        [--mim_cap_size MIM_CAP_SIZE MIM_CAP_SIZE]
                                        [--mim_cap_rows MIM_CAP_ROWS] [--rmult RMULT]
                                        [--add_pads] [--output_gds OUTPUT_GDS]
                                        [--no_lvt] [--PDK_ROOT PDK_ROOT] [--big_pad]

options:
  -h, --help            show this help message and exit
  --half_diffpair_params HALF_DIFFPAIR_PARAMS HALF_DIFFPAIR_PARAMS HALF_DIFFPAIR_PARAMS
                        half_diffpair_params (default: 6 1 4)
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
  --no_lvt              do not place any low threshold voltage transistors.
  --PDK_ROOT PDK_ROOT   path to the sky130 PDK library
  --big_pad             use 120um pad
```

## get_training_data mode
```
usage: sky130_nist_tapeout.py get_training_data [-h] [-t] [--temp TEMP] [--cload CLOAD]
                                                [--noparasitics] [--nparray NPARRAY]
                                                [--saverawsims] [--get_tset_len]
                                                [--output_second_stage] [--no_lvt]
                                                [--PDK_ROOT PDK_ROOT]

options:
  -h, --help            show this help message and exit
  -t, --test-mode       Set test_mode to True (default: False)
  --temp TEMP           Simulation temperature
  --cload CLOAD         run simulation with load capacitance units=pico Farads
  --noparasitics        specify that parasitics should be removed when simulating
  --nparray NPARRAY     overrides the test parameters and takes the ones you provide
                        (file path to .npy file). MUST HAVE LEN > 1
  --saverawsims         specify that the raw simulation directories should be saved
                        (default saved under save_gds_by_index/...)
  --get_tset_len        print the length of the default parameter set and quit
  --output_second_stage
                        measure relevant sim metrics at the output of the second stage
                        rather than output of third stage
  --no_lvt              do not place any low threshold voltage transistors.
  --PDK_ROOT PDK_ROOT   path to the sky130 PDK library
```

## test mode
```
usage: sky130_nist_tapeout.py test [-h] [--output_dir OUTPUT_DIR] [--temp TEMP]
                                   [--cload CLOAD] [--noparasitics]
                                   [--output_second_stage] [--no_lvt]
                                   [--PDK_ROOT PDK_ROOT]

options:
  -h, --help            show this help message and exit
  --output_dir OUTPUT_DIR
                        Directory for output GDS file
  --temp TEMP           Simulation temperature
  --cload CLOAD         run simulation with load capacitance units=pico Farads
  --noparasitics        specify that parasitics should be removed when simulating
  --output_second_stage
                        measure relevant sim metrics at the output of the second stage
                        rather than output of third stage
  --no_lvt              do not place any low threshold voltage transistors.
  --PDK_ROOT PDK_ROOT   path to the sky130 PDK library
```

## create_opamp_matrix mode
```
usage: sky130_nist_tapeout.py create_opamp_matrix [-h] [-p PARAMS] [-r RESULTS]
                                                  [--indices INDICES [INDICES ...]]
                                                  [--output_dir OUTPUT_DIR] [--no_lvt]
                                                  [--PDK_ROOT PDK_ROOT] [--big_pad]

options:
  -h, --help            show this help message and exit
  -p PARAMS, --params PARAMS
                        File path for params (default: params.npy)
  -r RESULTS, --results RESULTS
                        Optional File path for results
  --indices INDICES [INDICES ...]
                        list of int indices to pick from the opamp param.npy and add to
                        the matrix (default: the entire params list)
  --output_dir OUTPUT_DIR
                        Directory for output files (default: ./opampmatrix)
  --no_lvt              do not place any low threshold voltage transistors.
  --PDK_ROOT PDK_ROOT   path to the sky130 PDK library
  --big_pad             use 120um pad
```