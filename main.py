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

async def main():

    input = ReaderFile()

    info_result = await asyncio.gather(input.read("./input.txt"))
    infos = info_result[0]

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

    image_result = await asyncio.gather(engine.render(scene))
    # image = engine.render(scene)

    with open("firstImage.ppm", "w") as image_file:
        image_result[0].write_image(image_file)





if __name__ == "__main__":

    asyncio.run(main())

    # input = ReaderFile()
    # infos = input.read("./input.txt")

    # ambient_color = Color(0, 0, 0)

    # if "ambient_color" in infos:
    #     ambient_color = infos["ambient_color"]

    # camera = infos["camera"]

    # objects = infos["objects-3d"]
    # lights = infos["lights"]
    # width = infos["width"]
    # height = infos["height"]

    # scene = Scene(camera, objects, lights, width, height, ambient_color)
    # engine = RenderEngine()

    # image = engine.render(scene)

    

    # with open("firstImage.ppm", "w") as image_file:
    #     image.write_image(image_file)

    # width = 320
    # height = 200
    # camera = Camera(Point(0, 0, 0), Point(0, 0, 1), 50, height, width)
    # objects = [
    #     Sphere(Point(0.75, -0.1, 1), 0.6, Material(Color.from_hex("#FF0000"), 0.2)),
    #     Sphere(Point(-1.5, -0.1, 2.25), 0.6, Material(Color.from_hex("#0000FF"))),
    #     Plane(
    #         Material(Color.from_hex("#FF0000"), 0.2),
    #         Point(0, 0.8, 0.2),
    #         Point(0, 0.8, 0),
    #     ),
    #     # Triangle(
    #     #     Material(Color.from_hex("#FFFFFF"), 0.2),
    #     #     a=Point(0.14, -0.1, 1.61),
    #     #     b=Point(-0.75, 0.9, 1.6),
    #     #     c=Point(-0.751, -0.11, 1.62),
    #     # ),
    #     TriangleMesh(
    #         material=Material(Color.from_hex("#FFFFFF"), 0.2),
    #         vertices=[
    #             Point(0.14, -0.1, 2.2),
    #             Point(-0.75, 0.9, 2.2),
    #             Point(-0.751, -0.11, 2.2),
    #             Point(0.5, 0.1, 2.2),
    #             Point(-0.3, 0.5, 2.2),
    #         ],
    #         indices=[
    #             (0, 1, 2),
    #             (0, 3, 4),
    #         ],
    #     ),
    # ]

    # lights = [Light(Point(1.5, -0.5, -10.0), Color.from_hex("#FFFFFF"))]

    # scene = Scene(camera, objects, lights, width, height)
    # engine = RenderEngine()

    # image = engine.render(scene)

    # with open("firstImage.ppm", "w") as image_file:
    #     image.write_image(image_file)
