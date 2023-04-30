from __future__ import annotations
from components import Vector3, Object3D, Ray

class Camera(Object3D):
    def __init__(
            self, hr: int, vr: int, focal_distance: float, up_vector: Vector3,
            focus: Vector3, 
            target: Vector3,  pixel_size: float = 1):
        
        self.vr = vr
        self.hr = hr
        self.focal_distance = focal_distance
        self.focus = focus
        self.target = target
        self.up_vector = up_vector
        self.pixel_size = pixel_size

    def intersects(self, ray: Ray) -> tuple[float, Vector3] | tuple[None, None]:
        return None, None

    def _get_normal(self) -> Vector3:
        return None

    def transform(self, matrix: list[list[float]]) -> Object3D:
        new_target = self.target.transform(matrix)
        new_up = (self.up_vector + self.target).transform(matrix) - new_target
        return Camera(self.hr, self.vr, self.focal_distance, new_up, self.focus, new_target)


