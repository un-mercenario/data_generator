from .classes import Transform
from .classes import Element
from .utils import rotateBound

import cv2
import numpy as np
from .constants import Rotation, Flip

class RotateElement(Transform):
  def __init__(self, mode:Rotation = Rotation.random, min = 0, max = 0):
    self.mode = mode
    if(self.mode == Rotation.upside_down):
      self.angles = [0, 180]
    elif(self.mode == Rotation.ninety):
      self.angles = [0, 90, 180, 270]
    else:
      self.angles = [min, max]

  def __call__(self, element: Element) -> Element:
    assert element, "Element cannot be None"

    if(self.mode == Rotation.upside_down or self.mode == Rotation.ninety):
      angle = np.random.choice(self.angles)
    else:
      angle = np.random.uniform(
        low = self.angles[0],
        high = self.angles[1],
      )

    element.image = rotateBound(element.image, angle)

    return element


class FlipElement(Transform):
  def __init__(self, mode:Flip = Flip.random):
    self.mode = mode

  def __call__(self, element: Element) -> Element:
    assert element, "Element cannot be None"

    if(self.mode == Flip.x):
      dir = 0
    elif(self.mode == Flip.y):
      dir = 1
    else:
      dir = np.random.randint(low=0, high=2)

    if(np.random.randint(low=0, high=2) == 0): # Flip if 0
      element.image = cv2.flip(element.image, dir)

    return element