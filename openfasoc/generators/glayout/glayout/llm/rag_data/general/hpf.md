# High Pass Filter

## Purpose

A high pass filter is an electronic circuit that allows signals with a frequency higher than a certain cutoff frequency to pass through and attenuates frequencies lower than the cutoff frequency. It is used in audio applications to block low-frequency noise, in communication systems to eliminate interference, and in various signal processing tasks that require isolation of the high-frequency content of a signal.

## Terms Defined

Cutoff Frequency (f_c): The frequency at which the output signal power falls to half the power of the input signal (corresponds to -3dB point in magnitude).
Passband: The range of frequencies that the filter allows to pass with little or no attenuation.
Stopband: The range of frequencies that are significantly attenuated by the filter.
Roll-off Rate: The rate at which the filter attenuates frequencies beyond the cutoff frequency, often expressed in dB per octave or dB per decade.
Reactance: The resistance to the change of current by a capacitor, inversely proportional to the frequency.


## Theory

## Schematic

### In Words

In its simplest form, a high pass filter can be constructed with a resistor (R) and a capacitor (C) in series. In a passive RC high pass filter:

The input signal is fed through the capacitor. <br />
The resistor is connected to the capacitor and then grounded. <br />
The output signal is taken across the resistor. 

### Pseudo Netlist

A high pass filter has the following subckt definition: .subckt inputvoltage R C gnd outputvoltage .endsubckt

## Performance Specifications

For a high pass filter, important performance characteristics include:

Cutoff Frequency (f_c): Calculated as $( f_c = \frac{1}{2\pi RC} )$, where R is resistance and C is capacitance.
Bandwidth: The width of the passband, which, for a high pass filter, extends from the cutoff frequency to the highest frequency unattenuated by the filter.
Roll-off Rate: For an ideal RC high pass filter, it is 20 dB/decade or 6 dB/octave, meaning for every tenfold increase in frequency past the cutoff, the response decreases by 20 dB.
Impedance Matching: The filter's input and output impedance characteristics should match the source and load impedance to prevent signal reflections and power loss.

In addition to these passive RC filters, high pass filters can also be active, including amplifying components like transistors or operational amplifiers, which can provide gain and change the dynamics of the cutoff frequency and roll-off. Active high pass filters are especially useful when the signal needs amplification or a more precise filter response is required.