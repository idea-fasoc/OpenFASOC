# Common Source Amplifier 
The common source amplifier, serves as an amplifier with voltage gain and phase inversion.
The main amplifying transistor is in a common-source configuration. Its source is connected to a common reference (often ground), its gate receives the input signal, and the drain is connected to the active load.
There are two MOSFETs. One acts as the amplifying stage and we will call this M1, and the other is the active load which we will call M2. Depending on the type of active load, the port of the active load corresponding to the direction of current is connected to the drain of M1. The source of M1 is connected to a lower voltage level than the supply.
Pseudo Netlist:
an nmos is has the following subckt definition:
NMOS drain gate source body
a pmos is has the following subckt definition:
PMOS drain gate source body

a common source amplifier with a biased pfet transistor has the following subckt definition:
.subckt commonsourceamp vin vbias vdd vss vout
m1 vout vin vss vss NMOS
m2 vout vbias vdd vdd PMOS
.endsubckt
