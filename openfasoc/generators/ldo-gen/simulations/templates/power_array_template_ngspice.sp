* include from .../sky130A/libs.tech/ngspice/sky130.lib.spice
.lib '@model_file' @model_corner
* include the LDO spice netlist
.include 'power_array.spice'


xi1 VREG VDD VSS ldoInst


*Controls
V0 VSS 0 dc 0
*V1 VDD VSS pwl 0 0 2n 0 2.0001n 3.3
V1 VDD VSS 3.3
R1 VREG VSS @OUTPUT_RESISTANCE
C1 VREG VSS 1n


*.options savecurrents
.options rshunt=1e11
.ic v(VREG) = @VALUE_REF_VOLTAGE
*Analysis
.temp 25
.tran 100n 5u uic

.probe I(R1) V(VREG)
.control
run
meas TRAN VREG find V(VREG) AT=5u
meas TRAN id find I(R1) AT=5u
.endc

.GLOBAL VDD
.GLOBAL VSS
.end
