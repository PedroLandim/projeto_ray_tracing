from components import Vector3

class Camera:
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


