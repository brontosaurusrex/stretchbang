import bpy
from bpy.props import *
from ... sockets.info import toIdName
from ... tree_info import keepNodeState
from ... base_types.node import AnimationNode

class SwitchNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_SwitchNode"
    bl_label = "Switch"

    def assignedTypeChanged(self, context):
        self.generateSockets()

    assignedType = StringProperty(update = assignedTypeChanged)

    def create(self):
        self.assignedType = "Float"

    def drawAdvanced(self, layout):
        self.invokeSocketTypeChooser(layout, "assignType",
            text = "Change Type", icon = "TRIA_RIGHT")

    def edit(self):
        dataType = self.getWantedDataType()
        self.assignType(dataType)

    def getWantedDataType(self):
        for socket in (self.inputs[1], self.inputs[2], self.outputs[0], self.outputs[1]):
            dataOrigin = socket.dataOrigin
            if dataOrigin is not None: return dataOrigin.dataType
        return self.inputs[1].dataType

    def assignType(self, dataType):
        if dataType == self.assignedType: return
        self.assignedType = dataType

    def getExecutionCode(self):
        isLinked = self.getLinkedOutputsDict()
        if isLinked["output"]: yield "output = ifTrue if condition else ifFalse"
        if isLinked["other"]:  yield "other = ifFalse if condition else ifTrue"

    @keepNodeState
    def generateSockets(self):
        self.inputs.clear()
        self.outputs.clear()

        self.newInput("an_BooleanSocket", "Condition", "condition")
        self.newInput(self.assignedType, "If True", "ifTrue")
        self.newInput(self.assignedType, "If False", "ifFalse")
        self.newOutput(self.assignedType, "Output", "output")
        self.newOutput(self.assignedType, "Other", "other").hide = True
