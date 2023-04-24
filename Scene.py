
from Color import Color


class Scene:

    def __init__(self, camera, objects, lights, width, height, ambient_color = Color.from_hex("#000000"), end_depth = 0):
        self.camera = camera
        self.objects = objects
        self.width = width
        self.height = height
        self.lights = lights
        self.ambient_color = ambient_color
        self.end_depth = end_depth