import bpy
import textwrap
from collections import defaultdict
from .. utils.timing import prettyTime
from .. graphics.text_box import TextBox
from .. utils.operators import makeOperator
from .. utils.blender_ui import iterNodeCornerLocations

class NodeMeasurements:
    __slots__ = ("totalTime", "calls")

    def __init__(self):
        self.totalTime = 0
        self.calls = 0

    @property
    def averageTime(self):
        return self.totalTime / max(self.calls, 1)

    def __repr__(self):
        return textwrap.dedent("""\
            Average: {}
            Total: {}
            Calls: {:,d}\
            """.format(prettyTime(self.averageTime),
                       prettyTime(self.totalTime),
                       self.calls))

measurementsByNodeIdentifier = defaultdict(NodeMeasurements)

@makeOperator("an.reset_measurements", "Reset Measurements", redraw = True)
def resetMeasurements():
    measurementsByNodeIdentifier.clear()

def getMeasurementsDict():
    return measurementsByNodeIdentifier

def getAverageExecutionTime(node):
    return measurementsByNodeIdentifier[node.identifier].averageTime

def drawMeasurementResults():
    tree = bpy.context.space_data.edit_tree
    if tree is None: return
    if tree.bl_idname != "an_AnimationNodeTree": return

    nodes = tree.nodes
    region = bpy.context.region
    leftCorners = iterNodeCornerLocations(nodes, region, horizontal = "LEFT")
    rightCorners = iterNodeCornerLocations(nodes, region, horizontal = "RIGHT")

    for node, leftBottom, rightBottom in zip(nodes, leftCorners, rightCorners):
        if node.isAnimationNode and not node.hide:
            drawMeasurementResultForNode(node, leftBottom, rightBottom)

def drawMeasurementResultForNode(node, leftBottom, rightBottom):
    result = measurementsByNodeIdentifier[node.identifier]
    if result.calls == 0: text = "Not Measured"
    else: text = str(result)

    width = rightBottom.x - leftBottom.x

    textBox = TextBox(text, leftBottom, width,
                      fontSize = width / node.dimensions.x * 11)
    textBox.padding = 3
    textBox.draw()
