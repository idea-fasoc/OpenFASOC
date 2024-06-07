import copy
import inspect
import itertools
import operator
import re
import shutil
import string
from abc import ABC, abstractmethod
from importlib import import_module
from pathlib import Path
from typing import Callable, Literal, Optional, Union, cast
import datetime
import glayout.syntaxer.dynamic_load

import nltk
import glayout.syntaxer.nltk_init_deps

def list_cartesian_product(list1: list, list2: list, both: bool=False) -> list:
    """Compute the Cartesian product of two lists and combine elements into a list of strings.

    Args:
        list1 (list): The first list.
        list2 (list): The second list.
        both (bool): provide the cartesian product of list1,list2 AND list2,list1

    Returns:
        list: A list containing the Cartesian product of the input lists as strings.
    """
    # Cartesian product of the two lists
    cartesian_product = list(itertools.product(list1, list2))
    # Combine the elements into a list of strings
    combined_list = [' '.join(map(str, pair)) for pair in cartesian_product]
    return combined_list + (list_cartesian_product(list2,list1,False) if both else [])


# used to automatically update supported actions whenever a class which inherits from GlayoutAction is added to this file
def get_all_derived_classes(class_type, remove_parent: bool=True) -> list:
    """Finds all derived classes of a particular parent type in the current python file\
    Args:
        class_type (any): the parent type you want derived classes for
        remove_parent (bool): if True, do not include the parent class in the returned list
    Returns list of derived classes
    """
    all_classes = [classname for name, classname in globals().items() if isinstance(classname, type)]
    glayout_actions = [classname for classname in all_classes if issubclass(classname, GlayoutAction)]
    try:
        glayout_actions.remove(GlayoutAction)
    except ValueError:
        pass
    return glayout_actions


def parse_direction(direction: str) -> Union[str,None]:
    """parses a string to see if it contains a valid direction are up/north/above, right/east, left/west, down/south/below
    Args: 
        direction (str)
    Returns None if no direction found or an integer 0-3 (0=west,1=north,2=south,3=east)
    """
    direction = direction.lower().strip()
    findany = lambda strlst : any(ind in direction for ind in strlst)
    if findany(["left","west"]):
        return 0
    elif findany(["up","north","above"]):
        return 1
    elif findany(["right","east"]):
        return 2
    elif findany(["down","south","below"]):
        return 3
    else:
        return None



class ParametersList:
    """store function parameter information
    self.params is a list with the following format:
        [ {name, defaultvalue, type}, ... ]
    if niether type nor default is specified, both fields contain inspect.Parameter.empty
    self.func_name: str the name of the function
    """
    class noprintobj:
        def __init__(self,data):
            self.data = data
        def __str__(self):
            return str(self.data)
        def __repr__(self):
            return str(self.data)
    
    def __init__(self, func)->dict:
        self.func_name = func.__name__
        parameters = inspect.signature(func).parameters
        self.params = list()
        for param_name, param in parameters.items():
            paraminfo = {"name":param_name, 'defaultvalue':param.default, 'type':param.annotation}
            self.params.append(paraminfo)

    def __iter__(self):
        return iter(self.params)
    def names(self):
        return [param["name"] for param in self.params]
    def find(self, param_name: str):
        """look for param with name param_name. 
        If found, return info, else return None"""
        for param in self.params:
            if param["name"]==param_name:
                return param
        return None
    def __str__(self):
        return str(self.params)
    
    def __construct_glayers(self) -> dict:
        glayerids = ['met1', 'met2', 'met3', 'met4', 'met5', 'metal1', 'metal2', 'metal3', 'metal4', 'metal5', 'capmet', 'active', 'diffusion', 'tap', 'welltap', 'n+s/d', 'p+s/d', 'polysilicon', 'poly', 'p+', 'n+', 'deep nwell', 'pwell', 'nwell', 'dnwell']
        glayerids += ["metal 1", "metal 2","metal 3","metal 4","metal 5","met 1","met 2","met 3","met 4","met 5"]
        glayerids += ["via 1", "via 2","via 3","via 4","via1","via2","via3","via4","metal contact","mcon","metal con"]
        glayers = dict()
        for glayerid in glayerids:
            if "p+" in glayerid:
                glayers[glayerid] = "p+s/d"
            elif "n+" in glayerid:
                glayers[glayerid] = "n+s/d"
            elif "poly" in glayerid:
                glayers[glayerid] = "poly"
            elif "cap" in glayerid:
                glayers[glayerid] = "capmet"
            elif "tap" in glayerid:
                glayers[glayerid] = "active_tap"
            elif "active" in glayerid or "diff" in glayerid:
                glayers[glayerid] = "active_diff"
            elif "well" in glayerid:
                if "d" in glayerid:
                    glayers[glayerid] = "dnwell"
                elif "n" in glayerid:
                    glayers[glayerid] = "nwell"
                else:
                    glayers[glayerid] = "pwell"
            elif "via" in glayerid:
                for i in range(1,5):
                    if str(i) in glayerid:
                        glayers[glayerid] = f"via{i}"
            elif "met" in glayerid:
                for i in range(1,6):
                    if str(i) in glayerid:
                        glayers[glayerid] = f"met{i}"
            elif "con" in glayerid:
                glayers[glayerid] = "mcon"
            else:
                raise ValueError("could not parse this id")
        return glayers
    def __cfgformat_from_list(self, strlist: list[str]):
        rtrstr = str()
        for ele in strlist:
            rtrstr += "\'" + ele + "\' | "
        rtrstr =rtrstr.removesuffix("| ")
        return rtrstr
    def __custom_tokenize(self, sentence: str) -> list:
        sentence = sentence.strip().removesuffix(".").removeprefix("with")
        # save and replace all instances of strings with indicator words
        string_pattern = re.compile(r'\'[^\']*\'|\"[^\"]*\"')
        string_list = [str(match.group()) for match in string_pattern.finditer(sentence)]
        string_list = [w.replace("\"","").replace("'","").strip() for w in string_list]
        sentence = re.sub(string_pattern, "sTRingindICatorWOrd", sentence)
        # add a space after every symbol (except period and _)
        rsymbols = list(set(string.punctuation) - {'.', '_'})
        parsedsentence = str()
        for char in sentence:
            if char in rsymbols:
                parsedsentence += f" {char} "
            else:
                parsedsentence += char
        sentence = copy.deepcopy(parsedsentence)
        # double space (add one space everywhere there is a space)
        parsedsentence = str()
        for char in sentence:
            if char.isspace():
                parsedsentence += f" {char}"
            else:
                parsedsentence += char
        sentence = copy.deepcopy(parsedsentence)
        # save and replace all instances of numbers with indicator words
        number_pattern = re.compile(r'(?:^|\s|\b)-?\d+(\.\d+)?([eE]-?\d+)?(?=\s|$|[^\w\d])')
        number_list = [str(match.group()) for match in number_pattern.finditer(sentence)]
        number_list = [num.strip() for num in number_list]
        sentence = re.sub(number_pattern, "nUMptindICatorWOrd", sentence)
        # save numbers and strings to list and return tokenized sentence
        self.__number_list = number_list
        self.__string_list = string_list
        return sentence.split()
    def __get_str_grammar(self, known_paramsORvars: list) -> str:
        if len(known_paramsORvars)==0:
            known_paramsORvars = ["thiswordwillsurelyneverevercomeupduringparsing"]
        basic_grammar = str()
        basic_grammar += """S -> ArgList\n"""
        basic_grammar += """ArgList -> ArgDesc | ArgDesc ArgList | ArgDesc ListSeparator ArgList\n"""
        basic_grammar += """ListSeparator -> ',' | ', and' | 'and'\n"""
        basic_grammar += """ArgDesc -> Value Paramname | Paramname Value | Paramname Filler Value | Value Filler Paramname\n"""
        basic_grammar += """Filler -> 'is' | '=' | 'equal' | 'equals' | 'of' | 'for'\n"""
        basic_grammar += """Value  -> Number | Glayer | Dictionary | Boolean | List | Tuple | String | paramORvar\n"""
        basic_grammar += """Vpair -> Value ',' Value | Value Value \n"""
        basic_grammar += """Values -> Vpair | Vpair Values | Vpair ',' Values\n"""
        basic_grammar += """Number -> 'nUMptindICatorWOrd'\n"""
        basic_grammar += """String -> 'sTRingindICatorWOrd'\n"""
        basic_grammar += """Parity -> '+' | '-' | 'positive' | 'negative' | 'plus' | 'minus'\n"""
        basic_grammar += """Boolean -> 'true' | 'false' | 'True' | 'False'\n"""
        basic_grammar += """List   -> '[' Values ']' | '[' Value ']'\n"""
        basic_grammar += """Tuple  -> '(' Values ')' | '(' Value ')' | Values\n"""
        basic_grammar += """Dictionary  -> '{' keyvalpairs '}'\n"""
        basic_grammar += f"""paramORvar  -> {self.__cfgformat_from_list(known_paramsORvars)}\n"""
        basic_grammar += """keyvalpairs -> Value ':' Value | Value ':' Value ',' keyvalpairs\n"""
        basic_grammar += f"Glayer -> {self.__cfgformat_from_list(self.__construct_glayers().keys())}\n"
        basic_grammar += f"Paramname -> {self.__cfgformat_from_list(self.names())}\n"
        return basic_grammar

    def parse_user_params(self, known_paramsORvars: list, user_input_params: Optional[str]=None):
        """Take user params as a string and parse+error check to produce a dictionary of params
        Args:
            user_input_params (str)
        """
        if user_input_params is None or user_input_params.isspace() or len(user_input_params)==0:
            return {}
        # tokenize
        tokens = self.__custom_tokenize(user_input_params)
        # try to parse syntax
        # formulate the grammar using the parameters
        self.__grammar = nltk.CFG.fromstring(self.__get_str_grammar(known_paramsORvars))
        self.__grammar_parser = nltk.ChartParser(self.__grammar)
        try:
            mytree = list(self.__grammar_parser.parse(tokens))[0]
        except Exception as serr:
            raise ValueError("You may have provided a parameter that does not exist for this function OR there may be some other error") from serr
        # reinsert numbers and strings
        numlist_index = 0
        strlist_index = 0
        for pos in mytree.treepositions('leaves'):
            if "nUMptindICatorWOrd" in mytree[pos]:
                mytree[pos] = self.__number_list[numlist_index]
                numlist_index += 1
            elif "sTRingindICatorWOrd" in mytree[pos]:
                mytree[pos] = "\""+self.__string_list[strlist_index]+"\""
                strlist_index += 1
        # grab user params from the tree
        user_params = dict()
        for i, ArgDesc in enumerate(mytree.subtrees(lambda t: t.label()=="ArgDesc")):
            # TODO: implement param name aliasing
            paramname = "".join(list(ArgDesc.subtrees(lambda A: A.label()=="Paramname"))[0].leaves())
            # TODO: implement more sophisticated value parsing, and properly add double qoutes are glayers
            value = " ".join(list(ArgDesc.subtrees(lambda A: A.label()=="Value"))[0].leaves())
            user_params[paramname] = self.noprintobj(value)
        # split off kwargs into actual key word arguments in the params dictionary
        if user_params.get("kwargs") is not None:
            # TODO: maybe does not support edgecase where kwargs contains a dictionary? check
            user_params[self.noprintobj("None")] = self.noprintobj("None,"+user_params["kwargs"].data.split("{")[-1].replace("}",""))
            del user_params["kwargs"]
        user_params = str(user_params).replace("None: None,","")
        return user_params




######################################################
# Data structures for possible operations with Glayout
######################################################

class GlayoutAction(ABC):    
    """each GlayoutAction corresponds to one or several Glayout code operations
    GlayoutActions are convertible to code via the "get_code" method

    Args:
        ABC (_type_): _description_
    """
    # GlayoutActions must be convertible to Glayout code via the get_code method
    @abstractmethod
    def get_code(self) -> str:
        pass
    
    # GlayoutActions must have a test_suite to confirm functionality
    @classmethod
    @abstractmethod
    def test(cls):
        pass


class ImportCell(GlayoutAction):
    """Import an existing CellFactory
    The following information is stored:
        identifiers: list[str]
        handle: callable
        relative_path: str
        parameters: ParametersList
    """
    #@validate_call
    def __init__(self, component_identifiers: list[str], component_name: str, module_path: Optional[Union[str, Path]]=None, overwrite_module: bool=True):
        """Store neccessary information 
        Will try to import the module; if it fails, will raise an exception
        Args:
            component_identifiers (list[str]): a list of potential names the user may use to identify this component
            component_name (str): name of the thing we want to import from the target python module
            module_path (str | Path | None): path of the module we want to import from
            relative_path (bool): if true, takes the module_path directly as a python relative import path
        """
        # try to find an os path to the desired module by looking in Glayout
        if module_path is None:
            # try to resolve path of glayout package
            matching_files = Path(__file__).resolve().parents[1]
            # matching_files = list(Path("./").resolve().rglob("glayout"))
            if matching_files.is_dir():
                glayout_path = (matching_files.resolve() / "flow").resolve()
            else:
                raise FileNotFoundError("Glayout.flow package not found in a sub folder of ../ directory")
            # try to resolve path of user module in Glayout package
            # this will look for the file which starts with "component_name" ANYWHERE in the glayout.flow package
            matching_files = list(glayout_path.rglob(str(component_name)+".py"))
            matching_files += list(glayout_path.rglob(str(component_name)+"_cell.py"))
            matching_files += list(glayout_path.rglob(str(component_name)+".convo"))
            # also check the test_cases directory for convo files
            # matching_files += list((glayout_path / "../llm/syntax_data/convos").rglob(str(component_name)+".convo"))
            if len(matching_files)>0:
                module_path = matching_files[-1].resolve()
            else:
                raise FileNotFoundError("Could not find a module called "+str(component_name)+" in Glayout")
        # copy convo file into glayout Components and then create a python file and copy it into glayout components
        if str(module_path).endswith(".convo"):
            components_directory = glayout_path / "blocks"
            if module_path.parent != components_directory:
                shutil.copy(module_path, components_directory)
            glayoutcode = glayout.syntaxer.dynamic_load.run_session(module_path,True)
            component_name = glayout.syntaxer.dynamic_load.get_funccell_name(glayoutcode)
            module_path = components_directory / (component_name + ".py")
            # write python code from a convo to the components directory
            with open(module_path,mode="w") as pycell:
                pycell.write(glayoutcode)
        # resolve module_path into a python relative import path (if it is not already so)
        if any(ind in Path(module_path).as_posix() for ind in ["/",".py"]):
            module_path = Path(module_path).resolve()
            # error check that the path is indeed a python module and a real file
            if module_path.suffix != ".py" or (not module_path.is_file()):
                raise ValueError("module to import must be a python file ending in .py")
            # if the module is not in the glayout.flow directory, it should be copied into current directory so it can be imported
            module_path_parts = [part for part in module_path.parts]
            if "flow" in module_path_parts:
                module_path = "glayout." + ".".join(module_path_parts[module_path_parts.index("flow"):]).removesuffix(".py")
            else:
                # ensure the file does not already exist in the current directory, then copy
                if Path("./"+module_path.name).is_file() and not overwrite_module:
                    raise ValueError("module name cannot conflict with existing module name in "+str(Path("./").resolve()))
                shutil.copy(module_path,"./")
                module_path = module_path.stem
        # import callable (and make sure what we are importing is indeed callable)
        python_import_path = str(module_path)
        imported_obj = self.from_module_import(python_import_path, component_name)
        if not callable(imported_obj):
            raise TypeError("the thing you are trying to import must be callable")
        # store relavent import information
        self.identifiers = component_identifiers
        self.handle = imported_obj
        self.relative_path = python_import_path
        self.parameters = ParametersList(imported_obj)
    
    @classmethod
    def from_module_import(cls, module: str, nameofobjtoimport: str):
        """this function is similar to the following line of python
        from {module} import {nameofobjtoimport}
        Returns: the object that was imported
        """
        module_object = import_module(module)
        if module_object is None:
            raise ImportError("could not import module, maybe cell's __init__.py is missing?")
        try:
            return getattr(module_object, nameofobjtoimport)
        except AttributeError:
            # Try appending "_cell" if the direct attribute fetch failed
            cell_attr_name = f"{nameofobjtoimport}_cell"
            try:
                return getattr(module_object, cell_attr_name)
            except AttributeError:
                error_msg = (f"Could not find '{nameofobjtoimport}' or '{cell_attr_name}' in module '{module_object}'.")
                raise AttributeError(error_msg) from None
    
    def get_code(self) -> str:
        """returns as str a whole import line of code"""
        return "from "+self.relative_path+" import "+self.handle.__name__
    
    @classmethod
    def test(cls):
        tests = list()
        tests.append([["nmos","nfet"],"nmos","glayout.flow.primitives.fet"])
        tests.append([["pmos","pfet"],"pmos","glayout.flow.primitives.fet"])
        tests.append([["guardring","tapring","welltap","well tap", "tap ring"],"tapring","glayout.flow.primitives.guardring"])
        tests.append([["mimcap"],"mimcap","glayout.flow.primitives.mimcap"])
        tests.append([["mimcap array","mimcaparray","mimcap_array"],"mimcap_array","glayout.flow.primitives.mimcap"])
        tests.append([["via","via stack","via_stack"],"via_stack","glayout.flow.primitives.via_gen"])
        tests.append([["via array","via_array"],"via_array","glayout.flow.primitives.via_gen"])
        tests.append([["nlp"],"test_stream","../interpreter/deprecated/../deprecated/practice_stream.py"])
        tests.append([["nmos","nfet"],"nmos","./glayout/flow/primitives/fet.py"])
        #print("expected\t\t\tresult")
        for testinst in tests:
            print(ImportCell(*testinst).get_code())
    

class CreateCellParameter(GlayoutAction):
    """Create a new cell parameter
    The following information is stored:
        varname: str
        type: Any
        defaultvalue: int/float/None
        reqs: tuple[opcode, value]
    """
    #@validate_call
    def __init__(
            self, 
            varname: str, 
            vartype: Optional[Literal[int, float]]=None, 
            defaultvalue: Optional[Union[int,float]]=None, 
            requirements: Optional[tuple[Literal[">",">=","<","<=","!=","=="],Union[float,int]]]=None
        ):
        """Create a cell parameter
        Args:
            varname (str): name of parameter
            vartype (Literal[int, float]): type of parameter is either int or float
            defaultvalue: default value for parameter, Optional, None indicates no default
            requirements: tuple[condition,value] where variable must be {condition} {value}
            value can be a value or it can refer to another parameter
                for example, variable must be <= 5
        """
        self.varname = str(varname)
        self.type = vartype
        self.defaultvalue = defaultvalue if self.type is None or defaultvalue is None else self.type(defaultvalue)
        self.reqs = None
        if requirements is not None:
            required_op = None
            if requirements[0]==">":
                required_op = operator.gt
            elif requirements[0]=="<":
                required_op = operator.lt
            elif requirements[0]==">=":
                required_op = operator.ge
            elif requirements[0]=="<=":
                required_op = operator.le
            elif requirements[0]=="==":
                required_op = operator.eq
            elif requirements[0]=="!=":
                required_op = operator.ne
            self.reqs=(required_op,requirements[1])
    
    def get_code(self) -> str:
        """returns as str a single parameter with type annotation to go in function definition
        includes a tab in front and comma at the end
        """
        param = self.varname
        if self.type is not None:
            param += ": "+self.type.__name__
        if self.defaultvalue is not None:
            param += "="+str(self.defaultvalue)
        if self.reqs is not None:
            raise NotImplementedError("parameter error checking has not yet been implemented")
        return "\t" + param + ", "
    
    def __str__(self) -> str:
        return self.type.__name__ + " " + self.varname + ((" = "+str(self.defaultvalue)) if self.defaultvalue is not None else "")
    
    @classmethod
    def test(cls):
        tests = list()
        tests.append(["width",float])
        tests.append(["length",float,0])
        tests.append(["fingers",int,3])
        for testinst in tests:
            print(CreateCellParameter(*testinst).get_code())


class CreateWorkingVariable(GlayoutAction):
    """create a new working variable
    The following information is stored:
        varname: str
        expression: str
    """
    #@validate_call
    def __init__(self, varname: str, input_expression: str):
        """create a working variable
        Args:
            varname (str): name of working variable
            input_expression (str): mathematical expression or value
        """
        self.varname = str(varname)
        self.expression = input_expression #sympify(input_expression)
        #self.handle = symbols(self.varname)
    
    def get_code(self):
        """return a complete line of code that defines the working variable"""
        return self.varname + " = "+str(self.expression)
    
    @classmethod
    def test(cls):
        tests = list()
        tests.append(["max_metal_sep","pdk.util_max_metal_sep()"])
        tests.append(["pi","3.1415"])
        for testinst in tests:
            print(CreateWorkingVariable(*testinst).get_code())


class PlaceCell(GlayoutAction):
    """Place an existing cell at the origin
    The following information is stored:
        name: str (name for the component reference + _reference)
        handle: Callable
        params: parameters to pass to callable
    """
    ref_suffix = "ref"
    #@validate_call
    def __init__(self, toplvl_name: str, generator_handle: Callable, component_name: str, user_input_parameters: str, known_paramsORvars: list):
        """Store all information neccessary to place a cell without moving it anywhere
        Args:
            generator_handle (Callable): cell factory
            component_name (str): name to assign to this component
            user_input_parameters (str): just the portion of user input containing the parameters for the component
            user input should be parameter name followed by value (optionally with a filler word e.g. [of, =, is])
            user input should contain NOTHING except parameters and values
            known_paramsORvars (list): a list containing names of the currently defined parameters or variables
        """
        # append to the place table
        self.name = component_name
        self.handle = generator_handle
        self.params = ParametersList(generator_handle).parse_user_params(known_paramsORvars, user_input_parameters)
        self.toplvl_name = toplvl_name
    
    def get_code(self) -> str:
        """return 3 complete lines of code for placing a component"""
        comment = f"# placing {self.name} centered at the origin"
        l1 = f"{self.name} = {self.handle.__name__}(pdk,**{str(self.params)})"
        l2 = f"{self.name}_{self.ref_suffix} = prec_ref_center({self.name})"
        l3 = f"{self.toplvl_name}.add({self.name}_{self.ref_suffix})"
        l4 = f"{self.toplvl_name}.add_ports({self.name}_{self.ref_suffix}.get_ports_list(),prefix=\"{self.name}_\")"
        return comment + "\n" + l1 + "\n" + l2 + "\n" + l3 + "\n" + l4
    
    @classmethod
    def test(cls):
        exp_name = "example_toplvl"
        tests = list()
        from glayout.flow.primitives.fet import nmos
        tests.append([exp_name,nmos,"mirror","width of 4 length of 1"])
        for testinst in tests:
            print(PlaceCell.get_code(*testinst))


class AbsoluteMove(GlayoutAction):
    """Move an existing Component by an absolute (x,y) distance
    The following information is stored:
        name: str (name of component to move should match the place table)
        move_distance: tuple[float,float] (x,y) absolute move distance
    """
    #@validate_call
    def __init__(self, name_of_component_to_move: str, toplvl_name:str, absolute_move_info: tuple[float,float]):
        self.name = str(name_of_component_to_move)
        self.move_distance = eval(absolute_move_info) if isinstance(absolute_move_info,str) else absolute_move_info
        self.toplvl_name = toplvl_name
    
    def get_code(self) -> str:
        xmov = self.move_distance[0]
        ymov = self.move_distance[1]
        movecode = f"{self.name}_ref.movex({xmov}).movey({ymov})\n"
        movecode += f"remove_ports_with_prefix({self.toplvl_name},\"{self.name}_\")\n"
        movecode += f"{self.toplvl_name}.add_ports({self.name}_ref.get_ports_list(),prefix=\"{self.name}_\")"
        return movecode
    
    @classmethod
    def test(cls):
        tests = list()
        tests.append(["mirror","top",(4.2,3.5)])
        tests.append(["ref","top",(9,5)])
        for testinst in tests:
            print(AbsoluteMove(*testinst).get_code())

class RelativeMove(GlayoutAction):
    """Move an existing Component relative to another component
    The following information is stored:
        name: str (name of component to move should match the place table)
        comp_id: str (name of the referenced component)
        direction: tuple[int,int] either 0,1,-1 representing x,y multiplier to separation (up/north/above, right/east, left/west, down/south/below)
        separation: str (variable or value but do not try to parse just send directly to code)
        strdirection: str to use in creating the comment for the move
    """
    move_index = int(0)

    #@validate_call
    def __init__(self, name_of_component_to_move: str, toplvl_name: str, relative_comp: str, direction: str, separation: str="maxmetalsep"):
        """Store all information neccessary to move a Component relative to another component
        Args:
            name_of_component_to_move (str): name of the component that will be moved
            relative_comp (str): name of component that is taken as a reference for the move
            direction (str): up/north/above, right/east, left/west, down/south/below
            separation (str): value, variable, or expression to use for separation between relative comp and comp we are moving
        """
        self.name = str(name_of_component_to_move)
        self.relative_comp = str(relative_comp)
        self.toplvl_name = toplvl_name
        # TODO: more sophisticated validation that can distinguish float from var for separation
        self.separation = str(separation) if separation is not None else "maxmetalsep"
        # parse direction
        direction = direction.lower().strip()
        self.strdirection = direction
        dirint = parse_direction(direction)
        if dirint==1:
            self.direction = (0,1)
        elif dirint==2:
            self.direction = (1,0)
        elif dirint==0:
            self.direction = (-1,0)
        elif dirint==3:
            self.direction = (0,-1)
        else:
            raise ValueError("invalid direction, move must be either up/north/above, right/east, left/west, or down/south/below")
    
    def get_code(self) -> str:
        movinfo = [self.separation*direc for direc in self.direction]
        l1 = f"# move {self.name} {self.strdirection} {self.relative_comp}"
        l2 = None
        if self.direction[0]==1:# move to the right
            l2 = f"{self.direction[0]}*({self.separation} + center_to_edge_distance({self.relative_comp}_ref,3) + center_to_edge_distance({self.name}_ref,1))"
            movfunc, cidx = "movex", 0
        if self.direction[0]==-1:# move to the left
            l2 = f"{self.direction[0]}*({self.separation} + center_to_edge_distance({self.relative_comp}_ref,1) + center_to_edge_distance({self.name}_ref,3))"
            movfunc, cidx  = "movex", 0
        if self.direction[1]==1:# move to the north
            l2 = f"{self.direction[1]}*({self.separation} + center_to_edge_distance({self.relative_comp}_ref,2) + center_to_edge_distance({self.name}_ref,4))"
            movfunc, cidx  = "movey", 1
        if self.direction[1]==-1:# move to the south
            l2 = f"{self.direction[1]}*({self.separation} + center_to_edge_distance({self.relative_comp}_ref,4) + center_to_edge_distance({self.name}_ref,2))"
            movfunc, cidx  = "movey", 1
        if l2 is None:
            raise ValueError("move must be either up/north/above, right/east, left/west, or down/south/below")
        l2 = f"relativemovcorrection_{str(self.move_index)} = " + l2
        l3 = movfunc + f"({self.name}_ref,destination=(relativemovcorrection_{str(self.move_index)} + {self.relative_comp}_ref.center[{cidx}]))"
        # update ports
        l4 = f"remove_ports_with_prefix({self.toplvl_name},\"{self.name}_\")"
        l5 = f"{self.toplvl_name}.add_ports({self.name}_ref.get_ports_list(),prefix=\"{self.name}_\")"
        return l1 + "\n" + l2 + "\n" + l3 + "\n" + l4+ "\n" + l5

    @classmethod
    def test(cls):
        raise NotImplementedError("testing RelativeMove has not yet been implemented")


class Route(GlayoutAction):
    """Route between two existing Ports (port1->port2)
    The following information is stored:
        port1: str (name of first port)
        port2: str (name of second port)
        route_type: handle (c,l,or straight route)
        params: dict paramters to pass to function
    """
    #@validate_call
    def __init__(self, toplvl_name: str, route_type: Callable, port1: str, port2: str, parameters: str, known_paramsORvars: list, compref: str=None):
        """Store all neccessary information to route between two ports
        Args:
            route_type (Callable): l,c, straight, or smart route
            port1 (str):
            port2 (str):
            parameters (str): user input parameters
            known_paramsORvars (list): names of currently defined parameters and variables
            compref (str, optional): if smart route this will be passed along
        """
        self.port1 = str(port1)
        self.port2 = str(port2)
        self.route_type = route_type
        # parse user params
        self.params = ParametersList(self.route_type).parse_user_params(known_paramsORvars, parameters)
        self.toplvl_name = toplvl_name
        self.compref = compref
    
    def get_code(self) -> str:
        port1s = f"{self.toplvl_name}.ports[\"{self.port1}\"]"
        port2s = f"{self.toplvl_name}.ports[\"{self.port2}\"]"
        if "smart" in self.route_type.__name__:
            return f"{self.toplvl_name} << {self.route_type.__name__}(pdk,{port1s},{port2s},{self.compref},{self.toplvl_name},**{str(self.params)})"
        return f"{self.toplvl_name} << {self.route_type.__name__}(pdk,{port1s},{port2s},**{str(self.params)})"
    
    @classmethod
    def test(cls):
        from glayout.flow.routing.c_route import c_route
        tests = list()
        tests.append([c_route,"name_of_port_1","name_of_port_2","cwidth of 4 width1=3"])
        for testinst in tests:
            print(Route(*testinst).get_code())



# Top level Code Relational table
class GlayoutCode(GlayoutAction):
    """Stores all needed information to create Glayout code in relation tables
    GlayoutActions require some general context provided by the GlayoutCode class"""
    
    HEAD_MARKER = "####\n# Compiled Glayout\n# Apache License\n# Version 2.0, January 2004\n# http://www.apache.org/licenses/"

    # each table is implemented as a list of dictionaries
    def __init__(self, toplvl_name: str):
        self.toplvl_name = toplvl_name.replace(" ","_").strip()
        # tables
        self.import_table = list()# list of ImportCell type
        self.parameter_table = list()# list of CreateCellParameter type
        self.bulk_action_table = list()# list of Route, AbsoluteMove, RelativeMove, PlaceCell, CreateWorkingVariable
        # initialize the import table to contain all primitives and routing primitives
        self.__known_generator_ids = list()# list of str
        self.__random_name_index = int(0)
        # primitives
        self.update_import_table(["nmos","nfet"],"nmos","glayout.flow.primitives.fet")
        self.update_import_table(["pmos","pfet"],"pmos","glayout.flow.primitives.fet")
        self.update_import_table(["guardring","tapring","welltap","well tap", "tap ring"],"tapring","glayout.flow.primitives.guardring")
        self.update_import_table(["mimcap"],"mimcap","glayout.flow.primitives.mimcap")
        self.update_import_table(["mimcap array","mimcaparray","mimcap_array"],"mimcap_array","glayout.flow.primitives.mimcap")
        self.update_import_table(["via","via stack","via_stack"],"via_stack","glayout.flow.primitives.via_gen")
        self.update_import_table(["via array","via_array"],"via_array","glayout.flow.primitives.via_gen")
        # general components and layout strategies
        two_nfet_interdigitized_aliases = ["interdigitized","interdigitated"]+list_cartesian_product(["interdigitized","interdigitated"],["nmos","nfet"],True)
        self.update_import_table(two_nfet_interdigitized_aliases,"two_nfet_interdigitized","glayout.flow.placement.two_transistor_interdigitized")
        generic_4T_interdigitzed_aliases = list_cartesian_product(list_cartesian_product(["four","4"], ["interdigitized","interdigitated"]),["fet","transistor"])
        self.update_import_table(generic_4T_interdigitzed_aliases, "generic_4T_interdigitzed", "glayout.flow.placement.four_transistor_interdigitized")
        two_pfet_interdigitized_aliases = list_cartesian_product(["interdigitized","interdigitated"],["pmos","pfet"],True)
        self.update_import_table(two_pfet_interdigitized_aliases,"two_pfet_interdigitized","glayout.flow.placement.two_transistor_interdigitized")
        self.update_import_table(["diff pair","diff_pair","differential pair","differential pairs","differential transistor"],"diff_pair_generic","glayout.flow.blocks.diff_pair")
        # import routing funcs
        self.update_import_table(["smart route","smart","smart_route"],"smart_route","glayout.flow.routing.smart_route")
        self.update_import_table(["L route","L_route","l route","l_route"],"L_route","glayout.flow.routing.L_route")
        self.update_import_table(["C route","C_route","c route","c_route"],"c_route","glayout.flow.routing.c_route")
        self.update_import_table(["straight route","straight_route"],"straight_route","glayout.flow.routing.straight_route")
        # general utils are hardcoded imports in the get_code method
        # add working variable max metal separation
        self.update_variable_table("maxmetalsep","pdk.util_max_metal_seperation()")
        self.update_variable_table("double_maxmetalsep","2*pdk.util_max_metal_seperation()")
        self.update_variable_table("triple_maxmetalsep","3*pdk.util_max_metal_seperation()")
        self.update_variable_table("quadruple_maxmetalsep","4*pdk.util_max_metal_seperation()")
        self.__placed_noname_objs = dict()
    
    def search_import_table(self, generator_id: str) -> Callable:
        """find a component with one identifier matching generator_id and return the function handle"""
        handle = None
        for generator in self.import_table:
            if any(generator_id==identifier for identifier in generator.identifiers):
                handle = generator.handle
        if handle is None:
            raise LookupError("the generator you were looking for was not found. Perhaps it uses a different alias?")
        return handle
    
    def update_import_table(self, component_identifiers: list[str], component_name: Optional[str]=None, module_path: Optional[Union[str, Path]]=None):
        """Add an ImportCell to the import_table, see ImportCell class"""
        if component_name is None or component_name=="" or component_name.isspace():
            component_name = f"comp_{self.__random_name_index}"
            self.__random_name_index += 1
        self.__known_generator_ids += component_identifiers
        self.import_table.append(ImportCell(component_identifiers, component_name, module_path))
    
    def update_parameter_table(
            self, 
            varname: str, 
            vartype: Optional[Literal[int, float]]=None, 
            defaultvalue: Optional[Union[int,float]]=None, 
            requirements: Optional[tuple[Literal[">",">=","<","<=","!=","=="],Union[float,int]]]=None
        ):
        """Add a CreateCellParameter to the parameter_table, see CreateCellParameter class"""
        self.parameter_table.append(CreateCellParameter(varname,vartype, defaultvalue, requirements))
    
    def update_variable_table(self, varname: str, input_expression: str):
        """Add a CreateWorkingVariable to the variable_table, see CreateWorkingVariable class"""
        self.bulk_action_table.append(CreateWorkingVariable(varname, input_expression))
    
    def update_place_table(self, generator_id: str, user_input_parameters: str, component_name: Optional[str]=None):
        """Add a PlaceCell to the place_table, see PlaceCell class
        Args:
            generator_id (str): a known name for cell factory to use
            component_name (str): name to assign to this component
            user_input_parameters (str): just the portion of user input containing the parameters for the component
            user input should be parameter name followed by value (optionally with a filler word e.g. [of, =, is])
            user input should contain NOTHING except parameters and values
        """
        if component_name is None:
            current_val = self.__placed_noname_objs.get(generator_id,int(0))
            self.__placed_noname_objs[generator_id] = current_val + 1
            component_name = generator_id + str(current_val)
        self.bulk_action_table.append(PlaceCell(self.toplvl_name, self.search_import_table(generator_id), component_name, user_input_parameters, self.get_params_and_vars()))
    
    def update_move_table(self, move_type: str, name_of_component_to_move: str, *args, **kwargs):
        """move_type can be absolute, relative"""
        move_type = move_type.lower().strip()
        if move_type=="absolute":
            self.bulk_action_table.append(AbsoluteMove(name_of_component_to_move,self.toplvl_name,*args,**kwargs))
        elif move_type=="relative":
            self.bulk_action_table.append(RelativeMove(name_of_component_to_move,self.toplvl_name,*args,**kwargs))
    
    def update_route_table(self, port1: str, port2: str, parameters: str, route_type: Optional[str]=None):
        # guess route type if not specified
        if route_type is None:
            route_type = "smart_route"
        else:
            # parse route type
            route_type = str(route_type).lower().strip()
            rpre = "L" if "l" in route_type else ("c" if "c" in route_type else ("straight" if "s" in route_type else None))
            rpre = "smart" if "sma" in route_type else rpre
            if rpre is None:
                rpre = "smart"
            route_type = rpre + "_route"
        # look for top comp ref this goes back to
        if route_type=="smart_route":
            for cellname in self.names_of_placed_cells():
                compref = cellname in port1 and cellname in port2
                if compref is not None:
                    compref = cellname + "_ref"
                    break
        else:
            compref = None
        self.bulk_action_table.append(Route(self.toplvl_name,self.search_import_table(route_type),port1,port2,parameters,self.get_params_and_vars(),compref))
    
    def get_params_and_vars(self) -> list[str]:
        """Get the names of parameters and variables.
        This method retrieves the names of parameters from the parameter table and the names of variables created
        by 'CreateWorkingVariable' actions from the bulk action table.
        Returns:
            list[str]: A list containing the names of parameters and variables.
        """
        params = [param.varname for param in self.parameter_table]
        variables = [variable.varname for variable in self.bulk_action_table if isinstance(variable,CreateWorkingVariable)]
        return params + variables
    
    def get_code(self) -> str:
        # time this NLP was compiled to python code
        current_time = datetime.datetime.now()
        compilation_head = self.HEAD_MARKER + f"\n# {current_time}\n\n"
        # produce all import code
        import_code = "from glayout.flow.pdk.mappedpdk import MappedPDK\n"
        import_code += "from gdsfactory import Component\n"
        import_code += "from glayout.flow.pdk.util.comp_utils import move, movex, movey, prec_ref_center, evaluate_bbox, center_to_edge_distance\n"
        import_code += "from glayout.flow.pdk.util.port_utils import remove_ports_with_prefix\n"
        for comp_import in self.import_table:
            import_code += comp_import.get_code() + "\n"
        # create function header
        function_head = f"def {self.toplvl_name}_cell(\n\tpdk: MappedPDK,\n"
        for param in self.parameter_table:
            function_head += param.get_code()+"\n"
        function_head += "):\n"
        # create variables, place, route, and move in the order that user supplied these directions
        function_body = "pdk.activate()\n"
        function_body += f"{self.toplvl_name} = Component(name=\"{self.toplvl_name}\")\n"
        for bulk_action in self.bulk_action_table:
            function_body += bulk_action.get_code()+"\n"
        function_body = "\n".join(["\t"+line for line in function_body.splitlines()])
        # footer
        footer = "\n\treturn "+self.toplvl_name+"\n"
        return compilation_head + import_code + "\n" + function_head + function_body + footer
    
    @classmethod
    def test(cls, test_all: bool=True):
        glayout_actions = get_all_derived_classes(GlayoutAction)
        glayout_actions.remove(cls)
        print("now testing individual Glayout Actions")
        for action in glayout_actions:
            print(f"\ntesting{action.__name__}")
            try:
                action.test()
            except Exception as e:
                print(e)
        print("\n\nnow testing GlayoutCode")
        codeobj = GlayoutCode("newtoplvl")
        codeobj.update_import_table(["stream","test_stream"],"test_stream","./deprecated/practice_stream.py")
        codeobj.update_parameter_table("width",float,5.5)
        codeobj.update_variable_table("int_width","int(width)")
        codeobj.update_place_table("nfet","mirror","width of 5 length is 2")
        codeobj.update_move_table("absolute","mirror",(3.3,3.3))
        codeobj.update_route_table("nfet_drain_west","nfet_source_west","","c route")
        print(codeobj.get_code())
    
    def names_of_placed_cells(self) -> list:
        """Get the names of cells that have been placed.
        Returns:
            list: A list containing the names of cells that have been placed.
        """
        names = list()
        for action in self.bulk_action_table:
            if isinstance(action,PlaceCell):
                names.append(action.name)
        return names

    def find_first_generator_id(self, sentence: str) -> str:
        """returns the longest generator id in the given sentence
        should only be used on sentences which for sure have a generator id in them
        """
        # look for genids found in the sentence
        genid_candidates = list()
        for genid in self.__known_generator_ids:
            if genid in sentence:
                genid_candidates.append(genid)
        # error checking
        if len(genid_candidates) == 0:
            print(self.__known_generator_ids)
            print(sentence)
            raise LookupError("no known generator id was found in the provided sentence")
        # prefer longer strings
        return max(genid_candidates, key=len)






