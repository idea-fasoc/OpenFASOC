# OpenFASoC: Fully Open-Source Autonomous SoC Synthesis using Customizable Cell-Based Synthesizable Analog Circuits

The FASoC Program is focused on developing a complete system-on-chip (SoC) synthesis tool from user specification to GDSII with fully open-sourced tools.

See more on our [website](https://fasoc.engin.umich.edu/).

# Prerequisites

Please build the following tools:

  Magic <https://github.com/RTimothyEdwards/magic>

  Netgen <https://github.com/RTimothyEdwards/netgen>
  
  Klayout <https://github.com/KLayout/klayout>
  
  Yosys <https://github.com/The-OpenROAD-Project/yosys>

  OpenROAD <https://github.com/The-OpenROAD-Project/OpenROAD> (commid id: 8ed8414, with power pins generation enabled)

   - Before building the OpenROAD tools, please enable the `export_opendb_power_pins` function from OpenROAD: uncomment the `export_opendb_power_pins` in proc opendb_update_grid {} in `OpenROAD/src/pdngen/src/PdnGen.tcl` and then rebuild the OpenROAD tool.

   - Python3 is needed to run the generator. 

   - All the required tools need to be loaded into the environment before running this generator.

# Design Generation

Our fully open source flow only supports the temperature sensor generation so far. We are working on adding additional generators in the near future.

The generators are located inside `OpenFASOC/generators/`, the target for temperature sensor generation is `sky130hd_temp` and located inside `OpenFASOC/generators/temp-sense-gen`, the following parameters are supported:

- --specfile: input specifications where the min/max temperature for the temp sensor are specified
- --outputDir: output folder where the gds/def results will be exported
- --platform: only sky130hd platform is supported for now
- --clean: clean flow folder and start a fresh design flow
- --mode: support 'verilog' and 'macro' modes for now
- --nhead: specify a fixed number of headers (optional)
- --ninv: specify a fixed number of inverters (optional)

1. Clone the OpenFASOC repository

```
git clone git@github.com:idea-fasoc/OpenFASOC.git
```

2. Go to the temperature sensor generation folder

```
cd OpenFASOC/generators/temp-sense-gen
```

3. Modify the test.json or the **sky130hd_temp** target in Makefile, then run the flow

```
make sky130hd_temp
```

4. The output results will be stored in the **outputDir** folder specified in Makefile

Please contact mehdi@umich.edu if you have any questions.

# Things to improve

To improve our tools, flow, and QoR. The following limitations are currently being addressed:
   - In OpenROAD tools:
       - Add the power pins extraction in OpenROAD tool
       - LEF modification for NDR needs to be within the tool (no additional script)
       - write_cdl bug fix in source code    
       - fence aware placement step needs to be added
       - ioplacment step is now skipped at placement and is set to random palcement by default at floorplaning so it doesn't put power pins of additional voltage domains at the edge
   - add the spice simulation flow and modeling
   - add sky130_fd_sc_hs support
