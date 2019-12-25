from .classes import Transform
from .classes import Element
from .constants import Position, Resize
from . import utils
from ..common import Action

import cv2
import typing as tp
import numpy as np
import matplotlib.pyplot as plt

class Compose(Action):
  def __init__(self, actions: tp.List[Action]):
    if hasattr(actions, "__iter__"):
      self.actions = actions
    else:
      self.actions = [actions]

  def __call__(self, element: Element) -> Element:
    for system in self.actions:
      element = system(element)

    return element

class ApplyToObjects(Transform):
  def __init__(self, transforms: tp.List[Transform]):
    if hasattr(transforms, "__iter__"):
      self.transforms = transforms
    else:
      self.transforms = [transforms]

  def __call__(self, element: Element) -> Element:
    for object in element.objects:
      for system in self.transforms:
        object = system(object)
    return element

class DrawElement(Transform):
  def __call__(self, element: Element) -> Element:
    image = element.image.copy()

    img = cv2.GaussianBlur(element.objects[0].image, (7, 7), 0)
    b, g, r, a = cv2.split(img)

    cimg = element.objects[0].image.copy()
    cimg[:, :, 3] = a

    for obj in element.objects:
      image = utils.overlayTransparent(
        background=image,
        overlay=obj.image[..., :-1],
        mask=obj.image[..., -1],
        x=obj.x,
        y=obj.y,
      )

    # plt.imshow(image)
    # plt.show()
    # print("Image created")

    element.fimg = image

    return element

class RandomResize(Transform):
  def __init__(self, mode:Resize = Resize.asymmetric, wmin=None, wmax=None, hmin=None, hmax=None):
    self.wmin = wmin
    self.wmax = wmax
    self.hmin = hmin
    self.hmax = hmax
    self.mode = mode

  def __call__(self, element: Element) -> Element:
    assert element, "Element cannot be None"

    wmin = self.wmin if self.wmin is not None else element.image.shape[1]
    hmin = self.hmin if self.hmin is not None else element.image.shape[0]
    wmax = self.wmax if self.wmax is not None else element.image.shape[1]
    hmax = self.hmax if self.hmax is not None else element.image.shape[0]

    if(self.mode == Resize.symmetrich):
      h = hmin if hmin == hmax is not None else np.random.randint(
          low=hmin,
          high=hmax,
        )
      w = element.image.shape[1] * (h/element.image.shape[0])
      w = int(w)
    if(self.mode == Resize.symmetricw):
      w = wmin if wmin == wmax is not None else np.random.randint(
          low=wmin,
          high=wmax,
        )
      h = element.image.shape[0] * (w/element.image.shape[1])
      h = int(h)
    else:
      w = wmin if wmin == wmax is not None else np.random.randint(
          low=wmin,
          high=wmax,
        )

      h = hmin if hmin == hmax is not None else np.random.randint(
          low=hmin,
          high=hmax,
        )

    element.image = cv2.resize(element.image, (w, h))

    return element

# Only for element with objects
class ObjectsRandomPosition(Transform):
  def __init__(self, mode:Position = Position.random, xmin=None, xmax=None, ymin=None, ymax=None):
    self.xmin = xmin
    self.xmax = xmax
    self.ymin = ymin
    self.ymax = ymax
    self.mode = mode

  def __call__(self, element: Element) -> Element:
    assert element, "Element cannot be None"

    el_h: int = element.image.shape[0]
    el_w: int = element.image.shape[1]

    if(self.mode == Position.percentage):
      xmin = (self.xmin if self.xmin <= 1 else (self.xmin%100)/100) * el_w if self.xmin is not None else 0
      xmax = (self.xmax if self.xmax <= 1 else (self.xmax%100)/100) * el_w if self.xmax is not None else el_w
      ymin = (self.ymin if self.ymin <= 1 else (self.ymin%100)/100) * el_h if self.ymin is not None else 0
      ymax = (self.ymax if self.ymax <= 1 else (self.ymax%100)/100) * el_h if self.ymax is not None else el_h
    else:
      xmin = self.xmin if self.xmin is not None else 0
      xmax = self.xmax if self.xmax is not None else el_w
      ymin = self.ymin if self.ymin is not None else 0
      ymax = self.ymax if self.ymax is not None else el_h

    lastx, lasty = 0, 0
    for obj in element.objects:
      obj_h: int = int(obj.image.shape[0])
      obj_w: int = int(obj.image.shape[1])

      while True:
        obj.x = np.random.randint(
          low=max(0, xmin- obj_w/2) ,
          high=min(xmax, el_w),
        )

        if(obj.x > lastx + obj_w/2 or obj.x < lastx - obj_w/2):
          break

      while True:
        obj.y = np.random.randint(
          low=max(0, ymin- obj_h/2) ,
          high=min(ymax, el_h),
        )

        if(obj.y > lasty + obj_h/2 or obj.y < lasty - obj_h/2):
          break

      lastx, lasty = obj.x, obj.y

    return element

class ObjectsRandomResize(Transform):
  def __init__(self, mode:Resize = Resize.asymmetric, wmin=None, wmax=None, hmin=None, hmax=None):
    self.wmin = wmin
    self.wmax = wmax
    self.hmin = hmin
    self.hmax = hmax
    self.mode = mode

  def __call__(self, element: Element) -> Element:
    assert element, "Element cannot be None"

    el_h: int = element.image.shape[0]
    el_w: int = element.image.shape[1]

    wmin = (self.wmin if self.wmin <= 1 else (self.wmin%100)/100) * el_w if self.wmin is not None else 0
    wmax = (self.wmax if self.wmax <= 1 else (self.wmax%100)/100) * el_w if self.wmax is not None else el_w
    hmin = (self.hmin if self.hmin <= 1 else (self.hmin%100)/100) * el_h if self.hmin is not None else 0
    hmax = (self.hmax if self.hmax <= 1 else (self.hmax%100)/100) * el_h if self.hmax is not None else el_h

    rr = RandomResize(mode=Resize.symmetricw, wmin=wmin, wmax=wmax, hmin=hmin, hmax=hmax)

    for obj in element.objects:
      obj = rr(obj)

    return element

class ObjectsGetBGColor(Transform):
  def __init__(self):
    pass
  def __call__(self, element: Element) -> Element:
    for obj in element.objects:
      t = self.color_transfer(element.image, obj.image)
      obj.image = t

    return element

  def color_transfer(self, source, target):
    alpha = cv2.split(target)[3]
    # convert the images from the RGB to L*ab* color space, being
    # sure to utilizing the floating point data type (note: OpenCV
    # expects floats to be 32-bit, so use that instead of 64-bit)
    source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

    # compute color statistics for the source and target images
    (lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc) = self.image_stats(source)
    (lMeanTar, lStdTar, aMeanTar, aStdTar, bMeanTar, bStdTar) = self.image_stats(target)

    # subtract the means from the target image
    (l, a, b) = cv2.split(target)
    l -= lMeanTar
    a -= aMeanTar
    b -= bMeanTar

    # scale by the standard deviations
    l = (lStdTar / lStdSrc) * l
    a = (aStdTar / aStdSrc) * a
    b = (bStdTar / bStdSrc) * b

    # add in the source mean
    l += lMeanSrc
    a += aMeanSrc
    b += bMeanSrc

    # clip the pixel intensities to [0, 255] if they fall outside
    # this range
    l = np.clip(l, 0, 255)
    a = np.clip(a, 0, 255)
    b = np.clip(b, 0, 255)

    # merge the channels together and convert back to the RGB color
    # space, being sure to utilize the 8-bit unsigned integer data
    # type
    transfer = cv2.merge([l, a, b])
    transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)

    b_channel, g_channel, r_channel = cv2.split(transfer)
    transfer = cv2.merge((b_channel, g_channel, r_channel, alpha))

    # return the color transferred image
    return transfer

  def image_stats(self, image):
    # compute the mean and standard deviation of each channel
    (l, a, b) = cv2.split(image)
    (lMean, lStd) = (l.mean(), l.std())
    (aMean, aStd) = (a.mean(), a.std())
    (bMean, bStd) = (b.mean(), b.std())

    # return the color statistics
    return (lMean, lStd, aMean, aStd, bMean, bStd)
