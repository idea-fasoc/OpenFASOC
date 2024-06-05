# Current Mirror
A current mirror is a circuit designed to copy a current
The ratio is the width ratio between mirror and reference, used to tune the relative current between mirror transistor drain and reference transistor drain.
two transistors (either nfet or pfet) one labeled as the reference which accepts an input current at the drain, and one labeled as mirror which has the output current at the drain. The sources of reference and mirror are connected and the gates of reference and mirror are also connected. The drain of the reference is connected to gate of reference.
Pseudo Netlist:
an nmos is has the following subckt definition:
NMOS drain gate source body
the nfet current mirror has the following subckt definition:
.subckt currentmirror inputcurrent outputcurrent
reference inputcurrent inputcurrent gnd gnd NMOS
mirror outputcurrent inputcurrent gnd gnd NMOS
.endsubckt