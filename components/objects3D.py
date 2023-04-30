from __future__ import annotations
from abc import abstractmethod
from components import Vector3, Material, Ray, LinearTransformationsMixin
import math

class Object3D(LinearTransformationsMixin):
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
    
    def transform(self, matrix: list[list[float]]) -> Object3D:
        new_center = self.center.transform(matrix)
        return Sphere(new_center, self.radius, self.material)
    
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

    
    def transform(self, matrix: list[list[float]]) -> Object3D:
        new_point = self.point.transform(matrix)
        new_normal = (self.normal + self.point).transform(matrix) - new_point
        return Plane(new_point, new_normal, self.material)

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
        return self.normal
        normal = self.normal
        omega = -ray.direction
        # Checks if ray is leaving the object, is so, invert normal and coefficient (air coefficient is 1)
        if normal ^ omega < 0:
            normal = -self.normal
        return normal
    
    def transform(self, matrix: list[list[float]]) -> Object3D:
        new_vertex_A = self.vertex_A.transform(matrix)
        new_vertex_B = self.vertex_B.transform(matrix)
        new_vertex_C = self.vertex_C.transform(matrix)
        return Triangle(new_vertex_A, new_vertex_B, new_vertex_C, self.material)

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
    
    def transform(self, matrix: list[list[float]]) -> Object3D:
        new_verticies = []
        for vertex in self.list_vertices:
            new_vertex = Vector3(*vertex).transform(matrix)
            new_verticies.append(new_vertex)
        return TriangleMesh(new_verticies, self.list_triangles, self.material)
    
    
class BezierCurve:
    def __init__(self, control_points:list[Vector3]):
        self.control_points = control_points

    def __call__(self, t: float) -> Vector3:
        n = len(self.control_points) - 1
        point = Vector3()
        for i in range(n + 1):
            binomial = math.comb(n, i)
            basis = binomial * (1 - t) ** (n - i) * t ** i
            point += basis * self.control_points[i]
        return point


class RevolutionSurface(Object3D):
    def __init__(self, control_points: list[Vector3], resolution: int, point: Vector3, vector: Vector3, material: Material):
        super().__init__(material)
        self.bezier_curve = BezierCurve(control_points)
        self.point = point
        self.vector = vector
        self.triangle_mesh = self.generate_mesh(resolution)

    def evaluate_point(self, u, v):
        """Evaluate a point on the revolution surface at (u, v)"""
        point_on_curve = self.bezier_curve(u)

        # Rotate the point around the line
        theta = math.degrees(2 * math.pi * v)
        point_on_curve.rotate(self.point, self.vector, theta)

        return point_on_curve.rotate(self.point, self.vector, theta)

    def generate_mesh(self, resolution):
        """Generate a triangle mesh for the revolution surface"""
        vertices = []
        indices = []

        # Generate the vertices and normals
        for i in range(resolution):
            u = i / (resolution - 1)
            for j in range(resolution):
                v = j / (resolution - 1)
                point = self.evaluate_point(u, v)
                vertices.append(point)

        # Generate the indices for the triangle mesh
        for i in range(resolution - 1):
            for j in range(resolution - 1):
                a = i * resolution + j
                b = i * resolution + j + 1
                c = (i + 1) * resolution + j + 1
                d = (i + 1) * resolution + j
                indices.extend([[a, b, c], [a, c, d]])

        return TriangleMesh(vertices, indices, self.material)

    def intersects(self, ray: Ray) -> "tuple[float, Vector3] | tuple[None, None]":
        return self.triangle_mesh.intersects(ray)

    def _get_normal(self, triangle: Triangle) -> Vector3:
        return self.triangle_mesh._get_normal(triangle)
