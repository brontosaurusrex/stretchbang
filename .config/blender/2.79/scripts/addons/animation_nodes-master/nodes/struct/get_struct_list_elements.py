import bpy
from bpy.props import *
from operator import itemgetter
from ... utils.layout import writeText
from ... tree_info import keepNodeState
from ... base_types.node import AnimationNode
from ... sockets.info import isBase, toListDataType
from ... events import executionCodeChanged, propertyChanged

class GetStructListElementsNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_GetStructListElementsNode"
    bl_label = "Get Struct List Elements"
    bl_width_default = 170

    makeCopies = BoolProperty(name = "Make Copies", default = True,
        description = "Copy the data before outputting it",
        update = executionCodeChanged)

    def elementDataTypeChanged(self, context):
        self.recreateOutput()

    elementKey = StringProperty(name = "Key", update = propertyChanged)
    elementDataType = StringProperty(name = "Data Type", default = "Integer",
        update = elementDataTypeChanged)

    errorMessage = StringProperty()

    def create(self):
        self.newInput("Struct List", "Struct List", "structList")
        self.elementDataType = "Integer"

    def draw(self, layout):
        col = layout.column()
        col.prop(self, "elementKey")
        self.invokeSocketTypeChooser(col, "assignType",
            text = self.elementDataType, icon = "TRIA_RIGHT")

        if self.errorMessage != "":
            writeText(layout, self.errorMessage, icon = "ERROR")

    def assignType(self, dataType):
        self.elementDataType = dataType

    @keepNodeState
    def recreateOutput(self):
        self.outputs.clear()
        if isBase(self.elementDataType):
            self.newOutput(toListDataType(self.elementDataType), "Data")
        else:
            self.newOutput("Generic List", "Data")

    def execute(self, structList):
        key = (self.elementDataType, self.elementKey)
        try:
            self.errorMessage = ""
            return [struct[key] for struct in structList]
        except:
            self.errorMessage = "The key does not exist in all structs"
            return []
