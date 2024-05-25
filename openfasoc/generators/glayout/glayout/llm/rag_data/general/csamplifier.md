# Common Source Amplifier

## Purpose
The purpose of a cs amp (common source amplifier) is to apply a small input voltage to a circuit to eventually obtain a large output voltage with respect to a common source that is tied to ground.

## Terms Defined
Rl: the resistance of the load resistor in a cs amplifier. This resistance can be modeled by a transistor. <br />
Biasing: The process in which a circuit's transistor DC voltage and current is set to the operating range.

## Theory

The cs amplifier uses an nmos where the input signal is applied to the gate, the output is taken from the drain and the source is connected to a common reference. In this case the common reference is ground. The transistor is able to amplify the input signal by adjusting the resistance between the drain and source terminals. This adjusts the current through the load at the output which therefore amplifies the voltage.

## Schematic

### In Words

A typical cs amp contains an nmos with these characteristics: its ground is tied to an an input voltage, the source is tied to ground, and the drain is connected to a load resistor (Rl) that is tied to ground. In betweeen Rl and the drain of the nmos is a node for the output voltage. 

In a circuit in which Rl is modeled by another transistor, the gate of the transistor above is tied to a node called Vbias. Its source is connected to vdd and its drain is connected to the other transistor.

### Pseudo Netlist

A nmos has the following subckt definition: NMOS drain gate source body

A cs amp has the following subckt definition: .subckt NMOS Rl inputvoltage outputvoltage vdd gnd .endsubckt

## Performance Specifications
The specifications of a cs amplifier are as follows:
Transductance(gm), Gain(Av), Zin, Zout, Bandwidth, and Cutoff Frequency.

Transductance is a measure of amplification factor. Its measured by the ratio of the output current of the circuit over the output voltage of the circuit.

Gain is the ratio of output voltage over input voltage. It can also be modeled by -gm*Rl (negative transductance multiplied by load resistance)

Zin and Zout are the input impedance and the output impedance respectively. In a cs amplifier, the input impedance is equal to 0 and the output impedance is equal to the Rl (load resistance) of the circuit.

Bandwith is the frequencies in which the amplifier works. Similarly, cutoff frequency is where the gains falls off 3dB from its mid band value.