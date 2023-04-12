from Point import Point
from Vector3D import Vector3D


class Camera:
  def __init__(self, origin: Point, scene_center: Point,
  screen_distance: float, screen_height: int, screen_width: int,
   vector_up: Vector3D = Vector3D(0,1,0)):
    self.origin = origin
    self.scene_center = scene_center
    self.vector_up = vector_up
    self.screen_distance = screen_distance
    self.screen_height = screen_height
    self.screen_width = screen_width
    self.orthogonal_vectors()


  def orthogonal_vectors(self):
    self.w: Vector3D = (self.origin - self.scene_center).normalize()
    self.u: Vector3D = (self.vector_up.cross_product(self.w)).normalize()
    self.v: Vector3D = self.w.cross_product(self.u)

