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

        z_vector = camera.origin - camera.screen_distance * camera.w
        y_vector = (height / 2) * camera.v
        x_vector = (width / 2 ) * camera.u
        image_center = z_vector + 0.4 *(y_vector - x_vector)

        pixels = Image(width, height)

        for j in range(height):
            for i in range(width):
                position = image_center + 0.4 * (camera.u * i - j * camera.v)
                direction = (position - camera.origin).normalize()
                ray = Ray(camera.origin, direction)
                pixels.set_pixel(i, j, self.ray_trace(ray, scene))
        return pixels

    def ray_trace(self, ray, scene, depth=0):
        color = Color(0,0,0)
        # find the nearest object hitted by the ray
        distance_hit, object_hit = self.find_nearest(ray, scene)

        if object_hit is None:
            return scene.ambient_color

        hit_pos = ray.origin + ray.direction * distance_hit
        hit_normal = object_hit.normal(hit_pos)

        color += self.color_at(object_hit, hit_pos, hit_normal, scene)

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

    def find_nearest(self, ray, scene):
        distance_min, object_hit = None, None
        for obj in scene.objects:
            dist = obj.intersect(ray)
            if dist is not None and (object_hit is None or dist < distance_min):
                distance_min = dist
                object_hit = obj
        return (distance_min, object_hit)

    def color_at(self, object_hit, hit_pos, normal, scene):
        material = object_hit.material
        to_cam = (scene.camera.origin - hit_pos).normalize()
        object_color = material.color_at(hit_pos)
        color = material.ambient * (object_color.kron_product(scene.ambient_color))
        phong = 50
   
        #light calculations
        for light in scene.lights:
            to_light = Ray(hit_pos, light.position - hit_pos)

            distance_hit, object_hit = self.find_nearest(to_light, scene)
            distance = to_light.direction.dot_product((light.position - hit_pos))

            if object_hit != None and 0 < distance_hit < distance:
                continue
            ## diffuse shadding (Lambert)

            color += object_color.kron_product(light.color) * material.diffuse * max(normal.dot_product(to_light.direction), 0)
            # specular shading (blinn-phong)
            # half_vector = 2 * (to_light.direction + to_cam).normalize()
            half_vector = 2 * (normal.dot_product(to_light.direction)) * normal - to_light.direction
            color += light.color * material.specular * max(half_vector.dot_product(to_cam), 0) ** 5

        return color




