from Object import Object
from Material import Material
from Point import Point
from Vector3D import Vector3D
from Ray import Ray
from Plane import Plane


class Triangle(Object):

    def __init__(self, material: Material, a=Point(0.14, -0.1, 1.61), b=Point(-0.75, 0.9, 1.6), c=Point(-0.751, -0.11, 1.62)):
        super().__init__(material)

        self.a = a
        self.b = b
        self.c = c

        c_to_a = self.c - self.a
        b_to_a = self.b - self.a
        self._normal = c_to_a.cross_product(b_to_a).normalize()

        self.distance = self._normal.dot_product(self.a)

    def normal(self, surface_point):
        return self._normal

    def intersect(self, ray):
        dot = ray.direction.dot_product(self._normal)

        if dot == 0:
            return None

        dummy = (self._normal.dot_product(ray.origin + (self._normal * self.distance) ) * -1)
        dist_to_triangle = -1 * dummy / dot

        q = ray.direction * dist_to_triangle + ray.origin

        c_to_a = self.c - self.a
        qa = q - self.a

        bc = self.b - self.c
        qc = q - self.c

        ab = self.a - self.b
        qb = q - self.b

        inside = c_to_a.cross_product(qa).dot_product(self._normal) >= 0 and \
                    bc.cross_product(qc).dot_product(self._normal) >= 0 and \
                    ab.cross_product(qb).dot_product(self._normal) >= 0

        if inside:
            return dist_to_triangle
        else:
            return None