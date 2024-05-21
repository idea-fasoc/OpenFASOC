# Voltage Follower

## Purpose

A voltage follower, also known as a buffer amplifier, is a circuit configuration where the output voltage directly follows the input voltage. This means the output voltage is the same as the input voltage. The primary purpose of a voltage follower is to increase the input impedance (ideally to infinity) and decrease the output impedance (ideally to zero), thus providing no voltage gain but significant current gain. This allows the voltage follower to serve as a buffer, isolating the source from the load while preventing signal attenuation that would occur if the load were directly connected to the source.

## Terms Defined

Anode: The terminal through which conventional current flows into the diode, typically marked with a plus sign.
Cathode: The terminal through which conventional current flows out of the diode, often denoted with a line or band on the diode body.
Forward Bias: A condition where the anode is more positive relative to the cathode, allowing current flow.
Reverse Bias: A condition where the cathode is more positive in relation to the anode, restricting current flow.
Forward Voltage Drop (Vf): The potential difference across the diode terminals when current is conducted in the forward direction, typically 0.7V for silicon diodes and 0.3V for germanium diodes.
Reverse Breakdown Voltage (V_br): The voltage at which the diode will conduct a significant reverse current, potentially leading to device damage if sustained.

## Theory

The voltage follower is realized using an operational amplifier (op-amp) with 100% negative feedback provided by a direct connection from the output terminal back to the inverting input. There is no external feedback network of resistors or capacitors, simplifying the configuration.

## Schematic

### In Words

In the schematic for a voltage follower:

The positive (+) terminal of the op-amp is the non-inverting input.
The negative (−) terminal of the op-amp, the inverting input, is connected directly to the output terminal of the op-amp.
The input voltage is applied to the non-inverting input (+).
The output is taken from the output terminal of the op-amp.


### Pseudo Netlist

An operational amplifier has the following subckt definition: .subckt opamp inverting_input non_inverting_input output v_positive v_negative

A voltage follower has the following subckt definition: .subckt voltagefollower in out opamp_model X1 in out out opamp_model .endsubckt

X1 represents the operational amplifier with the in net connected to the non-inverting input, the out net connected to both the inverting input and the output, with opamp_model defining the operational amplifier’s characteristics.

## Performance Specifications

Key specifications for a voltage follower include:

Input Impedance (Z_in): Ideally infinite, which means no current is drawn from the input source. <br />
Output Impedance (Z_out): Ideally zero, which allows the circuit to drive heavy loads without significant voltage drop. <br />
Voltage Gain (A_v): Unity (1), meaning the output voltage equals the input voltage without amplification. <br />
Bandwidth: Broad, often limited only by the op-amp’s characteristics since no reactive components are introduced. <br />
Slew Rate: This defines the maximum rate at which the output can change and can be a limiting factor in high-frequency applications.

Voltage followers are widely used in circuits where signal isolation is needed without altering the signal voltage, such as interfacing between high and low impedance circuit blocks or driving capacitive loads without stability issues.