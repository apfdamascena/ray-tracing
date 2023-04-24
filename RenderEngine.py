from Image import Image
from Ray import Ray
from Point import Point
from Color import Color
from math import sqrt

class RenderEngine:

    def render(self, scene):
        width = scene.width
        height = scene.height
        camera = scene.camera

        pixel_length = 0.4

        z_vector = camera.origin - camera.screen_distance * camera.w
        y_vector = (height / 2) * camera.v
        x_vector = (width / 2 ) * camera.u
        image_center = z_vector + pixel_length * (y_vector - x_vector)

        pixels = Image(width, height)

        for j in range(height):
            for i in range(width):
                position = image_center + pixel_length * (camera.u * i - j * camera.v)
                direction = (position - camera.origin).normalize()
                ray = Ray(camera.origin, direction)
                pixels.set_pixel(i, j, self.ray_trace(ray, scene))
        return pixels

    def ray_trace(self, ray, scene, depth=0):

        # find the nearest object hitted by the ray
        distance_hit, object_hit = self.find_nearest(ray, scene)
        color = Color(0,0,0)

        if object_hit is None:
            return scene.ambient_color
            
        hit_pos = ray.origin + ray.direction * distance_hit
        hit_normal = object_hit.normal(hit_pos)

        color += self.color_at(object_hit, hit_pos, hit_normal, scene)

        if depth < scene.end_depth:
            material_hitted = object_hit.material
            if material_hitted.reflection > 0:
                omega = -ray.direction
                normal = normal_hit

                normal = -normal if omega ^ normal < 0 else normal

                new_ray_position = hit_pos + normal * 0.001
                new_ray_direction = ray.direction - 2 * ray.direction.dot_product(normal) * normal
                new_ray = Ray(new_ray_position, new_ray_direction)
                color += self.ray_trace(new_ray, scene, depth + 1) * material_hitted.reflection

            if material_hitted.refraction > 0:
                omega = -ray.direction
                normal = normal_hit
                relative_refraction = material_hitted.refraction

                relative_refraction = 1/material_hitted.refraction if omega ^ normal < 0 else relative_refraction
                normal = -normal if omega ^ normal < 0 else normal
                
            variation = 1-(1/(relative_refraction**2) * (1-(normal ^ omega)**2))

            if variation >= 0:
                inverse_refraction = 1 / relative_refraction
                new_ray_direction = -inverse_refraction * omega - (sqrt(variation) - inverse_refraction * (normal ^omega)) * normal
                new_ray_position = hit_pos - normal * 0.001
                new_ray = Ray(new_ray_position, new_ray_direction)

                color += self.rayTrace(new_ray, scene, depth +1) * material_hitted.transmission
            else:
                new_ray_position = hit_pos + normal * 0.001
                new_ray_direction = ray.direction - 2 * ray.direction.dot_product(normal) * normal
                new_ray = Ray(new_ray_position, new_ray_direction)

                color += self.ray_trace(new_ray, scene, depth +1) * material_hitted.transmission
        return color

    def find_nearest(self, ray, scene):
        distance_min, object_hit = None, None
        for obj in scene.objects:
            dist = obj.intersect(ray)
            if self.isAnyObjectHittedAndHasBetterDistance(dist, object_hit, distance_min):
                distance_min = dist
                object_hit = obj
        return (distance_min, object_hit)

    def isAnyObjectHittedAndHasBetterDistance(self, dist, object_hit, distance_min):
        return dist is not None and (object_hit is None or dist < distance_min)

    def color_at(self, object_hit, hit_pos, normal, scene):
        material = object_hit.material
        to_cam = (scene.camera.origin - hit_pos).normalize()

        object_color = material.color_at(hit_pos)
        color = material.ambient * (object_color.kron_product(scene.ambient_color))

        #light calculations
        for light in scene.lights:
            to_light = Ray(hit_pos, light.position - hit_pos)

            distance_hit, object_hit = self.find_nearest(to_light, scene)
            distance = to_light.direction.dot_product((light.position - hit_pos))

            if self.isDiffuseAndPhongNotNeeded(object_hit, distance_hit, distance):
                continue
            ## diffuse shadding (Lambert)

            color += object_color.kron_product(light.color) * material.diffuse * max(normal.dot_product(to_light.direction), 0)
            # specular shading (blinn-phong)
            # half_vector = 2 * (to_light.direction + to_cam).normalize()
            half_vector = 2 * (normal.dot_product(to_light.direction)) * normal - to_light.direction
            color += light.color * material.specular * max(half_vector.dot_product(to_cam), 0) ** 5

        return color

    def isDiffuseAndPhongNotNeeded(self, object_hit, distance_hit, distance):
        return object_hit != None and 0 < distance_hit < distance




