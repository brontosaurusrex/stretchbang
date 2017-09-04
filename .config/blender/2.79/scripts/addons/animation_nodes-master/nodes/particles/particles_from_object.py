import bpy
from ... base_types.node import AnimationNode

class ParticlesFromObjectNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_ParticlesFromObjectNode"
    bl_label = "Particles from Object"

    def create(self):
        self.newInput("Object", "Object", "object", defaultDrawType = "PROPERTY_ONLY")
        self.newOutput("Particle List", "Particles", "particles")

    def execute(self, object):
        if object is None: return []

        particles = []
        for system in object.particle_systems:
            particles.extend(system.particles)
        return particles
