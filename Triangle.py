from Object import Object
from Material import Material
from Point import Point
from Vector3D import Vector3D
from Ray import Ray
from Plane import Plane

class Triangle(Object):
    def __init__(
        self,
        material: Material,
        a: Point,
        b: Point,
        c: Point
    ):
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

    def intersect(self, ray: Ray) -> float:
        dot = ray.direction.dot_product(self._normal)

        if dot == 0:
            return None

        dummy = (
            self._normal.dot_product(ray.origin + (self._normal * self.distance)) * -1
        )
        dist_to_triangle = -1 * dummy / dot

        q = ray.direction * dist_to_triangle + ray.origin

        c_to_a = self.c - self.a
        qa = q - self.a

        bc = self.b - self.c
        qc = q - self.c

        ab = self.a - self.b
        qb = q - self.b

        inside = (
            c_to_a.cross_product(qa).dot_product(self._normal) >= 0
            and bc.cross_product(qc).dot_product(self._normal) >= 0
            and ab.cross_product(qb).dot_product(self._normal) >= 0
        )

        if inside:
            return dist_to_triangle
        else:
            return None


class TriangleMesh(Object):
    def __init__(self, material: Material, vertices: list[Point], indices: list[tuple[int, int, int]]):
        super().__init__(material)

        self.triangles = [
            Triangle(material, vertices[i], vertices[j], vertices[k])
            for i, j, k in indices
        ]
        self.vertices = vertices
        self.indices = indices

    def intersect(self, ray: Ray) -> float:
        closest_intersection = None

        for triangle in self.triangles:
            distance = triangle.intersect(ray)
            if distance is not None and (
                closest_intersection is None or distance < closest_intersection
            ):
                closest_intersection = distance

        return closest_intersection

    def get_mesh(self) -> list[tuple[float, float, float]]:
        mesh = []

        for triangle in self.triangles:
            a = triangle.a.to_tuple()
            b = triangle.b.to_tuple()
            c = triangle.c.to_tuple()

            mesh.extend([a, b, c])

        return mesh
