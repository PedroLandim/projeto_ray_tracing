from components import Vector3

class Material:
    def __init__(
            self, color=Vector3(1,1,1), diffuse=1.0, specular=1.0, ambient=0.05,
            reflection=0.5, transmission=0.0, phong=50.0,  refraction=1.52):
        
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection
        self.phong = phong
        self.transmission = transmission
        self.refraction = refraction
        

