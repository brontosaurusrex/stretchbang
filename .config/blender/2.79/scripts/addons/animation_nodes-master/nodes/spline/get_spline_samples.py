import bpy
from ... base_types.node import AnimationNode
from . spline_evaluation_base import SplineEvaluationBase

class GetSplineSamplesNode(bpy.types.Node, AnimationNode, SplineEvaluationBase):
    bl_idname = "an_GetSplineSamplesNode"
    bl_label = "Get Spline Samples"

    def create(self):
        self.newInput("Spline", "Spline", "spline", defaultDrawType = "PROPERTY_ONLY")
        self.newInput("Integer", "Amount", "amount", value = 50)
        self.newInput("Float", "Start", "start", value = 0.0).setRange(0.0, 1.0)
        self.newInput("Float", "End", "end", value = 1.0).setRange(0.0, 1.0)
        self.newOutput("Vector List", "Positions", "positions")
        self.newOutput("Vector List", "Tangents", "tangents")

    def draw(self, layout):
        layout.prop(self, "parameterType", text = "")

    def drawAdvanced(self, layout):
        col = layout.column()
        col.active = self.parameterType == "UNIFORM"
        col.prop(self, "resolution")

    def getExecutionCode(self):
        isLinked = self.getLinkedOutputsDict()
        if not (isLinked["positions"] or isLinked["tangents"]): return []

        yield "spline.update()"
        yield "if spline.isEvaluable:"

        if self.parameterType == "UNIFORM":
            if isLinked["positions"]: yield "    positions = spline.getUniformSamples(amount, start, end, self.resolution)"
            if isLinked["tangents"]:  yield "    tangents = spline.getUniformTangentSamples(amount, start, end, self.resolution)"
        elif self.parameterType == "RESOLUTION":
            if isLinked["positions"]: yield "    positions = spline.getSamples(amount, start, end)"
            if isLinked["tangents"]:  yield "    tangents = spline.getTangentSamples(amount, start, end)"

        yield "else: positions, tangents = [], []"
