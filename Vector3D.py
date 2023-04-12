from __future__ import annotations
import math

class Vector3D:

    def __init__(self, x=0.0, y=0.0, z=0.0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.y})'

    def dot_product(self, vector: Vector3D) -> float:
        assert isinstance(vector, Vector3D)
        dot = self.x * vector.x + self.y * vector.y + self.z * vector.z
        return dot

    def cross_product(self, other: Vector3D) -> Vector3D:
        return self.__class__(
            self.y*other.z - self.z*other.y,
            self.z*other.x - self.x*other.z,
            self.x*other.y - self.y*other.x
        )

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.dot_product(self))

    def normalize(self) -> float:
        return self / self.magnitude

    def __add__(self, vector: Vector3D) -> Vector3D:
        return self.__class__(self.x + vector.x, self.y + vector.y, self.z + vector.z)

    def __sub__(self, vector: Vector3D) -> Vector3D :
        return self.__class__(self.x - vector.x, self.y - vector.y, self.z - vector.z)

    def __mul__(self, const: float) -> Vector3D:
        return self.__class__(self.x * const, self.y * const, self.z * const)

    def __rmul__(self, const: float) -> Vector3D:
        return self.__mul__(const)

    def __truediv__(self, const: float) -> Vector3D:
        return self.__class__(self.x / const, self.y / const, self.z / const)
