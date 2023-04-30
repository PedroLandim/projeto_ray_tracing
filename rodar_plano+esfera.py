from components import Scene, Camera, Vector3, Light, Sphere, Material, Plane, Triangle, RevolutionSurface
from engine import EngineRender

sphere1 = Sphere(Vector3(-5, 0, -10), 3, Material(Vector3(1, 0.2, 0.2), reflection=0.8, refraction=1.9)).transform([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])
sphere2 = Sphere(Vector3(0, 0, -15), 2, Material(Vector3(0.2, 0.8, 0.2),diffuse=0.1, transmission = 0.8, reflection=0.6))
sphere3 = Sphere(Vector3(5, 0, -20), 3, Material(Vector3(0.2, 0.2, 1), reflection=0.8, refraction=1.9))

#triangle = Triangle(Vector3(-1, 0, -20), Vector3(-1, 5, -21), Vector3(1, 2, -20), Material(Vector3(1, 0.2, 0.2),transmission=0.5, reflection=1.2))

sphere4 = Sphere(Vector3(), 1, Material(Vector3(1, 0.2, 0.2), reflection=0.8, refraction=1.9))
plane = Plane(Vector3(0, -5, 0), Vector3(0, 1, 0), Material(Vector3(0.8, 0.8, 0.8), reflection=0.5))
RevolutionSurfa = RevolutionSurface([Vector3(0,0,-24), Vector3(4,0,-24), Vector3(2,2,-24)], 5,)


light1 = Light(Vector3(0, 20, 0), Vector3(1, 1, 1))
light2 = Light(Vector3(-10, 15, -10), Vector3(0.5, 0.5, 0.5))
light3 = Light(Vector3(10, 15, -10), Vector3(0.2, 0.2, 0.8))

camera = Camera(800, 600, 50, Vector3(0, 1, 0), Vector3(0, 0, -30), Vector3(0, 0, 0))

scene = Scene(camera, [sphere1, sphere2, sphere3, plane, sphere4], [light1, light2, light3], Vector3(0.2, 0.2, 0.2), Vector3(), 2)


engine = EngineRender()
image = engine.render(scene, True)

with open("reflection79.ppm", "w") as img_file:
    image.write_ppm(img_file)
