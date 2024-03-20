import argparse
import inspect
import fileinput
import io
import sys
from pathlib import Path
from typing import Optional, Callable, Literal
from gdsfactory import Component
# import primitives
from glayout.primitives.fet import nmos, pmos, multiplier
from glayout.primitives.guardring import tapring
from glayout.primitives.mimcap import mimcap, mimcap_array
from glayout.primitives.via_gen import via_array, via_stack
# import placement macros
from glayout.placement.two_transistor_interdigitized import two_transistor_interdigitized, two_nfet_interdigitized
from glayout.placement.two_transistor_place import two_transistor_place
# import routing macros
from glayout.routing.c_route import c_route
from glayout.routing.L_route import L_route
from glayout.routing.straight_route import straight_route


PLACE_HELP="""
In place mode, the keyword “place” begins a sentence.
The keyword “place” is followed by one or more generators.
The generator is one of 
nmos, pmos, multiplier, mimcap, mimcap_array, via_stack, via_array, tapring, two_nfet_interdigitized

To specify arguments to a generator, you should write the argument name and value followed by a , or and

Following the list of “circuits”, An optional configuration can be specified.
The following are examples of valid configurations
configuration xyx yxy xyx
configuration x y
configuration xxxy
configuration yyyx
And so on…

Here is an example sentence for place mode: 
place an nfet and pfet in xyx yxy xyx configuration.
place an nfet with width=5,length=7
place an nfet with width 5 and length 7
"""


########################################
# helper functions
########################################

def prompt_from_list(prompt_list, convo) -> int:
	for i,prompt_item in enumerate(prompt_list):
		convo.print_and_update_session(str(i)+". "+str(prompt_item))
	convo.print_and_update_session("enter the number corresponding to the desired input_and_process:",False)
	choosen_index = int(convo.inputstream.readline().strip().strip("\n"))
	while(choosen_index>=len(prompt_list)):
		convo.print_and_update_session("choosen_index out of range please try again:",False)
		choosen_index = input(convo.inputstream.readline().strip().strip("\n"))
	return choosen_index

#TODO finish implement
def get_param_val_as_str(input: str, generator_name: str, param_name: str) -> str:
	input = input.strip().strip(".").lower().replace(",","and").replace("="," ")
	# only keep the stuff after the generator name
	if input.find(generator_name)!=-1:
		input = input.split(generator_name)
		if len(input)<2:# no params were specfied by the user
			return str()
		input = input[1].strip()
	else:
		raise ValueError(generator_name+" was not found in input")
	# only keep the stuff after the parameter name
	if input.find(param_name)!=-1:
		input = input.split(param_name)[1].strip()
	else:
		raise ValueError(param_name+" was not found in input")
	# TODO this is not versatile
	return input.split("and")[0]


########################################
# Session state
########################################

class GlayoutCode:
	"""Store Glayout code in a way that allows both dynamic running and quick printing"""
	
	class PlaceInfo:
		def __init__(self, generator: Callable, pdk: str, params: dict):
			self.generator = generator
			self.PDK = pdk # NAME of pdk variable
			self.params = params # params are stored as str:str, param_name:param_val
		def tostr(self)->str:
			line = generator.__name__
			line += "("+self.PDK.name+"_mpdk, "
			for key,val in self.params.items():
				line += key + "=" + val + ", "
			line += ")"
	
	def __init__(self, cell_name: str, pdk: str):
		"""Store basic header info for this generator"""
		self.toplvl_args = list()
		self.PDK = pdk # NAME of pdk variable
		self.name = cell_name
		self.line_infos = list()
	
	def add_line(mode: Literal["place","route","move"], kwargs):
		if mode=="place":
			self.line_infos.append(PlaceInfo(**kwargs))
		elif mode=="route":
			self.line_infos.append(RouteInfo(**kwargs))
		elif mode=="move":
			self.line_infos.append(MoveInfo(**kwargs))
	
	def dump_code() -> str:
		code = str()
		for line_info in line_infos:
			code += line_info.tostr() + "\n"


class Session:
	"""The session stores all relevant information for producing code from a conversation"""

	# comp_options must be callable cells. The first argument must be "pdk"
	generators = [nmos,pmos,multiplier,mimcap,mimcap_array,via_stack,via_array,tapring, two_nfet_interdigitized]
	# supported pdks must be of mapped pdk type
	supported_pdks = {0:"gf180",1:"sky130"}

	def __init__(self, inputstream: io.IOBase, outputstream: io.IOBase):
		"""initialize a conversation and greet the user"""
		# init PDK, and io streams
		self.inputstream = inputstream
		self.outputstream = outputstream
		self.PDK = None
		# initialize metadata
		self.components = dict()
		self.variables = dict()
		self.conversation_prompts = list()
		self.conversation_responses = list()
		# greet the user and load pdk
		self.print_and_update_session("Hello!")
		self.__load_pdk()
		self.print_and_update_session("What would you like to create today?")
		self.print_and_update_session("Please provide a name for the Component you want to create")
		self.print_and_update_session("remember, this will be the name of your top level component: ",False)
		name = inputstream.readline()
		self.print_and_update_session("now, lets go through all the steps to create " + name)
		# init the rest of the data
		self.code = GlayoutCode(name,self.PDK.name)
		self.toplevel_comp = Component(name=name)
	
	def __load_pdk(self):
		# prompt for supportpdk
		self.print_and_update_session("please specify a PDK to get started. The supported PDKs include:)")
		pdk_index = prompt_from_list(Session.supported_pdks.values(),self)
		pdk_name = Session.supported_pdks.get(pdk_index)
		if pdk_name == "gf180":
			from glayout.pdk.gf180_mapped import gf180_mapped_pdk
			self.PDK = gf180_mapped_pdk
		elif pdk_name == "sky130":
			from glayout.pdk.sky130_mapped import sky130_mapped_pdk
			self.PDK = sky130_mapped_pdk
		else:
			raise ValueError("specify a support pdk")
		self.PDK.activate()
	
	def print_and_update_session(self, toprint: str, save: bool=True):
		"""Correctly updates the conversation prompts
		then writes toprint to the output stream provided"""
		if save:
			self.conversation_prompts.append(str(toprint))
		self.outputstream.write(toprint+"\n")
	
	def process_next_input(self) -> str:
		"""main driver for doing things"""
		response = self.inputstream.readline().strip().lower()
		# parse user input
		if response[0]=="h":# help
			self.__help(response)
		elif response[0]=="p":# place
			if "configuration" in response:
				raise NotImplementedError("configs not yet implemented")
			self.__place(response)
		elif response[0]=="r":# route
			self.__route(response)
		elif response[0]=="g":# dump code
			self.__generate_code(response)
		elif response[0]=="s":# show a component
			self.__show_component(response)
		else:
			self.print_and_update_session("invalid input",save=False)
			self.print_and_update_session("sentences must begin with either place, route, generate, or move",save=False)
		# save response
		self.conversation_responses["responses"].append(str(response))
	
	# TODO finish implement
	def __place(self, response: str):
		generators = [(i,fnc.__name__) for i,fnc in enumerate(Session.generators)]
		generators = [generator for generator in generators if generator[1] in response]
		generator_fncs = [Session.generators[i] for i,fncname in generators]
		# loop over all generators. Each generator represents a task that must be completed
		func_calls = list()
		for generator in generator_fncs:
			
			for param in inspect.signature(generator).parameters.values():
				if param.name.lower() in ["pdk"]:
					continue
				param_val = get_param_val_as_str(response, generator.__name__, param.name)
				if (param_val=="" and param.default==inspect.Parameter.empty):
				 	self.print_and_update_session("you did not provide a value for an argument that does not have a default",save=False)
				elif param_val == "": # value not provided but param has a default
				 	continue
				else:# value was provided
					pass




if __name__=="__main__":
	# parse args
	parser = argparse.ArgumentParser(description="Load conversation from a file")
	parser.add_argument("--load_conversation", type=Path, help="Specify the file path to load a previous conversation")
	args = parser.parse_args()

	# start convo and load PDK
	convo = Session(inputstream=sys.stdin,outputstream=sys.stdout)
	
	# enter design loop
	session_ongoing = True
	loop_count = 0
	while(session_ongoing):
		convo.print_and_update_session("task "+str(loop_count)+":")
		loop_count = loop_count + 1
		convo.print_and_update_session("What do you want to do?")
		
