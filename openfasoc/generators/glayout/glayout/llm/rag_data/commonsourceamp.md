# Common Source Amplifier 
## Purpose
The common source amplifier, serves as an amplifier with voltage gain and phase inversion.

## Terms Defined
Amplifying Stage: The main amplifying transistor is in a common-source configuration. Its source is connected to a common reference (often ground), its gate receives the input signal, and the drain is connected to the active load.
Active Load - A second MOSFET, sometimes in a diode-connected configuration or part of a more complex current mirror, serves as the active load. This transistor is biased to operate as a constant current sink, creating a high output impedance at the drain of M1.

## Schematic
## Described in words
There are two MOSFETs. One acts as the amplifying stage and we will call this M1, and the other is the active load which we will call M2. Depending on the type of active load, the port of the active load corresponding to the direction of current is connected to the drain of M1. The source of M1 is connected to a lower voltage level than the supply.
### Pseudo Netlist
an nmos is has the following subckt definition:
NMOS drain gate source body
a pmos is has the following subckt definition:
PMOS drain gate source body

a common source amplifier with a biased pfet transistor has the following subckt definition:
.subckt commonsourceamp vin vbias vdd vss vout
m1 vout vin vss vss NMOS
m2 vout vbias vdd vdd PMOS
.endsubckt

## Performance Specifications
Biasing - Both MOSFETs are biased in the saturation region. For M1, the gate-source voltage (VGS) is set above the threshold voltage (Vth) to ensure it remains in the saturation region across the input signal range. M2, configured as a current source, is also biased to ensure it stays in saturation.

Input Signal - The input AC signal is superposed on the DC bias at the gate of M1. This causes variations in the gate-source voltage, modulating the drain current based on the transconductance (gm) of M1.

Output Signal - The modulated drain current of M1 flows through the active load. Since the active load's output impedance is very high, usually much higher than a passive load resistor, the voltage swing at the drain of M1 is increased. The output signal is taken at this point.
