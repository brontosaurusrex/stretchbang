import bpy
from bpy.props import *
from ... base_types.node import AnimationNode
from ... events import executionCodeChanged
from ... sockets.info import toIdName
from ... tree_info import keepNodeLinks

compare_types = ["A = B", "A != B", "A < B", "A <= B", "A > B", "A >= B", "A is B","A is None"]
compare_types_items = [(t, t, "") for t in compare_types]

numericLabelTypes = ["Integer", "Float"]

class CompareNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_CompareNode"
    bl_label = "Compare"
    dynamicLabelType = "HIDDEN_ONLY"

    def assignedTypeChanged(self, context):
        self.generateSockets()
    
    def compareTypeChanged(self, context):
        self.generateSockets()
        self.executionCodeChanged(self, context)
    
    assignedType = StringProperty(update = assignedTypeChanged)
    compareType = EnumProperty(name = "Compare Type", items = compare_types_items, update = compareTypeChanged)

    def create(self):
        self.assignedType = "Float"
        self.newOutput("an_BooleanSocket", "Result", "result")

    def draw(self, layout):
        layout.prop(self, "compareType", text = "Type")

    def drawLabel(self):
        label = self.compareType
        if self.assignedType in numericLabelTypes:
            if getattr(self.socketA, "isUnlinked", False):
                label = label.replace("A", str(round(self.socketA.value, 4)))
            if getattr(self.socketB, "isUnlinked", False):
                label = label.replace("B", str(round(self.socketB.value, 4)))
        return label

    def drawAdvanced(self, layout):
        self.invokeSocketTypeChooser(layout, "assignType",
            text = "Change Type", icon = "TRIA_RIGHT")

    def getExecutionCode(self):
        type = self.compareType
        if type == "A = B":     return "result = a == b"
        if type == "A != B":    return "result = a != b"
        if type == "A < B":	    return "try: result = a < b \nexcept: result = False"
        if type == "A <= B":    return "try: result = a <= b \nexcept: result = False"
        if type == "A > B":	    return "try: result = a > b \nexcept: result = False"
        if type == "A >= B":    return "try: result = a >= b \nexcept: result = False"
        if type == "A is B":    return "result = a is b"
        if type == "A is None": return "result = a is None"
        return "result = False"

    def edit(self):
        dataType = self.getWantedDataType()
        self.assignType(dataType)

    def getWantedDataType(self):
        for input in self.inputs:
            if input.dataOrigin is not None:
                return input.dataType
        return self.inputs[0].dataType

    def assignType(self, dataType):
        if self.assignedType == dataType: return
        self.assignedType = dataType

    @keepNodeLinks
    def generateSockets(self):
        self.inputs.clear()
        self.newInput(self.assignedType, "A", "a")
        if self.compareType != "A is None":
            self.newInput(self.assignedType, "B", "b")

    @property
    def socketA(self):
        return self.inputs.get("A")

    @property
    def socketB(self):
        return self.inputs.get("B")
