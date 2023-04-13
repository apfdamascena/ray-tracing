from Color import Color
from Sphere import Sphere
from Plane import Plane
from Material import Material
from Point import Point
from Camera import Camera
from Light import Light
from Triangle import TriangleMesh

objects = []

with open('input.txt', 'r') as file:
    for line in file:
        values = line.split()
        if values[0] == 's':
            center = Point(float(values[1]), float(values[2]), float(values[3]))
            radius = float(values[4])
            color = Color(float(values[5]), float(values[6]), float(values[7]))
            kd, ks, ka, kr, kt, p = map(float, values[8:])
            material = Material(color, ka, kd, ks, roughness=p)
            objects.append(Sphere(center, radius, material))

        elif values[0] == 'p':
            point = Point(float(values[1]), float(values[2]), float(values[3]))
            normal = Point(float(values[4]), float(values[5]), float(values[6]))
            color = Color(float(values[7]), float(values[8]), float(values[9]))
            kd, ks, ka, kr, kt, p = map(float, values[10:])
            material = Material(color, ka, kd, ks, roughness=p)
            objects.append(Plane(material, point, normal))

        elif values[0] == 'c':
            hres = int(values[1])
            vres = int(values[2])
            d = float(values[3])
            up = Point(float(values[4]), float(values[5]), float(values[6]))
            center = Point(float(values[7]), float(values[8]), float(values[9]))
            point = Point(float(values[10]), float(values[11]), float(values[12]))
            objects.append(Camera(point, center, d, vres, hres, up))

        elif values[0] == 'l':
            position = Point(float(values[1]), float(values[2]), float(values[3]))
            color = Color(float(values[4]), float(values[5]), float(values[6]))
            objects.append(Light(position, color))

        elif values[0] == 't' or values[0].isnumeric():
            nt = int(values[1])
            nv = int(values[2])

            vertices = []
            for i in range(nv):
                x, y, z = map(float, file.readline().split())
                vertices.append(Point(x, y, z))

            indices = []
            for i in range(nt):
                a, b, c = map(int, file.readline().split())
                indices.append((a, b, c))

            if len(values) > 3:

                color = Color(float(values[0]), float(values[1]), float(values[2]))
                kd, ks, ka, kr, kt, p = map(float, values[3:])
                material = Material(color, ka, kd, ks, roughness=p)

                objects.append(TriangleMesh(material, vertices, indices))

print(objects)
