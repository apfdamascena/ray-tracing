from Color import Color

class Material:

    def __init__(self, color = Color.from_hex("#FFFFFF"), ambient = 0.05, diffuse=1.0, specular = 1.0, reflection = 1.0, transmission = 1.0, roughness = 1.0, refraction=1.20):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection
        self.transmission = transmission
        self.roughness = roughness
        self.refraction = refraction

    def color_at(self, position):
        return self.color