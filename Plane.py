from Object import Object
from Material import Material
from Point import Point
from Vector3D import Vector3D
from Ray import Ray

class Plane(Object):

    def __init__(self, material: Material, point: Point, normal: Vector3D):
        super().__init__(material)
        self.point = point
        self.normal_vector = normal.normalize()

    def intersect(self, ray: Ray):
        if abs(self.normal_vector.dot_product(ray.direction)) >= 0.001:
            distance = (self.normal_vector.dot_product((self.point - ray.origin))) / (self.normal_vector.dot_product(ray.direction))
            if distance > 0.001:
                return distance
        return None

    def normal(self, surface_point):
        return self.normal_vector
