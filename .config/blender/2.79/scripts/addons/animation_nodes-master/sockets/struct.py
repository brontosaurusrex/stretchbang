import bpy
from .. data_structures.struct import Struct
from .. base_types.socket import AnimationNodeSocket

class StructSocket(bpy.types.NodeSocket, AnimationNodeSocket):
    bl_idname = "an_StructSocket"
    bl_label = "Struct Socket"
    dataType = "Struct"
    allowedInputTypes = ["Struct"]
    drawColor = (0.3, 0.3, 0.3, 1)
    storable = True
    comparable = False

    @classmethod
    def getDefaultValue(cls):
        return Struct()

    @classmethod
    def getDefaultValueCode(cls):
        return "animation_nodes.data_structures.struct.Struct()"

    @classmethod
    def getCopyExpression(cls):
        return "value.copyValues()"

    @classmethod
    def correctValue(cls, value):
        if isinstance(value, Struct) or value is None:
            return value, 0
        return cls.getDefaultValue(), 2


class StructListSocket(bpy.types.NodeSocket, AnimationNodeSocket):
    bl_idname = "an_StructListSocket"
    bl_label = "Struct List Socket"
    dataType = "Struct List"
    baseDataType = "Struct"
    allowedInputTypes = ["Struct List"]
    drawColor = (0.3, 0.3, 0.3, 0.5)
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
        return "[element.copyValues() for element in value]"

    @classmethod
    def correctValue(cls, value):
        if isinstance(value, list):
            if all(isinstance(element, Struct) or element is None for element in value):
                return value, 0
        return cls.getDefaultValue(), 2
