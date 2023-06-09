from math import sqrt
from Object import Object
from Ray import Ray

class Sphere(Object):

    def __init__(self, center, radius, material):
        super().__init__(material)
        self.center = center
        self.radius = radius

    def intersect(self, ray: Ray):
        sphere_to_ray = ray.origin - self.center
        #a = 1
        b = 2 * ray.direction.dot_product(sphere_to_ray)
        c = sphere_to_ray.dot_product(sphere_to_ray) - self.radius*self.radius
        discriminant = b * b - 4 * c

        if discriminant >= 0:
            dist = (-b - sqrt(discriminant))/2
            if dist > 0:
                return dist
        return None

    def normal(self, surface_point):
        return (surface_point - self.center).normalize()