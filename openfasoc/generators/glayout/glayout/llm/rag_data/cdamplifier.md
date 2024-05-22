# Common Drain Amplifier

## Purpose

The purpose of a common drain amplifier, aka a source follower, is to provide buffering to the input signal amplitude. It is typically used when impedance matching is required or to drive a low-impedance load, or to avoid loading down the previous stage of a circuit.

It offers high input impedance, low output impedance, and a voltage gain close to unity.

## Terms Defined

Rs: the resistance of the biasing resistor. Can be interchange/replaced with another nmos' equivalent resistance <br />
Buffer: A circuit designed to isolate different stages of a circuit, often with unity gain, to prevent any loading effect. <br />
Unity Gain: A condition where the output signal is the same amplitude as the input signal (gain = 1). <br />
Input Impedance (Z_in): The impedance presented by the amplifier's input, which is typically high for a source follower. <br />
Output Impedance (Z_out): The impedance presented by the amplifier's output, which is typically low for a source follower. <br />
Transductance: Masure of amplification factor. Its measured by the ratio of the output current of the circuit over the output voltage of the circuit.

## Theory

The common drain amplifier works by applying an input signal to the gate of the nmos. The source of the nmos follows the input voltage. Because the drain is connected directly to the supply voltage, the device is in saturation. This allows the voltage gain to be at around unity. The high input impedance means minimal loading on the driving circuit, while the low output impedance allows the source follower to drive heavy loads effectively.

## Schematic

### In Words

A typical source follower schematic includes: an nmos with the drain terminal connected to vdd and an input signal that is applied to the gate terminal. Additionally, there is a resistor (Rs) that connects the source terminal to the ground which sets the DC bias point and stabilizes the source voltage. The output node is at the source voltage of the transistor.

If another nmos is used to replace the resistor, its source is connected to ground, the drain is connected to the source of the first transistor, and the gate is connected to a voltage called Vbias which controls the nmos' resistance.

### Pseudo Netlist

A nmos has the following subckt definition: NMOS drain gate source body

A cd amp has the following subckt definition: .subckt NMOS Rs inputvoltage outputvoltage vdd gnd .endsubckt

## Performance Specifications

For an example source follower, typical performance specifications might include voltage gain, input impedance, output impedance, transconductance, and maximum output swing.

The voltage gain (Av) can be defined as the ratio between output voltage over input voltage. This is equivalent to $(gm*Rs)/(1+gm*Rs)$. Additionally, the input impedance (Zin) is typically very high (infinite in an ideal circuit) because the gate of the nmos draws negligible current. The output impedance (Zout) is low and is determined by $Rs/(1+g_mRs)$

Bandwidth is the frequencies in which the amplifier works. This is generally wide in a cd amplifier since the gain is unity. The maximum output swing is the largest peak to peak voltage the circuit can output without distortion. In a source follower, the swing is vdd minuse the voltage drop over the transistor and resistor.