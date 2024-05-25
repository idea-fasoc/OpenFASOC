# Common Drain Amplifier
The purpose of a common drain amplifier, aka a source follower, is to provide buffering to the input signal amplitude.
It offers high input impedance, low output impedance, and a voltage gain close to unity.
A typical source follower schematic includes: an nmos with the drain terminal connected to vdd and an input signal that is applied to the gate terminal. Additionally, there is a resistor (Rs) that connects the source terminal to the ground. The output node is at the source voltage of the transistor.
If another nmos is used to replace the resistor, its source is connected to ground, the drain is connected to the source of the first transistor, and the gate is connected to a voltage called Vbias which controls the nmos' resistance.
