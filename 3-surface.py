from components import Scene, Camera, Vector3, Light, Material, Plane, RevolutionSurface
from engine import EngineRender

# Perfil da elipsoide
profile = [
    Vector3(2, 0, 0),
    Vector3(2, 1, 0),
    Vector3(1.5, 1.5, 0),
    Vector3(1, 2, 0),
    Vector3(0, 2, 0)
]

resolution = 50
point = Vector3(0, 0, 0)
vector = Vector3(0, 1, 0)
material = Material(Vector3(1, 0.8, 0.5), reflection=0.3)

# Criando a superfície de revolução com o perfil da elipsoide
surface = RevolutionSurface(profile + [-p for p in profile[::-1]], resolution, point, vector, material)

plane = Plane(Vector3(0, -5, 0), Vector3(0, 1, 0), Material(Vector3(0.8, 0.8, 0.8), reflection=0))

light1 = Light(Vector3(0, 20, 0), Vector3(1, 1, 1))
light2 = Light(Vector3(-10, 15, -10), Vector3(0.5, 0.5, 0.5))
light3 = Light(Vector3(10, 15, -10), Vector3(0.2, 0.2, 0.8))

camera = Camera(800, 600, 50, Vector3(0, 1, 0), Vector3(4, 0, -10), Vector3(0, 0, 0))


scene = Scene(camera, [plane, surface], [light1, light2, light3], Vector3(0.2, 0.2, 0.2), Vector3(), 2)

engine = EngineRender() 
image = engine.render(scene, True)

with open("elipsoid.ppm", "w") as img_file:
    image.write_ppm(img_file)
