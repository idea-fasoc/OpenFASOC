Developer's Guide
===============================

* First setup the environment by installing all dependencies using the Dependencies.sh script present in the home of OpenFASOC github repository. To test whether the installation happened correctly or not, try running the temp-sense-gen.

* Once the setup is ready, read the "Things to improve" under this section (right below) and start working on them.

* You can also start working on improving the code base, docs, CI flow, improving the generators or creating your own generator.


Things to improve
********************

To improve our generators, flow, and the QoR, efforts are directed towards the following items under different categories -

* Infrastructure:
    * Add more regression tests to the CI.
    * Checks at each step (Verilog generation, Synthesis, APAR, DRC and LVS) inside each generator.
    * Simulation after synthesis.

* Circuit level
    * Multi-config enablement for each generator.
    * Circuit-level optimization

* General
    * Enable the stable spice simulation flow and modeling (ngspice and Xyce)
    * Add sky130_fd_sc_hs support
