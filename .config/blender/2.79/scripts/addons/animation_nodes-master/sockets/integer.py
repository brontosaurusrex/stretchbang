import bpy
from bpy.props import *
from .. events import propertyChanged
from .. base_types.socket import AnimationNodeSocket

def getValue(self):
    return min(max(self.minValue, self.get("value", 0)), self.maxValue)
def setValue(self, value):
    self["value"] = min(max(self.minValue, value), self.maxValue)

class IntegerSocket(bpy.types.NodeSocket, AnimationNodeSocket):
    bl_idname = "an_IntegerSocket"
    bl_label = "Integer Socket"
    dataType = "Integer"
    allowedInputTypes = ["Integer"]
    drawColor = (0.3, 0.4, 1.0, 1.0)
    comparable = True
    storable = True

    value = IntProperty(default = 0,
        set = setValue, get = getValue,
        update = propertyChanged)

    minValue = IntProperty(default = -2**31)
    maxValue = IntProperty(default = 2**31-1)

    def drawProperty(self, layout, text, node):
        layout.prop(self, "value", text = text)

    def getValue(self):
        return self.value

    def setProperty(self, data):
        self.value = data

    def getProperty(self):
        return self.value

    def setRange(self, min, max):
        self.minValue = min
        self.maxValue = max

    def shouldBeFloatSocket(self):
        targets = self.dataTargets
        if len(targets) == 0: return True

        for socket in targets:
            if socket.dataType == "Float": return True

        return False

    @classmethod
    def getDefaultValue(cls):
        return 0

    @classmethod
    def correctValue(cls, value):
        if isinstance(value, int):
            return value, 0
        else:
            try: return int(value), 1
            except: return cls.getDefaultValue(), 2


class IntegerListSocket(bpy.types.NodeSocket, AnimationNodeSocket):
    bl_idname = "an_IntegerListSocket"
    bl_label = "Integer List Socket"
    dataType = "Integer List"
    baseDataType = "Integer"
    allowedInputTypes = ["Integer List"]
    drawColor = (0.3, 0.4, 1.0, 0.5)
    storable = True
    comparable = False

    @classmethod
    def getDefaultValue(cls):
        return []

    @classmethod
    def getDefaultValueCode(cls):
        return "[]"

    @classmethod
    def getCopyExpression(cls):
        return "value[:]"

    @classmethod
    def correctValue(cls, value):
        if isinstance(value, list):
            if all(isinstance(element, int) for element in value):
                return value, 0
        try: return [int(element) for element in value], 1
        except: return cls.getDefaultValue(), 2
