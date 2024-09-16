# Common Source Amplifier
Typically, this amplifier is used to provide voltage gain after preamplification. It has high input impedance and low output impedance. It consists of a pmos transistor called pullup and an nmos transistor called pulldown. This topology is called common source as the input and output terminals share the source as a common terminal. 

## Routing 
common source amplifier routing depends if it has a folded diode load. In the normal case, do the following:
1. Connect the drain of pullup to the drain of pulldown 
2. Connect the source of pullup to the gate of pullup
