# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2021

@author: Qirui Zhang

Sky130TempSensor chip testing: RO frequencies (raw temperature reads) of all 64 designs across temperatures
"""

'''
Check if FT232H devices are connected. Should list 3 devices.
'''
from pyftdi.usbtools import UsbTools
FT232H_list = UsbTools.find_all([(0x403, 0x6014)])
for i in FT232H_list:
    print(i)
print('')

'''
Import Libraries
'''
import tempsensor_ctrl as tsc
from tempsensor_ctrl import tempsensorIO as ts_ctrl
import pandas as pd
import pyvisa as pvisa
import minimalmodbus as modbus
import time

'''
Connect to TestEquity Temperature Chamber
'''
Tchamber = modbus.Instrument('COM1', 1)  # Windows: port name, slave address (in decimal)
#Tchamber = modbus.Instrument('/dev/ttyS5', 1)  # Linux: port name, slave address (in decimal)
Tchamber.mode = modbus.MODE_RTU
Tchamber.serial.baudrate = 9600

'''
Connect to the B2902A
'''
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
B2902A.write(':INITiate:IMMediate:ALL (%s)' % ('@1,2'))

'''
Initialize GPIO bridge boards
'''
print('Initializing GPIO Boards......')
freq = 1e6
gpio_ts = ts_ctrl(tsc.gpio_in_addr, tsc.gpio_out1_addr, tsc.gpio_out0_addr, freq)
gpio_ts.get_state()
print('')

'''
Chip Bring-Up Sequence
'''
print('Start chip bringing-up!')
# Open VDD
opened = 'no'
while opened != 'yes':
    opened = input("Please set VDD (Typ. 3.0V): enter yes/no to finish.\n")

# Open VDD1v8
opened = 'no'
while opened != 'yes':
    opened = input("Please set VDD1v8 (Typ. 1.8V): enter yes/no to finish.\n")

# Turn on CLK ref
opened = 'no'
while opened != 'yes':
    opened = input("Please turn on reference clock (Typ. 32.768kHz): enter yes/no to finish.\n")

print('')

'''
Test Frequency and Power for all 64 nodes across temperatures and voltages
'''
freq_ref = 32.768 # kHz 
temp_check_step = 12 # Sec
temp_win_length = 10 
temp_stab_time  = 60 * 1 # Sec
itr = 1

ChipNo = 10 # QP Tech. Ones starts from 10
temp_list = range(-40, 121, 10) # degree C
Supply_list = [(3.0, 1.8)]

stime = time.time()

for temp in temp_list:
    # Set temperature and wait for it to settle
    temp_set = tsc.convert_temp_write(temp)
    Tchamber.write_register(300, temp_set, 0)  # Registernumber, value, number of decimals for storage
    print('Changed SetPoint Temperature to ' + str(temp) + 'C')
    time.sleep(2)
    temp_window = []
    while True:
        # Read real chamber temperature
        temp_read = Tchamber.read_register(100, 0)  # Registernumber, number of decimals
        temp_real = tsc.convert_temp_read(temp_read)
        print('Real Temperature in the chamber is ' + str(temp_real) + 'C')
        # Maintain the window of past N-minutes temperatures
        if len(temp_window) < temp_win_length:
            temp_window.append(temp_real)
        else:
            temp_window.pop(0)
            temp_window.append(temp_real)
        # Check whether all temperature reads of past N-minutes are settled
        settled = 1
        for T in temp_window:
            if abs(T-temp) > 0.11:
                settled = 0
        # Break if temperature settles
        if settled and (len(temp_window) == temp_win_length):
            print('Temperature Settled!\n')
            break
        time.sleep(temp_check_step) # Sleep for some time before next read    
    
    time.sleep(temp_stab_time) # Wait some time for temperature of the chip to further stabalize
    
    # Begin Testing
    for supply in Supply_list: 
        # Set supply voltages
        VDD = supply[0] # V
        VDD1v8 = supply[1] # V
        B2902A.write(':SOURce1:VOLTage:LEVel:IMMediate:AMPLitude %G' % (VDD))
        B2902A.write(':SOURce2:VOLTage:LEVel:IMMediate:AMPLitude %G' % (VDD1v8))
        B2902A.write(':INITiate:IMMediate:ALL (%s)' % ('@1,2'))
        time.sleep(1)
        print('\nTesting with VDD=' + str(VDD) + ', VDD1v8=' + str(VDD1v8))

        print('Start testing RingOsc frequencies')
        repeat = 16
        dict_freqs = gpio_ts.test_all_freqs_wlut(repeat, temp, freq_ref)
        dict_freqs['Freq0 (kHz)'] = dict_freqs['Freq (kHz)']
        del dict_freqs['Freq (kHz)']
        for r in range(itr - 1):
            dict_freqs_tmp = gpio_ts.test_all_freqs_wlut(repeat, temp, freq_ref)
            dict_freqs['Freq' + str(r+1)+ ' (kHz)'] = dict_freqs_tmp['Freq (kHz)']
        
        df_meas = pd.DataFrame(dict_freqs)
        
        # Save to csv
        meas_res_path = './MeasResults/ChipNo' + str(ChipNo) + '/'
        res_csv_name = meas_res_path + 'Meas_ChipNo' + str(ChipNo) + '_Vdio' + str(VDD) + 'Vdd' + str(VDD1v8) + '_' + str(temp) + 'C.csv'
        df_meas.to_csv(res_csv_name)

'''
Set temperature to safe room temperature
'''
temp_set = tsc.convert_temp_write(20)
Tchamber.write_register(300, temp_set, 0)  # Registernumber, value, number of decimals for storage
print('Changed SetPoint Temperature to ' + str(20) + 'C')
time.sleep(2)
while True:
    # Read real chamber temperature
    temp_read = Tchamber.read_register(100, 0)  # Registernumber, number of decimals
    temp_real = tsc.convert_temp_read(temp_read)
    print('Real Temperature in the chamber is ' + str(temp_real) + 'C')
    if abs(temp_real - 20) < 5:
        print('Temperature Safe!\n')
        break
    time.sleep(temp_check_step) # Sleep for some time before next read
    
etime = time.time()

print('Time Spent is ' + str((etime - stime) / 3600) + ' hours.\n')

'''
Test Finished. Reset Chip and Close GPIO Ports
'''
finish = 'no'
while finish != 'yes':
    finish = input("Do you want to end the test?: enter yes/no.\n")
print('End of Test!')
print('')

gpio_ts.reset()
gpio_ts.close()

'''
Close Equipment Connections
'''
Tchamber.serial.close()
B2902A.close()
rm.close()