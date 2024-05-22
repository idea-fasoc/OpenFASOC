# Transmission Gate

## Purpose

A transmission gate is a bidirectional analog switch that uses a pair of complementary transistors to pass or block signals. It operates as an effective switch in digital and analog circuits, allowing the isolation or connection of circuit nodes depending on the control signal. Transmission gates are fundamental components in CMOS digital logic, often used in multiplexers, switches, and data buses.

## Terms Defined

Pass Gate: Alternative name for a transmission gate. <br />
CMOS: Complementary Metal-Oxide-Semiconductor, a technology for constructing integrated circuits using a pair of p-type and n-type MOSFETs. <br />
nMOS (n-channel MOSFET): A type of MOSFET that conducts when a positive voltage is applied to the gate relative to the source. <br />
pMOS (p-channel MOSFET): A type of MOSFET that conducts when a negative voltage is applied to the gate relative to the source. <br />
Control Voltage (V_control): The voltage applied to the gates of the MOSFETs to open or close the transmission gate.

## Theory

In a transmission gate, the complementary MOSFETs are used to create a switch that can pass both high and low logic levels effectively. This is because nMOS transistors pass strong '0's (low voltages) and weak '1's (high voltages) while pMOS transistors pass strong '1's and weak '0's. By pairing an nMOS with a pMOS, the transmission gate can pass both logic levels with low resistance.

## Schematic

### In Words

The transmission gate consists of an nMOS and a pMOS transistor connected in parallel, with their drains and sources tied together, respectively. The gate of the nMOS transistor connects to the control voltage, while the gate of the pMOS transistor connects to the inverse of the control voltage. This arrangement ensures that both transistors are either on or off simultaneously.

### Pseudo Netlist

A transmission gate has the following subckt definition: .subckt transmissiongate input output control gnd vdd
Mn1 output input gnd gnd nMOS
Mp1 output input vdd vdd pMOS
.endsubckt

Here, Mn1 represents the nMOS transistor with terminals connected to output, input, gnd (source), and gnd (body), while Mp1 represents the pMOS transistor with terminals connected to output, input, vdd (source), and vdd (body). control ties to the gate of the nMOS, and the inverted control ties to the gate of the pMOS.

## Performance Specifications

Important performance characteristics for transmission gates include:

On Resistance (R_on): The resistance of the TG when it is in the conducting state, ideally as low as possible to reduce voltage drop and power dissipation. <br />
Off State Leakage: The current that flows through the TG when it is supposed to be off. It should be minimized to prevent unintended signal pass-through. 
Switching Speed: The time it takes for the TG to transition from on to off (and vice versa), which influences the maximum operating frequency. <br />
Charge Injection: The amount of charge shared between the gate and the channel during switching, which can cause glitches in the output. <br />
Signal Integrity: The ability of the TG to pass the signal without distortion, which is influenced by factors such as channel length modulation and body effect.

