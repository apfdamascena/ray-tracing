from Image import Image
from Ray import Ray
from Point import Point
from Color import Color

class RenderEngine:

    def render(self, scene):
        width = scene.width
        height = scene.height
        camera = scene.camera

        aspect_ratio = float(width) / height
        x0 = -1.0
        x1 = +1.0
        xstep = (x1 - x0) / (width - 1)
        y0 = -1.0 / aspect_ratio
        y1 = +1.0 / aspect_ratio
        ystep = (y1 - y0) / (height - 1)

        pixels = Image(width, height)

        for j in range(height):
            y = y0 + j*ystep
            for i in range(width):
                x = x0 + i * xstep
                ray = Ray(camera.origin, Point(x,y) - camera.origin)
                pixels.set_pixel(i, j, self.ray_trace(ray, scene))
        return pixels

    def ray_trace(self, ray, scene):
        color = Color(0,0,0)
        # find the nearest object hitted by the ray
        distance_hit, object_hit = self.find_nearest(ray, scene)

        if object_hit is None:
            return color

        hit_pos = ray.origin + ray.direction * distance_hit
        hit_normal = object_hit.normal(hit_pos)
        color += self.color_at(object_hit, hit_pos, hit_normal, scene)
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
        object_color = material.color_at(hit_pos)
        to_cam = scene.camera.origin - hit_pos
        color = material.ambient * Color.from_hex("#FFFFFF")
        specular_k = 50
        
        #light calculations
        for light in scene.lights:
            to_light = Ray(hit_pos, light.position - hit_pos)
            ## diffuse shadding (Lambert)
            color += (object_color * material.diffuse * max(normal.dot_product(to_light.direction), 0))

            # specular shading (blinn-phong)
            half_vector = (to_light.direction + to_cam).normalize()
            color += light.color * material.specular * max(normal.dot_product(half_vector), 0) ** specular_k

        return color




