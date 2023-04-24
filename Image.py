from Color import Color


class Image:

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        self.__createPixels()

    def __createPixels(self):
        self.pixels = [[None for _ in range(self.width)] for _ in range(self.height)] 


    def set_pixel(self, x: int, y: int, color: Color):
        self.pixels[y][x] = color

    def write_image(self, image_file):
        image_file.write(f"P3 {self.width} {self.height}\n255\n")
        for row in self.pixels:
            for color in row:
                x = self.to_byte(color.x)
                y = self.to_byte(color.y)
                z = self.to_byte(color.z)

                image_file.write(f"{x} {y} {z} ")
            image_file.write("\n")

    def to_byte(self, color: float) -> float:
        return round(max(min(color * 255, 255), 0))