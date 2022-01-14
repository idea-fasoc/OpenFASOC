# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2021

@author: Qirui Zhang

Sky130TempSensor chip testing: sanity check for a single instance
"""


'''
Check if FT232H devices are connected. Should list 3 devices.
'''
from pyftdi.usbtools import UsbTools
FT232H_list = UsbTools.find_all([(0x403, 0x6014)])
for i in FT232H_list:
    print(i)


'''
Import Libraries
'''
import tempsensor_ctrl as tsc
from tempsensor_ctrl import tempsensorIO as ts_ctrl

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

# Set CTR
sel_ctr_list = [str(i) for i in range(16)]
while True:
    sel_ctr = input("Please set the length of measurement time window: enter n = 0 ~ 15, 16*(2^n) CLK_REF cycles.\n")
    if sel_ctr not in sel_ctr_list:
        print('Please enter a number from 0 ~ 15!\n')
    else:
        break
sel_ctr = int(sel_ctr)
gpio_ts.set_sel_ctr(sel_ctr)

print('')

'''
Design Selection
'''
# Set Design Selections
sel_design_list = [str(i) for i in range(2)]
while True:
    sel_design = input("Please select between different NMOS header designs: enter 0 (gate connected to ground) or 1 (gate connected to source).\n")
    if sel_design not in sel_design_list:
        print('Please enter a number from 0 ~ 1!\n')
    else:
        break
sel_design = int(sel_design)
gpio_ts.set_sel_design(sel_design)

# Set GRP Selections
sel_grp_list = [str(i) for i in range(8)]
while True:
    sel_grp = input("Please select between different supply current: enter 0 ~ 7.\n")
    if sel_grp not in sel_grp_list:
        print('Please enter a number from 0 ~ 7!\n')
    else:
        break    
sel_grp = int(sel_grp)
gpio_ts.set_sel_grp(sel_grp)

# Set INST Selections
sel_inst_list = [str(i) for i in range(4)]
while True:
    sel_inst = input("Please select between different RingOsc inverter-chain length: enter 0 ~ 3.\n")
    if sel_inst not in sel_inst_list:
        print('Please enter a number from 0 ~ 3!\n')
    else:
        break   
sel_inst = int(sel_inst)
gpio_ts.set_sel_inst(sel_inst)

''' For checking if every node works
sel_design = 1
sel_grp = 7
sel_inst = 3
gpio_ts.set_sel_design(sel_design)
gpio_ts.set_sel_grp(sel_grp)
gpio_ts.set_sel_inst(sel_inst)
'''

'''
Reset Release
'''
# Release Chip Reset
release = 'no'
while release != 'yes':
    release = input("Do you want to release chip reset?: enter yes/no.\n")
gpio_ts.chip_reset(1)
print('Chip Reset Released!')
print('')

'''
Wait for DONE and report DOUT
'''
print('Waiting for test result......')
while True:
    done = gpio_ts.get_done()
    if done:
        print("** DONE DETECTED **")
        dout = gpio_ts.get_dout()
        print("DOUT result is " + str(dout))
        break
print('')

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