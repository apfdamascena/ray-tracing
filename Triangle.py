from Object import Object
from Material import Material
from Point import Point
from Vector3D import Vector3D
from Ray import Ray

##https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-polygon-mesh/ray-tracing-polygon-mesh-part-2.html
class Triangle(Object):
    def __init__(self, material: Material, a: Point, b: Point, c: Point):
        super().__init__(material)

        self.a = a
        self.b = b
        self.c = c

        self.b_to_a = self.b - self.a
        self.c_to_a = self.c - self.a
        
        self._normal = self.b_to_a.cross_product(self.c_to_a).normalize()

    def normal(self, surface_point):
        return self._normal

    def intersect(self, ray: Ray):
        h = ray.direction.cross_product(self.c_to_a)
        d = self.b_to_a.dot_product(h)

        if -0.001 < d < 0.001:
            return None

        f = 1/d
        s = ray.origin - self.a
        u = f * (s.dot_product(h))

        if u < 0 or u > 1:
            return None

        q = s.cross_product(self.b_to_a)
        v = f * (ray.direction.dot_product(q))
        if v < 0 or u + v > 1:
            return None
        
        t = f * (self.c_to_a.dot_product(q))
        if t > 0.001:
            return t
        return None
    
class TriangleMesh(Object):
    def __init__(
        self,
        material,
        vertices,
        indices
    ):
        super().__init__(material)

        self.triangles = [
            Triangle(material, vertices[i], vertices[j], vertices[k])
            for i, j, k in indices
        ]

        self.vertices = vertices
        self.indices = indices

    def intersect(self, ray: Ray):
        distance_min = None
        for triangle in self.triangles:
            distance = triangle.intersect(ray)
            if distance is not None and (distance_min is None or distance < distance_min):
                distance_min = distance
                self.min_triangle = triangle

        return distance_min
 

    def normal(self, surface_point) -> Vector3D:
        return self.min_triangle.normal(surface_point)
