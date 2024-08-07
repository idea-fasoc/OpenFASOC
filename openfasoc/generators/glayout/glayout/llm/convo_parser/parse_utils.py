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