# Common Drain Stage
## Purpose
The common-drain stage, or source follower, serves as a voltage buffer in electronic circuit designs, providing a high input impedance, low output impedance, and voltage gain without phase inversion.

## Terms Defined
Source follower - The gate of this transistor receives the input signal, the drain is connected to a power supply, and the source provides the output, which follows the input signal but subtracted down by the gate-source voltage drop, thus functioning as a buffer
Current source - In a simple configuration, this transistor operates in saturation and is biased such that it acts as a constant current sink, controlling the current flowing through M1.

## Schematic
## Described in words
There are two MOSFETs. One acts like source follower which we will call M1, and the input is the gate of this transistor. The source of this transistor is connected to the drain of the second transistor and also serves as the output, and the drain is connected to a power supply. The second transistor is a current source, with the source tied to a lower voltage level from the power supply and the gate is biased to control the current sink.
### Pseudo Netlist
an nmos is has the following subckt definition:
NMOS drain gate source body

a common drain stage has the following subckt definition:
.subckt commondrain vin vbias vdd vss vout
m1 vdd vin vout vss NMOS
m2 vout vbias vss vss NMOS
.endsubckt

## Performance Specifications
M2 Biasing - M2 is biased to operate in its saturation region, where it behaves as a current source with a near-constant current, relatively independent of the drain-source voltage.
M1 as Source Follower - In this mode, the input voltage is applied to the gate of M1, and it operates in its saturation region due to the current supplied by M2. Since the gate to source voltage of M1 is relatively constant for a given operating point, the source voltage the output voltage follows the input voltage, hence the name "source follower."
Low Output Impedance -  The output impedance of a source follower is low because the source tracks the gate voltage and the MOSFET acts to minimize any change in the source voltage by allowing more or less current to pass. This property makes the source follower an excellent buffer stage.
Voltage Gain - Ideally, the voltage gain of a source follower is slightly less than unity due to the voltage gate to source drop. This means that the output voltage almost equals the input voltage minus the gate-source voltage of M1.
High Input Impedance - Since the gate of a MOSFETs does not draw DC current, the input impedance of the source follower stage is very high, which is beneficial when interfacing with signal sources with high output impedances to prevent loading effects.