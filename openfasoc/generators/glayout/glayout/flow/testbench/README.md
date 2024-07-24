# NGSpice Testbenches

This directory contains testbenches to evaluate components generated from the glayout flow using NGSpice.

Currently, the following testbenches are available:

- `diffpair_tb.sp`: Testbench for the differential pair
- `opamp_tb.sp` : Testbench for a 2 stage Operational Amplifier
- `currmirror_tb.sp` : Testbench for the current mirror 

To run the testbenches, you need to have NGSpice installed and the python script `process_tb.py` must be run 

It can be run as follows - 

``` 
python3 process_tb.py \
--temperature <temp> \
--mode <stp/cryo/custom> \
--pdkroot <path to pdkroot> \
--testbench <opamp/currmirror/diffpair> \
--pexpath <path to extracted netlist> \
--modulename <Name of the module in the netlist> 
```

The first four arguments are not mandatory. Their default values are as follows - 

- `temperature` : 27
- `mode` : stp
- `pdkroot` : /usr/bin/miniconda3/share/pdk/
- `testbench` : opamp


<bold>Do not modify the `@@___` values in the testbenches, these are automatically filled in by the python script</bold>

The results are written to the directory that the script is run in.