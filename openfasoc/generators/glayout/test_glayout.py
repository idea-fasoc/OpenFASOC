from glayout.flow.primitives.fet import nmos
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk as sky130
import sys
import os
import subprocess
from pathlib import Path
from importlib import metadata
from tempfile import TemporaryDirectory
import warnings
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

# used for pretty printing messages
try:
    import colorama
except ImportError as e:
    os.system('pip install colorama')
    import colorama

try:
    import pyfiglet
except ImportError as e:
    os.system('pip install pyfiglet')
    import pyfiglet

from colorama import Fore, Style
from pyfiglet import Figlet

colorama.init(autoreset=True)
figlet = Figlet(font='slant')

def print_heading(text):
    """Prints a colorful heading for the current action using colorama and pyfiglet"""
    print(Fore.YELLOW + figlet.renderText(text))

import shutil

def print_dynamic_separator(text=None):
    """Prints a separator that spans the width of the terminal, with optional text in the middle"""
    terminal_width = shutil.get_terminal_size().columns  # Get the width of the terminal
    if text:
        # Ensure the separator is not longer than the terminal width
        total_length = len(text) + 2
        side_length = (terminal_width - total_length) // 2
        print("\n" + "#" * side_length + " " + text + " " + "#" * side_length)
    else:
        print("\n" + "#" * terminal_width)
 
# Check if the current Python version meets the minimum requirement
def check_python_version():
    """Check if the current Python version meets the minimum requirement of Python 3.10"""
    print_heading("Python version check")
    print("\n...Checking Python version...")
    if sys.version_info < (3, 10):
        print("This script requires Python 3.10 or higher. Please upgrade your Python installation.")
        sys.exit(1) 
    print("\nPython version is 3.10 or above!")
        
# check if all requirements have been installed
def check_python_requirements(requirements_file):
    """Check if all Python requirements are installed using the requirements file provided
    in the top level directory of OpenFASOC. Checks the package versions as well"""
    print_heading("Checking Python requirements")
    with open(requirements_file, 'r') as f:
        requirements = f.read().splitlines()
    for requirement in requirements:
        # Split the requirement safely
        parts = requirement.split('==')
        package_name = parts[0]
        if len(parts) == 2:
            required_version = parts[1]
            print(f"\n...Checking {package_name}=={parts[1]}...")
        else:
            required_version = None  # No specific version required
            print(f"\n...Checking {package_name}...")
        try:
            installed_version = metadata.version(package_name)
            if required_version and installed_version != required_version:
                raise ImportError(f"Version mismatch for {package_name}: Expected {required_version}, found {installed_version}. Consider running 'pip install -r {requirements_file}'")
        except metadata.PackageNotFoundError:
            raise ImportError(f"Requirement {package_name} not installed. Consider running 'pip install -r {requirements_file}'")
        print(f"\n{package_name} is installed!")
        
# function to check for system-wide tools like Magic, Netgen, and Ngspice
def check_system_tools(tool_names, miniconda3_path):
    """Checks if magic and ngspice are installed by running the respective commands with the --version flag. Checks if netgen is present in the Miniconda3 installation directory (where the executables are placed)"""
    print_heading("Checking system tools")
    for tool in tool_names:
        try:
            # spawn a subprocess with the tool and the --version flag
            print(f"\n...Checking {tool}...")
            result = subprocess.run([tool, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            print(f"\n{tool} is installed!")
        except subprocess.CalledProcessError as e:
            raise EnvironmentError(f"{tool} not installed or not in PATH. Please install it.") from e
    
    # check netgen installation in the miniconda3 library folder
    print("\n...Checking netgen...")
    netgen_path = miniconda3_path / "lib" / "netgen"
    if not netgen_path.exists():
        raise EnvironmentError("Netgen not found in expected location!")
    print("\nnetgen is installed!")


def check_miniconda3_and_pdk():
    """Checks if Miniconda3 is installed and in PATH, and if the PDK root is present in the expected locations. Also checks if the required PDK directories are present in the PDK root."""
    print_heading("Checking Miniconda3 and PDK")
    # Check if miniconda3 is installed
    try:
        # conda installation check
        result = subprocess.run(['conda', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print(f"\nMiniconda3 is installed: {result.stdout}")
    except subprocess.CalledProcessError as e:
        raise EnvironmentError("Miniconda3 not installed or not in PATH. Please install it.") from e

    # Check if PDK root is present in the expected locations
    paths_to_check = [
        Path("/usr/bin/miniconda3/share/pdk/"), 
        Path(f"/home/{os.getenv('LOGNAME')}/miniconda3/share/pdk/")
    ]
    pdk_root = None
    for path in paths_to_check:
        print(f"\n...Checking for PDK root at: {path}...")
        if path.exists():
            pdk_root = path
            break

    if not pdk_root:
        raise EnvironmentError("PDK root not found in expected locations!")
    else:
        print(f"\nPDK root found at: {pdk_root}")
    
    # check if the pdk directories are present
    miniconda3_path = pdk_root.resolve().parents[1]
    required_pdk_dirs = ["sky130A", "gf180mcuC"]
    missing_dirs = [pdk_dir for pdk_dir in required_pdk_dirs if not (pdk_root / pdk_dir).exists()]

    if missing_dirs:
        warnings.warn(f"\nMissing required PDK directories: {', '.join(missing_dirs)}")

    print("\nAll required PDK directories are present!")
    return miniconda3_path, pdk_root

def place_nfet_run_lvs():
    """places a default nmos components using the sky130 pdk, and runs netgen lvs on it. This utilises the spice generation of the component, magic, and netgen, so it makes up a good test for the installation"""
    
    print_heading("NMOS and LVS")
    print("\n...Creating nmos component...")
    nmos_component = nmos(sky130)
    print("Created nmos component!")
    print("\n...Running LVS...")
    nmos_component.name = 'nmos_test'
    sky130.lvs_netgen(nmos_component, 'nmos_test')        
    print("LVS run successful!")

    
if __name__ == "__main__":
    system_tools = ['magic', 'ngspice']
    
    print_dynamic_separator()
    check_python_version()
    print_dynamic_separator()
    check_python_requirements("../../../requirements.txt")
    print_dynamic_separator()
    miniconda3_path, pdk_root = check_miniconda3_and_pdk()
    print_dynamic_separator()
    check_system_tools(system_tools, miniconda3_path)
    print_dynamic_separator()
    place_nfet_run_lvs()
    print_dynamic_separator("Tool check successful!")
    
   
