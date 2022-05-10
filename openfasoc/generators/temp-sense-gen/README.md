# Thermal-sensor generator

We use an all-digital temperature sensor architecture, that relies on a new subthreshold oscillator (achieved using the auxiliary cell “Header Cell“) for realizing synthesizable thermal sensors. We choose frequency as the temperature dependent variable. So, we use a ring oscillators that is based on inverters only and stacked native IO devices for better line sensitivity.


For more documentation check on our [website](https://fasoc.engin.umich.edu/thermal-sensor/).


# Design Temperature sensor Generator

The target for temperature sensor generation is `sky130hd_temp` and located inside `OpenFASOC/openfasoc/generators/temp-sense-gen`, the following parameters are supported:

- --specfile: input specifications where the min/max temperature for the temp sensor are specified
- --outputDir: output folder where the gds/def results will be exported
- --platform: only sky130hd platform is supported for now
- --clean: clean flow folder and start a fresh design flow
- --mode: support verilog/macro/full modes, macro mode runs through APR/DRC/LVS steps to generate macros, full mode completes macro generation + simulations
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

3. Modify the test.json or the targets in Makefile based on the requirements, then run the flow. The **sky130hd_temp** target generates a tempsensor macro, the **sky130hd_temp_full** target runs the full mode and finishes macro generation + simulations.

```
make sky130hd_temp 
```

4. The outputs will be stored in the **outputDir** folder specified in Makefile

Please contact mehdi@umich.edu if you have any questions.


# Spice Simulation Flow

To run the simulation, please edit your local model file in `common/platform_config.json`:

- simTool:  simulation tool, only ngspice is supported for now -- We plan to support Xyce in the future

- simMode: `partial` (recommended to reduce runtime) or `full`, partial simulation only includes headers and cells in low voltage domain to calculate the frequency errors, full simulation includes the internal counter (full simulation is slow using ngspice and is still being tested)

- nominal_voltage: the nominal voltage of the specified technology, it is used to set a supply voltage in the simulation testbench

- model_file: the path to the top model lib file

- model_corner: the corner used in the simulation

- an example of the `common/platform_config.json` looks like:

```
{
  "simTool": "ngspice",
  "simMode": "partial",
  "platforms": {
    "sky130hd": {
      "nominal_voltage": 1.8,
      "model_file": "~/open_pdks/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice",
      "model_corner": "tt"
    }
  }
}
```
