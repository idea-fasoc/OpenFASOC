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


**The placeholders in the testbenches with `@@__` can be filled in manually as well, if the user so choses. Take care of the following if you use the script:** 
1. Temperature must be an integer
  - Temperature less than 0 is automatically treated as a cryo sim if the python script is used
  - Temperature equal to 27 degrees is treated as STP
2. The PDK_ROOT must be a valid and accessible path
3. The pex script path (can be a post or pre-pex netlist) must exist
4. The module name must be the exact same as in the netlist
  - Pin orders:
    - Differential Pair  
      `XDUT minus drain_right drain_left source plus @@MODULE_NAME`
    - Current Mirror  
      `XDUT mirr_drain ref_drain GND @@MODULE_NAME`
    - Opamp  
      `XDUT GND csoutputnetNC vo VDD vip vin biascsn biason biasdpn @@MODULE_NAME`
      - `csoutputnetNC` is the 2nd stage Amplifier's output
      - `vo` is the output from the NMOS driver circuit
      - the current bias components are connected to the mirror drains of the corresponding current mirrors

***The results are written to the directory that the script is run in.***
