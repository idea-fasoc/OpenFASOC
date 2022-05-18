##for HSPICE netlist
import re
import function
import os
import sys
import math

import numpy as np
from scipy import interpolate

def gen_dcdc_netlist(cells, args, jsonSpec, platformConfig, srcDir):
    
    # power mux models
    xs = [100, 330, 1000, 3300, 10000]
    ys = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8]
    zz = np.array([-3.36E-11, -3.63E-11, -3.71E-11, -3.75E-11, -3.76E-11, 8.41E-04, 2.87E-04, 9.82E-05, 3.01E-05, 9.98E-06, 1.66E-03, 5.71E-04, 1.96E-04, 6.02E-05, 2.00E-05, 2.44E-03, 8.50E-04, 2.93E-04, 9.03E-05, 2.99E-05, 3.17E-03, 1.12E-03, 3.90E-04, 1.20E-04, 3.99E-05, 3.84E-03, 1.39E-03, 4.85E-04, 1.50E-04, 4.98E-05, 4.43E-03, 1.63E-03, 5.78E-04, 1.80E-04, 5.98E-05, 4.88E-03, 1.85E-03, 6.66E-04, 2.09E-04, 6.96E-05, 5.17E-03, 2.03E-03, 7.44E-04, 2.37E-04, 7.93E-05, 5.34E-03, 2.14E-03, 8.03E-04, 2.60E-04, 8.84E-05, 5.49E-03, 2.21E-03, 8.38E-04, 2.78E-04, 9.63E-05, 5.68E-03, 2.29E-03, 8.75E-04, 2.98E-04, 1.06E-04, 5.91E-03, 2.39E-03, 9.35E-04, 3.36E-04, 1.17E-04, 6.19E-03, 2.52E-03, 1.05E-03, 3.73E-04, 1.28E-04, 6.50E-03, 2.69E-03, 1.20E-03, 4.07E-04, 1.38E-04, 6.84E-03, 2.93E-03, 1.32E-03, 4.39E-04, 1.48E-04, 7.21E-03, 3.31E-03, 1.44E-03, 4.70E-04, 1.58E-04, 7.60E-03, 3.73E-03, 1.55E-03, 5.02E-04, 1.69E-04, 8.03E-03, 4.11E-03, 1.66E-03, 5.32E-04, 1.79E-04]).reshape((19, 5))
    powmux_f = interpolate.interp2d( xs, ys, zz)
    
    # Get the design spec & parameters from spec file
    try:
        Iload = float(jsonSpec['specifications']['Iload (mA)'])
    except KeyError as e:
        print('Error: Bad Input Specfile. \'Iload (mA)\' value is missing under \'specifications\'.')
        sys.exit(1)
    except ValueError as e:
        print('Error: Bad Input Specfile. Please use a float value for \'Iload (mA)\' under \'specifications\'.')
        sys.exit(1)
    if Iload > 10.0 or Iload < 0.1:
        print('Error: Only support Iload from 0.1 ~ 10 now')
        sys.exit(1)

    try:
        Frequency = float(jsonSpec['specifications']['Clock frequency (kHz)'])
    except KeyError as e:
        print('Error: Bad Input Specfile. \'Clock frequency (kHz)\' value is missing under \'specifications\'.')
        sys.exit(1)
    except ValueError as e:
        print('Error: Bad Input Specfile. Please use a float value for \'Clock frequency (kHz)\' under \'specifications\'.')
        sys.exit(1)
	
    
    designName = jsonSpec['module_name']
    
    SupplyVolt = platformConfig['platforms'][args.platform]['nominal_voltage']
        
    print('\n\n<DCDC Spec>')
    print('DCDC Instance Name - \"' + designName + '\"')
    print('Supply Voltage - \"' + str(SupplyVolt) + '\"')
    print('Iload(mA) - \"' + str(Iload) + '\"')
    print('Frequency (kHz) - \"' + str(Frequency) + '\"')    
    
    
    # process 2:1 stage switch and cap configuration
    # Technology parameter ######
    if re.search('sky130',args.platform): 
        k_sqrt_rc = 6.1E-6
        deltaV  = 0.10
        unit_cap_capacitance = 1E-12
        unit_r_resistance = 6750
    #############################

    # Determine the cap and switch size
    dcdc_cap_size = int((Iload * 0.001) / (2 * deltaV * Frequency * 1000) / 2 / unit_cap_capacitance)
    if dcdc_cap_size == 0:
        dcdc_cap_size = 1

    dcdc_sw_size = int(unit_r_resistance / (k_sqrt_rc * SupplyVolt * math.sqrt(Frequency * 1000) / (Iload * 0.001)))
    if dcdc_sw_size == 0:
        dcdc_sw_size = 1

    # Determine Offset_y
    # offset_y = 50 * int(dcdc_sw_size / (1<<(dcdc_num_stage-1)))       # Eventually will need this to tune the APR settings
    # if offset_y == 0:
        # offset_y = 50

    # Determine power mux configuration
    num_stages = 6
    powmux_config = []
    
    for stage in range(0, num_stages):
        Iout_stage = (Iload * 0.001) * pow(2, -(num_stages - (stage + 1)))
        
        # for voltage, assuming 1/2 vdd for all stages for now
        Vout_stage = 1/2 * SupplyVolt
        
        # calculated load = V/I
        Rout_stage = Vout_stage / Iout_stage
        
        # single powmux drive
        unit_powmux_current = powmux_f(Rout_stage, Vout_stage) / 8
        
        # calculate number of parallel muxes
        num_mux = int(math.ceil(Iout_stage / unit_powmux_current)) 
        
        powmux_config.append(num_mux) 
    
    powmux_config = ["8'd" + str(cfg) for cfg in powmux_config]
    
    print('\n\n<DCDC Configuration>')
    print('dcdc_cap_size: ' + str(dcdc_cap_size))
    print('dcdc_sw_size: ' + str(dcdc_sw_size))
    print('pow_mux_config: ' + ','.join(powmux_config) + '\n\n')

    # process 6-stage conv verilog
    with open(srcDir + '/DCDC_SIX_STAGES_CONV.template.v', 'r') as file:
        filedata = file.read()
        filedata = re.sub(r'(?<=DCDC_CAP_SIZE = ).+(?=;)', str(dcdc_cap_size), filedata)
        filedata = re.sub(r'(?<=DCDC_SW_SIZE = ).+(?=;)', str(dcdc_sw_size), filedata)
        filedata = re.sub(r'(?<=DCDC_PWR_MUX_CONF = ).+(?=;)', '{' + ','.join(powmux_config) + '}', filedata)

    with open(srcDir + '/DCDC_SIX_STAGES_CONV.v', 'w') as file:
        file.write(filedata)

    # process the top level verilog
    r_netlist=open(srcDir + "/dcdcInst.template.v","r")
    lines=list(r_netlist.readlines())
    w_netlist=open(srcDir + "/dcdcInst.v","w")

    netmap_top=function.netmap()
    netmap_top.get_net('na',cells['ff_cell'],1,1,1)
    netmap_top.get_net('nb',cells['inv_cell'],1,1,1)
    netmap_top.get_net('nc',cells['clkgate_cell'],1,1,1)
	
    for line in lines:
        netmap_top.printline(line,w_netlist)

    # process the non-inverting clock verilog
    r_netlist=open(srcDir + "/DCDC_NOV_CLKGEN.template.sv","r")
    lines=list(r_netlist.readlines())
    w_netlist=open(srcDir + "/DCDC_NOV_CLKGEN.sv","w")

    netmap_novclkgen=function.netmap()
    netmap_novclkgen.get_net('na',cells['nand2_cell'],1,1,1)
    netmap_novclkgen.get_net('nb',cells['clkinv_cell'],1,1,1)
    netmap_novclkgen.get_net('nc',cells['clkinv_cell'],1,1,1)
    netmap_novclkgen.get_net('ne',cells['clkinv_cell'],1,1,1)
    netmap_novclkgen.get_net('nf',cells['clkinv_cell'],1,1,1)
    netmap_novclkgen.get_net('nd',cells['nor2_cell'],1,1,1)
	
    for line in lines:
        netmap_novclkgen.printline(line,w_netlist)
        
    
    netmap_buffer=function.netmap()
    netmap_buffer.get_net('nb',cells['clkinv_cell'],1,1,1)
    netmap_buffer.get_net('nc',cells['clkinv_cell'],1,1,1)
    
    r_netlist=open(srcDir + "/DCDC_BUFFER.template.sv","r")
    lines=list(r_netlist.readlines())
    w_netlist=open(srcDir + "/DCDC_BUFFER.sv","w")
	
    for line in lines:
        netmap_buffer.printline(line,w_netlist)
    
    # process the power mux verilog
    r_netlist=open(srcDir + "/DCDC_POWMUX.template.v","r")
    lines=list(r_netlist.readlines())
    w_netlist=open(srcDir + "/DCDC_POWMUX.v","w")

    netmap_powmux=function.netmap()
    netmap_powmux.get_net('na',cells['inv_cell_w'],1,1,1)
    netmap_powmux.get_net('nb',cells['inv_cell_w'],1,1,1)
	
    for line in lines:
        netmap_powmux.printline(line,w_netlist)
        
    return

