# Class A Amplifier

## Purpose

The purpose of a Class A amplifier is to provide linear amplification of an input signal. This results in low distortion of the amplified signal. 

## Terms Defined
Biasing: Is where you set the operating point for your devices so they remain in the active region
Linearity: The proportion between the input and output signals where the output is a linear function of the input
Efficiency: The ratio of the power at the load over the total power consumed by the amplifier.
vgg: biasing voltage that is applied to m2, allows the transistor to act as a biasing resistor.

## Theory

Class A amplifiers typically has current flow in the mosfets during the entire period of a sinusiodal signal. It biases the transistor so any input signal causes the current flowing through to vary over the waveform. As a result, current is flowing through the output resulting in unsymmetrical sinking, poor efficiency, and a linear waveform.

## Schematic

### In Words

A class a amplifier can be modeled with two nmos or two pmos transistors, m1 and m2 respectivly. The gate of m1 is connected to input voltage and the drain is connected the the drain of m2. The source of m1 is tied to vss and the source of m2 is connected to vdd. The gate of m2 is connected to vgg. The node between the drains of m1 and m2 are connected to vout which can be connect to a capacitor and resistor in parallel to block unwanted signals from reaching the load.

### Pseudo Netlist

A nmos has the following subckt definition: NMOS drain gate source body

A class a amplifier has the following subckt definition: .subckt NMOS NMOS inputvoltage outputvoltage vss vgg vdd gnd Rl Cl .endsubckt

## Performance Specifications

For a class a amplifier, performance specifications may include efficiency, signal to noise ratio (SNR), linearity, and maximum output swing.

Efficiency can be found by taking the output voltage at the peak over vdd-vss and squaring the result. For a class a amplifier, the circuit is very inefficient (usually between 20-30%) because the device is constantly active for an entire input signal cycle.

The SNR of a class a amp is usually high since there is low distortion. Meanwhile, the class a amplifier is usually bery linear if its designed properly and in the linear operatin range.

We typically get a high max output swing in terms of the supply voltage, the max output swing is the largest peak to peak voltage the circuit can output without distortion.
