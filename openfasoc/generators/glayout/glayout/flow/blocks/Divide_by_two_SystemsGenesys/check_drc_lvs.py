#!pip install pyfiglet
#!pip install netgen
from colorama import Fore, Style
from pyfiglet import Figlet
import sys
import os
import subprocess

def run_lvs(layout_gds: str, schematic_spice: str, setup_file: str, output_report: str = "lvs_report.log"):
    """
    Run LVS (Layout vs. Schematic) using Netgen.

    Args:
        layout_gds (str): Path to the GDS layout file.
        schematic_spice (str): Path to the SPICE schematic file.
        setup_file (str): Path to the Netgen setup file for the PDK.
        output_report (str): Path to save the LVS report. Default is "lvs_report.log".
    """
    print_heading("Running LVS")
    print(f"\n...LVS on Layout: {layout_gds} and Schematic: {schematic_spice}...")

    # Check if input files exist
    if not os.path.exists(layout_gds):
        raise FileNotFoundError(f"Layout GDS file not found: {layout_gds}")
    if not os.path.exists(schematic_spice):
        raise FileNotFoundError(f"Schematic SPICE file not found: {schematic_spice}")
    if not os.path.exists(setup_file):
        raise FileNotFoundError(f"Netgen setup file not found: {setup_file}")
    
    try:
        # Run Netgen LVS command
        lvs_command = [
            "netgen",
            "-batch", "lvs",
            f"{schematic_spice} {Path(schematic_spice).stem}",
            f"{layout_gds} {Path(layout_gds).stem}",
            setup_file,
            output_report
        ]
        print(f"\n...Executing: {' '.join(lvs_command)}...")
        result = subprocess.run(lvs_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        # Print Netgen output
        print("\nNetgen Output:")
        print(result.stdout)
        print(f"\nLVS completed successfully. Report saved to {output_report}")

    except subprocess.CalledProcessError as e:
        print("\nError during LVS:")
        print(e.stderr)
        raise EnvironmentError("LVS failed! Check the input files and setup.")


#colorama.init(autoreset=True)
figlet = Figlet(font='slant')

def print_heading(text):
    """Prints a colorful heading for the current action using colorama and pyfiglet"""
    print(Fore.YELLOW + figlet.renderText(text))

import shutil

layout_gds = "/content/OpenFASOC/openfasoc/generators/glayout/glayout/flow/blocks/Divide_by_two_SystemsGenesys/divide_two.gds"
schematic_spice = "/content/OpenFASOC/openfasoc/generators/glayout/glayout/flow/spice/netlist.py"
setup_file = "/content/OpenFASOC/openfasoc/generators/glayout/glayout/flow/pdk/sky130_mapped/sky130A_mapped.py"

run_lvs(layout_gds, schematic_spice, setup_file)
