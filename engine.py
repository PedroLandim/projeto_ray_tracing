from components import Vector3, Ray, Object3D, Image, Scene
from random import random
import math

class EngineRender:
    MINIMAL_DISPLACE = 0.001

    def render(self, scene: Scene, progress: bool = False) -> Image:
        width = scene.width
        height = scene.height
        camera = scene.camera
        pixel_size = 0.1
        focal_distance = camera.focal_distance
        focus = camera.focus
        target = camera.target
        up_vector = camera.up_vector

        w = (focus - target).normalize()
        u = up_vector.crossProduct(w).normalize()
        v = w.crossProduct(u).normalize()
        z_vector = focus - focal_distance * w
        y_vector = (height / 2) * v
        x_vector = (width / 2) * u

        image_center = z_vector + pixel_size * (y_vector - x_vector)
        pixels = Image(width, height)
        for y in range(height):
            for x in range(width):
                position = image_center + pixel_size * (x * u - y * v)
                ray_direction = position - focus
                ray = Ray(focus, ray_direction)
                pixels.set_pixel(x, y, self.rayTrace(ray, scene))
            if progress:
                print(f"{(y / height) * 100:.2f}%", end="\r")
        return pixels

    def rayTrace(self, ray: Ray, scene: Scene, depth=0) -> Vector3:
        color = Vector3()
        distace_hit, normal_hit, object_hit = self.findNearest(ray, scene)
        if object_hit is None:
            return scene.background_color
        hit_position = ray.origin + ray.direction * distace_hit
        color += self.color_at(object_hit, hit_position, normal_hit, scene)
        if depth < scene.max_depth:
            material_hit = object_hit.material
            if material_hit.reflection > 0:
                omega = -ray.direction
                normal = normal_hit
                if omega ^ normal < 0:
                    normal = -normal
                new_pos = hit_position + normal * self.MINIMAL_DISPLACE
                new_dir = ray.direction - 2 * ray.direction.dotProduct(normal) * normal
                new_ray = Ray(new_pos, new_dir)
                color += self.rayTrace(new_ray, scene, depth + 1) * material_hit.reflection

            if material_hit.refraction > 0:
                omega = -ray.direction
                normal = normal_hit
                relative_refraction = material_hit.refraction

                if omega ^ normal < 0:
                    relative_refraction = 1/material_hit.refraction
                    normal = -normal
                
            delta = 1-(1/(relative_refraction**2) * (1-(normal ^omega)**2))

            if delta >= 0:
                inverse_refra = 1 / relative_refraction
                new_dir = -inverse_refra * omega - (math.sqrt(delta) - inverse_refra * (normal ^omega)) * normal
                new_pos = hit_position - normal * self.MINIMAL_DISPLACE
                new_ray = Ray(new_pos, new_dir)

                color += self.rayTrace(new_ray, scene, depth +1) * material_hit.transmission
            else:
                new_pos = hit_position + normal *self.MINIMAL_DISPLACE
                new_dir = ray.direction - 2 * ray.direction.dotProduct(normal) * normal
                new_ray = Ray(new_pos, new_dir)

                color += self.rayTrace(new_ray, scene, depth +1) * material_hit.transmission

        return color
    
    def findNearest(self, ray: Ray, scene: Scene) -> "tuple[float, Vector3, Object3D] | tuple[None, None, None]":
        minimum_distance = None
        object_hit = None
        minimum_normal = None
        for obj in scene.objects:
            distance, normal = obj.intersects(ray)
            if distance is not None and (object_hit is None or distance < minimum_distance):
                minimum_distance = distance
                object_hit = obj
                minimum_normal = normal
        return minimum_distance, minimum_normal, object_hit

    def color_at(
            self, object_hit: Object3D, hit_position: Vector3,
            normal: Vector3, scene: Scene) -> Vector3:
        
        to_camera = (scene.camera.focus - hit_position).normalize()
        material = object_hit.material
        color = material.ambient * (material.color.kron(scene.ambient_light))
        for light in scene.lights:
            to_light = Ray(hit_position, light.origin - hit_position)
            distace_hit, normal_hit, object_hit = self.findNearest(to_light, scene)
            if object_hit is not None and 0 < distace_hit < to_light.direction ^ (light.origin - hit_position):
                continue
        
            color += material.color.kron(light.color) \
                * material.diffuse \
                * max(normal ^ to_light.direction, 0)

            half_vector = 2 * (normal ^ to_light.direction) * normal - to_light.direction

            color += light.color * material.specular \
                * max(half_vector ^ to_camera, 0) ** material.phong

        return color
                

            



