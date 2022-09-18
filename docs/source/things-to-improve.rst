Things to improve
=================

To improve our generators, flow, and the QoR, efforts are directed towards the following items under different categories:

* Infrastructure:
    * Add more regression tests to the CI
    * Checks at each step (Verilog generation, Synthesis, APAR, DRC and LVS) inside each generator
    * Add dashboard to vizualize data (pre-PEX, PEX, Silicon)

* Circuit level
    * Multi-config enablement for each generator
    * Circuit-level optimization
    * Add other variants of the aux cells

* Documentation
    * Create example notebooks for all generators
    * Document the OpenFASoC flow for all generators

* General
    * Enable stable spice simulation flow and modeling (ngspice and Xyce)
    * Add modeling file for the Temp. Sensors based on silicon data
    * Add sky130_fd_sc_hs support
    * Simulation after synthesis
    * Add Special Router in OpenROAD
    * PCells in gdsfactory

Last updated: |today|
