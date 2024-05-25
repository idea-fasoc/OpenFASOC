# Voltage Divider
## Purpose

A voltage divider is a linear circuit that converts a high voltage into a lower one using two series resistors. The primary function of a voltage divider is to produce a voltage that is a fraction of the input voltage, making it useful for creating reference voltages, reducing voltage to safe levels for measurement or for circuit operation, and for biasing of transistors in amplifiers and other devices.

## Terms Defined

R1: The first resistor in the series connection, closest to the voltage source. <br />
R2: The second resistor in the series, connected between R1 and ground. <br />
Vin: Input voltage applied across the series combination of R1 and R2. <br />
Vout: Output voltage taken across R2.

## Theory 
The voltage divider works on the principle of resistive scaling. When a voltage is applied across a series of resistors, the voltage drop across each resistor is proportional to its resistance. The basic formula for a two-resistor voltage divider is derived from Ohm's Law $(V = I * R)$ and Kirchhoff's laws. The output voltage (Vout) across R2 is given by:

$[ V_{out} = V_{in} \times \frac{R2}{R1 + R2} ]$

This relationship shows that the output voltage is a fraction of the input voltage, with the fraction determined by the relative values of R1 and R2.

## Schematic

### Described in Words

In a voltage divider schematic, the input voltage Vin is connected to the first terminal of R1. The second terminal of R1 is connected to the first terminal of R2, and the second terminal of R2 is grounded. Vout is the voltage drop measured across R2, which is a result of the partial pressure provided by the resistors R1 and R2.
### Pseudo Netlist

A pseudo netlist of a voltage divider can be written as: .subckt voltagedivider Vin Vout GND R1 Vin Vout R2 Vout GND .endsubckt

## Performance Specifications

The key specifications for a voltage divider include:

Voltage Output (Vout): Can be calculated with the formula Vout = Vin * (R2 / (R1 + R2)). <br />
Resistor Values (R1 and R2): Chosen based on the desired output voltage and current requirements. They affect the power rating and physical size of the resistors. <br />
Power Dissipation: Determined by the voltage drop and the current through each resistor. Each resistor must have a power rating that can handle the power it dissipates without overheating. <br />
Load Effect: The voltage divider ideally works for no-load or high-impedance load conditions. A connected load can alter the expected Vout if not considered properly. <br />

