import re
import sys
import subprocess as sp

genDir = os.path.join(os.path.dirname(os.path.relpath(__file__)),"../")
flowTopDir = genDir + "../../OpenROAD-flow-scripts/"

p = sp.Popen([''], cwd=flowTopDir)
