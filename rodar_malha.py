from components import Scene, Camera, Vector3, Light, Sphere, Material, Plane, Triangle, TriangleMesh
from engine import EngineRender


vertices = [
    Vector3(0.0, 49.999996, 200.0), #0
    Vector3(0, -50.000008, 200), #1
    Vector3(86.602539, -49.999996, 49.999992), #2
    Vector3(86.602539,
                    50.0,
                    49.999992), #3
    Vector3(-86.602539,
                    -49.999996,
                    49.999992), #4
    Vector3(-86.602539,
                    50.0,
                    49.999992) #5
]

triangles = [
    (0, 1, 2),
    (0, 2, 3),
    (2, 1, 3),
    (3, 4, 5),
    (2, 1, 4),
    (5, 4, 1),
    (5, 1, 0),
    (0, 3, 5)
]

malha = TriangleMesh(vertices, triangles, Material(Vector3(200/255, 10/255, 150/255), ambient=0.5))

light1 = Light(Vector3(700, 800, 600), Vector3(50/255, 1, 1))
light2 = Light(Vector3(300, 900, 800), Vector3(1, 50/255, 1))
light3 = Light(Vector3(1000, 350, 800), Vector3(1, 1, 50/255))

camera = Camera(640, 480, 100, Vector3(0, 0, 1), Vector3(700, 450, 800), Vector3(0, 0, 0))

scene = Scene(camera, [malha], [light1, light2, light3], Vector3(1, 200/255, 200/255), Vector3())
engine = EngineRender()
image = engine.render(scene, True)

with open("teste-de-malha.ppm", "w") as img_file:
    image.write_ppm(img_file)
