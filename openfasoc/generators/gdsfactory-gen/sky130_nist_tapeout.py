from opamp import opamp
from gdsfactory.read.import_gds import import_gds

def opamp_add_pads():
	"""adds the MPW-5 pads to opamp.
	Also adds text labels and pin layers so that extraction is nice
	"""
	pad = import_gds("mpw5_pad.gds")


