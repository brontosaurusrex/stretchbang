import bpy
from bpy.props import *
from ... tree_info import keepNodeState
from ... events import executionCodeChanged
from ... base_types.node import AnimationNode
from ... data_structures.splines.bezier_spline import BezierSpline
from ... data_structures.splines.from_blender import createSplinesFromBlenderObject, createSplineFromBlenderSpline

importTypeItems = [
    ("SINGLE", "Single", "Only load one spline from the object", "", 0),
    ("ALL", "All", "Load all splines from the object", "", 1) ]

class SplinesFromObjectNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_SplinesFromObjectNode"
    bl_label = "Splines from Object"

    def importTypeChanged(self, context):
        self.recreateSockets()

    useWorldSpace = BoolProperty(
        name = "Use World Space",
        description = "Use the position in global space",
        default = True, update = executionCodeChanged)

    importType = EnumProperty(name = "Import Type", default = "ALL",
        items = importTypeItems, update = importTypeChanged)

    errorMessage = StringProperty()

    def create(self):
        self.recreateSockets()

    def draw(self, layout):
        layout.prop(self, "useWorldSpace")

        if self.errorMessage != "":
            layout.label(self.errorMessage, icon = "ERROR")

    def drawAdvanced(self, layout):
        layout.prop(self, "importType")

    def getExecutionCode(self):
        yield "self.errorMessage = ''"
        if self.importType == "SINGLE":
            yield "spline = self.getSingleSpline(object, index)"
        elif self.importType == "ALL":
            yield "splines = self.getAllSplines(object)"

    def getSingleSpline(self, object, index):
        if object is None: return BezierSpline()
        if object.type != "CURVE":
            self.errorMessage = "Not a curve object"
            return BezierSpline()

        bSplines = object.data.splines
        if 0 <= index < len(bSplines):
            bSpline = bSplines[index]
            if bSpline.type in ("POLY", "BEZIER"):
                spline = createSplineFromBlenderSpline(bSpline)
                if self.useWorldSpace: spline.transform(object.matrix_world)
                return spline
            else:
                self.errorMessage = "Spline type not supported: " + bSpline.type
                return BezierSpline()
        else:
            self.errorMessage = "Index out of range"
            return BezierSpline()

    def getAllSplines(self, object):
        splines = createSplinesFromBlenderObject(object)
        if self.useWorldSpace:
            for spline in splines:
                spline.transform(object.matrix_world)
        return splines

    @keepNodeState
    def recreateSockets(self):
        self.inputs.clear()
        self.outputs.clear()

        self.newInput("Object", "Object", "object", defaultDrawType = "PROPERTY_ONLY")
        if self.importType == "SINGLE":
            self.newInput("Integer", "Index", "index", minValue = 0)
            self.newOutput("Spline", "Spline", "spline")
        else:
            self.newOutput("Spline List", "Splines", "splines")
