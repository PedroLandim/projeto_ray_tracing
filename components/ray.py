from components import Vector3

class Ray:
    def __init__(self, origin: Vector3, direction: Vector3) -> None:
        self.origin = origin
        self.direction = direction.normalize()

    def __str__(self) -> str:
        return f"Ray: (Origin: {self.origin}, Direction: {self.direction})"
    

