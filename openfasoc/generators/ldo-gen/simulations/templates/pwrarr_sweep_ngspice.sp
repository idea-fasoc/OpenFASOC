* include from .../sky130A/libs.tech/ngspice/sky130.lib.spice
.lib '@model_file' @model_corner
* include the LDO spice netlist
.include 'power_array.spice'


xi1 VREG VDD VSS ldoInst


*Controls
V0 VSS 0 dc 0
*V1 VDD VSS pwl 0 0 2n 0 2.0001n 3.3
V1 VDD VSS 3.3
V2 VREF VSS @VALUE_REF_VOLTAGE
R1 VREG VSS 1000
C1 VREG VSS 1n


*.options savecurrents
.options rshunt=1e11

*Analysis
.dc R1 10 50k 10

.probe I(R1) V(VREG) v(vref)
.control
run
*set hcopydevtype = svg
*set svg_intopts = ( 2560 1440 30 0 1 2 0 )
*setcs svg_stropts = ( white Arial Arial )
*set color1 = black
*set color2 = red
*hardcopy PowerLoadSweep.svg vreg vs r1#branch VREF vs r1#branch title 'VREG load sweep'
set filetype=binary
write isweep.raw v(VREG) r1#branch v(vref)

.endc

.GLOBAL VDD
.GLOBAL VSS
.end
