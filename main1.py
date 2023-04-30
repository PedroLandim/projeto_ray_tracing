from components import Scene, Camera, Vector3, Light, Sphere, Material, Plane, Triangle, RevolutionSurface
from engine import EngineRender


plane = Plane(Vector3(0, -5, 0), Vector3(0, 1, 0), Material(Vector3(0.8, 0.8, 0.8), reflection=0.5))
RevolutionSurfa = RevolutionSurface([Vector3(0,0,0), Vector3(1,1,0), Vector3(1,2,0), Vector3(0,3,0), Vector3(-1,2,0), Vector3(-1,1,0)], 40, Vector3(0,0,0), Vector3(0,1,0), Material(Vector3(1,0,0), reflection=0.8))


light1 = Light(Vector3(0, 20, 0), Vector3(0.8, 0.8, 0.8))
light2 = Light(Vector3(-10, 10, -10), Vector3(0.5, 0.5, 0.5))
light3 = Light(Vector3(10, 10, -10), Vector3(0.2, 0.2, 0.8))
light4 = Light(Vector3(0,0,0), Vector3(0.2, 0.2, 1))

camera = Camera(800, 600, 50, Vector3(0, 1, 0), Vector3(0, 0, -5), Vector3(0, 0, 0))

scene = Scene(camera, [plane, RevolutionSurfa], [light1, light2, light3, light4], Vector3(0.2, 0.2, 0.2), Vector3(), 1)


engine = EngineRender()
image = engine.render(scene, True)

with open("surface11.ppm", "w") as img_file:
    image.write_ppm(img_file)
