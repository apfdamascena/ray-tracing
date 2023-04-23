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

        self.distance = self._normal.dot_product(self.a)

    def normal(self, surface_point):
        return self._normal

    def intersect(self, ray: Ray):
        h = ray.direction.cross_product(self.c_to_a)
        d = self.b_to_a.dot_product(h)

        if -0.001 < d < 0.001:
            return None, None

        f = 1/d
        s = ray.origin - self.a
        u = f * (s.dot_product(h))

        if u < 0 or u > 1:
            return None, None

        q = s.cross_product(self.b_to_a)
        v = f * (ray.direction.dot_product(q))
        if v < 0 or u + v > 1:
            return None, None
        
        t = f * (self.c_to_a.dot_product(q))
        if t > 0.001:
            return t, self.getNormal(ray)
        return None, None

        
    def getNormal(self, ray: Ray):
        normal = self._normal
        omega = -ray.direction
        if normal.dot_product(omega) < 0:
            normal = -self._normal
        return normal
        
        # dot = ray.direction.dot_product(self._normal)

        # if dot == 0:
        #     return None

        # dummy = (
        #     self._normal.dot_product(ray.origin + (self._normal * self.distance)) * -1
        # )
        # dist_to_triangle = -1 * dummy / dot

        # q = ray.direction * dist_to_triangle + ray.origin

        # c_to_a = self.c - self.a
        # qa = q - self.a

        # bc = self.b - self.c
        # qc = q - self.c

        # ab = self.a - self.b
        # qb = q - self.b

        # inside = (
        #     c_to_a.cross_product(qa).dot_product(self._normal) >= 0
        #     and bc.cross_product(qc).dot_product(self._normal) >= 0
        #     and ab.cross_product(qb).dot_product(self._normal) >= 0
        # )

        # if inside:
        #     return dist_to_triangle
        # else:
        #     return None


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
        hit_normal = None
        for triangle in self.triangles:
            # vertecies = (
            #     self.list_vertices[triangle_data[0]],
            #     self.list_vertices[triangle_data[1]],
            #     self.list_vertices[triangle_data[2]]
            # )
            # triangle = Triangle(*vertecies, self.material)
            distance, normal = triangle.intersect(ray)
            if distance is not None and (distance_min is None or distance < distance_min):
                distance_min = distance
                hit_normal = normal

        return distance_min, hit_normal
        # closest_intersection = None

        # for triangle in self.triangles:
        #     distance = triangle.intersect(ray)
        #     if distance is not None and (
        #         closest_intersection is None or distance < closest_intersection
        #     ):
        #         closest_intersection = distance

        # return closest_intersection

    def normal(self, surface_point) -> Vector3D:
        closest_triangle = None
        closest_distance = float("inf")

        for triangle in self.triangles:
            distance = triangle.intersect(
                Ray(surface_point, triangle.normal(surface_point))
            )
            if distance is not None and distance < closest_distance:
                closest_distance = distance
                closest_triangle = triangle

        return closest_triangle.normal(surface_point)
