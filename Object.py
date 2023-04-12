from Material import Material
from Ray import Ray

class Object:

    def __init__(self, material: Material):
        self.material = material

    def intersect(self, ray: Ray):
        pass

    def normal(self, surface_point):
        pass 