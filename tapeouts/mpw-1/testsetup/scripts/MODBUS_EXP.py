# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 20:57:47 2021

@author: Qirui Zhang

Example codes for automating the temperature chamber through Modbus
"""

import minimalmodbus as modbus

Tchamber = modbus.Instrument("COM1", 1)  # port name, slave address (in decimal)
Tchamber.mode = modbus.MODE_RTU
Tchamber.serial.baudrate = 9600

## Read temperature. Output from Temp Chamber is 16b 2's comp numbers with 1 decimal ##
temperature = Tchamber.read_register(100, 0)  # Registernumber, number of decimals
temp_bin = f"{temperature:016b}"
if temp_bin[0] == "1":  # T < 0C
    temperature = -(2**16 - temperature) / 10.0
else:
    temperature = temperature / 10.0
print("Real Temperature in the chamber is " + str(temperature))

## Change temperature setpoint (SP) ##
temperature = Tchamber.read_register(300, 0)  # Registernumber, number of decimals
temp_bin = f"{temperature:016b}"
if temp_bin[0] == "1":  # T < 0C
    temperature = -(2**16 - temperature) / 10.0
else:
    temperature = temperature / 10.0
print("SetPoint Temperature is " + str(temperature))

new_temp = 25
if new_temp < 0:  # T < 0C
    set_point = 2**16 + new_temp * 10
else:
    set_point = new_temp * 10
# print(new_temp)
Tchamber.write_register(
    300, set_point, 0
)  # Registernumber, value, number of decimals for storage
print("Changed SetPoint Temperature to " + str(new_temp))

# Close Serial Port
Tchamber.serial.close()
