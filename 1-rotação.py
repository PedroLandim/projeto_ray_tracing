from components import Scene, Camera, Vector3, Light, Sphere, Material, Plane, Triangle, TriangleMesh
from engine import EngineRender

sphere1 = Sphere(Vector3(-10, 0, -10), 3, Material(Vector3(1, 0.2, 0.2), reflection=0, refraction=1.9))
sphere2 = Sphere(Vector3(0, 5, -15), 2, Material(Vector3(0.2, 0.8, 0.2), reflection=0, refraction=1.9))
sphere3 = Sphere(Vector3(10, 0, -20), 3, Material(Vector3(0.2, 0.2, 1), reflection=0, refraction=1.9)).rotate(Vector3(0, 0, -20), Vector3(0,0,1), 90)

triangle = Triangle(Vector3(-1, 3, -20), Vector3(-1, 0, -20), Vector3(1, 0, -20), Material(Vector3(1, 1, 0), reflection=0)).rotate(Vector3(-1/3, 1, -20), Vector3(0,0,1), 90)

plane = Plane(Vector3(0, -5, 0), Vector3(0, 1, 0), Material(Vector3(0.8, 0.8, 0.8), reflection=0))

light1 = Light(Vector3(0, 20, 0), Vector3(1, 1, 1))
light2 = Light(Vector3(-10, 15, -10), Vector3(0.5, 0.5, 0.5))
light3 = Light(Vector3(10, 15, -10), Vector3(0.2, 0.2, 0.8))

camera = Camera(900, 900, 60, Vector3(0, 1, 0), Vector3(4, 0, -40), Vector3(0, 0, 0))

mesh_vertices = [    
                Vector3(2, 2, -10),#0    
                Vector3(2, 0, -10),#1      
                Vector3(6, 0, -10),#2     
                Vector3(6, 2, -10),#4
] 

mesh_triangles = [(0, 1, 2), (2, 3, 0)]

mesh_material = Material(Vector3(1, 0.2, 0.2), reflection=0)

mesh = TriangleMesh(mesh_vertices, mesh_triangles, mesh_material).rotate(Vector3(4, 1, -10), Vector3(0,0,1), 90)


scene = Scene(camera, [plane, sphere1, sphere2, sphere3, triangle, mesh], [light1, light2, light3], Vector3(0.2, 0.2, 0.2), Vector3(), 1)


engine = EngineRender()
image = engine.render(scene, True)

with open("rotateteste.ppm", "w") as img_file:
    image.write_ppm(img_file)
