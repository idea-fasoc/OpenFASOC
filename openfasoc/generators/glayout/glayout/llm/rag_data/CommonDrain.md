# Common Drain Amplifier
The purpose of a common drain amplifier, aka a source follower, is to provide buffering. It has high input impedance, low output impedance, and a voltage gain close to unity.
A typical source follower consists of two NMOS transistors called inp and degen. The degen transistor connected such that it acts as a resistor and its drain is shorted with the source of the inp transistor. The input is applied to the gate of inp and the output is taken from the source of inp. 

## Routing 
Only route together these ports, nothing else
1. Connect the source of inp to the drain of degen. 
2. Connect the drain of the degen to the gate of degen

