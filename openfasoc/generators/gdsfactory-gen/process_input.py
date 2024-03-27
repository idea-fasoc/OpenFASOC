import nltk
from relational import GlayoutCode, parse_direction
import io
from pathlib import Path
import copy
from typing import Optional, Union, Literal



class Session:
	"""The session stores all relevant information for producing code from a conversation"""
	
	generic_prompt = """Place a cell, move a cell, route, create a parameter, or define a variable.
You can also dump code or save this conversation, or enter "help" to see supported syntax in detail
What would you like to do?"""
    
	def __init__(self, outputstream: io.IOBase, inputstream: Optional[io.IOBase]=None, toplvlname: Optional[str]=None):
		"""initialize a conversation and greet the user
		Args:
			outputstream (io.IOBase): used to print outputs
			inputstream (io.IOBase): saved for (optionally) reading in user input, also just provide a string
			NOTE: if input stream not provided, str input must be provided
			toplvlname (str): in string only mode, you can input toplvl name using this arg
		"""
		self.inputstream = inputstream
		self.outputstream = outputstream
		# greet the user and get a top level name for the component
		if toplvlname is None:
			if inputstream is None:
				raise RuntimeError("you must specify AT LEAST one of inputstream or name")
			self.print_to_stream("Hello!")
			self.print_to_stream("Please provide a name for the Component you want to create")
			self.print_to_stream("remember, this will be the name of your top level component: ")
			self.name = self.read_from_stream().strip()
		else:
			self.name = str(toplvlname).strip()
		# save a list of responses to recreate this component from a .conv file
		self.conversation_responses = list()
		self.conversation_responses.append(self.name)
		# init the code object
		self.code = GlayoutCode(self.name)
		# create a backup that goes back exactly one call to process_next_input
		self.backup = self.__backup()
	

	def __backup(self):
		newobj = self.__class__
		backup = newobj.__new__(newobj)
		backup.inputstream = self.inputstream
		backup.outputstream = self.outputstream
		backup.conversation_responses = copy.deepcopy(self.conversation_responses)
		backup.code = copy.deepcopy(self.code)
		backup.backup = None
		return backup
	
	def save_to_disk(self, savecode: bool=True, savepath: Optional[Union[str,Path]]=None):
		"""Save NLP results to disk, either save code or conversation responses.
		Args:
			savemode: bool, default to True==save code, false==save conversation responses
			savepath: Optional (defaults to None), 
			NOTE: None is the same as specifying the current directory "./"
		"""
		# figure out which save mode we are in
		suffix = ".py" if savecode else ".convo"
		if savepath is None:
			savepath = Path("./").resolve()
		savepath = Path(savepath.strip()) if isinstance(savepath,str) else savepath
		if savepath.is_dir():
			savepath /= f"{self.code.toplvl_name}{suffix}"
		if savepath.parent.is_dir():
			with savepath.open("w") as savefile:
				if savecode:
					savefile.write(self.code.get_code())
				else:
					savefile.writelines([r+"\n" for r in self.conversation_responses])
		else:
			raise FileNotFoundError("the directory you specfied does not exist")
	
	def print_to_stream(self, toprint: Optional[str]=None):
		if toprint is None:
			toprint=""
		self.outputstream.write(toprint+"\n")
	

	def read_from_stream(self) -> str:
		response = self.inputstream.readline()
		#self.conversation_responses.append(response)
		return response
	
	def __save_response(self, response: str):
		self.conversation_responses.append(response.strip())

	def process_next_input(self, text_input: str) -> bool:
		"""main driver for doing things
		returns True if session is ongoing
		"""
		self.backup = self.__backup()
		sentences = nltk.sent_tokenize(text_input)
		for sentence in sentences:
			saveresponse = True
			sentence = sentence.strip().removesuffix(".")
			words = nltk.word_tokenize(sentence)
			mode_indicator = words[0].strip().replace("-","").lower()
			# parse user input
			if mode_indicator[0]=="h":# help
				saveresponse = False
				syntaxes = list()
				syntaxes.append("place an genidhere called/named compnamehere with paramshere")#place_syntax
				syntaxes.append("route between/from port1 and/to port2 using routetype with paramshere")#route_syntax
				syntaxes.append("move compname [by] (x,y)")# absolute move syntax
				syntaxes.append("move compname [filler words] direction [filler words] reference_comp [by separation]")# relative move syntax
				import_syntax = "import comp1, comp2 from mod1, and comp3 from some/path/mod.py"
				import_syntax += "\n\tNOTE: imports from glayout only need component name"
				import_syntax += "\n\tNOTE: if mod name is not specified, it is assumed to be the component name"
				syntaxes.append(import_syntax) # import
				syntaxes.append("create/define [a/an] param_type parameter called/named paramname")# parameter
				syntaxes.append("create/define [a/an] var_type variable called/named varname =/equal valorexpr")#variable
				syntaxes.append("save/dump [conversation/code] to pathtosaveto\n\tNOTE: save code is assumed if neither conversation nor code are specified")#
				# print all
				self.print_to_stream("\nBelow are valid sentences:")
				#for i, syntax in enumerate(syntaxes):
				for syntax in syntaxes:
					#self.print_to_stream(str(i)+" : "+syntax)
					self.print_to_stream(syntax)
				self.print_to_stream()
			elif mode_indicator[0]=="i":# import
				imports = sentence.replace("and",",").replace("import","").replace("from","").strip().split(",")
				for modimport in imports:
					if modimport=="" or modimport.isspace():
						continue
					words = modimport.strip().split()
					compname = words[0]
					modpath = words[1] if len(words)>1 else None
					aliases = [compname]#TODO implement comp aliasing
					self.code.update_import_table(aliases,compname,modpath)
			elif "create" in mode_indicator or "define" in mode_indicator:# create/define a variable or param
				vartype = None
				for word in words:
					word = word.lower().strip()
					if "int" in word:
						vartype = int
					elif "float" in word:
						vartype = float
					elif "bool" in word:
						vartype = bool
					elif "str" in word:
						vartype = str
					elif "tupl" in word:
						vartype = tuple
					if vartype is not None:
						break
				varname = None
				for i, word in enumerate(words):
					if word in ["called","named"]:
						varname = words[i+1]
						break
				expr = None
				eqpar = sentence.replace("equal","=").strip().removesuffix(".")
				expr = eqpar.split("=")[1] if "=" in eqpar else None
				if "parameter" in words:
					self.code.update_parameter_table(varname,vartype,None,None)
				else:#variable
					self.code.update_variable_table(varname,expr)
			elif mode_indicator[0]=="p":# place
				if "configuration" in sentence:
					raise NotImplementedError("configs not yet implemented")
				genid = self.code.find_first_generator_id(sentence)
				comp_name = None
				for i, word in enumerate(words):
					if word in ["called","named"]:
						comp_name = words[i+1]
						break
				params = None
				for i, word in enumerate(words):
					if word=="with":
						params = " ".join(words[i:])
						break
				self.code.update_place_table(genid,params,comp_name)
			elif mode_indicator[0]=="r":# route
				port1 = None
				port2 = None
				routetype = None
				params = None
				for i, word in enumerate(words):
					if word in ["between","from"]:
						port1 = words[i+1] if port1 is None else port1
					elif word in ["from","and"]:
						port2 = words[i+1] if port2 is None else port2
					elif word in ["using","a","an"]:
						routetype=words[i+1]
					elif word=="with":
						params = " ".join(words[i:])
				self.code.update_route_table(port1,port2,params,routetype)
			elif mode_indicator[0]=="m":# move
				direction = None
				for word in words:
					if parse_direction(word) is not None:
						direction = word
						break
				if direction is not None:
					spacesepwords = sentence.split()
					relative_comp = spacesepwords[-3] if spacesepwords[-2]=="by" else spacesepwords[-1]
					separation = spacesepwords[-1] if spacesepwords[-2]=="by" else None
					self.code.update_move_table("relative",words[1],relative_comp,direction,separation)
				else:# assume absolute move
					words = nltk.word_tokenize(sentence.replace("(","").replace(")","").replace("by",""))
					self.code.update_move_table("absolute",words[1], words[2])
			elif mode_indicator[0]=="e":# dump code
				saveresponse = False
				self.print_to_stream("\n"+self.code.get_code())
				return False
			elif mode_indicator=="save" or mode_indicator=="dump":# save the conversation to a .convo file, or code to .py file
				saveresponse = False
				savepath = None
				for i,word in enumerate(words):
					if word in ["to","at","path"]:
						savepath = "".join(words[i+1:])
						break
				savecode = any(wr in words for wr in ["code","python","py","program"])
				self.save_to_disk(savecode, savepath)
			elif mode_indicator[0]=="s":# show a component
				saveresponse = False
				raise NotImplementedError("dynamic show mode not yet implemented")
			else:
				self.print_to_stream("invalid input")
				self.print_to_stream("sentences must begin with either place, route, generate, or move")
			# save when needed and return True to continue prompting for input
			if saveresponse:
				self.__save_response(sentence)
			return True



