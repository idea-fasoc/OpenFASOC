Stages of a generator
======================

Typically a generator is divided into following stages -
    * generation of final gds, verilog, spice netlist and relevant reports
    * checking for drc/lvs errors using the generated reports
    * running simulations for the available testbenches
    * processing the simulation logfiles
    * building the final result of the generator showcasing metrics

It is expected that these stages are modular and standalone which means that the modules can be imported and executed from other scripts too.
This will not only help in debugging and but also in building a flexible regression setup for the generator.

**Notes**

* Make sure the generator returns a proper exit status when something fails with Yosys, OpenROAD, Klayout, Magic and Netgen
* All the input parameters must be accessible via make target or a specifications file.
* The naming of the generator should be consistent across the generator implementation.
