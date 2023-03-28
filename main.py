from Vector3D import Vector3D
from Image import Image
from Color import Color
from Point import Point
from Sphere import Sphere
from Scene import Scene
from RenderEngine import RenderEngine
from Light import Light
from Material import Material


if __name__ == "__main__":
    width = 320
    height = 200
    camera = Vector3D(0, 0, -1)
    objects = [Sphere(Point(0,0,0), 0.5, Material(Color.from_hex("#FF0000")))]
    lights = [Light(Point(1.5, -0.5, -10.0), Color.from_hex("#FFFFFF"))]
    scene = Scene(camera, objects, lights, width, height)
    engine = RenderEngine()
    image = engine.render(scene)
    
    with open("firstImage.ppm", "w") as image_file:
        image.write_image(image_file)

