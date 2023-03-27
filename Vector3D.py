

class Vector3D:

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.y})'

    def dot_product(self, vector: Vector3D) -> float:
        assert isinstance(vector, Vector3D)
        dot = self.x * vector.x + self.y * vector.y + self.z * vector.z
        return dot

