from components import Vector3

class Light:
    def __init__(self, origin: Vector3, color: Vector3 = Vector3(1, 1, 1)) -> None:
        self.origin = origin
        self.color = color

    def __str__(self) -> str:
        return f"Light: (Origin: {self.origin}, Color: {self.color})"