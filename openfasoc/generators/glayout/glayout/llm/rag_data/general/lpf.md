# Low Pass Filter

## Purpose
A low pass filter is a circuit made to allow signalls with a frequency lowed than a specified cutoff frequency to pass through while cutting off frequencies that are higher.

## Terms Defined
Cuttoff Frequency ($f_c$): The frequency in which the low pass filter will begin to filter signals.

Passband: The range of frequencies that are allowed to pass through the filter.

Stopband: The range of frequencies that are not alloed to pass through.

Attenuation Rate: The rate where the signal is reduced past the cutoff frequency. Measured in dB/octave or dB/decade

## Theory
A simple low pass filter can be composed of a single resistor and capacitor (RC). Since the capacitor's impedance decreases when frequency increases, there is greater attenuation at high frequencies. More complex filters can be implemented by uing more stages of RC.

## Schematic

### In Words
A simple low pass filter will contain an input resistor connected in series with the input voltage. The capacitor will be connected in parallel with the output voltage and be tied to ground. And the output voltage is taken across the capacitor.

### Pseudo Netlist

A low pass filter has the following subckt definition: .subckt inputvoltage R C gnd outputvoltage .endsubckt

## Performance Specifications

For a simple low pass filter, typical performance specifications may include cutoff frequency, passband, and phase shift.

The cutoff frequency is the frequency at which the amplitude of the output signal is reduced by -3 dB from the input and is calculated as $1/(2πRC)$. Based off this, the passband ranges from DC to slightly below the cutoff frequency.

A phase shift typically occurs in a lpf. At the cutoff frequency, the filter has a phase shift of -45 degrees. At other frequencyes, the filter can have a phase shift that ranges from 0 at DC to -90 at very high frequencies.


