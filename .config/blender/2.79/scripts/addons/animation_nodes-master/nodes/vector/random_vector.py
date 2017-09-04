import bpy
import random
from bpy.props import *
from ... events import propertyChanged
from ... base_types.node import AnimationNode

class RandomVectorNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_RandomVectorNode"
    bl_label = "Random Vector"

    nodeSeed = IntProperty(name = "Node Seed", update = propertyChanged, max = 1000, min = 0)

    def create(self):
        self.newInput("Integer", "Seed", "seed")
        self.newInput("Float", "Scale", "scale", value = 2.0)
        self.newOutput("Vector", "Vector", "randomVector")

    def draw(self, layout):
        layout.prop(self, "nodeSeed")

    def getExecutionCode(self):
        yield "startSeed = (seed + self.nodeSeed * 1000) % (len(random_number_cache) - 3)"
        yield ("randomVector = scale * Vector((random_number_cache[startSeed]     - 0.5, "
                                              "random_number_cache[startSeed + 1] - 0.5, "
                                              "random_number_cache[startSeed + 2] - 0.5))")

    def duplicate(self, sourceNode):
        self.nodeSeed = int(random.random() * 100)
