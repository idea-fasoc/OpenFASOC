# Differential Pair
## Purpose
The gates of the MOSFETs that make up the differential pair act as inputs. If there is a difference in the voltage at the gates of the NMOS' then the transistor with the higher gate voltage will conduct more current leading to a difference in the currents at the drains of the transistors.

## Terms Defined
Differential Mode - When a differential voltage is applied to the gates of M1 and M2, the MOSFET with the higher gate-source voltage will enter deeper into the saturation region, conducting more current. Consequently, the other MOSFET will conduct less current. This results in an imbalance in drain currents, creating a voltage differential at the output proportional to the input signal difference.

Common-Mode Operation - If an identical voltage, referred to as the common-mode voltage, is applied to both gate terminals, ideally, there is no change in the drain current balance since no differential signal is present. MOSFETs in a well-matched differential pair will each conduct half the total current of the current source at the source of the NMOS', assuming they are operating above the threshold voltage and in saturation.

## Schematic
## Described in words
There are two MOSFETs, with the sources shorted and connected to a current source. The outputs are the drains of the MOSFETs.
### Pseudo Netlist
an nmos is has the following subckt definition:
NMOS drain gate source body

the nfet or n-type differential pair has the following subckt definition:
.subckt diffpair in1 in2 out1 out2 ibias
m1 out1 in1 ibias gnd NMOS
m2 out2 in2 ibias gnd NMOS
.endsubckt

## Performance Specifications
Transconductance (g_m): For MOSFETs, transconductance is the ratio of the change in the drain current (ΔI_D) to the change in the gate-source voltage (ΔV_GS) when the drain-source voltage (V_DS) is constant. g_m quantifies the MOSFET's ability to convert a voltage input (at the gate) into a current output (at the drain). It is essential in determining the differential gain of the pair.

Differential Gain (A_diff): The differential gain is a function of the transconductance of the MOSFETs and the total load resistance (R_D) seen by each transistor's drain. In a MOSFET differential pair, A_diff is typically given as A_diff = g_m * R_D.

Common-Mode Gain (A_cm): In a practical MOSFET differential pair, the gain for common-mode signals is not perfectly zero due to device mismatches and non-idealities. The goal is to minimize A_cm through careful circuit design and component matching.

Common-Mode Rejection Ratio (CMRR): The CMRR measures how well the differential pair rejects common-mode signals and amplifies differential signals. It is given as CMRR = A_diff / A_cm, and like in BJTs, it is an important metric that is ideally large.

Input Range: The voltage range over which the differential pair operates linearly is limited by the need to keep both MOSFETs in saturation and the matching of the pairs. Large differential input signals may push one of the MOSFETs into the triode region or cutoff, leading to nonlinear operation.
