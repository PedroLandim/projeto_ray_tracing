from components import Scene, Camera, Vector3, Light, Sphere, Material, Plane, Triangle, TriangleMesh
from engine import EngineRender

sphere1 = Sphere(Vector3(0, 1, 0), 2, Material(Vector3(1, 0, 0), reflection=0.5, refraction=1.2))
sphere2 = Sphere(Vector3(-3, 3, -5), 1.5, Material(Vector3(0, 0, 1), reflection=0.2, refraction=1.5))
plane = Plane(Vector3(0, -2, 0), Vector3(0, 1, 0), Material(Vector3(0, 0, 1), reflection=0.1))
triangle = Triangle(Vector3(3, 0, -5), Vector3(3, 5, -5), Vector3(5, 0, -5), Material(Vector3(0, 1, 0), reflection=0.3))
vertices = [    Vector3(1, 1, 1),    Vector3(1, 1, 0),    Vector3(1, 0, 0),    Vector3(1, 0, 1),    Vector3(0, 0, 1),    Vector3(0, 0, 0),    Vector3(0, 1, 0),    Vector3(0, 1, 1)]

triangles = [    (1, 4, 2),    (2, 4, 3),    (3, 4, 6),    (4, 5, 6),    (5, 7, 6),    (6, 7, 7)]

malha = TriangleMesh(vertices, triangles, Material(Vector3(200/255, 10/255, 150/255), reflection=0.4))

light1 = Light(Vector3(0, 20, 5), Vector3(1, 1, 1))
light2 = Light(Vector3(2, 15, 10), Vector3(0, 1, 0))
light3 = Light(Vector3(5, 10, -7), Vector3(0, 0, 1))

camera = Camera(600, 400, 10, Vector3(0, 1, 0), Vector3(5, 10, -8), Vector3(0, 0, 0))
scene = Scene(camera, [sphere1, sphere2, plane, triangle, malha], [light1, light2, light3], Vector3(1, 200/255, 200/255), Vector3())
engine = EngineRender()
image = engine.render(scene, True)

with open("teste1.ppm", "w") as img_file:
    image.write_ppm(img_file)
