from components import Scene, Camera, Vector3, Light, Sphere, Material, Plane, Triangle, TriangleMesh
from engine import EngineRender
import random

plane = Plane(Vector3(0, -2, 0), Vector3(0, 1, 0), Material(Vector3(0, 0, 1)))

light1 = Light(Vector3(0, 20, 5), Vector3(1, 1, 1))
light2 = Light(Vector3(2, 15, 10), Vector3(0, 1, 0))
light3 = Light(Vector3(5, 10, -7), Vector3(0, 0, 1))

camera = Camera(600, 400, 10, Vector3(0, 1, 0), Vector3(5, 10, -8), Vector3(0, 0, 0))


scene = Scene(camera, [plane], [light1, light2, light3], Vector3(1, 200/255, 200/255), Vector3())

engine = EngineRender()
image = engine.render(scene, True)

with open("plane.ppm", "w") as img_file:
    image.write_ppm(img_file)
