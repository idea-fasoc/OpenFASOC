Description:
The Opamp is a standard two stage amplifier which is designed for achieveing low noise. 
The amplifier is programmable in the sense that the input referred noise (integrated noise upto 20MHz) can vary from 35uV to 6uV for the power consumption variation of 560uW to 5.2mW.
The gain varies from 80dB to 90dB and the phase margin varies in the range 40deg to 60deg for different bias currents.
The current in the current reference branch is programmable via a bias voltage (0 to 2V)
The opamp stability is ensured for the whole bias range specified.

The required performance parameters can be extracted by editing the ngspice testbench template. The netlist directory has the opamp netlist which is to be executed along with the testbench .spice file.
The model library path is specified in the test bench .spice file which can be modified according to the local path where the ngspice simulations are invoked.
