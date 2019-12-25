def invChanels(image):
  image[...,:3] = image[...,(2, 1, 0)]
  return image