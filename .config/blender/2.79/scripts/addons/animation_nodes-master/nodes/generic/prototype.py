import bpy
from ... base_types.node import AnimationNode

class PrototypeNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_PrototypeNode"
    bl_label = "Prototype Node"
    options = {"No Execution"}

    def draw(self, layout):
        if len(self.sockets) == 0:
            col = layout.column(align = True)
            col.label("Create sockets in the")
            col.label("advanced settings")

    def drawAdvanced(self, layout):
        row = layout.row(align = True)
        self.invokeSocketTypeChooser(row, "newInputSocket", text = "New Input")
        self.invokeSocketTypeChooser(row, "newOutputSocket", text = "New Output")

    def newInputSocket(self, dataType):
        socket = self.newInput(dataType, dataType)
        self.setupSocket(socket)

    def newOutputSocket(self, dataType):
        socket = self.newOutput(dataType, dataType)
        self.setupSocket(socket)

    def setupSocket(self, socket):
        socket.text = socket.dataType
        socket.textProps.editable = True
        socket.display.textInput = True
        socket.display.text = True
        socket.moveable = True
        socket.removeable = True
