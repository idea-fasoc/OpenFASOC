class Command:
    def __init__(self, type: str):
        self.type = type
    def type(self):
        return self.type
    def changeParamDependency(self, param, newparam):
        return
    def changeCompDependency(self, comp, newcomp):
        return
    
class Import:
    def __init__(self, line):
        self.line = line 
        self.type = "import"
        self.parseLine()
    def parseLine(self):
        words = self.line.split(" ")
        self.importFile = words[1]
    def regenCommand(self):
        return f"import {self.importFile}"

class Param(Command):
    def __init__(self, line):
        self.line = line
        self.type = "create"
        self.parseLine()
    def parseLine(self):
        words = self.line.split(" ")
        self.paramType = words[2]
        self.name = words[5]
    def regenCommand(self):
        return f"create a {self.paramType} parameter called {self.name}"
    def changeParamDependency(self, param, newparam):
        if self.name == param:
            self.name = newparam

# has parameter dependencies
class Place(Command):
    def __init__(self, line):
        self.line = line
        self.type = "place"
        self.parseLine()
    def parseLine(self):
        words = self.line.split(" ")
        self.compType = words[2]
        if self.compType == "interdigitated":
            self.compType += " "+words[3]
            self.compName = words[5]
        else:
            self.compName = words[4]
        withIndex = self.line.find(" with ")
        if withIndex > -1:
            keyValues = self.line[self.line.find(" with ")+len(" with "):]
            self.keyValues = parseKeyValues(keyValues)
        else:
            self.keyValues = None
    def changeParamDependency(self, param, newparam):
        if self.keyValues == None:
            return
        for key in self.keyValues:
            if self.keyValues[key] == param:
                self.keyValues[key] = newparam
        if "kwargs" in self.keyValues:
            for key in self.keyValues["kwargs"]:
                if self.keyValues["kwargs"][key] == param:
                    self.keyValues["kwargs"][key] = newparam
    def changeCompDependency(self, comp, newcomp):
        if self.compName == comp:
            self.compName = newcomp
    def regenCommand(self):
        string = f"place a {self.compType} called {self.compName}"
        if self.keyValues != None:
            string += " with " + regenKeyValues(self.keyValues)
        return string
    
# Has component dependencies
class Move(Command):
    def __init__(self, line):
        self.line = line
        self.type = "move"
        self.parseLine()
    def parseLine(self):
        words = self.line.split(" ")
        self.comp1 = words[1]
        self.comp2 = words[-1]
        self.moveType = " ".join(words[2:-1])
    def changeCompDependency(self, comp, newcomp):
        if self.comp1 == comp:
            self.comp1 = newcomp
        if self.comp2 == comp:
            self.comp2 = newcomp
    def regenCommand(self):
        return f"move {self.comp1} {self.moveType} {self.comp2}"

# Has component dependencies, and might have parameter dependencies
class Route(Command):
    def __init__(self, line):
        self.line = line
        self.type = "route"
        self.parseLine()
    def parseLine(self):
        words = self.line.split(" ")
        self.port1 = words[2]
        self.port2 = words[4]
        self.routeType = words[6]
        withIndex = self.line.find(" with ")
        if withIndex > -1:
            keyValues = self.line[self.line.find(" with ")+len(" with "):]
            self.keyValues = parseKeyValues(keyValues)
        else:
            self.keyValues = None
    def changeParamDependency(self, param, newparam):
        if self.keyValues == None:
            return
        for key in self.keyValues:
            if self.keyValues[key] == param:
                self.keyValues[key] = newparam
        if "kwargs" in self.keyValues:
            for key in self.keyValues["kwargs"]:
                if self.keyValues["kwargs"][key] == param:
                    self.keyValues["kwargs"][key] = newparam
    def changeCompDependency(self, comp, newcomp):
        comp1 = ""
        comp2 = ""
        if self.port1.find("_") != -1:
            comp1 = self.port1[:self.port1.find("_")]
        if self.port2.find("_") != -1:
            comp2 = self.port2[:self.port2.find("_")]
        if comp1 == comp:
            self.port1 = newcomp+self.port1[self.port1.find("_"):]
        if comp2 == comp:
            self.port2 = newcomp+self.port2[self.port2.find("_"):]
    def regenCommand(self):
        string = f"route between {self.port1} and {self.port2}"
        if self.keyValues != None:
            string += " with " + regenKeyValues(self.keyValues)
        return string

class Comment(Command):
    def __init__(self, line):
        self.line = line
        self.type = "comment"
    def regenCommand(self):
        return self.line


def parseKeyValues(line: str):
    key = ""
    value = ""
    keyToken = True
    keyValue = dict()
    kwargStart = False
    tupleStart = False
    for ch in line:
        if ch == "{":
            kwargStart = True
        elif ch == "(":
            tupleStart = True
        elif ch == "}":
            kwargStart = False
            value = parseKwarg(value)
        elif ch == ")":
            tupleStart = False
            value = parseTuple(value)
        elif ch == "=":
            keyToken = False
        elif (ch == " " or ch == ",") and (not kwargStart and not tupleStart):
            if key != "" and value != "":
                keyValue[key] = value
            keyToken = True
            key = ""
            value = ""
        else:
            if keyToken:
                key = key + ch
            else:
                value = value + ch
    keyValue[key]= value
    return keyValue

def parseKwarg(line: str):
    trimmed = line.replace(' ','')
    words = trimmed.split(",")
    kwargs = dict()
    for word in words:
        keyVal = word.split(":")
        kwargs[keyVal[0][1:-1]] = keyVal[1]
    return kwargs

def parseTuple(line: str):
    trimmed = line.replace(' ','')
    words = trimmed.split(",")
    return (words[0], words[1])

def regenKeyValues(keyValues: dict):
    keyVals = ""
    for key in keyValues:
        if key == "kwargs":
            value = regenKwargs(keyValues[key])
        elif type(keyValues[key]) == tuple:
            value = regenTuple(keyValues[key])
        else:
            value = keyValues[key]
        keyVals += f"{key}={value}, "
    keyVals = keyVals[:-2]
    return keyVals

def regenKwargs(kwargs: dict):
    kwarg = "{"
    for arg in kwargs:
        kwarg += f"\'{arg}\': {kwargs[arg]}, "
    kwarg = kwarg[:-2]
    kwarg += "}"
    return kwarg

def regenTuple(tuple):
    return f"({tuple[0]},{tuple[1]})"

class Convo:
    def __init__(self, compName):
        self.compName = compName
        self.commands = []
    def addCommand(self, command):
        self.commands.append(command)
    def changeParam(self, param, newparam):
        for command in self.commands:
            command.changeParamDependency(param, newparam)
    def changeComp(self, comp, newcomp):
        for command in self.commands:
            command.changeCompDependency(comp, newcomp)
    def unparametrize(self, param, value):
        for index in range(len(self.commands)):
            if self.commands[index].type == "create":
                if self.commands[index].name == param:
                    del self.commands[index]
                    break
        self.changeParam(param, value)

    def regen(self):
        str = self.compName + "\n"
        for command in self.commands:
            str += command.regenCommand() + "\n"
        str = str[:-1]
        return str

class ConvoParser:
    def __init__(self, filename: str):
        self.fileContents = open(filename).read()
        self.readContents()
    def readContents(self):
        commClassMap = {"import":Import, "create":Param, "place":Place, "move": Move, "route":Route}
        lines = self.fileContents.split('\n')
        self.convo = Convo(lines[0])
        for line in lines[1:]:
            commandType = line.split(" ")[0]
            if commandType in commClassMap:
                self.convo.addCommand(commClassMap[commandType](line))
            elif line[0] == "#":
                self.convo.addCommand(Comment(line))

convo = ConvoParser("syntax_data/convos/CascodeCommonSourceInterdigitated.convo").convo
convo.changeComp("CascodeCommonSource", "ccs")
convo.changeParam("width", "widthCS")
convo.unparametrize("fingers", "1")
print(convo.regen())