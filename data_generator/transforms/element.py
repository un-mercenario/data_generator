import numpy as np
from dataclasses import dataclass


@dataclass
class Element:
    name: str = ""
    image: np.array = None
    objects: [] = None
    x: int = None
    y: int = None
    tags: {} = {}

