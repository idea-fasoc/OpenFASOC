# Push Pull Amp (Class B Amplifier)

## Purpose

A push-pull amplifier is an amplifier that uses a pair of active devices (transistors or tubes) that alternately amplify the positive and negative halves of an input signal waveform. This configuration is widely used because it improves efficiency by reducing the power wasted in the form of heat when compared to single-ended amplifier designs.

## Terms Defined

Class: The amplifier class, such as Class A, B, AB, or C, indicating the portion of the input signal cycle during which each transistor conducts.
Active Device: The amplifying element, often a transistor, that can control a large current flow with a smaller input signal.
Biasing: The process of setting the initial operating point of an active device.
Crossover Distortion: A form of distortion that occurs in Class B and AB push-pull amplifiers due to the transition between the "push" and "pull" transistors.

## Theory

The push-pull design uses two active devices to amplify different halves of the input waveform. In a Class B amplifier, one device amplifies the positive half-cycle while the other device handles the negative half-cycle. A Class AB design utilizes a small bias to both devices to ensure they are both conducting in the small region around the zero-crossing of the signal, thus reducing crossover distortion associated with Class B.

## Schematic

### In Words

A push-pull amplifier typically consists of two transistors, an NPN (or N-channel MOSFET) and a PNP (or P-channel MOSFET) transistor. The emitters (or sources) of the two transistors are connected together and to the output load. The bases (or gates) receive the input signal through a phase splitter, which creates two signals that are 180 degrees out of phase with each other. The collectors (or drains) of each transistor are connected to the supply voltages.

### Pseudo Netlist

A push pull amp has the following subckt definition: .subckt pushpullamp input output vcc vee
Q1 NPN_collector input common vcc NPN
Q2 PNP_collector input common vee PNP
.endsubckt

## Performance Specifications

For push-pull amplifiers, the performance specifications typically include:

Efficiency: Refers to the percentage of input power that is converted to useful output power as opposed to being dissipated as heat. <br />
Linearity: The ability to amplify all parts of the input signal equally, which determines the fidelity of the amplification. <br />
Power Output: The maximum signal power that the amplifier can deliver to the load. <br />
Gain: The ratio of the output signal amplitude to the input signal amplitude. <br />
Output Impedance: The impedance that the amplifier presents to the load, which affects the power transfer. <br />
Frequency Response: The range of frequencies over which the amplifier operates effectively. <br />
Harmonic Distortion: The generation of overtones that were not present in the input signal, typically more noticeable at higher power levels.

Real-world push-pull amplifiers often incorporate additional components and circuitry for biasing, phase splitting, and feedback to overcome non-idealities such as crossover distortion and to improve performance metrics like linearity and frequency response.

