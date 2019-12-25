import numpy as np

class Element:
  name: str
  image: np.array
  objects: []
  x: int
  y: int
  tags: {}

  # parent
  def __init__(self, image, objects = None, name = None):
    self.name = name if name is not None else ""
    self.image = image
    self.objects = objects if objects is not None else []
    self.x = 0
    self.y = 0

class Transform(): # Abstract class
  pass
