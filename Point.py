from Vector3D import Vector3D


class Point(Vector3D):
    def to_tuple(self):
        return (self.x, self.y, self.z)
