import copy
import io
from pathlib import Path
from typing import Optional, Union

import nltk
import glayout.syntaxer.nltk_init_deps
import glayout.syntaxer.dynamic_load
from glayout.syntaxer.relational import GlayoutCode, parse_direction
from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk

class Session:
    """The session stores all relevant information for producing code from a conversation"""

    generic_prompt = """Place a cell, move a cell, route, create a parameter, or define a variable.
You can also dump code or save this conversation, or enter "help" to see supported syntax in detail
What would you like to do?"""

    def __init__(
        self,
        outputstream: io.IOBase,
        inputstream: Optional[io.IOBase] = None,
        toplvlname: Optional[str] = None,
    ):
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
                raise RuntimeError(
                    "you must specify AT LEAST one of inputstream or name"
                )
            self.print_to_stream("Hello!")
            self.print_to_stream(
                "Please provide a name for the Component you want to create"
            )
            self.print_to_stream(
                "remember, this will be the name of your top level component: "
            )
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
        """Produce an exact copy of this class to revert after an exception"""
        newobj = self.__class__
        backup = newobj.__new__(newobj)
        backup.inputstream = self.inputstream
        backup.outputstream = self.outputstream
        backup.conversation_responses = copy.deepcopy(self.conversation_responses)
        backup.code = copy.deepcopy(self.code)
        backup.backup = None
        return backup

    def print_help(self):
        """print help message to self.outputstream"""
        syntaxes = list()
        # place_syntax
        syntaxes.append("place an genidhere called/named compnamehere with paramshere")
        # route_syntax
        syntaxes.append("route between/from port1 and/to port2 using routetype with paramshere")
        # absolute move syntax
        syntaxes.append("move compname [by] (x,y)")
        # relative move
        syntaxes.append("move compname [filler words] direction [filler words] reference_comp [by separation]")
        # import
        import_syntax = "import comp1, comp2 from mod1, and comp3 from some/path/mod.py"
        import_syntax += "\n\tNOTE: imports from glayout only need component name"
        import_syntax += "\n\tNOTE: if mod name is not specified, it is assumed to be the component name"
        syntaxes.append(import_syntax)
        # parameter
        syntaxes.append("create/define [a/an] param_type parameter called/named paramname")
        # variable
        syntaxes.append("create/define [a/an] var_type variable called/named varname =/equal valorexpr")
        syntaxes.append("save/dump [conversation/code] to pathtosaveto\n\tNOTE: save code is assumed if neither conversation nor code are specified")
        syntaxes.append("show\n\tNOTE: This will show the current component in klayout using .show and klive plugin")
        # print all
        self.print_to_stream("\nBelow are valid sentences:")
        for syntax in syntaxes:
            self.print_to_stream(syntax)
        self.print_to_stream()

    def save_to_disk(
        self, savecode: bool = True, savepath: Optional[Union[str, Path]] = None
    ):
        """Save NLP results to disk, either save code or conversation responses.
        Args:
                savemode: bool, default to True==save code, false==save conversation responses
                savepath: Optional (if None, defaults to ./),
                NOTE: None is the same as specifying the current directory "./"
        """
        # figure out which save mode we are in
        suffix = ".py" if savecode else ".convo"
        if savepath is None:
            savepath = Path("./").resolve()
        savepath = Path(savepath.strip()) if isinstance(savepath, str) else savepath
        if savepath.is_dir():
            savepath /= f"{self.code.toplvl_name}{suffix}"
        if savepath.parent.is_dir():
            with savepath.open("w") as savefile:
                if savecode:
                    savefile.write(self.code.get_code())
                else:
                    savefile.writelines([r + "\n" for r in self.conversation_responses])
        else:
            raise FileNotFoundError("the directory you specfied does not exist")

    def print_to_stream(self, toprint: Optional[str] = None):
        """prints to the configured outputstream

        Args:
            toprint (Optional[str]): string to print. If None then prints a newline.
        """
        if toprint is None:
            toprint = ""
        self.outputstream.write(toprint + "\n")

    def read_from_stream(self) -> str:
        """reads user input from the configured inputstream

        Returns:
            str: the next line of user input
        """
        response = self.inputstream.readline()
        # self.conversation_responses.append(response)
        return response

    def __save_response(self, response: str):
        self.conversation_responses.append(response.strip())

    def process_import_sentence(self, text_input: str) -> bool:
        """Will update the internal code table using a sentence which follows the import syntax

        Args:
            text_input (str): user input text
        
        Returns:
            bool: saveresponse
        """
        words = nltk.word_tokenize(text_input)
        imports = text_input.replace("and", ",").replace("import", "").replace("from", "").strip().split(",")
        for modimport in imports:
            if modimport == "" or modimport.isspace():
                continue
            words = modimport.strip().split()
            compname = words[0]
            modpath = words[1] if len(words) > 1 else None
            aliases = [compname]  # TODO implement comp aliasing
            self.code.update_import_table(aliases, compname, modpath)
        return True

    def process_param_or_var_sentence(self, text_input: str) -> bool:
        """Will update the internal code table using a sentence which follows the variable or parameter define syntax

        Args:
            text_input (str): user input text
        
        Returns:
            bool: saveresponse
        """
        words = nltk.word_tokenize(text_input)
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
            if word in ["called", "named"]:
                varname = words[i + 1]
                break
        expr = None
        eqpar = text_input.replace("equal", "=").strip().removesuffix(".")
        expr = eqpar.split("=")[1] if "=" in eqpar else None
        if "parameter" in words:
            self.code.update_parameter_table(varname, vartype, None, None)
        else:  # variable
            self.code.update_variable_table(varname, expr)
        return True

    def process_place_sentence(self, text_input: str) -> bool:
        """Will update the internal code table using a sentence which follows the place syntax

        Args:
            text_input (str): user input text
        
        Returns:
            bool: saveresponse
        """
        words = text_input.strip().split()#nltk.word_tokenize(text_input)
        if "configuration" in text_input:
            raise NotImplementedError("configs not yet implemented")
        # util func
        def split_input_on_compname(text_input:str) -> str:
                """Split a string on the words 'called' or 'named' and retain everything before these keywords.
                Args:
                    text_input (str): The input string.
                Returns:
                    str: The part of the text_input before 'called' or 'named'.
                """
                # look for either named or called in a lower case version of parts
                lc_parts = text_input.lower().split()
                indexCalled, indexNamed = None, None
                if "called" in lc_parts:
                    indexCalled = lc_parts.index("called")
                if "named" in lc_parts:
                    indexNamed = lc_parts.index("named")
                # pick which index to use or raise error if neither
                index = None
                if (indexCalled is not None) and (indexNamed is not None):
                    index = max(indexCalled,indexNamed)
                else:
                    index = indexCalled if (indexCalled is not None) else indexNamed
                if index is None:
                    raise SyntaxError("invalid place syntax, place sentence must include 'called' or 'named' keyword")
                # return everything in the sentence before the "called" or "named" keyword
                parts = text_input.split()
                return " ".join(parts[0:index])
        genid = self.code.find_first_generator_id(split_input_on_compname(text_input))
        comp_name = None
        for i, word in enumerate(words):
            if word in ["called", "named"]:
                comp_name = words[i + 1]
                break
        params = None
        for i, word in enumerate(words):
            if word == "with":
                params = " ".join(words[i:])
                break
        self.code.update_place_table(genid, params, comp_name)
        return True

    def process_route_sentence(self, text_input: str) -> bool:
        """Will update the internal code table using a sentence which follows the route syntax

        Args:
            text_input (str): user input text
        
        Returns:
            bool: saveresponse
        """
        words = nltk.word_tokenize(text_input)
        port1 = None
        port2 = None
        routetype = None
        params = None
        for i, word in enumerate(words):
            if word in ["between", "from"]:
                port1 = words[i + 1] if port1 is None else port1
            elif word in ["from", "and"]:
                port2 = words[i + 1] if port2 is None else port2
            elif word in ["using", "a", "an"]:
                routetype = words[i + 1]
            elif word == "with":
                params = " ".join(words[i:])
        self.code.update_route_table(port1, port2, params, routetype)
        return True

    def process_move_sentence(self, text_input: str) -> bool:
        """Will update the internal code table using a sentence which follows the route syntax

        Args:
            text_input (str): user input text
        
        Returns:
            bool: saveresponse
        """
        words = nltk.word_tokenize(text_input)
        direction = None
        reference_comp = None
        separation = None
        # words[0] is "move" and words[1] is the component name
        for i, word in enumerate(words[2:]):
            # try to find direction until we see it then move on
            if parse_direction(word) is not None and direction is None:
                direction = word
            # once you see a direction, look for a reference_comp
            elif (word=="by" or word=="with") and reference_comp is None:
                reference_comp = words[2:][i-1]
                separation = words[2:][i+1]
                if len(separation)>3 and separation.strip().lower()[0:3]=="sep":
                    separation = words[2:][i+2]
        # you may not find it in the loop, in which case reference_comp is the last word
        if reference_comp is None:
            reference_comp = words[-1]
        # relative move
        if direction is not None:
            spacesepwords = text_input.split()
            self.code.update_move_table("relative", words[1], reference_comp, direction, separation)
        else:  # assume absolute move
            words = nltk.word_tokenize(
                text_input.replace("(", "").replace(")", "").replace("by", "").replace("with","")
            )
            move_distance = words[2]
            if len(words) > 4 and "," in words[3]:
                move_distance = words[2] + "," + words[4]
            self.code.update_move_table("absolute", words[1], move_distance)
        return True

    def show_current_component(self, text_input: str) -> False:
        """displays the current state of the layout with klayout using .show in sky130nm tech
        if the keyword "port" is found within text_input, port tree (with depth 6) will be saved to a file instead
        Args:
            text_input (str): user input text
        Returns:
            False: saveresponse=False
        """
        if "port" in text_input.lower():
            glayout.syntaxer.dynamic_load.printPortTree_glayout_code_cell(sky130_mapped_pdk,self.code.get_code())
        elif "param" in text_input.lower():
            print(*self.code.parameter_table,sep="\n")
        else:
            glayout.syntaxer.dynamic_load.show_glayout_code_cell(sky130_mapped_pdk, self.code.get_code())
        return False
    
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
            mode_indicator = words[0].strip().replace("-", "").lower()
            # parse user input
            if mode_indicator[0] == "h":  # help
                saveresponse = False
                self.print_help()
            elif mode_indicator[0] == "i":  # import
                saveresponse = self.process_import_sentence(sentence)
            elif "create" in mode_indicator or "define" in mode_indicator:  # create/define a variable or param
                saveresponse = self.process_param_or_var_sentence(sentence)
            elif mode_indicator[0] == "p":  # place
                saveresponse = self.process_place_sentence(sentence)
            elif mode_indicator[0] == "r":  # route
                saveresponse = self.process_route_sentence(sentence)
            elif mode_indicator[0] == "m":  # move
                saveresponse = self.process_move_sentence(sentence)
            elif mode_indicator[0] == "e":  # dump code and exit
                saveresponse = False
                self.print_to_stream("\n" + self.code.get_code())
                return False
            elif (
                mode_indicator == "save" or mode_indicator == "dump"
            ):  # save the conversation to a .convo file, or code to .py file
                saveresponse = False
                savepath = None
                for i, word in enumerate(words):
                    if word in ["to", "at", "path"]:
                        savepath = "".join(words[i + 1 :])
                        break
                savecode = any(
                    wr in words for wr in ["code", "python", "py", "program"]
                )
                self.save_to_disk(savecode, savepath)
            elif mode_indicator[0] == "s":  # show a component
                saveresponse = self.show_current_component(sentence)
            elif mode_indicator[0] == "#" or mode_indicator[0]=="/": # comment
                saveresponse=True
            else:
                self.print_to_stream("invalid input")
                self.print_to_stream("sentences must begin with either place, route, generate, show, dump, or move")
                saveresponse = False
            # save when needed and return True to continue prompting for input
            if saveresponse:
                self.__save_response(sentence)
            return True
