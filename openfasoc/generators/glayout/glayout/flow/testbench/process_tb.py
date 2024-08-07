import sys
import os
import argparse 
from pathlib import Path
from typing import Union, Optional 
import tempfile 
import subprocess as sp

def process_spice_testbench(
    testbench: Union[str,Path], 
    temperature: Optional[int] = 25,
    pex_path: Optional[str] = None,
    module_name: Optional[str] = None,
    mode: Optional[str] = 'normal'
):
    global PDK_ROOT
    PDK_ROOT = Path(PDK_ROOT).resolve()
    testbench = Path(testbench).resolve()
    if not testbench.is_file():
        raise ValueError("testbench must be file")
    if not PDK_ROOT.is_dir():
        raise ValueError("PDK_ROOT is not a valid directory")
    PDK_ROOT = str(PDK_ROOT)
    with open(testbench, "r") as spice_file:
        spicetb = spice_file.read()
        spicetb = spicetb.replace('{@@TEMP}', str(temperature))
        spicetb = spicetb.replace("@@PDK_ROOT", PDK_ROOT)
        spicetb = spicetb.replace("@@PEX_PATH", pex_path)
        spicetb = spicetb.replace("@@MODULE_NAME", module_name)
        if mode == "cryo":
            spicetb = spicetb.replace("*@@cryo ","")
        else:
            spicetb = spicetb.replace("*@@stp ","")
    with open(testbench, "w") as spice_file:
        spice_file.write(spicetb)

parser = argparse.ArgumentParser(
    description='Process the testbench for the given design'
)

parser.add_argument(
    '--temperature', 
    type = int, 
    help = 'Temperature to run simulation at in degrees', 
    default = 25
)

parser.add_argument(
    '--mode', 
    type = str,
    help = 'Temperature Mode: "stp", "cryo", "custom"', 
    default = 'stp'
)

parser.add_argument(
    '--pdkroot', 
    type = str, 
    help = 'Path to the PDK_ROOT',
    default = '/usr/bin/miniconda3/share/pdk/'
)

parser.add_argument(
    '--testbench', 
    type = str, 
    help = 'The component to run: opamp, currmirror, diffpair', 
    default = 'opamp'
)

parser.add_argument(
    '--pexpath',
    type = str,
    help = 'Path to the extracted spice netlist'
)

parser.add_argument(
    '--modulename',
    type = str,
    help = 'Name of the module to simulate'
)

args = parser.parse_args()

if __name__ == '__main__':
    global PDK_ROOT

    PDK_ROOT = args.pdkroot
    if Path(PDK_ROOT).resolve().exists() == False:
        print(f'PDK_ROOT path {PDK_ROOT} does not exist')
        sys.exit(1)
    else: 
        PDK_ROOT = Path(PDK_ROOT).resolve()

    temp = args.temperature
    mod = args.testbench
    pex_path = str(Path(args.pexpath).resolve())
    
    if mod == 'opamp':
        testbench = Path('opamp_tb.sp').resolve()
    elif mod == 'currmirror':
        testbench = Path('currmirror_tb.sp').resolve()
    elif mod == 'diffpair':
        testbench = Path('diffpair_tb.sp').resolve()
    else:
        print(f'Invalid component {mod}! Exiting...')
        sys.exit(1)
        
    if args.mode == 'cryo': 
        print('Overriding temperature to -269 degreees for cryo sims!')
        temp = -269
    elif args.mode == 'stp':
        print('Overriding temperature to 25 degreees for stp sims!')
        temp = 25
    elif args.mode == 'custom':
        if temp < 0: 
            print('Running Sim in cryo mode! Pinning temperature at -269 degrees!')
        elif temp == 25:
            print('Running Sim in stp mode! Pinning temperature at 25 degrees!')
        else:
            print(f'Running Sim in custom mode! Pinning temperature at {temp} degrees!')
    
    with tempfile.TemporaryDirectory() as tmpdirname:
        # copy testbench to temp directory
        tmpdirname = Path(tmpdirname)
        testbench = str(args.testbench) + '_tb.sp'
        print(testbench)
        target = tmpdirname / testbench
        with open(target, 'w') as f:
            with open(testbench, 'r') as tb:
                f.write(tb.read())
        
        
        process_spice_testbench(
            testbench=target,
            temperature=temp,
            mode=args.mode, 
            pex_path=pex_path,
            module_name=args.modulename
        )
        
        print(f'Processed testbench for {mod} at {temp} degrees in {args.mode} mode!')
        print(f'Running simulation using: ngspice -b {testbench}')
        
        sp.Popen(['ngspice', '-b', testbench], cwd=tmpdirname).wait()
    
