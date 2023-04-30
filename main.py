from components import Scene, Camera, Vector3, Light, Sphere, Material, Plane, Triangle, RevolutionSurface
from engine import EngineRender


plane = Plane(Vector3(0, -5, 0), Vector3(0, 1, 0), Material(Vector3(0.8, 0.8, 0.8), reflection=0.5))
RevolutionSurfa = RevolutionSurface([Vector3(-2,0,0), Vector3(0,2,0), Vector3(2,0,0), Vector3(0,-2,0)], 50, Vector3(0,0,0), Vector3(0,1,0), Material(Vector3(0.5,0.5,0.5), reflection=0.5, reflection_color=Vector3(0.3,0.5,1)))


light1 = Light(Vector3(-10, 10, 10), Vector3(1, 1, 1))
light2 = Light(Vector3(10, 5, -10), Vector3(0.5, 0.5, 0.5))

camera = Camera(800, 600, 50, Vector3(0, 1, 0), Vector3(0, 0, -10), Vector3(0, 0, 0))

scene = Scene(camera, [plane, RevolutionSurfa], [light1, light2], Vector3(0.2, 0.2, 0.2), Vector3(), 2)


engine = EngineRender()
image = engine.render(scene, True)

with open("superficie_refletindo.ppm", "w") as img_file:
    image.write_ppm(img_file)
