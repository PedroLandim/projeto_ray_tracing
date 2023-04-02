from abc import abstractmethod
from components import Vector3, Material, Ray
import math

class Object3D:
    def __init__(self, material: Material) -> None:
        self.material = material
    
    @abstractmethod
    def intersects(self, ray: Ray) -> "tuple[float, Vector3] | tuple[None, None]":
        pass

    @abstractmethod
    def _normal(self, point: Vector3 = None) -> Vector3:
        pass

class Sphere(Object3D):
    def __init__(self, center: Vector3, radius: float, material: Material) -> None:
        super().__init__(material)
        self.center = center
        self.radius = radius
    
    def intersects(self, ray: Ray) -> "tuple[float, Vector3] | tuple[None, None]":
        sphere_to_ray = ray.origin - self.center
        b = 2 * (ray.direction ^ sphere_to_ray)
        c = (sphere_to_ray ^ sphere_to_ray) - self.radius ** 2
        delta = b ** 2 - 4 * c
        if delta >= 0:
            distance = (-b - math.sqrt(delta)) / 2
            if distance > 0.001:
                return distance, self._normal(ray.origin + ray.direction * distance)
            else:
                distance = (-b + math.sqrt(delta)) / 2
                if distance > 0.001:
                    return distance, self._normal(ray.origin + ray.direction * distance)
        return None, None
    
    def _normal(self, point: Vector3) -> Vector3:
        return (point - self.center).normalize()
    
    def transform(self, matrix):
        self.center = self.center.transform(matrix)
    
class Plane(Object3D):
    def __init__(self, point: Vector3, normal: Vector3, material: Material) -> None:
        super().__init__(material)
        self.point = point
        self.normal = normal.normalize()

    def intersects(self, ray: Ray) -> "tuple[float, Vector3] | tuple[None, None]":
        if abs(self.normal ^ ray.direction) >= 0.001:
            distance = (self.normal ^ (self.point - ray.origin)) / (self.normal ^ ray.direction)
            if distance > 0.001:
                return distance, self._normal()
        return None, None
    
    def _normal(self) -> Vector3:
        return self.normal

class Triangle(Object3D):
    def __init__(
            self, vertex_A: Vector3, vertex_B: 
            Vector3, vertex_C: Vector3, material: Material) -> None:
        
        super().__init__(material)
        self.vertex_A = vertex_A
        self.vertex_B = vertex_B
        self.vertex_C = vertex_C
        edge_A = self.vertex_B - self.vertex_A
        edge_B = self.vertex_C - self.vertex_A
        self.normal = edge_A.crossProduct(edge_B).normalize()

    def intersects(self, ray: Ray) -> "tuple[float, Vector3] | tuple[None, None]":
        edge_A = self.vertex_B - self.vertex_A
        edge_B = self.vertex_C - self.vertex_A
        h = ray.direction.crossProduct(edge_B)
        a = edge_A ^ h
        if abs(a) < 0.001:
            return None, None
        f = 1/a
        s = ray.origin - self.vertex_A
        u = f * (s ^ h)
        if u < 0 or u > 1:
            return None, None
        q = s.crossProduct(edge_A)
        v = f * (ray.direction ^ q)
        if v < 0 or u + v > 1:
            return None, None
        t = f * (edge_B ^ q)
        if t > 0.001:
            return t, self._normal()
        return None, None
    
    def _normal(self) -> Vector3:
        return self.normal

class TriangleMesh(Object3D):
    def __init__(self, vertex_A: Vector3, vertex_B: 
            Vector3, vertex_C: Vector3, material: Material):
        a = 3
