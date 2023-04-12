from Camera import Camera
from Vector3D import Vector3D
from Image import Image
from Color import Color
from Point import Point
from Sphere import Sphere
from Scene import Scene
from RenderEngine import RenderEngine
from Light import Light
from Material import Material
from Plane import Plane
from Triangle import Triangle

if __name__ == "__main__":
    width = 320
    height = 200
    camera = Camera(Point(0, 0, 0), Point(0,0,1), 50, height, width)
    objects = [Sphere(Point(0.75, -0.1, 1), 0.6, Material(Color.from_hex("#FF0000"), 0.2)),
               Sphere(Point(-0.75, -0.1, 2.25), 0.6, Material(Color.from_hex("#0000FF"))),
               Plane(Material(Color.from_hex("#FF0000"), 0.2), Point(0, 0.8, 0.2), Point(0, 0.8,0)),
               Triangle(Material(Color.from_hex("#FFFFFF"), 0.2))
               ]

    lights = [ Light(Point(1.5, -0.5, -10.0), Color.from_hex("#FFFFFF")) ]
    scene = Scene(camera, objects, lights, width, height)
    engine = RenderEngine()
    image = engine.render(scene)
    
    with open("firstImage.ppm", "w") as image_file:
        image.write_image(image_file)

