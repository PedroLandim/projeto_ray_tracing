from __future__ import annotations
from components import Light, Camera, Object3D, Vector3

class Scene:
    def __init__(
            self, camera: Camera, objects: list[Object3D], 
            lights: list[Light], ambient_light: Vector3 = Vector3(1,1,1),
            background_color: Vector3 = Vector3(), max_depth: float = 0):
        
        self.camera = camera
        self.objects = objects
        self.lights = lights
        self.ambient_light = ambient_light
        self.background_color = background_color
        self.max_depth = max_depth
        self.width = camera.hr
        self.height = camera.vr
        
        