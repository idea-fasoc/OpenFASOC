# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 21:46:45 2021

@author: Qirui Zhang

Example codes for automating Agilent B2902A
"""

import pyvisa as pvisa
import time

# Connect to B2902A through USB
rm = pvisa.ResourceManager()
B2902A = rm.open_resource('USB0::0x0957::0x8C18::MY51140630::0::INSTR')

# Set Modes to be VOLTS
B2902A.write(':SOURce1:VOLTage:MODE %s' % ('FIXed'))
B2902A.write(':SOURce2:VOLTage:MODE %s' % ('FIXed'))

# Set Voltage Levels
VDD = 3.0 # V
VDD1v8 = 1.8 # V
B2902A.write(':SOURce1:VOLTage:LEVel:IMMediate:AMPLitude %G' % (VDD))
B2902A.write(':SOURce2:VOLTage:LEVel:IMMediate:AMPLitude %G' % (VDD1v8))

# Set Current Limits
I_VDD_limit = 0.1 # A
I_VDD1v8_limit = 0.01 #A
B2902A.write(':SENSe1:CURRent:DC:PROTection:LEVel %G' % (I_VDD_limit))
B2902A.write(':SENSe2:CURRent:DC:PROTection:LEVel %G' % (I_VDD1v8_limit))

# Initiate the two channels
time.sleep(1)
#B2902A.write(':INITiate:IMMediate:ALL (%s)' % ('@1,2'))
B2902A.write(':OUTPut1:STATe %d' % (1))
B2902A.write(':OUTPut2:STATe %d' % (1))
time.sleep(3)


# Measurements
I_avg = 0
for i in range(100):
    I_values = B2902A.query_ascii_values(':MEASure:CURRent:DC? (%s)' % ('@1,2'))
    print(I_values)
    I_avg += I_values[1]
    V_values = B2902A.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % ('@1,2'))
    print(V_values)
    print('')
    time.sleep(0.1)

I_avg /= 100
print('Average VDD1v8 Current is ' + str(I_avg))

# Turn off the channels
time.sleep(1)
#B2902A.write(':OUTPut1:STATe %d' % (0))
#B2902A.write(':OUTPut2:STATe %d' % (0))

# Close connection
B2902A.close()
rm.close()
