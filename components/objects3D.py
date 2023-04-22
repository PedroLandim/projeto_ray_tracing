from __future__ import annotations
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

    @abstractmethod
    def translate(self, vector: Vector3) -> Object3D:
        pass

    @abstractmethod
    def rotate(self, vector: Vector3, angle: float) -> Object3D:
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

    def translate(self, vector: Vector3) -> Object3D:
        return Sphere(self.center + vector, self.radius, self.material)
    
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

    def translate(self, vector: Vector3) -> Object3D:
        return Plane(self.point + vector, self.normal, self.material)
    

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
        if -0.001 < a < 0.001:
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
            return t, self._normal(ray)
        return None, None
    
    def _normal(self, ray: Ray) -> Vector3:
        """Returns surface normal, same normal for any surface_point"""
        normal = self.normal
        omega = -ray.direction
        # Checks if ray is leaving the object, is so, invert normal and coefficient (air coefficient is 1)
        if normal ^ omega < 0:
            normal = -self.normal
        return normal
    
    def translate(self, vector: Vector3) -> Object3D:
        return Triangle(self.vertex_A + vector, self.vertex_B + vector, self.vertex_C + vector, self.material)

class TriangleMesh(Object3D):
    def __init__(self, list_vertices: list[Vector3], list_triangles: list[tuple[int, int, int]], material: Material) -> None:
        super().__init__(material)
        self.list_vertices = list_vertices
        self.list_triangles = list_triangles

    def intersects(self, ray: Ray) -> "tuple[float, Vector3] | tuple[None, None]":
        distance_min = None
        hit_normal = None
        for triangle_data in self.list_triangles:
            vertecies = (
                self.list_vertices[triangle_data[0]],
                self.list_vertices[triangle_data[1]],
                self.list_vertices[triangle_data[2]]
            )
            triangle = Triangle(*vertecies, self.material)
            distance, normal = triangle.intersects(ray)
            if distance is not None and (distance_min is None or distance < distance_min):
                distance_min = distance
                hit_normal = normal

        return distance_min, hit_normal

    def _normal(self, triangle: Triangle) -> Vector3:
        return triangle._normal()
    
    def translate(self, vector: Vector3) -> Object3D:
        list_new = []
        for vertex in self.list_vertices:
            list_new.append([vertex[0] + vector.x, vertex[1] + vector.y, vertex[2] + vector.z])
        return TriangleMesh(list_new, self.list_triangles, self.material)
