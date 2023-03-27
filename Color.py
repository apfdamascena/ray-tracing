from Vector3D import Vector3D

class Color(Vector3D):

    @classmethod
    def from_hex(cls, hex_color: str="#000000"):
        x = int(hex_color[1:3], 16) / 255.0
        y = int(hex_color[3:5], 16) / 255.0
        z = int(hex_color[5:7], 16) / 255.0
        return cls(x, y, z)