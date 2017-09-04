import bpy
from bpy.props import *
from ... events import executionCodeChanged
from ... base_types.node import AnimationNode

outputItems = [	("BASIS", "Basis", "", "NONE", 0),
                ("LOCAL", "Local", "", "NONE", 1),
                ("PARENT INVERSE", "Parent Inverse", "", "NONE", 2),
                ("WORLD", "World", "", "NONE", 3) ]

class ObjectMatrixOutputNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_ObjectMatrixOutputNode"
    bl_label = "Object Matrix Output"

    outputType = EnumProperty(items = outputItems, update = executionCodeChanged, default = "WORLD")

    def create(self):
        self.newInput("Object", "Object", "object", defaultDrawType = "PROPERTY_ONLY")
        self.newInput("Matrix", "Matrix", "matrix")
        self.newOutput("Object", "Object", "object")

    def draw(self, layout):
        layout.prop(self, "outputType", text = "Type")

    def getExecutionCode(self):
        t = self.outputType
        yield "if object is not None:"
        if t == "BASIS":          yield "    object.matrix_basis = matrix"
        if t == "LOCAL":          yield "    object.matrix_local = matrix"
        if t == "PARENT INVERSE": yield "    object.matrix_parent_inverse = matrix"
        if t == "WORLD":          yield "    object.matrix_world = matrix"

    def getBakeCode(self):
        yield "if object is not None:"
        yield "    object.keyframe_insert('location')"
        yield "    object.keyframe_insert('rotation_euler')"
        yield "    object.keyframe_insert('scale')"
