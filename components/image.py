from components import Vector3
from io import TextIOWrapper

class Image:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.pixels = [[Vector3() for _ in range(width)] for _ in range(height)]

    def set_pixel(self, x, y, vector: Vector3) -> None:
        self.pixels[y][x] = vector

    def write_ppm(self, image_file: TextIOWrapper) -> None:
        image_file.write(f"P3 {self.width} {self.height}\n255\n")
        for line in self.pixels:
            for pixel in line:
                pixel_rgb = pixel.to_rgb()
                image_file.write(f"{pixel_rgb.x} {pixel_rgb.y} {pixel_rgb.z} ")

            image_file.write("\n")

