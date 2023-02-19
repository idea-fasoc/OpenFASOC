* include from .../sky130A/libs.tech/ngspice/sky130.lib.spice
.lib '@model_file' @model_corner
* include the LDO spice netlist
.include 'power_array.spice'


xi1 VREG VDD VSS ldoInst


*Controls
V0 VSS 0 dc 0
*V1 VDD VSS pwl 0 0 2n 0 2.0001n 3.3
V1 VDD VSS dc 3.3
V2 VREF VSS @VALUE_REF_VOLTAGE
R1 VREG VSS 1000
C1 VREG VSS 1n

.options LINSOL type=klu
*Analysis
.dc R1 10 50k 10

.print tran format=raw file=isweep.raw v(VREG) v(VREF) i(R1)

.GLOBAL VDD
.GLOBAL VSS
.end
