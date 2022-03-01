##for HSPICE netlist
import re
import function
import os
import sys
import math

def gen_dcdc_netlist(cells, args, jsonSpec, platformConfig, srcDir):

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
    
    
    # Get the design spec & parameters from spec file
    try:
        Iload = float(jsonSpec['specifications']['Iload (mA)'])
    except KeyError as e:
        print('Error: Bad Input Specfile. \'Iload (mA)\' value is missing under \'specifications\'.')
        sys.exit(1)
    except ValueError as e:
        print('Error: Bad Input Specfile. Please use a float value for \'Iload (mA)\' under \'specifications\'.')
        sys.exit(1)
    if Iload > 3.0 or Iload < 0.001:
        print('Error: Only support Iload from 0.001 ~ 1.0 now')
        sys.exit(1)

    try:
        OutVolt = float(jsonSpec['specifications']['Output voltage (V)'])
    except KeyError as e:
        print('Error: Bad Input Specfile. \'Output voltage (V)\' value is missing under \'specifications\'.')
        sys.exit(1)
    except ValueError as e:
        print('Error: Bad Input Specfile. Please use a float value for \'Output voltage (V) under \'specifications\'.')
    if OutVolt > 1.0 or OutVolt < 0.3:
        print('Error: Only support OutVolt in the range [0.3, 1.0] now')
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
        
    print('\n\nDCDC Spec:')
    print('DCDC Instance Name - \"' + designName + '\"')
    print('Supply Voltage - \"' + str(SupplyVolt) + '\"')
    print('Iload(mA) - \"' + str(Iload) + '\"')
    print('Output voltage (V) - \"' + str(OutVolt) + '\"')
    print('Frequency (kHz) - \"' + str(Frequency) + '\"')

    # process the power mux configuration
    
    
    
    
    
    # process 2:1 stage switch and cap configuration
    # Technology parameter ######
    if re.search('sky130',args.platform): 
        k_sqrt_rc = 6.1E-6
        deltaV  = 0.10
        unit_cap_capacitance = 2E-12
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

    # Determine metals for power lines                          # Update
    # if args.platform == 'gf12lp':
        # pg_m_h      = "K3"
        # pg_m_v      = "K2"
        # pg_via_hv   = "U2"
        # pg_unit_cap = "H2"
    # else:
        # pg_m_h      = "M7"
        # pg_m_v      = "M6"
        # pg_via_hv   = "VIA6"
        # pg_unit_cap = "M9"

    # Test Samples
    #dcdc_num_stage = 2;
    #dcdc_cap_size = 8;
    #dcdc_sw_size = 4;

    #dcdc_num_stage = 4;
    #dcdc_cap_size = 48;
    #dcdc_sw_size = 12;

    #dcdc_num_stage = 4;
    #dcdc_cap_size = 8;
    #dcdc_sw_size = 4;

    print('\n\n<DCDC Configuration>')
    print('dcdc_cap_size: ' + str(dcdc_cap_size))
    print('dcdc_sw_size: ' + str(dcdc_sw_size) + '\n\n')

    # 6-stage conv Verilog Modification
    with open(srcDir + '/DCDC_SIX_STAGES_CONV.template.v', 'r') as file:
        filedata = file.read()
        filedata = re.sub(r'parameter DCDC_CAP_SIZE = \d+;', r'parameter DCDC_CAP_SIZE = ' + str(dcdc_cap_size) + ';', filedata)
        filedata = re.sub(r'parameter DCDC_SW_SIZE = \d+;', r'parameter DCDC_SW_SIZE = ' + str(dcdc_sw_size) + ';', filedata)

    with open(srcDir + '/DCDC_SIX_STAGES_CONV.v', 'w') as file:
        file.write(filedata)

    return

