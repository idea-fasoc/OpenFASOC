# Push Pull Amp (Class B Amplifier)
A push-pull amplifier is a type of amplifier which is able to 

## Terms Defined

Class: The amplifier class, such as Class A, B, AB, or C, indicating the portion of the input signal cycle during which each transistor conducts.
Active Device: The amplifying element, often a transistor, that can control a large current flow with a smaller input signal.
Biasing: The process of setting the initial operating point of an active device.
Crossover Distortion: A form of distortion that occurs in Class B and AB push-pull amplifiers due to the transition between the "push" and "pull" transistors.

## Schematic

### In Words

A push-pull amplifier typically consists of two transistors, an NPN (or N-channel MOSFET) and a PNP (or P-channel MOSFET) transistor. The emitters (or sources) of the two transistors are connected together and to the output load. The bases (or gates) receive the input signal through a phase splitter, which creates two signals that are 180 degrees out of phase with each other. The collectors (or drains) of each transistor are connected to the supply voltages.

### Pseudo Netlist

A push pull amp has the following subckt definition: .subckt pushpullamp input output vcc vee
Q1 NPN_collector input common vcc NPN
Q2 PNP_collector input common vee PNP
.endsubckt

