"""Provides a reusable module for creating generator main functionality
imports all pdks
provides a command line arg for choosing pdk: -p or --pdk
    current options include:
    gf180
    sky130

generator main function can import this module as follows:
from PDK.util.standard_main import pdk

the pdk is the pdk object which defaults to sky130 if none selected
"""

from PDK.sky130_mapped import sky130_mapped_pdk
from PDK.gf180_mapped import gf180_mapped_pdk
from argparse import ArgumentParser

parser = ArgumentParser(prog="PDK agnostic fet generator")
parser.add_argument("--pdk", "-p", choices=["sky130", "gf180"])
args = parser.parse_args()

pdk = None
if args.pdk == "sky130":
    pdk = sky130_mapped_pdk
elif args.pdk == "gf180":
    pdk = gf180_mapped_pdk
else:
    pdk = sky130_mapped_pdk
pdk.activate()


