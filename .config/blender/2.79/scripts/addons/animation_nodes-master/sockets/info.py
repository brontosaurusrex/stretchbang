import bpy
from collections import defaultdict
from .. utils.enum_items import enumItemsFromList

class SocketInfo:
    def __init__(self):
        self.reset()

    def reset(self):
        self.idNames = set()
        self.dataTypes = set()

        self.classByType = dict()
        self.typeConversion = dict()

        self.baseIdName = dict()
        self.listIdName = dict()
        self.baseDataType = dict()
        self.listDataType = dict()

        self.baseDataTypes = set()
        self.listDataTypes = set()

        self.copyFunctionByType = dict()

    def update(self, socketClasses):
        self.reset()

        # create lookup tables first
        for socket in socketClasses:
            self.insertSocket(socket)

        # then insert the socket connections
        for socket in socketClasses:
            if hasattr(socket, "baseDataType"):
                self.insertSocketConnection(socket.baseDataType, socket.dataType)

    def insertSocket(self, socketClass):
        idName = socketClass.bl_idname
        dataType = socketClass.dataType

        self.idNames.add(idName)
        self.dataTypes.add(dataType)

        self.classByType[idName] = socketClass
        self.classByType[dataType] = socketClass

        self.typeConversion[idName] = dataType
        self.typeConversion[dataType] = idName

        if socketClass.isCopyable():
            copyFunction = eval("lambda value: " + socketClass.getCopyExpression())
        else:
            copyFunction = lambda value: value

        self.copyFunctionByType[idName] = copyFunction
        self.copyFunctionByType[dataType] = copyFunction

    def insertSocketConnection(self, baseDataType, listDataType):
        baseIdName = self.typeConversion[baseDataType]
        listIdName = self.typeConversion[listDataType]

        self.baseIdName[listIdName] = baseIdName
        self.baseIdName[listDataType] = baseIdName
        self.listIdName[baseIdName] = listIdName
        self.listIdName[baseDataType] = listIdName

        self.baseDataType[listIdName] = baseDataType
        self.baseDataType[listDataType] = baseDataType
        self.listDataType[baseIdName] = listDataType
        self.listDataType[baseDataType] = listDataType

        self.baseDataTypes.add(baseDataType)
        self.listDataTypes.add(listDataType)


_socketInfo = SocketInfo()

def updateSocketInfo():
    socketClasses = getSocketClasses()
    _socketInfo.update(socketClasses)

def getSocketClasses():
    from .. base_types.socket import AnimationNodeSocket
    return AnimationNodeSocket.__subclasses__()


def returnOnFailure(returnValue):
    def failHandlingDecorator(function):
        def wrapper(*args, **kwargs):
            try: return function(*args, **kwargs)
            except: return returnValue
        return wrapper
    return failHandlingDecorator

# Check if list or base socket exists
def isList(input):
    return input in _socketInfo.baseIdName

def isBase(input):
    return input in _socketInfo.listIdName

# to Base
@returnOnFailure(None)
def toBaseIdName(input):
    return _socketInfo.baseIdName[input]

@returnOnFailure(None)
def toBaseDataType(input):
    return _socketInfo.baseDataType[input]

# to List
@returnOnFailure(None)
def toListIdName(input):
    return _socketInfo.listIdName[input]

@returnOnFailure(None)
def toListDataType(input):
    return _socketInfo.listDataType[input]

# Data Type <-> Id Name
@returnOnFailure(None)
def toIdName(input):
    if isIdName(input): return input
    return _socketInfo.typeConversion[input]

@returnOnFailure(None)
def toDataType(input):
    if isIdName(input):
        return _socketInfo.typeConversion[input]
    return input

def isIdName(name):
    return name in _socketInfo.idNames


@returnOnFailure(False)
def isComparable(input):
    return _socketInfo.classByType[input].comparable

@returnOnFailure(False)
def isCopyable(input):
    return _socketInfo.classByType[input].isCopyable()

def getCopyExpression(input):
    return _socketInfo.classByType[input].getCopyExpression()

def getCopyFunction(input):
    return _socketInfo.copyFunctionByType[input]


def getListDataTypeItemsCallback(self, context):
    return getListDataTypeItems()

def getBaseDataTypeItemsCallback(self, context):
    return getBaseDataTypeItems()

def getListDataTypeItems():
    return enumItemsFromList(getListDataTypes())

def getBaseDataTypeItems():
    return enumItemsFromList(getBaseDataTypes())

def getDataTypeItems(skipInternalTypes = False):
    return enumItemsFromList(getDataTypes(skipInternalTypes))

def getListDataTypes():
    return list(_socketInfo.listDataTypes)

def getBaseDataTypes():
    return list(_socketInfo.baseDataTypes)

def getDataTypes(skipInternalTypes = False):
    internalTypes = {"Node Control"}
    if skipInternalTypes:
        return [dataType for dataType in _socketInfo.dataTypes if dataType not in internalTypes]
    else:
        return list(_socketInfo.dataTypes)
