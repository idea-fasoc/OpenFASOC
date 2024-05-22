# Opamp

## Purpose

An operational amplifier, commonly known as an op amp, is a voltage amplifying device designed to be used with external feedback components, such as resistors and capacitors, between its output and input terminals. These components determine the operation or "amplification function" of the amplifier, which can range from simple amplification to complex filtering, mathematical operations, signal conditioning, and more.

## Terms Defined

Inverting Input (IN-): The input terminal where the signal is inversely amplified. <br />
Non-inverting Input (IN+): The input terminal where the signal is amplified retaining its original phase. <br />
Output Terminal: Where the amplified signal is provided. <br />
Power Supply Ports: Two ports, one for the positive power supply voltage (V+), and one for the negative (V-). <br />
Bias Current: The current that flows into the input terminals due to internal transistor biasing. <br />
Open-Loop Gain: The amplification factor of the operational amplifier without any feedback. <br />
Slew Rate: The maximum rate at which the output voltage can change, often specified in V/µs. <br />
Offset Voltage: A small voltage that must be applied between the input terminals to ensure a zero volt output without any signal.


## Theory

An ideal operational amplifier is a theoretical construct that serves as a standard against which real-world op amp performance is measured. The characteristics of an ideal op amp include:

1. Infinite open-loop gain (A_vo), which means an infinite amplification factor without feedback. <br />
2. Infinite input impedance (Z_in), so that it draws no current from the source. <br />
3. Zero output impedance (Z_out), enabling it to provide unlimited current to the load. <br />
4. Infinite bandwidth with no phase shift and flat frequency response from DC to the highest AC frequencies. <br />
5. Zero offset voltage at the input, ensuring a zero-output voltage when both inputs are at the same voltage. <br />
6. Infinite common-mode rejection ratio (CMRR) and power supply rejection ratio (PSRR), implying no sensitivity to voltages that appear at both inputs or to fluctuations in supply voltage.

These ideal characteristics allow for simplified analysis and design, understanding that real-world op amps will fall short of these ideals.

## Schematic

### In Words

The op amp symbol consists of a triangle pointing to the right with five terminals: two input terminals on the left side, one output terminal on the triangle's right tip, and two power supply terminals (-V and +V) at the top and bottom respectively. The non-inverting input (IN+) is usually shown at the top left of the triangle, and the inverting input (IN-) is depicted below it.

### Pseudo Netlist

An operational amplifier has the following subckt definition: .subckt opamp inverting_input non_inverting_input output v_positive v_negative

## Performance Specifications

Key specifications for op amps include: <br />
Input Impedance: Ideally infinite to ensure no current flows into the inputs. <br />
Output Impedance: Ideally zero, representing a perfect voltage source. <br />
Gain Bandwidth Product (GBP): The product of the op amp’s bandwidth and the gain at which it can operate. <br />
Common-Mode Rejection Ratio (CMRR): The ability of the op amp to reject common-mode signals applied to both inputs. <br />
Total Harmonic Distortion (THD): A measure of the distortion added to the input signal. <br />
Supply Rejection Ratio (PSRR): The ability of an op amp to reject fluctuations in its supply voltage. <br />
Temperature Coefficient: Describes how the op amp parameters change with temperature.

