import bpy
from bpy.props import *
from math import radians
from mathutils import Euler
from ... events import propertyChanged
from ... base_types.node import AnimationNode
from ... algorithms.perlin_noise import perlinNoise

class EulerWiggleNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_EulerWiggleNode"
    bl_label = "Euler Wiggle"

    nodeSeed = IntProperty(update = propertyChanged)

    def create(self):
        self.newInput("Float", "Seed", "seed")
        self.newInput("Float", "Evolution", "evolution")
        self.newInput("Float", "Speed", "speed", value = 1, minValue = 0)
        self.newInput("Euler", "Amplitude", "amplitude", value = [radians(30), radians(30), radians(30)])
        self.newInput("Integer", "Octaves", "octaves", value = 2)
        self.newInput("Float", "Persistance", "persistance", value = 0.3)
        self.newOutput("Euler", "Euler", "euler")

    def draw(self, layout):
        layout.prop(self, "nodeSeed", text = "Node Seed")

    def execute(self, seed, evolution, speed, amplitude, octaves, persistance):
        euler = Euler()
        evolution = evolution * max(speed, 0) / 20 + 2541 * seed + 823 * self.nodeSeed
        euler[0] = perlinNoise(evolution, persistance, octaves) * amplitude[0]
        evolution += 79
        euler[1] = perlinNoise(evolution, persistance, octaves) * amplitude[1]
        evolution += 263
        euler[2] = perlinNoise(evolution, persistance, octaves) * amplitude[2]
        return euler
