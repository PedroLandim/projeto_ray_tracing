from __future__ import annotations
import math

class Vector3:
    def __init__(self, x=0, y=0, z=0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"
    
    @classmethod
    def fromHex(cls, hex="#000000"):
        """Creates Color from hexcode"""
        x = int(hex[1:3], 16) / 255.0
        y = int(hex[3:5], 16) / 255.0
        z = int(hex[5:], 16) / 255.0
        return cls(x, y, z)
    
    @classmethod
    def fromRGB(cls, r=0, g=0, b=0):
        """Creates Color from RGB"""
        return cls(r / 255, g / 255, b / 255)


    def kron(self, othervector: Vector3) -> Vector3:
        assert isinstance(othervector, Vector3)
        return Vector3(self.x * othervector.x, self.y * othervector.y, self.z * othervector.z)

    def dotProduct(self, othervector: Vector3) -> float:
        assert isinstance(othervector, Vector3)
        return self.x * othervector.x + self.y * othervector.y + self.z * othervector.z

    def crossProduct(self, othervector: Vector3) -> Vector3:
        assert isinstance(othervector, Vector3)
        return Vector3(self.y*othervector.z - self.z*othervector.y,
                        self.z*othervector.x - self.x*othervector.z,
                        self.x*othervector.y - self.y*othervector.x)

    def magnitude(self) -> float:
        return math.sqrt(self.dotProduct(self))
    
    def normalize(self) -> Vector3:
        return self / self.magnitude()
    
    def __add__(self, othervector: Vector3) -> Vector3:
        assert isinstance(othervector, Vector3)
        return Vector3(self.x + othervector.x, self.y + othervector.y, self.z + othervector.z)
    
    def __sub__(self, othervector: Vector3) -> Vector3:
        assert isinstance(othervector, Vector3)
        return Vector3(self.x - othervector.x, self.y - othervector.y, self.z - othervector.z)
    
    def __neg__(self) -> Vector3:
        return Vector3(-self.x, -self.y, -self.z)

    def __xor__(self, othervector: Vector3) -> float:
        assert isinstance(othervector, Vector3)
        return self.dotProduct(othervector)

    def __mul__(self, number: float) -> float:
        return Vector3(self.x * number, self.y * number, self.z * number)

    def __rmul__(self, number: float) -> float:
        return self.__mul__(number)

    def __eq__(self, othervector: Vector3) -> bool:
        assert isinstance(othervector, Vector3)
        return self.x == othervector.x and self.y == othervector.y and self.z == othervector.z

    def __truediv__(self, number: float) -> Vector3:
        number = number or 1
        return Vector3(self.x / number, self.y / number, self.z / number)
    
    def __floordiv__(self, number: float) -> Vector3:
        number = number or 1
        return Vector3(self.x // number, self.y // number, self.z // number)
    
    def to_rgb(self) -> Vector3:
        return self*255 // max(self.x, self.y, self.z, 1)
    
    def transform(self, matrix):
        return 






