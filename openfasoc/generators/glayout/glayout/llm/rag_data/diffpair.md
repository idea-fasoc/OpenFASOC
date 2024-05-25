# Differential Pair
A differential pair has two inputs and two outputs. The purpose of a differential pair is to amplify voltage differences between these two inputs. When one input is much higher than the other, one output goes to high voltage and the other goes to near zero voltage. When the other input is much higher, the opposite happens.
There are two MOSFETs, with the sources shorted and connected to a current source. The outputs are the drains of the MOSFETs.
### Pseudo Netlist
an nmos is has the following subckt definition:
NMOS drain gate source body

the nfet or n-type differential pair has the following subckt definition:
.subckt diffpair in1 in2 out1 out2 ibias
m1 out1 in1 ibias gnd NMOS
m2 out2 in2 ibias gnd NMOS
.endsubckt
