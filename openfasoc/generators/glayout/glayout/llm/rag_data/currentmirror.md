# Current Mirror
## Purpose
A current mirror is a circuit designed to copy a current through one active device by controlling the current in another active device of a circuit, keeping the output current constant regardless of loading.
## theory

## terms defined
reference: reference transistor.
mirror: the transistor which mirrors reference current
ratio: width ratio between mirror and reference, used to tune the relative current between mirror drain and reference drain
## schematic
### described in words
two transistors (either nfet or pfet) one labeled as the reference which accepts an input current at the drain, and one labeled as mirror which has the output current at the drain. The sources of reference and mirror are connected and the gates of reference and mirror are also connected. The drain of the reference is connected to gate of reference.
### Pseudo Netlist
an nmos is has the following subckt definition:
NMOS drain gate source body

the nfet or n-type current mirror has the following subckt definition:
.subckt currentmirror inputcurrent outputcurrent
reference inputcurrent inputcurrent gnd gnd NMOS
mirror outputcurrent inputcurrent gnd gnd NMOS
.endsubckt

## Performance Specifications
There are three main specifications that characterize a current mirror. The first is the transfer ratio (in the case of a current amplifier) or the output current magnitude (in the case of a constant current source CCS). The second is its AC output resistance, which determines how much the output current varies with the voltage applied to the mirror. The third specification is the minimum voltage drop across the output part of the mirror necessary to make it work properly. This minimum voltage is dictated by the need to keep the output transistor of the mirror in active mode. The range of voltages where the mirror works is called the compliance range and the voltage marking the boundary between good and bad behavior is called the compliance voltage. There are also a number of secondary performance issues with mirrors, for example, temperature stability.
