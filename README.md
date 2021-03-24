# FASoC: Fully Open-Sourced Autonomous SoC Synthesis using Customizable Cell-Based Synthesizable Analog Circuits

The FASoC Program is focused on developing a complete system-on-chip (SoC) synthesis tool from user specification to GDSII with fully open-sourced tools.

See more on our [website](https://fasoc.engin.umich.edu/).

# Prerequisites

Magic <https://github.com/RTimothyEdwards/magic>
Netegn <https://github.com/RTimothyEdwards/netgen>
OpenROAD <https://github.com/The-OpenROAD-Project/OpenROAD> (with `export_opendb_power_pins` enabled )

   - Before building the OpenROAD tools, please enable the `export_opendb_power_pins` function from OpenROAD: uncomment the `export_opendb_power_pins` in proc opendb_update_grid {} in `OpenROAD-flow-scripts/tools/OpenROAD/src/pdngen/src/PdnGen.tcl` and then rebuild the OpenROAD tool

# Run

The generators are located inside `open_fasoc/generators/temp-sense-gen/`, the target of temperature sensor generation is `sky130hd_temp`, these parameters are supported:

- --specfile: input specifications where the min/max temperature for the temp sensor are specified
- --output: output folder where the gds/def results will be exported
- --platform: only sky130hd platform is supported for now
- --clean: clean flow folder and start a fresh design flow
- --mode: support 'verilog' and 'macro' modes for now
- --nhead: specify a fixed number of headers (optional)
- --ninv: specify a fixed number of inverters (optional)

Please contact mehdi@umich.edu if you have enay questions.


