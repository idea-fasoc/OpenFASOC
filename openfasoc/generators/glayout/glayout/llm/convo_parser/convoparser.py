from Command import Import, Param, Place, Move, Route, Comment, Newline
from validate_synthetic_data import run_all_tests, instantiate_convo 
from glayout.flow.pdk.mappedpdk import MappedPDK
import tempfile

class Convo:
    def __init__(self, compName):
        self.compName = compName
        self.commands = []
        self.parameters = dict()
        self.components = dict()

    def addParam(self, param, type, line):
        self.parameters[param]= (type, line)

    def addComp(self, comp, type, line):
        self.components[comp] = (type, line)

    def addCommand(self, command):
        self.commands.append(command)

    def changeParam(self, param, newparam):
        for command in self.commands:
            command.changeParamDependency(param, newparam)
        old = self.parameters[param]
        del self.parameters[param]
        self.parameters[newparam] = old

    def changeComp(self, comp, newcomp):
        for command in self.commands:
            command.changeCompDependency(comp, newcomp)
        old = self.components[comp]
        del self.components[comp]
        self.parameters[newcomp] = old

    def unparametrize(self, param, value):
        del self.commands[self.parameters[param][1]]
        self.changeParam(param, value)
        del self.parameters[param]

    def regen(self):
        str = self.compName + "\n"
        for command in self.commands:
            str += command.regenCommand() + "\n"
        str = str[:-2]
        return str

    def runDRC(self, pdk: MappedPDK):
        temp = tempfile.NamedTemporaryFile()
        temp.write(self.regen())
        component = instantiate_convo(pdk, temp.name, return_component=True)
        pdk.drc_magic(component, component.name)
    
    def run_LVSandPEX(self, pdk, netlist):
        temp = tempfile.NamedTemporaryFile()
        temp.write(self.regen())
        component = instantiate_convo(pdk, temp.name, return_component=True)
        pdk.lvs_netgen(component, component.name, copy_intermediate_files=True, netlist=netlist)

class ConvoParser:
    def __init__(self, filename: str):
        self.fileContents = open(filename).read()
        self.readContents()

    def readContents(self):
        commClassMap = {"import":Import, "create":Param, "place":Place, "move": Move, "route":Route}
        lines = self.fileContents.split('\n')
        self.convo = Convo(lines[0])

        lineIndex = 0
        for line in lines[1:]:
            commandType = line.split(" ")[0]

            if commandType in commClassMap:
                command = commClassMap[commandType](line)
                self.convo.addCommand(command)
                if commandType == "create":
                    self.convo.addParam(command.name, command.paramType, lineIndex)
                elif commandType == "place":
                    self.convo.addComp(command.compName, command.compType, lineIndex)

            elif len(line) > 0 and line[0] == "#":
                self.convo.addCommand(Comment(line))

            elif line == "":
                self.convo.addCommand(Newline())

            lineIndex += 1
