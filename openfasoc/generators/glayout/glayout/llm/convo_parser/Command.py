from parse_utils import parseKeyValues, parseKwarg, parseTuple, regenKeyValues, regenKwargs, regenTuple

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
    
class Newline(Command):
    def __init__(self):
        self.type = "newline"
    def regenCommand(self):
        return ""
    