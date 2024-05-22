# Transimpedance Amplifier (TIA)

## Purpose

A Transimpedance Amplifier (TIA) is an amplifier that converts an input current to a proportional output voltage. The primary role of a TIA is in applications where current signals need to be detected or measured, and amplified into a more usable voltage level. Commonly, TIAs are used with photodiodes, photomultiplier tubes, or other sensors that produce a current proportional to the intensity of light they receive.

## Terms Defined

Photodiode: A semiconductor device that generates a current when exposed to light. <br />
Feedback Resistor $(R_f)$: The resistor in the feedback loop of the TIA that sets the gain of the amplifier. <br />
Transimpedance Gain: The ratio of the output voltage to the input current, given in ohms, which is numerically equal to the value of the feedback resistor (R_f).

## Theory

The TIA uses a feedback resistor to set the gain of the amplifier and convert a small input current (I_in) from a sensor or photodiode to a larger output voltage (V_out). Ohm’s law describes the relationship between the input current and the output voltage of a TIA: $V_out = I_in * R_f$. Because the input is current and the output is voltage, the transimpedance gain has units of resistance, which is what gives the TIA its name. In an ideal TIA, the input impedance is close to zero, which ensures that the current flows through the amplifier, and the output impedance is low.

## Schematic

### Described in Words

In the schematic of a TIA, an op-amp is configured with the photodiode connected between its inverting input and the ground, effectively reverse-biasing the photodiode when the op-amp output swings positive. The non-inverting input is connected to a reference voltage, often ground. A feedback resistor is connected between the op-amp's output and its inverting input.

### Pseudo Netlist

An operational amplifier has the following subckt definition: .subckt opamp inverting_input non_inverting_input output v_positive v_negative

A pseudo netlist of a tia can be written as:
.subckt tia pd_in v_out v_ref XU1 op_out pd_in v_ref opamp Rf op_out pd_in .endsubckt

In this netlist, XU1 represents the operational amplifier, pd_in is the input from the photodiode, v_out is the output voltage of the TIA, and v_ref is the reference voltage for the non-inverting input. Rf is the feedback resistor which sets the gain of the TIA.

## Performance Specifications

Important specifications for a TIA include:

Bandwidth: The range of frequencies over which the TIA will have a consistent gain. This is often affected by the feedback resistor and any parasitic capacitance at the input.<br />
Noise Performance: Critical for the sensitivity of the TIA as it amplifies the signal from the photodiode. Includes contributions from the feedback resistor, the op-amp, and the diode itself. <br />
Dynamic Range: The range of input currents over which the TIA can provide a linear output voltage response. <br />
Stability: Factors such as the capacitance of the photodiode and the value of Rf can affect the stability and may lead to oscillations if not properly compensated.

