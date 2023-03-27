from Vector3D import Vector3D
from Image import Image
from Color import Color

if __name__ == "__main__":
    width = 320
    height = 200
    
    image = Image(width, height)

    with open("firstImage.ppm", "w") as image_file:
        image.write_image(image_file)

