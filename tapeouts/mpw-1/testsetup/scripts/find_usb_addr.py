# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 21:46:45 2021

@author: Qirui Zhang

Checking the addresses of each bridge board
"""

from pyftdi.gpio import GpioMpsseController
from pyftdi.usbtools import UsbTools

# GPIO Board USB addresses
FT232H_list = UsbTools.find_all([(0x403, 0x6014)])
gpio0_addr = "ftdi://ftdi:232h:" + hex(FT232H_list[0][0].bus)[2:].zfill(2) + ":"+hex(FT232H_list[0][0].address)[2:].zfill(2)+"/1"
gpio1_addr = "ftdi://ftdi:232h:" + hex(FT232H_list[1][0].bus)[2:].zfill(2) + ":"+hex(FT232H_list[1][0].address)[2:].zfill(2)+"/1"
gpio2_addr = "ftdi://ftdi:232h:" + hex(FT232H_list[2][0].bus)[2:].zfill(2) + ":"+hex(FT232H_list[2][0].address)[2:].zfill(2)+"/1"

# Check which bridge is gpio0
print("USB Address of the first board to be checked is: " + gpio0_addr)
gpio0 = GpioMpsseController()
gpio0.configure(gpio0_addr, direction=0xffff, frequency=1e6)

    # Write D0 to 0
gpio0.write(0x0000)
    # Write D0 to 1
gpio0.write(0x0001)

gpio0.close()

# Check which bridge is gpio1
print("USB Address of the second board to be checked is: " + gpio1_addr)
gpio1 = GpioMpsseController()
gpio1.configure(gpio1_addr, direction=0xffff, frequency=1e6)

    # Write D0 to 0
gpio1.write(0x0000)
    # Write D0 to 1
gpio1.write(0x0001)

gpio1.close()

# Check which bridge is gpio2
print("USB Address of the third board to be checked is: " + gpio2_addr)
gpio2 = GpioMpsseController()
gpio2.configure(gpio2_addr, direction=0xffff, frequency=1e6)

    # Write D0 to 0
gpio2.write(0x0000)
    # Write D0 to 1
gpio2.write(0x0001)

gpio2.close()