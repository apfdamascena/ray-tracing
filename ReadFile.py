from Color import Color
from Sphere import Sphere
from Plane import Plane
from Material import Material
from Point import Point
from Camera import Camera
from Light import Light
from Triangle import TriangleMesh
import asyncio

## need refactoring the way of read file

class ReaderFile:

    def read(self, path: str):
        objects = {}
        objects["objects-3d"] = []
        objects["lights"] = []

        with open(path, 'r') as file:
            lines = [ line.strip().split() for line in file.readlines()]
            
            index = 0
            while index < len(lines):
                object_info = lines[index]
                object_to_create = object_info[0]

                if object_to_create == "s":
                    info = [float(value) for value in object_info[1::]]

                    center = Point(info[0], info[1], info[2])
                    radius = info[3]
                    
                    color = Color(info[4]/255.0, info[5]/255.0, info[6]/255.0)
                    kd, ks, ka, kr, kt, p = info[7::]
                    material = Material(color, ka, kd, ks, roughness=p)
                    objects["objects-3d"].append(Sphere(center, radius, material))

                if object_to_create == "c":
                    info = [float(value) for value in object_info[1::]]
                    hres = int(info[0])
                    vres = int(info[1])
                    d = info[2]
                    up = Point(info[3], info[4], info[5])
                    center = Point(info[6], info[7], info[8])
                    point = Point(info[9], info[10], info[11])
                    objects["width"] = hres
                    objects["height"] = vres
                    objects["camera"] = Camera(center, point, d, vres, hres, up)

                if object_to_create == "a":
                    info = [float(value) for value in object_info[1::]]
                    ambient_color = Color(info[0]/255.0, info[1]/255.0, info[2]/255.0)
                    objects["ambient_color"] = ambient_color

                if object_to_create == "p":
                    info = [float(value) for value in object_info[1::]]
                    point = Point(info[0], info[1], info[2])
                    normal = Point(info[3], info[4], info[5])
                    color = Color(info[6]/255.0, info[7]/255.0, info[8]/255.0)
                    kd, ks, ka, kr, kt, p = info[9::]
                    material = Material(color, ka, kd, ks, roughness=p)
                    objects["objects-3d"].append(Plane(material, point, normal))

                if object_to_create == "l":
                    info = [float(value) for value in object_info[1::]]
                    position = Point(info[0], info[1], info[2])
                    color = Color(info[3]/255.0, info[4]/255.0, info[5]/255.0)
                    objects["lights"].append(Light(position, color))

                
                if object_to_create == "t":
                    info = [float(value) for value in object_info[1::]]
                    
                    nt = int(info[0])
                    nv = int(info[1])

                    vertices = []
                    index += 1

                    for i in range(nv):
                        vertice_info = lines[index + i]
                        x,y,z = [float(value) for value in vertice_info]
                        point = Point(x, y, z)
                        vertices.append(point)
                    index += nv

                    indices = []
                    for i in range(nt):
                        indices_info = lines[index + i]
                        a, b, c = map(int, indices_info)
                        indices.append((a-1, b-1, c-1))
                    index += nt
                    
                    values = [ float(value) for value in lines[index]]
                    color = Color(values[0]/255.0, values[1]/255.0, values[2]/255.0)

                    kd, ks, ka, kr, kt, p = values[3::]

                    material = Material(color, ka, kd, ks, roughness=p)

                    objects["objects-3d"].append(TriangleMesh(material, vertices, indices))

                index += 1
        return objects


if __name__ == "__main__":
    reader = ReaderFile()
    info = reader.read("./input.txt")