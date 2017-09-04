import bpy
from bpy.props import *
from ... sockets.info import toListDataType
from ... events import executionCodeChanged
from ... base_types.node import AnimationNode

dataTypes = ["Object", "Scene", "Object Group", "Text Block"]

filterTypeItems = [("STARTS_WITH", "Starts With", "All Objects with names starting with"),
                   ("ENDS_WITH", "Ends With", "All Objects with names ending with")]

class FilterBlendDataListByNameNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_FilterBlendDataListByNameNode"
    bl_label = "Filter Blend Data List By Name"
    bl_width_default = 170
    dynamicLabelType = "ALWAYS"

    onlySearchTags = True
    searchTags = [("Filter {} List by Name".format(name), {"dataType" : repr(name)}) for name in dataTypes]

    def dataTypeChanged(self, context):
        self.createSockets()

    # Should be set only on node creation
    dataType = StringProperty(name = "Data Type", default = "Object",
        update = dataTypeChanged)

    filterType = EnumProperty(name = "Filter Type", default = "STARTS_WITH",
        items = filterTypeItems, update = executionCodeChanged)

    caseSensitive = BoolProperty(name = "Case Sensitive", default = False,
        update = executionCodeChanged)

    def create(self):
        self.createSockets()

    def draw(self, layout):
        layout.prop(self, "filterType", expand = True)
        layout.prop(self, "caseSensitive")

    def drawLabel(self):
        return "Filter {} List".format(self.dataType)

    def createSockets(self):
        self.inputs.clear()
        self.outputs.clear()
        listDataType = toListDataType(self.dataType)
        self.newInput(listDataType, listDataType, "sourceList")
        self.newInput("String", "Name", "name")
        self.newOutput(listDataType, listDataType, "targetList")

    def getExecutionCode(self):
        operation = "startswith" if self.filterType == "STARTS_WITH" else "endswith"

        if self.caseSensitive:
            return "targetList = [object for object in sourceList if object is not None and getattr(object, 'name', 'NONE').{}(name)]".format(operation)
        else:
            return "targetList = [object for object in sourceList if object is not None and getattr(object, 'name', 'NONE').lower().{}(name.lower())]".format(operation)
