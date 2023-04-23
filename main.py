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
from Triangle import Triangle, TriangleMesh
from ReadFile import ReaderFile
from AffineTransformation import rotation, translation
import asyncio

def main():

    input = ReaderFile()
    infos = input.read("./input.txt")

    ambient_color = Color(0, 0, 0)

    if "ambient_color" in infos:
        ambient_color = infos["ambient_color"]

    camera = infos["camera"]
    objects = infos["objects-3d"]
    lights = infos["lights"]
    width = infos["width"]
    height = infos["height"]

    scene = Scene(camera, objects, lights, width, height, ambient_color)
    engine = RenderEngine()

    image = engine.render(scene)

    with open("firstImage.ppm", "w") as image_file:
        image.write_image(image_file)



if __name__ == "__main__":

    main()
